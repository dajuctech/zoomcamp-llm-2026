from dotenv import load_dotenv
from openai import OpenAI
from sentence_transformers import SentenceTransformer
from tqdm.auto import tqdm
import numpy as np
from minsearch import VectorSearch

from ingest import load_faq_data
from rag_helper import RAGBase


load_dotenv()
openai_client = OpenAI()

model = SentenceTransformer("all-MiniLM-L6-v2")

documents = load_faq_data()

texts = []

for doc in documents:
    text = doc["question"] + " " + doc["answer"]
    texts.append(text)

batch_size = 50
vectors = []

for i in tqdm(range(0, len(texts), batch_size)):
    batch = texts[i:i + batch_size]
    batch_vectors = model.encode(batch)
    vectors.extend(batch_vectors)

X = np.array(vectors)

vindex = VectorSearch(keyword_fields=["course"])
vindex.fit(X, documents)


class RAGVector(RAGBase):

    def __init__(self, embedder, **kwargs):
        super().__init__(**kwargs)
        self.embedder = embedder

    def search(self, query, num_results=5):
        query_vector = self.embedder.encode(query)
        filter_dict = {"course": self.course}

        return self.index.search(
            query_vector,
            num_results=num_results,
            filter_dict=filter_dict
        )


vector_assistant = RAGVector(
    embedder=model,
    index=vindex,
    llm_client=openai_client,
)

query = "I just found out about the program, can I still sign up?"

answer = vector_assistant.rag(query)

print(answer)