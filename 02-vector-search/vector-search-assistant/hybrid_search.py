from gitsource import GithubRepositoryDataReader, chunk_documents
from minsearch import Index, VectorSearch
from tqdm.auto import tqdm
import numpy as np

from embedder import Embedder


reader = GithubRepositoryDataReader(
    repo_owner="DataTalksClub",
    repo_name="llm-zoomcamp",
    commit_id="8c1834d",
    allowed_extensions={"md"},
    filename_filter=lambda path: "/lessons/" in path,
)

documents = [file.parse() for file in reader.read()]

chunks = chunk_documents(documents, size=2000, step=1000)

embed = Embedder()

texts = []

for doc in chunks:
    texts.append(doc["content"])

batch_size = 50
vectors = []

for i in tqdm(range(0, len(texts), batch_size)):
    batch = texts[i:i + batch_size]
    batch_vectors = embed.encode_batch(batch)
    vectors.extend(batch_vectors)

X = np.array(vectors)

vindex = VectorSearch(keyword_fields=[])
vindex.fit(X, chunks)

text_index = Index(
    text_fields=["content"],
    keyword_fields=[]
)

text_index.fit(chunks)


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


query = "How do I give the model access to tools?"

query_vector = embed.encode(query)

vector_results = vindex.search(
    query_vector,
    num_results=5
)

text_results = text_index.search(
    query,
    boost_dict={"content": 1.0},
    num_results=5
)

results = rrf([vector_results, text_results])

print("VECTOR RESULTS")
for doc in vector_results:
    print(doc["filename"], doc["start"])

print()
print("TEXT RESULTS")
for doc in text_results:
    print(doc["filename"], doc["start"])

print()
print("HYBRID RESULTS")
for doc in results:
    print(doc["filename"], doc["start"])