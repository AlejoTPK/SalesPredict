# SalesPredict AI CRM

SalesPredict is a modern AI-powered Customer Relationship Management (CRM) platform designed for advanced sales forecasting and real-time dashboard analytics. It leverages a clean architecture with a high-performance FastAPI backend, a sleek Next.js 15 frontend, and specialized ML pipelines for predictive modeling.

## 🚀 Key Features

- **AI Sales Forecasting**: Predictive modeling using XGBoost to anticipate market trends and sales performance.
- **Real-Time Analytics**: Live dashboards for sales tracking and performance metrics.
- **Clean Architecture**: Decoupled backend layers (API, Services, Repositories, Domain) for maximum maintainability.
- **Modern Tech Stack**: Next.js 15, FastAPI, SQLAlchemy 2.0, PostgreSQL, and Tailwind CSS.
- **Dockerized Environment**: Seamless deployment using Docker Compose.

---

## 🏗️ Architecture

### Backend (FastAPI)
- **Framework**: FastAPI with Pydantic V2.
- **Database**: PostgreSQL (via SQLAlchemy 2.0 + `asyncpg`).
- **Persistence**: Async repository pattern.
- **Background Tasks**: Celery for ETL and model retraining.
- **Authentication**: JWT-based secure auth flow.

### Frontend (Next.js 15)
- **Framework**: React 19 + Next.js 15 (App Router).
- **Styling**: Tailwind CSS + shadcn/ui + Tremor.
- **State Management**: Native React hooks (Zero TanStack).
- **Real-Time**: WebSockets for live data updates.

### ML Pipelines
- **Models**: XGBoost for time-series forecasting.
- **Experiment Tracking**: MLflow for metrics and artifact registry.
- **Processing**: Pandas and NumPy for feature engineering.

---

## 🛠️ Getting Started

### Prerequisites
- Python 3.12+ (managed via Poetry)
- Node.js 20+ (managed via pnpm)
- Docker & Docker Compose

### Development Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/AlejoTPK/SalesPredict.git
   cd SalesPredict
   ```

2. **Backend Setup**:
   ```bash
   cd backend
   poetry install
   cp .env.example .env
   poetry run alembic upgrade head
   poetry run uvicorn app.main:app --reload
   ```

3. **Frontend Setup**:
   ```bash
   cd frontend
   pnpm install
   pnpm dev
   ```

4. **ML Pipeline (Optional)**:
   ```bash
   cd ml-pipelines
   poetry install
   poetry run python training/train_xgboost.py
   ```

---

## 🐳 Docker Deployment

The entire stack can be launched using Docker Compose:

```bash
docker-compose -f docker/docker-compose.yml up --build
```

---

## 📜 Commands

See [AGENTS.md](./AGENTS.md) for a full list of available commands for testing, linting, and database migrations.

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
