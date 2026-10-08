# Setup validation — 2026-10-08

The installed setup passed structural, behavioral, live discovery, profile-loading, and native sandbox checks. No application feature or model inference was needed for these checks.

## Environment and preserved state

- Installed CLI: `codex-cli 0.160.1`; central folder started as an empty Git repository with no commits.
- Actual home was discovered as `/Users/bikashsharma`. The explicit requested `agents/daily-work-agent-flow` location is used. `~/tyorel/bolt` exists; `~/meroafno/code` was absent and was not created.
- Existing global config selected Astra/high and included project trust plus Atlassian/Sentry integrations. The installer never opens it for writing. No global AGENTS.md or original feature-delivery/openai.yaml was supplied or found in the inspected skill locations; the attachment's principles were implemented directly.
- Six skill links, six native agent links and six profile links are installed, including the separate Sol/medium discovery role added after the initial setup. Every source is central. No application repository was modified during setup, and no company `.gitignore` was changed. No commits, pushes, merges or deployments were performed.
- Temporary test repositories and official-manual/schema caches were created under permitted temporary directories. Codex capability probes can update their normal user-level caches/runtime metadata. Authentication was not read or relocated.

## Completed checks

- Codex bundled `quick_validate.py`: all six skills passed valid skill/frontmatter checks.
- `python3.11 scripts/test_setup.py`: 15 behavioral tests passed. Covers launcher option ordering/permissions, mixed `--verbose`/`--write-plan`/`--auto-implement` order, explicit named MCP opt-in/default denial, literal prompt handling, default read-only planning versus the constrained write-plan coordinator, versioned plan artifacts, subdirectory roots, company index/personal fallback, idempotent exclusion, partial ignore/negation handling, tracked artifacts, original draft preservation, overwrite/path/symlink rejection, owned-link installation/uninstallation/collision preflight, and linked worktrees. Git operations occur only in temporary repositories; no commits are created.
- Signed-in `model/list` returned Astra, Sol and Luna with selected efforts. This verifies advertised availability, not future quota or model responses.
- Native `skills/list` discovered all six enabled user-level skills with no parser errors.
- `python3.11 scripts/validate.py --live` completed successfully after the discovery-model correction: all central references, 18 installed links, six native profile loads, supported model/effort/sandbox/approval values, and six skill discovery checks passed. The current 15 behavioral tests include explicit launcher assertions for discovery Sol/medium and planning Astra/high.
- `python3.11 scripts/test_native.py` passed: `:read-only` analysis/review could read but could not write inside or outside the test workspace; `:workspace` implementation could write inside and was denied outside it. These are native command sandbox tests using the built-in profiles corresponding to the configured legacy modes, not model compliance tests. Standard workspace mode also permits system temporary directories.
- Independent review found two issues (argument ordering and partial exclusion). Both were fixed and covered by regression tests. A second independent inspection confirmed the fixes and found no further blocking issues within its inspected scope.

## Resolved validation failures

- The outer sandbox blocked manual DNS and app-server runtime access; narrowly scoped approved commands completed those read-only inspections.
- The initial launcher argument parser rejected the documented mixed argument order; changed to intermixed parsing.
- An exclusion probe could mistake one ignored filename for an ignored artifact directory; now checks directory and actual target and refuses conflicting repository rules.
- This CLI rejects `--profile` for `app-server` and `--strict-config` for `debug`. The validator tests native profile loading with supported `debug prompt-input` and uses strict configuration overrides for schema/value checks. `codex sandbox` requires an explicit built-in permission profile; native boundary checks use `:read-only` / `:workspace` corresponding to the configured modes.

## Limits and manual follow-up

- Approval gates, routing judgment, flag interpretation inside a chat, and quality of review are model instructions; mechanical tests cannot prove universal obedience. No application feature was implemented for validation.
- A skill alone cannot enforce sandbox/model changes. Use the launcher. Native subagent defaults can be overridden by parent live permissions; enforced read-only phases use fresh CLI processes.
- Standalone review is read-only. Fixing findings requires separately authorized writable remediation (included in full delivery). Three review passes is the default total budget.
- No production migrations, destructive infrastructure tests, external connector writes, or application test suites were run. Read-only workers report validation gaps instead of writing test caches.
- No live inference was required for structural validation. The everyday workflow should be exercised on a small authorized task when first used; confirm specification/plan checkpoints and final review evidence then.
- Reopen Codex if `/skills` has a cached list. Existing sessions keep their original model/permissions. Python 3.11+ is required; the installed `python3.11` is available, while system `python3` is 3.9.
