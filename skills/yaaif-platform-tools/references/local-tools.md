# Platform local tools reference

Built-in tools live in agent-service (`internal/mcp/local_tools.go`). The bridge discovers them via `GET /api/local-tools` (`yaaif_local_tools_list`).

## Families

| Family | Examples | Session? |
|--------|----------|----------|
| skill | `skill_create_guided_draft`, `skill_get_module_bundle`, `skill_update_module_files`, `skill_validate_module`, `skill_develop`, `skill_edit_section`, `skill_search`, `skill_mcp_tool_catalog`, `skill_tool_link_manager`, `skill_mapping_manager` | No (workspace resolved server-side) |
| files | `files_list`, `files_search`, `file_load_context`, `load_artifacts`, `file_share_link`, `generate_file` | Yes — use `yaaif_dev_session_ensure` |
| ambient | `list_ambient_workflows`, `trigger_ambient_workflow`, `ambient_approval_*` | No |
| approval | `yaaif_approval_inbox_*`, `yaaif_approval_task_*` | No |
| state | `session_state_*`, `workflow_state_*` | Yes |
| memory | `memory_*`, `agent_memory_*` (feature-flagged) | Yes |
| context_store | `context_store_*` (license-gated) | Varies |
| client | `get_client_context` | No |

## MCP REST vs local tools

| Goal | Prefer |
|------|--------|
| Browse catalog / enable / map agents | MCP REST: `yaaif_skill_*`, `yaaif_agent_*` |
| Author / validate module on disk | Local: `skill_*` via `yaaif_local_tool_call` |
| List ambient graphs for install | Either REST `yaaif_ambient_workflow_list` or local `list_ambient_workflows` |
| Trigger ambient from a chat skill | Local name in frontmatter: `trigger_ambient_workflow` |
| Approval strategy CRUD | MCP REST `yaaif_approval_strategy_*` |
| Approval inbox decide at runtime | Local `yaaif_approval_*` or Claude Code ambient/approval ops tools |

## Mutating ack

These require `allow_mutating: true` on `yaaif_local_tool_call`:

- `skill_archive_or_delete`
- `skill_repo_ops`
- `skill_release_manager`
- `ambient_approval_delete`
- `session_state_delete`

## Frontmatter example

```yaml
tools:
  - list_ambient_workflows
  - trigger_ambient_workflow
  - files_list
  - file_load_context
  - load_artifacts
```

## ADK artifacts

Ingested files are addressable by durable `file_id` **or** ADK artifact name
(`report.pdf`, `user:profile.json`) with an incrementing `artifact_version`.

- Prefer `load_artifacts` when referring to files by human-readable name/version
- `file_load_context` accepts the same dual reference (`file_id` or filename + optional `version`)
- MCP REST helpers (outside local tools): `yaaif_file_artifact_versions`,
  `yaaif_file_get_extracted`, `yaaif_session_files_list` (`latest_only=true`)
