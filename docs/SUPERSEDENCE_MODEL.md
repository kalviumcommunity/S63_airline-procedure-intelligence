# Version & Supersession Resolution Model
## SkyOps Intelligence: Ensuring Zero-Stale Procedure Delivery

**Document Status:** Approved Baseline  
**Model Identifier:** SKY-SUPER-001  
**Target Milestone:** 3.37 (Supersession & Document Lifecycle Engine)  
**Applicable Milestones:** 3.1, 3.8, 3.37  
**Effective Date:** 2026-10-27  
**Author:** Operational Safety & Systems Assurance Working Group  

---

## 1. Problem Definition: The Supersession Hazard in Aviation

In commercial aviation, the operational manual is never static. Ground Operations Manuals (GOMs) undergo planned periodic revisions (typically twice a year). However, real-world operational incidents, aircraft manufacturer alerts (Boeing Multi-Operator Messages, Airbus Operator Information Transmissions), and civil aviation directives (FAA Emergency Airworthiness Directives, EASA Safety Information Bulletins) trigger rapid, unscheduled operational changes.

These rapid updates are published as:
- **Operations Safety Bulletins (OSBs)**
- **Safety Action Notices (SANs)**
- **Station Operations Advisories (SOAs)**
- **Temporary Revisions (TRs)**

### The Hazard:
If an AI assistant retrieves text from the comprehensive 1,200-page GOM v2025.1 without realizing that **OSB-2026-03** issued two weeks ago changed the maximum allowable fuel imbalance prior to pushback or altered the lithium battery fire suppression protocol, **it provides an obsolete, illegal, and potentially catastrophic procedure to ground staff.**

---

## 2. Regulatory Precedence Hierarchy

SkyOps Intelligence implements a deterministic, multi-tiered hierarchy of authority. When two procedural documents offer conflicting guidance on the same operational topic, the conflict is resolved strictly according to legal and operational precedence:

```
+-------------------------------------------------------------------------------+
| LEVEL 1: Regulatory Directives & Emergency Airworthiness Directives (EADs)   |
| (FAA, EASA, DGCA, ICAO) - Highest Legal Authority. Absolute Override.         |
+---------------------------------------+---------------------------------------+
                                        | overrides
                                        v
+-------------------------------------------------------------------------------+
| LEVEL 2: Airline Operations Safety Bulletins (OSBs) & Temporary Revisions (TR)|
| Issued by Airline Safety Director. Immediate operational enforcement.         |
+---------------------------------------+---------------------------------------+
                                        | overrides
                                        v
+-------------------------------------------------------------------------------+
| LEVEL 3: Local Station Operating Procedures (LOPs)                            |
| Airport-specific constraints (e.g., ORD winter ops, JFK gate push restrictions|
+---------------------------------------+---------------------------------------+
                                        | overrides
                                        v
+-------------------------------------------------------------------------------+
| LEVEL 4: Base Ground Operations Manual (GOM) & Airport Handling Manual (AHM)  |
| Baseline corporate standard operating procedure (SOP).                        |
+-------------------------------------------------------------------------------+
```

---

## 3. The Supersession Directed Acyclic Graph (DAG)

To model document evolution across time, SkyOps Intelligence maintains a **Supersession Graph**. Rather than treating documents as disconnected flat files, every procedure chunk is a node in a versioned DAG.

### 3.1 Relationship Types
A relationship between Document/Chunk $B$ and Document/Chunk $A$ can take one of four explicit edge types:
1. `REPLACES`: Chunk $B$ completely invalidates and substitutes Chunk $A$.
2. `AMENDS`: Chunk $B$ modifies specific parameters, steps, or warnings in Chunk $A$ while preserving unchanged steps.
3. `SUSPENDS`: Chunk $B$ temporarily halts the execution of Chunk $A$ pending further technical review or specific environmental conditions.
4. `EXTENDS`: Chunk $B$ adds local requirements (e.g., a station-specific cold weather rule) on top of base Chunk $A$ without deleting base rules.

### 3.2 Visualizing the Supersession Tree
```
  [GOM 2024.1 Sec 4.2] 
           |
           | superseded_by (REPLACES)
           v
  [GOM 2025.1 Sec 4.2] <------------------------------------+
           |                                                |
           +-----------------------------+                  | amends
           |                             |                  |
           | amends                      | amends           |
           v                             v                  |
  [OSB-2025-14 (Expired)]       [OSB-2026-03 (ACTIVE)] -----+
  (Effective until 2025-12-31)   (Effective: 2026-01-10 to INDEFINITE)
           |
      [INACTIVE]
```

---

## 4. Document Metadata Schema

Every document and procedure chunk in the database adheres to this strict schema:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "AeroProcedureChunk",
  "type": "object",
  "required": [
    "chunk_id",
    "document_id",
    "document_type",
    "precedence_level",
    "section_code",
    "version",
    "effective_from",
    "status",
    "superseded_by"
  ],
  "properties": {
    "chunk_id": { "type": "string", "example": "chk_gom_2026_ch4_s2" },
    "document_id": { "type": "string", "example": "DOC-GOM-2026.1" },
    "document_type": { 
      "type": "string", 
      "enum": ["REGULATORY_DIRECTIVE", "SAFETY_BULLETIN", "STATION_LOP", "BASE_GOM"] 
    },
    "precedence_level": { "type": "integer", "enum": [1, 2, 3, 4] },
    "section_code": { "type": "string", "example": "4.2.1" },
    "title": { "type": "string", "example": "De-icing Fluid Holdover Time Compliance" },
    "version": { "type": "string", "example": "2026.1" },
    "effective_from": { "type": "string", "format": "date-time" },
    "effective_until": { "type": ["string", "null"], "format": "date-time" },
    "status": { 
      "type": "string", 
      "enum": ["draft", "active", "superseded", "suspended", "revoked"] 
    },
    "supersedes": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "target_chunk_id": { "type": "string" },
          "relationship": { "type": "string", "enum": ["REPLACES", "AMENDS", "SUSPENDS", "EXTENDS"] },
          "amendment_details": { "type": "string" }
        }
      }
    },
    "superseded_by": { "type": ["string", "null"] },
    "verified_by_safety_officer": { "type": "string", "example": "EMP-94812 (Chief Safety Inspector)" },
    "verification_timestamp": { "type": "string", "format": "date-time" }
  }
}
```

---

## 5. Query-Time Supersession Resolution Algorithm

When a query is received, the engine enforces a four-stage filtration and precedence synthesis algorithm:

```python
def resolve_applicable_procedures(retrieved_candidates, current_time, station_code, fleet_type):
    """
    Deterministically resolves candidate procedure chunks to eliminate stale or
    superseded guidance and produce the single authoritative operational answer.
    """
    valid_active_chunks = []
    
    # STEP 1: Temporal & Status Filter
    for chunk in retrieved_candidates:
        # Check active status
        if chunk.status != "active":
            continue
            
        # Check temporal validity window
        if chunk.effective_from > current_time:
            continue  # Future procedure, not yet in force
        if chunk.effective_until is not None and chunk.effective_until <= current_time:
            continue  # Expired temporary bulletin
            
        # Check station and fleet applicability
        if not is_applicable(chunk, station_code, fleet_type):
            continue
            
        valid_active_chunks.append(chunk)

    # STEP 2: Supersession Pruning
    # Build map of chunks that have been superseded by active higher-precedence documents
    pruned_chunks = []
    for candidate in valid_active_chunks:
        # Check if any other candidate REPLACES this candidate
        is_replaced = False
        for superseder in valid_active_chunks:
            if any(s.target_chunk_id == candidate.chunk_id and s.relationship == "REPLACES" 
                   for s in superseder.supersedes):
                # Ensure the superseding document has higher or equal precedence
                if superseder.precedence_level <= candidate.precedence_level:
                    is_replaced = True
                    break
        if not is_replaced:
            pruned_chunks.append(candidate)

    # STEP 3: Hierarchical Precedence Sorting
    # Order: Level 1 (Regulatory) -> Level 2 (Bulletin) -> Level 3 (LOP) -> Level 4 (Base GOM)
    sorted_chunks = sorted(pruned_chunks, key=lambda c: (c.precedence_level, -c.effective_from.timestamp()))

    # STEP 4: Conflict & Override Annotation
    # If a Level 2 bulletin AMENDS a Level 4 GOM chunk, package both with explicit override metadata
    final_execution_context = package_amended_context(sorted_chunks)
    
    return final_execution_context
```

---

## 6. How the System Guarantees Zero Superseded Information

1. **Pre-Index Gating (Document Ingestion Gate):**
   - No document can enter the active vector store in an `active` status without a cryptographic digital signature from an authorized Airline Flight Operations / Safety officer.
   - When a new document or bulletin is marked `active`, an automated graph traversal immediately updates all target nodes:
     $$\text{Target Chunk}.\text{status} \leftarrow \text{"superseded"}$$
     $$\text{Target Chunk}.\text{superseded\_by} \leftarrow \text{New Chunk ID}$$
2. **Hard Database Query Partitions:**
   - Operational ramp queries execute against a database view that hard-filters `WHERE status = 'active' AND effective_from <= NOW() AND (effective_until IS NULL OR effective_until > NOW())`.
   - Superseded chunks reside in an isolated cold-storage table inaccessible to the primary ramp API endpoint.
3. **Retrieval-Time Graph Verification:**
   - Even if an active chunk mentions older context, the prompt assembler inspects its metadata against the Supersession Registry. If any newer bulletin touches the section code, the bulletin is forcibly merged into the LLM context window.
4. **Visual UI Badging & Transparency:**
   - Every response rendered to ground crew displays an authoritative badge:
     ```
     +-----------------------------------------------------------------------+
     | [VERIFIED ACTIVE] Ground Operations Manual (GOM) v2026.2              |
     | OVERRIDE IN EFFECT: Safety Bulletin OSB-2026-08 (Issued 14-Feb-2026)  |
     | Section: 5.3.2 | Precedence: Level 2 Safety Bulletin                  |
     +-----------------------------------------------------------------------+
     ```

---

## 7. Concrete Real-World Operational Walkthrough

### Scenario: Damaged Lithium-Ion Battery Discovered at Gate 32 (ORD)

#### Historical Context:
- **Base Document:** GOM 2025.1, Section 8.4 ("Dangerous Goods Handling"), published 2025-06-01.
  - *Instruction:* Place leaking or damaged consumer electronics in a sealable polyethylene bag and transport to station lost-and-found.
- **Superseding Event:** Safety Bulletin **OSB-2026-03**, published 2026-01-10 (Precedence: Level 2).
  - *Instruction:* In accordance with FAA SAFO 25002, any compromised or smoking lithium device MUST NOT be placed in polyethylene bags. It MUST be placed immediately into a dedicated Fire Containment Bag (FCB), soaked in cold water/aqueous agent if active thermal runaway occurs, and ground ramp dispatch must be notified for HAZMAT fire response.

#### SkyOps Intelligence Execution:
1. **Query:** Gate agent types: *"What do I do with a cracked, overheating laptop battery at the gate?"*
2. **Retrieval:** Vector search identifies GOM Section 8.4 and OSB-2026-03.
3. **Supersession Resolution:**
   - Engine identifies OSB-2026-03 has `precedence_level = 2` and has an `AMENDS` / `REPLACES` edge targeting GOM Section 8.4.
   - GOM 2025.1 Section 8.4 is marked `superseded` in the context window.
4. **Output Generation:**
   - Assistant outputs the OSB-2026-03 procedure with a high-priority red warning:
     > **MANDATORY SAFETY OVERRIDE (OSB-2026-03):** DO NOT use standard polyethylene bags. Utilize the Gate Emergency Fire Containment Bag (FCB) located under the jet bridge counter.
   - Cites OSB-2026-03 (Effective Jan 10, 2026) as the sole governing procedure.
   - Result: Catastrophic gate fire hazard averted.

