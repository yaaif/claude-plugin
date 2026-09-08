---
name: yaaif-plan
description: Plan a YAA\F use case (chat + ambient + desktop), then execute after approval
---

Use the `yaaif-plan-usecase` skill. Authenticate first if needed (`yaaif-login` /
`yaaif-auth`). Capture the use case, write `yaaif-plans/<slug>-plan.md`, stop for
approval, then create a Scenario (`yaaif_agent_spec_create`) and execute via
`yaaif-create-mcp`, `yaaif-create-ambient`, `yaaif-create-skill`, agent create,
and skill mapping tools — each with `spec_id` + `slot_key`. Maintain later with
`/yaaif-platform:yaaif-scenario`.
