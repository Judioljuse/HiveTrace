import {createAsyncThunk, createSlice} from '@reduxjs/toolkit';
import {assemble_absolute_endpoint, client} from "../../api/client";

const initialState = {
  file: "",
  dialect: "",
  content: "",
  contentComposed: "",
  editable: false,
  editorStatus: 'idle',
  editorError: null,
  dagContent: [],
  dagColumn: [],
  dagLevel: "table",
  dagVerbose: "",
  dagStatus: 'idle',
  dagError: null,
  visualizeToBottom: false // Added state for visualization control
}

export const fetchContent = createAsyncThunk('editor/fetchContent', async (payload) => {
  return await client.post(assemble_absolute_endpoint("/script"), payload);
})

export const fetchContentAll = createAsyncThunk('editor/fetchContentAll', async (payload) => {
  console.log("fetchContentAll", payload )
  return await client.post(assemble_absolute_endpoint("/scriptall"), payload);
})

export const fetchDAG = createAsyncThunk('dag/fetchDAG', async (payload) => {
  let dialect = localStorage.getItem("dialect");
  if (dialect !== null) {
    payload["dialect"] = dialect
  }
  return await client.post(assemble_absolute_endpoint("/lineage"), payload);
})

export const fetchDAGAll = createAsyncThunk('dag/fetchDAGAll', async (payload) => {
  let dialect = localStorage.getItem("dialect");
  if (dialect !== null) {
    payload["dialect"] = dialect
  }
  console.log("lineageall", payload )
  return await client.post(assemble_absolute_endpoint("/lineageall"), payload);
})


export const editorSlice = createSlice({
  name: 'editor',
  initialState,
  reducers: {
    setContentComposed(state, action) {
      state.contentComposed = action.payload
    },
    setEditable(state, action) {
      state.editable = action.payload
    },
    setFile(state, action) {
      state.file = action.payload
    },
    setDialect(state, action) {
      state.dialect = action.payload
    },
    setDagLevel(state, action) {
      state.dagLevel = action.payload
    },
    setVisualizeToBottom(state, action) {
      state.visualizeToBottom = action.payload;
    }
  },
  extraReducers: {
    [fetchContent.pending]: (state) => {
      state.editorStatus = "loading"
    },
    [fetchContent.fulfilled]: (state, action) => {
      state.editorStatus = "succeeded";
      state.content = action.payload.content
    },
    [fetchContent.rejected]: (state, action) => {
      state.editorStatus = "failed"
      state.editorError = action.error.message
    },
    [fetchDAG.pending]: (state) => {
      state.dagStatus = "loading"
    },
    [fetchDAG.fulfilled]: (state, action) => {
      state.dagStatus = "succeeded";
      state.dagContent = action.payload.dag;
      state.dagVerbose = action.payload.verbose;
      state.dagColumn = action.payload.column;
    },
    [fetchDAG.rejected]: (state, action) => {
      state.dagStatus = "failed";
      state.dagError = action.error.message;
    },
    [fetchContentAll.pending]: (state) => {
      state.editorStatus = "loading"
    },
    [fetchContentAll.fulfilled]: (state, action) => {
      state.editorStatus = "succeeded";
      state.content = action.payload.content
    },
    [fetchContentAll.rejected]: (state, action) => {
      state.editorStatus = "failed"
      state.editorError = action.error.message
    },
    [fetchDAGAll.pending]: (state) => {
      state.dagStatus = "loading"
    },
    [fetchDAGAll.fulfilled]: (state, action) => {
      state.dagStatus = "succeeded";
      state.dagContent = action.payload.dag;
      state.dagVerbose = action.payload.verbose;
      state.dagColumn = action.payload.column;
    },
    [fetchDAGAll.rejected]: (state, action) => {
      state.dagStatus = "failed";
      state.dagError = action.error.message;
    }
  }
});

export const selectEditor = state => state.editor;
export const {setContentComposed, setDagLevel, setEditable, setFile, setDialect} = editorSlice.actions;

export default editorSlice.reducer;
