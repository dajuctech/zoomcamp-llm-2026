from embedder import Embedder
from ingest import load_faq_data
from tqdm.auto import tqdm
import numpy as np


embed = Embedder()

q1 = "Can I still join the course after the start date?"
q2 = "How to install Docker on Windows?"
d = "You don't need to register. You're accepted. You can also just start learning and submitting homework without registering."

v1 = embed.encode(q1)
v2 = embed.encode(q2)
dv = embed.encode(d)

print(v1.dot(dv))
print(v2.dot(dv))

documents = load_faq_data()

texts = []

for doc in documents:
    text = doc["question"] + " " + doc["answer"]
    texts.append(text)

batch_size = 50
X = []

for i in tqdm(range(0, len(texts), batch_size)):
    batch = texts[i:i + batch_size]
    batch_vectors = embed.encode_batch(batch)
    X.extend(batch_vectors)

X = np.array(X)

query = "Can I still join the course after the start date?"
v_query = embed.encode(query)

scores = X.dot(v_query)

top5 = np.argsort(-scores)[:5]

for idx in top5:
    print(scores[idx])
    print(documents[idx])
    print()