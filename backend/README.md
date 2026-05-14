# SalesPredict Backend

FastAPI async backend with Clean Architecture.

## Quick Start

```bash
cd backend
cp .env.example .env
poetry install
poetry run uvicorn app.main:app --reload
```

## Docker

```bash
docker build -t salespredict-backend .
docker run -p 8000:8000 salespredict-backend
```

## Database Migrations

```bash
# Create migration
poetry run alembic revision --autogenerate -m "description"

# Apply migrations
poetry run alembic upgrade head

# Rollback
poetry run alembic downgrade -1
```

## Tests

```bash
# Run all tests
poetry run pytest

# Run single test
poetry run pytest tests/unit/test_sale_repo.py::test_create_sale

# With coverage
poetry run pytest --cov=app --cov-report=html
```

## Linting & Formatting

```bash
poetry run ruff check .          # lint
poetry run ruff check --fix .    # lint + auto-fix
poetry run black .               # format
poetry run mypy .                # type check
```

## Architecture

```
app/
├── api/          # FastAPI routers
├── core/         # Config, security, exceptions
├── domain/       # Pure domain entities
├── infrastructure/ # DB, repositories, external services
├── schemas/      # Pydantic V2 models
├── services/     # Business logic
└── tasks/        # Celery background tasks
```

## Environment Variables

See `.env.example` for all required variables.
