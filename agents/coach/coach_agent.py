"""
coach_agent.py — Security Lead (Coach) Agent Orchestrator
Cybersecurity Multi-Agent Learning Loop Model

Orchestrates the full multi-agent security assessment pipeline:
  Business Request → Coach Dispatch → [Architect | Validation | Governance] → Coach Synthesis → Executive Report

Usage:
    python coach_agent.py --scenario playbooks/example_mcp_review.md
    python coach_agent.py --request "Review our new payment API" --frameworks pci_dss hipaa
"""

import argparse
import json
import os
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Optional

# ---------------------------------------------------------------------------
# LLM Client (swap this shim for your provider SDK)
# ---------------------------------------------------------------------------
# Default: Anthropic Claude. Set LLM_PROVIDER=openai to use OpenAI.
# Both require an API key in LLM_API_KEY environment variable.

LLM_PROVIDER = os.environ.get("LLM_PROVIDER", "anthropic")
LLM_MODEL = os.environ.get("LLM_MODEL", "claude-opus-4-5")


def llm_call(system_prompt: str, user_message: str, max_tokens: int = 8192) -> str:
    """
    Thin wrapper around whichever LLM provider is configured.
    Replace this with your preferred SDK integration.
    """
    api_key = os.environ.get("LLM_API_KEY")
    if not api_key:
        raise EnvironmentError("LLM_API_KEY environment variable is not set.")

    if LLM_PROVIDER == "anthropic":
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=api_key)
            message = client.messages.create(
                model=LLM_MODEL,
                max_tokens=max_tokens,
                system=system_prompt,
                messages=[{"role": "user", "content": user_message}],
            )
            return message.content[0].text
        except ImportError:
            raise ImportError("anthropic SDK not installed. Run: pip install anthropic")

    elif LLM_PROVIDER == "openai":
        try:
            from openai import OpenAI
            client = OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model=LLM_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message},
                ],
                max_tokens=max_tokens,
            )
            return response.choices[0].message.content
        except ImportError:
            raise ImportError("openai SDK not installed. Run: pip install openai")

    else:
        raise ValueError(f"Unsupported LLM_PROVIDER: {LLM_PROVIDER}")


# ---------------------------------------------------------------------------
# Data Structures
# ---------------------------------------------------------------------------

@dataclass
class BusinessRequest:
    description: str
    asset_description: str
    scope_in: list[str] = field(default_factory=list)
    scope_out: list[str] = field(default_factory=list)
    compliance_frameworks: list[str] = field(default_factory=list)
    risk_appetite: str = "Standard"
    prior_findings: str = ""
    audience: str = "CISO"  # CISO | Board | Engineering | GRC


@dataclass
class AgentOutput:
    agent_name: str
    output: str
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    token_count: int = 0


@dataclass
class AssessmentRun:
    run_id: str
    request: BusinessRequest
    architect_output: Optional[AgentOutput] = None
    validation_output: Optional[AgentOutput] = None
    governance_output: Optional[AgentOutput] = None
    executive_report: Optional[str] = None
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())


# ---------------------------------------------------------------------------
# Prompt Loader
# ---------------------------------------------------------------------------

PROMPT_DIR = Path(__file__).parent.parent.parent / "prompts"


def load_system_prompt(agent_name: str) -> str:
    """
    Load versioned system prompt from prompts/ directory.
    Expects files named: {agent_name}_system_prompt.md
    Strips markdown code fences to extract the prompt text.
    """
    prompt_path = PROMPT_DIR / f"{agent_name}_system_prompt.md"
    if not prompt_path.exists():
        raise FileNotFoundError(f"System prompt not found: {prompt_path}")

    content = prompt_path.read_text(encoding="utf-8")

    # Extract content between ``` fences (the actual prompt)
    if "```" in content:
        parts = content.split("```")
        # Take the first fenced block after the header
        for i, part in enumerate(parts):
            if i % 2 == 1:  # Odd indices are inside fences
                return part.strip()

    return content.strip()


# ---------------------------------------------------------------------------
# Individual Agents
# ---------------------------------------------------------------------------

class SecurityArchitectAgent:
    def __init__(self):
        self.system_prompt = load_system_prompt("architect")

    def run(self, request: BusinessRequest) -> AgentOutput:
        print("\n[COACH] → Security Architect Agent: dispatching...")

        user_message = f"""
SECURITY ARCHITECTURE ASSESSMENT REQUEST

Business Request:
{request.description}

Asset Description:
{request.asset_description}

In-Scope Components:
{chr(10).join(f'- {s}' for s in request.scope_in) if request.scope_in else 'All components described above'}

Out-of-Scope:
{chr(10).join(f'- {s}' for s in request.scope_out) if request.scope_out else 'Nothing explicitly excluded'}

Prior Findings:
{request.prior_findings if request.prior_findings else 'None provided'}

Compliance Context (for your awareness — Governance Agent will assess):
{', '.join(request.compliance_frameworks) if request.compliance_frameworks else 'Not specified'}

Please produce a complete security architecture assessment following your output format specification.
"""
        output = llm_call(self.system_prompt, user_message)
        print("[COACH] ← Security Architect Agent: output received.")
        return AgentOutput(agent_name="Security Architect", output=output)


class ValidationAgent:
    def __init__(self):
        self.system_prompt = load_system_prompt("validation")

    def run(self, request: BusinessRequest, architect_output: AgentOutput) -> AgentOutput:
        print("\n[COACH] → Validation Agent: dispatching...")

        user_message = f"""
VALIDATION AND ADVERSARIAL ANALYSIS REQUEST

Original Business Request:
{request.description}

Asset Under Review:
{request.asset_description}

Security Architect's Assessment (challenge and validate this):
{architect_output.output}

Your Task:
1. Validate each control proposed by the Security Architect
2. Identify attack paths and bypass conditions
3. Map all findings to MITRE ATT&CK Enterprise v15
4. Identify threats the Architect missed
5. Develop top-3 adversarial test cases

Scope: {', '.join(request.scope_in) if request.scope_in else 'All in-scope components from Architect assessment'}
"""
        output = llm_call(self.system_prompt, user_message)
        print("[COACH] ← Validation Agent: output received.")
        return AgentOutput(agent_name="Validation Agent", output=output)


class GovernanceAgent:
    def __init__(self):
        self.system_prompt = load_system_prompt("governance")

    def run(
        self,
        request: BusinessRequest,
        architect_output: AgentOutput,
        validation_output: AgentOutput,
    ) -> AgentOutput:
        print("\n[COACH] → Governance Agent: dispatching...")

        frameworks_str = (
            "\n".join(f"- {f}" for f in request.compliance_frameworks)
            if request.compliance_frameworks
            else "- Not specified — apply NIST CSF 2.0 as default baseline"
        )

        user_message = f"""
COMPLIANCE AND GOVERNANCE REVIEW REQUEST

Original Business Request:
{request.description}

Asset Under Review:
{request.asset_description}

Applicable Compliance Frameworks:
{frameworks_str}

Organizational Risk Appetite: {request.risk_appetite}

Security Architect's Assessment:
{architect_output.output}

Validation Agent's Findings:
{validation_output.output}

Your Task:
1. Assess compliance posture against each applicable framework
2. Map Validation Agent findings to compliance implications
3. Assess audit readiness per control domain
4. Identify inter-framework conflicts
5. Flag items requiring legal or regulatory affairs determination
"""
        output = llm_call(self.system_prompt, user_message)
        print("[COACH] ← Governance Agent: output received.")
        return AgentOutput(agent_name="Governance Agent", output=output)


# ---------------------------------------------------------------------------
# Coach Orchestrator
# ---------------------------------------------------------------------------

class CoachAgent:
    def __init__(self):
        self.system_prompt = load_system_prompt("coach")
        self.architect = SecurityArchitectAgent()
        self.validation = ValidationAgent()
        self.governance = GovernanceAgent()

    def run(self, request: BusinessRequest, mode: str = "sequential") -> AssessmentRun:
        """
        Execute the full multi-agent workflow.

        Args:
            request: The structured business request
            mode: 'sequential' (default) or 'parallel'
                  Sequential: each agent reads prior agent's output
                  Parallel: all agents run independently (faster, less rich)
        """
        run_id = f"run_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        print(f"\n{'='*60}")
        print(f"ASSESSMENT RUN: {run_id}")
        print(f"Mode: {mode.upper()}")
        print(f"{'='*60}")

        assessment = AssessmentRun(run_id=run_id, request=request)

        if mode == "sequential":
            # Phase 1: Architecture
            assessment.architect_output = self.architect.run(request)

            # Phase 2: Validation (reads Architect output)
            assessment.validation_output = self.validation.run(
                request, assessment.architect_output
            )

            # Phase 3: Governance (reads both prior outputs)
            assessment.governance_output = self.governance.run(
                request,
                assessment.architect_output,
                assessment.validation_output,
            )

        elif mode == "parallel":
            # All three agents run independently
            # Note: In production, use asyncio or ThreadPoolExecutor for true parallelism
            assessment.architect_output = self.architect.run(request)

            # For parallel mode, Validation and Governance run with only the original request
            # (not each other's outputs) — Coach bears more synthesis burden
            from agents.validation.validation_agent import ValidationAgent as VA
            from agents.governance.governance_agent import GovernanceAgent as GA
            vp = VA()
            gp = GA()
            # Create a minimal architect output stub for parallel mode
            stub = AgentOutput(agent_name="Security Architect", output="[Parallel mode: agents running independently]")
            assessment.validation_output = vp.run(request, stub)
            assessment.governance_output = gp.run(request, stub, stub)
        else:
            raise ValueError(f"Unknown mode: {mode}. Use 'sequential' or 'parallel'.")

        # Phase 4: Coach synthesis
        print("\n[COACH] Synthesizing all agent outputs...")
        assessment.executive_report = self._synthesize(request, assessment)
        print("[COACH] Executive report produced.")

        return assessment

    def _synthesize(self, request: BusinessRequest, assessment: AssessmentRun) -> str:
        synthesis_prompt = f"""
SYNTHESIS REQUEST — PRODUCE EXECUTIVE RECOMMENDATION PACKAGE

Business Request:
{request.description}

Target Audience: {request.audience}

--- SECURITY ARCHITECT OUTPUT ---
{assessment.architect_output.output}

--- VALIDATION AGENT OUTPUT ---
{assessment.validation_output.output}

--- GOVERNANCE AGENT OUTPUT ---
{assessment.governance_output.output}

Instructions:
1. Deduplicate findings across all three agents
2. Apply conflict resolution protocol per your system prompt
3. Prioritize all findings using the Priority Score formula
4. Produce the full Executive Recommendation Package calibrated to the {request.audience} audience
5. Document all conflicts in the Conflict Log section
6. Flag any findings that require human expert escalation
"""
        return llm_call(self.system_prompt, synthesis_prompt, max_tokens=8192)


# ---------------------------------------------------------------------------
# Output Persistence
# ---------------------------------------------------------------------------

def save_assessment(assessment: AssessmentRun, output_dir: Path = Path("run_artifacts")) -> Path:
    """Save the full assessment run to disk for human review and feedback capture."""
    output_dir.mkdir(exist_ok=True)
    run_dir = output_dir / assessment.run_id
    run_dir.mkdir(exist_ok=True)

    # Save metadata
    metadata = {
        "run_id": assessment.run_id,
        "timestamp": assessment.timestamp,
        "request": asdict(assessment.request),
    }
    (run_dir / "metadata.json").write_text(json.dumps(metadata, indent=2))

    # Save individual agent outputs
    if assessment.architect_output:
        (run_dir / "01_architect_output.md").write_text(assessment.architect_output.output)
    if assessment.validation_output:
        (run_dir / "02_validation_output.md").write_text(assessment.validation_output.output)
    if assessment.governance_output:
        (run_dir / "03_governance_output.md").write_text(assessment.governance_output.output)

    # Save executive report
    if assessment.executive_report:
        (run_dir / "04_executive_report.md").write_text(assessment.executive_report)

    print(f"\n[COACH] Assessment saved to: {run_dir}")
    return run_dir


# ---------------------------------------------------------------------------
# CLI Entry Point
# ---------------------------------------------------------------------------

def load_scenario(scenario_path: str) -> BusinessRequest:
    """
    Load a scenario from a playbook markdown file.
    Expects YAML front matter with request fields, or parses the
    'Business Request' section as the description.
    """
    content = Path(scenario_path).read_text(encoding="utf-8")

    # Simple extraction — for production use a proper YAML front matter parser
    description = ""
    asset = ""
    frameworks = []

    lines = content.split("\n")
    for i, line in enumerate(lines):
        if "## Business Request" in line and i + 1 < len(lines):
            description = lines[i + 1].strip()
        if "## Asset Description" in line and i + 1 < len(lines):
            asset = lines[i + 1].strip()
        if "**Frameworks:**" in line:
            frameworks_str = line.split("**Frameworks:**")[1].strip()
            frameworks = [f.strip() for f in frameworks_str.split(",")]

    return BusinessRequest(
        description=description or content[:500],
        asset_description=asset or "See scenario file for full asset description.",
        compliance_frameworks=frameworks,
    )


def main():
    parser = argparse.ArgumentParser(
        description="Cybersecurity Multi-Agent Learning Loop Model — Coach Orchestrator"
    )
    parser.add_argument("--scenario", help="Path to a playbook scenario file (.md)")
    parser.add_argument("--request", help="Business request description (inline)")
    parser.add_argument("--asset", help="Asset description (inline)", default="")
    parser.add_argument(
        "--frameworks",
        nargs="+",
        default=[],
        help="Compliance frameworks to assess (e.g., pci_dss hipaa nist_csf)",
    )
    parser.add_argument(
        "--mode",
        choices=["sequential", "parallel"],
        default="sequential",
        help="Agent execution mode (default: sequential)",
    )
    parser.add_argument(
        "--audience",
        choices=["CISO", "Board", "Engineering", "GRC"],
        default="CISO",
        help="Target audience for executive report (default: CISO)",
    )
    parser.add_argument(
        "--output-dir",
        default="run_artifacts",
        help="Directory to save assessment outputs (default: run_artifacts/)",
    )

    args = parser.parse_args()

    if args.scenario:
        request = load_scenario(args.scenario)
        request.audience = args.audience
    elif args.request:
        request = BusinessRequest(
            description=args.request,
            asset_description=args.asset,
            compliance_frameworks=args.frameworks,
            audience=args.audience,
        )
    else:
        parser.error("Provide either --scenario or --request")

    coach = CoachAgent()
    assessment = coach.run(request, mode=args.mode)
    output_path = save_assessment(assessment, Path(args.output_dir))

    print(f"\n{'='*60}")
    print("ASSESSMENT COMPLETE")
    print(f"Executive report: {output_path / '04_executive_report.md'}")
    print(f"{'='*60}\n")

    # Print executive report to stdout
    if assessment.executive_report:
        print(assessment.executive_report)


if __name__ == "__main__":
    main()
