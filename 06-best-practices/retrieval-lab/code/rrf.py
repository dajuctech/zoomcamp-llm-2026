def compute_rrf(rank, k=60):
    return 1 / (k + rank)


def reciprocal_rank_fusion(search_results, k=60, num_results=5):
    scores = {}
    documents = {}

    for results in search_results:
        for rank, doc in enumerate(results, start=1):
            doc_id = doc["id"]

            if doc_id not in scores:
                scores[doc_id] = 0
                documents[doc_id] = doc

            scores[doc_id] += compute_rrf(rank, k=k)

    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    return [documents[doc_id] for doc_id, _ in ranked[:num_results]]
