---
name: yaaif-platform-updates
description: >-
  Inspect platform release status and approval-gated update jobs without
  checking, cancelling, or upgrading the installation.
---

# Inspect YAA\F platform updates

```
Task Progress:
- [ ] 1. Auth + tenant
- [ ] 2. Read current/active release status
- [ ] 3. Inspect relevant jobs and components
- [ ] 4. Report status and safe next action
```

## Rules

- Requires `api.installation.read`. A 403 is a permission issue, not proof that updates are unavailable. Call `yaaif_features` first: `permission_denied` means the route exists but access is missing; `unavailable` means api-server/update-service needs an upgrade.
- This workflow is **read-only**. Do not call platform update check/cancel endpoints and do not run `yaaifctl upgrade`, Helm upgrades, or container replacements.
- Release checks and cancellations require `installation.write`; upgrades remain approval-gated in Admin UI or the installer-managed operational flow.

## Inspect

1. `yaaif_platform_update_status`: report the update driver (`docker_compose` or `kubernetes`), installed version, last registry check, and any active job.
2. `yaaif_platform_update_jobs_list`: find recent target versions and statuses. Use a bounded `limit`.
3. `yaaif_platform_update_job_get`: inspect components, current/target images, approval instance, requester, errors and timestamps.

Explain `awaiting_approval`, active/non-terminal, and terminal states (`succeeded`, `failed`, `rejected`, `cancelled`) accurately. Do not infer that a release is deployed merely because a job was created or approved.

## Done when

The report distinguishes installed version from target version, names the active/relevant job and approval state, and leaves release checks, approvals, cancellations and upgrades to the authorized operational surface.
