# RAG Retrieval Quality Lab

This project follows Module 6 of LLM Zoomcamp.

It focuses on improving RAG retrieval quality using:

- keyword search
- vector search
- hybrid search
- Reciprocal Rank Fusion
- LangChain ElasticsearchRetriever

The goal is to understand how better retrieval improves the context sent to the LLM.

## Project Structure

```text
retrieval-lab/
├── README.md
├── code/
├── notebooks/
└── reports/
```

## Run The Hybrid Search Notebook

Run these commands from the course root:

```bash
cd 06-best-practices/retrieval-lab
```

Start Elasticsearch:

```bash
docker compose up -d
```

Check that Elasticsearch is running:

```bash
curl http://localhost:9200
```

Build the `course-questions` index:

```bash
uv run python code/ingest.py
```

Then open:

```text
notebooks/01_hybrid_search_elasticsearch.ipynb
```

Use the course kernel:

```text
Python (zoomcamp-llm-2026)
```

If the notebook says Elasticsearch is not running, start it with:

```bash
docker compose up -d
```

If the notebook says the index is missing, run:

```bash
uv run python code/ingest.py
```
