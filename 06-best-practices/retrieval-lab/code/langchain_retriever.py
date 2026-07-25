from typing import Dict

from langchain_elasticsearch import ElasticsearchRetriever
from langchain_huggingface import HuggingFaceEmbeddings


ES_URL = "http://localhost:9200"
INDEX_NAME = "course-questions"
DEFAULT_COURSE = "data-engineering-zoomcamp"
EMBEDDING_MODEL = "sentence-transformers/multi-qa-MiniLM-L6-cos-v1"


embedding = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)


def hybrid_query(search_query: str) -> Dict:
    vector = embedding.embed_query(search_query)

    return {
        "query": {
            "bool": {
                "must": {
                    "multi_match": {
                        "query": search_query,
                        "fields": ["question^3", "text", "section"],
                        "type": "best_fields",
                    }
                },
                "filter": {
                    "term": {
                        "course": DEFAULT_COURSE
                    }
                },
            }
        },
        "knn": {
            "field": "question_text_vector",
            "query_vector": vector,
            "k": 5,
            "num_candidates": 10000,
            "filter": {
                "term": {
                    "course": DEFAULT_COURSE
                }
            },
        },
        "size": 5,
    }


def create_hybrid_retriever():
    return ElasticsearchRetriever(
        es_url=ES_URL,
        index_name=INDEX_NAME,
        body_func=hybrid_query,
        content_field="text",
    )
