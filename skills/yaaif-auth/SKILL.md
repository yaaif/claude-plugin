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

Active profile is stored in `~/.yaaif/claude/active-profile.json`. Switching
issuer clears the local session (re-login required).

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
