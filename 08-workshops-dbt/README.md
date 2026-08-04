# Module 8: dlt Agent Logs Pipeline And Dashboard

This module follows the LLM Zoomcamp dlt workshop.

The folder name says `08-workshops-dbt`, but this project is about `dlt`, not dbt.

## Project Goal

Build a small data workflow for coding-agent logs:

```text
local JSONL logs
-> dlt filesystem pipeline
-> DuckDB
-> marimo dashboard

hosted REST API traces
-> dlt REST API pipeline
-> dltHub Platform playground destination
-> deployed dashboard
-> scheduled runs
```

## Project Files

```text
08-workshops-dbt/
├── code/
│   ├── filesystem_pipeline.py
│   ├── claude_logs_dashboard.py
│   ├── rest_api_pipeline.py
│   └── agent_traces_dashboard.py
├── __deployment__.py
├── README.md
└── homework-logfire/
```

The homework folder is separate from the workshop project.

## Environment

Use the course-level Python environment from the repo root:

```bash
source .venv/bin/activate
```

Install missing workshop packages from the course root:

```bash
uv add "dlt[duckdb,hub]" marimo altair deltalake
```

Do not create a nested `uv` project inside this module.

## 1. Run The Local Filesystem Pipeline

The local pipeline reads JSONL coding-agent logs and loads them into DuckDB.

Default log folder:

```text
~/.claude/projects
```

Run:

```bash
uv run python code/filesystem_pipeline.py
```

If your logs are somewhere else:

```bash
uv run python code/filesystem_pipeline.py --bucket-url path/to/jsonl/logs
```

Inspect the local dlt output:

```bash
uv run dlthub local show
```

## 2. Run The Local marimo Dashboard

```bash
uv run marimo edit code/claude_logs_dashboard.py
```

This dashboard attaches to the local `agent_logs` pipeline and queries the DuckDB dataset.

## 3. Run The REST API Pipeline

The REST API pipeline uses the hosted fake Claude Code traces API from the workshop.

Sample run:

```bash
uv run python code/rest_api_pipeline.py
```

Full run:

```bash
uv run python code/rest_api_pipeline.py --full
```

The sample run loads one page. The full run removes the offset cap.

## 4. Deploy To dltHub Platform

Log in and connect a workspace:

```bash
uv run dlthub login
uv run dlthub workspace connect
uv run dlthub show
```

Deploy and run:

```bash
uv run dlthub deploy
uv run dlthub run
```

Publish the dashboard:

```bash
uv run dlthub job publish agent_traces_dashboard
```

List jobs:

```bash
uv run dlthub job list
```

## Notes

- `dev_mode=True` and `write_disposition="replace"` are useful during development.
- For production-style loading, remove `dev_mode`, use `merge`, and add an incremental cursor.
- The REST API pipeline can use `index` as the incremental cursor.
- Do not commit `.env`, DuckDB files, dlt pipeline state, or credentials.
