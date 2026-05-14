# AGENTS.md — SalesPredict AI CRM

## Commands

### Backend (Poetry)
```bash
cd backend
poetry install                          # install deps
poetry run uvicorn app.main:app --reload # dev server
poetry run pytest                        # run all tests
poetry run pytest tests/unit/test_sale_repo.py::test_create_sale  # single test
poetry run ruff check .                  # lint
poetry run ruff check --fix .            # lint + auto-fix
poetry run black .                       # format
poetry run mypy .                        # type check
poetry run alembic revision --autogenerate -m "msg"  # migration
poetry run alembic upgrade head           # apply migrations
```

### Frontend (pnpm only — no npm/yarn)
```bash
cd frontend
pnpm install
pnpm dev
pnpm build
pnpm lint
```

### ML Pipelines (Poetry)
```bash
cd ml-pipelines
poetry install
poetry run python training/train_xgboost.py
```

## Code Style

### Python
- **Formatter**: Black (line length 100).
- **Linter**: Ruff (`E`, `F`, `I`, `N`, `W`, `UP`, `B`, `C4`, `SIM`).
- **Types**: Strict mypy (`disallow_untyped_defs = true`). Use `X | None`, never `Optional[X]`. Avoid `Any`.
- **Imports**: stdlib → third-party → local. Ruff sorts automatically.
- **Naming**: `snake_case` for functions/variables, `PascalCase` for classes, `UPPER_SNAKE` for constants.

### TypeScript / React
- **Formatter/Linter**: Use Next.js built-in ESLint config.
- **Types**: Strict TypeScript. No `any` without explicit comment.
- **Naming**: `PascalCase` for components/types, `camelCase` for functions/variables, `kebab-case` for files.

## Architecture Rules

### Backend (Clean Architecture)
Maintain strict layer separation:
1. `app/api/` — routers only. Validate with Pydantic V2 schemas, inject deps, return responses. Never put business logic here.
2. `app/services/` — business logic. Orchestrate repositories, handle rules.
3. `app/infrastructure/repositories/` — data access. Use async SQLAlchemy 2.0 + `asyncpg`. Never sync sessions.
4. `app/infrastructure/db/models/` — ORM models.
5. `app/domain/` — pure domain entities and value objects (no framework imports).
6. `app/schemas/` — Pydantic V2 models for API I/O.
7. `app/tasks/` — Celery tasks for background/ETL work.

- Use `Annotated[..., Depends(...)]` for FastAPI dependency injection.
- Raise custom domain exceptions in services (`app/core/exceptions.py`). Convert to HTTPException only inside routers or exception handlers.
- All database interactions must be async. Never use synchronous SQLAlchemy drivers.

### Frontend (Next.js 15 App Router)
- Use App Router exclusively. No `pages/` directory.
- Prefer React Server Components and native `fetch`. Use Server Actions for mutations.
- **Zero TanStack**: No React Query, no TanStack Table. Use native `useState`/`useEffect` or custom hooks when client-side state is unavoidable.
- UI: Tailwind CSS + shadcn/ui primitives + Tremor for dashboards.
- Styling: utility-first Tailwind. No inline styles unless dynamic.

### ML Pipelines
- Keep training scripts separate from backend inference code.
- Log all experiments, metrics, and artifacts to MLflow.
- Use Pandas/NumPy for feature engineering, XGBoost/scikit-learn for models.
- Save/load models via MLflow registry; never hardcode model paths.

## General
- Add comments only when logic is non-obvious. No docstring requirement for internal helpers.
- Never commit secrets (`.env`, credentials). Use `.env.example` for templates.
- Never use `npm` or `yarn` in the frontend; only `pnpm`.
- Prefer native implementations over heavy third-party dependencies.
- WebSocket communication should use async patterns on both backend and frontend.
