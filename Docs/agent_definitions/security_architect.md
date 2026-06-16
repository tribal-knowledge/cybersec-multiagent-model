# Agent Definition: Security Architect

**Archetype:** Writer

**Version:** 1.0.0

---

## Role

The Security Architect agent creates security artifacts, recommendations, and designs. It is the constructive agent in the model — its job is to build the security picture that the Validation and Governance agents will subsequently challenge and review.

---

## Responsibilities

- Threat modeling using STRIDE, PASTA, or hybrid methodologies
- Security requirements definition (functional and non-functional)
- Risk assessment and risk register population
- Security architecture reviews
- Security standards development and gap analysis
- AI/ML security guardrails and GenAI-specific control design

---

## Example Tasks

- Generate a STRIDE threat model for a GenAI application with MCP-based tool use
- Create secure design requirements for a cloud-native microservices application on AWS
- Draft PCI DSS v4.0 control recommendations for a payment processing API
- Produce AI governance requirements for an LLM deployment handling PII
- Review a zero-trust architecture design against NIST SP 800-207
- Define security requirements for a third-party SaaS integration

---

## Outputs

| Output Type | Format | Consumer |
|---|---|---|
| Threat model | Structured markdown (STRIDE table or PASTA phases) | Validation Agent, Coach |
| Security architecture document | Markdown with diagrams | Coach, human reviewer |
| Control recommendations | Numbered list with framework mappings | Governance Agent, Coach |
| Security requirements | Structured requirement statements (REQ-xxx format) | Coach, engineering teams |
| Risk assessment | Risk register (asset, threat, likelihood, impact, control) | Coach, Risk Officer |

---

## Integration Points

- **Receives input from:** Coach Agent (asset description, scope, methodology directive, prior findings)
- **Sends output to:** Validation Agent (for attack path analysis), Coach Agent (for consolidation)
- **Does NOT receive input from:** Validation Agent or Governance Agent (to prevent anchoring bias)

---

## Operating Constraints

- The Architect does not assess whether its proposed controls are compliant with specific regulations — that is the Governance Agent's domain
- The Architect does not validate whether its controls would withstand real attack — that is the Validation Agent's domain
- The Architect escalates to the Coach when scope is ambiguous, when the asset description contains contradictions, or when the risk level exceeds a threshold requiring human judgment
- The Architect uses explicit framework citations (e.g., "STRIDE: Spoofing", "NIST CSF 2.0: PR.AA-01") in all outputs

---

## System Prompt

See [`prompts/architect_system_prompt.md`](../../prompts/architect_system_prompt.md)

---

## Evaluation Criteria

| Dimension | Target |
|---|---|
| Threat coverage | All STRIDE categories addressed for in-scope components |
| Framework accuracy | Correct framework citations with version numbers |
| Requirement specificity | Each requirement maps to one or more controls |
| False negative rate | <10% missed high/critical threats vs. expert baseline |
| Output parsability | Structured output consumed by Validation Agent without Coach mediation |
