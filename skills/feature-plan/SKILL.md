---
name: feature-plan
description: Produce an executable technical plan from requirements or a Markdown specification; stop for approval unless the current invocation explicitly includes --auto-implement.
---

# Feature plan

Read [shared workflow](../../references/workflow.md) and [enforced execution](../../references/execution.md). Inputs: approved specification, supplied task, or repository-relative Markdown path.

```text
$feature-plan Add employee approval delegation
$feature-plan .ai-workflow/features/approval-delegation/specification.md
$feature-plan --auto-implement .ai-workflow/features/approval-delegation/specification.md
```

Planning itself runs in a read-only worker. Route through project docs; inspect architecture, reusable helpers/components, impacted files, APIs/data contracts, authorization/security, compatibility, migrations, tests, and rollout implications. Resolve blocking requirement ambiguity before representing the plan as executable. Organize large changes into ordered stages; keep small plans concise.

Output: objective; confirmed requirements; architecture approach; key decisions; relevant docs; expected file changes; API/data contracts; migration strategy (or not applicable); ordered implementation steps; tests and exact validation commands based on repository evidence; documentation updates; risks; assumptions; open questions. The plan must be actionable by a new implementer. Validate coverage of acceptance criteria and mark unavailable validation prerequisites.

Default: display the complete plan and stop for explicit approval. Do not edit code, dependencies, artifacts, or Git. Persistence is a separate authorized [artifact step](../../references/artifacts.md).

Only if the current user invocation contains the exact `--auto-implement` token: a writable coordinator obtains the plan from a separate read-only worker without that flag, displays it, resolves blockers, then follows [feature-implement](../feature-implement/SKILL.md). This skips only plan approval for this task. If currently in a read-only session, return a handoff to a writable coordinator; do not attempt to loosen permissions. Do not add multi-round review unless requested or part of feature-delivery.

Model strategy: `dw-analysis`, Astra/high for planning; Sol/medium for authorized implementation. Escalate material architectural/product conflicts to the user. Use selective evidence and one planner, not broad fan-out.
