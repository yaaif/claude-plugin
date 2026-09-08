# Changelog

## 1.3.0

- Align plugin version with `@yaaif/platform-mcp` 1.3.0 and the Cursor / Codex plugins.
- Shared Node installer: `npx @yaaif/platform-mcp@1.3.0 --install --client claude` (optional `--plugin-src` / `--offline`).
- Enable-time `userConfig` for `YAAIF_*` profile, OIDC, API URLs, tenant, CA, and mTLS; values are injected into `.mcp.json` as `${user_config.*}`.
- Short slash-command aliases matching Cursor names (`/yaaif-platform:yaaif-login`, `:yaaif-plan`, `:yaaif-sync-scenario`, and the rest of the Cursor command set).
- Scenario skill: `/yaaif-platform:yaaif-sync-scenario` shortcut and observe-by-default catalog ground rule.
- Inventory + skill-sync CI against `cursor-plugin` (IDE-token substitutions only).
- Logo at `assets/logo.svg` (marketplace / README).

## 0.1.0

- Initial Claude Code plugin: nine skills, `.mcp.json` via `npx @yaaif/platform-mcp --client claude`, isolated `~/.yaaif/claude` state.
