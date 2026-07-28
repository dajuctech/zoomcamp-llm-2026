# Module 8 Homework - Logfire and dlt

This homework uses the course Python environment from the project root:

```text
zoomcamp-llm-2026/.venv
zoomcamp-llm-2026/pyproject.toml
zoomcamp-llm-2026/uv.lock
```

The homework secrets stay in this folder:

```text
08-workshops-dbt/homework-logfire/.env
```

Do not commit `.env`.

## 1. Add Keys

Fill in `.env`:

```text
OPENAI_API_KEY=...
LOGFIRE_TOKEN=...
LOGFIRE_READ_TOKEN=...
```

## 2. Run The Agent

```bash
cd zoomcamp-llm-2026
source .venv/bin/activate

cd 08-workshops-dbt/homework-logfire
uv run python main.py
```

The query in `main.py` is:

```text
How do I run Ollama locally?
```

After running, open Logfire and count the spans for this trace.

## 3. Build The dlt Pipeline

Use this prompt with the coding agent:

```text
Using the dltHub Logfire source context at https://dlthub.com/context/source/logfire,
build a dlt pipeline that reads traces from my Pydantic Logfire project
and loads them into DuckDB with dataset/schema name agent_traces.

Use the existing course uv environment from the zoomcamp-llm-2026 project root.
Use the Logfire credentials from 08-workshops-dbt/homework-logfire/.env.
Do not create a new uv project inside homework-logfire.
Do not expose or print my tokens.
```

## 4. Answer The Questions

Use `home_work.md` to record:

- span count
- dlt table count
- input token range
