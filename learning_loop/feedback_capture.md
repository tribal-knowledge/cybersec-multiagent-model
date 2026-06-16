# Learning Loop: Feedback Capture

## Purpose

This is the mechanism that separates a static automation from a compounding asset. Every time a human security expert reviews agent output and makes a correction, that correction is potential organizational intelligence. This document defines the schema and process for capturing that intelligence.

---

## The Learning Loop Cycle

```
Agent produces output
        |
        V
Human expert reviews output
        |
        ├── Output is correct ──────────────> Archive (no feedback record needed)
        |
        ├── Output has correctable error ───> Feedback record (see schema below)
        |                                           |
        └── Output missed something critical ─> Feedback record (type: missed_finding)
                                                    |
                                                    V
                                        Monthly review by maintainers
                                                    |
                                                    ├── Promote to playbook update
                                                    └── Promote to prompt refinement PR
```

---

## Feedback Record Schema

Create one YAML file per feedback record in `learning_loop/feedback_records/`. Filename format: `[YYYY-MM-DD]_[agent-name]_[short-slug].yaml`

```yaml
# Feedback Record Schema v1.0

# Identification
feedback_id: "FB-[YYYY-MM-DD]-[###]"   # Assign sequential within date
date: "YYYY-MM-DD"
submitted_by: "Initials or GitHub handle"
scenario_id: "TC-001"                   # Reference to test case if applicable, or playbook filename

# Agent that produced the output being corrected
agent: architect | validation | governance | coach

# The agent's output being corrected (quote the relevant excerpt, not the full output)
original_output: |
  [Paste the specific section of agent output that was incorrect or incomplete]

# The correction or addition the human expert made
expert_correction: |
  [What the correct output should have said, or what was missing]

# Classification of the correction type
correction_type:
  - false_positive          # Agent flagged something that isn't actually a finding
  - missed_finding          # Agent failed to identify a real finding
  - wrong_framework         # Agent cited incorrect framework or control ID
  - wrong_severity          # Agent assigned incorrect severity rating
  - scope_error             # Agent assessed something outside defined scope
  - synthesis_error         # Coach agent incorrectly resolved a conflict or merged findings
  - output_format_error     # Agent produced output in wrong format or structure

# Impact of this correction
severity_of_miss: critical | high | medium | low | informational
# Use the same severity scale as the agents (see evals/eval_framework.md)

# Resolution and disposition
resolution: |
  [Brief description of how the output should have been different]

# Has this correction pattern appeared in prior feedback records?
recurring_pattern: true | false
related_feedback_ids:
  - "FB-YYYY-MM-DD-###"    # List related records if recurring

# Playbook and prompt impact
promoted_to_playbook: true | false
playbook_file: ""            # Filename if promoted

prompt_refinement_candidate: true | false
prompt_change_description: |
  [If this feedback suggests a prompt change, describe the change and rationale]

# Business context (optional — redact sensitive details)
asset_type: ""               # e.g., "cloud-native web app", "GenAI system"
domain: ""                   # e.g., "Healthcare", "Financial Services", "Technology"
frameworks_in_scope: []      # e.g., ["PCI DSS v4.0", "NIST CSF 2.0"]
```

---

## Example Feedback Record

```yaml
feedback_id: "FB-2026-06-15-001"
date: "2026-06-15"
submitted_by: "KM"
scenario_id: "example_mcp_review"

agent: validation

original_output: |
  Control Bypass: Command allowlist (bash MCP server)
  Status: Effective
  Notes: The allowlist prevents execution of unapproved commands.

expert_correction: |
  Rating should be "Partial - Effective" not "Effective".
  Python3 being on the allowlist creates a secondary execution path.
  Any allowlisted interpreter (python3, node, ruby) that can itself exec
  arbitrary code means the allowlist is a deterrent, not a hard control.
  The agent should default to identifying interpreter-class bypasses for
  any language runtime on the allowlist.

correction_type:
  - missed_finding
  - wrong_severity

severity_of_miss: high

resolution: |
  Validation Agent should apply a sub-check: for each allowlisted command,
  if that command is a language interpreter or can itself spawn child processes
  (python3, node, bash, sh, ruby, perl, java, etc.), flag as "Partial" and
  note the secondary execution risk.

recurring_pattern: false
related_feedback_ids: []

promoted_to_playbook: true
playbook_file: "example_mcp_review.md"

prompt_refinement_candidate: true
prompt_change_description: |
  Add to Validation Agent system prompt under "Methodology":
  "For each command on a bash/shell allowlist, check whether the command
  is a language interpreter or process spawner (python, node, ruby, perl,
  bash, sh, java, etc.). If so, note that the allowlist provides deterrence
  but not hard prevention, and rate the control as 'Partial' with a bypass
  description referencing the interpreter's exec/subprocess capabilities."

asset_type: "GenAI Agentic System (MCP-based)"
domain: "Technology"
frameworks_in_scope: ["NIST AI RMF 1.0", "OWASP LLM Top 10", "NIST CSF 2.0"]
```

---

## Submission Process

1. Create your feedback record YAML file in `learning_loop/feedback_records/`
2. Open a GitHub Issue using the **Feedback Record** issue template
3. Reference the feedback record filename in the issue
4. Add labels: the relevant `agent:*` label and `type:feedback`

Maintainers review all feedback records monthly. Records marked `prompt_refinement_candidate: true` are batched into prompt improvement PRs. Records marked `promoted_to_playbook: true` are incorporated into the relevant playbook or used to create a new one.

---

## What Makes a Good Feedback Record

**Be specific about the correction.** "The agent was wrong about PCI" is not useful. "The agent cited PCI DSS v3.2.1 Requirement 8.2 but the correct citation is PCI DSS v4.0 Requirement 8.3.6, which materially changed the MFA requirement" is actionable.

**Include the correct output.** Don't just say what was wrong — say what right looks like. This is what gets turned into a prompt improvement.

**Flag recurring patterns.** If you've seen the same mistake three times, that's a systematic prompt issue, not a one-off. Flag it.

**Separate what the agent got wrong from what it missed.** These drive different prompt changes. A false positive suggests the agent is over-reaching; a missed finding suggests a coverage gap.
