# Independent review and bounded remediation

Use a fresh isolated read-only reviewer via execution.md. Input: explicit scope, user requirements/approved specification, current diff and surrounding code, applicable rules/docs, actual test results. Plans are optional background, never proof of correctness. Determine whether scope is uncommitted changes, explicit commit, base branch comparison, supplied diff, or feature paths; resolve ambiguity before attributing unrelated edits. Include relevant untracked files without blindly reading secrets/binaries. Use `git diff --no-ext-diff --no-textconv` to avoid configured external diff helpers; use an identified merge base for branch comparisons.

Check functional/business correctness, edge cases, regressions, frontend/backend and API compatibility, migrations, data integrity/transactions, authorization/security, races, error paths, backwards compatibility, performance, tests, docs, and repository conventions. Only report concrete evidence or a plausible specific failure scenario. Distinguish missing evidence from confirmed defects.

Each finding: stable ID; critical/high/medium/low severity; blocking/suggestion classification; file and line/location; evidence/failure scenario; expected versus actual behavior; recommended fix. End with total counts and severity counts, unresolved blocking IDs, validation gaps, and exactly one verdict: APPROVED, CHANGES_REQUESTED, NEEDS_USER_DECISION. Never approve unresolved blocking findings or a material unreviewed scope. Low-severity findings can still block when requirements justify it; do not silently downgrade findings to finish.

Default maximum: **three reviewer passes total**, not three per issue. Use fewer when risk and evidence justify completion. For substantial delivery, require at least two distinct independent checks and a third when remediation/risk warrants it:

1. Functional correctness: inspect requirements, full task diff, surrounding behavior; find missing behavior/regressions.
2. Integration/regression: fresh context, independently inspect cross-module/API/data/migration behavior and important missing tests, beyond merely checking earlier fixes.
3. Final verification: review the complete current task diff, resolved findings, new regressions, requirements and validation evidence.

Reviewers never remediate. A separate authorized writable implementer/remediator handles blocking findings within approved scope, then runs focused validation before the next review. Keep a ledger of each finding, resolution evidence, remaining blockers, and pass count. Prefer suggestions as report-only. User decisions affecting requirements/safety stop remediation immediately. Standalone review does not itself authorize fixes; an explicit fix request, existing scope authorization, or full delivery does.

Never remediate after pass three and label the unseen result approved. Stop with remaining findings, or mark later user-authorized edits unreviewed until the user explicitly expands the review budget. Do not reset the budget across session resumes. If independent context/enforcement is unavailable, report NEEDS_USER_DECISION with the limitation; do not represent self-review as independent review.
