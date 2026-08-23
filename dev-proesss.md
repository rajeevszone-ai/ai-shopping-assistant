# Development Process

This document records the repeatable process used to develop the AI Shopping Assistant.

## 1. Define the outcome

Capture the user problem, target shopper, supported shopping journey, non-functional requirements, and measurable acceptance criteria. Record unknowns rather than silently choosing behavior that will be difficult to change later.

## 2. Choose the smallest vertical slice

Create one user-facing capability that can be exercised end to end. Start with a domain model and application use case, then add the API and infrastructure adapters required by that slice.

## 3. Design the boundary

Keep vendor-specific concerns behind interfaces or ports. The domain must not import web frameworks, database clients, or LLM SDKs. Define typed inputs and outputs at each boundary.

## 4. Implement with tests

Write unit tests for business rules first, integration tests for real adapters, and contract tests for external APIs. Add a regression test whenever a defect is found. Keep tests deterministic and never use real customer data.

## 5. Run local quality checks

Before opening a pull request, run:

```powershell
uv sync --dev
uv run pytest --cov
uv run ruff check .
uv run ruff format --check .
uv run mypy src
```

`uv.lock` is committed so local development and CI resolve the same dependency versions. Update it intentionally with `uv lock` when dependencies change, then review the resulting diff.

Use a local `.env` for credentials and verify that it remains ignored by Git.

## 6. Review security and privacy

Treat prompts, product data, user profiles, and conversation history as potentially sensitive. Minimize retained data, validate input, redact secrets from logs, set provider timeouts, and review dependencies before adoption.

## 7. Integrate through a pull request

Use a focused branch and commit messages that describe intent. A pull request should include the behavior change, tests, operational impact, configuration changes, and known limitations. Keep CI required before merging.

## 8. Release deliberately

Tag releases from a clean main branch. Record breaking changes, migrations, model or prompt changes, dependency updates, and rollback instructions. Deploy with environment-specific configuration supplied by the runtime, never from committed secrets.

## 9. Operate and learn

Monitor latency, failures, cost, retrieval quality, recommendation quality, and user feedback. Create representative evaluation datasets for assistant responses and rerun them when prompts, models, catalog sources, or ranking logic change.

## Initial implementation status

The repository currently provides the package boundary, command-line entry point, development dependencies, quality configuration, VS Code configuration, and a smoke test. The next implementation slice should establish the domain and application contracts for a single shopping conversation before connecting a model provider or product catalog.
