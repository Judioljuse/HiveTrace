# -*- encoding: utf-8 -*-
'''
https://cooper.didichuxing.com/knowledge/share/book/YcSAIftpNcle/2199608760908

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    ----------------------
2023-05-10         Pengjiandong  1.0      For data-service-sdk
'''
#pylint: skip-file
import time
import requests
import base64
import hmac
import json
from hashlib import sha256
from voydstools.common.exceptions import DatalinkException
endPoint = '10.88.128.15:8000'

import sys
import io
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')



class DataServiceHttp:
  """DataServiceHttp:用于访问数链API的接口封装"""

  def __init__(self, x_app_key, secret_key):
    self.x_app_key = x_app_key
    self.secret_key = secret_key

  def set_api(self, api_name):
    self.api_name = api_name
    self.url = f'http://{endPoint}/dataservice/gateway/v1/api/{api_name}'

  def sign(self, method: str, url: str, date: str, app_key: str):
    v = method.upper() + "\n" + url + "\n" + date + "\n" + app_key + "\n"
    return v

  def encry(self, data, app_secret):
    signature = base64.b64encode(
        hmac.new(
            app_secret.encode('utf-8'), data.encode('utf-8'),
            digestmod=sha256).digest())
    return signature

  def get_headers(self):
    headers = {}
    headers.update({
        "Content-Type": "application/json",
        "User-Agent": "data-service-sdk-v1",
        "Accept": "application/json"
    })
    date = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.localtime(time.time()))
    # 构建head sign
    headers["x-date"] = date
    headers['x-app-key'] = self.x_app_key
    headers["sign"] = self.encry(
        self.sign("POST", self.url, date, self.x_app_key), self.secret_key)
    return headers

  def post(self, data, only_count=False):
    result = []
    complete = False
    data.update({"pageSize": 5000, "page": 1})
    if only_count:
      data.update({
          "pageSize": 10,
          "page": 1,
          "needPagination": True,
      })
    while not complete:
      response = requests.post(
          url=self.url, json=data, timeout=30, headers=self.get_headers())
      print(f"请求：{self.url}，数据：{data}")
      if only_count:
        return self.count_response(response)
      tmp_result = self.check_response(response)
      if tmp_result == 429:
        time.sleep(0.05)
      else:
        result.extend(tmp_result)
        data.update({"page": data['page'] + 1})
        complete = bool(len(tmp_result) != 5000)

    return result

  def check_response(self, response):
    if response.status_code == 200:
      res_data = json.loads(response.content.decode("utf-8"))
      if int(res_data['resultCode']) != 0:
        raise DatalinkException("数链返回异常,{}:{}".format(res_data['resultCode'],
                                                      res_data['returnMsg']))
      return res_data['data']['data']
    elif response.status_code == 429:  # 查询过快
      return 429
    raise DatalinkException('数链查询失败.')

  def count_response(self, response):
    if response.status_code == 200:
      res_data = json.loads(response.content.decode("utf-8"))
      if res_data['resultCode'] == '20003':
        raise DatalinkException('数链查询失败, 请尝试更新表结构并回溯数据.')
      if not res_data['data']['paginationDTO']:
        return 0
      return res_data['data']['paginationDTO']['total']
    raise DatalinkException('数链查询失败.')


if __name__ == '__main__':

  # For test
  x_app_key = '73812519'
  secret_key = 'abce9e9a9d9fe7db29eb11cbc2941dc420505cb0'
  api_name = 'query_hm_junction_pass_times'

  api = DataServiceHttp(x_app_key, secret_key)
  api.set_api(api_name)

  query_data = {
      "apiName":
          "query_hm_junction_pass_times",
      "fieldList": [{
          "name": "junction_id",
      }, {
          "name": "junction_border",
          "alias": "junction_border_MAX",
          "aggFunctionEnum": "MAX",
      }, {
          "name": "pass_times",
          "alias": "pass_times_SUM",
          "aggFunctionEnum": "SUM",
      }],
      "conditionList": [{
          "name": "region",
          "value": "beijing_yizhuang",
          "operatorEnum": "EQ",
      }, {
          "name": "trip_date",
          "value": ["2023-04-20", "2023-04-30"],
          "operatorEnum": "BETWEEN",
      }, {
          "name": "lane_turn",
          "value": ["LEFT", "STRAIGHT"],
          "operatorEnum": "IN",
      }],
      "groupList": ["junction_id"],
      "needPagination":
          True,
  }

  response = api.post(query_data, only_count=True)
  print(response)
