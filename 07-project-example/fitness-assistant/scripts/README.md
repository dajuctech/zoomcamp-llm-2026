# Helper Scripts

Run these commands from the `fitness-assistant` folder.

Start the project services first:

```bash
docker compose --env-file ../../.env up -d
```

Initialize the PostgreSQL tables:

```bash
UV_CACHE_DIR=.uv-cache uv run python scripts/init_db.py
```

Send one test question to the Flask API:

```bash
UV_CACHE_DIR=.uv-cache uv run python scripts/test_api.py "What exercise can I do for chest?"
```

Send a question and save user feedback:

```bash
UV_CACHE_DIR=.uv-cache uv run python scripts/test_api.py "What exercise can I do for chest?" --feedback 1
```

Check the latest database rows:

```bash
UV_CACHE_DIR=.uv-cache uv run python scripts/check_db.py
```

`test_api.py` calls the running Flask API, so it uses the OpenAI API through the app.
