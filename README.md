# Cybersecurity Multi-Agent Learning Loop Model

> **An AI-native security operating model that converts organizational expertise into compounding intellectual property.**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

---

## What This Is

This is not a security automation tool. It is an **operating model**.

The Cybersecurity Multi-Agent Learning Loop Model deploys specialized AI agents that mirror how mature security organizations are staffed — each agent owning a discrete domain of expertise, coordinated by an orchestrating Security Lead. The design objective is to create a continuous feedback loop that converts human expert judgment into reusable, organization-owned security intelligence.

The key concept: your experts remain in the loop. Their corrections, decisions, and refinements are systematically captured and fed back into the model. Over time, the system gets faster, more accurate, and increasingly specific to your organization's threat landscape.

---

## The Agent Roster

| Agent | Archetype | Primary Function |
|---|---|---|
| Security Architect | Writer | Threat modeling, security requirements, architecture reviews |
| Validation Agent | Tester | Attack path analysis, MITRE ATT&CK mapping, gap identification |
| Governance Agent | Reviewer | Compliance validation (PCI DSS, HIPAA, NIST CSF 2.0, SOC2) |
| Security Lead (Coach) | Orchestrator | Workflow coordination, conflict resolution, executive synthesis |

---

## Workflow Architecture

```
Business Request
      |
      V
 Coach Agent  ─────────────────────────────────────────┐
      |                                                 |
      ├──> Security Architect Agent                     |
      |         Creates threat model                    |
      |         Defines security requirements           |
      |                                                 |
      ├──> Validation Agent                             |
      |         Identifies attack paths                 |
      |         Maps to MITRE ATT&CK                    |
      |                                                 |
      └──> Governance Agent                             |
                Validates compliance posture            |
                Assesses regulatory exposure            |
                                                        |
      ┌─────────────────────────────────────────────────┘
      |
      V
 Coach Agent
      |
      V
 Executive Recommendation
      |
      V
 Human Expert Review ──> Feedback Capture ──> Playbook Update ──> Agent Improvement
```

---

## The Learning Loop

The agents are the mechanism. The learning loop is the value.

After every workflow run:
1. Human security experts review agent outputs
2. Corrections and decisions are captured in structured feedback records
3. Successful patterns are promoted to reusable playbooks
4. Playbooks and corrections are used to refine agent system prompts
5. Institutional cybersecurity knowledge accumulates as owned organizational IP
6. Future assessments run faster and with higher accuracy

This is what separates a point-in-time automation from a compounding asset.

---

## Human Capital and Token Capital

**Human Capital** — the expertise your practitioners carry: threat intuition, regulatory knowledge, business context, pattern recognition built over years.

**Token Capital** — the AI capability your organization owns: threat modeling agents, risk assessment workflows, security knowledge bases, compliance automation, evaluation frameworks, and security copilots.

The strategic objective is to convert human capital into token capital systematically. The organizations that build the strongest learning loop — not necessarily those with access to the most powerful foundation model — will compound the fastest.

---

## Quick Start

### Prerequisites
- Python 3.10+
- API access to an LLM provider (Anthropic Claude, OpenAI, or equivalent)
- Set `LLM_API_KEY` in your environment

### Run a Sample Workflow

```bash
git clone https://github.com/YOUR_USERNAME/cybersec-multiagent-model.git
cd cybersec-multiagent-model
pip install -r requirements.txt
python agents/coach/coach_agent.py --scenario playbooks/example_mcp_review.md
```

See `playbooks/example_mcp_review.md` for a fully worked example: reviewing an MCP-based AI coding assistant from business request through to executive recommendation.

---

## Extended 6-Agent Enterprise Model

For organizations running mature security programs at scale, the model expands to six specialized agents. See [`docs/extended_model.md`](docs/extended_model.md).

---

## Repository Structure

```
cybersec-multiagent-model/
├── docs/
│   ├── architecture.md              # Detailed workflow and interaction model
│   ├── agent_definitions/           # Per-agent specification files
│   └── extended_model.md            # 6-agent enterprise variant
├── agents/                          # Orchestration code
│   ├── coach/
│   ├── architect/
│   ├── validation/
│   └── governance/
├── prompts/                         # Versioned system prompts for each agent
├── playbooks/                       # Worked real-world scenario examples
├── evals/                           # Agent output evaluation framework
├── learning_loop/                   # Feedback capture schema and tooling
└── .github/                         # Issue templates, PR templates, workflows
```

---

## Contributing

Security practitioners are encouraged to contribute:
- New playbooks from real-world scenarios you've run
- Prompt refinements based on observed agent failures
- Eval results from running the framework against known cases
- New agent variants for specialized domains

See [CONTRIBUTING.md](CONTRIBUTING.md) for the full contribution guide.

---

## License

MIT — see [LICENSE](LICENSE)
