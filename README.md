# Airline Procedure Intelligence (SkyOps Intelligence)

[![Status: Baseline Approved](https://img.shields.io/badge/Status-Baseline%20Approved-success.svg)](#)
[![Milestones: 3.1, 3.8, 3.9, 3.10, 3.11, 3.37](https://img.shields.io/badge/Milestones-3.1%20%7C%203.8%20%7C%203.9%20%7C%203.10%20%7C%203.11%20%7C%203.37-blue.svg)](#)
[![Domain: Aviation Safety](https://img.shields.io/badge/Domain-Commercial%20Aviation%20Safety-red.svg)](#)
[![CI Quality Gates](https://github.com/kalviumcommunity/S63_airline-procedure-intelligence/actions/workflows/ci.yml/badge.svg)](https://github.com/kalviumcommunity/S63_airline-procedure-intelligence/actions/workflows/ci.yml)

AI-powered operational procedure assistant designed for airline ground staff, ramp agents, gate personnel, station dispatchers, and safety compliance auditors.

---

## 1. Overview & Operational Problem

Commercial airline ground turnaround operations are conducted under extreme time constraints (25–45 minute turns) in hazardous tarmac environments. Operational rules are distributed across thousands of pages of:
- **Ground Operations Manuals (GOM)**
- **IATA Airport Handling Manuals (AHM)**
- **Operations Safety Bulletins (OSBs)**
- **Local Station Operating Procedures (LOPs)**
- **Regulatory Directives (FAA, EASA, DGCA, ICAO)**

When an emergency safety bulletin or temporary revision modifies a standard procedure (e.g., lithium battery fire response, pushback towbar shear pin inspection, fueling with passengers on board), frontline ramp staff frequently access outdated binders or unindexed PDFs. **Following a superseded procedure can cause ground collisions, ramp fires, worker injuries, turn delays, and catastrophic civil regulatory penalties.**

**SkyOps Intelligence** solves this with a high-integrity Retrieval-Augmented Generation (RAG) platform delivering:
1. **Sub-3-second responses** optimized for rugged tablets and handheld devices on the ramp.
2. **Deterministic Supersession Resolution:** Guarantees that superseded, revoked, or unverified procedures are **never** presented as active guidance.
3. **100% Grounded Citations:** Exact document ID, version number, section code, and page number for every step and safety alert.
4. **Fail-Closed Safety Guardrails:** Clear, unambiguous fallback protocols when procedures are missing or ambiguous.

---

## 2. Workspace Structure & Technology Stack

```
S63_airline-procedure-intelligence/
├── .github/                           # GitHub Team Workflow & CI (Milestone 3.11)
│   ├── workflows/ci.yml               # Automated CI quality gates (lint, test, typecheck, secrets)
│   ├── ISSUE_TEMPLATE/                # Bug reports, feature requests & safety discrepancy reports
│   └── PULL_REQUEST_TEMPLATE.md       # PR checklist & mandatory human review gate
├── backend/                           # FastAPI Python Service (Milestone 3.10)
│   ├── app/
│   │   ├── main.py                    # App entrypoint, CORS & route mounting
│   │   ├── core/config.py             # Pydantic Settings & safe env loading
│   │   └── api/routes/health.py       # /health & /status diagnostic endpoints
│   ├── tests/                         # Pytest unit tests (health, config)
│   ├── pyproject.toml                 # Ruff, Pytest, packaging configuration
│   ├── requirements.txt               # Locked runtime dependencies
│   ├── requirements-dev.txt           # Development and testing dependencies
│   └── .env.example                   # Backend environment template
├── frontend/                          # Next.js 14 Progressive Web App (Milestone 3.10)
│   ├── src/app/                       # App router (layout, landing page, health API)
│   ├── package.json                   # Dependencies, linting, build scripts
│   ├── tsconfig.json                  # TypeScript compiler options
│   ├── next.config.mjs                # Next.js runtime configuration
│   ├── .eslintrc.json                 # ESLint rules
│   └── .env.example                   # Frontend environment template
├── prototype/                         # Interactive Clickable Prototype (Milestone 3.9)
│   ├── index.html                     # Self-contained responsive HTML5/CSS3/JS prototype
│   └── README.md                      # Prototype user guide & scenario walkthrough
├── docs/                              # Comprehensive Architectural Documentation
│   ├── UX_DESIGN.md                   # UX Architecture & Wireframes (Milestone 3.9)
│   ├── PRD.md                         # Product Requirements Document (Milestone 3.8)
│   ├── ARCHITECTURE.md                # Initial RAG Architecture & Ingestion Design (Milestone 3.37)
│   ├── SUPERSEDENCE_MODEL.md          # Versioning & Supersession Graph Engine (Milestone 3.37)
│   ├── RISKS_AND_SAFETY.md            # Safety Constraints & HIRA Risk Matrix (Milestones 3.8, 3.37)
│   └── ROADMAP.md                     # 30-Day Implementation Roadmap & Milestones (Milestone 3.1)
├── CONTRIBUTING.md                    # Branch naming, conventional commits & review policy (Milestone 3.11)
├── .editorconfig                      # Universal code formatting rules
├── .env.example                       # Unified root environment configuration
├── .gitignore                         # Strict credential and artifact exclusions
└── Makefile                           # Common local development commands
```

---

## 3. Team Workflow & Contribution Standards (Milestone 3.11)

- **Branch Naming:** `feat/day-<NN>-<short-description>`, `fix/...`, `docs/...`, `chore/...`, `safety/...`.
- **Commit Style:** [Conventional Commits](https://www.conventionalcommits.org/) (`feat:`, `fix:`, `docs:`, `test:`, `chore:`, `safety:`).
- **Automated CI Quality Gates:** Every PR is verified by GitHub Actions:
  - Backend Ruff linting & formatting (`ruff check . && ruff format --check .`)
  - Backend unit test validation (`pytest -v`)
  - Frontend TypeScript validation (`npx tsc --noEmit`)
  - Credential leak & secret hygiene scanning
- **Manual PR Approval Requirement:** Merging is strictly a human-controlled action. Auto-merges are disabled to guarantee safety review.
- Detailed guidelines are in [CONTRIBUTING.md](CONTRIBUTING.md).

---

## 4. Local Setup & Quick Start (Milestone 3.10)

### Backend (FastAPI) Setup
```bash
# 1. Navigate to backend directory
cd backend

# 2. Configure local environment (all variables have safe defaults)
cp .env.example .env

# 3. Install dependencies
pip install -r requirements-dev.txt

# 4. Run tests & linters
pytest
ruff check .

# 5. Start the backend service
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Frontend (Next.js) Setup
```bash
# 1. Navigate to frontend directory
cd frontend

# 2. Configure local environment
cp .env.example .env.local

# 3. Install dependencies
npm install

# 4. Start the frontend application
npm run dev
```

---

## 5. Health Check & Diagnostics

| Endpoint | Method | Expected Output | Purpose |
| :--- | :--- | :--- | :--- |
| `http://localhost:8000/health` | `GET` | `{"status": "healthy", "service": "SkyOps Intelligence Backend", ...}` | Backend liveness probe |
| `http://localhost:8000/status` | `GET` | `{"status": "operational", "subsystems": {...}}` | Subsystem diagnostic readiness |
| `http://localhost:8000/api/v1/health` | `GET` | `{"status": "healthy", ...}` | Versioned API gateway health |
| `http://localhost:8000/docs` | `GET` | Interactive Swagger OpenAPI UI | API documentation & testing |
| `http://localhost:3000/api/health` | `GET` | `{"status": "healthy", "service": "skyops-frontend", ...}` | Frontend Next.js health route |

---

## 6. Milestones Alignment

- **Milestone 3.1 (Project Kickoff & Setup):** Baseline repository established, clean branching workflow, project overview, and implementation plan.
- **Milestone 3.8 (Product Requirements Document):** Full PRD covering personas, operational pain points, functional requirements, NFRs, safety constraints, and acceptance criteria.
- **Milestone 3.9 (Mock UX & Clickable Prototype):** Wireframe specifications, primary user journey documentation, and interactive prototype covering active procedures, superseded warnings, no-evidence refusals, and conflicting sources.
- **Milestone 3.10 (Development Environment & Workspace):** Modular Next.js and FastAPI workspace, dependency manifests, safe environment loading, `.env.example`, formatting/linting configs, and health-check instructions.
- **Milestone 3.11 (GitHub Repository & Team Workflow):** CI quality gates, PR template with human review gate, aviation procedure discrepancy issue template, contribution guidelines, branch naming conventions, and secret hygiene check.
- **Milestone 3.37 (Initial RAG Architecture):** Detailed architecture specifications covering ingestion, parsing, vector index, supersession model, hybrid retrieval, fail-closed generation, and risk mitigation.
