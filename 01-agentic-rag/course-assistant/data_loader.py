import requests


def load_documents():
    docs_url = "https://datatalks.club/faq/json/courses.json"

    response = requests.get(docs_url)
    response.raise_for_status()

    courses_raw = response.json()

    documents = []
    url_prefix = "https://datatalks.club/faq"

    for course in courses_raw:
        course_url = f"{url_prefix}{course['path']}"

        course_response = requests.get(course_url)
        course_response.raise_for_status()

        course_data = course_response.json()
        documents.extend(course_data)

    return documents


if __name__ == "__main__":
    documents = load_documents()

    print(f"Loaded documents: {len(documents)}")
    print(documents[0])