import time
from concurrent.futures import as_completed

from tqdm.auto import tqdm

from rag_helper import RAGBase


def llm_structured(client, instructions, user_prompt, output_type, model="gpt-5.4-mini"):
    response = client.responses.parse(
        model=model,
        input=[
            {"role": "developer", "content": instructions},
            {"role": "user", "content": user_prompt},
        ],
        text_format=output_type,
    )

    return response.output_parsed, response.usage


def llm_structured_retry(
    client,
    instructions,
    user_prompt,
    output_type,
    model="gpt-5.4-mini",
    max_tries=3,
):
    last_exception = None

    for attempt in range(max_tries):
        try:
            return llm_structured(
                client,
                instructions,
                user_prompt,
                output_type,
                model=model,
            )
        except Exception as e:
            last_exception = e
            time.sleep(2)

    raise last_exception


def calc_price(usage, input_price=0.00000015, output_price=0.0000006):
    return usage.input_tokens * input_price + usage.output_tokens * output_price


def calc_total_price(usages, input_price=0.00000015, output_price=0.0000006):
    total = 0

    for usage in usages:
        total = total + calc_price(
            usage,
            input_price=input_price,
            output_price=output_price,
        )

    return total


def map_progress(pool, seq, f):
    futures = []

    for el in seq:
        future = pool.submit(f, el)
        futures.append(future)

    results = []

    for future in tqdm(as_completed(futures), total=len(futures)):
        result = future.result()
        results.append(result)

    return results


def compute_relevance(q, search_function):
    doc_id = q["document"]
    results = search_function(query=q["question"])

    relevance = []

    for doc in results:
        relevance.append(int(doc["id"] == doc_id))

    return relevance


def compute_relevance_total(ground_truth, search_function):
    relevance_total = []

    for q in tqdm(ground_truth):
        relevance = compute_relevance(q, search_function)
        relevance_total.append(relevance)

    return relevance_total


def hit_rate(relevance):
    cnt = 0

    for line in relevance:
        if 1 in line:
            cnt = cnt + 1

    return cnt / len(relevance)


def mrr(relevance):
    total_score = 0.0

    for line in relevance:
        for rank in range(len(line)):
            if line[rank] == 1:
                total_score = total_score + 1 / (rank + 1)
                break

    return total_score / len(relevance)


def evaluate(ground_truth, search_function):
    relevance_total = compute_relevance_total(ground_truth, search_function)

    return {
        "hit_rate": hit_rate(relevance_total),
        "mrr": mrr(relevance_total),
    }


class RAGWithUsage(RAGBase):
    def search(self, query, num_results=5):
        boost_dict = {
            "question": 1.0,
            "answer": 2.0,
            "section": 0.1,
        }

        filter_dict = {"course": self.course}

        return self.index.search(
            query,
            num_results=num_results,
            boost_dict=boost_dict,
            filter_dict=filter_dict,
        )

    def llm(self, prompt):
        input_messages = [
            {"role": "developer", "content": self.instructions},
            {"role": "user", "content": prompt},
        ]

        response = self.llm_client.responses.create(
            model=self.model,
            input=input_messages,
        )

        return response

    def rag(self, query):
        search_results = self.search(query)
        prompt = self.build_prompt(query, search_results)
        response = self.llm(prompt)

        return response.output_text, response.usage

