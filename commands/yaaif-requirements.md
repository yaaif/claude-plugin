---
name: yaaif-requirements
description: Write requirement analysis, FS, TS, and an estimate for a scenario
---

Use the `yaaif-requirements` skill. Authenticate first if needed (`yaaif-login` /
`yaaif-auth`).

If the prompt includes `spec_id`, stay in Claude Code (do not open Admin UI URLs).
Load that Scenario with `yaaif_agent_spec_get`. Draft a requirement analysis,
functional specification, technical specification, and an estimate with
timeline. Wait for confirmation, then store each with `yaaif_agent_spec_file_put`
and upsert `REQ-*` rows with `yaaif_agent_spec_upsert_requirement`.

If there is no `spec_id`, list existing scenarios, reuse a match, or create one
with `yaaif_agent_spec_create` before writing the documents.
