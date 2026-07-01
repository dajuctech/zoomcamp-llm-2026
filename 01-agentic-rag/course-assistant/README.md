# Agentic RAG Course Assistant

This project is a small Agentic RAG course assistant.

The goal is to build a course assistant that answers questions using the DataTalksClub FAQ dataset.

The project starts with plain RAG:

```text
question -> search -> context -> prompt -> LLM answer
```

Then it becomes agentic RAG:

```text
question -> LLM decides to search -> Python runs search -> LLM reads result -> final answer
```

## Project Folder

This project lives here:

```text
01-agentic-rag/course-assistant/
```

## Files

```text
course-assistant/
  README.md
  project_notebook.ipynb
  config.py
  data_loader.py
  search_engine.py
  rag.py
  tools.py
  agent.py
  app.py
```

## What Each File Does

### `config.py`

Function:

```text
Loads environment variables and creates the OpenAI client.
```

Important idea:

```text
The API key lives in .env, not inside the code.
```

The `.env` file is here:

```text
zoomcamp-llm-2026/.env
```

### `data_loader.py`

Function:

```text
Downloads the FAQ dataset from DataTalksClub.
```

Uses:

```text
requests
```

Loads data from:

```text
https://datatalks.club/faq/json/courses.json
```

Beginner meaning:

```text
This file creates the knowledge base.
```

### `search_engine.py`

Function:

```text
Builds a minsearch index and searches FAQ documents.
```

Uses:

```text
from minsearch import Index
```

Search fields:

```text
question
section
answer
```

Filter field:

```text
course = llm-zoomcamp
```

Beginner meaning:

```text
This file finds useful FAQ entries before asking the LLM.
```

### `rag.py`

Function:

```text
Runs plain RAG.
```

Plain RAG flow:

```text
question -> search -> context -> prompt -> LLM answer
```

Uses:

```text
INSTRUCTIONS
USER_PROMPT_TEMPLATE
build_context()
build_prompt()
client.responses.create()
response.output_text
```

Important:

```text
This project uses the OpenAI Responses API from the module.
It does not use chat.completions.create().
```

Beginner meaning:

```text
This file makes the LLM answer using retrieved FAQ context.
```

### `tools.py`

Function:

```text
Defines search as a tool that the LLM can request.
```

Uses:

```text
search_tool dictionary
response.output
json.loads(call.arguments)
function_call_output
```

Beginner meaning:

```text
The model cannot run Python by itself.
It asks for a tool call, then Python runs the function.
```

### `agent.py`

Function:

```text
Runs the agentic loop.
```

Agentic loop:

```text
model response -> tool call -> tool result -> next model response
```

Beginner meaning:

```text
The LLM decides when to search and when it has enough information to answer.
```

### `app.py`

Function:

```text
Runs the complete project from one file.
```

It shows:

```text
plain RAG answer
agentic RAG answer
```

### `project_notebook.ipynb`

Function:

```text
Tests and explains the project step by step.
```

Use this notebook for learning:

```text
load documents
build index
test search
build context
build prompt
call LLM
run plain RAG
test function calling
run agentic loop
compare plain RAG and agentic RAG
```

Important:

```text
The notebook should import from the .py files.
The final logic should stay in the .py files.
```

## How To Run

Run commands from the project root:

```text
zoomcamp-llm-2026/
```

Go there:

```bash
cd zoomcamp-llm-2026
```

Run the full project:

```bash
uv run python 01-agentic-rag/course-assistant/app.py
```

Run each file separately:

```bash
uv run python 01-agentic-rag/course-assistant/data_loader.py
uv run python 01-agentic-rag/course-assistant/search_engine.py
uv run python 01-agentic-rag/course-assistant/rag.py
uv run python 01-agentic-rag/course-assistant/tools.py
uv run python 01-agentic-rag/course-assistant/agent.py
uv run python 01-agentic-rag/course-assistant/app.py
```

## Expected Output

When `app.py` works, you should see:

```text
QUESTION:
I just discovered the course. Can I still join it?

PLAIN RAG ANSWER:
Yes, you can still join the course...

AGENTIC RAG ANSWER:
iteration #1...
function_call: search {...}
iteration #2...
ASSISTANT:
Yes, you can still join the course...
```

## Plain RAG vs Agentic RAG

### Plain RAG

```text
Your code controls the flow.
Search happens first.
The LLM answers after receiving context.
```

Flow:

```text
question -> search -> prompt -> LLM -> answer
```

### Agentic RAG

```text
The LLM controls when to search.
Python runs the tool calls.
The loop stops when the LLM gives a final answer.
```

Flow:

```text
question -> LLM -> search tool -> result -> LLM -> final answer
```

## Concepts Covered

This project touches the main Module 1 concepts:

```text
environment variables
OpenAI client
FAQ dataset
knowledge base
search index
minsearch
boosting
filtering
context
prompt template
developer message
Responses API
plain RAG
function calling
tool schema
function_call_output
message history
agentic loop
```

## Common Errors And Fixes

### Wrong `uv` Command

Wrong:

```bash
uv python search_engine.py
```

Correct:

```bash
uv run python 01-agentic-rag/course-assistant/search_engine.py
```

`uv python` is for managing Python versions. `uv run python` runs a Python file inside the project environment.

### Missing `minsearch`

Error:

```text
ModuleNotFoundError: No module named 'minsearch'
```

Fix:

```bash
cd zoomcamp-llm-2026
uv sync
```

Then run files with:

```bash
uv run python 01-agentic-rag/course-assistant/search_engine.py
```

### Wrong `gitsource` API

Error:

```text
TypeError: GithubRepositoryDataReader.__init__() got an unexpected keyword argument 'org'
```

For this project, use the FAQ dataset code with `requests`, not `gitsource`.

### Running Python From The Wrong Folder

Wrong:

```bash
python search_engine.py
```

from:

```text
zoomcamp-llm-2026/
```

Correct:

```bash
uv run python 01-agentic-rag/course-assistant/search_engine.py
```

Or:

```bash
cd 01-agentic-rag/course-assistant
uv run python search_engine.py
```

### `tools.py` Missing `search_tool`

Error:

```text
ImportError: cannot import name 'search_tool' from 'tools'
```

Fix:

Make sure `tools.py` has `search_tool` at the top level, not inside:

```python
if __name__ == "__main__":
```

The variable should be importable like this:

```python
from tools import search_tool
```

### `.env` Not Found

If the OpenAI client cannot find your API key, confirm `.env` exists here:

```text
zoomcamp-llm-2026/.env
```

Run commands from the project root:

```bash
cd zoomcamp-llm-2026
```

## What To Do Next

After this project works:

```text
1. Use project_notebook.ipynb to explain each step.
2. Try more course questions.
3. Try typo questions like "How do I run Olama locally?"
4. Compare plain RAG and agentic RAG outputs.
5. Move to Module 2 vector search when ready.
```
