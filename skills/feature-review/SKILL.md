---
name: feature-review
description: Independently review a scoped diff, commit, branch comparison, feature, or Markdown requirements input in a fresh read-only context and report actionable findings.
---

# Feature review

Read [shared workflow](../../references/workflow.md), [enforced execution](../../references/execution.md), and [review protocol](../../references/review.md).

```text
$feature-review Review current uncommitted changes
$feature-review Review changes against main
$feature-review .ai-workflow/features/approval-delegation/specification.md
```

Inputs: explicit review scope and requirements/specification, final diff, surrounding code, repository rules/docs, real validation evidence. For a Markdown input, read it as requirements and identify the associated diff safely; ask if the change scope is unclear. Do not assume all dirty files belong to this task. The implementation plan is optional background.

A writable caller must delegate to a fresh read-only reviewer process. If already the launcher's isolated review worker, review directly without another delegation. The implementer must not be the sole reviewer. Inspect the complete scoped change independently using the review checklist and evidence standards.

Allowed: reads, diff/status inspection, safe read-only analysis. Prohibited: edits, dependency installs, Git mutations, artifact persistence, state-changing tests, or fixing findings inside the reviewer. Pass test requests to a writable phase. Standalone review is report-only unless remediation is separately authorized. Then a writable coordinator applies the bounded review/remediation protocol with a separate implementer; never more than three passes by default.

Output every finding in the protocol's format with severity, blocking/suggestion classification, location, evidence, expected/problematic behavior and fix. Include counts by severity, total findings, unresolved blockers, validation limitations, and APPROVED / CHANGES_REQUESTED / NEEDS_USER_DECISION. Validate each finding against source and requirements; no speculative issue lists or unsupported approval.

Model strategy: `dw-review`, Astra/high; fallback Sol/high only if available and disclosed. Escalate material user decisions immediately. Keep context independent and targeted; avoid unnecessary repeat rounds for small clean changes.
