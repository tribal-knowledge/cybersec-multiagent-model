# Architecture: Cybersecurity Multi-Agent Learning Loop Model

## Design Philosophy

The model is architected around three principles:

1. **Separation of concerns** — Each agent owns exactly one domain of expertise. Agents do not overlap functions; conflicts between their outputs are surfaced explicitly and resolved by the Coach.
2. **Human-in-the-loop by design** — The learning loop requires human expert review at every cycle. The system is not autonomous. It amplifies expert judgment, it does not replace it.
3. **Compounding over time** — The model is designed to improve with use. Every workflow run generates feedback data. Every feedback record is potential playbook material. The value accumulates.

---

## Agent Interaction Model

### Sequential vs. Parallel Execution

The three specialist agents (Architect, Validation, Governance) can run in two modes:

**Sequential (default, recommended for complex scenarios)**
```
Coach → Architect → Validation (reads Architect output) → Governance (reads both) → Coach
```
Each agent reasons over the prior agent's output, enabling richer cross-agent analysis. The Validation Agent can specifically challenge the Architect's assumptions. The Governance Agent can flag compliance implications of specific technical controls.

**Parallel (recommended for speed-sensitive workflows)**
```
Coach → [Architect | Validation | Governance] simultaneously → Coach consolidates
```
Faster, but agents operate independently. The Coach bears more responsibility for synthesis and conflict resolution.

For most security assessments, sequential execution produces materially better outputs.

---

## Information Flow

### Input Contract (Business Request → Coach)

The Coach receives:
- **Business request** — what the human needs assessed
- **Asset description** — the system, application, or process under review
- **Scope boundaries** — what is in and out of scope
- **Compliance context** — which regulatory frameworks apply
- **Risk appetite** — organizational thresholds for acceptable risk
- **Prior findings** — any existing assessments, pen test results, or audit findings relevant to this scenario

### Coach → Architect Contract

The Coach forwards:
- Structured asset description
- Threat modeling methodology directive (STRIDE, PASTA, or hybrid)
- Specific security concerns from the business request
- Relevant architectural context (cloud provider, deployment model, trust boundaries)

### Architect → Validation Contract

The Validation Agent receives the Architect's full output plus:
- Coach directive to challenge specific threat categories
- Attack surface scope (what the Validation Agent should attempt to circumvent)
- MITRE ATT&CK version to use for mapping

### [Architect + Validation] → Governance Contract

The Governance Agent receives both prior outputs plus:
- Applicable compliance frameworks
- Known organizational policy constraints
- Audit timeline if relevant

### Coach Consolidation Contract

The Coach receives all three agent outputs and applies:
- **Deduplication** — same finding cited by multiple agents is merged
- **Conflict resolution** — contradictory severity ratings are adjudicated with explicit reasoning
- **Risk prioritization** — findings ranked by business impact, exploitability, and compliance exposure
- **Executive synthesis** — output calibrated to the stated audience (CISO, board, engineering lead)

---

## Feedback Loop Architecture

```
Agent Outputs
      |
      V
Human Expert Review
      |
      ├── Approved finding ──────────────> Playbook archive
      |
      ├── Corrected finding ─────────────> Feedback record (YAML)
      |                                          |
      └── Missed finding ────────────────> Feedback record (YAML)
                                                 |
                                                 V
                                    Prompt refinement candidate
                                                 |
                                                 V
                                    Versioned prompt update (PR)
                                                 |
                                                 V
                                    Improved agent behavior
```

### Feedback Record Storage

Feedback records live in `learning_loop/feedback_records/`. They are YAML files following the schema in `learning_loop/feedback_capture.md`. Records are:
- Committed to git (full history preserved)
- Periodically reviewed by maintainers for prompt refinement candidates
- Aggregated into eval baseline updates on each minor version release

---

## Prompt Versioning

System prompts are version-controlled in `prompts/` using semantic versioning in the filename:
- `architect_system_prompt_v1.0.0.md` — initial release
- `architect_system_prompt_v1.1.0.md` — minor behavioral improvement
- `architect_system_prompt_v2.0.0.md` — breaking change in output format

The `prompts/` directory always contains the canonical current version under the base filename (e.g., `architect_system_prompt.md`) as a symlink or copy of the latest. Prior versions are retained for reproducibility.

---

## Security Considerations for the System Itself

Running a multi-agent security assessment system introduces its own attack surface:

- **Prompt injection** — Malicious content in the asset under review (e.g., a web app's error messages, a document's metadata) could attempt to hijack agent behavior. Input sanitization before injection into prompts is mandatory.
- **Output trust** — Agent outputs must never be treated as authoritative without human review. The system is advisory, not decisional.
- **API key handling** — LLM API keys must be managed via secrets management (e.g., AWS Secrets Manager, HashiCorp Vault), never committed to the repository.
- **Data residency** — Sensitive architectural details submitted to the agents may be processed by third-party LLM APIs. Review your LLM provider's data processing agreements before submitting regulated data.
- **Access control** — Restrict write access to `prompts/` — unauthorized prompt changes are a supply chain risk to the model's integrity.
