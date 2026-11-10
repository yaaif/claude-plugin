# Changelog

## 1.7.0

- Align with platform 1.7.0 and support matching-source npx installation with optional archive verification.
- Add isolated multi-server sessions, endpoint-only profile cloning, and safe cross-server Scenario draft copy.
- Remove older version caches after verified updates and move them to per-client backups.
- Restore previous managed sources and launcher configuration after failed updates.
- Add side-effect-free dry-run install and update plans.
- Add portable profile bundles with secret-safe validation and conflict-protected imports.
- Add safe complete skill-pack copying with ID remapping and secret-file exclusion.
- Add sanitized ambient workflow copying with disabled-for-review installation.
- Add secret-free MCP server connection copying with non-secret header mappings and explicit credential rebinding.
- Add agent-definition migration with disabled-for-review creation and explicit skill remapping.
- Add unified dry-run-first catalog migration with dependency ordering and conflict aborts.
- Add secret-free MCP server connection copying with non-secret header mappings and explicit credential rebinding.

## 1.4.0

- Synchronize all Cursor canonical skills, including product docs, file workflows, Wiki inspection, and platform-update inspection.
- Add credential-profile guidance, Scenario sync preview/apply guidance, and `yaaif_features` backend capability checks; align with bridge 1.4.0.

## 1.3.2

- Align plugin version with platform 1.3.2.

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
