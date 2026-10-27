.PHONY: help setup test lint run-backend run-frontend health-check

help:
	@echo "SkyOps Intelligence Workspace Commands:"
	@echo "  make setup        - Install backend and frontend dependencies"
	@echo "  make test         - Run backend unit tests"
	@echo "  make lint         - Run linters for backend and frontend"
	@echo "  make run-backend  - Start FastAPI backend server on :8000"
	@echo "  make run-frontend - Start Next.js frontend on :3000"
	@echo "  make health-check - Probe backend health endpoints"

setup:
	pip install -r backend/requirements-dev.txt
	cd frontend && npm install

test:
	python -m pytest backend/tests

lint:
	ruff check backend
	cd frontend && npm run lint

run-backend:
	uvicorn app.main:app --app-dir backend --host 0.0.0.0 --port 8000 --reload

run-frontend:
	cd frontend && npm run dev

health-check:
	curl -f http://localhost:8000/health || echo "Backend not running on :8000"

