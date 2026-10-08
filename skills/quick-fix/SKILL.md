---
name: quick-fix
description: Implement a small, clear bug fix or localized low-risk change with focused discovery and validation, avoiding full feature orchestration.
---

# Quick fix

Read [shared workflow](../../references/workflow.md). Inputs: concise request or repository-relative Markdown issue description.

```text
$quick-fix Fix incorrect employee date formatting
$quick-fix .ai-workflow/features/date-format/draft.md
$quick-fix --verbose Fix incorrect employee date formatting
```

The explicit fix request authorizes a clear localized change. Inspect necessary instructions, routed docs, relevant code/tests, and Git state. Identify the failure, implement the smallest correct fix, and run focused checks. Update existing tests/docs when meaningful. Do not create persistent plans or a review swarm for a trivial change.

Allowed: authorized local application/test/doc edits in workspace-write. Prohibited: unrelated refactors, unnecessary installs, automatic staging/commits/pushes/deployment, personal config in company repositories, or silent scope expansion. Escalate to feature-discovery/feature-plan **before broad edits** when business rules are ambiguous or the task touches migrations, authorization/security, significant architecture, broad integrations, or material regression risk. Clearly explain the newly discovered decision; preserve already verified authorization.

Output: issue/cause; fix and files; focused validation with real results; remaining limitations. Validate against the reported failure, not merely syntax. User may run feature-review separately. Follow shared reporting rules: concise by default; with `--verbose`, expand changed-file, completed-work, test, validation, and limitation summaries without raw reasoning or complete logs.

Model strategy: `dw-quick`, Luna/medium; move to Sol/medium or stronger reasoning when complexity warrants it. One agent normally suffices. Use symbol searches, concise context, and no repetitive full-suite runs.
