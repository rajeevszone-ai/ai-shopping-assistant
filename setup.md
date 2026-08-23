# Project Setup

This guide describes the supported local setup for Windows 10/11 and VS Code.

## Prerequisites

- Git for Windows
- Python 3.11 or newer, installed from [python.org](https://www.python.org/downloads/windows/)
- `uv`, installed using the [official Windows instructions](https://docs.astral.sh/uv/getting-started/installation/)
- VS Code with the Python, Pylance, and Ruff extensions
- PowerShell 5.1 or newer

During Python installation, enable **Add Python to PATH**. Confirm the installation in a new PowerShell window:

```powershell
python --version
uv --version
```

## Create and sync the environment with uv

From the repository root:

```powershell
uv venv --python 3.11
uv sync --dev
```

`uv sync` creates or updates `.venv` and installs the project with its development dependency group from `pyproject.toml` and `uv.lock`. Prefer `uv run ...` so commands always use the synchronized environment; activation is optional.

If you prefer an activated PowerShell session, or if PowerShell blocks activation, allow scripts for the current Windows user:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then activate the environment again. The `.venv` directory is local-only and is excluded from Git.

## Configure VS Code

1. Open the repository folder in VS Code.
2. Run **Python: Select Interpreter**.
3. Choose `.venv\Scripts\python.exe`.
4. Open the Testing view and confirm that `tests/test_smoke.py` is discovered.
5. Accept the recommended extensions when VS Code prompts.

The checked-in `.vscode/settings.json` configures `src` imports, pytest discovery, Ruff formatting, and import cleanup.

## Verify the setup

```powershell
uv sync --dev
uv run pytest
uv run shopping-assistant
```

For the full quality gate, also run:

```powershell
uv run ruff check .
uv run ruff format --check .
uv run mypy src
```

The expected application output is:

```text
AI Shopping Assistant is ready.
```

## Environment variables

Copy `.env.example` to `.env` for local values. Do not commit `.env` or credentials. When integrations are introduced, document variable names and safe example values in `.env.example`.

## Git initialization and first push

```powershell
git init
git add .
git commit -m "chore: initialize AI shopping assistant"
git branch -M main
git remote add origin https://github.com/<owner>/<repository>.git
git push -u origin main
```

## Dataset
[McAuley-Lab/Amazon-Reviews-2023 under the Sports_and_Outdoors category](https://huggingface.co/datasets/McAuley-Lab/Amazon-Reviews-2023/blob/main/raw/meta_categories/meta_Sports_and_Outdoors.jsonl)
[Reviews](https://huggingface.co/datasets/McAuley-Lab/Amazon-Reviews-2023/blob/main/raw/review_categories/Sports_and_Outdoors.jsonl)

Review `git diff --cached` before committing. Never commit API keys, access tokens, customer data, local databases, or the `.venv` directory.
