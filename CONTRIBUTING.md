# Contributing to the Cybersecurity Multi-Agent Learning Loop Model

Thank you for contributing. This project improves through the feedback of practitioners who run the model against real security scenarios. Every playbook, prompt refinement, and eval result makes the system sharper for everyone.

---

## What We're Looking For

### Playbooks
The highest-value contributions are worked examples from real security assessments. A good playbook documents:
- The business request that triggered the workflow
- What each agent produced (you can redact sensitive client details)
- Where the agents were correct, and where human experts had to correct them
- The final executive recommendation

Playbooks are how organizational knowledge becomes reusable IP. See `playbooks/example_mcp_review.md` for the expected format.

### Prompt Improvements
If you observe consistent agent failures — a threat category the Architect misses, a compliance framework the Governance Agent miscites, a conflict pattern the Coach resolves incorrectly — open a PR against the relevant file in `prompts/` with the improved prompt and a description of the failure mode it addresses.

Include in the PR description:
- The failure mode observed (one sentence)
- The scenario type where it appears (e.g., "cloud-native GenAI applications")
- The prompt change and its rationale
- Before/after output examples if available

### Eval Results
Run the evaluation framework in `evals/eval_framework.md` against the existing test cases and submit your scores. Variance across practitioners helps calibrate the scoring rubric.

### New Agent Variants
The core model defines four agents. For specialized domains (e.g., OT/ICS security, healthcare-specific compliance, AI red teaming), new agent variants with domain-specific system prompts are welcome.

---

## Contribution Process

1. **Fork** the repository
2. **Create a branch** named descriptively: `playbook/cloud-sso-review`, `prompt/governance-hipaa-fix`, `eval/baseline-v2`
3. **Follow the schema** for the file type you're contributing (see below)
4. **Open a PR** using the provided pull request template
5. **One reviewer** from the maintainer team will respond within 5 business days

---

## File Schemas

### Playbook Schema (`playbooks/`)

```markdown
# Playbook: [Scenario Name]

## Scenario
**Domain:** [Cloud | GenAI | Network | Application | OT/ICS | Identity]
**Frameworks:** [List applicable: STRIDE, MITRE ATT&CK, PCI DSS, etc.]
**Date:** YYYY-MM
**Agent Version:** [Prompt version tag, e.g., v1.2.0]

## Business Request
[Verbatim or paraphrased input that triggered the workflow]

## Coach Dispatch
[What context and scoping the Coach sent to each agent]

## Security Architect Output
[Threat model, security requirements, or architecture review produced]

## Validation Agent Output
[Attack paths, MITRE ATT&CK mappings, gaps identified]

## Governance Agent Output
[Compliance assessment, regulatory gaps, audit findings]

## Human Expert Corrections
[What the reviewing practitioner changed and why]

## Final Executive Recommendation
[Coach-synthesized output]

## Key Learnings
[What this scenario revealed about agent behavior or model gaps]
```

### Feedback Record Schema (`learning_loop/`)

See `learning_loop/feedback_capture.md` for the YAML schema. Bulk feedback submissions (5+ records) can be submitted as a single PR against `learning_loop/feedback_records/`.

---

## Code of Conduct

- Critique outputs, not contributors
- Redact client-identifying information from playbooks before submitting
- Do not submit playbooks containing real vulnerability details for unpatched systems
- Maintain the framework's design principle: humans remain in the loop

---

## Questions?

Open a GitHub Discussion. Tag it `question` and include the relevant agent or component.
