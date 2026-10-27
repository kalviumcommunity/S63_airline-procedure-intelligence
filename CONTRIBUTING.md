# Contributing to SkyOps Intelligence

Thank you for contributing to **SkyOps Intelligence**. Because this system provides safety-critical procedural guidance to airline ground handling personnel, all code and documentation must adhere to high standards of rigor, traceability, and determinism.

---

## 1. Branch Naming Conventions

All team members and contributors must follow structured branch naming conventions:

| Branch Type | Format | Example | Description |
| :--- | :--- | :--- | :--- |
| **Milestone / Feature** | `feat/day-<NN>-<short-description>` | `feat/day-04-github-workflow` | Daily milestone deliveries or new product features. |
| **Bug Fix** | `fix/<short-description>` | `fix/citation-page-parser` | Remediation of software defects or parsing errors. |
| **Documentation** | `docs/<short-description>` | `docs/day-01-prd-architecture` | Architecture blueprints, PRDs, or guides. |
| **Maintenance / Tooling** | `chore/<short-description>` | `chore/ci-runner-upgrade` | Build system, dependency, or linting updates. |
| **Aviation Safety Hotfix** | `safety/<bulletin-id>` | `safety/osb-2026-04-override` | Urgent safety override or supersession correction. |

---

## 2. Commit Message Standards (Conventional Commits)

We enforce the [Conventional Commits](https://www.conventionalcommits.org/) specification. Each commit message must start with a recognized type:

- `feat:` Introduces a new capability or user-facing feature.
- `fix:` Fixes a bug or algorithmic defect.
- `docs:` Documentation only changes.
- `test:` Adds or fixes unit, integration, or regression tests.
- `chore:` Maintenance, dependency, or workspace configuration updates.
- `safety:` Updates to supersession logic, hazard guardrails, or regulatory rules.

*Example:*
```bash
git commit -m "feat: add hybrid reciprocal rank fusion for ATA section codes"
```

---

## 3. Local Development & Pre-Push Checklist

Before opening or updating a Pull Request, ensure all local quality gates pass cleanly:

### 3.1 Backend Quality Gates
```bash
# 1. Run Ruff linter
ruff check backend

# 2. Check code formatting
ruff format --check backend

# 3. Run full Pytest suite
pytest backend/tests
```

### 3.2 Frontend Quality Gates
```bash
cd frontend

# 1. Run type check
npx tsc --noEmit

# 2. Run Next.js linter
npm run lint
```

### 3.3 Credential Hygiene
- **Never commit `.env` or credential files.**
- Always verify that new parameters are added to `.env.example` with safe, placeholder values.

---

## 4. Pull Request & Review Workflow

```
[ Local Branch ] ──> [ Push to Origin ] ──> [ Open PR to main ] ──> [ CI Quality Gates ] ──> [ Human Peer Review ] ──> [ Manual Merge ]
```

1. **Open Pull Request:**
   - Base branch: `main`
   - Complete all sections of the [PULL_REQUEST_TEMPLATE.md](.github/PULL_REQUEST_TEMPLATE.md).
2. **Automated CI Validation:**
   - Every PR triggers `.github/workflows/ci.yml`.
   - All three quality jobs (`backend-checks`, `frontend-checks`, `security-audit`) must pass with green status.
3. **Manual Human Approval Gate (MANDATORY):**
   > [!IMPORTANT]
   > **Merging is strictly a human-controlled action.**
   > - Automated merging (bots / auto-merge) is strictly forbidden.
   > - Every PR requires manual review and sign-off by a code owner or ground safety reviewer before merging.
   > - Do not merge pull requests designated for day-by-day milestone review until instructed by project leads.

---

## 5. Safety-Critical Code Expectations

When contributing to the RAG, ingestion, or supersession engines:
1. **Zero-Stale Guarantee:** Ensure that no query path can return a chunk with `status != 'active'`.
2. **Entailment Verification:** All generated procedures must be grounded by explicit citations containing Document ID, Version, Section, and Page.
3. **Fail-Closed Design:** If confidence is below threshold ($\tau < 0.82$) or a conflict is detected between directives of equal rank, the system must fail closed and escalate to human dispatchers.

