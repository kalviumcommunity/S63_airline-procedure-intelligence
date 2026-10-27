# Product Requirements Document (PRD)
## SkyOps Intelligence: Airline Procedure Intelligence Assistant

**Document Status:** Approved Baseline  
**Project Identifier:** SKY-PRD-001  
**Target Milestone:** 3.8 (PRD & Requirements Specification)  
**Applicable Milestones:** 3.1, 3.8, 3.37  
**Effective Date:** 2026-10-27  
**Author:** Airline Ground Operations Intelligence Working Group  

---

## 1. Executive Summary & Vision

Ground handling operations are among the most safety-critical, time-compressed, and regulation-intensive domains in commercial aviation. Turnaround windows range between 25 and 45 minutes, during which ramp agents, gate agents, baggage handlers, fueling crews, and mechanics must coordinate flawlessly around wide-body and narrow-body aircraft. 

Operating procedures are governed by thousands of pages spanning Ground Operations Manuals (GOM), IATA Airport Handling Manuals (AHM), Airline Safety Action Bulletins, Dangerous Goods Regulations (DGR), and Regulatory Directives (FAA, EASA, DGCA, ICAO). A persistent, severe operational hazard is **procedural ambiguity and latency**: frontline staff often struggle to identify whether a procedure in an operational manual has been temporarily or permanently superseded by a recent safety bulletin or regulatory directive. Following a superseded procedure can cause ground collisions, lithium battery cargo fires, ramp worker injuries, flight delays, and severe civil regulatory penalties.

**SkyOps Intelligence** is a specialized, safety-constrained Retrieval-Augmented Generation (RAG) assistant designed for airline ground personnel. It delivers instant (sub-3-second), verifiable, and station/aircraft-scoped procedure checklists, complete with authoritative source citations, visual hierarchy badges, and a **zero-tolerance supersession guarantee**—ensuring unverified or superseded instructions are never presented as current operational guidance.

---

## 2. Problem Statement & Operational Pain Points

### 2.1 The Operational Reality
1. **Manual Proliferation & Fragmentation:**
   - Standard GOM documents exceed 1,200 pages across 12 distinct chapters.
   - Stations maintain localized Station Operating Procedures (SOPs) for local airport constraints (e.g., gate layout, winter operations, noise abatement).
   - Airlines release 15–30 Operations Safety Bulletins (OSBs) and Flash Alerts per quarter, which temporarily or permanently override base manual sections.
2. **The "Superseded Procedure" Trap:**
   - Ground staff frequently access cached PDFs, printed binders, or unindexed intranet portals. When a safety bulletin updates the cargo fire suppression procedure or lithium-ion device handling protocols, older manual versions remain accessible, leading to non-compliant execution.
3. **Severe Time Pressure during Aircraft Turns:**
   - On a 30-minute turn, a ramp supervisor has less than 60 seconds to resolve an unexpected anomaly (e.g., damaged baggage cargo door seal, fueling with passengers on board, hazmat notification). Waiting for an operational call center or flipping through a PDF binder leads to costly turnaround delays (averaging \$100+ per minute of ground delay) or safety shortcuts.
4. **Harsh Ramp Environmental Constraints:**
   - Ground crew operate in loud (90–115 dB), all-weather environments (glare, rain, snow, sub-zero cold), wearing ramp gloves, using rugged tablets or handheld mobile devices with intermittent Wi-Fi/LTE connectivity.
5. **Regulatory & Audit Exposure:**
   - Civil aviation authorities (FAA, EASA, DGCA) conduct unannounced ramp inspections. Failure to demonstrate that ground staff are executing the *latest active revision* results in immediate audit findings, fines, and potential aircraft grounding.

---

## 3. User Personas & Scenarios

| Persona | Role & Work Environment | Primary Pain Point | Core Need from SkyOps |
| :--- | :--- | :--- | :--- |
| **Ramp Lead / Marshaller** *(Alex M.)* | Tarmac apron, high noise, ramp tablet / phone, rugged gloves. | Quick clarification on pushback clearance protocols under icy apron conditions. | Instant step-by-step checklist with prerequisite safety precautions and mandatory towbar pin checks. |
| **Baggage & Cargo Handler** *(David K.)* | Cargo ramp / baggage sorting room. High physical activity. | Clarifying limits and packing instructions for damaged lithium-ion power banks discovered in gate-checked baggage. | Immediate cross-reference of IATA DGR and airline safety bulletin override on battery disposal packaging. |
| **Gate Agent** *(Sarah T.)* | Gate counter and jet bridge. High passenger volume, rapid boarding clock. | Verifying wheelchair battery disconnection procedures and pet-in-cabin crate compliance. | Clear binary (Permitted / Prohibited) criteria and step-by-step gate-side checklist. |
| **Station Operations Supervisor** *(Elena R.)* | Station Ops Center (SOC) / Ramp tower, multi-screen environment. | Resolving conflicting procedures between airport local authority directives and airline GOM during irregular ops (IROPS). | Authoritative precedence resolution showing regulatory authority vs. airline GOM hierarchy. |
| **Safety & Compliance Auditor** *(Marcus B.)* | Corporate Safety Office / Ramp audit floor. | Verifying compliance history, auditing which procedure versions were accessed during an incident investigation. | Immutable query audit log with exact document IDs, versions, and timestamped retrieval trails. |

---

## 4. Goals & Quantifiable Success Metrics

| Metric Category | Metric | Baseline (Manual) | SkyOps Target (MVP / 30-Day) | Measurement Methodology |
| :--- | :--- | :--- | :--- | :--- |
| **Retrieval Speed** | P95 Response Latency | 4–12 minutes | **< 2.5 seconds** | End-to-end API response tracking under standard load |
| **Safety / Precision** | Superseded Procedure Accuracy | High risk of stale citations | **0.00% superseded guidance presented as active** | Automated regression test suite against superseded procedure database |
| **Citation Fidelity** | Grounded Citation Rate | N/A (Manual lookup) | **100% of responses cite specific Document, Version, Section, Page** | Source-claim alignment verification pipeline |
| **Operational Impact** | Procedural Turn Delay (PTD) | 4.2 delays per 1,000 departures | **< 1.5 delays per 1,000 departures (<60% reduction)** | Airline Station Delay Attribution System |
| **User Confidence** | Frontline CSAT / Trust Score | 42% trust in digital manuals | **> 90% positive rating** | Monthly in-app usability survey & pulse checks |

---

## 5. Functional Requirements (FR)

### FR-1: Natural Language Semantic Procedure Querying
- The system shall accept natural language questions entered by ground personnel (e.g., *"What is the minimum clearance distance for GSE around an A321neo engine cowl?"* or *"Can we fuel while passengers are deplaning?"*).
- The system shall interpret common aviation terminology, acronyms, and shorthand (e.g., GOM, GSE, GPU, ASU, FOD, AHM, DGR, NOTAM, IROPS, APU, LOP).

### FR-2: Contextual Scoping (Station, Aircraft Fleet, Role)
- The system shall provide contextual filtering based on:
  - **Station/Airport Code:** (e.g., `ORD`, `JFK`, `LHR`, `DEL`) to apply Local Operating Procedures (LOP).
  - **Aircraft Type / Fleet:** (e.g., `A320-200`, `A321neo`, `B737-800`, `B787-9`).
  - **User Role:** (e.g., `Ramp`, `Gate`, `Fueling`, `De-icing`, `Baggage`).
- When a query lacks specific fleet or station context, the assistant shall provide the baseline system-wide procedure and explicitly prompt for specific fleet/station modifiers if variations exist.

### FR-3: Automated Version & Supersession Resolution
- Every procedure chunk shall have an immutable version ID, effective date range (`effective_from`, `effective_until`), and status (`active`, `superseded`, `draft`, `revoked`).
- When a Safety Bulletin or Regulatory Directive modifies or replaces a section of the base GOM, the system shall **automatically prioritize the superseding document** and suppress the superseded text from the operational answer.
- The assistant shall display a visual badge: `[ACTIVE PROCEDURE: OSB-2026-08 (Supersedes GOM Sec 4.12)]`.

### FR-4: Strict Verification Badging & Authoritative Metadata
- Every synthesized response must include an **Authoritative Metadata Header**:
  - Document Title & Code (e.g., `Ground Operations Manual - GOM-REV-2026.2`)
  - Effective Date & Status (e.g., `Effective: 15-JAN-2026 | Status: Verified Active`)
  - Section & Page Reference (e.g., `Chapter 5 (Ramp Safety), Section 5.3.2, p. 142`)
  - Direct deep-link to the verified source PDF in the electronic document management system.

### FR-5: Step-by-Step Procedure Checklist Generation
- Where applicable, operational procedures must be formatted as numbered sequential action steps.
- Each step must clearly distinguish between:
  - **Mandatory Actions** (designated with `MUST` or `SHALL` in bold)
  - **Advisory Actions** (designated with `SHOULD` or `RECOMMENDED`)
  - **Prohibitions** (designated with `DO NOT` or `NEVER` in red alert styling)

### FR-6: Pre-requisite Safety Warnings & PPE Highlighting
- Any procedural response involving hazardous conditions (fueling, high voltage, jet blast hazard areas, de-icing fluids, dangerous goods) must render a prominent **Safety Alert Box** at the very top of the response before procedural steps.
- Prerequisite Personal Protective Equipment (PPE) (e.g., high-visibility vest, ear defenders, chemical goggles, safety boots) must be surfaced immediately.

### FR-7: Historical & Superseded Archive Exploration Mode (Auditor Role Only)
- In standard mode, superseded procedures are strictly hidden from operational queries.
- For compliance auditors and incident investigators, the system shall provide an explicit `Audit Mode` toggle.
- When `Audit Mode` is activated, searching past procedures will display a prominent warning watermark/banner:
  > **WARNING: SUPERSEDED PROCEDURE - FOR INVESTIGATION / AUDIT PURPOSES ONLY. DO NOT EXECUTE OPERATING ON THE RAMP.**

### FR-8: Frontline Discrepancy & Feedback Loop
- Ground staff shall have a one-tap feedback mechanism (`Thumbs Up`, `Report Discrepancy`, `Flag Ambiguity`).
- Reporting a discrepancy triggers an immediate notification to the Station Operations Quality & Safety team, creating an audit ticket.

### FR-9: Emergency Quick-Access & Offline Fallback
- Critical emergency procedures (e.g., *Aircraft Fuel Spill on Apron*, *Lithium Battery Thermal Runaway in Cabin/Hold*, *Evacuation Slide Accidental Deployment*, *Severe Ramp Weather Stop*) must be cached locally on devices for instant zero-network retrieval.

---

## 6. Non-Functional Requirements (NFR)

### 6.1 Performance & Latency
- **NFR-1.1:** Response latency for standard queries must achieve $P_{95} \le 2.5\text{ seconds}$ and $P_{99} \le 4.0\text{ seconds}$ on 4G/LTE ramp network conditions.
- **NFR-1.2:** Ingestion and indexing pipeline must process and activate emergency safety bulletins within $\le 5\text{ minutes}$ of corporate publication.

### 6.2 Availability & Reliability
- **NFR-2.1:** High availability of $99.95\%$ uptime ($24/7/365$) with active-passive multi-region failover.
- **NFR-2.2:** Zero scheduled maintenance downtime during airport peak operational banks (05:00–23:00 local station time).

### 6.3 Security, Privacy & Access Control
- **NFR-3.1:** Role-Based Access Control (RBAC) integrated with enterprise identity providers (Okta / Azure AD / Ping) using SAML 2.0 / OIDC.
- **NFR-3.2:** Procedure documents classified as Proprietary/Restricted; all data at rest encrypted using AES-256; all data in transit encrypted using TLS 1.3.
- **NFR-3.3:** Strict multi-tenant isolation if deployed across partner codeshare carriers or ground handling agencies (e.g., Swissport, Menzies, Dnata).

### 6.4 Auditability & Compliance
- **NFR-4.1:** Complete immutable logging of every query, matched vector chunks, resolved supersession tree, model prompt, raw response, and user interaction timestamp.
- **NFR-4.2:** Retention of audit trails for a minimum of 7 years in compliance with FAA Part 121 / ICAO Annex 6 standards for incident investigation.

### 6.5 Usability & Hardware Form Factor
- **NFR-5.1:** High-contrast daylight visual theme optimized for direct sunlight readability on tarmac aprons.
- **NFR-5.2:** Minimum touch target size of $48 \times 48\text{ dp}$ to facilitate operation with rugged protective gloves.
- **NFR-5.3:** Clean typography with high font legibility and clear color coding for danger/caution/info.

---

## 7. Safety Constraints & Anti-Hallucination Guardrails

1. **Strict Citation Grounding (Zero Confabulation):**
   - The generation model is strictly prohibited from interpolating, extrapolating, or inventing procedural steps not explicitly present in the retrieved context.
   - If the retrieved context does not contain sufficient verified information to answer the query, the system **MUST FAIL CLOSED** with an explicit refusal:
     > *"No verified active procedure found in the current operational manuals for this query. Please consult your Station Duty Manager or Ramp Supervisor immediately."*
2. **Deterministic Precedence Hierarchy:**
   - When a local airport directive, airline safety bulletin, and base GOM contain contradictory instructions, the system must deterministically resolve precedence using the aviation regulatory hierarchy (Regulatory Directives > Emergency Safety Bulletins > Local Station Operating Procedures > Base GOM). It must never leave the conflict to model discretion.
3. **Mandatory Human-in-the-Loop for Irreversible Operations:**
   - Any procedure involving hazardous material declaration, aircraft towing without brake pressure, or emergency fuel shutoff must require the user to acknowledge: *"I have verified this procedure against the physical aircraft configuration and notified the Ramp Lead."*

---

## 8. Out-of-Scope Features (Day 1 / MVP Boundaries)

To ensure razor-sharp focus on safety-critical procedural intelligence, the following capabilities are explicitly declared **Out-of-Scope** for this initial release:

- Direct automated dispatch or telemetry integration with aircraft Flight Management Systems (FMS) / ACARS.
- Automated document authoring or unsupervised automated manual revision without human Flight Ops review.
- Automated biometric facial recognition for ground crew sign-off.
- Passenger-facing baggage tracking or self-service conversational bots.
- Direct mechanical maintenance diagnostics (reserved for Part 145 Aircraft Maintenance Manual / AMM systems).

---

## 9. Acceptance Criteria (PRD & Requirements Gate)

- [x] Clear articulation of target ground operational personas, environment constraints, and pain points.
- [x] Quantifiable operational and technical metrics defined ($<2.5\text{s}$ latency, $0.00\%$ superseded procedures).
- [x] Functional requirements detailed covering querying, scoping, supersession resolution, citation, and audit.
- [x] Non-functional requirements established for performance, availability, security, and daylight usability.
- [x] Explicit safety constraints and fail-closed anti-hallucination protocols defined.
- [x] Strict scope boundary separating core procedure retrieval from future maintenance/flight deck capabilities.
