from sentence_transformers import SentenceTransformer
from tqdm.auto import tqdm
import numpy as np
from minsearch import VectorSearch

from ingest import load_faq_data


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

query = "I just discovered the course. Can I still join it?"
query_vector = model.encode(query)

results = vindex.search(
    query_vector,
    filter_dict={"course": "llm-zoomcamp"},
    num_results=5,
)

for doc in results:
    print(doc)
    print()