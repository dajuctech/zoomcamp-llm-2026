import json

from config import client, MODEL
from data_loader import load_documents
from search_engine import create_index


search_tool = {
    "type": "function",
    "name": "search",
    "description": "Search the FAQ database for entries matching the given query.",
    "parameters": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "Search query text to look up in the course FAQ."
            }
        },
        "required": ["query"],
        "additionalProperties": False
    }
}


def search(index, query):
    boost_dict = {
        "question": 3.0,
        "section": 0.5
    }

    filter_dict = {
        "course": "llm-zoomcamp"
    }

    return index.search(
        query,
        num_results=5,
        boost_dict=boost_dict,
        filter_dict=filter_dict
    )


if __name__ == "__main__":
    documents = load_documents()
    index = create_index(documents)

    messages = [
        {
            "role": "user",
            "content": "I just discovered the course. Can I join it?"
        }
    ]

    response = client.responses.create(
        model=MODEL,
        input=messages,
        tools=[search_tool],
    )

    print("First response:")
    print(response.output)

    call = response.output[0]

    if call.type != "function_call":
        print(response.output_text)
        raise SystemExit

    args = json.loads(call.arguments)

    results = search(index, **args)
    result_json = json.dumps(results, indent=2)

    messages.extend(response.output)

    messages.append({
        "type": "function_call_output",
        "call_id": call.call_id,
        "output": result_json,
    })

    response = client.responses.create(
        model=MODEL,
        input=messages,
        tools=[search_tool],
    )

    print("Final answer:")
    print(response.output_text)