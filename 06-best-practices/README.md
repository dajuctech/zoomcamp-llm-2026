# RAG Retrieval Quality Lab

This project follows Module 6 of LLM Zoomcamp.

The goal is to improve the retrieval part of a RAG system before sending context to the LLM.

The lab compares:

- keyword search
- vector search
- hybrid search
- Reciprocal Rank Fusion
- LangChain `ElasticsearchRetriever`

## Project Structure

```text
retrieval-lab/
├── README.md
├── docker-compose.yml
├── code/
│   ├── ingest.py
│   ├── search.py
│   ├── rrf.py
│   ├── evaluation.py
│   └── langchain_retriever.py
├── notebooks/
│   ├── 01_hybrid_search_elasticsearch.ipynb
│   ├── 02_reranking_rrf.ipynb
│   └── 03_langchain_elasticsearch_retriever.ipynb
└── reports/
    └── retrieval-results.md
```

## What Each File Does

`docker-compose.yml` starts Elasticsearch locally.

`code/ingest.py` loads the course FAQ data, creates embeddings, and indexes the documents into Elasticsearch.

`code/search.py` contains keyword search, vector search, and hybrid search helpers.

`code/rrf.py` contains the Reciprocal Rank Fusion reranking helper.

`code/evaluation.py` contains Hit Rate and MRR evaluation helpers.

`code/langchain_retriever.py` wraps the hybrid Elasticsearch query with LangChain.

`reports/retrieval-results.md` summarizes the final retrieval results.

## Setup

Run commands from the course root:

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

Check that the index exists:

```bash
curl "http://localhost:9200/_cat/indices?v"
```

You should see:

```text
course-questions
```

## Notebook Order

Run the notebooks in this order:

```text
1. notebooks/01_hybrid_search_elasticsearch.ipynb
2. notebooks/02_reranking_rrf.ipynb
3. notebooks/03_langchain_elasticsearch_retriever.ipynb
```

Use the shared course kernel:

```text
Python (zoomcamp-llm-2026)
```

## Notebook 1: Hybrid Search

This notebook compares:

- keyword search
- vector search
- Elasticsearch hybrid search

Main idea:

```text
keyword search catches exact words
vector search catches similar meaning
hybrid search combines both
```

## Notebook 2: RRF Reranking

This notebook compares:

- keyword search
- vector search
- manual RRF reranking
- Elasticsearch hybrid search

RRF formula used:

```text
RRF(d) = sum(1 / (k + rank(d)))
```

with:

```text
k = 60
```

Main idea:

```text
RRF gives stronger ranking to documents that appear high in multiple result lists.
```

## Notebook 3: LangChain Retriever

This notebook wraps the same hybrid Elasticsearch search with LangChain.

Direct Elasticsearch uses:

```text
es_client.search(...)
```

LangChain uses:

```text
retriever.invoke(query)
```

Main idea:

```text
LangChain changes the interface, not the retrieval logic.
```

## Final Report

The final report is here:

```text
reports/retrieval-results.md
```

It includes:

- methods tested
- local Hit Rate
- local MRR
- short findings
- Module 6 reference results

## Troubleshooting

If Elasticsearch is not running:

```bash
docker compose up -d
```

If port `9200` is already in use, another Elasticsearch container may already be running.

Check containers:

```bash
docker ps -a --filter name=elasticsearch
```

If the `course-questions` index is missing:

```bash
uv run python code/ingest.py
```

If imports fail in a notebook, make sure the selected kernel is:

```text
Python (zoomcamp-llm-2026)
```

If LangChain output gives a recursion error, do not display the retriever object directly.

Use:

```python
print("Retriever loaded:", type(hybrid_retriever).__name__)
```

If LangChain results do not contain `source["text"]`, use:

```python
result.page_content
```

LangChain stores the retrieved text in `page_content`.
