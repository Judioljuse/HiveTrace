.
├── demo.ipynb
├── Dockerfile
├── docs
│   ├── basic_concepts
│   │   ├── analyzer.rst
│   │   ├── holder.rst
│   │   ├── metadata_provider.rst
│   │   ├── model.rst
│   │   └── runner.rst
│   ├── behind_the_scene
│   │   ├── column-level_lineage_design.rst
│   │   ├── dialect-awareness_lineage_design.rst
│   │   ├── dos_and_donts.rst
│   │   ├── how_sqllineage_work.rst
│   │   └── why_sqllineage.rst
│   ├── conf.py
│   ├── first_steps
│   │   ├── advanced_usage.rst
│   │   ├── beyond_command_line.rst
│   │   └── getting_started.rst
│   ├── gear_up
│   │   ├── configuration.rst
│   │   └── metadata.rst
│   ├── index.rst
│   ├── make.bat
│   ├── Makefile
│   ├── release_note
│   │   └── changelog.rst
│   └── _static
│       ├── column.jpg
│       └── table.jpg
├── MANIFEST.in
├── mypy.ini
├── __pycache__
│   └── DataServiceAPI.cpython-312.pyc
├── README.md
├── setup.py
├── sqllineage
│   ├── build
│   │   ├── asset-manifest.json
│   │   ├── editor.worker.js
│   │   ├── editor.worker.js.map
│   │   ├── favicon.ico
│   │   ├── index.html
│   │   ├── logo192.png
│   │   ├── logo512.png
│   │   ├── manifest.json
│   │   ├── robots.txt
│   │   └── static
│   │       ├── css
│   │       │   ├── main.84d1d546.css
│   │       │   └── main.84d1d546.css.map
│   │       ├── js
│   │       │   ├── 333.140e3456.chunk.js
│   │       │   ├── 333.140e3456.chunk.js.map
│   │       │   ├── main.3b88c6e3.js
│   │       │   ├── main.3b88c6e3.js.LICENSE.txt
│   │       │   └── main.3b88c6e3.js.map
│   │       └── media
│   │           └── codicon.4168b9c11e5075e9cfe6.ttf
│   ├── cli.py
│   ├── config.py
│   ├── core
│   │   ├── analyzer.py
│   │   ├── holders.py
│   │   ├── __init__.py
│   │   ├── metadata
│   │   │   ├── dummy.py
│   │   │   ├── __init__.py
│   │   │   ├── __pycache__
│   │   │   │   ├── dummy.cpython-312.pyc
│   │   │   │   └── __init__.cpython-312.pyc
│   │   │   └── sqlalchemy.py
│   │   ├── metadata_provider.py
│   │   ├── models.py
│   │   ├── parser
│   │   │   ├── __init__.py
│   │   │   ├── __pycache__
│   │   │   │   └── __init__.cpython-312.pyc
│   │   │   ├── sqlfluff
│   │   │   │   ├── analyzer.py
│   │   │   │   ├── extractors
│   │   │   │   │   ├── base.py
│   │   │   │   │   ├── copy.py
│   │   │   │   │   ├── create_insert.py
│   │   │   │   │   ├── cte.py
│   │   │   │   │   ├── drop.py
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── merge.py
│   │   │   │   │   ├── noop.py
│   │   │   │   │   ├── __pycache__
│   │   │   │   │   │   ├── base.cpython-312.pyc
│   │   │   │   │   │   ├── copy.cpython-312.pyc
│   │   │   │   │   │   ├── create_insert.cpython-312.pyc
│   │   │   │   │   │   ├── cte.cpython-312.pyc
│   │   │   │   │   │   ├── drop.cpython-312.pyc
│   │   │   │   │   │   ├── __init__.cpython-312.pyc
│   │   │   │   │   │   ├── merge.cpython-312.pyc
│   │   │   │   │   │   ├── noop.cpython-312.pyc
│   │   │   │   │   │   ├── rename.cpython-312.pyc
│   │   │   │   │   │   ├── select.cpython-312.pyc
│   │   │   │   │   │   └── update.cpython-312.pyc
│   │   │   │   │   ├── rename.py
│   │   │   │   │   ├── select.py
│   │   │   │   │   └── update.py
│   │   │   │   ├── __init__.py
│   │   │   │   ├── models.py
│   │   │   │   ├── __pycache__
│   │   │   │   │   ├── analyzer.cpython-312.pyc
│   │   │   │   │   ├── __init__.cpython-312.pyc
│   │   │   │   │   ├── models.cpython-312.pyc
│   │   │   │   │   └── utils.cpython-312.pyc
│   │   │   │   └── utils.py
│   │   │   └── sqlparse
│   │   │       ├── analyzer.py
│   │   │       ├── handlers
│   │   │       │   ├── base.py
│   │   │       │   ├── cte.py
│   │   │       │   ├── __init__.py
│   │   │       │   ├── __pycache__
│   │   │       │   │   ├── base.cpython-312.pyc
│   │   │       │   │   ├── cte.cpython-312.pyc
│   │   │       │   │   ├── __init__.cpython-312.pyc
│   │   │       │   │   ├── source.cpython-312.pyc
│   │   │       │   │   ├── swap_partition.cpython-312.pyc
│   │   │       │   │   └── target.cpython-312.pyc
│   │   │       │   ├── source.py
│   │   │       │   ├── swap_partition.py
│   │   │       │   └── target.py
│   │   │       ├── __init__.py
│   │   │       ├── models.py
│   │   │       ├── __pycache__
│   │   │       │   ├── analyzer.cpython-312.pyc
│   │   │       │   ├── __init__.cpython-312.pyc
│   │   │       │   ├── models.cpython-312.pyc
│   │   │       │   └── utils.cpython-312.pyc
│   │   │       └── utils.py
│   │   └── __pycache__
│   │       ├── analyzer.cpython-312.pyc
│   │       ├── holders.cpython-312.pyc
│   │       ├── __init__.cpython-312.pyc
│   │       ├── metadata_provider.cpython-312.pyc
│   │       └── models.cpython-312.pyc
│   ├── drawing.py
│   ├── exceptions.py
│   ├── __init__.py
│   ├── io.py
│   ├── __pycache__
│   │   ├── config.cpython-312.pyc
│   │   ├── drawing.cpython-312.pyc
│   │   ├── exceptions.cpython-312.pyc
│   │   ├── __init__.cpython-312.pyc
│   │   ├── io.cpython-312.pyc
│   │   └── runner.cpython-312.pyc
│   ├── runner.py
│   └── utils
│       ├── constant.py
│       ├── entities.py
│       ├── helpers.py
│       ├── __init__.py
│       └── __pycache__
│           ├── constant.cpython-312.pyc
│           ├── entities.cpython-312.pyc
│           ├── helpers.cpython-312.pyc
│           └── __init__.cpython-312.pyc
├── sqllineagejs
│   ├── config-overrides.js
│   ├── package.json
│   ├── package-lock.json
│   ├── public
│   │   ├── favicon.ico
│   │   ├── index.html
│   │   ├── logo192.png
│   │   ├── logo512.png
│   │   ├── manifest.json
│   │   └── robots.txt
│   └── src
│       ├── api
│       │   └── client.js
│       ├── app
│       │   └── store.js
│       ├── App.js
│       ├── features
│       │   ├── directory
│       │   │   ├── Directory.js
│       │   │   ├── directorySlice.js
│       │   │   └── DirectoryTreeItem.js
│       │   ├── editor
│       │   │   ├── DAGDesc.js
│       │   │   ├── DAG.js
│       │   │   ├── Editor.js
│       │   │   └── editorSlice.js
│       │   └── widget
│       │       ├── LoadError.js
│       │       └── Loading.js
│       ├── index.css
│       └── index.js
├── tests
│   ├── core
│   │   ├── __init__.py
│   │   ├── test_cli.py
│   │   ├── test_config.py
│   │   ├── test_drawing.py
│   │   ├── test_exception.py
│   │   ├── test_holder.py
│   │   ├── test_metadata_provider.py
│   │   ├── test_models.py
│   │   ├── test_parser.py
│   │   └── test_runner.py
│   ├── helpers.py
│   ├── __init__.py
│   └── sql
│       ├── column
│       │   ├── __init__.py
│       │   ├── multiple_statements
│       │   │   ├── __init__.py
│       │   │   └── test_session_metadata.py
│       │   ├── test_column_merge.py
│       │   ├── test_column_select_case_when.py
│       │   ├── test_column_select_cast.py
│       │   ├── test_column_select_column_dialect_specific.py
│       │   ├── test_column_select_column.py
│       │   ├── test_column_select_column_specified_in_dml.py
│       │   ├── test_column_select_expression.py
│       │   ├── test_column_select_from_cte.py
│       │   ├── test_column_select_from_join.py
│       │   ├── test_column_select_from_subquery.py
│       │   ├── test_column_select_function.py
│       │   ├── test_column_select_lateral_alias_ref.py
│       │   ├── test_column_select_union.py
│       │   ├── test_column_update.py
│       │   ├── test_metadata_target_column.py
│       │   ├── test_metadata_unqualified_column.py
│       │   └── test_metadata_wildcard.py
│       ├── __init__.py
│       └── table
│           ├── __init__.py
│           ├── multiple_statements
│           │   ├── __init__.py
│           │   ├── test_split.py
│           │   ├── test_tmp_table.py
│           │   ├── test_tsql_no_semicolon.py
│           │   └── test_variable.py
│           ├── test_create_dialect_specific.py
│           ├── test_create.py
│           ├── test_cte_dialect_specific.py
│           ├── test_cte.py
│           ├── test_insert_dialect_specific.py
│           ├── test_insert.py
│           ├── test_merge_dialect_specific.py
│           ├── test_merge.py
│           ├── test_other_with_lineage_dialect_specific.py
│           ├── test_other_with_lineage.py
│           ├── test_other_without_lineage_dialect_specific.py
│           ├── test_other_without_lineage.py
│           ├── test_path_dialect_specific.py
│           ├── test_select_dialect_specific.py
│           ├── test_select.py
│           ├── test_update_dialect_specific.py
│           └── test_update.py
├── tox.ini
├── tree.md
├── voydstools
│   ├── common
│   │   ├── DataServiceAPI.py
│   │   ├── exceptions.py
│   │   ├── __init__.py
│   │   └── __pycache__
│   │       ├── DataServiceAPI.cpython-312.pyc
│   │       ├── exceptions.cpython-312.pyc
│   │       └── __init__.cpython-312.pyc
│   ├── __init__.py
│   └── __pycache__
│       └── __init__.cpython-312.pyc
└── wgsi.ipynb

51 directories, 224 files
