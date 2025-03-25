# Install Instructions

0. Export your API keys
For the default setup, you will need both MistralAI and OpenAI keys set as your env vars.

1. Install uv 
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. Install Python with uv and a virtual environment with all dependencies
```bash
    uv python install 3.11.11
    uv sync --all-groups
```

3. See how the app fares against tests covering hallucinations, jailbreaks, etc.
```bash
    uv run pytest -v
```
