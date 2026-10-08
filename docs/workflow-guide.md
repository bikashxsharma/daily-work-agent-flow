# Repository context, approvals, and review

The global skills define how to work. Business rules and architecture come from the active repository. No company source/documentation is copied into these skills. Every phase reads applicable instructions, checks Git state, routes through relevant documentation, and verifies current code.

`documents/documents-knowledge-base.md`, whenever present, is the primary feature-document routing index. Read only the relevant linked documents and corresponding helpers, components, data layer, and tests. Report material discrepancies. Actual authorized feature documentation updates stay in the repository's existing documentation structure.

`.ai-workflow/repository-context.md` is optional custom routing explicitly loaded by the skills. Codex does not automatically discover arbitrary Markdown. Example company routing:

```markdown
# Repository context
Follow applicable AGENTS.md and relevant scoped repository rules.
Start with documents/documents-knowledge-base.md.
Map the requested behavior to its feature documents, then inspect the
corresponding code, shared helpers, data conventions, and tests.
Report meaningful documentation/code conflicts before deciding behavior.
Keep feature documentation updates in documents/ when implementation is authorized.
```

Example personal routing (adjust to actual files; do not create unnecessary docs):

```markdown
# Repository context
Follow AGENTS.md, then README.md and docs/architecture.md when relevant.
Use package scripts and existing tests as the source of validation commands.
This repository has no company knowledge-base index.
Keep small fixes lightweight; record plans only for substantial features.
```

Initialize locally only when needed and allowed by repository policy using `scripts/artifact.py init --repo <repo>`. The helper refuses tracked `.ai-workflow` content, checks existing exclusions, and appends `/.ai-workflow/` only when needed to Git's resolved `info/exclude`; it never changes company `.gitignore`. Linked worktrees may share this exclude file. Check with:

```sh
git check-ignore .ai-workflow/features/approval-delegation/plan.md
git ls-files -- .ai-workflow
git status --short
```

The second command should be empty. Source/test/feature-doc edits remain visible in the third. If local artifacts are already tracked or disallowed, agree on an external local destination; do not untrack team files automatically.

## Phase permissions and decisions

Discovery and planning return proposed artifacts. Separate persistence saves finalized content without granting permission to implement. User approval applies to a specific scope/version. Current explicit instructions supersede old drafts; code and documentation are evidence, not automatically the desired behavior.

The default full workflow is discovery → specification approval → planning → plan approval → implementation/validation → independent review → scoped remediation/validation → final review report. A verified approved input can enter at its appropriate phase. `--auto-implement` applies to one invocation's plan gate only.

Read-only phases use `read-only` plus `approval_policy="never"` and cannot escalate to writes. Since parent overrides can supersede native subagent defaults, writable coordinators launch fresh CLI workers for these phases. Runtime metadata may still be written by Codex itself. App/MCP tools are disabled in the launcher because an OS filesystem sandbox does not constrain remote service side effects.

Substantial delivery gets two independent review checks, optionally a third; three passes is the default total cap. Reviewers receive requirements, current scoped diff, surrounding code, rules, docs and actual validation evidence, not an implementation sales pitch. Reviewers never edit. Remediation uses a separate writer; no fix after the last pass is represented as reviewed. Report APPROVED, CHANGES_REQUESTED or NEEDS_USER_DECISION with severity counts and unresolved blocking IDs.

The small helpers enforce path/exclusion/launch mechanics. Product approval and review judgment remain model workflows, not a state-machine guarantee. On consequential ambiguity, stop for the specific missing decision. No automatic commits, pushes, merges, deployments, production migrations, secret edits, or unrelated repository changes.
