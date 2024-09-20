"""
app is a wsgi application which accepts environ and start_response as argument.
Here We implement a simple flask-like api to avoid explicitly add it as dependency.
wsgiref is used to spawn a server from sqllineage commandline. To serve production traffic, you can/should put
the app behind a real production server like gunicorn or uwsgi, as app is wsgi compatible.
A simple gunicorn example: gunicorn sqllineage.drawing:app
"""

import json
import logging
import mimetypes
import os
from argparse import Namespace
from http import HTTPStatus
from pathlib import Path
from typing import Any, Callable, Dict, List
from urllib.parse import urlencode
from wsgiref.simple_server import make_server

from sqllineage import DEFAULT_DIALECT, DEFAULT_HOST, DEFAULT_PORT, STATIC_FOLDER
from sqllineage.config import SQLLineageConfig
from sqllineage.core.metadata.dummy import DummyMetaDataProvider
from sqllineage.exceptions import SQLLineageException
from sqllineage.utils.constant import LineageLevel
from sqllineage.utils.helpers import extract_sql_from_args

logger = logging.getLogger(__name__)

import os

def get_source_tables_from_sql(sql,format=False):
    from sqllineage.runner import LineageRunner
    try:
        if format:
            formatted_sql = format_sql(sql)
        else:
            formatted_sql = sql
        result = LineageRunner(formatted_sql,dialect='non-validating')
        source_tables = [str(i).split('.')[1] for i in result.source_tables]
        return source_tables
    except:
        return []

# def get_sql_from_table_name(table_name):
#     query_data = {
#         "table_name": table_name
#     }
#     response = api.post(query_data)
#     return response[0]['file_content']

def get_sql_from_table_name(table_name):
    ## 在file_path内搜索table_name.sql，返回sql
    file_path = '/home/zhengzong/workspace/DS/HiveTrace/HiveTrace/sqllineage/data/vgds/'
    table_name =  table_name+'.sql'
    ## 如果找不到，返回None，否则返回sql
    if table_name not in os.listdir(file_path):
        return None
    with open(file_path+table_name,'r') as f:
        sql = f.read()
    return sql
    

## 给定初始化的sql，获取所有的source tables，返回一个list，继续递归直到无法通过table_name找到sql,
## 把所有的sql都获取到，存在一个list里面，一开始的sql也要加进去
## 再维护一个list，存储已经获取过的table_name，避免重复获取，如果已经获取过，就不再获取

def get_all_source_tables(sql,all_sql,source_tables,level=3):
    ## 超过5层递归，返回
    if level == 0:
        return
    if sql is None:
        return 
    source_tables_ = get_source_tables_from_sql(sql)
    print(source_tables_)
    for table_name in source_tables_:
        if table_name not in source_tables:
            source_tables.append(table_name)
            sql = get_sql_from_table_name(table_name)
            all_sql.append(sql)
            get_all_source_tables(sql,all_sql,source_tables,level-1)
        
            

def combine_sql(sql_list):
    # 去掉None  
    sql_list = [i for i in sql_list if i is not None]
    # print(len(sql_list))
    # 如果最后不是分号结尾，加上分号
    for i in range(len(sql_list)):
        if sql_list[i][-1] != ';':
            sql_list[i] += ';'
    return '\n'.join(sql_list)


class SQLLineageApp:
    """ 
    SQLLineageApp: A simple flask-like wsgi application to serve static files and handle lineage requests.
    """
    def __init__(self) -> None:
        # save route path 
        self.routes: Dict[str, Callable[[Dict[str, Any]], Dict[str, Any]]] = {}
        self.root_path = Path(SQLLineageConfig.DIRECTORY)
        self.metadata_provider = DummyMetaDataProvider()

    def route(self, path: str):
        def wrapper(handler):
            self.routes[path] = handler
            return handler

        return wrapper

    def __call__(self, environ, start_response) -> List[bytes]:
        static_folder = Path(os.path.dirname(__file__)).joinpath(Path(STATIC_FOLDER))
        request_method = environ["REQUEST_METHOD"]
        path_info = environ["PATH_INFO"]
        try:
            if request_method == "GET":
                mimetype = "text/html; charset=utf-8"
                if path_info == "/":
                    static_fname = str(static_folder.joinpath(Path("index.html")))
                else:
                    if ".." in path_info:
                        # Do not allow going back to parent path of static folder
                        return self.handle_404(start_response)
                    static_file = static_folder.joinpath(Path(path_info.strip("/")))
                    if static_file.exists():
                        static_fname = str(static_file)
                        optional_mimetype = mimetypes.guess_type(path_info)[0]
                        mimetype = (
                            optional_mimetype
                            if optional_mimetype is not None
                            else mimetype
                        )
                    else:
                        return self.handle_404(start_response)
                with open(static_fname, "rb") as f:
                    text = f.read()
                return self.handle_200_text(start_response, mimetype, text)
            elif request_method == "POST":
                print("routes:", self.routes)
                if path_info in self.routes:
                    request_body_size = int(environ["CONTENT_LENGTH"])
                    request_body = environ["wsgi.input"].read(request_body_size)
                    payload = json.loads(request_body)
                    for param in ["d", "f"]:
                        if param in payload and not str(
                            Path(payload[param]).absolute()
                        ).startswith(str(Path(self.root_path).absolute())):
                            return self.handle_403(start_response)
                    data = self.routes[path_info](payload)
                    # print("data:", data)
                    return self.handle_200_json(start_response, data)
                else:
                    return self.handle_404(start_response)
            elif request_method == "OPTIONS":
                if path_info in self.routes:
                    start_response(
                        "200 OK",
                        [
                            ("Access-Control-Allow-Origin", "*"),
                            (
                                "Access-Control-Allow-Headers",
                                "Content-Type",
                            ),
                            ("Access-Control-Allow-Methods", "POST"),
                        ],
                    )
                    return []
                else:
                    return self.handle_404(start_response)
            else:
                return self.handle_405(start_response)
        except (SystemExit, IsADirectoryError, FileNotFoundError, PermissionError):
            return self.handle_404(start_response)
        except (SQLLineageException, RuntimeError) as e:
            return self.handle_400(start_response, str(e))

    @staticmethod
    def handle_200_text(start_response, mimetype, text) -> List[bytes]:
        status_code = HTTPStatus.OK
        start_response(
            f"{status_code.value} {status_code.phrase}", [("Content-type", mimetype)]
        )
        return [text]

    def handle_200_json(self, start_response, data) -> List[bytes]:
        return self.handle_json_response(start_response, HTTPStatus.OK, data)

    def handle_400(self, start_response, message) -> List[bytes]:
        return self.handle_client_error_response(
            start_response, HTTPStatus.BAD_REQUEST, message
        )

    def handle_403(self, start_response) -> List[bytes]:
        message = "File Not Allowed For Accessing"
        return self.handle_client_error_response(
            start_response, HTTPStatus.FORBIDDEN, message
        )

    def handle_404(self, start_response) -> List[bytes]:
        message = "File Not Found"
        return self.handle_client_error_response(
            start_response, HTTPStatus.NOT_FOUND, message
        )

    def handle_405(self, start_response) -> List[bytes]:
        message = "Method Not Allowed"
        return self.handle_client_error_response(
            start_response, HTTPStatus.METHOD_NOT_ALLOWED, message
        )

    def handle_client_error_response(
        self, start_response, status_code, message
    ) -> List[bytes]:
        data = {"message": message}
        return self.handle_json_response(start_response, status_code, data)

    @staticmethod
    def handle_json_response(start_response, status_code, data) -> List[bytes]:
        start_response(
            f"{status_code.value} {status_code.phrase}",
            [
                ("Content-type", "application/json"),
                ("Access-Control-Allow-Origin", "*"),
            ],
        )
        return [json.dumps(data).encode("utf-8")]


app = SQLLineageApp()


@app.route("/lineage")
def lineage(payload):
    # this is to avoid circular import
    from sqllineage.runner import LineageRunner

    req_args = Namespace(**payload)
    sql = extract_sql_from_args(req_args)
    dialect = getattr(req_args, "dialect", DEFAULT_DIALECT)
    lr = LineageRunner(
        sql, dialect=dialect, verbose=True, metadata_provider=app.metadata_provider
    )
    data = {
        "verbose": str(lr),
        "dag": lr.to_cytoscape(),
        "column": lr.to_cytoscape(LineageLevel.COLUMN),
    }
    return data

@app.route("/lineageall")
def lineage(payload):
    # this is to avoid circular import
    from sqllineage.runner import LineageRunner

    req_args = Namespace(**payload)
    sql = extract_sql_from_args(req_args)

    all_sql = []
    source_tables = []
    all_sql.append(sql)
    get_all_source_tables(sql,all_sql,source_tables)
    all_sql = [i for i in all_sql if i is not None]
    print("len of all_sql:",len(all_sql))
    if len(all_sql) > 5:
        print("len of sql:",len(all_sql[0]))
        print("len of sql_list:",len(combine_sql(all_sql[0:5])))
        sql_all_ = combine_sql(all_sql[0:5])
    else:
        sql_all_ =  combine_sql(all_sql)

    dialect = getattr(req_args, "dialect", DEFAULT_DIALECT)
    lr = LineageRunner(
        sql_all_, dialect=dialect, verbose=True, metadata_provider=app.metadata_provider
    )
    data = {
        "verbose": str(lr),
        "dag": lr.to_cytoscape(),
        "column": lr.to_cytoscape(LineageLevel.COLUMN),
    }
    print("data:",data)
    return data



@app.route("/script")
def script(payload):
    req_args = Namespace(**payload)
    sql = extract_sql_from_args(req_args)
    return {"content": sql}

@app.route("/scriptall")
def scriptall(payload):
    req_args = Namespace(**payload)
    sql = extract_sql_from_args(req_args)
    # print("SCRIPTALL:", sql)
    # 这里写递归函数，获取所有的sql
    all_sql = []
    source_tables = []
    all_sql.append(sql)
    get_all_source_tables(sql,all_sql,source_tables)
    all_sql = [i for i in all_sql if i is not None]
    print("len of all_sql:",len(all_sql))
    if len(all_sql) > 5:
        print("len of sql:",len(all_sql[0]))
        print("len of sql_list:",len(combine_sql(all_sql[0:5])))
        return {"content": combine_sql(all_sql[0:5])}
    else:
        return {"content": combine_sql(all_sql)}


@app.route("/directory")
def directory(payload):
    if payload.get("f"):
        root = Path(payload["f"]).parent
    elif payload.get("d"):
        root = Path(payload["d"])
    else:
        root = Path(SQLLineageConfig.DIRECTORY)
    data = {
        "id": str(root),
        "name": root.name,
        "is_dir": True,
        "children": [
            {"id": str(p), "name": p.name, "is_dir": p.is_dir()}
            for p in sorted(root.iterdir(), key=lambda _: (not _.is_dir(), _.name))
        ],
    }
    return data


def draw_lineage_graph(**kwargs) -> None:
    host = kwargs.pop("host", DEFAULT_HOST) 
    port = kwargs.pop("port", DEFAULT_PORT)
    querystring = urlencode({k: v for k, v in kwargs.items() if v}) # 将字典转换为url参数
    path = f"/?{querystring}" if querystring else "/" # 生成url
    if f := kwargs.get("f"): # 获取文件路径
        app.root_path = Path(f).parent # 设置文件路径
    if metadata_provider := kwargs.get("metadata_provider"): # 获取元数据
        app.metadata_provider = metadata_provider # 设置元数据
    with make_server(host, port, app) as httpd: # 启动服务 
        print(f" * SQLLineage Running on http://{host}:{port}{path}") # 打印服务地址
        httpd.serve_forever()  # 服务一直运行
