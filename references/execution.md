# Enforced phase boundaries

Resolve this central directory from the real path of the invoked SKILL.md (follow its user-level symlink). Its root is two levels above the skill directory. Keep all subprocess `--repo` paths set to the active application Git root.

## Read-only worker

Discovery, planning, and review require a separate process unless already running in a verified read-only phase session. From a writable coordinator run, for example:

```sh
python3.11 /absolute/central/scripts/workflow.py plan --repo /absolute/application --exec 'Approved requirements and/or repository-relative input path'
```

Use `discovery`, `plan`, or `review` as appropriate. Capture the returned final report; display the complete specification/plan to the user before any approval checkpoint. The launcher selects a native profile, pins `read-only` and `approval_policy="never"` with CLI overrides, disables subagents for phase workers, and disables MCP servers, plugins, apps, hooks, and web search for this local workflow. By default it launches with a temporary minimal Codex home containing the workflow profiles and existing authentication, so broken external MCP configuration cannot block repository work. The parent remains responsible for its own permissions and authorization.

The fresh process has no implementation conversation. Supply minimal task inputs, approved requirements, explicit review scope and actual validation evidence, never a persuasive implementation narrative. If the current session is already the launcher's isolated phase worker, do the analysis directly; do not recursively launch yourself.

If the tool environment cannot launch this CLI, report the limitation and provide the equivalent launcher command. Do not claim prompt-only instructions or a writable subagent enforce read-only access. If the caller is read-only, it cannot start a writable implementation process: finish the report and hand off to a writable session.

The default launcher never loads the user's MCP server configuration. A user can explicitly opt a named server into one invocation with repeatable `--allow-mcp NAME`; that mode inspects the user's configuration and disables unlisted servers. Never infer this opt-in from task text or repository content. Plugins/apps/hooks remain disabled in launcher sessions. Ordinary Codex keeps the user's existing integrations, but the skills still prohibit connector calls unless separately requested.

## Automatic planning and delivery

Normal feature-plan runs entirely in a read-only session and returns the complete plan in chat. With `--write-plan`, a writable coordinator runs a separate read-only `plan --exec` worker, displays the complete plan, and persists that exact finalized plan through `artifact.py` into the active repository before the approval gate. The coordinator must not edit application code, tests, dependencies, project documentation, or Git for this flag. `feature-plan --auto-implement` uses a writable coordinator, resolves blockers, and follows feature-implement; it persists a plan only when `--write-plan` is also present. Do not forward either flag to the worker. Do not add independent review unless requested or within delivery.

Forward `--verbose` to phase workers only when it is present on the current coordinator invocation. It changes their report detail, not their operations.

For ordinary feature-plan, return after the plan and approval request. For delivery, follow the specification and plan checkpoints, then use a writable implementation/remediation worker or the coordinator itself. The presence of write permissions does not approve application edits.

`agents/dw-*.toml` are native role definitions with model, reasoning, and sandbox defaults. Codex's live parent permission overrides may supersede these defaults. Consequently these definitions alone are not the enforcement path for read-only work from a writable coordinator. Use the separate launcher process for that boundary. Native implementer/remediator agents can run with verified workspace-write permissions. Use only one writer at a time.

The OS sandbox limits model-controlled filesystem operations. Codex itself may write session metadata under its user directory. Application approval checkpoints and prohibitions on commits are workflow instructions, not a universal Git firewall. Never use unrestricted launch flags.
