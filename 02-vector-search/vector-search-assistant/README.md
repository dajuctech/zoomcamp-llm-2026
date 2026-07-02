# Vector Search Assistant

This project is a hands-on implementation of the vector search workflow from Module 2 of LLM Zoomcamp.

The goal is to understand how search improves when text is converted into embeddings, how those embeddings can be searched with different tools, and how vector search can be used inside a RAG application.

The project starts small with two sentence embeddings, then builds up to manual vector search, `minsearch`, SQLite persistence, PGVector, ONNX embeddings, and hybrid search.

## What This Project Achieves

This project shows how to:

- Load the course FAQ dataset.
- Convert questions and answers into embedding vectors.
- Compare vectors with dot product / cosine similarity.
- Search manually with NumPy.
- Search with `minsearch.VectorSearch`.
- Use vector search inside a RAG pipeline.
- Save and reopen a vector index with SQLite.
- Store and search embeddings in PostgreSQL with `pgvector`.
- Replace `sentence-transformers` with a lighter ONNX embedder.
- Combine keyword search and vector search with Reciprocal Rank Fusion.

By the end, the project answers a course-related question by finding relevant context from the FAQ data and sending that context to an LLM.

## Project Files

```text
vector-search-assistant/
  README.md
  ingest.py
  embeddings.py
  manual_vector_search.py
  minsearch_vector_search.py
  rag_helper.py
  vector_rag.py
  sqlite_vector_search.py
  sqlite_reopen_search.py
  pgvector_search.py
  download.py
  embedder.py
  models/
  onnx_embedder_demo.py
  hybrid_search.py
  faq_vectors2.db
```

## File Guide

`ingest.py`

Loads the FAQ dataset used by the course. The rest of the project depends on this file because every search method needs documents to search over.

`embeddings.py`

Loads `SentenceTransformer("all-MiniLM-L6-v2")`, embeds two similar questions, and compares them with a dot product. This is the first check that embeddings are working.

`manual_vector_search.py`

Builds document embeddings for the FAQ dataset and searches by hand with NumPy:

```text
query -> query vector -> X.dot(query vector) -> top results
```

This makes the core idea of vector search visible before using a library.

`minsearch_vector_search.py`

Uses `minsearch.VectorSearch` to do vector search with filtering. The important improvement is filtering by course:

```python
filter_dict={"course": "llm-zoomcamp"}
```

This keeps results focused on the LLM Zoomcamp FAQ instead of returning similar answers from other courses.

`rag_helper.py`

Provides the base RAG helper used in the course. It handles:

- building context from search results
- building the prompt
- calling the LLM
- returning the answer

`vector_rag.py`

Uses vector search as the retrieval step in RAG. The key class is `RAGVector`, which overrides `search()` so a user query is embedded before searching.

`sqlite_vector_search.py`

Builds a persistent vector search index with `sqlitesearch.VectorSearchIndex`.

Unlike the in-memory `minsearch` example, this creates a local database:

```text
faq_vectors2.db
```

`sqlite_reopen_search.py`

Reopens the saved SQLite vector index and searches without rebuilding all document embeddings. This shows the production-style split between:

```text
ingestion time: embed documents and save index
query time: embed only the user query and search
```

`pgvector_search.py`

Stores embeddings in PostgreSQL using the `pgvector` extension. It demonstrates:

- `CREATE EXTENSION IF NOT EXISTS vector`
- `embedding vector(384)`
- cosine distance with `<=>`
- filtering with SQL
- HNSW indexing
- using PGVector inside a RAG class

This is the production-style database option in the project.

`download.py`

Downloads the ONNX model files used by the lightweight embedder.

`embedder.py`

Provides the ONNX `Embedder` class. It gives a similar interface to `sentence-transformers`:

```python
embed.encode(text)
embed.encode_batch(texts)
```

`models/`

Stores the local ONNX model files:

```text
models/Xenova/all-MiniLM-L6-v2/
  tokenizer.json
  model.onnx
```

`onnx_embedder_demo.py`

Repeats the embedding and manual vector search flow using the ONNX embedder instead of `sentence-transformers`.

The output should be close to the earlier vector search results, but with a lighter runtime dependency.

`hybrid_search.py`

Combines vector search and keyword search.

It uses:

- `gitsource` to load lesson files
- `chunk_documents` to split long pages
- ONNX `Embedder` for vector search
- `minsearch.Index` for keyword search
- Reciprocal Rank Fusion to merge both ranked lists

The key function is:

```python
def rrf(result_lists, k=60, num_results=5):
    scores = {}
    docs = {}

    for results in result_lists:
        for rank, doc in enumerate(results):
            key = (doc["filename"], doc["start"])
            scores[key] = scores.get(key, 0) + 1 / (k + rank)
            docs[key] = doc

    ranked = sorted(scores, key=scores.get, reverse=True)
    return [docs[key] for key in ranked[:num_results]]
```

Hybrid search is useful because keyword search is strong with exact terms, while vector search is strong with meaning and paraphrases.

## How To Run

Run commands from the course root unless a section says otherwise:

```bash
uv run python 02-vector-search/vector-search-assistant/embeddings.py
uv run python 02-vector-search/vector-search-assistant/manual_vector_search.py
uv run python 02-vector-search/vector-search-assistant/minsearch_vector_search.py
uv run python 02-vector-search/vector-search-assistant/vector_rag.py
uv run python 02-vector-search/vector-search-assistant/sqlite_vector_search.py
uv run python 02-vector-search/vector-search-assistant/sqlite_reopen_search.py
uv run python 02-vector-search/vector-search-assistant/pgvector_search.py
```

For the ONNX and hybrid search scripts, run from inside the project folder so the local `models/` folder is found correctly:

```bash
cd 02-vector-search/vector-search-assistant
uv run python onnx_embedder_demo.py
uv run python hybrid_search.py
```

## PGVector Setup

`pgvector_search.py` needs Docker and PostgreSQL with the `pgvector` extension.

Start the container:

```bash
docker run -it \
  --name pgvector \
  -e POSTGRES_USER=user \
  -e POSTGRES_PASSWORD=pswd \
  -e POSTGRES_DB=faq \
  -v pgvector_data:/var/lib/postgresql/data \
  -p 5432:5432 \
  pgvector/pgvector:pg17
```

Install the Python driver:

```bash
uv add 'psycopg[binary]'
```

Then run:

```bash
uv run python 02-vector-search/vector-search-assistant/pgvector_search.py
```

## Main Learning Flow

The project follows this learning order:

```text
1. Embed small text examples
2. Embed the FAQ dataset
3. Search manually with NumPy
4. Use minsearch for vector search
5. Add vector search to RAG
6. Persist vectors with SQLite
7. Reopen the saved SQLite index
8. Store vectors in PostgreSQL with pgvector
9. Use ONNX Runtime for lighter embeddings
10. Combine keyword and vector search with RRF
```

## What To Pay Attention To

Embeddings are just arrays of numbers, but the numbers capture meaning.

Dot product works here because the embedding vectors are normalized, so it behaves like cosine similarity.

Manual NumPy search helps explain what vector databases do internally.

Filtering matters because similar answers from the wrong course can rank highly.

SQLite and PGVector show why projects separate ingestion from querying.

ONNX gives the same embedding workflow with less deployment overhead than PyTorch.

Hybrid search is useful because there is no single perfect search method.

## Current Status

The project currently includes working examples for:

- sentence embeddings
- manual vector search
- `minsearch` vector search
- vector RAG
- SQLite vector search
- SQLite index reopening
- PGVector search and RAG
- ONNX embeddings
- hybrid search with RRF

The remaining useful improvement is to add a project notebook that walks through the same steps interactively.
