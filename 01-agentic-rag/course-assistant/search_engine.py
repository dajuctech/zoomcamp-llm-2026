from minsearch import Index
from data_loader import load_documents


def create_index(documents):
    index = Index(
        text_fields=["question", "section", "answer"],
        keyword_fields=["course"]
    )

    index.fit(documents)
    return index


def search(index, question, course="llm-zoomcamp"):
    boost_dict = {
        "question": 2.0,
        "section": 0.5
    }

    filter_dict = {
        "course": course
    }

    results = index.search(
        question,
        boost_dict=boost_dict,
        filter_dict=filter_dict,
        num_results=5
    )

    return results


if __name__ == "__main__":
    documents = load_documents()
    print(f"Loaded documents: {len(documents)}")

    index = create_index(documents)

    question = "I just discovered the course. Can I join now?"

    results = search(index, question)

    for result in results:
        print(result["question"])