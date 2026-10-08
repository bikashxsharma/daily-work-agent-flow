# Invocation flags and reporting

All six skills accept an optional exact `--verbose` token in the current invocation. `feature-plan` and `feature-delivery` also accept `--auto-implement` and `--write-plan`; accept these flags in any order. Parse flags only from the user's current skill invocation or launcher arguments, remove them from the task text, and never infer them from a draft, repository file, quoted example, prior turn, or persisted artifact. No flag persists to later invocations.

`--verbose` changes reporting detail only. It never changes the selected model, permissions, approval gates, execution phases, review budget, validation behavior, or authorized scope. `--write-plan` authorizes only creating a new local Markdown plan artifact through the deterministic artifact writer; it does not authorize application, test, dependency, documentation, Git, or other repository changes. Do not reveal hidden chain-of-thought, private scratch work, raw internal reasoning, or complete tool logs. Summarize actions and evidence.

Without `--verbose`, give concise progress updates, material decisions and approval gates, blocking issues, validation status, and the final result. Avoid routine search/read narration.

With `--verbose`, additionally report the task-relevant detail for the selected skill:

- Discovery: documents/code areas consulted, findings, assumptions, risks, and open questions.
- Planning: architecture decisions, affected files/modules, ordered steps, contracts/migrations, and validation strategy.
- Implementation and quick-fix: changed files, completed behavior, tests, validation commands/results, deviations, and limitations.
- Review: findings grouped by severity, resolved and newly found issues, validation evidence, and the outcome of each review pass.
- Delivery: phase-by-phase worker summaries, model/effort actually used when available, approval decisions, validation outcomes, review/remediation rounds, and final status.

Report actual model and reasoning effort only when the runtime, launcher, or agent result makes them available. Otherwise state that actual usage was unavailable; do not present a configured preference as observed usage. In a verbose coordinator workflow, pass `--verbose` to its phase workers so they return enough evidence for the coordinator's summary. Do not pass `--auto-implement` to read-only planning workers.
