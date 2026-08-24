# Ambient workflow patterns

Author **step-only** graphs. The Admin UI designer palette is ACTION / MESSAGE / BRANCH / WAIT / HUMAN / TERMINAL. Engine phases (watcher, evaluator, guardian, orchestrator, recorder) still load for legacy runs via migrate, but **do not author them** on new installs.

| Pattern | When | Shape |
|---------|------|--------|
| Linear | Single automated path | One step graph |
| Linear + approval | HITL gate | Graph with `approval` nodes + published `approval_strategy_id` |
| Linear + HOTL | Inform without blocking | Graph with `hotl` nodes + published `approval_strategy_id` (same strategy channels as approval; run does **not** pause) |
| Branching | Multi-route | `switch` / `if` |
| Recon / resolve | Batch detect then clearance | Often two graphs |
| Chat-triggered | Chat starts graph | Graph + chat skill with trigger tools |

## Canvas category labels

Use these types. The designer shows the category on the node chrome:

| Category | Node types | Role |
|----------|------------|------|
| ACTION | `tool_call`, `action`, `skill`, `trigger_workflow`, `desktop_task` | Call MCP, reshape context, dispatch child workflow or desktop skill |
| MESSAGE | `send_email`, `send_teams`, `notify` | Outbound email, Teams, or in-app user notification |
| BRANCH | `if`, `switch`, `merge` | Route or join paths |
| WAIT | `wait` | Timed or signal wait |
| HUMAN | `approval`, `hotl` | HITL pause vs HOTL notify-and-continue |
| TERMINAL | `do_nothing`, `error` | End the path or record failure |

HOTL vs HITL vs Notify vs Send Teams:

- `approval` (HITL) **pauses** the run until a decision.
- `hotl` **notifies** via approval-strategy channels and **continues**. Do not expect pause/resume.
- `notify` sends an **in-app** notification to a platform user (Admin UI bell). Does not pause.
- `send_teams` sends proactive Teams text or adaptive card. Does not pause.

## Minimal linear skeleton

Author steps only. Tool names in step configs must match the MCP catalog exactly.

```json
{
  "nodes": [
    {
      "id": "lookup",
      "type": "tool_call",
      "config": { "tool": "example_lookup", "arguments": {} }
    },
    {
      "id": "gate",
      "type": "if",
      "config": { "condition": "needs_review" }
    },
    {
      "id": "review",
      "type": "approval",
      "config": { "approval_strategy_id": "<published-strategy-id>" }
    },
    {
      "id": "apply",
      "type": "action",
      "config": { "tool": "example_apply", "arguments": {} }
    },
    {
      "id": "done",
      "type": "do_nothing",
      "config": {}
    }
  ],
  "edges": [
    { "from": "lookup", "to": "gate" },
    { "from": "gate", "to": "review", "condition": "true" },
    { "from": "gate", "to": "apply", "condition": "false" },
    { "from": "review", "to": "apply" },
    { "from": "apply", "to": "done" }
  ]
}
```

For Linear + HOTL, use `hotl` instead of `approval` on the human node. For Linear (no human), omit the HUMAN node and connect BRANCH (or the prior ACTION) straight to the next ACTION / TERMINAL.

## Anti-patterns

- Do **not** add watcher / evaluator / guardian / orchestrator / recorder nodes. Those are engine phases (settings), not canvas steps.
- Do **not** convert a skill-flow-only orchestrator into a `skill` node.
- Do **not** author a W→E→G→O→R spine and expect the designer to treat it as the process.
- Do not invent MCP tool names. Resolve them from the catalog first.
