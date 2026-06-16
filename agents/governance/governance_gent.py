"""
governance_agent.py — Governance Agent (Compliance Reviewer)
Cybersecurity Multi-Agent Learning Loop Model

Standalone runner for the Governance agent.
Can be used independently or imported by coach_agent.py.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from agents.coach.coach_agent import (
    BusinessRequest,
    AgentOutput,
    GovernanceAgent,
)


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Governance Agent — Standalone Runner")
    parser.add_argument("--request", required=True, help="Business request description")
    parser.add_argument("--asset", required=True, help="Asset description")
    parser.add_argument(
        "--architect-output",
        required=True,
        help="Path to Security Architect output file (.md)",
    )
    parser.add_argument(
        "--validation-output",
        required=True,
        help="Path to Validation Agent output file (.md)",
    )
    parser.add_argument(
        "--frameworks",
        nargs="+",
        default=["NIST CSF 2.0"],
        help="Compliance frameworks to assess",
    )
    args = parser.parse_args()

    request = BusinessRequest(
        description=args.request,
        asset_description=args.asset,
        compliance_frameworks=args.frameworks,
    )

    architect_output = AgentOutput(
        agent_name="Security Architect",
        output=Path(args.architect_output).read_text(encoding="utf-8"),
    )
    validation_output = AgentOutput(
        agent_name="Validation Agent",
        output=Path(args.validation_output).read_text(encoding="utf-8"),
    )

    agent = GovernanceAgent()
    output = agent.run(request, architect_output, validation_output)

    print("\n" + "=" * 60)
    print("GOVERNANCE AGENT OUTPUT")
    print("=" * 60)
    print(output.output)


if __name__ == "__main__":
    main()
