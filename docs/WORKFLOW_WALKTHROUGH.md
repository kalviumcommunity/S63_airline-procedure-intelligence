# Git Workflow, Team Operations & Review Walkthrough
## SkyOps Intelligence: Engineering Standards & Verification Evidence

**Document Status:** Approved Baseline  
**Target Milestone:** 3.11 (GitHub Repository & Team Workflow)  
**Effective Date:** 2026-10-27  
**Author:** Airline AI Engineering Leadership & Ground Operations Taskforce  

---

## Executive Summary: The 5 Core Workflow Pillars

This document serves as the authoritative operational walkthrough for all five GitHub workflow topics evaluated in Milestone 3.11:
1. **Branching Strategy & Source Branch Identification**
2. **Issue Creation, Assignment & Labeling**
3. **Pull Request Review Protocol & Mandatory Human Gate**
4. **Commit Message Standards & Commit History Evidence**
5. **Deterministic Merge-Conflict Resolution Protocol**

---

## Topic 1: Branching Strategy & Source Branch Identification

SkyOps Intelligence uses a structured, trunk-based feature-branching workflow designed for safety-critical aviation development:

```
[ main (Production Trunk) ]
      |
      +---> [ docs/day-01-prd-architecture ]       (Day 1: PRD & RAG Architecture)
      |
      +---> [ feat/day-02-ux-wireframes ]          (Day 2: Mock UX & Prototype)
      |
      +---> [ feat/day-03-workspace-setup ]        (Day 3: FastAPI & Next.js Setup)
      |
      +---> [ feat/day-04-github-workflow ]        (Day 4: GitHub Actions & CI)
      |
      +---> [ feat/day-05-llm-client ]             (Day 5: LLM Client Adapter)
```

### Source Branch Naming Rules
1. **Feature / Milestone Branches:** `feat/day-<NN>-<short-description>`
2. **Documentation Branches:** `docs/day-<NN>-<short-description>`
3. **Bugfix Branches:** `fix/<short-description>`
4. **Urgent Safety Overrides:** `safety/<bulletin-id>-<override>`

### Active Branch Evidence Table
| Milestone | Source Branch Name | Base Branch | Target Capability | Active PR Link |
| :--- | :--- | :--- | :--- | :--- |
| **3.1 / 3.8 / 3.37** | `docs/day-01-prd-architecture` | `main` | PRD, Architecture, Supersession DAG | [PR #1](https://github.com/kalviumcommunity/S63_airline-procedure-intelligence/pull/1) |
| **3.9** | `feat/day-02-ux-wireframes` | `main` | Clickable Prototype & Wireframes | [PR #2](https://github.com/kalviumcommunity/S63_airline-procedure-intelligence/pull/2) |
| **3.10** | `feat/day-03-workspace-setup` | `main` | FastAPI, Next.js, Health Checks | [PR #3](https://github.com/kalviumcommunity/S63_airline-procedure-intelligence/pull/3) |
| **3.11** | `feat/day-04-github-workflow` | `main` | CI Gates, PR & Issue Templates | [PR #4](https://github.com/kalviumcommunity/S63_airline-procedure-intelligence/pull/4) |
| **3.12** | `feat/day-05-llm-client` | `main` | LLM Adapter, Error Mapping, Mocks | [PR #5](https://github.com/kalviumcommunity/S63_airline-procedure-intelligence/pull/5) |

---

## Topic 2: Issue Creation, Assignment & Labeling

To track operational safety hazards, feature requests, and system defects, three concrete issues have been created directly in the GitHub repository:

### 1. Safety Discrepancy Issue (Aviation Safety Critical)
- **Issue Reference:** [Issue #6: [PROCEDURE DISCREPANCY]: Ingestion of Safety Bulletin OSB-2026-03 superseding GOM Section 8.4 Lithium Fire Protocols](https://github.com/kalviumcommunity/S63_airline-procedure-intelligence/issues/6)
- **Assignee:** `@sakxhamm`
- **Labels:** `safety`, `discrepancy`, `high-priority`
- **Operational Hazard:** Legacy GOM 8.4 instructed putting smoking electronics in polyethylene bags. FAA SAFO 25002 mandates Fire Containment Bags (FCB) with cold-water immersion.
- **Workflow Action:** Ingest OSB-2026-03 and mark target GOM chunk `status: superseded`.

### 2. Team Workflow & CI Feature Issue
- **Issue Reference:** [Issue #7: [FEAT]: GitHub Repository CI Quality Gates & Team Workflow (Milestone 3.11)](https://github.com/kalviumcommunity/S63_airline-procedure-intelligence/issues/7)
- **Assignee:** `@sakxhamm`
- **Labels:** `workflow`, `enhancement`
- **Deliverables:** Automated GitHub Actions (`ci.yml`), PR template, issue templates, branch naming conventions, and secret quarantine check.

### 3. Backend Defect / Capability Issue
- **Issue Reference:** [Issue #8: [BUG]: Error Mapping & Timeout Handling in LLM Client Adapter (Milestone 3.12)](https://github.com/kalviumcommunity/S63_airline-procedure-intelligence/issues/8)
- **Assignee:** `@sakxhamm`
- **Labels:** `backend`, `bug`
- **Deliverables:** Handling missing credentials (`LLMConfigurationError`), timeouts (`LLMTimeoutError`), HTTP 429 (`LLMRateLimitError`), and provider 5xx outages (`LLMProviderError`).

---

## Topic 3: Pull Request Review Protocol & Mandatory Human Gate

Pull Requests act as the primary safety gate in SkyOps Intelligence. Every PR is governed by strict review standards:

### 1. Pull Request Description Standard
Every PR must explicitly link to its corresponding issue using GitHub keywords (`Closes #7`, `Fixes #8`, `Resolves #6`), state its source branch, and detail test evidence.

### 2. Automated CI Quality Gates (`.github/workflows/ci.yml`)
Every PR automatically triggers three parallel quality jobs:
- **`backend-checks`:** Ruff linter (`ruff check .`), Ruff formatting check (`ruff format --check .`), and Pytest test suite (`pytest -v`).
- **`frontend-checks`:** Node.js 20 environment, dependency installation, and TypeScript type validation (`npx tsc --noEmit`).
- **`security-audit`:** Scans tracked Git files to guarantee live `.env` files are never committed.

### 3. Mandatory Human-in-the-Loop Review Gate (NO AUTO-MERGES)
> [!IMPORTANT]
> **Merging is strictly a human-controlled action.**
> Automated merges (e.g. Dependabot auto-merge or GitHub auto-merge bots) are **strictly disabled**.
> In commercial aviation, an automated merge could inadvertently overwrite an active safety bulletin override with obsolete standard operating procedures.
> Every merge requires:
> 1. Manual code review by an authorized reviewer.
> 2. Verification of the supersession status.
> 3. Confirmation of green CI quality checks.

---

## Topic 4: Commit Messages & Conventional Commits

We enforce the **Conventional Commits** specification to guarantee semantic versioning and auditable release trails.

### Format Structure
```
<type>(<optional scope>): <imperative description>
```

### Recognized Types
- `feat`: New operational or architectural capability.
- `fix`: Remediation of software defect or parser bug.
- `docs`: Documentation, PRD, or architecture update.
- `test`: Unit, integration, or regression test additions.
- `chore`: Build system, linting, or workspace tooling maintenance.
- `safety`: Aviation safety override or regulatory supersession update.

### Verified Commit History Evidence
```
* bc8bb8d (HEAD -> feat/day-05-llm-client, origin/feat/day-05-llm-client) feat: implement Day 5 LLM client adapter, error handling, mock and smoke test (milestone 3.12)
* be92819 (origin/feat/day-04-github-workflow, feat/day-04-github-workflow) feat: implement Day 4 GitHub team workflow, CI quality gates, and templates (milestone 3.11)
* feae8e3 (origin/feat/day-03-workspace-setup, feat/day-03-workspace-setup) feat: implement Day 3 development environment and modular workspace (milestone 3.10)
* 164fe8c (origin/feat/day-02-ux-wireframes, feat/day-02-ux-wireframes) feat: implement Day 2 ground-staff UX wireframes and interactive prototype (milestone 3.9)
* 88e12c8 (origin/docs/day-01-prd-architecture, docs/day-01-prd-architecture) docs: implement Day 1 PRD, RAG architecture, and supersession model (milestones 3.1, 3.8, 3.37)
* a82b5a1 (origin/main, main) chore: initial project kickoff setup
```

---

## Topic 5: Deterministic Merge-Conflict Resolution Protocol

In parallel airline development, multiple engineers may edit shared manual definitions or API routes simultaneously (e.g., both Developer A and Developer B editing `backend/app/core/config.py` or `docs/SUPERSEDENCE_MODEL.md`).

### Real-World Conflict Scenario
- **Branch A (`feat/deicing-lop`):** Updates de-icing fluid holdover times for KORD Station LOP.
- **Branch B (`safety/faa-ad-override`):** Ingests Emergency Airworthiness Directive mandating tactile inspections.
- **Conflict:** Git flags conflicting changes in the precedence table within `docs/SUPERSEDENCE_MODEL.md`.

### Step-by-Step Resolution Protocol

#### Step 1: Rebase Feature Branch onto Target Base Trunk
```bash
# Fetch latest changes from remote
git fetch origin

# Rebase feature branch onto updated main
git checkout feat/day-04-github-workflow
git rebase origin/main
```

#### Step 2: Inspect Conflict Markers
Git halts rebase and marks conflicting sections:
```
<<<<<<< HEAD (Base Branch - Regulatory Directive)
PREFERENCE_LEVEL_1 = "FAA Emergency Airworthiness Directive (Mandatory Tactile Check)"
=======
PREFERENCE_LEVEL_1 = "Base Ground Operations Manual (Cabin Visual Inspection)"
>>>>>>> feat/branch (Feature Branch - Legacy Procedure)
```

#### Step 3: Apply Aviation Precedence Hierarchy Resolution
Under aviation law, Regulatory Directives (Level 1) strictly supersede Base GOM (Level 4). The engineer resolves the conflict in favor of Level 1:
```python
PREFERENCE_LEVEL_1 = "FAA Emergency Airworthiness Directive (Mandatory Tactile Check)"
# Base GOM Cabin Visual Inspection marked as SUPERSEDED
```

#### Step 4: Validate and Continue Rebase
```bash
# 1. Run local tests to ensure no regressions
pytest backend/tests
ruff check backend

# 2. Stage resolved file
git add docs/SUPERSEDENCE_MODEL.md

# 3. Complete rebase
git rebase --continue

# 4. Force push with lease (protecting concurrent team commits)
git push --force-with-lease origin feat/day-04-github-workflow
```
*(Using `--force-with-lease` guarantees that if another team member has pushed commits in the interim, the push fails safely instead of overwriting work).*

