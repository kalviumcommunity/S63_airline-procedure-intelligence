# UX Architecture & Wireframe Specifications
## SkyOps Intelligence: Ground-Staff Operational Experience

**Document Status:** Approved Baseline  
**Design Identifier:** SKY-UX-001  
**Target Milestone:** 3.9 (Mock UX & Wireframe Specification)  
**Applicable Milestones:** 3.8, 3.9, 3.37  
**Effective Date:** 2026-10-27  
**Author:** Airline Human Factors & Ground Operations UX Taskforce  

---

## 1. Operational Environment & Human Factors

Designing for airline tarmac and gate personnel differs fundamentally from conventional enterprise software. Ground staff operate under unique physical, cognitive, and environmental constraints:

1. **Severe Ambient Glare & Variable Weather:**
   - Apron operations occur in direct sunlight, heavy downpours, freezing rain, and night conditions. Standard low-contrast UI palettes wash out completely under 100,000 lux tarmac sunlight.
   - *Design Response:* High-contrast daylight mode with minimum contrast ratio $\ge 7:1$ (WCAG AAA), high-legibility bold typography, and distinct dark/light mode toggles.
2. **Heavy Protective Gear (Glove Ergonomics):**
   - Ground personnel wear thick thermal or impact-resistant leather work gloves.
   - *Design Response:* Minimum touch target sizing of $48 \times 48\text{ dp}$ (recommended $56\text{ dp}$ for primary actions), large card buttons, and generous touch margins ($\ge 12\text{ px}$).
3. **Cognitive Pressure & Noise (90–115 dB):**
   - Jet engines, APUs, and Ground Support Equipment (GSE) create an overwhelming auditory environment. Voice-only interfaces are unreliable; text must be digestible in $<5$ seconds.
   - *Design Response:* Hierarchical card format: Critical Safety Warnings $\to$ Action Step Checklist $\to$ PPE Prerequisites $\to$ Source Citations.
4. **Intermittent Ramp Connectivity:**
   - Metal aircraft fuselages and remote apron parking pads frequently obstruct 4G/5G and airport Wi-Fi signals.
   - *Design Response:* Persistent offline indicator, edge-cached emergency procedures, and instant state feedback.

---

## 2. Primary User Journey: Ask → Retrieve → Verify → Review

The end-to-end journey guides ground staff from an urgent question to verified compliance:

```
+----------------------------------------------------------------------------------------------------+
|                                    PRIMARY USER JOURNEY                                            |
+-------------------+--------------------+--------------------+--------------------+-----------------+
|   STEP 1: ASK     |   STEP 2: RETRIEVE |   STEP 3: VERIFY   |   STEP 4: REVIEW   |  STEP 5: EXECUTE|
|                   |                    |                    |                    |                 |
| Ground staff      | Hybrid RAG engine  | Supersession graph | Clear checklist    | Frontline staff |
| enters query or   | searches dense &   | checks active      | rendered with      | performs step   |
| selects quick     | sparse indices;    | status, station    | mandatory verbs,   | and marks       |
| chip; scopes      | extracts candidate | code, fleet type,  | required PPE,      | verification or |
| Station & Fleet.  | passages.          | & precedence.      | & deep citations.  | logs feedback.  |
+-------------------+--------------------+--------------------+--------------------+-----------------+
```

### Detailed Journey Steps:
1. **Ask Procedure Question:**
   - User opens SkyOps on rugged mobile tablet (e.g., Getac / Zebra).
   - User selects current Station (e.g., `ORD`) and Fleet (e.g., `A321neo`), or system auto-populates from flight dispatch assignment.
   - User types or selects query: *"Can we fuel with passengers embarking?"*
2. **Retrieve Supporting Passages:**
   - Multi-stage hybrid search locates relevant sections across GOM Chapter 6 (Fueling), Safety Bulletin OSB-2026-04 (Boarding Fuel Protocol), and FAA Advisory Circular AC 150/5230-4B.
   - Passages are extracted with section codes and timestamps.
3. **Verify Applicability & Supersession:**
   - System evaluates temporal validity (`effective_from <= NOW() < effective_until`).
   - Identifies that OSB-2026-04 supersedes GOM Section 6.2.1 regarding emergency exit stair placement during fueling.
   - Precedence engine confirms OSB-2026-04 (Level 2) overrides base GOM (Level 4).
4. **Review Cited Answer:**
   - Assistant displays green `[VERIFIED ACTIVE]` badge.
   - Displays bold safety warning: *"Emergency exit doors MUST remain unobstructed with two stairs or jet bridge attached."*
   - Step-by-step checklist formatted with bold mandatory terms (`MUST`, `SHALL`, `DO NOT`).
   - Grounded citations link directly to verified source documents.
5. **Execution & Feedback:**
   - Staff confirms procedure compliance on ramp.
   - Optional one-tap feedback (`Thumbs Up` / `Flag Ambiguity`) recorded in audit log.

---

## 3. Wireframes: Core Screens & Safety States

### Wireframe 1: Main Search & Operational Dashboard (Mobile / Tablet)
```
+------------------------------------------------------------------------+
| [=] SkyOps Intelligence   [Station: ORD v] [Fleet: A321neo v]  [Sun/Moon]|
+------------------------------------------------------------------------+
|  (!) RAMP ALERT: Freezing Fog Advisory in effect for KORD runways.      |
+------------------------------------------------------------------------+
|                                                                        |
|   Search Ground Procedures, Bulletins, & Directives                    |
|  +------------------------------------------------------------------+  |
|  | [Q] Fueling with passengers on board procedure...          [Clear]|  |
|  +------------------------------------------------------------------+  |
|                                                                        |
|  Quick Scenarios:                                                      |
|  [ A321neo Fuel Spill ] [ Gate Lithium Fire ] [ Icy Pushback Check ]  |
|                                                                        |
|  Active Filters: [ Station: ORD (Active LOP) ] [ Aircraft: A321neo ]    |
|                                                                        |
+------------------------------------------------------------------------+
|  RECENT SEARCHES & STATION PINNED CHECKLISTS                           |
|  - GOM 5.3.2: High-wind cargo door operating limits (Active)           |
|  - OSB-2026-08: APU exhaust hazard clearance zone (Updated 14-Feb)     |
|  - DGR Class 9: Gate-checked battery inspection protocol               |
+------------------------------------------------------------------------+
| [?] Emergency Hotline   [v] Offline Sync: OK   [O] Audit Log: Active   |
+------------------------------------------------------------------------+
```

---

### Wireframe 2: Standard Active Procedure with Deep Citations
```
+------------------------------------------------------------------------+
| [<- Back]  Procedure Response                     [Share] [Report Issue]|
+------------------------------------------------------------------------+
| [VERIFIED ACTIVE]  GOM 6.2.1 (Overridden by OSB-2026-04)               |
| Effective: 2026-02-01 | Precedence: Level 2 Safety Bulletin | KORD     |
+------------------------------------------------------------------------+
| (!) MANDATORY SAFETY WARNING                                           |
| Ground fueling while passengers embark is STRICTLY PROHIBITED unless   |
| designated evacuation routes are manned and clear of GSE obstructions. |
+------------------------------------------------------------------------+
| REQUIRED PPE:                                                          |
| [ High-Vis Vest ]  [ Steel-Toe Boots ]  [ Ear Defenders ]              |
+------------------------------------------------------------------------+
| PROCEDURAL ACTION STEPS:                                               |
|                                                                        |
| 1. Fueling Supervisor MUST notify Flight Crew and Cabin Purser before  |
|    connecting the fuel hydrant coupler.                                |
|                                                                        |
| 2. Main passenger door L1 MUST remain connected to jet bridge or       |
|    mobile passenger stairs with unobstructed egress path.              |
|                                                                        |
| 3. Door R2 or L2 MUST have ground stairs positioned OR dedicated slide  |
|    deployment clearance area kept completely clear of fuel tankers.    |
|                                                                        |
| 4. DO NOT activate or position Ground Power Units (GPU) within 3 meters|
|    of fueling vent outlets during active pumping.                      |
+------------------------------------------------------------------------+
| AUTHORITATIVE SOURCE CITATIONS:                                        |
| [1] OSB-2026-04: Ground Fueling Safety Revision (p. 2, Sec 3.1) [PDF]  |
| [2] GOM Chapter 6: Fuel Servicing Procedures (p. 184, Sec 6.2.1) [PDF] |
| [3] FAA Advisory Circular AC 150/5230-4B (Sec 4.8)                    |
+------------------------------------------------------------------------+
| [v] Mark Checklist Complete   [!] Flag Discrepancy   [?] Call Ramp Lead|
+------------------------------------------------------------------------+
```

---

### Wireframe 3: Superseded-Document Warning State (Safety Guardrail)
*Rendered if user searches an older document reference or views historical records.*

```
+------------------------------------------------------------------------+
| [<- Back]  Historical Procedure Inquiry                                |
+------------------------------------------------------------------------+
| !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! |
| !                       CRITICAL SAFETY WARNING                      ! |
| !       YOU ARE VIEWING A SUPERSEDED / INACTIVE PROCEDURE            ! |
| !        DO NOT EXECUTE THIS PROCEDURE ON THE ACTIVE RAMP             ! |
| !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! |
| Document: GOM 2024.2, Section 8.4 (Lithium Device Response)           |
| Status: SUPERSEDED on 2026-01-10 by Bulletin OSB-2026-03              |
| Reason: Incompatible with FAA SAFO 25002 Fire Containment Standards    |
+------------------------------------------------------------------------+
|                                                                        |
|  [ >> CLICK HERE TO VIEW ACTIVE REPLACEMENT PROCEDURE (OSB-2026-03) ]  |
|                                                                        |
+------------------------------------------------------------------------+
| Archived Text (For Investigation & Audit Reference Only):              |
| "...damaged consumer electronics should be placed in a standard sealed |
| polyethylene evidence bag and delivered to station lost-and-found..."  |
| [!] HAZARD: Risk of thermal runaway flash fire in polyethylene bag!    |
+------------------------------------------------------------------------+
| Logged in Safety Audit Store | User: EMP-4491 | Station: ORD          |
+------------------------------------------------------------------------+
```

---

### Wireframe 4: No-Evidence Refusal (Fail-Closed State)
*Rendered when query similarity is below safety threshold ($\tau < 0.82$) or outside indexed manuals.*

```
+------------------------------------------------------------------------+
| [<- Back]  Procedure Search Result                                     |
+------------------------------------------------------------------------+
| [X] NO VERIFIED ACTIVE PROCEDURE FOUND                                  |
| Query: "Can we use towbarless tug on nose gear with flat tire?"         |
+------------------------------------------------------------------------+
| (!) SAFETY COMPLIANCE NOTICE:                                          |
| No verified active operational procedure or manufacturer bulletin was   |
| found matching this query for Fleet: A321neo / Station: ORD.           |
|                                                                        |
| In accordance with Airline SMS & FAA Part 121 Safety Regulations:     |
| - DO NOT improvise or extrapolate non-standard towing procedures.      |
| - Ground movement of aircraft with tire deflation requires direct      |
|   Engineering Maintenance (Part 145) authorization.                    |
+------------------------------------------------------------------------+
| IMMEDIATE ESCALATION CHANNELS:                                         |
|                                                                        |
| [ Call Station Maintenance Control: Ext. 4410 ]                        |
| [ Page Ramp Duty Manager (ORD SOC): Ext. 4422 ]                        |
| [ Open Incident / Procedure Inquiry Ticket   ]                        |
+------------------------------------------------------------------------+
| Related Verified Procedures:                                           |
| - GOM 5.2.4: Standard Aircraft Towing Protocols (Normal Tires)         |
| - GOM 9.1.2: Aircraft Tire Deflation Ramp Reporting Checklist          |
+------------------------------------------------------------------------+
```

---

### Wireframe 5: Conflicting-Sources Resolution State
*Rendered when local airport authority (LOP) conflicts with corporate GOM or emergency bulletin.*

```
+------------------------------------------------------------------------+
| [<- Back]  Conflict Resolution Analysis                                |
+------------------------------------------------------------------------+
| [?] PROCEDURAL PRECEDENCE CONFLICT RESOLVED                             |
| Topic: De-icing Holdover Inspection Responsibilities at KORD           |
+------------------------------------------------------------------------+
| PRECEDENCE HIERARCHY RESOLUTION:                                       |
|                                                                        |
| [HIGHEST AUTHORITY APPLIED: LEVEL 1 - REGULATORY DIRECTIVE]            |
| -> FAA Emergency Airworthiness Directive AD-2026-02-04                |
|    Rule: Physical tactile check mandatory for all A320 wing surfaces   |
|    prior to pushback when freezing drizzle is reported.                |
|                                                                        |
| [SUPERSEDED INSTRUCTION: LEVEL 4 - BASE GOM 7.3.1]                     |
| -> Base GOM allows visual check only from cabin window under light ice.|
|    Status: OVERRIDDEN BY FAA AD FOR ALL HUB STATIONS.                  |
+------------------------------------------------------------------------+
| GOVERNING OPERATIONAL MANDATE:                                         |
| 1. Ground De-icing Crew MUST perform physical hand-tactile check of     |
|    the wing leading edge within 5 minutes prior to dispatch.           |
| 2. Visual inspection alone is NULL AND VOID under current AD.          |
+------------------------------------------------------------------------+
| Citations: FAA AD-2026-02-04 | KORD Winter LOP-12 | GOM Rev 2026.1     |
+------------------------------------------------------------------------+
```

---

### Wireframe 6: Document Upload & Bulletin Ingestion Flow (Safety Officer View)
```
+------------------------------------------------------------------------+
| [X] Document Ingestion & Supersession Management Portal                 |
+------------------------------------------------------------------------+
| Step 1: Upload Source Document                                         |
| [ Browse / Drag PDF: OSB-2026-09_APU_Blast_Zone.pdf (2.4 MB) ]        |
|                                                                        |
| Step 2: Document Classification & Authority                            |
| Document Type:    [ Level 2: Operations Safety Bulletin (OSB) v ]      |
| Document ID:      [ OSB-2026-09                                 ]      |
| Effective Date:   [ 2026-03-01 00:00 UTC                        ]      |
| Expiration Date:  [ INDEFINITE (Until next GOM revision)        ]      |
|                                                                        |
| Step 3: Supersession & Override Targeting                              |
| Target Document:  [ GOM 2026.2                                   v ]   |
| Target Chapter:   [ Chapter 5: Ramp Operations                  v ]   |
| Target Section:   [ Section 5.8: APU Hazard Zones               v ]   |
| Relationship:     (o) REPLACES   ( ) AMENDS   ( ) SUSPENDS             |
|                                                                        |
| Step 4: Verification & Digital Signature                               |
| Safety Officer:   Marcus B. (Chief Inspector #94812)                   |
| Digital Key:      [ Validated PKI Certificate: 0x8F92...B31 ]          |
|                                                                        |
| [ Preview Graph Impact ]                 [ Sign & Publish to Vector DB ]|
+------------------------------------------------------------------------+
```

---

## 4. Accessibility & Responsive Engineering Standards

1. **Touch Ergonomics & Ramp Glove Support:**
   - Primary buttons: Minimum height $52\text{ px}$, width $100\%$ on mobile devices, minimum horizontal spacing $16\text{ px}$.
   - Text inputs: Large padding ($16\text{ px}$ vertical) with clear-all `[X]` buttons.
2. **Daylight Sunlight Mode (Contrast Compliance):**
   - Background: Pure White `#FFFFFF` or High-Contrast Yellow `#FFF9C4` for alerts.
   - Text: Pure Charcoal `#0D1117` with bold font weight (600–700) for procedural instructions.
   - Contrast ratio: $\ge 8.5:1$ against background, exceeding WCAG 2.1 AAA.
3. **Screen Reader & Keyboard Accessibility (ARIA):**
   - `aria-live="polite"` for asynchronous search result loading.
   - `aria-alert="true"` for superseded warning banners.
   - Semantic `<header>`, `<main>`, `<article>`, and `<nav>` elements throughout.
