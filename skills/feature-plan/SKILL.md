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
$feature-plan --write-plan Add employee approval delegation
$feature-plan --verbose Add employee approval delegation
$feature-plan --write-plan --verbose Add employee approval delegation
$feature-plan --auto-implement --write-plan --verbose .ai-workflow/features/approval-delegation/specification.md
```

Planning itself runs in a read-only worker. Route through project docs; inspect architecture, reusable helpers/components, impacted files, APIs/data contracts, authorization/security, compatibility, migrations, tests, and rollout implications. Resolve blocking requirement ambiguity before representing the plan as executable. Organize large changes into ordered stages; keep small plans concise.

Output reviewable Markdown. Begin with the feature name, `Status: PROPOSED`, source/scope, and a short **Review focus** section containing the decisions or risks the user should inspect before approval. Then include: objective; confirmed requirements; architecture approach; key decisions; relevant docs; expected file changes; API/data contracts; migration strategy (or not applicable); ordered implementation steps; tests and exact validation commands based on repository evidence; documentation updates; risks; assumptions; open questions; acceptance-criteria coverage; and an explicit approval checkpoint. The plan must be actionable by a new implementer and easy for a human to review without the chat transcript. Mark unavailable validation prerequisites.

Without `--write-plan`, run the entire planning invocation read-only, display the complete plan in chat, and create no files.

Only when the current invocation contains the exact `--write-plan` token, a writable coordinator may persist the exact complete plan as reviewable Markdown in the active/calling repository: `.ai-workflow/features/<feature-slug>/plan.md`, or the next `plan-N.md` when a prior plan exists. Use the separate deterministic [artifact step](../../references/artifacts.md); the planner itself remains read-only. This flag authorizes only the new Markdown artifact and required local Git exclusion entry. Do not edit application code, tests, dependencies, project documentation, other workflow artifacts, or Git state. Never save the plan in this global skills repository unless it is itself the application repository being planned. Report the repository-relative artifact path. If repository policy or tracked `.ai-workflow` content prevents safe persistence, stop and report that blocker rather than silently saving elsewhere.

Default: after displaying the plan, stop for explicit approval. If `--write-plan` was supplied, save it before stopping. The artifact remains `PROPOSED`; creating it is not approval.

Only if the current user invocation contains the exact `--auto-implement` token: a writable coordinator obtains the plan from a separate read-only worker without forwarding `--auto-implement` or `--write-plan`, displays it, resolves blockers, then follows [feature-implement](../feature-implement/SKILL.md). Save the plan only when `--write-plan` is also present. `--auto-implement` skips only plan approval for this task. If `--write-plan` was requested from a read-only session, return the complete plan plus a handoff stating that artifact persistence requires the constrained writable coordinator; do not loosen the planner's permissions. Do not add multi-round review unless requested or part of feature-delivery.

Follow shared reporting rules. Default output keeps progress concise while the saved plan remains complete. With `--verbose`, include architecture decisions, affected files, ordered steps, contracts/migrations, and validation strategy in the chat summary as well. Verbosity does not affect the plan content, persistence, approval gate, or execution.

Model strategy: `dw-analysis`, Astra/high for planning; Sol/medium for authorized implementation. Escalate material architectural/product conflicts to the user. Use selective evidence and one planner, not broad fan-out.
