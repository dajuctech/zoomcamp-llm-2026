def hit_rate(relevance_total):
    cnt = 0

    for line in relevance_total:
        if True in line:
            cnt = cnt + 1

    return cnt / len(relevance_total)


def mrr(relevance_total):
    total_score = 0.0

    for line in relevance_total:
        for rank, is_relevant in enumerate(line):
            if is_relevant:
                total_score = total_score + 1 / (rank + 1)
                break

    return total_score / len(relevance_total)


def evaluate(ground_truth, search_function):
    relevance_total = []

    for item in ground_truth:
        query = item["question"]
        course = item.get("course", "data-engineering-zoomcamp")
        expected_id = item.get("document") or item.get("id")

        results = search_function(query, course=course)
        relevance = [doc["id"] == expected_id for doc in results]

        relevance_total.append(relevance)

    return {
        "hit_rate": hit_rate(relevance_total),
        "mrr": mrr(relevance_total),
    }
