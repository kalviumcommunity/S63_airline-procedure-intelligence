# SkyOps Intelligence Clickable Prototype (Milestone 3.9)

A lightweight, zero-dependency, self-contained interactive prototype demonstrating the primary user journey and safety-critical states for airline ground operations.

---

## 1. Quick Start / How to Open

Since the prototype is built with modern, vanilla HTML5, CSS3, and JavaScript, it requires **no external packages, Node.js server, or build tools**.

### Option A: Open directly in your browser
Simply double-click [`prototype/index.html`](index.html) or run in PowerShell:
```powershell
Start-Process "prototype\index.html"
```

### Option B: Local Python HTTP Server
```bash
python -m http.server 8080 --directory prototype
```
Then navigate to: `http://localhost:8080`

---

## 2. Interactive States & Scenarios Demonstrated

Use the top **SkyOps State Simulator** bar or type corresponding keywords in the search bar:

| Scenario / State | Description | How to Trigger | Key Safety Features Demonstrated |
| :--- | :--- | :--- | :--- |
| **1. Standard Active Procedure** | Displays verified active procedure with an overriding bulletin. | Click **"1. Active Procedure"** or preset chip *"Fueling with Pax On Board"*. | `[VERIFIED ACTIVE]` badge, `[OSB Override]` badge, mandatory modal verbs (`MUST`, `SHALL`, `DO NOT`), required PPE badges, and deep source PDF citations. |
| **2. Superseded-Document Warning** | Safety guardrail activated when user searches an obsolete document section. | Click **"2. Superseded Warning"** or preset chip *"Damaged Lithium Battery"*. | High-visibility red alert banner, warning against ramp execution, citation of invalidating order, and a direct 1-click button to load the active replacement bulletin (`OSB-2026-03`). |
| **3. No-Evidence Refusal (Fail-Closed)** | System refuses to extrapolate or invent procedures when no verified procedure exists. | Click **"3. No-Evidence Refusal"** or preset chip *"Non-Standard Towing"*. | Fail-closed refusal card, explanation of why extrapolation is prohibited, and direct one-tap emergency escalation buttons (Maintenance Control & Ramp Duty Lead). |
| **4. Conflicting Sources Resolution** | Automatically resolves conflicting directives using the Aviation Precedence Hierarchy. | Click **"4. Conflicting Sources"** or preset chip *"De-icing Tactile Check"*. | Side-by-side comparison showing Level 1 Regulatory Directive (FAA AD) overriding Level 4 Base GOM, with governing checklist rendered. |
| **5. Document Upload & Ingestion** | Ingestion portal for Flight Operations & Safety Officers. | Click **"5. Upload Document"** button in toolbar. | PDF upload simulation, document authority classification, supersession relationship targeting (`REPLACES`, `AMENDS`, `SUSPENDS`), and cryptographic digital signature validation. |

---

## 3. Human Factors & Accessibility Controls

- **Daylight Ramp Mode:** Toggle via the top right `☀️ Daylight Mode` button to switch between High-Contrast Sunlight Mode (contrast ratio $>8.5:1$ for tarmac aprons), Low-Light Night Mode, and Standard Mode.
- **Ramp Glove Touch Targets:** Primary touch targets are sized at $50\text{--}54\text{ px}$ with clear tap margins.
- **Contextual Scoping:** Dynamic dropdown selectors for **Station** (`KORD`, `KJFK`, `KLAX`, `KDFW`), **Fleet** (`A321neo`, `A320`, `B737`, `B787`), and **Role** (`Ramp`, `Gate`, `Fueling`, `Baggage`).
