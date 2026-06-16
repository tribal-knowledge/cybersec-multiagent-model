"""
validation_agent.py — Validation Agent (Adversarial Tester)
Cybersecurity Multi-Agent Learning Loop Model

Standalone runner for the Validation agent.
Can be used independently or imported by coach_agent.py.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from agents.coach.coach_agent import (
    BusinessRequest,
    AgentOutput,
    ValidationAgent,
)


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Validation Agent — Standalone Runner")
    parser.add_argument("--request", required=True, help="Business request description")
    parser.add_argument("--asset", required=True, help="Asset description")
    parser.add_argument(
        "--architect-output",
        required=True,
        help="Path to Security Architect output file (.md)",
    )
    args = parser.parse_args()

    request = BusinessRequest(
        description=args.request,
        asset_description=args.asset,
    )

    architect_content = Path(args.architect_output).read_text(encoding="utf-8")
    architect_output = AgentOutput(
        agent_name="Security Architect",
        output=architect_content,
    )

    agent = ValidationAgent()
    output = agent.run(request, architect_output)

    print("\n" + "=" * 60)
    print("VALIDATION AGENT OUTPUT")
    print("=" * 60)
    print(output.output)


if __name__ == "__main__":
    main()
