---
name: feature-discovery
description: Explore a feature request or Markdown draft against repository evidence and produce a functional specification for approval, without implementation planning or code changes.
---

# Feature discovery

Read [shared workflow](../../references/workflow.md), then [enforced execution](../../references/execution.md). Purpose: align requirements before detailed planning. Inputs are conversational requirements or a repository-relative Markdown file.

Examples inside Codex:

```text
$feature-discovery Add employee approval delegation
$feature-discovery .ai-workflow/features/approval-delegation/draft.md
$feature-discovery --verbose Add employee approval delegation
```

Run in an enforced read-only discovery worker. Read the draft, applicable rules and routed documents, then inspect current behavior and affected modules. Explain relevant existing functionality and architectural constraints. Identify missing requirements, contradictions, meaningful business/security/data questions, and preliminary acceptance criteria. Make modest assumptions explicit; do not invent product rules.

Allowed: targeted reads/searches and non-mutating analysis. Prohibited: code/config/draft/artifact edits, dependency installs, Git mutations, state-changing validation, or a full file-by-file technical plan. A separate authorized writer can persist the final specification per [artifacts](../../references/artifacts.md).

Output: current-state summary; refined requirements; in/out of scope; acceptance criteria; open questions; risks; assumptions; proposed next step. Cite relevant repository evidence. Validate that each proposed requirement is sourced or marked for decision. Stop for specification approval. Important unanswered requirements block detailed planning. Follow the shared reporting rules: concise by default; with `--verbose`, include relevant documents/code areas, findings, assumptions, risks, and open questions without raw reasoning or tool logs.

Model strategy: `dw-discovery`, Sol/medium. Detailed technical planning and independent review use Astra/high in their separate phases. Escalate unresolved consequential decisions to the user. Retrieve only relevant documentation/code and avoid subagent fan-out. A clear task needs few questions.
