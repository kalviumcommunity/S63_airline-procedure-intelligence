## Pull Request Description

### 1. Milestone & Scope Alignment
- **Milestone Reference:** <!-- e.g., Milestone 3.11 - GitHub repository and team workflow -->
- **Branch Name:** <!-- e.g., feat/day-04-github-workflow -->
- **Summary of Changes:**
  <!-- High-level description of what this PR introduces or fixes -->

---

### 2. Type of Change
- [ ] `feat`: New feature or capability
- [ ] `fix`: Bug fix
- [ ] `docs`: Documentation update or addition
- [ ] `test`: Unit, integration, or regression test additions
- [ ] `chore`: Build, workflow, or dependency maintenance
- [ ] `safety`: Aviation procedure or safety guardrail modification

---

### 3. Aviation Safety & Compliance Verification
- [ ] **No Superseded Procedures Exposed:** This change does not introduce or expose stale, unverified, or superseded procedures as active guidance.
- [ ] **Zero Hardcoded Credentials:** Verified that no production API keys, passwords, private keys, or `.env` files are tracked or exposed.
- [ ] **Deterministic Behavior:** Logic maintains deterministic outputs ($T=0$ constraints or fail-closed fallbacks where applicable).

---

### 4. Quality & Testing Checklist
- [ ] Local tests pass cleanly (`pytest backend/tests`).
- [ ] Python linter and formatter check passed (`ruff check . && ruff format --check .`).
- [ ] Frontend type check passed (`npm run build` or `npx tsc --noEmit`).
- [ ] Documentation and comments updated to reflect changes.

---

### 5. Human-in-the-Loop Review Gate (MANDATORY)
> [!IMPORTANT]
> **Merging is strictly a human-controlled action.** Automated merges (e.g., auto-merge bots) are strictly prohibited for this repository to protect aviation compliance integrity.
- [ ] Code reviewed and approved by an authorized peer/lead.
- [ ] Manual approval confirmed before merge.
- [ ] **Do NOT merge until human safety sign-off is completed.**
