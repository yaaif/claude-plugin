---
name: yaaif-login
description: Select YAA\F platform profile, authenticate, and select a tenant
---

Use the `yaaif-auth` skill.

1. Optional: `yaaif_platform_use` (`hosted` | `local-hybrid` | `local` | custom).
2. Prefer `yaaif_ensure_session` with `login_if_needed: true` (optional `profile_id` / `tenant`).
3. If `needs_tenant_selection`, call `yaaif_set_tenant` with name, slug, or uuid.
4. Confirm with `yaaif_whoami` (profile + email + tenant name/id).
