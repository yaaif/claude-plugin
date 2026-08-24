# Example plan: chat → ambient

Use when chat triages and then starts a long-running ambient workflow (optional HITL).

```markdown
# YAA\F use-case plan: Invoice clearance

- **Slug:** invoice-clearance
- **Status:** proposed

## 1. Use case summary

Chat collects invoice id, then triggers an ambient clearance graph with a finance approval gate.

## 2. Intent capture

| Field | Value |
|-------|-------|
| Outcome | Invoice cleared or rejected with audit trail |
| Triggers | chat + ambient |
| Sync vs async | chat sync; clearance async |
| HITL | yes — finance approver email |
| Systems | invoice MCP tools |
| Desktop GUI | no |

## 4. Components

- MCP: create/link invoice tools if missing
- Agents: chat (skills) + workflow
- Ambient: Linear + approval (chat-triggered). Step-only graph: ACTION (`tool_call` / `action`) → optional BRANCH (`if`) → HUMAN (`approval`) → TERMINAL (`do_nothing`). Do not author watcher / evaluator / guardian / orchestrator / recorder.
- Approval strategy: create WORKFLOW_PAUSE, publish, wire approval_strategy_id on the `approval` node
- Skills: orchestration chat skill with list_ambient_workflows + trigger_ambient_workflow

## 6. Install order

1. MCP deploy/register (if needed)
2. Create workflow + chat agents
3. Approval strategy create+publish
4. Ambient agent + workflow (approval node uses strategy id)
5. Chat orchestration skill
6. yaaif_skill_map_agents_merge → chat agent
7. yaaif_plan_dry_run (optional) then yaaif_plan_verify + test-trigger
```
