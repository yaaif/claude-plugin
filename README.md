# YAAIF for Claude Code

The YAAIF Claude Code plugin provides a local stdio MCP bridge and
Claude-Code-native skills and slash commands for authenticated YAAIF planning,
skill creation, MCP deployment, scenario lifecycle, ambient workflows,
diagnostics, platform tools, and read-only operations support.

**Version:** 1.3.2  
**Logo:** [`assets/logo.svg`](assets/logo.svg)

## Install

```bash
cd ~
npx -y @yaaif/platform-mcp@1.3.3 --install --client claude
claude plugin marketplace add yaaif/claude-plugin
claude plugin install yaaif-platform@yaaif
```

The installer asks you to choose hosted `https://platform.yaaif.ai` or type
another YAAIF URL. Non-interactive: `--yaaif-url https://your.yaaif.host` or
`--profile hosted`.

On enable, Claude Code prompts for `userConfig` values (platform profile, OIDC,
API URLs, tenant, CA, mTLS). Those become `YAAIF_*` environment variables for
the MCP process. You can also set the same variables in the shell.

For local development, load the plugin directly without installing it:

```bash
claude --plugin-dir /path/to/claude-plugin
```

The plugin starts:

```text
npx -y @yaaif/platform-mcp@1.3.3 --client claude
```

Node.js 20 or later is required. Run `/yaaif-platform:yaaif-login` (or
`yaaif_ensure_session`) in a new session for browser PKCE login, or
`yaaif_login_device` where a browser callback is not available.

> **Note:** `@yaaif/platform-mcp` must be on the public npm registry before a
> marketplace install can start the bridge. See
> [docs/npm-publish.md](docs/npm-publish.md). For bridge development, use a
> [local MCP override](#local-mcp-override).

## Profiles and state

Claude Code uses `~/.yaaif/claude` exclusively. It never reads or overwrites
Cursor state in `~/.yaaif/cursor` or Codex state in `~/.yaaif/codex`.

| Profile | Intended use |
| --- | --- |
| `hosted` | Hosted YAAIF endpoints |
| `local` | OIDC and APIs on the local stack |
| `local-hybrid` | Hosted/tunnel OIDC with local APIs |

Override endpoints, tenant, CA, and mTLS with plugin `userConfig` or `YAAIF_*`
environment variables. Use `YAAIF_EXTRA_CA_FILE` for a local CA and
`YAAIF_CLIENT_CERT_FILE` / `YAAIF_CLIENT_KEY_FILE` for mTLS.

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
`/yaaif-platform:yaaif-login`, then follow the skill named in the prompt.

## Skills and commands

Skills are also available as `/yaaif-platform:<skill-name>`. Short command
aliases match the Cursor plugin names and appear as `/yaaif-platform:<command>`.

| Skill | Short command | Purpose |
| --- | --- | --- |
| `yaaif-auth` | `/yaaif-platform:yaaif-login` | Platform profile + login + tenant |
| `yaaif-doctor` | `/yaaif-platform:yaaif-doctor` | Connectivity / TLS / auth diagnostics |
| `yaaif-plan-usecase` | `/yaaif-platform:yaaif-plan` | Use-case plan → approve → create Scenario + objects |
| `yaaif-scenario` | `/yaaif-platform:yaaif-scenario` | Create or maintain a Scenario; Admin UI **Open in Claude Code** |
| — | `/yaaif-platform:yaaif-sync-scenario` | Apply spec → objects, or explicitly adopt live drift |
| `yaaif-create-skill` | `/yaaif-platform:yaaif-new-skill` | Author + load skill |
| `yaaif-create-mcp` | `/yaaif-platform:yaaif-new-mcp` | Scaffold + deploy MCP + API key bind |
| `yaaif-create-ambient` | `/yaaif-platform:yaaif-new-workflow` | Ambient workflows; Admin UI handoff for `workflow_id` |
| `yaaif-platform-tools` | `/yaaif-platform:yaaif-platform-tools` | Discover/call agent-service built-in local tools |
| `yaaif-ops-support` | `/yaaif-platform:yaaif-ops` | Read-only incident triage |

## Local MCP override

When developing the bridge, clone [yaaif/cursor-plugin](https://github.com/yaaif/cursor-plugin),
build `packages/mcp`, and point Claude at that `cli.js` (do not commit a
machine-local path):

```bash
git clone https://github.com/yaaif/cursor-plugin.git
cd cursor-plugin/packages/mcp
npm install && npm run build
```

```json
{
  "mcpServers": {
    "yaaif": {
      "command": "node",
      "args": [
        "/path/to/cursor-plugin/packages/mcp/dist/cli.js",
        "--client",
        "claude"
      ]
    }
  }
}
```

## Development and release

This plugin ships no MCP source — the tool surface lives in
[`cursor-plugin/packages/mcp`](https://github.com/yaaif/cursor-plugin/tree/main/packages/mcp),
published as `@yaaif/platform-mcp` and shared across Cursor, Codex, and Claude
Code via `--client cursor|codex|claude`.

```bash
python3 scripts/check-plugin.py --require-skill-sync
claude plugin validate . --strict
```

Release order: publish `@yaaif/platform-mcp@<version>` from `cursor-plugin` →
confirm with `npm view @yaaif/platform-mcp version` → bump the pin in
[`.mcp.json`](.mcp.json) → install and smoke-test with `claude --plugin-dir` →
submit the tested repository to the Claude Code plugin directory (see
[`docs.claude.com`](https://docs.claude.com) for current submission steps).

See [CHANGELOG.md](CHANGELOG.md) and [docs/npm-publish.md](docs/npm-publish.md).
