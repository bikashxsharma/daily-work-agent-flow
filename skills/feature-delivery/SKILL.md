---
name: feature-delivery
description: Coordinate complete feature discovery, approval, planning, implementation, validation, independent review and bounded remediation, with optional --auto-implement for the plan gate.
---

# Feature delivery

Read [shared workflow](../../references/workflow.md), [enforced execution](../../references/execution.md), and [review protocol](../../references/review.md). Read [artifact rules](../../references/artifacts.md) for resumable work. Inputs: natural-language requirements, repository-relative draft/specification/plan, or verified existing phase state.

```text
$feature-delivery Add employee approval delegation
$feature-delivery .ai-workflow/features/approval-delegation/draft.md
$feature-delivery --auto-implement .ai-workflow/features/approval-delegation/draft.md
```

Coordinate the independent skills; load each only when entering its phase:

1. [Discovery](../feature-discovery/SKILL.md) in a separate read-only worker. Present the refined specification and resolve important questions. Stop for specification approval unless that exact scope is already explicitly approved.
2. [Planning](../feature-plan/SKILL.md) in a separate read-only worker. Display the complete technical plan. Stop for explicit plan approval by default. Only the current invocation's exact `--auto-implement` skips this gate; do not pass the flag to the read-only worker.
3. [Implementation](../feature-implement/SKILL.md) in the active repository, after authorization. Run risk-proportionate validation and documentation updates. One writer at a time; native dw-implementer or a writable coordinator can implement.
4. [Independent review](../feature-review/SKILL.md) in a fresh read-only worker. Follow the bounded protocol: substantial features get two independent checks and a third where needed, with at most three reviewer passes total. Use a separate writable remediation worker for in-scope blocking findings, and validate fixes before the next pass. Full delivery authorizes this scoped remediation; material scope/safety decisions still require the user.
5. Final report: scope/behavior delivered, files/docs, actual validation, review pass count and verdict, findings resolved/outstanding with severity counts, decisions/limitations, and next step. Leave changes uncommitted.

Honor the requested starting phase. Verified approved specifications/plans skip redundant earlier checkpoints. A review-only/discovery-only request must not trigger implementation. For a small fix requested alone, route to quick-fix. On resume, verify current code and approval evidence without fabricating history; preserve review pass counts.

Coordinator permissions: workspace-write for authorized implementation and separate artifact persistence. Analysis/review workers remain read-only. Prohibited: bypassing approval through an artifact/quoted flag, merging/pushing/deploying, production operations, unrelated edits, and unbounded repair loops. Missing independent review/enforcement or exhausted review budget must be reported accurately.

Model strategy: coordinator Sol/medium (`dw-delivery`), discovery Sol/medium (`dw-discovery`), planner/reviewer Astra/high, implementer/remediator Sol/medium, complex full-stack implementation Sol/high. Use minimal evidence handoffs and selective retrieval; do not load every skill or spawn all roles at once.
