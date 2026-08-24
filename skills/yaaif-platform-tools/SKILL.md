---
name: yaaif-platform-tools
description: >-
  Discover and correctly use YAA\F agent-service built-in local tools (skill
  lifecycle, files, ambient trigger, session/workflow state) when authoring
  skills or exercising platform functions from Claude Code.
---

# Discover and use YAA\F platform local tools

```
Task Progress:
- [ ] 1. Auth + doctor (local_tools check)
- [ ] 2. List / filter local tools
- [ ] 3. Resolve schemas for SKILL.md tools:
- [ ] 4. Call lifecycle / files / ambient tools as needed
- [ ] 5. Document exact names in skill frontmatter
```

## Prerequisites

1. `yaaif-auth`
2. Prefer `yaaif_doctor` — confirm `local_tools` check passes

## Discovery

1. `yaaif_local_tools_catalog_overview` — family counts + recommended authoring tools
2. `yaaif_local_tools_list` with `family` (`skill` | `files` | `ambient` | `state` | `approval` | …) and optional `q`
3. `yaaif_local_tool_get` for full `input_schema` before calling

Read [references/local-tools.md](references/local-tools.md) for family ↔ REST parity.

## Authoring rules

- Every name in skill frontmatter `tools:` / `allowed-tools` must exist in **local tools** or **external MCP catalog** (`yaaif_mcp_tools_list` / `yaaif_skill_mcp_tool_catalog`)
- Chat→ambient skills must include exact locals: `list_ambient_workflows`, `trigger_ambient_workflow`
- Prefer platform lifecycle locals over raw REST file write when available:
  - `skill_create_guided_draft` / `yaaif_skill_guided_draft`
  - `yaaif_skill_update_module_files` / `yaaif_skill_edit_section` / `yaaif_skill_develop`
  - `skill_validate_module` / `yaaif_skill_validate_module`
  - `skill_tool_link_manager` + `skill_mcp_tool_catalog`
- Always run `yaaif_skill_tools_check` before enabling/mapping a new skill
- File-aware skills: call `yaaif_dev_session_ensure` then `files_list` / `load_artifacts` / `file_load_context` / `file_share_link`
  (artifact names + optional `version`; use `yaaif_file_artifact_versions` for version history)
- High-impact tools (`skill_archive_or_delete`, `skill_repo_ops`, `skill_release_manager`, …) require `allow_mutating: true` on `yaaif_local_tool_call`

## Invoke

Generic: `yaaif_local_tool_call` with `name`, `arguments`, optional `session_id` / `agent_id` / `branch`.

Aliases: `yaaif_skill_validate_module`, `yaaif_skill_develop`, `yaaif_skill_guided_draft`, `yaaif_skill_mcp_tool_catalog`, `yaaif_files_list`, `yaaif_files_search`, `yaaif_file_load_context`, `yaaif_load_artifacts`, `yaaif_file_share_link`, `yaaif_generate_file`.

See [docs/file-artifacts.md](../../docs/file-artifacts.md).
## Hand-off

Report the local tool names confirmed for the skill, any validation result, and whether a dev session was created.
