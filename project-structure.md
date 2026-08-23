# Project Structure

The project uses a `src` layout so installed-package behavior matches production behavior and accidental imports from the repository root are avoided.

```text
ai-shopping-assistant/
|-- .github/                         # CI and contribution automation (to be added)
|-- .vscode/
|   |-- extensions.json              # Recommended VS Code extensions
|   `-- settings.json                # Shared Python, pytest, and Ruff settings
|-- src/
|   `-- shopping_assistant/
|       |-- __init__.py              # Package identity and version
|       |-- main.py                  # CLI/application entry point
|       |-- api/                      # HTTP/API adapters and request schemas
|       |-- application/              # Use cases and orchestration services
|       |-- domain/                   # Business entities, value objects, and rules
|       |-- infrastructure/           # Databases, LLMs, search, and external services
|       |-- configuration/            # Typed settings and environment loading
|       `-- observability/            # Logging, tracing, and metrics
|-- tests/
|   |-- test_smoke.py                 # Initial package installation smoke test
|   |-- unit/                         # Fast isolated tests
|   |-- integration/                  # Tests crossing infrastructure boundaries
|   `-- contract/                     # External API and schema contract tests
|-- .env.example                      # Safe template for local configuration
|-- .gitignore                        # Files excluded from version control
|-- .pre-commit-config.yaml           # Local quality hooks
|-- LICENSE                           # MIT license
|-- README.md                         # Project overview and quick start
|-- dev-proesss.md                    # Development process and engineering workflow
|-- project-structure.md              # This architecture reference
|-- pyproject.toml                    # Build metadata, dependencies, and tool config
|-- uv.lock                           # Reproducible uv dependency resolution
`-- setup.md                           # Windows and VS Code setup instructions
```

## Architecture boundaries

- **API** translates transport concerns into application commands and responses.
- **Application** coordinates use cases without knowing HTTP, database, or vendor SDK details.
- **Domain** owns shopping behavior and remains independent of frameworks and integrations.
- **Infrastructure** implements ports defined by the application or domain, such as catalog search, persistence, and model providers.
- **Configuration** creates validated settings from environment variables.
- **Observability** provides consistent diagnostics without embedding logging policy in business rules.

New features should enter through an application use case, keep business rules in the domain, and depend on abstractions for external systems. The architecture is intentionally expandable: folders are boundaries, not commitments to implement every capability immediately.

## File documentation rule

Every new module should have one clear responsibility, tests should mirror the package boundary, and public behavior should be documented in the README or an appropriate design document. Keep secrets and customer data outside the repository.
