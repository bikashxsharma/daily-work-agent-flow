# Enforced phase boundaries

Resolve this central directory from the real path of the invoked SKILL.md (follow its user-level symlink). Its root is two levels above the skill directory. Keep all subprocess `--repo` paths set to the active application Git root.

## Read-only worker

Discovery, planning, and review require a separate process unless already running in a verified read-only phase session. From a writable coordinator run, for example:

```sh
python3.11 /absolute/central/scripts/workflow.py plan --repo /absolute/application --exec 'Approved requirements and/or repository-relative input path'
```

Use `discovery`, `plan`, or `review` as appropriate. Capture the returned final report; display the complete specification/plan to the user before any approval checkpoint. The launcher selects a native profile, pins `read-only` and `approval_policy="never"` with CLI overrides, disables subagents for phase workers, and disables configured MCP servers, plugins, apps, hooks, and web search for this local workflow. Configuration inspection failure aborts launch. The parent remains responsible for its own permissions and authorization.

The fresh process has no implementation conversation. Supply minimal task inputs, approved requirements, explicit review scope and actual validation evidence, never a persuasive implementation narrative. If the current session is already the launcher's isolated phase worker, do the analysis directly; do not recursively launch yourself.

If the tool environment cannot launch this CLI, report the limitation and provide the equivalent launcher command. Do not claim prompt-only instructions or a writable subagent enforce read-only access. If the caller is read-only, it cannot start a writable implementation process: finish the report and hand off to a writable session.

The launcher intentionally disables connectors for all its local workflow sessions; ordinary Codex keeps the user's existing integrations. External evidence needed for a task can be supplied by the user or retrieved in a separately authorized session.

## Automatic planning and delivery

For `feature-plan --auto-implement`, the writable coordinator runs a separate read-only `plan` worker **without forwarding that flag**, displays the complete plan, resolves blockers, and then follows feature-implement. Do not add independent review unless requested or within delivery.

For ordinary feature-plan, return after the plan and approval request. For delivery, follow the specification and plan checkpoints, then use a writable implementation/remediation worker or the coordinator itself. The presence of write permissions does not approve application edits.

`agents/dw-*.toml` are native role definitions with model, reasoning, and sandbox defaults. Codex's live parent permission overrides may supersede these defaults. Consequently these definitions alone are not the enforcement path for read-only work from a writable coordinator. Use the separate launcher process for that boundary. Native implementer/remediator agents can run with verified workspace-write permissions. Use only one writer at a time.

The OS sandbox limits model-controlled filesystem operations. Codex itself may write session metadata under its user directory. Application approval checkpoints and prohibitions on commits are workflow instructions, not a universal Git firewall. Never use unrestricted launch flags.
