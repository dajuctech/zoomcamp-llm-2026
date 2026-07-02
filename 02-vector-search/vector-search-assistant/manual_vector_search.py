from sentence_transformers import SentenceTransformer
from tqdm.auto import tqdm
import numpy as np

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

query = "Can I still join the course after the start date?"
v_query = model.encode(query)

scores = X.dot(v_query)

top5 = np.argsort(-scores)[:5]

for idx in top5:
    print(scores[idx])
    print(documents[idx])
    print()