# Course Assistant Monitoring Summary

## Project Overview

This project builds a monitored RAG course assistant for LLM Zoomcamp questions.

The assistant answers course-related questions, records each interaction, stores monitoring data in PostgreSQL, and shows the results in Streamlit and Grafana dashboards.

## What Was Built

The project includes:

- a RAG assistant
- a Streamlit chat app
- response-time tracking
- token usage tracking
- cost tracking
- PostgreSQL logging
- user feedback with thumbs up and thumbs down
- LLM-as-a-judge relevance feedback
- a Streamlit monitoring dashboard
- a Grafana monitoring dashboard
- Docker Compose for PostgreSQL, Grafana, and the app

## Monitoring Flow

The monitoring flow is:

```text
user question
-> RAG search
-> prompt building
-> LLM answer
-> metrics captured
-> conversation saved
-> user feedback saved
-> judge feedback saved
-> dashboard updated
```

## Metrics Captured

Each conversation stores:

- question
- answer
- model
- prompt
- instructions
- prompt tokens
- completion tokens
- total tokens
- response time
- cost
- timestamp

These metrics help track both usage and performance.

## Feedback Captured

The project captures two types of feedback.

User feedback:

```text
+1 = useful answer
-1 = not useful answer
```

Judge feedback:

```text
RELEVANT
PARTLY_RELEVANT
NON_RELEVANT
```

The judge checks whether the generated answer is relevant to the question.

## Dashboards

The project captures dashboards at three levels.

Level 1 is the chat app output.

It shows the result of one question immediately:

- answer
- response time
- token usage
- cost
- conversation ID
- judge relevance
- user feedback buttons

Level 2 is the Streamlit monitoring dashboard.

It summarizes saved conversations:

- total conversations
- average response time
- total cost
- average tokens
- cost over time
- response time over time
- judge relevance
- user feedback
- recent conversations

Level 3 is the Grafana dashboard.

It shows the same monitoring data with SQL-based panels:

- response time over time
- cost over time
- token usage
- model usage
- judge relevance distribution
- user feedback distribution
- recent conversations table

## Dashboard Screenshots

Chat app:

![Chat app](../images/chat-app.png)

Streamlit monitoring dashboard:

![Streamlit dashboard](../images/streamlit-dashboard.png)

Grafana dashboard:

![Grafana dashboard](../images/grafana-dashboard.png)

## Docker Compose

Docker Compose runs:

- PostgreSQL
- Grafana
- Streamlit app

This makes the project easier to run as one complete monitoring stack.

## Key Learning

The main lesson from this module is that building a RAG app is not enough.

After users start asking questions, we need to monitor:

- how fast the app responds
- how much it costs
- how many tokens it uses
- whether users like the answers
- whether the answers are relevant

Monitoring helps us understand how the assistant behaves in real usage.
