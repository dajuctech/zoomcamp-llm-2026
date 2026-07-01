from config import client, MODEL
from data_loader import load_documents
from search_engine import create_index


INSTRUCTIONS = """
Your task is to answer questions from the course participants
based on the provided context.

Use the context to find relevant information and provide accurate
answers. If the answer is not found in the context,
respond with "I don't know."
"""

USER_PROMPT_TEMPLATE = """
Question:
{question}

Context:
{context}
"""


def search(index, question, course="llm-zoomcamp", num_results=5):
    boost_dict = {
        "question": 3.0,
        "section": 0.5
    }

    filter_dict = {
        "course": course
    }

    return index.search(
        question,
        boost_dict=boost_dict,
        filter_dict=filter_dict,
        num_results=num_results
    )


def build_context(search_results):
    lines = []

    for doc in search_results:
        lines.append(doc["section"])
        lines.append("Q: " + doc["question"])
        lines.append("A: " + doc["answer"])
        lines.append("")

    return "\n".join(lines).strip()


def build_prompt(question, search_results):
    context = build_context(search_results)

    prompt = USER_PROMPT_TEMPLATE.format(
        question=question,
        context=context
    )

    return prompt.strip()


def llm(instructions, user_prompt, model=MODEL):
    message_history = [
        {"role": "developer", "content": instructions},
        {"role": "user", "content": user_prompt}
    ]

    response = client.responses.create(
        model=model,
        input=message_history
    )

    return response.output_text


def rag(query, index, model=MODEL):
    search_results = search(index, query)
    prompt = build_prompt(query, search_results)
    answer = llm(INSTRUCTIONS, prompt, model=model)

    return answer


if __name__ == "__main__":
    documents = load_documents()
    index = create_index(documents)

    answer = rag(
        "I just discovered the course. Can I join now?",
        index
    )

    print(answer)