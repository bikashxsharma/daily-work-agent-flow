---
name: feature-implement
description: Implement an approved technical plan or an explicitly authorized clear change, including appropriate tests, existing project documentation, and validation.
---

# Feature implement

Read [shared workflow](../../references/workflow.md). Inputs: approved plan, repository-relative Markdown path, or a sufficiently clear authorized change.

```text
$feature-implement Implement the approved approval-delegation plan
$feature-implement .ai-workflow/features/approval-delegation/plan.md
$feature-implement --verbose .ai-workflow/features/approval-delegation/plan.md
```

Verify scope and approval from the current request or reliable prior evidence. Read requirements, routed docs, applicable scoped rules, current code and Git state. Confirm key plan assumptions against code. Implement the smallest complete behavior using existing patterns. For full-stack work, consider frontend, backend, business logic, contracts, persistence, migrations/backfills, authorization, errors, integrations, edge cases and regression coverage as relevant. Use the existing migration framework; never run production migrations.

Allowed: scoped source/test/documentation changes and safe local validation in workspace-write. Update actual feature documentation when behavior or architecture changes. Preserve user changes. Prohibited: automatic Git staging/commits/pushes/merges/deployments, personal configuration in application repos, unauthorized dependencies/infrastructure/secrets or unrelated refactors. If a material plan flaw changes approved scope, stop and request a decision. Routine implementation details do not require repeated approval.

Apply the shared risk-based testing policy. Inspect the final diff/status and accidental artifact tracking. Output: implemented behavior; changed files; tests added/updated; exact validation commands/results; documentation changes; assumptions; deviations; remaining limitations. Separate failures/skips from passes. Follow shared reporting rules: concise by default; with `--verbose`, expand changed-file, completed-work, test, validation, deviation, and limitation summaries without raw reasoning or complete logs.

Model strategy: `dw-code`, Sol/medium for standard implementation; select Sol/high for complex full-stack work, security, financial logic, migrations, broad architecture, or difficult regressions. Astra/high is an optional explicit escalation, not the default implementation model. Verify available settings before switching. Avoid multiple writers and redundant checks. Independent review is available separately; implementing a plan does not automatically start full delivery.
