# YAAIF for Claude Code

The YAAIF Claude Code plugin provides a local stdio MCP bridge and
Claude-Code-native skills for authenticated YAAIF planning, skill creation,
MCP deployment, scenario lifecycle, ambient workflows, diagnostics, platform
tools, and read-only operations support.

## Install

```bash
claude plugin marketplace add yaaif/claude-plugin
claude plugin install yaaif-platform
```

For local development, load the plugin directly without installing it:

```bash
claude --plugin-dir /path/to/claude-plugin
```

The plugin starts:

```text
npx -y @yaaif/platform-mcp@1.3.0 --client claude
```

The process inherits `YAAIF_*` configuration from your environment. Node.js
20 or later is required. Run `yaaif_ensure_session` in a new session to use
browser PKCE login, or `yaaif_login_device` where browser callback login is
not available.

> **Note:** `@yaaif/platform-mcp` must be published to npm before this
> plugin can start (see [Development and release](#development-and-release)).

## Profiles and state

Claude Code uses `~/.yaaif/claude` exclusively. It never reads or overwrites
Cursor state in `~/.yaaif/cursor` or Codex state in `~/.yaaif/codex`.

| Profile | Intended use |
| --- | --- |
| `hosted` | Hosted YAAIF endpoints |
| `local` | OIDC and APIs on the local stack |
| `local-hybrid` | Hosted/tunnel OIDC with local APIs |

Override endpoints, tenant, CA, and mTLS with the existing `YAAIF_*`
environment variables. In particular, use `YAAIF_EXTRA_CA_FILE` for a local CA
and `YAAIF_CLIENT_CERT_FILE` / `YAAIF_CLIENT_KEY_FILE` for mTLS.

## Admin UI handoffs

YAAIF Admin UI exposes **Open in IDE** on scenarios, skills, agents, and
workflows. Choose **Open in Claude Code** to start a new Claude Code session
with a prefilled prompt via Claude Code's
[deep link scheme](https://code.claude.com/docs/en/deep-links.md):
`claude://code/new?q=<prompt>` in the Claude Desktop app (Admin UI omits
`folder` because it cannot know each developer's local clone path). Terminal-only
setups can use `claude-cli://open?q=<prompt>` instead.

| Admin surface | Claude Code skill | Typical prompt fields |
| --- | --- | --- |
| Scenarios | `yaaif-scenario` | `spec_id`, `slug`, readiness blockers |
| Skills | `yaaif-create-skill` | `skill_id`, `goal` |
| Ambient workflows | `yaaif-create-ambient` | `workflow_id`, `agent_id` |
| Agents | MCP agent tools | `agent_id`, `agent_type` |

Install this plugin before using Admin UI handoffs. Authenticate with
`yaaif-auth`, then follow the skill named in the prompt. Claude Code state
stays in `~/.yaaif/claude` and never shares Cursor or Codex profiles.

## Skills

| Skill | Purpose |
| --- | --- |
| `yaaif-auth` | Platform profile + login + tenant |
| `yaaif-doctor` | Connectivity / TLS / auth diagnostics |
| `yaaif-plan-usecase` | Use-case plan → approve → create Scenario + agents/skills/workflows |
| `yaaif-scenario` | Create or maintain a Scenario (Agent Spec); Admin UI **Open in Claude Code** |
| `yaaif-create-skill` | Author + load skill (prefers platform local lifecycle tools) |
| `yaaif-platform-tools` | Discover/call agent-service built-in local tools |
| `yaaif-ops-support` | Read-only incident triage (session/ambient/desktop) |
| `yaaif-create-mcp` | Scaffold + deploy MCP (compose or k8s GitOps) + API key bind |
| `yaaif-create-ambient` | Ambient workflows; Admin UI **Open in Claude Code** for `workflow_id` |

Each skill is invoked as `/yaaif-platform:<skill-name>`, e.g. `/yaaif-platform:yaaif-doctor`.

## Development and release

This plugin ships no source code of its own — the MCP tool surface (~184
`yaaif_*` tools) lives in [`cursor-plugin/packages/mcp`](https://github.com/yaaif/cursor-plugin/tree/main/packages/mcp),
published as `@yaaif/platform-mcp` and shared across the Cursor, Codex, and
Claude Code plugins via a `--client cursor|codex|claude` flag.

Before installing a release candidate, run `claude plugin validate .` against
this repository.

Release order: publish `@yaaif/platform-mcp@<version>` from `cursor-plugin` →
bump the version pinned in this repo's [`.mcp.json`](.mcp.json) → install and
smoke-test locally with `claude --plugin-dir` → submit the tested repository
to the Claude Code plugin directory (see
[`docs.claude.com`](https://docs.claude.com) for current submission steps).
