# Optional local state

Use persistent artifacts only when requested or useful for a substantial/resumable feature. Respect repository policy before initializing `.ai-workflow`; if tracked or prohibited, stop and agree on an external local path. No application repositories are initialized during global installation.

An authorized coordinator or the user can run:

```sh
python3.11 /absolute/central/scripts/artifact.py init --repo /absolute/repository
python3.11 /absolute/central/scripts/artifact.py save --repo /absolute/repository --feature approval-delegation --kind plan --source /path/to/finalized-plan.md
```

The deterministic writer receives only a target feature/kind and finalized Markdown content (file or stdin). It has no model and does not implement application changes. It refuses original draft names, overwrites, tracked `.ai-workflow` files, traversal, and symlinked artifact paths. Later reports use `plan-2`, `review-2`, etc. Existing drafts remain untouched.

The helper checks whether local artifacts are tracked/excluded, and only if necessary appends `/.ai-workflow/` to Git's resolved `info/exclude`. `git rev-parse --git-path` handles linked worktrees; the exclusion may be shared with sibling worktrees. It never edits `.gitignore`. Exclusions cannot conceal tracked files, and a deliberate `git add -f` can bypass an exclusion: never stage these artifacts.

Each artifact records: feature, scope, source draft/specification, current status, approved requirements when verifiable, open decisions, assumptions, and code revision/diff scope. Approval records quote the user's actual decision and identify the relevant scope/version; generated content starts as PROPOSED. A timestamp or generated `APPROVED` heading alone is not approval evidence. Review verdict APPROVED concerns code review, not permission to deploy.

On resume, read the latest relevant artifacts, verify any required user approval, and compare the repository's current state with recorded scope. Ask only for unverifiable approvals or changed material decisions. Fresh explicit instructions override stale artifacts. Keep review findings separate from planning rationale.
