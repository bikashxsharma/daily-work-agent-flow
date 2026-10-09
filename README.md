# Daily Codex development workflow

Six reusable skills for company and personal repositories. This folder is the source of truth; user-level symlinks make the skills available wherever Codex starts. Built for the installed Codex CLI **0.160.1** on macOS, using Python **3.11+** for the small setup helpers.

Canonical location: `/Users/bikashsharma/agents/daily-work-agent-flow`. Your explicit current-folder request supersedes the pasted task's `agetns` example. No second workflow directory is created.

## Start here

From your application repository, open Codex and invoke a skill:

```text
$quick-fix Fix incorrect employee date formatting
$feature-delivery Add employee approval delegation
```

For pinned models, explicit permissions and connector isolation, use the launcher from the application repository:

```sh
python3.11 /Users/bikashsharma/agents/daily-work-agent-flow/scripts/workflow.py quick-fix 'Fix incorrect employee date formatting'
python3.11 /Users/bikashsharma/agents/daily-work-agent-flow/scripts/workflow.py delivery 'Add employee approval delegation'
```

Planning, discovery and review use separate read-only sessions; a skill alone cannot change a session's sandbox or model. Native parent permission overrides can supersede subagent defaults, so the launcher is the enforced phase boundary. The writable coordinator displays the plan and waits for approval unless explicitly invoked with `--auto-implement`.

Planning is fully read-only by default. Add `--write-plan` to save only a reviewable Markdown plan in the calling repository under `.ai-workflow/features/<feature>/plan.md`; later plans are versioned without overwrite. That flag does not authorize application-code or other project changes. All skills accept `--verbose` for expanded evidence summaries. MCP/connectors are disabled unless explicitly opted into the launcher with `--allow-mcp NAME` for a separately requested operation.

| Skill | Use it for |
|---|---|
| `$feature-discovery` | Explore requirements and get a specification for approval |
| `$feature-plan` | Produce a technical plan and stop for approval |
| `$feature-implement` | Implement an approved plan or explicitly authorized clear change |
| `$quick-fix` | Fix a small, well-understood issue economically |
| `$feature-review` | Independently inspect a scoped change without editing it |
| `$feature-delivery` | Coordinate approvals, implementation, validation, review and scoped remediation |

## Files

```text
daily-work-agent-flow/
├── README.md
├── .gitignore
├── skills/
│   ├── feature-discovery/{SKILL.md,agents/openai.yaml}
│   ├── feature-plan/{SKILL.md,agents/openai.yaml}
│   ├── feature-implement/{SKILL.md,agents/openai.yaml}
│   ├── quick-fix/{SKILL.md,agents/openai.yaml}
│   ├── feature-review/{SKILL.md,agents/openai.yaml}
│   └── feature-delivery/{SKILL.md,agents/openai.yaml}
├── agents/dw-{discovery,planner,reviewer,implementer,remediator,explorer}.toml
├── profiles/dw-{discovery,analysis,review,code,quick,delivery}.config.toml
├── references/{workflow,execution,artifacts,reporting,review}.md
├── scripts/{install,workflow,artifact,codex_rpc,probe,test_setup,test_native,validate}.py
└── docs/{daily-usage,workflow-guide,model-configuration,validation}.md
```

### How the pieces fit

| Part | Purpose |
|---|---|
| `skills/*/SKILL.md` | Instructions for each workflow: what to inspect, change, validate, and report. `agents/openai.yaml` holds skill UI metadata, not model settings. |
| `profiles/*.config.toml` | Model, reasoning effort, and permission defaults for launcher sessions. Edit the relevant profile to change the model used by `workflow.py`. |
| `agents/*.toml` | Model, instructions, and permission defaults for native Codex subagents. These are separate from launcher profiles. |
| `references/*.md` | Shared rules used by multiple skills, including approval gates and read-only work. |
| `scripts/workflow.py` | Launches Codex with the selected profile, explicit permissions, and default MCP isolation. A skill invoked in an existing chat cannot switch that chat's model. |
| `scripts/install.py` and `scripts/artifact.py` | Install the central skill/profile/agent links; manage optional local specification and plan files. |
| `scripts/codex_rpc.py`, `probe.py`, `validate.py`, and `test_*.py` | Inspect Codex capabilities, check setup, and test the workflow helpers. |

Outside this folder the installer creates only six skill links under `~/.agents/skills/`, six agent links under `${CODEX_HOME:-~/.codex}/agents/`, and six profile links under `${CODEX_HOME:-~/.codex}/`. It never edits the existing `config.toml`, authentication, integrations, global instructions, or application repositories. Sources remain here. Codex's own inspection commands may update its normal caches/runtime metadata.

## Setup and maintenance

```sh
python3.11 scripts/install.py                    # Show proposed links; refuse collisions
python3.11 scripts/test_setup.py                 # Isolated safety/behavior tests
python3.11 scripts/install.py --apply            # Install globally; may need sandbox approval
python3.11 scripts/validate.py                   # Local file/link/config checks
python3.11 scripts/validate.py --live            # Codex discovery/model/profile checks; no inference
python3.11 scripts/test_native.py               # Native sandbox probes; may require outer sandbox approval
```

Restart Codex or use `/skills` if a running session has a stale skill list. Edit the central source files to maintain the system. Never replace an existing destination blindly. `scripts/install.py --uninstall` previews removal; add `--apply` to remove only this installation's matching links. Sources and existing settings are retained.

Read [daily usage](docs/daily-usage.md), [repository context and approval guide](docs/workflow-guide.md), [models and permissions](docs/model-configuration.md), and [validation evidence/limitations](docs/validation.md).
