# SkyOps Intelligence - Backend Service

High-Integrity Airline Procedure Verification API built with FastAPI, Pydantic, and Python 3.10+.

---

## 1. Local Setup Instructions

### Prerequisites
- Python 3.10+ (tested on Python 3.12)
- Virtual environment tool (`venv` or `conda`)

### Step 1: Create and Activate Virtual Environment
```bash
# From repository root or backend/
python -m venv .venv

# On Windows PowerShell:
.venv\Scripts\Activate.ps1

# On Linux / macOS:
source .venv/bin/activate
```

### Step 2: Install Dependencies
```bash
pip install -r requirements-dev.txt
```

### Step 3: Configure Environment
```bash
cp .env.example .env
```
*(All variables have safe default fallbacks; no external credentials are required for local development or health checks).*

---

## 2. Running the Service & Health Checks

### Start Development Server
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Verify Endpoints
- **Liveness Probe:** `curl http://localhost:8000/health`
- **Diagnostic Status:** `curl http://localhost:8000/status`
- **Versioned API Health:** `curl http://localhost:8000/api/v1/health`
- **Interactive Swagger Docs:** Visit `http://localhost:8000/docs`

---

## 3. Running Tests & Linters

```bash
# Run unit tests
pytest

# Run linter and formatter check
ruff check .
ruff format --check .
```

