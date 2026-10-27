# Airline Procedure Intelligence (SkyOps Intelligence)

[![Status: Baseline Approved](https://img.shields.io/badge/Status-Baseline%20Approved-success.svg)](#)
[![Milestones: 3.1, 3.8, 3.9, 3.37](https://img.shields.io/badge/Milestones-3.1%20%7C%203.8%20%7C%203.9%20%7C%203.37-blue.svg)](#)
[![Domain: Aviation Safety](https://img.shields.io/badge/Domain-Commercial%20Aviation%20Safety-red.svg)](#)

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

## 2. Documentation & Prototype Suite

| Document / Artifact | Purpose & Scope | Target Milestone |
| :--- | :--- | :--- |
| **[Clickable Prototype](prototype/index.html)** | Interactive, zero-dependency clickable prototype demonstrating active procedures, superseded warnings, no-evidence refusals, conflict resolution, and document ingestion. | **Milestone 3.9** |
| **[UX Architecture & Wireframes](docs/UX_DESIGN.md)** | Human factors analysis for tarmac environments, ASCII wireframes for 6 core screens, primary user journey, and WCAG accessibility standards. | **Milestone 3.9** |
| **[Product Requirements Document (PRD)](docs/PRD.md)** | Target personas, operational pain points, functional & non-functional requirements, safety constraints, acceptance criteria, and out-of-scope boundaries. | **Milestone 3.8** |
| **[System Architecture & Initial RAG Design](docs/ARCHITECTURE.md)** | Subsystems, ingestion pipeline, hierarchical chunking, hybrid BM25 + dense search, re-ranking, generation guardrails, and data flow diagrams. | **Milestone 3.37** |
| **[Version & Supersession Resolution Model](docs/SUPERSEDENCE_MODEL.md)** | Regulatory precedence hierarchy, Directed Acyclic Graph (DAG) specification, metadata schemas, query-time resolution algorithm, and zero-stale guarantee. | **Milestone 3.37** |
| **[Safety Constraints & Operational Risk Analysis](docs/RISKS_AND_SAFETY.md)** | Hazard Identification & Risk Assessment (HIRA), Swiss Cheese Model, fail-closed protocols, human-in-the-loop (HITL) checkpoints, and SMS compliance. | **Milestone 3.8 / 3.37** |
| **[30-Day Implementation Roadmap](docs/ROADMAP.md)** | 5-phase execution plan spanning Days 1–30, milestone mapping (3.1 to 3.99), evaluation benchmarks, and pilot readiness criteria. | **Milestone 3.1** |

---

## 3. Primary User Journey (Ground Staff Experience)

```
[ Step 1: ASK ] ------------> [ Step 2: RETRIEVE ] --------> [ Step 3: VERIFY ] --------> [ Step 4: REVIEW ]
Natural language query       Hybrid dense vector &           Supersession DAG &             Structured checklist,
scoped by Station & Fleet    sparse BM25 passage search      precedence validation          mandatory verbs & citations
```

---

## 4. How to Launch the Prototype

The interactive prototype requires no dependencies or build steps. Open directly in a browser:
```powershell
Start-Process "prototype\index.html"
```
Or view [prototype instructions](prototype/README.md).

---

## 5. Repository Structure

```
S63_airline-procedure-intelligence/
├── README.md                          # Master overview, architecture summary & navigation
├── .gitignore                         # Comprehensive Git ignore rules
├── prototype/                         # Interactive Clickable Prototype (Milestone 3.9)
│   ├── index.html                     # Self-contained responsive HTML5/CSS3/JS prototype
│   └── README.md                      # Prototype user guide & scenario walkthrough
└── docs/
    ├── UX_DESIGN.md                   # UX Architecture & Wireframe Specifications (Milestone 3.9)
    ├── PRD.md                         # Product Requirements Document (Milestone 3.8)
    ├── ARCHITECTURE.md                # Initial RAG Architecture & Ingestion Design (Milestone 3.37)
    ├── SUPERSEDENCE_MODEL.md          # Versioning & Supersession Graph Engine (Milestone 3.37)
    ├── RISKS_AND_SAFETY.md            # Safety Constraints & HIRA Risk Matrix (Milestones 3.8, 3.37)
    └── ROADMAP.md                     # 30-Day Implementation Roadmap & Milestones (Milestone 3.1)
```

---

## 6. Milestones Alignment

- **Milestone 3.1 (Project Kickoff & Setup):** Baseline repository established, clean branching workflow, project overview, and implementation plan.
- **Milestone 3.8 (Product Requirements Document):** Full PRD covering personas, operational pain points, functional requirements, NFRs, safety constraints, and acceptance criteria.
- **Milestone 3.9 (Mock UX & Clickable Prototype):** Wireframe specifications, primary user journey documentation, and interactive prototype covering active procedures, superseded warnings, no-evidence refusals, and conflicting sources.
- **Milestone 3.37 (Initial RAG Architecture):** Detailed architecture specifications covering ingestion, parsing, vector index, supersession model, hybrid retrieval, fail-closed generation, and risk mitigation.
