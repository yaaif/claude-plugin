---
name: yaaif-sync-scenario
description: Apply a YAA\F Scenario onto catalog objects, or explicitly adopt live catalog drift
---

Use the `yaaif-scenario` skill in **sync** mode. Authenticate first if needed
(`yaaif-login` / `yaaif-auth`).

Resolve `spec_id` from the prompt, or `yaaif_agent_spec_list` / the last
selected scenario.

- **Apply** (default; after editing `workflow_design` or slot names on the spec):
  `yaaif_agent_spec_sync_preview` `to_objects`, then `yaaif_agent_spec_sync_apply`.
- **Adopt** (explicit; overwrites Scenario-owned names/graphs from live objects):
  `yaaif_agent_spec_sync_preview` `from_objects`, then `yaaif_agent_spec_sync_apply`.

Preview, then apply. Finish with `yaaif_agent_spec_readiness` and
`yaaif_agent_spec_coverage`. Stay in Claude Code; do not open Admin UI URLs.
