---
name: yaaif-create-ambient
description: >-
  Design and install YAA\F ambient workflows via the Claude Code MCP bridge for
  customer/partner tenants (no monorepo required).
---

# Create ambient workflows on YAA\F

```
Task Progress:
- [ ] 1. Auth + tenant
- [ ] 2. Pick pattern
- [ ] 3. Ensure MCP tools exist
- [ ] 4. Workflow agent + ambient agent
- [ ] 5. Workflow graph + triggers
- [ ] 6. Optional chat skill
- [ ] 7. Test trigger
```

## Prerequisites

1. `yaaif-auth`
2. Domain MCP tools registered (`yaaif-create-mcp` or link)
3. Ambient feature enabled on the deployment

If Admin UI **Open in Claude Code** included `workflow_id`, stay in Claude Code — do not
open Admin UI URLs. Load `yaaif_ambient_workflow_get` and update that graph /
triggers. Do not create a second workflow with the same id.

## Patterns

See [references/patterns.md](references/patterns.md). Default to **Linear**.

Author **step-only** graphs (`tool_call` / `action` (Set Context) / `trigger_workflow` / `desktop_task` / `send_email` / `send_teams` / `notify` / `context_store` / `file_artifact` / `webhook_outbound` / `for_each` / `try` / `catch` / `if` / `approval` / `hotl` / `wait` / `do_nothing`, etc.). The designer canvas labels those as ACTION, MESSAGE, BRANCH, WAIT, HUMAN, TERMINAL. Do **not** add watcher / evaluator / guardian / orchestrator / recorder nodes — those are engine phases (settings), not canvas steps. `approval` pauses (HITL); `hotl` notifies and continues (HOTL).

### Step selection (orchestration)

| Need | Step | Notes |
|------|------|-------|
| Copy state only | `action` (Set Context) | Bindings into `context.*`; no external calls |
| External API / SAP / files | `tool_call` | MCP tool + credential profile |
| Start another ambient workflow | `trigger_workflow` | Prefer over MCP `trigger_ambient_workflow` in graphs; optional `wait_for_completion` + `fail_on_child_failure`; restrict targets with workflow `policy.allowed_child_workflow_ids` |
| Desktop automation | `desktop_task` | Explicit `skill_id` + `dispatch_mode` |
| Email | `send_email` | Mailbox + outbound credential |
| Teams notify | `send_teams` | Conversation ID or binding; `continue_on_error` default true |
| In-app user notify | `notify` | Platform user id or binding; Admin UI bell / notification bus; not Teams |
| Trivial IF/Switch | `if` / `switch` | Use `expression` (comparator) when no decision skill needed |
| Failure path | `error` | `fail_fast` (default) or `record_and_continue` |
| Structured try/catch | `try` / `catch` | Retry region + catch node (optional) |
| Context Store | `context_store` | CRUD/query/search_similar; or `tool_call` → `context_*` |
| Files / artifacts | `file_artifact` | load/list/search/share_link; or `tool_call` → `files_*` |
| Outbound webhook | `webhook_outbound` | HTTPS GET/POST/PUT/PATCH; `timeout_seconds`; optional `expected_status_codes`; response body on output (8KB cap); `policy.allowed_webhook_host_suffixes` (Policy tab); optional `credential_id` (kind `webhook-outbound`) — do not put bearer/HMAC secrets in context |
| Batch / loop | `for_each` | `mode` `child_workflow` (default) or `sequential` (`body_node_ids`, `checkpoint_every`); `wait_mode`; `max_concurrency`; `child_wait_timeout_seconds`; `fail_on_child_failure` waits until children are terminal; cap via `max_iterations` + policy `max_for_each_iterations` |
| Step retries | `retry_policy` on side-effect nodes | `tool_call`, `send_email`, `send_teams`, `notify`, `webhook_outbound`, `context_store`, `file_artifact` |

**Notify vs HOTL vs Send Teams:** `notify` → in-app bell (no run pause). `hotl` → approval-strategy channels, continues without pause. `send_teams` → Microsoft Teams conversation.

Tool Call workarounds remain valid for advanced context/file patterns. See monorepo `docs/operations/workflow-step-types.md` and example packs under `examples/workflow-packs/`.

External HTTP stays at **Tool Call → MCP** — do not expect a raw HTTP palette step.

## Install order

1. `yaaif_agent_create` with `agent_type: "workflow"`
2. If Linear+approval / HITL: `yaaif_approval_strategy_create` (`publish: true`) or reuse via `yaaif_approval_strategies_list`; set `approval_strategy_id` on approval nodes
2b. If Linear+HOTL (inform without blocking): reuse or create a published strategy; set `approval_strategy_id` on `hotl` nodes (optional `continue_on_error`, default true). Do **not** expect pause/resume — HOTL auto-closes after notify.
3. `yaaif_ambient_agent_create` (`mode: "active"`, async on)
4. `yaaif_ambient_workflow_create` with `workflow_graph` + `trigger_rules` — set workflow `policy.allowed_child_workflow_ids`, `policy.max_for_each_iterations`, and `policy.allowed_webhook_host_suffixes` in JSON or via Admin UI **Policy** tab when editing the graph
5. Optional chat skill via `yaaif-create-skill` including exact local tools
   `list_ambient_workflows` + `trigger_ambient_workflow` (confirm via
   `yaaif_local_tools_list` family `ambient`)
6. Optional smoke: `yaaif_local_tool_call` → `list_ambient_workflows`
7. `yaaif_ambient_test_trigger` → `yaaif_ambient_runs_list`
8. If this workflow belongs to a Scenario, pass `spec_id` + `slot_key` on
   create/update. After editing `workflow_design` on the spec, apply with
   `yaaif_agent_spec_sync_to_objects`. Do not finish with
   `yaaif_agent_spec_sync_from_objects` unless the user asks to adopt live
   catalog drift.

## Hand-off

Report workflow agent id, ambient agent id, workflow id, event/entity types, run ids.
