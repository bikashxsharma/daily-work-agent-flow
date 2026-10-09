# Models, profiles, and permissions

Verified on 2026-10-08 against installed `codex-cli 0.160.1`, local help, the official manual, and the signed-in app-server `model/list`. The catalog returned `gpt-6-astra`, `gpt-6.1-sol`, and `gpt-6-luna` with the reasoning efforts used below. Catalog availability is not a guarantee of future quota or every inference succeeding. No new authentication or provider is configured.

| Role | Selected model | Effort | Phase permission | Fallback | Verification |
|---|---|---|---|---|---|
| Discovery | gpt-6.1-sol | medium | read-only, never escalate | gpt-6-astra/medium | model/list |
| Detailed planning | gpt-6-astra | high | read-only, never escalate | gpt-6.1-sol/high | model/list |
| Quick fix | gpt-6-luna | medium | workspace-write, on-request | gpt-6.1-sol/medium | model/list |
| Standard implementation | gpt-6.1-sol | medium | workspace-write, on-request | gpt-6-astra/medium | model/list |
| Complex implementation | gpt-6.1-sol | high, selected explicitly | workspace-write, on-request | gpt-6-astra/high | model/list; no separate profile |
| Independent review | gpt-6-astra | high | read-only, never escalate | gpt-6.1-sol/high | model/list |
| Remediation | gpt-6.1-sol | medium | workspace-write, on-request | gpt-6-astra/high | model/list |
| Simple file discovery | gpt-6-luna | low | read-only, never escalate | gpt-6.1-sol/low | model/list |
| Delivery coordinator | gpt-6.1-sol | medium | workspace-write, on-request | gpt-6-astra/medium | model/list |

Fallbacks are deliberate choices, never silent retries that change quality/cost. Recheck `model/list` using `scripts/probe.py` when availability changes. Edit the central profile and/or agent file to select an available model/effort. Do not set model IDs in `openai.yaml`; it holds skill UI metadata, not execution configuration.

Use Luna for localized low-risk fixes and searches, Sol for normal coding, and Astra for demanding planning/review. Increase effort for authorization/security, financial/domain logic, migrations, architecture, cross-service contracts and hard regressions. Stronger reasoning and more agents consume more tokens; inspect selective evidence and avoid needless repeat review. Exact account pricing was not inspected and is not hardcoded.

Native profile files are `~/.codex/dw-discovery.config.toml`, `dw-analysis.config.toml`, `dw-review.config.toml`, `dw-code.config.toml`, `dw-quick.config.toml`, and `dw-delivery.config.toml`, symlinked to `profiles/`. `dw-discovery` uses Sol/medium for feature discovery; `dw-analysis` remains Astra/high for detailed technical planning. Codex 0.134+ uses separate `<name>.config.toml` layers, not `[profiles.name]` tables. Existing `~/.codex/config.toml` remains intact. `$CODEX_HOME` is respected by installation.

Native custom agents are symlinked under `~/.codex/agents/`; standalone TOML supports `name`, `description`, `developer_instructions`, model, reasoning, and sandbox settings. Read-only defaults are insufficient when a writable parent's live overrides take precedence. The launcher uses separate processes and CLI overrides for enforced analysis boundaries. Default sessions use a temporary minimal Codex home with existing authentication and no MCP configuration. An explicit repeatable `--allow-mcp NAME` opt-in uses the normal configuration and enables only named configured servers. Ordinary Codex remains unchanged; skill instructions still prohibit unsolicited connector use. Profiles alone do not disable arbitrary future MCP servers.

The launcher fixes its role model/effort above project settings. Workspace-write includes system temporary directories; it does not grant arbitrary writes to other application repositories. Higher-priority managed policies still govern permitted operation. To intentionally run a complex implementation directly after approval:

```sh
codex --profile dw-code --model gpt-6.1-sol -c 'model_reasoning_effort="high"' --sandbox workspace-write -a on-request
```

Direct CLI use retains your configured integrations. Check current permissions before delegating, and use the separate launcher for planning/review. A skill invoked in an existing chat cannot switch the parent model in prose.

Sources: [official skills discovery](https://learn.chatgpt.com/docs/build-skills), [custom agents and override behavior](https://learn.chatgpt.com/docs/agent-configuration/subagents), [profiles and CLI overrides](https://learn.chatgpt.com/docs/config-file/config-advanced), [configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference), [app-server model and skill discovery](https://developers.openai.com/codex/app-server). The current official manual was fetched during setup; local CLI behavior takes precedence where versions differ.
