# 30-Day Implementation Roadmap & Milestones
## SkyOps Intelligence: Engineering Execution Plan

**Document Status:** Approved Baseline  
**Roadmap Identifier:** SKY-ROAD-001  
**Applicable Milestones:** 3.1 (Kickoff), 3.8 (PRD), 3.37 (Initial RAG Architecture)  
**Effective Date:** 2026-10-27  
**Author:** Airline AI Engineering Leadership & Ground Operations Taskforce  

---

## 1. Roadmap Overview & Strategic Objectives

The SkyOps Intelligence platform follows an aggressive, safety-governed 30-day implementation plan designed to transition from architecture baseline to a validated production-ready pilot for ground ramp operations.

```
+---------------------------------------------------------------------------------------------------+
|                                  30-DAY IMPLEMENTATION PHASES                                     |
+-------------------+--------------------+--------------------+--------------------+----------------+
|  DAYS 1 - 7       |  DAYS 8 - 14       |  DAYS 15 - 21      |  DAYS 22 - 28      |  DAYS 29 - 30  |
|  Phase 1:         |  Phase 2:          |  Phase 3:          |  Phase 4:          |  Phase 5:      |
|  Foundation, PRD  |  Ingestion Engine  |  Hybrid Search,    |  Ground UI, Mobile |  Field Pilot,  |
|  & Architecture   |  & Supersession    |  Re-ranking & LLM  |  PWA, Audit Logs   |  Evaluation    |
|  (Milestones      |  Graph Pipeline    |  Safety Guardrails |  & Integration     |  & Sign-off    |
|  3.1, 3.8, 3.37)  |                    |                    |                    |                |
+-------------------+--------------------+--------------------+--------------------+----------------+
```

---

## 2. Detailed Phase Breakdown

### Phase 1: Foundation, PRD & Architecture (Days 1 – 7)
*Focus: Alignment, formal specifications, architecture blueprints, data schema, repository setup.*

- **Day 1 (Milestones 3.1, 3.8, 3.37) — COMPLETED:**
  - Establish project structure, version control branching model, and clean Git repository.
  - Deliver comprehensive Product Requirements Document (PRD) covering ground personas, operational pain points, and safety constraints.
  - Architect the end-to-end RAG pipeline, document lifecycle state machine, and data flow specifications.
  - Define the Version & Supersession Resolution Model to eliminate stale/superseded procedures.
  - Perform Hazard Identification & Risk Assessment (HIRA) for aviation safety compliance.
- **Day 2 – 3:**
  - Build synthetic sample dataset of airline operational manuals:
    - Base GOM chapters (Aircraft Marshalling, Towing, Pushback, Baggage Handling, De-icing, Fueling).
    - Safety Bulletins (OSBs) with explicit supersession overrides (e.g., lithium battery fire safety, cold-weather shear pin checks).
    - Regulatory Emergency Directives (FAA EADs).
- **Day 4 – 5:**
  - Finalize Pydantic data schemas for document metadata, procedural chunks, and supersession links.
  - Configure PostgreSQL with `pgvector` and Docker compose environment for reproducible local development.
- **Day 6 – 7:**
  - Implement baseline unit test suite for supersession resolution algorithms and graph edge validation.
  - Complete Phase 1 Architecture Review with Airline Safety Council.

---

### Phase 2: Ingestion & Supersession Graph Engine (Days 8 – 14)
*Focus: Document parsing, structure preservation, table extraction, and graph linking.*

- **Day 8 – 9:**
  - Implement `AeroDoc` structural parser using `PyMuPDF` / `Docling` to extract headers, warnings, cautions, notes, and tables.
  - Implement procedural chunker that preserves sequential step numbers and safety pre-requisites.
- **Day 10 – 11:**
  - Integrate metadata extraction pipeline (identifying Doc ID, Chapter, Section, Version, Effective Date).
  - Build the Supersession Registry & DAG builder to establish `REPLACES`, `AMENDS`, and `SUSPENDS` relationships.
- **Day 12 – 13:**
  - Implement dense vector generation (`text-embedding-3-large`) and sparse BM25 tokenization for aviation codes.
  - Populate the vector and relational database with the 500-page benchmark procedure corpus.
- **Day 14:**
  - Ingestion benchmark testing: verify that updating a manual automatically marks previous chunk versions as `superseded` within $< 30\text{ seconds}$.

---

### Phase 3: Hybrid Retrieval & Safety Generation Engine (Days 15 – 21)
*Focus: RRF hybrid retrieval, cross-encoder re-ranking, zero-temperature generation, and citation grounding.*

- **Day 15 – 16:**
  - Implement Reciprocal Rank Fusion (RRF) combining dense semantic search and BM25 lexical search.
  - Integrate Cross-Encoder Re-ranking (`bge-reranker-large`) to prioritize the top 5 authoritative chunks.
- **Day 17 – 18:**
  - Integrate Query-Time Supersession Resolution Engine:
    - Hard filtering of `status = 'active'`.
    - Temporal validity window checking.
    - Automatic injection of overriding bulletin chunks.
- **Day 19 – 20:**
  - Implement Generation Pipeline with strict zero-temperature ($T = 0.0$) and constrained JSON schema:
    - Safety Header, Verification Badge, Step-by-Step Checklist, Mandatory PPE, Source Citations.
  - Implement Fail-Closed anti-hallucination logic (threshold $\tau < 0.82 \implies$ explicit refusal).
- **Day 21:**
  - Automated evaluation harness using RAGAS / TruLens measuring:
    - Faithfulness (target $> 0.98$)
    - Answer Relevance (target $> 0.95$)
    - Context Precision (target $> 0.92$)
    - Superseded Procedure Rejection Rate (target: $100.0\%$).

---

### Phase 4: Ground Staff UI & Audit Infrastructure (Days 22 – 28)
*Focus: Daylight-optimized PWA, mobile-first interface, offline caching, and WORM audit logging.*

- **Day 22 – 23:**
  - Develop daylight-optimized responsive Progressive Web App (React / Tailwind):
    - Large $48\times 48\text{ dp}$ touch targets for gloved ramp personnel.
    - High-contrast alert boxes for safety cautions.
    - Quick filter selector for Station Code, Aircraft Fleet, and Ground Role.
- **Day 24 – 25:**
  - Build Human-in-the-Loop (HITL) confirmation modal for high-consequence operations.
  - Implement offline local storage cache for Top 100 Emergency Procedures (Service Worker + IndexedDB).
- **Day 26 – 27:**
  - Build WORM (Write-Once-Read-Many) compliant audit logging service capturing query, matched chunks, prompt, response, user badge ID, and station.
  - Implement Compliance Auditor View with historical revision lookup and explicit superseded warning banners.
- **Day 28:**
  - End-to-end integration testing: simulated 25-minute aircraft turn scenarios under high query load.

---

### Phase 5: Field Pilot Readiness & Evaluation (Days 29 – 30)
*Focus: Station pilot validation, user acceptance testing (UAT), safety sign-off.*

- **Day 29:**
  - Conduct pilot simulation with ramp supervisors, gate agents, and safety inspectors at test station (e.g., Station ORD).
  - Collect user feedback on response clarity, touch target ergonomics, and latency under ramp Wi-Fi/LTE.
- **Day 30:**
  - Final Safety Audit & Verification Review with Chief Safety Officer.
  - Deliver Pilot Readiness Report, API documentation, and handover to Station Operations.

---

## 3. Milestones Mapping

| Milestone | Title | Target Day | Deliverables & Verification Method | Status |
| :--- | :--- | :--- | :--- | :--- |
| **3.1** | **Project Kickoff & Baseline Architecture** | Day 1 | Git repo initialized, branching policy, README, project structure. | **COMPLETED** |
| **3.8** | **Product Requirements Document (PRD)** | Day 1 | Approved PRD (`docs/PRD.md`) with user personas, NFRs, and safety constraints. | **COMPLETED** |
| **3.37** | **Initial RAG Architecture & Supersession Model** | Day 1 | System architecture (`docs/ARCHITECTURE.md`), Supersession Model (`docs/SUPERSEDENCE_MODEL.md`), and Safety Analysis (`docs/RISKS_AND_SAFETY.md`). | **COMPLETED** |
| **3.45** | **Ingestion & Parser Subsystem** | Day 10 | Functional PDF/table parser with section and warning preservation. | Planned |
| **3.52** | **Supersession Graph & Vector Index** | Day 14 | Populated vector database with linked revision DAG. | Planned |
| **3.60** | **Hybrid Retrieval & Reranker Engine** | Day 18 | Combined BM25 + dense search with cross-encoder re-ranking. | Planned |
| **3.75** | **Generation Guardrails & Citation Verifier** | Day 21 | Zero-temperature generator with citation validation and refusal fallback. | Planned |
| **3.88** | **Ramp Mobile Interface & Offline Cache** | Day 25 | Glove-friendly PWA with cached emergency procedures. | Planned |
| **3.99** | **Pilot Deployment & Field Evaluation** | Day 30 | Field validation at test hub station and safety sign-off. | Planned |
