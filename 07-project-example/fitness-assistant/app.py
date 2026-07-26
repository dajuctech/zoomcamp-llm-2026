import uuid
import os

import psycopg
from flask import Flask, jsonify, request

from fitness_assistant.db import save_conversation, save_feedback
from fitness_assistant.rag import rag


app = Flask(__name__)


@app.route("/question", methods=["POST"])
def handle_question():
    data = request.get_json(silent=True) or {}
    question = data.get("question")

    if not question:
        return jsonify({"error": "No question provided"}), 400

    conversation_id = str(uuid.uuid4())
    answer_data = rag(question)
    save_conversation(conversation_id, question, answer_data)

    result = {
        "conversation_id": conversation_id,
        "question": question,
        "answer": answer_data["answer"],
        "model_used": answer_data["model_used"],
        "response_time": answer_data["response_time"],
        "relevance": answer_data["relevance"],
        "relevance_explanation": answer_data["relevance_explanation"],
        "prompt_tokens": answer_data["prompt_tokens"],
        "completion_tokens": answer_data["completion_tokens"],
        "total_tokens": answer_data["total_tokens"],
        "eval_prompt_tokens": answer_data["eval_prompt_tokens"],
        "eval_completion_tokens": answer_data["eval_completion_tokens"],
        "eval_total_tokens": answer_data["eval_total_tokens"],
        "openai_cost": answer_data["openai_cost"],
    }

    return jsonify(result)


@app.route("/feedback", methods=["POST"])
def handle_feedback():
    data = request.get_json(silent=True) or {}
    conversation_id = data.get("conversation_id")
    feedback = data.get("feedback")

    if not conversation_id or feedback not in [1, -1]:
        return jsonify({"error": "Invalid input"}), 400

    try:
        save_feedback(conversation_id, feedback)
    except psycopg.errors.ForeignKeyViolation:
        return jsonify({"error": "Conversation ID does not exist"}), 400

    return jsonify({"message": f"Feedback received: {feedback}"})


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    app.run(debug=True, host="0.0.0.0", port=port)
