from data_loader import load_documents
from search_engine import create_index
from rag import rag
from agent import agent_loop, instructions


def main():
    documents = load_documents()
    index = create_index(documents)

    question = "I just discovered the course. Can I still join it?"

    print("QUESTION:")
    print(question)
    print()

    print("PLAIN RAG ANSWER:")
    answer = rag(question, index)
    print(answer)
    print()

    print("AGENTIC RAG ANSWER:")
    agent_answer = agent_loop(index, instructions, question)
    print(agent_answer)


if __name__ == "__main__":
    main()