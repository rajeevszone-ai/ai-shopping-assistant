# AI Shopping Assistant

A professional Python foundation for building an AI-powered shopping assistant. The codebase is organized for incremental evolution as product, conversation, catalog, recommendation, and integration capabilities are added.

## Quick start

```powershell
uv sync --dev
uv run pytest
uv run shopping-assistant
```

See [setup.md](setup.md) for complete Windows and VS Code setup instructions, [project-structure.md](project-structure.md) for the architecture, and [dev-proesss.md](dev-proesss.md) for the development workflow.

## Current status

The repository contains the initial package boundary, executable entry point, quality tooling, and smoke test. Domain and infrastructure modules should be added behind these boundaries as requirements become concrete.
