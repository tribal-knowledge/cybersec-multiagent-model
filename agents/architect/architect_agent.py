"""
architect_agent.py — Security Architect Agent
Cybersecurity Multi-Agent Learning Loop Model

Standalone runner for the Security Architect agent.
Can be used independently or imported by coach_agent.py.
"""

import os
import sys
from pathlib import Path

# Add project root to path for shared imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from agents.coach.coach_agent import (
    BusinessRequest,
    AgentOutput,
    SecurityArchitectAgent,
    save_assessment,
    AssessmentRun,
)


def main():
    """
    Standalone runner: invokes only the Security Architect agent.
    Useful for testing prompt changes or running architecture-only assessments.
    """
    import argparse

    parser = argparse.ArgumentParser(description="Security Architect Agent — Standalone Runner")
    parser.add_argument("--request", required=True, help="Business request description")
    parser.add_argument("--asset", required=True, help="Asset description")
    parser.add_argument("--scope-in", nargs="+", default=[], help="In-scope components")
    parser.add_argument("--scope-out", nargs="+", default=[], help="Out-of-scope components")
    args = parser.parse_args()

    request = BusinessRequest(
        description=args.request,
        asset_description=args.asset,
        scope_in=args.scope_in,
        scope_out=args.scope_out,
    )

    agent = SecurityArchitectAgent()
    output = agent.run(request)

    print("\n" + "=" * 60)
    print("SECURITY ARCHITECT OUTPUT")
    print("=" * 60)
    print(output.output)


if __name__ == "__main__":
    main()
