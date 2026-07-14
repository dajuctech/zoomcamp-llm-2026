from ingest import build_index, load_faq_data


documents = load_faq_data()

documents_llm = []

for doc in documents:
    if doc["course"] == "llm-zoomcamp":
        documents_llm.append(doc)

documents = documents_llm
index = build_index(documents)

results = index.search(
    "Can I still join the course?",
    num_results=5,
    boost_dict={"question": 3.0, "section": 0.5},
)

print("documents:", len(documents))
print("first result:", results[0]["question"])
