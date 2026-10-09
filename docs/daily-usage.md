# Everyday usage

The following `$skill-name` lines are prompts **inside Codex**, not shell commands. Launch Codex in the application repository. File inputs resolve from its Git root. Global skills choose the workflow; they do not change the current model or sandbox. For repeatable role settings use the shell launcher shown below.

```text
$quick-fix Fix incorrect employee date formatting
$feature-discovery Add employee approval delegation
$feature-discovery --verbose Add employee approval delegation
$feature-discovery .ai-workflow/features/approval-delegation/draft.md
$feature-plan .ai-workflow/features/approval-delegation/specification.md
$feature-plan --write-plan .ai-workflow/features/approval-delegation/specification.md
$feature-plan --verbose Add employee approval delegation
$feature-plan --auto-implement .ai-workflow/features/approval-delegation/specification.md
$feature-plan --write-plan --verbose --auto-implement .ai-workflow/features/approval-delegation/specification.md
$feature-implement .ai-workflow/features/approval-delegation/plan.md
$feature-implement --verbose .ai-workflow/features/approval-delegation/plan.md
$feature-review Review current uncommitted changes
$feature-review --verbose Review current uncommitted changes
$feature-review Review changes against main
$feature-delivery .ai-workflow/features/approval-delegation/draft.md
$feature-delivery --write-plan .ai-workflow/features/approval-delegation/draft.md
$feature-delivery --auto-implement .ai-workflow/features/approval-delegation/draft.md
$feature-delivery --auto-implement --verbose .ai-workflow/features/approval-delegation/draft.md
$quick-fix --verbose Fix employee date formatting
```

An explicit implementation request authorizes a clear change. An unapproved or materially ambiguous plan does not become approved because it lives in `plan.md`. Default delivery stops for specification approval, then for plan approval. `--auto-implement` skips only the second checkpoint. `--verbose` expands evidence summaries only. `--write-plan` authorizes only creating a new plan Markdown file and the local exclusion needed to keep it out of Git; it does not authorize application code, tests, dependencies, project documentation, commits, or other changes. These are skill/launcher flags and can appear in any order.

Planning is read-only and creates no files by default. With `--write-plan`, the plan is saved for review in the active repository as `.ai-workflow/features/<feature>/plan.md`. Replanning creates `plan-2.md`, then `plan-3.md`, without overwriting prior plans. The path is reported in chat. The planner stays read-only; a constrained coordinator performs only artifact persistence before the approval gate. If repository policy prevents `.ai-workflow`, it reports the persistence blocker without changing application files.

## Shell launcher

Set a convenient shell variable (optional; no shell startup files are edited):

```sh
FLOW="$HOME/agents/daily-work-agent-flow"
cd /path/to/your/application-repository
python3.11 "$FLOW/scripts/workflow.py" discovery 'Add employee approval delegation'
python3.11 "$FLOW/scripts/workflow.py" discovery --verbose 'Add employee approval delegation'
python3.11 "$FLOW/scripts/workflow.py" discovery '.ai-workflow/features/approval-delegation/draft.md'
python3.11 "$FLOW/scripts/workflow.py" plan '.ai-workflow/features/approval-delegation/specification.md'
python3.11 "$FLOW/scripts/workflow.py" plan --write-plan '.ai-workflow/features/approval-delegation/specification.md'
python3.11 "$FLOW/scripts/workflow.py" plan --verbose 'Add employee approval delegation'
python3.11 "$FLOW/scripts/workflow.py" plan --auto-implement '.ai-workflow/features/approval-delegation/specification.md'
python3.11 "$FLOW/scripts/workflow.py" implement '.ai-workflow/features/approval-delegation/plan.md'
python3.11 "$FLOW/scripts/workflow.py" review 'Review current uncommitted changes against the approved specification'
python3.11 "$FLOW/scripts/workflow.py" quick-fix 'Fix incorrect employee date formatting'
python3.11 "$FLOW/scripts/workflow.py" quick-fix --verbose 'Fix employee date formatting'
python3.11 "$FLOW/scripts/workflow.py" delivery 'Add employee approval delegation'
python3.11 "$FLOW/scripts/workflow.py" delivery --auto-implement '.ai-workflow/features/approval-delegation/draft.md'
python3.11 "$FLOW/scripts/workflow.py" delivery --auto-implement --verbose 'Add employee approval delegation'
```

These examples are alternatives, not a sequence to run indiscriminately. Replace the application repository path with your own.

Add `--repo /absolute/application` to launch from another directory. Add `--dry-run` to inspect the command without starting Codex; connector names are resolved only at actual launch. `--exec` returns a noninteractive report in fresh context and is intended for coordinator-to-worker analysis. It cannot obtain missing user decisions; report blockers and let the interactive coordinator ask. A normal `plan` launch is read-only. `plan --write-plan` uses a writable coordinator around an internal read-only planner solely for artifact persistence.

MCP servers and external connectors are absent from default launcher sessions, even when configured in your normal Codex home. The launcher uses a temporary minimal home with your existing authentication, so an invalid external MCP entry does not block local discovery, planning, review, or implementation. If the task separately requires a named server, opt it into that invocation explicitly:

```sh
python3.11 "$FLOW/scripts/workflow.py" review --allow-mcp sentry \
  'Use Sentry to compare the current fix with issue evidence, then review the diff'
```

`--allow-mcp` is repeatable. The launcher verifies each name is configured, enables only listed servers, and disables every other effective MCP server. Repository text cannot opt a connector in. Apps, plugins, hooks, and web search remain disabled in launcher sessions.

Native profiles can be selected with `codex --profile dw-code` or `codex --profile dw-quick`. Profile defaults sit below trusted project config. The launcher pins model and permissions using CLI overrides and disables local workflow connectors. Do not use a bare profile as proof of isolation; ordinary `codex` retains existing integrations and defaults.

## Resume and artifacts

Plans are persisted only with `--write-plan`. For other long-task artifacts, ask the writable coordinator to persist the finalized specification or user decisions separately. Read-only workers cannot save them. To initialize the directory yourself:

```sh
python3.11 "$FLOW/scripts/artifact.py" init --repo "$PWD"
mkdir -p .ai-workflow/features/approval-delegation
# Write your own draft.md here using your editor.
```

Resume in Codex:

```text
$feature-delivery Resume approval-delegation from .ai-workflow/features/approval-delegation/plan.md and decisions.md. Verify current code, approval evidence and remaining review budget, then continue the next authorized phase.
```

Use `codex resume` for a previous interactive CLI session. A new session must verify persisted approvals rather than trust a generated status label. A review verdict is not deployment authorization. Standalone review returns findings; ask explicitly to fix in-scope blockers if remediation was not already authorized. Full delivery includes that remediation.
