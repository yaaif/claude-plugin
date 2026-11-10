---
name: yaaif-auth
description: >-
  Authenticate to YAA\F from Claude Code, select platform profile and tenant, and
  verify session before skills/MCP/ambient mutations. Use for YAA\F login,
  platform switch (hosted/local), tenant selection, whoami, ensure_session, or
  configure_check.
---

# YAA\F Auth

```
Task Progress:
- [ ] 1. Pick platform profile (if needed)
- [ ] 2. ensure_session / configure_check
- [ ] 3. Login if required
- [ ] 4. Select tenant if required
- [ ] 5. Confirm whoami
```

## Preferred path

1. If the user names an environment (`hosted`, `local`, `local-hybrid`, or a
   custom profile), call `yaaif_platform_use` with that `profile_id`.
2. Call **`yaaif_ensure_session`** with `login_if_needed: true` (and optional
   `tenant` name/slug/uuid, optional `profile_id`).
3. If the result has `needs_tenant_selection: true`, show `tenants` and call
   `yaaif_set_tenant` with a name, slug, or uuid.
4. Call `yaaif_whoami` and report **profile**, **email**, **tenant name + id**.
5. Before using optional feature families, call `yaaif_features` and distinguish backend support (`available` / `permission_denied`) from an older backend (`unavailable`) or a transport failure (`error`).

## Manual steps (when debugging)

1. `yaaif_platform_list` — see builtin + custom profiles
2. `yaaif_platform_use` / `yaaif_platform_save` — switch or save a customer env
3. `yaaif_configure_check` — OIDC discovery + health + issuer match
4. `yaaif_login` — browser PKCE (auto last/single tenant when possible)
5. `yaaif_list_tenants` — normalized list (`id`, `name`, `slug`, `is_last`)
6. `yaaif_set_tenant` — accepts **name / slug / uuid** (not uuid-only)
7. `yaaif_logout` — optional `end_session: true` for Keycloak logout

## Platform profiles

| Id | Meaning |
|----|---------|
| `hosted` | OIDC + APIs on `platform.yaaif.ai` |
| `local-hybrid` | OIDC `platform.yaaif.com`, APIs `platform.yaaif.local` |
| `local` | OIDC + APIs on `platform.yaaif.local` |
| custom | Saved via `yaaif_platform_save` |

Active profile is stored in `~/.yaaif/claude/active-profile.json`. Each profile has a separate session under `~/.yaaif/claude/profile-sessions/<profile-id>/session.json`. Switching profiles restores that server's existing login and tenant when present; it does not reuse another server's token.

## Multiple YAA\F servers

- `yaaif_platform_list` shows every profile with safe `authenticated` / tenant status only, never token values.
- `yaaif_platform_clone` duplicates endpoint and TLS settings into a new profile id, never the session. Login is required separately on the destination.
- `yaaif_platform_bundle_export` writes a portable configuration document without sessions. `yaaif_platform_bundle_import` previews conflicts and requires `confirm: true` with `dry_run: false`; it never overwrites existing profiles or copies tokens.
- `yaaif_scenario_copy` copies a Scenario as a **new draft** between `source_profile_id` and `destination_profile_id`. It previews by default and requires `confirm: true` with `dry_run: false` to write. Conflicting destination slugs never overwrite; choose `new_slug`.
- `yaaif_skill_copy` copies a complete skill pack with remapped files and frontmatter, excluding `.env`, `credentials.yaml`, and private-key files/content. It previews by default, requires confirmation, refuses destination conflicts, and does not copy agent mappings or Scenario bindings.
- `yaaif_ambient_workflow_copy` preserves graph logic while removing server-specific credentials, approval strategy ids, Scenario bindings and run history. It requires an existing destination ambient agent, previews by default, refuses name conflicts, and installs the workflow disabled with async execution and approval requirements off.
- `yaaif_mcp_server_copy` copies endpoint metadata and non-secret header mappings only. Credential ids, profiles, mappings, literal headers and tool refresh calls are excluded. Preview first, then confirm and rebind destination credentials explicitly.
- `yaaif_agent_copy` preserves prompt, description and agent type while excluding skill mappings, Scenario bindings and activation state. It previews by default, refuses name conflicts, and creates the destination disabled for review.
- `yaaif_catalog_copy` previews selected MCP servers, skills, agents, ambient agents, workflows and Scenarios together, aborts on any destination conflict, and applies in that dependency order without sessions, credentials, bindings or run history.
- Scenario copy excludes catalog bindings, release history, provenance, tenant ids, credentials and tokens. Recreate or rebind destination resources explicitly after review.

## Rules

- Prefer `yaaif_ensure_session` over ad-hoc login/tenant calls.
- Do not invent tokens or paste Keycloak secrets into chat.
- Do not use S2S / desktop / AI-gateway keys.
- Session file: `~/.yaaif/claude/session.json` (includes `profile_id` + `oidc_authority`).
- On `reauth_required` or `issuer_mismatch`, switch profile if needed and login again.
- Plugin variables still work; `YAAIF_PLATFORM_PROFILE` can force a builtin/custom id.

## Done when

`yaaif_whoami` (or `yaaif_ensure_session`) returns `authenticated`/`ready` with a
non-empty `tenant_id` and matching platform profile.
