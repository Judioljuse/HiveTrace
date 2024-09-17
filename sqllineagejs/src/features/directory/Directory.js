import React, { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { fetchRootDirectory, selectDirectory, setOpenNonSQLWarning } from "./directorySlice";
import { Loading } from "../widget/Loading";
import { LoadError } from "../widget/LoadError";
import { Snackbar, TextField } from "@material-ui/core";
import DirectoryTreeItem from "./DirectoryTreeItem";

export function Directory(props) {
  const dispatch = useDispatch(); // 获取dispatch函数, 用于发送action, 触发state变化
  const directoryState = useSelector(selectDirectory); // 获取目录状态
  const [searchTerm, setSearchTerm] = useState("");  // 新增状态用于保存搜索词
  const [searchResults, setSearchResults] = useState(null);  // 新增状态用于保存搜索结果

  // 递归搜索整个目录树
  function searchDirectory(directory, term) {
    if (!directory) return [];
    
    let result = [];
    
    for (const item of directory) {
      if (item.name.toLowerCase().includes(term.toLowerCase())) {
        result.push(item);
      }
      
      if (item.is_dir && item.children) {
        result = result.concat(searchDirectory(item.children, term));
      }
    }
    
    return result;
  }

  useEffect(() => {
    if (directoryState.status === "idle") {
      let url = new URL(window.location.href); // 从URL中获取查询参数
      // 打印查询参数
      console.log("Query Parameters:");
      for (const [key, value] of url.searchParams) {
        console.log(key, value);
      }
      dispatch(fetchRootDirectory(Object.fromEntries(url.searchParams))); // 发起获取根目录请求
      // 打印请求参数
      console.log("Request Parameters:");
      console.log(Object.fromEntries(url.searchParams));
    } else if (directoryState.status === "succeeded" && searchTerm) {  // 目录树加载成功后
      // 如果有搜索词，递归搜索目录树
      const results = searchDirectory([directoryState.content], searchTerm);
      console.log(results);
      setSearchResults(results);  // 更新搜索结果
      // 打印搜索结果
      console.log("Search Results:");
      for (const item of results) {
        console.log(item.name);
      }
    }
  }, [directoryState.status, searchTerm]);

  if (directoryState.status === "loading") {
    return <Loading minHeight={props.height} />;
  } else if (directoryState.status === "failed") {
    return <LoadError minHeight={props.height} message={directoryState.error} />;
  } else {
    return (
      <div>
        {/* 搜索框 */}
        <TextField
          label="Search Files"
          variant="outlined"
          size="small"
          fullWidth
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}  // 更新搜索词
        />

        {/* 如果有搜索结果则显示搜索结果，否则显示完整目录 */}
        {searchResults && searchResults.length > 0 ? (
          searchResults.map((item) => (
            <DirectoryTreeItem
              key={item.id}
              id={item.id}
              name={item.name}
              is_dir={item.is_dir}
              is_root={false}
            />
          ))
        ) : (
          <DirectoryTreeItem
            id={directoryState.content.id}
            name={directoryState.content.name}
            is_dir={true}
            is_root={true}
          />
        )}

        {/* 非SQL文件警告 */}
        <Snackbar
          anchorOrigin={{
            vertical: 'bottom',
            horizontal: 'left',
          }}
          open={directoryState.openNonSQLWarning}
          autoHideDuration={1000}
          onClose={() => {
            dispatch(setOpenNonSQLWarning(false));
          }}
          message="Non SQL File Is Not Supported"
        />
      </div>
    );
  }
}