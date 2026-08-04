# LLM Zoomcamp 2026 Learning Repository

This is my working repository for DataTalksClub LLM Zoomcamp 2026. I use it to keep my notes, notebooks, homework files, and the projects I build while going through the course.

Most folders match the course modules, so it is easy to go back to a topic and see the files for that part.

## Course Links

- Course repository: https://github.com/DataTalksClub/llm-zoomcamp
- Course docs: https://datatalks.club/docs/courses/llm-zoomcamp/
- My course repository: https://github.com/dajuctech/zoomcamp-llm-2026

## Repository Structure

| Module | Folder | What It Covers |
|---|---|---|
| 01 | `01-agentic-rag` | RAG basics, search, prompt building, LLM calls, helper functions, data ingestion, agents, function calling, and an agentic loop. |
| 02 | `02-vector-search` | Embeddings, vector search, indexing, retrieval, and a vector-search assistant project. |
| 03 | `03-orchestration` | Context engineering, workflow orchestration, agent flow, YAML-style planning, and module practice work. |
| 04 | `04-evaluation` | Ground truth generation, retrieval evaluation, Hit Rate, MRR, search tuning, RAG evaluation, LLM-as-a-judge, and agent evaluation. |
| 05 | `05-monitoring` | Logging LLM calls, PostgreSQL storage, user feedback, built-in judge, Streamlit dashboards, Grafana, Docker Compose, and OpenTelemetry homework. |
| 06 | `06-best-practices` | Retrieval quality, keyword search, vector search, hybrid search, Reciprocal Rank Fusion, reranking, Elasticsearch, and LangChain retrievers. |
| 07 | `07-project-example` | One end-to-end fitness assistant project using generated data, RAG, evaluation, Flask, PostgreSQL, Grafana, Docker Compose, and chunking guidance. |
| 08 | `08-workshops-dbt` | dlt workshop: JSONL agent logs, filesystem pipelines, DuckDB, marimo dashboards, REST API ingestion, dltHub deployment, and scheduling. |
| 09 | `09-capstone-project` | Capstone project reference and links to the team therapeutic strategy assistant project. |

## Project Highlights

- `01-agentic-rag/course-assistant`: course assistant based on RAG and agentic concepts.
- `02-vector-search/vector-search-assistant`: vector search assistant project.
- `04-evaluation/evaluation-lab`: evaluation lab for retrieval, RAG, and agent outputs.
- `05-monitoring/monitoring-lab`: monitored course assistant with PostgreSQL, Streamlit, Grafana, and Docker Compose.
- `06-best-practices/retrieval-lab`: retrieval quality lab with Elasticsearch, hybrid search, RRF, reranking, and LangChain.
- `07-project-example/fitness-assistant`: end-to-end fitness assistant project from notebook prototype to monitored app.
- `08-workshops-dbt`: dlt agent logs pipeline and dashboard workshop.
- `09-capstone-project`: capstone reference for the therapeutic strategy assistant.

## Environment

The repository uses one shared Python environment from the repository root.

```bash
uv sync
source .venv/bin/activate
```

Secrets are kept in a local `.env` file and are not committed.

Example:

```text
OPENAI_API_KEY=your_openai_api_key_here
```

Each module may also include its own `README.md` with more specific setup and run instructions.

## Common Commands

Install or sync dependencies:

```bash
uv sync
```

Run Python with the project environment:

```bash
uv run python script.py
```

Run notebooks from VS Code or Jupyter using the project virtual environment:

```text
.venv
```

Run Docker-based module projects from the module project folder:

```bash
docker compose up -d
```

## Privacy And Git Hygiene

The repository is configured to avoid publishing local or sensitive files:

- `.env` files are ignored.
- `.venv` and `.uv-cache` are ignored.
- Python cache files are ignored.
- SQLite, DuckDB, and sidecar database files are ignored.
- Personal planning files such as `prd.md` and `practice.md` are ignored unless intentionally allowed.
- Public module `README.md` files are tracked.

## Capstone Project

The final capstone project was built as a team project under a separate GitHub organization.

- Team organization: https://github.com/AI-Precision-Medicine-Zoomcamp
- Capstone project: https://github.com/AI-Precision-Medicine-Zoomcamp/therapeutic-strategy-assistant

The `09-capstone-project` folder in this repository keeps the course-side reference and documentation links.
