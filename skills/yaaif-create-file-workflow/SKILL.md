---
name: yaaif-create-file-workflow
description: >-
  Create a custom file workflow on YAA\F via the Claude Code MCP bridge: an ambient
  workflow that runs when an uploaded file finishes extraction (file.ready /
  file.failed / file.review_decided), reads the extracted text or tables, runs
  your own tool steps and replies to where the file came from (chat, Teams,
  Lark, email).
---

# Create a file extraction workflow on YAA\F

Extraction itself runs in the platform worker and is not pluggable per agent. What you attach
is a **post-extraction workflow**: the platform publishes a file event, an ambient trigger rule
(source `file`) matches it, and your workflow runs **as the uploader**.

```
Task Progress:
- [ ] 1. Auth + tenant
- [ ] 2. Clarify event, scope, processing and reply
- [ ] 3. Ensure the tools your steps call exist
- [ ] 4. Ambient agent
- [ ] 5. Preview with yaaif_file_workflow_template
- [ ] 6. Install with yaaif_file_workflow_create
- [ ] 7. Test with a real upload, check the file timeline
```

## Prerequisites

1. `yaaif-auth`
2. Ambient feature enabled on the deployment
3. For custom processing steps: the MCP tool is registered (`yaaif-create-mcp` / `yaaif_mcp_tools_list`)

If Admin UI **Open in Claude Code** included `workflow_id`, stay in Claude Code: load
`yaaif_ambient_workflow_get` and update that graph with `yaaif_ambient_workflow_update`. Do not create a duplicate.

## 1. Clarify

Ask only what is missing:

| Question | Maps to |
|---|---|
| Which events? (default ready + failed) | `events`: `file.ready`, `file.failed`, `file.review_decided` |
| All uploads, one chat agent, one file type? | `agent_id` **or** `filter_contains` (substring of the payload: agent id, MIME type, file name fragment, channel) |
| Need the extracted text / tables in the workflow? | `load_content`, `load_tables` |
| What custom processing? | `steps[]`: `{tool_name, input: {arg: binding}, output_key}` |
| What should the user be told? | `message_binding` (default `signal.payload.summary`; use your step's `context.*` result to send it) |
| Reply at all? | `reply` (default true) |

Payload fields for bindings (`signal.payload.*`): `file_id`, `name`, `mime_type`, `status`, `run_id`,
`data_class`, `quality_score`, `extracted_chars`, `review_status`, `summary`, `error`,
`origin.channel|session_id|user_id|agent_id`. No file content is in the payload: read it with
`file_load_context` / `file_tables` (steps `load_content` / `load_tables`).

## 2. Ambient agent

Reuse one (`yaaif_ambient_agent_list`) or create it (`yaaif_ambient_agent_create`, `mode: "active"`).
It only **owns** the workflow; replies go to the uploader, not to this agent.

## 3. Preview, then install

1. `yaaif_file_workflow_template` with the options: returns the workflow bodies without installing anything.
2. Show the user the steps and the rule(s); adjust.
3. `yaaif_file_workflow_create` with `ambient_agent_id` and the same options (`dry_run: true` first if unsure).
   It creates one workflow + trigger rule per event.

Example (price lists from one agent, post to an ERP tool, tell the uploader the result):

```json
{
  "ambient_agent_id": "<ambient agent id>",
  "name": "Price list intake",
  "events": ["file.ready", "file.failed"],
  "agent_id": "<chat agent id>",
  "load_tables": true,
  "steps": [{
    "tool_name": "erp_post_price_changes",
    "input": { "file_id": "signal.payload.file_id", "tables": "context.file_tables" },
    "output_key": "context.erp_result"
  }],
  "message_binding": "context.erp_result"
}
```

Need branching, approval or a skill step? Install with this tool first, then extend the graph with
`yaaif_ambient_workflow_update` (see `yaaif-create-ambient` for step types: `switch` on
`signal.payload.data_class` or `quality_score`, `approval`, `skill`, `send_email`, …).

## 4. Test

1. Upload a matching file in chat (or Teams/Lark/email).
2. `yaaif_ambient_runs_list` → `yaaif_ambient_run_get` for the run started by `file.ready`.
3. Admin UI → Files → the file's **Processing timeline** shows every stage and the `deliver:<channel>` reply.

## Rules to remember

- Rules are **per tenant**; scope with `agent_id` / `filter_contains`. Rules with source `any` or `*` never receive file events.
- The built-in automatic chat summary is independent: turn it off (Admin UI → File handling →
  "Summarise new uploads automatically") if the workflow sends its own reply, or the user gets both.
- Email replies go to the original sender only, at most 3 per session per 10 minutes. Channels without a route are recorded as `skipped`.
- The workflow runs as the uploader: tools see only files that user can read.
- Reference: `agent-service/docs/file-workflows.md` and the pack `examples/workflow-packs/file-intake-workflow-pack/` in the YAAIF repository.
