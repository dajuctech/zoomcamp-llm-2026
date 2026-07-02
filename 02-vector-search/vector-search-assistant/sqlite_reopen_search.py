from sentence_transformers import SentenceTransformer
from sqlitesearch import VectorSearchIndex


model = SentenceTransformer("all-MiniLM-L6-v2")

vs_index = VectorSearchIndex(
    keyword_fields=["course"],
    mode="ivf",
    db_path="02-vector-search/vector-search-assistant/faq_vectors2.db"
)

query = "How do I run Kafka?"
query_vector = model.encode(query)

results = vs_index.search(
    query_vector,
    filter_dict={"course": "llm-zoomcamp"},
    num_results=5
)

for doc in results:
    print(doc)
    print()

vs_index.close()
