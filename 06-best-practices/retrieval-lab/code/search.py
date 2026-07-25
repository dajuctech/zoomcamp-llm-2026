from elasticsearch import Elasticsearch
from langchain_huggingface import HuggingFaceEmbeddings


ES_URL = "http://localhost:9200"
INDEX_NAME = "course-questions"
DEFAULT_COURSE = "data-engineering-zoomcamp"
EMBEDDING_MODEL = "sentence-transformers/multi-qa-MiniLM-L6-cos-v1"


def create_es_client():
    return Elasticsearch(ES_URL)


def create_embedding_model():
    return HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)


def keyword_search(query, course=DEFAULT_COURSE, num_results=5, es_client=None):
    if es_client is None:
        es_client = create_es_client()

    search_query = {
        "size": num_results,
        "query": {
            "bool": {
                "must": {
                    "multi_match": {
                        "query": query,
                        "fields": ["question^3", "text", "section"],
                        "type": "best_fields",
                    }
                },
                "filter": {
                    "term": {
                        "course": course
                    }
                },
            }
        },
    }

    response = es_client.search(index=INDEX_NAME, body=search_query)

    return [hit["_source"] for hit in response["hits"]["hits"]]


def vector_search(query, course=DEFAULT_COURSE, num_results=5, es_client=None, embedding_model=None):
    if es_client is None:
        es_client = create_es_client()

    if embedding_model is None:
        embedding_model = create_embedding_model()

    query_vector = embedding_model.embed_query(query)

    response = es_client.search(
        index=INDEX_NAME,
        knn={
            "field": "question_text_vector",
            "query_vector": query_vector,
            "k": num_results,
            "num_candidates": 10000,
            "filter": {
                "term": {
                    "course": course
                }
            },
        },
        size=num_results,
    )

    return [hit["_source"] for hit in response["hits"]["hits"]]


def hybrid_search(query, course=DEFAULT_COURSE, num_results=5, es_client=None, embedding_model=None):
    if es_client is None:
        es_client = create_es_client()

    if embedding_model is None:
        embedding_model = create_embedding_model()

    query_vector = embedding_model.embed_query(query)

    response = es_client.search(
        index=INDEX_NAME,
        query={
            "bool": {
                "must": {
                    "multi_match": {
                        "query": query,
                        "fields": ["question^3", "text", "section"],
                        "type": "best_fields",
                    }
                },
                "filter": {
                    "term": {
                        "course": course
                    }
                },
            }
        },
        knn={
            "field": "question_text_vector",
            "query_vector": query_vector,
            "k": num_results,
            "num_candidates": 10000,
            "filter": {
                "term": {
                    "course": course
                }
            },
        },
        size=num_results,
    )

    return [hit["_source"] for hit in response["hits"]["hits"]]
