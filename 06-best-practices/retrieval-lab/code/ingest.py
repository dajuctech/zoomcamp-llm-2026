import requests
from elasticsearch import Elasticsearch
from langchain_huggingface import HuggingFaceEmbeddings
from tqdm.auto import tqdm


ES_URL = "http://localhost:9200"
INDEX_NAME = "course-questions"
EMBEDDING_MODEL = "sentence-transformers/multi-qa-MiniLM-L6-cos-v1"


def load_documents():
    docs_url = "https://datatalks.club/faq/json/courses.json"

    docs_response = requests.get(docs_url)
    docs_response.raise_for_status()
    courses_raw = docs_response.json()

    documents = []
    url_prefix = "https://datatalks.club/faq"

    for course in courses_raw:
        course_url = f'{url_prefix}{course["path"]}'
        course_response = requests.get(course_url)
        course_response.raise_for_status()
        course_data = course_response.json()

        for doc in course_data:
            doc["text"] = doc["answer"]
            documents.append(doc)

    return documents


def create_index(es_client):
    index_settings = {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0,
        },
        "mappings": {
            "properties": {
                "text": {"type": "text"},
                "section": {"type": "text"},
                "question": {"type": "text"},
                "course": {"type": "keyword"},
                "question_text_vector": {
                    "type": "dense_vector",
                    "dims": 384,
                    "index": True,
                    "similarity": "cosine",
                },
            }
        },
    }

    es_client.indices.delete(index=INDEX_NAME, ignore_unavailable=True)
    es_client.indices.create(index=INDEX_NAME, body=index_settings)


def index_documents(documents, es_client, embedding_model):
    for i, doc in enumerate(tqdm(documents)):
        question = doc["question"]
        text = doc["text"]
        question_text = question + " " + text

        doc["id"] = str(i)
        doc["question_text_vector"] = embedding_model.embed_query(question_text)

        es_client.index(index=INDEX_NAME, document=doc)


def main():
    es_client = Elasticsearch(ES_URL)
    embedding_model = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

    documents = load_documents()
    create_index(es_client)
    index_documents(documents, es_client, embedding_model)

    print("Indexed documents:", len(documents))


if __name__ == "__main__":
    main()
