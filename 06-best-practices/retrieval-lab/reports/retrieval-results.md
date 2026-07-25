# Retrieval Results

This report summarizes the Module 6 retrieval lab.

The goal was to compare different retrieval methods before sending context to an LLM.

## What Was Tested

The project tested:

- keyword search
- vector search
- hybrid search
- hybrid search with Reciprocal Rank Fusion
- LangChain hybrid retriever

All tests used the same Elasticsearch index:

```text
course-questions
```

The examples used the course filter:

```text
data-engineering-zoomcamp
```

## Search Methods

### Keyword Search

Keyword search uses Elasticsearch text matching across:

```text
question^3
text
section
```

The `question^3` weight gives the question field more importance.

### Vector Search

Vector search embeds the user query and compares it with:

```text
question_text_vector
```

This helps retrieve documents with similar meaning even when the exact words are different.

### Hybrid Search

Hybrid search combines:

```text
keyword search + vector search
```

This gives the retriever both exact matching and semantic matching.

### RRF Reranking

RRF means Reciprocal Rank Fusion.

It combines ranked results from keyword search and vector search.

The project uses:

```text
RRF(d) = sum(1 / (k + rank(d)))
```

with:

```text
k = 60
```

### LangChain Retriever

LangChain wraps the same Elasticsearch hybrid search logic.

Direct Elasticsearch uses:

```text
es_client.search(...)
```

LangChain uses:

```text
retriever.invoke(query)
```

The search idea stays the same.

## Local Evaluation

The local sanity evaluation used 30 indexed FAQ questions as ground truth.

Each test checked whether the expected document appeared in the top 5 results.

Metrics:

- Hit Rate
- MRR

| Method | Hit Rate | MRR |
|---|---:|---:|
| Keyword search | 1.000 | 1.000 |
| Vector search | 1.000 | 0.978 |
| Hybrid search | 1.000 | 1.000 |
| Hybrid search with RRF | 1.000 | 1.000 |
| LangChain hybrid retriever | 1.000 | 1.000 |

## Module Reference Results

The module showed these reference results:

| Method | Hit Rate | MRR |
|---|---:|---:|
| Hybrid search without RRF | 0.917 | 0.824 |
| Hybrid search with RRF | 0.925 | 0.851 |

The main lesson from the module is that RRF can improve the ranking quality.

## Findings

Keyword search worked well on the local sample because the evaluation questions came from the same FAQ documents.

Vector search also retrieved the right documents, but one expected document appeared slightly lower in the ranking, so the MRR was lower.

Hybrid search recovered strong results by combining keyword matching and semantic matching.

RRF gives a clear way to merge keyword and vector rankings without needing paid Elasticsearch RRF features.

LangChain did not change the retrieval logic. It simply wrapped the same Elasticsearch query in a retriever interface.

## Final Learning Point

Good RAG depends on good retrieval.

A stronger LLM cannot fully fix poor context. Module 6 shows how to improve retrieval before the answer generation step.
