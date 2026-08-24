---
name: yaaif-doctor
description: >-
  Run YAA\F Claude Code connectivity diagnostics (platform profile, OIDC, TLS/mTLS,
  auth/tenant, catalog ping, local tools API). Use when login fails, local
  Traefik TLS breaks, or before plan/create work.
---

# YAA\F Doctor

```
Task Progress:
- [ ] 1. Call yaaif_doctor
- [ ] 2. Fix reported failures
- [ ] 3. Re-run until ready
```

## Steps

1. Call `yaaif_doctor` (optionally `login_if_needed: true`).
2. If profile/OIDC wrong: `yaaif_platform_use` then doctor again.
3. If TLS/CA errors on `.local`: doctor auto-loads (and merges) mkcert `rootCA.pem` for `local` / `local-hybrid`. If `ca_source` is `none`, run `mkcert -install` or set `YAAIF_EXTRA_CA_FILE` / profile `extra_ca_file` (see docs/configure-environment.md). Ensure `yaaif_platform_use` saved `local-hybrid` (active-profile.json wins over plugin var `hosted`) and reload the YAA\F MCP after rebuilding.
4. If not authenticated: `yaaif_ensure_session` or `yaaif_login` / `yaaif_login_device`.
5. Confirm with `yaaif_whoami`.
6. If `local_tools` fails: ensure agent-service exposes `/api/local-tools` and
   the session has `agent.skills.read` (restart agent-service after upgrade).
7. If `local_tools_files` / `local_tools_files_smoke` / `file_artifacts_api` / `file_registry*` fail: upgrade
   agent-service for ADK artifacts (`load_artifacts`, `/api/files/artifacts/versions`,
   registry lifecycle). Reload the YAA\F MCP after rebuilding the plugin.

## Done when

`yaaif_doctor` returns `ready: true` with all checks ok (including `local_tools`,
`local_tools_files`, `local_tools_files_smoke`, and file registry/artifacts when the
platform supports them).
