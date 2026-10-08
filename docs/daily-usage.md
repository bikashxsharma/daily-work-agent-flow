# Everyday usage

The following `$skill-name` lines are prompts **inside Codex**, not shell commands. Launch Codex in the application repository. File inputs resolve from its Git root. Global skills choose the workflow; they do not change the current model or sandbox. For repeatable role settings use the shell launcher shown below.

```text
$quick-fix Fix incorrect employee date formatting
$feature-discovery Add employee approval delegation
$feature-discovery .ai-workflow/features/approval-delegation/draft.md
$feature-plan .ai-workflow/features/approval-delegation/specification.md
$feature-plan --auto-implement .ai-workflow/features/approval-delegation/specification.md
$feature-implement .ai-workflow/features/approval-delegation/plan.md
$feature-review Review current uncommitted changes
$feature-review Review changes against main
$feature-delivery .ai-workflow/features/approval-delegation/draft.md
$feature-delivery --auto-implement .ai-workflow/features/approval-delegation/draft.md
```

An explicit implementation request authorizes a clear change. An unapproved or materially ambiguous plan does not become approved because it lives in `plan.md`. Default delivery stops for specification approval, then for plan approval. `--auto-implement` skips only the second checkpoint. It is interpreted by these skills, not a built-in `codex` option.

## Shell launcher

Set a convenient shell variable (optional; no shell startup files are edited):

```sh
FLOW=/Users/bikashsharma/agents/daily-work-agent-flow
cd /Users/bikashsharma/tyorel/bolt
python3.11 "$FLOW/scripts/workflow.py" discovery 'Add employee approval delegation'
python3.11 "$FLOW/scripts/workflow.py" discovery '.ai-workflow/features/approval-delegation/draft.md'
python3.11 "$FLOW/scripts/workflow.py" plan '.ai-workflow/features/approval-delegation/specification.md'
python3.11 "$FLOW/scripts/workflow.py" plan --auto-implement '.ai-workflow/features/approval-delegation/specification.md'
python3.11 "$FLOW/scripts/workflow.py" implement '.ai-workflow/features/approval-delegation/plan.md'
python3.11 "$FLOW/scripts/workflow.py" review 'Review current uncommitted changes against the approved specification'
python3.11 "$FLOW/scripts/workflow.py" quick-fix 'Fix incorrect employee date formatting'
python3.11 "$FLOW/scripts/workflow.py" delivery 'Add employee approval delegation'
python3.11 "$FLOW/scripts/workflow.py" delivery --auto-implement '.ai-workflow/features/approval-delegation/draft.md'
```

These examples are alternatives, not a sequence to run indiscriminately. Replace the repository path for a personal project. The supplied personal-project directory did not exist at installation; the setup does not create it.

Add `--repo /absolute/application` to launch from another directory. Add `--dry-run` to inspect the command without starting Codex; connector names are resolved only at actual launch. `--exec` returns a noninteractive report in fresh context and is intended for coordinator-to-worker analysis. It cannot obtain missing user decisions; report blockers and let the interactive coordinator ask.

Native profiles can be selected with `codex --profile dw-code` or `codex --profile dw-quick`. Profile defaults sit below trusted project config. The launcher pins model and permissions using CLI overrides and disables local workflow connectors. Do not use a bare profile as proof of isolation; ordinary `codex` retains existing integrations and defaults.

## Resume and artifacts

For long tasks, ask the writable coordinator to persist the finalized specification/plan and user decisions separately. Read-only workers cannot save them. To initialize the optional directory yourself:

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
