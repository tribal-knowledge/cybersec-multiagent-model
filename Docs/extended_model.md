# Extended 6-Agent Enterprise Model

For enterprise-scale cybersecurity programs, the core 4-agent model expands to six specialized agents. This variant is appropriate for organizations with:
- Dedicated security functions for threat intelligence, red teaming, and risk management
- Complex multi-framework compliance environments (PCI DSS + HIPAA + SOC2 + HITRUST simultaneously)
- High-volume security assessment workloads (50+ assessments per quarter)
- Mature security programs where agent specialization reduces handoff errors

---

## Agent Roster

| Agent | Archetype | Primary Function |
|---|---|---|
| Security Architect | Writer | Design security controls, architecture reviews, security requirements |
| Threat Modeler | Analyst | STRIDE and PASTA analysis, trust boundary mapping, data flow threat enumeration |
| Red Team Analyst | Adversary | Attack simulation, exploit path development, adversarial test case generation |
| Compliance Reviewer | Reviewer | PCI DSS, HIPAA, SOC2, HITRUST, ISO 27001 validation |
| Risk Officer | Quantifier | Risk quantification (FAIR or RVSS), risk register management, risk appetite calibration |
| Security Program Manager (Coach) | Orchestrator | Workflow orchestration, executive decision support, stakeholder communication |

---

## Why Split the Core Agents?

### Security Architect → Security Architect + Threat Modeler

In the 4-agent model, the Security Architect handles both high-level architecture review and detailed threat modeling. For complex systems (multi-cloud GenAI platforms, hybrid OT/IT environments), these are genuinely distinct skills. Separating them:
- Allows the Threat Modeler to go deep on specific threat enumeration techniques (PASTA process stages, attack tree decomposition) without constraining the Architect's design work
- Reduces the Architect's context window burden on complex scenarios
- Enables parallel execution: Architect designs, Threat Modeler analyzes simultaneously

### Validation Agent → Red Team Analyst

The Validation Agent in the core model performs conceptual attack path analysis. The Red Team Analyst in the extended model goes further — it develops operationalized adversarial scenarios with specific TTPs, tooling, and test cases that can be handed directly to a penetration testing team or used to validate controls empirically. This is the difference between "MFA could be bypassed via SIM swapping" and a full attack chain with technique IDs, tool recommendations, and test pass/fail criteria.

### Governance Agent → Compliance Reviewer + Risk Officer

Compliance review (are we meeting the standard?) and risk management (what is our residual risk and does it fall within appetite?) require different reasoning. Separating them:
- Prevents the Governance Agent from conflating compliance status with risk posture (a common and dangerous error — you can be compliant and still carry unacceptable risk)
- Allows the Risk Officer to apply quantitative risk frameworks (FAIR, CVSS, RVSS) independently of compliance status
- Enables the Risk Officer to surface business risk language that resonates with non-technical executives

---

## Extended Workflow Architecture

```
Business Request
      |
      V
Security Program Manager (Coach)
      |
      ├──> Security Architect
      |         High-level architecture review
      |         Security control design
      |
      ├──> Threat Modeler
      |         STRIDE/PASTA analysis
      |         Trust boundary mapping
      |         Data flow threat enumeration
      |
      ├──> Red Team Analyst
      |         (receives Architect + Threat Modeler outputs)
      |         Operationalized attack scenarios
      |         TTP-mapped exploit paths
      |         Penetration test cases
      |
      ├──> Compliance Reviewer
      |         (receives Architect + Threat Modeler outputs)
      |         Framework compliance gap analysis
      |         Audit readiness assessment
      |
      └──> Risk Officer
                (receives all prior outputs)
                FAIR/RVSS risk quantification
                Residual risk vs. risk appetite
                Risk register update
      |
      V
Security Program Manager (Coach)
      |
      V
Executive Recommendation + Risk Decision Package
```

---

## Sequencing Recommendation

For the extended model, the following sequencing minimizes context gaps:

**Phase 1 (parallel):** Security Architect + Threat Modeler
**Phase 2 (sequential, reads Phase 1):** Red Team Analyst + Compliance Reviewer
**Phase 3 (reads all prior):** Risk Officer
**Phase 4 (reads all):** Security Program Manager synthesis

This sequencing allows the Red Team Analyst and Compliance Reviewer to work from the same complete design + threat picture, and gives the Risk Officer all technical and compliance inputs before quantification.

---

## When to Use Which Model

| Scenario | Recommended Model |
|---|---|
| Single-system security review | 4-agent core |
| New product security assessment | 4-agent core |
| Enterprise architecture review | 6-agent extended |
| Multi-framework compliance assessment | 6-agent extended |
| High-stakes M&A security due diligence | 6-agent extended |
| Ongoing security program management | 6-agent extended |
| AI/ML system security assessment | 4-agent core + Threat Modeler variant |
| OT/ICS security review | 4-agent core with domain-specific prompts |

---

## Implementation Notes

The 6-agent model requires approximately 2.5× the token budget of the 4-agent model per workflow run. For organizations cost-optimizing agent usage, consider:
- Using the 4-agent model for routine assessments
- Reserving the 6-agent model for high-criticality systems and compliance-heavy scenarios
- Running the Risk Officer only when quantitative risk output is required by stakeholders
