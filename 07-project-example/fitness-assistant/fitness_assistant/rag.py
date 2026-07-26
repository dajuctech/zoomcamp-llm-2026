import json
from pathlib import Path
from time import time

from dotenv import load_dotenv
from openai import OpenAI

from fitness_assistant import ingest


def find_course_root():
    current = Path(__file__).resolve()

    for path in [current, *current.parents]:
        if (path / "pyproject.toml").exists():
            return path

    return Path.cwd()


load_dotenv(find_course_root() / ".env")

openai_client = OpenAI()
index = ingest.load_index()

BOOST = {
    "exercise_name": 2.11,
    "type_of_activity": 1.46,
    "type_of_equipment": 0.65,
    "body_part": 2.65,
    "type": 1.31,
    "muscle_groups_activated": 2.54,
    "instructions": 0.74,
}


def search(query):
    results = index.search(
        query=query,
        filter_dict={},
        boost_dict=BOOST,
        num_results=10,
    )

    return results


prompt_template = """
You're a fitness instructor. Answer the QUESTION based on the CONTEXT from our exercises database.
Use only the facts from the CONTEXT when answering the QUESTION.

QUESTION: {question}

CONTEXT:
{context}
""".strip()


entry_template = """
exercise_name: {exercise_name}
type_of_activity: {type_of_activity}
type_of_equipment: {type_of_equipment}
body_part: {body_part}
type: {type}
muscle_groups_activated: {muscle_groups_activated}
instructions: {instructions}
""".strip()


evaluation_prompt_template = """
You are an expert evaluator for a RAG system.
Your task is to analyze the relevance of the generated answer to the given question.
Based on the relevance of the generated answer, classify it
as "NON_RELEVANT", "PARTLY_RELEVANT", or "RELEVANT".

Question: {question}
Generated Answer: {answer}

Return valid JSON without code blocks:

{{
  "Relevance": "NON_RELEVANT" | "PARTLY_RELEVANT" | "RELEVANT",
  "Explanation": "Brief explanation for the evaluation"
}}
""".strip()


def build_prompt(query, search_results):
    context = ""

    for doc in search_results:
        context = context + entry_template.format(**doc) + "\n\n"

    prompt = prompt_template.format(question=query, context=context).strip()
    return prompt


def llm(prompt, model="gpt-5.4-mini"):
    response = openai_client.responses.create(
        model=model,
        input=[{"role": "user", "content": prompt}],
    )

    answer = response.output_text
    token_stats = {
        "prompt_tokens": response.usage.input_tokens,
        "completion_tokens": response.usage.output_tokens,
        "total_tokens": response.usage.total_tokens,
    }

    return answer, token_stats


def evaluate_relevance(question, answer):
    prompt = evaluation_prompt_template.format(question=question, answer=answer)
    evaluation, tokens = llm(prompt, model="gpt-5.4-mini")

    try:
        json_eval = json.loads(evaluation)
        return json_eval, tokens
    except json.JSONDecodeError:
        result = {
            "Relevance": "UNKNOWN",
            "Explanation": "Failed to parse evaluation",
        }
        return result, tokens


def calculate_openai_cost(model, tokens):
    openai_cost = 0

    if "gpt-5.4-mini" in model:
        openai_cost = (
            tokens["prompt_tokens"] * 0.15
            + tokens["completion_tokens"] * 0.60
        ) / 1_000_000

    return openai_cost


def rag(query, model="gpt-5.4-mini"):
    t0 = time()

    search_results = search(query)
    prompt = build_prompt(query, search_results)
    answer, token_stats = llm(prompt, model=model)
    relevance, rel_token_stats = evaluate_relevance(query, answer)

    took = time() - t0
    openai_cost_rag = calculate_openai_cost(model, token_stats)
    openai_cost_eval = calculate_openai_cost(model, rel_token_stats)
    openai_cost = openai_cost_rag + openai_cost_eval

    return {
        "answer": answer,
        "model_used": model,
        "response_time": took,
        "relevance": relevance.get("Relevance", "UNKNOWN"),
        "relevance_explanation": relevance.get("Explanation", "Failed to parse"),
        "prompt_tokens": token_stats["prompt_tokens"],
        "completion_tokens": token_stats["completion_tokens"],
        "total_tokens": token_stats["total_tokens"],
        "eval_prompt_tokens": rel_token_stats["prompt_tokens"],
        "eval_completion_tokens": rel_token_stats["completion_tokens"],
        "eval_total_tokens": rel_token_stats["total_tokens"],
        "openai_cost": openai_cost,
    }
