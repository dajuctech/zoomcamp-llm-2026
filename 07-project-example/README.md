# Fitness Assistant

This project follows Module 7 of LLM Zoomcamp as one end-to-end project example.

It starts with a generated fitness exercise dataset, builds a RAG assistant, evaluates retrieval and answers, exposes the assistant through Flask, logs usage to PostgreSQL, collects feedback, and shows monitoring data in Grafana.

## Project Flow

```text
generate exercise data
-> build minsearch index
-> retrieve exercise records
-> build prompt
-> call OpenAI
-> evaluate retrieval
-> evaluate RAG answers
-> expose Flask API
-> save conversations and feedback
-> monitor with Grafana
```

## Tech Stack

- Python
- uv
- Jupyter
- OpenAI API
- Pydantic
- minsearch
- Flask
- PostgreSQL
- Grafana
- Docker Compose

## Project Structure

```text
fitness-assistant/
├── data/
│   ├── data.csv
│   ├── ground-truth-retrieval.csv
│   ├── retrieval-evaluation-results.csv
│   └── rag-eval-gpt-5.4-mini.csv
├── notebooks/
│   ├── 01_generate_dataset.ipynb
│   ├── 02_build_rag.ipynb
│   ├── 03_evaluate_retrieval.ipynb
│   └── 04_evaluate_rag.ipynb
├── fitness_assistant/
│   ├── ingest.py
│   ├── rag.py
│   └── db.py
├── grafana/
│   ├── dashboard.json
│   └── init.py
├── scripts/
│   ├── init_db.py
│   ├── test_api.py
│   ├── check_db.py
│   └── README.md
├── app.py
├── Dockerfile
├── docker-compose.yaml
├── .env.example
└── README.md
```

## Environment

Use the shared course virtual environment from the course root:

```bash
source .venv/bin/activate
```

Create a `.env` file in the course root with:

```text
OPENAI_API_KEY=your_openai_api_key_here
```

Do not commit the real `.env` file.

## Notebooks

Run the notebooks in order:

```text
01_generate_dataset.ipynb
02_build_rag.ipynb
03_evaluate_retrieval.ipynb
04_evaluate_rag.ipynb
```

The notebook flow is:

- generate structured exercise records
- save `data/data.csv`
- build the first RAG flow
- generate ground truth questions
- evaluate retrieval with Hit Rate and MRR
- evaluate RAG answers with LLM-as-a-judge

## Evaluation Results

Retrieval evaluation:

| Run | Hit Rate | MRR |
| --- | ---: | ---: |
| Baseline | 1.0000 | 0.9403 |
| Tuned validation | 1.0000 | 0.7241 |
| Tuned test | 1.0000 | 0.9028 |

RAG answer evaluation:

```text
RELEVANT: 19
PARTLY_RELEVANT: 1
NON_RELEVANT: 0
```

The retrieval results are saved in:

```text
data/retrieval-evaluation-results.csv
```

The RAG judge results are saved in:

```text
data/rag-eval-gpt-5.4-mini.csv
```

## Run With Docker Compose

From this project folder:

```bash
docker compose --env-file ../../.env up -d --build
```

Initialize the database:

```bash
docker compose --env-file ../../.env exec -T app python -m fitness_assistant.db
```

The services are:

```text
app       -> http://localhost:5001
postgres  -> localhost:5432
grafana   -> http://localhost:3000
```

If port `3000` is already busy, start Grafana on another port:

```bash
GRAFANA_PORT=3001 docker compose --env-file ../../.env up -d --build
```

## Test The API

Ask a question:

```bash
curl -X POST http://localhost:5001/question \
  -H "Content-Type: application/json" \
  -d '{"question": "What exercise can I do for chest?"}'
```

The response includes:

- answer
- conversation ID
- response time
- token usage
- relevance label
- relevance explanation
- OpenAI cost

Send feedback using the `conversation_id` returned by `/question`:

```bash
curl -X POST http://localhost:5001/feedback \
  -H "Content-Type: application/json" \
  -d '{"conversation_id": "PASTE_CONVERSATION_ID", "feedback": 1}'
```

Use:

```text
1  -> useful answer
-1 -> not useful answer
```

## Check PostgreSQL

```bash
docker exec -i fitness-assistant-postgres psql -U user -d fitness_assistant \
  -c "SELECT id, question, relevance, openai_cost FROM conversations ORDER BY timestamp DESC LIMIT 5;"
```

```bash
docker exec -i fitness-assistant-postgres psql -U user -d fitness_assistant \
  -c "SELECT id, conversation_id, feedback FROM feedback ORDER BY timestamp DESC LIMIT 5;"
```

## Helper Scripts

The `scripts/` folder contains small commands for repeated project tasks.

Initialize the database tables:

```bash
UV_CACHE_DIR=.uv-cache uv run python scripts/init_db.py
```

Send a test question to the running Flask API:

```bash
UV_CACHE_DIR=.uv-cache uv run python scripts/test_api.py "What exercise can I do for chest?"
```

Send a test question and save feedback:

```bash
UV_CACHE_DIR=.uv-cache uv run python scripts/test_api.py "What exercise can I do for chest?" --feedback 1
```

Check recent PostgreSQL rows:

```bash
UV_CACHE_DIR=.uv-cache uv run python scripts/check_db.py
```

## Load Grafana Dashboard

After Docker Compose is running, load the Grafana data source and dashboard:

```bash
UV_CACHE_DIR=.uv-cache uv run python grafana/init.py
```

Open:

```text
http://localhost:3000/d/fitness-assistant-monitoring/fitness-assistant-monitoring
```

Default Grafana login:

```text
username: admin
password: admin
```

The dashboard shows:

- response time over time
- OpenAI cost over time
- token usage over time
- model usage
- judge relevance
- user feedback
- recent conversations

## Chunking Guidance

The fitness dataset is already structured, so each exercise record can be indexed directly.

For longer content, such as articles, transcripts, books, images, or slides, Module 7 recommends chunking first.

Basic chunking flow:

```text
long document
-> split into chunks
-> assign doc_id and chunk_id
-> index chunks
-> retrieve relevant chunks
-> build prompt from retrieved chunks
```

Useful IDs:

```json
{
  "doc_id": "article_001",
  "chunk_id": "article_001_01",
  "text": "chunk text here"
}
```

For retrieval evaluation, check both:

- document-level Hit Rate
- chunk-level Hit Rate

Simple chunking splits by size or paragraphs. Logical chunking uses an LLM to split text into meaningful blocks.

## Troubleshooting

If the API fails, check that Docker Compose is running:

```bash
docker compose ps
```

If the database tables are missing, run:

```bash
docker compose --env-file ../../.env exec -T app python -m fitness_assistant.db
```

If Grafana shows no data:

- ask at least one question through `/question`
- send feedback through `/feedback`
- check the dashboard time range
- check that the Postgres data source is connected

If port `5000` is busy locally, this project maps the app to port `5001`.

## Stop The Project

```bash
docker compose down
```
