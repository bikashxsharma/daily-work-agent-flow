# Optional local state

Technical plans are persisted only when the current feature-plan or feature-delivery invocation contains the exact `--write-plan` flag. Other artifacts remain optional and require explicit authorization. Respect repository policy before initializing `.ai-workflow`; if tracked or prohibited, stop and report that the requested plan file could not be persisted, then agree on a repository-approved local path. Never silently save it in the global workflow repository. No application repositories are initialized during global installation.

An authorized coordinator or the user can run:

```sh
python3.11 /absolute/central/scripts/artifact.py init --repo /absolute/repository
python3.11 /absolute/central/scripts/artifact.py save --repo /absolute/repository --feature approval-delegation --kind plan --source /path/to/finalized-plan.md
python3.11 /absolute/central/scripts/artifact.py save --repo /absolute/repository --feature approval-delegation --kind plan --next --source /path/to/finalized-plan.md
```

The deterministic writer receives only a target feature/kind and finalized Markdown content (file or stdin). It has no model and does not implement application changes. It refuses original draft names, overwrites, tracked `.ai-workflow` files, traversal, and symlinked artifact paths. `--next` selects `plan.md`, then `plan-2.md`, and so on without overwriting prior review history. Existing drafts remain untouched.

For `--write-plan` output, use the feature directory already named by an input path under `.ai-workflow/features/<feature>/`. Otherwise derive a short lowercase kebab-case slug from the feature objective. Save the exact user-visible plan with a `PROPOSED` status, scope/source, a short review-focus section, assumptions, open decisions, acceptance-criteria coverage, an approval checkpoint, and enough repository evidence for review. Report the repository-relative path prominently. Persistence is not approval; planning still stops after showing the plan and path unless a separate `--auto-implement` flag was supplied.

The helper checks whether local artifacts are tracked/excluded, and only if necessary appends `/.ai-workflow/` to Git's resolved `info/exclude`. `git rev-parse --git-path` handles linked worktrees; the exclusion may be shared with sibling worktrees. It never edits `.gitignore`. Exclusions cannot conceal tracked files, and a deliberate `git add -f` can bypass an exclusion: never stage these artifacts.

Each artifact records: feature, scope, source draft/specification, current status, approved requirements when verifiable, open decisions, assumptions, and code revision/diff scope. Approval records quote the user's actual decision and identify the relevant scope/version; generated content starts as PROPOSED. A timestamp or generated `APPROVED` heading alone is not approval evidence. Review verdict APPROVED concerns code review, not permission to deploy.

On resume, read the latest relevant artifacts, verify any required user approval, and compare the repository's current state with recorded scope. Ask only for unverifiable approvals or changed material decisions. Fresh explicit instructions override stale artifacts. Keep review findings separate from planning rationale.
