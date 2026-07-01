import json

from config import client, MODEL
from data_loader import load_documents
from search_engine import create_index
from tools import search_tool, search


instructions = """
You're a course teaching assistant.
You're given a question from a course student and your task is to answer it.

If you want to look up information, use the search function. 
Use as many keywords from the user question as possible when making first requests.

Make multiple searches. First perform search, analyze the results 
and then perform more searches. 

The question has to be about the course or its logistics, offtopic questions 
shouldn't be answered. If the search returns nothing, it's likely an off-topic question.
If you can't answer the question using FAQ, don't do it yourself. Only use the 
facts from the FAQ database.

At the end, ask if there are other areas that the user wants to explore.
""".strip()


def make_call(index, call):
    args = json.loads(call.arguments)

    if call.name == "search":
        result = search(index, **args)

    result_json = json.dumps(result, indent=2)

    return {
        "type": "function_call_output",
        "call_id": call.call_id,
        "output": result_json,
    }


def agent_loop(index, instructions, question, model=MODEL):
    messages = [
        {"role": "developer", "content": instructions},
        {"role": "user", "content": question}
    ]

    it = 1
    last_answer = None

    while True:
        print(f"iteration #{it}...")
        has_function_calls = False

        response = client.responses.create(
            model=model,
            input=messages,
            tools=[search_tool]
        )

        messages.extend(response.output)

        for item in response.output:
            if item.type == "function_call":
                print("function_call:", item.name, item.arguments)
                call_output = make_call(index, item)
                messages.append(call_output)
                has_function_calls = True

            elif item.type == "message":
                print("ASSISTANT:")
                last_answer = item.content[0].text
                print(item.content[0].text)

        it = it + 1

        if has_function_calls == False:
            break

    return last_answer


if __name__ == "__main__":
    documents = load_documents()
    index = create_index(documents)

    answer = agent_loop(
        index,
        instructions,
        "I just discovered the course. Can I still join it?"
    )

    print()
    print("FINAL ANSWER:")
    print(answer)