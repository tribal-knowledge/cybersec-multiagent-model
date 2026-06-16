# Evaluation Framework

## Purpose

This framework defines how agent outputs are measured against human expert baselines. It serves two purposes:
1. **Calibration** — establish whether current prompt versions produce outputs of acceptable quality
2. **Regression detection** — catch quality degradation when prompts are updated

Run evaluations against the test cases in `evals/test_cases/` before merging any prompt change.

---

## Evaluation Process

### Step 1: Select Test Cases
Use the 5 canonical test cases provided in `evals/test_cases/`. These cases have known human expert ground truth outputs. Do not use live client scenarios for calibration evals.

### Step 2: Run Each Agent
Execute each agent individually (using standalone runners in `agents/*/`) against each test case. Record outputs.

### Step 3: Score Against Rubric
Score each output on the dimensions below. Use the provided scoring rubric. Two independent scorers should assess each output; use the average if scores differ by more than 1 point.

### Step 4: Calculate Agent Score
For each agent, compute the weighted score across all dimensions (see weights below). Compare to the minimum acceptable threshold.

### Step 5: Record Results
Submit eval results as a PR against `evals/results/YYYY-MM-DD_vX.X.X.md` using the results template below.

---

## Scoring Dimensions by Agent

### Security Architect Agent

| Dimension | Weight | Description | Score 1 | Score 2 | Score 3 | Score 4 | Score 5 |
|---|---|---|---|---|---|---|---|
| Threat Coverage | 30% | STRIDE categories addressed for all in-scope components | <50% coverage | 50–65% | 65–80% | 80–90% | >90% |
| Framework Accuracy | 25% | Correct citations with version + control ID | <60% correct | 60–74% | 75–84% | 85–94% | ≥95% |
| Requirement Specificity | 20% | Each requirement maps to ≥1 control | <50% mapped | 50–64% | 65–79% | 80–89% | ≥90% |
| False Negative Rate | 15% | Critical/High threats missed vs. expert baseline | >30% missed | 20–30% | 10–19% | 5–9% | <5% |
| Output Parsability | 10% | Validation Agent can consume output without Coach mediation | Not parsable | Major gaps | Minor gaps | Mostly clean | Fully parsable |

**Minimum acceptable weighted score:** 3.5/5.0

---

### Validation Agent

| Dimension | Weight | Description | Score 1 | Score 2 | Score 3 | Score 4 | Score 5 |
|---|---|---|---|---|---|---|---|
| ATT&CK Mapping Accuracy | 30% | Correct technique IDs for identified threats | <60% correct | 60–74% | 75–84% | 85–94% | ≥95% |
| Control Bypass ID | 25% | % of bypasses found by human red teamers also found by agent | <50% | 50–64% | 65–79% | 80–89% | ≥90% |
| False Positive Rate | 20% | Findings rated non-issues by human expert | >25% | 20–24% | 10–19% | 5–9% | <5% |
| Gap Coverage | 15% | % of unmitigated threats from expert baseline identified | <60% | 60–74% | 75–84% | 85–94% | ≥95% |
| Severity Calibration | 10% | Severity within one level of expert rating | <70% | 70–79% | 80–84% | 85–94% | ≥95% |

**Minimum acceptable weighted score:** 3.5/5.0

---

### Governance Agent

| Dimension | Weight | Description | Score 1 | Score 2 | Score 3 | Score 4 | Score 5 |
|---|---|---|---|---|---|---|---|
| Framework Citation Accuracy | 35% | Correct control IDs and versions | <70% correct | 70–79% | 80–89% | 90–94% | ≥95% |
| Gap Identification | 30% | % of compliance gaps from expert baseline found | <60% | 60–74% | 75–84% | 85–94% | ≥95% |
| False Positive Rate | 15% | Findings rated non-applicable by GRC reviewer | >20% | 15–19% | 10–14% | 5–9% | <5% |
| Conflict Detection | 10% | % of inter-framework conflicts surfaced | <70% | 70–79% | 80–89% | 90–99% | 100% |
| Audit Readiness Calibration | 10% | Disposition matches auditor rating | <70% | 70–79% | 80–84% | 85–94% | ≥95% |

**Minimum acceptable weighted score:** 3.8/5.0 (higher bar — compliance errors are higher risk than technical analysis errors)

---

### Coach Agent

| Dimension | Weight | Description | Score 1 | Score 2 | Score 3 | Score 4 | Score 5 |
|---|---|---|---|---|---|---|---|
| Conflict Resolution Accuracy | 25% | Resolved conflicts rated correct by expert | <60% | 60–69% | 70–79% | 80–89% | ≥90% |
| Risk Prioritization Alignment | 25% | Top-3 findings match expert prioritization | <50% | 50–64% | 65–74% | 75–84% | ≥85% |
| Synthesis Completeness | 20% | Material findings preserved in executive output | <80% | 80–84% | 85–89% | 90–94% | ≥95% |
| Executive Readability | 15% | Output interpretable by non-technical executive | Not interpretable | Major jargon | Some jargon | Mostly clear | Fully clear |
| Escalation Accuracy | 15% | Escalates cases that require escalation; avoids unnecessary escalation | >10% miss rate | 5–10% miss | 2–4% miss | 1% miss | 0% miss + <5% unnecessary |

**Minimum acceptable weighted score:** 3.5/5.0

---

## Severity Scale Reference

Used consistently across all agents for severity assignment:

| Rating | Definition |
|---|---|
| Critical | Exploitable with high confidence; direct path to significant data breach, system compromise, or compliance violation with material business impact. Requires immediate attention. |
| High | Exploitable under realistic conditions; significant security or compliance impact. Remediation required within 30 days. |
| Medium | Exploitable under specific conditions; moderate impact. Remediation required within 90 days. |
| Low | Difficult to exploit or limited impact if exploited. Address in standard security backlog. |
| Informational | Noted for completeness or future consideration. No material security impact. |

---

## Eval Results Template

```markdown
# Eval Results: [Date] — Prompt Version [vX.X.X]

## Summary

| Agent | Weighted Score | Pass/Fail | Previous Score | Delta |
|---|---|---|---|---|
| Security Architect | | | | |
| Validation Agent | | | | |
| Governance Agent | | | | |
| Coach Agent | | | | |

## Test Cases Run

- [ ] TC-001: Cloud-native web application (baseline)
- [ ] TC-002: GenAI/LLM application with agentic capabilities
- [ ] TC-003: Payment processing API (PCI DSS focus)
- [ ] TC-004: Healthcare data platform (HIPAA focus)
- [ ] TC-005: Identity and access management system

## Notable Changes from Prior Version

[Describe any dimensions where scores changed by >0.5 points]

## Prompt Changes Validated

[List the prompt changes this eval run validates]

## Recommended Actions

[Any dimensions below threshold; any regressions to investigate]
```

---

## Test Case Index

| ID | Scenario | Primary Framework | Expert Baseline Version |
|---|---|---|---|
| TC-001 | Cloud-native web application on AWS | STRIDE, NIST CSF 2.0 | v1.0 |
| TC-002 | GenAI agentic system with MCP | OWASP LLM Top 10, NIST AI RMF 1.0 | v1.0 |
| TC-003 | Payment processing API | STRIDE, PCI DSS v4.0 | v1.0 |
| TC-004 | Healthcare patient data platform | STRIDE, HIPAA, HITRUST | v1.0 |
| TC-005 | Enterprise IAM system | STRIDE, NIST SP 800-53, NIST CSF 2.0 | v1.0 |

Expert baseline outputs for each test case are in `evals/test_cases/[TC-ID]/expert_baseline.md`. These are write-protected and require maintainer approval to modify.
