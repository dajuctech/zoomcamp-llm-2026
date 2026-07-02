# Vector Search Assistant

Vector Search Assistant is a small retrieval project for answering LLM Zoomcamp course questions with semantic search and RAG.

It starts with the course FAQ data, turns each question and answer into an embedding, searches for the most relevant records, and uses the retrieved context to answer a user question. The project includes several retrieval backends so the same search problem can be compared across simple NumPy search, in-memory vector search, SQLite persistence, PostgreSQL with `pgvector`, ONNX embeddings, and hybrid retrieval.

## What It Does

The assistant can:

- load FAQ documents from the course dataset
- create embeddings with `sentence-transformers`
- rank documents manually with NumPy dot products
- search with `minsearch.VectorSearch`
- use retrieved documents inside a RAG prompt
- persist a vector index with SQLite
- search embeddings stored in PostgreSQL using `pgvector`
- run embeddings with a lightweight ONNX Runtime implementation
- combine vector search and keyword search using Reciprocal Rank Fusion

The main question the project demonstrates is:

```text
I just discovered the course. Can I still join?
```

The expected answer is retrieved from the LLM Zoomcamp FAQ and then passed into a RAG flow.

## Architecture

```text
FAQ data
  -> document text
  -> embeddings
  -> vector index
  -> search results
  -> prompt context
  -> LLM answer
```

For hybrid search, the retrieval path becomes:

```text
query
  -> vector search results
  -> keyword search results
  -> Reciprocal Rank Fusion
  -> final ranked results
```

## Project Structure

```text
vector-search-assistant/
  README.md
  project_notebook.ipynb
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

## Files

`ingest.py` loads the FAQ data used by the search examples.

`embeddings.py` verifies that `SentenceTransformer("all-MiniLM-L6-v2")` can encode text and compare similar questions.

`manual_vector_search.py` embeds the FAQ records, stores them in a NumPy matrix, and ranks documents with:

```python
scores = X.dot(v_query)
```

`minsearch_vector_search.py` replaces the manual ranking code with `minsearch.VectorSearch` and filters results to `llm-zoomcamp`.

`rag_helper.py` contains the reusable RAG helper: build context, build prompt, call the LLM, and return the answer.

`vector_rag.py` connects vector search to the RAG flow by overriding the search step and embedding the user query before retrieval.

`sqlite_vector_search.py` builds a persistent vector index with `sqlitesearch.VectorSearchIndex`.

`sqlite_reopen_search.py` opens the saved SQLite index and searches it without rebuilding all document embeddings.

`pgvector_search.py` stores embeddings in PostgreSQL with the `pgvector` extension and queries them with cosine distance.

`download.py`, `embedder.py`, and `models/` support the ONNX Runtime embedding path.

`onnx_embedder_demo.py` repeats the embedding and vector search workflow with the lightweight ONNX embedder.

`hybrid_search.py` combines vector search and keyword search with Reciprocal Rank Fusion.

`project_notebook.ipynb` is an interactive walkthrough of the same project files.

## Setup

Install dependencies from the repository root:

```bash
uv sync
```

The project uses Python 3.12 because the embedding stack is more stable there than on Python 3.14.

The main dependencies used by this project are:

```text
sentence-transformers
numpy
tqdm
minsearch
sqlitesearch
onnxruntime
tokenizers
gitsource
openai
python-dotenv
psycopg[binary]
```

## Running The Scripts

From the repository root:

```bash
uv run python 02-vector-search/vector-search-assistant/embeddings.py
uv run python 02-vector-search/vector-search-assistant/manual_vector_search.py
uv run python 02-vector-search/vector-search-assistant/minsearch_vector_search.py
uv run python 02-vector-search/vector-search-assistant/vector_rag.py
uv run python 02-vector-search/vector-search-assistant/sqlite_vector_search.py
uv run python 02-vector-search/vector-search-assistant/sqlite_reopen_search.py
uv run python 02-vector-search/vector-search-assistant/pgvector_search.py
```

For ONNX and hybrid search, run from the project folder so the local `models/` path resolves correctly:

```bash
cd 02-vector-search/vector-search-assistant
uv run python onnx_embedder_demo.py
uv run python hybrid_search.py
```

## PGVector

`pgvector_search.py` needs a running PostgreSQL container with the `pgvector` extension:

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

The script creates the `vector` extension, stores 384-dimensional embeddings, runs similarity search with `<=>`, creates an HNSW index, and uses the PostgreSQL-backed search inside a RAG class.

## SQLite Index

`sqlite_vector_search.py` creates or rebuilds:

```text
faq_vectors2.db
```

`sqlite_reopen_search.py` reuses that database without re-embedding all FAQ documents.

That separation matters because embedding every document is an ingestion-time job. At query time, the app only needs to embed the user question and search the saved index.

## ONNX Runtime

The ONNX version uses the same embedding model family without loading the full PyTorch stack.

The local model files live under:

```text
models/Xenova/all-MiniLM-L6-v2/
  tokenizer.json
  model.onnx
```

`embedder.py` exposes:

```python
embed.encode(text)
embed.encode_batch(texts)
```

This keeps the rest of the search pipeline almost identical to the `sentence-transformers` examples.

## Hybrid Search

`hybrid_search.py` compares semantic retrieval and keyword retrieval, then merges both result lists with Reciprocal Rank Fusion.

The fusion function ranks documents by their positions in each result list:

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

This is useful because vector search handles meaning and paraphrases, while keyword search handles exact terms more reliably.

## Notes For Git

The following files are generated locally and should normally stay out of Git:

```text
models/
faq_vectors2.db
__pycache__/
*.pyc
.env
```

The source files, README, and notebook are the important project artifacts to commit.
