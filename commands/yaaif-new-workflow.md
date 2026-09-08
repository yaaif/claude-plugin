---
name: yaaif-new-workflow
description: Create an ambient workflow on YAA\F and test-trigger it
---

Use the `yaaif-create-ambient` skill. Ensure auth and domain MCP tools first.

If the prompt includes `workflow_id`, stay in Claude Code (do not open Admin UI URLs)
and maintain that workflow with `yaaif_ambient_workflow_get` /
`yaaif_ambient_workflow_update`. Otherwise create workflow agent → ambient
agent → **step-only** workflow graph (ACTION / MESSAGE / BRANCH / WAIT / HUMAN /
TERMINAL — not watcher / evaluator / guardian / orchestrator / recorder) →
test-trigger.
