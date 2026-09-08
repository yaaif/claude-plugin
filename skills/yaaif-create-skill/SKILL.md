---
name: yaaif-create-skill
description: >-
  Author or maintain a YAA\F SKILL.md pack and load it into the tenant catalog
  via the yaaif Claude Code MCP bridge. Use when Admin UI Open in Claude Code / Create in
  Claude Code selected a skill_id, or when creating a new skill. Prefers platform
  local skill lifecycle tools when available.
---

# Create and load a YAA\F skill

```
Task Progress:
- [ ] 1. Auth + tenant
- [ ] 2. Capture intent + discover tools
- [ ] 3. Search existing / guided draft
- [ ] 4. Edit + validate module (local tools)
- [ ] 5. Enable + map agents (REST)
- [ ] 6. Refresh / runtime reload
```

## Prerequisites

Run `yaaif-auth` first. Optionally `yaaif_doctor` (confirm `local_tools`).
If the prompt includes `skill_id` from Admin UI, stay in Claude Code — do not open
Admin UI URLs. Load that skill and maintain it; do not create a second skill
with the same id.

## Maintain a selected skill

When `skill_id` is present:

1. `yaaif_skill_get` / `yaaif_skill_file_tree` / `yaaif_skill_read_file`
2. Edit with `yaaif_skill_update_module_files` / `yaaif_skill_edit_section` /
   `yaaif_skill_develop`
3. `yaaif_skill_tools_check` then `yaaif_skill_validate_module`
4. `yaaif_skill_map_agents_merge` if mapping changed
5. `yaaif_skill_refresh` then `yaaif_skill_runtime_reload`
6. If this skill is bound to a Scenario (`spec_id` in the prompt or a known
   slot), keep editing through the skill tools. Do not finish with
   `yaaif_agent_spec_sync_from_objects`; live skill-file edits become drift
   until someone explicitly adopts them.

## Authoring

Read [references/frontmatter.md](references/frontmatter.md). Prefer lean chat skills unless SAP GUI / ambient / always-active is required.

- `id` is the path relative to the tenant skills root (e.g. `domain/my-skill`)
- Final path segment must equal frontmatter `name`
- Use **real** tool names from local tools or MCP catalog only
- Chat→ambient skills must include `list_ambient_workflows` and `trigger_ambient_workflow`

### Preferred path (platform local tools)

1. Discover: `yaaif_local_tools_list` (`family: skill`) and/or `yaaif-platform-tools`
2. Search: `yaaif_local_tool_call` → `skill_search` / `skill_search_workspace`
3. Draft: `yaaif_skill_guided_draft` (or `skill_create_guided_draft`)
4. Edit: `yaaif_skill_update_module_files` / `yaaif_skill_edit_section` / `yaaif_skill_develop`
5. **Check tools:** `yaaif_skill_tools_check` with the draft markdown (or `tools[]`) — must pass
6. Link tools: `yaaif_skill_mcp_tool_catalog` + `skill_tool_link_manager`
7. Validate: `yaaif_skill_validate_module` (strict) — prefer over `yaaif_skill_validate`
8. Map: `yaaif_skill_map_agents_merge`
9. `yaaif_skill_refresh` then `yaaif_skill_runtime_reload`
10. If creating under a Scenario, pass `spec_id` + `slot_key` on
    `yaaif_skill_create`. Binding is enough; do not call
    `yaaif_agent_spec_sync_from_objects` as a default finish step.

### Fallback (REST only)

When local tools are unavailable (doctor `local_tools` failed):

1. `yaaif_skill_create` with `id`, `description`, `instruction`, `tools` / `allowed_tools`, `enabled: true`
2. Companions via `yaaif_skill_write_file`
3. Prefer `yaaif_skill_map_agents_merge`
4. `yaaif_skill_validate` (optional)
5. `yaaif_skill_refresh` then `yaaif_skill_runtime_reload`

## File-aware skills

Call `yaaif_dev_session_ensure`, then exercise `yaaif_files_list` / `yaaif_load_artifacts` / `yaaif_file_load_context` while drafting. Put `files_list` / `load_artifacts` / `file_load_context` (and `file_share_link` if needed) in frontmatter. Files may be referenced by durable `file_id` or ADK artifact name (+ optional `version`).

## Hand-off

Report skill id, validation result, enabled flag, mapped agent ids, and whether local lifecycle tools were used.
