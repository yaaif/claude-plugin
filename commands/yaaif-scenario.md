---
name: yaaif-scenario
description: Create or maintain a YAA\F scenario (Agent Spec)
---

Use the `yaaif-scenario` skill. Authenticate first if needed (`yaaif-login` /
`yaaif-auth`).

If the prompt includes `spec_id`, stay in Claude Code (do not open Admin UI URLs).
Load that Scenario with `yaaif_agent_spec_get` and treat it as the selected
system of record. Maintain segments, slots, bindings, and `workflow_design`
through the spec. After spec design edits, preview then apply with
`yaaif_agent_spec_sync_preview` (`to_objects`) and `yaaif_agent_spec_sync_apply`.
Adopt live catalog changes only with `yaaif_agent_spec_sync_preview`
(`from_objects`) then `yaaif_agent_spec_sync_apply` (explicit; not the default
finish step).

If there is no `spec_id`, list existing scenarios, reuse a match, or create one
with `yaaif_agent_spec_create`. For a full chat + ambient + desktop use case,
prefer `/yaaif-platform:yaaif-plan` and create the spec immediately after approval.
