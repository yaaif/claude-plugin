---
name: yaaif-plan-usecase
description: >-
  Understand a business use case, propose a YAA\F architecture plan (chat
  skills, ambient workflows, desktop skills, agents, MCP tools, mappings),
  wait for approval, then execute via yaaif-create-* skills and bridge tools.
  Supports interview mode, dry-run, plan verify, approval strategies, and
  desktop worker mappings. Use when the user describes a process to automate,
  asks how to split a solution across chat/ambient/desktop, or wants an
  end-to-end install plan.
---

# Plan and implement a YAA\F use case

Turn a use-case description into an **approved install plan**, then implement it
by delegating to existing plugin skills and `yaaif_*` bridge tools. Do not jump
straight to create tools before the plan is approved.

```
Task Progress:
- [ ] 1. Auth + catalog snapshot
- [ ] 2. Capture intent (interview if vague)
- [ ] 3. Decompose (chat / ambient / desktop / MCP / agents)
- [ ] 4. Write plan file + stop for approval
- [ ] 5. Optional dry-run (yaaif_plan_dry_run) with local_tool_names
- [ ] 6. Save execution checklist (yaaif_plan_execution_save); include yaaif_skill_tools_check before skill create
- [ ] 7. Execute (MCP → API key bind → agents → approvals → ambient → skills → map → desktop)
- [ ] 8. On failure: yaaif_plan_execution_resume and continue
- [ ] 9. Verify (yaaif_plan_verify including local_tool_names) + hand off
```

## Prerequisites

1. `yaaif-auth` (session + non-empty tenant)
2. Read [references/decomposition.md](references/decomposition.md)
3. Emit plans using [references/plan-template.md](references/plan-template.md)
4. Prefer examples in [references/examples/](references/examples/) when shapes match

## Phase A — Propose (always first)

### 1. Auth + catalog

- Ensure auth via `yaaif-auth`
- Call `yaaif_catalog_overview` (includes `local_tools` when reachable)
- Use targeted list tools when needed: `yaaif_agent_list`, `yaaif_skill_list`,
  `yaaif_mcp_tools_list`, `yaaif_ambient_workflow_list`,
  `yaaif_approval_strategies_list`, `yaaif_desktop_workers_list`,
  `yaaif_local_tools_list` (exact platform tool names for skill frontmatter)
- Prefer **reuse** of existing agents / skills / MCP tools / workflows when names
  or purposes clearly overlap
- For chat→ambient skills, resolve real local names via
  `list_ambient_workflows` / `trigger_ambient_workflow` (local tools), not invented aliases
- For file-heavy use cases, include `files_list` / `load_artifacts` / `file_load_context` (and note
  `yaaif_dev_session_ensure` for Claude Code authoring; artifact name + version dual identity)

### 2. Capture intent

If the use case is clear, extract fields and ask **at most one** clarifying
question for the biggest gap.

If the use case is **vague** (missing trigger, systems, or HITL), use
**interview mode** — ask these as a short structured list (one message), then
continue once answered:

1. Outcome — what should be true when done?
2. Triggers — chat / schedule / webhook / batch / manual?
3. HITL — any human approval gate? who approves (email)?
4. Systems — SAP OData, SAP GUI, custom APIs, none?
5. Desktop — local GUI / OS automation needed?
6. Chat role — triage only, or chat starts the long-running work?

Confirm in 1–2 sentences, then continue.

### 3. Decompose

Apply [references/decomposition.md](references/decomposition.md). Produce a
component list covering only what is needed:

| Component | When |
|-----------|------|
| MCP tools | Domain APIs missing from catalog |
| Chat agent (`agent_type: skills`) | Interactive chat skills |
| Workflow agent (`agent_type: workflow`) | Host for ambient |
| Desktop agent (`agent_type: desktop`) | Desktop skills need a home |
| Ambient agent + workflow | Async / batch / schedule / HITL graphs |
| Approval strategy | Ambient pattern Linear+approval (or any `approval` node) |
| Chat skill | Triage, Q&A, light tools |
| Chat orchestration skill | Chat → `trigger_ambient_workflow` |
| Desktop skill | SAP GUI / local UI (`classification: desktop`) |
| Desktop worker mapping | After desktop skill exists — map workers |
| Ambient step skill | Only when a graph step needs a dedicated skill |

State the ambient pattern briefly when ambient is in scope (Linear default;
see `yaaif-create-ambient` patterns).

### 4. Write plan + stop

1. Write `yaaif-plans/<slug>-plan.md` in the **user workspace** using the plan
   template (slug = short hyphen-case domain, e.g. `invoice-clearance`).
2. Summarize the plan in chat (components + install order).
3. **Stop.** Ask for explicit approval (`approve`, `go ahead`, or equivalent).
   Offer optional **`dry-run`** before mutate.
4. Do **not** call create/deploy/map/enable tools until the user approves
   (dry-run via `yaaif_plan_dry_run` is allowed — it does not mutate).
5. If the user requests changes, revise the plan file (or `yaaif_agent_update`
   after execute) and stop again.

### 5. Dry-run (optional / when user asks)

Build the intended tool call list from the plan and call `yaaif_plan_dry_run`
with `actions` (+ `verify_catalog: true` and `expected` names from the plan).
Show the dry-run result; wait again for execute approval if not already granted.

## Phase B — Execute (only after approval)

Immediately after approval, persist a platform **Scenario** (Agent Spec) with
`yaaif_agent_spec_create` (slug from the plan, segments from §1–§8 / §10,
architecture slots from §4). Store `spec_id` and the returned `version` as
`spec_version` on the local plan execution (`yaaif_plan_execution_save`). Every subsequent create tool must pass
`spec_id` + `slot_key` so agents, skills, workflows, and MCP servers bind
automatically. Those objects are created from the spec; later changes go
through the spec slot (and `workflow_design` for graphs), not as parallel
catalog edits. Use the `yaaif-scenario` skill / `yaaif_agent_spec_*` tools to
maintain the spec. Use `yaaif_agent_spec_bind` if a reused existing entity
needs mapping. After execute, preview catalog sync with
`yaaif_agent_spec_sync_preview`, explicitly apply it with the current version,
record passing evidence for every `must` requirement, refresh readiness, and
only then publish and transition to `active`. `yaaif_plan_execution_resume`
refreshes readiness/version and halts for conflicts or failed evidence. Later object edits in
Claude Code keeps the task on the spec automatically; invoke the `yaaif-scenario`
skill to pull or push the full inventory.

Before mutating, call `yaaif_plan_execution_save` with the ordered steps (status
`pending`). After each successful/failed step call
`yaaif_plan_execution_update_step`. If interrupted, call
`yaaif_plan_execution_resume` and continue from `next_step` using
`collected_ids` — do not recreate completed agents/skills/workflows.

Follow this order. Skip steps the plan marks as reuse / not needed.

1. **MCP** — If the plan lists missing tools, use `yaaif-create-mcp`. Preflight
   `yaaif_deployment_settings_status`, then create/deploy (compose or
   kubernetes_gitops). Verify with `yaaif_mcp_tools_list`. When the MCP calls
   platform APIs (context-store, approvals read, ambient HTTP, …), also
   `yaaif_api_key_create` + `yaaif_api_key_bind_deployment` (never platform S2S
   in MCP pods).
2. **Agents** — `yaaif_agent_create` for each planned agent with the correct
   `agent_type` (`skills` | `workflow` | `desktop`). Reuse existing ids when
   marked reuse. Use `yaaif_agent_update` to revise name/goal/`skill_ids` /
   enabled on existing agents (type is immutable).
3. **Approval strategies** — If the plan includes HITL / Linear+approval:
   - Prefer reuse via `yaaif_approval_strategies_list`
   - Else `yaaif_approval_strategy_create` with `approver_email`,
     `object_type: "WORKFLOW_PAUSE"`, `publish: true`
   - Put the returned `approval_strategy_id` into ambient approval node configs
4. **Ambient** — Use `yaaif-create-ambient` (workflow agent → ambient agent →
   workflow graph + triggers). Do not invent MCP tool names inside step configs.
5. **Skills** — Use `yaaif-create-skill` for each chat / orchestration / desktop
   / ambient-step skill. Chat→ambient skills **must** include
   `list_ambient_workflows` and `trigger_ambient_workflow`.
6. **Map skills → agents** — Prefer **`yaaif_skill_map_agents_merge`** (safe
   union). Only use `yaaif_skill_map_agents` when intentionally replacing the
   full list. Ensure skills are enabled.
7. **Desktop worker mappings** — For each desktop skill, if worker ids are known
   (from plan or `yaaif_desktop_workers_list`):
   `yaaif_desktop_skill_mapping_set` with `{ skill_id, worker_ids }`.
8. **Reload** — `yaaif_skill_refresh` and/or `yaaif_skill_runtime_reload` when
   skills changed.
9. **Verify** — `yaaif_plan_verify` with expected names/ids from the plan; then
   `yaaif_catalog_overview`. If ambient was created, optional
   `yaaif_ambient_test_trigger` → `yaaif_ambient_runs_list`.

Update the plan file's execution checklist with created ids as you go.

## Mapping rules

- Prefer `yaaif_skill_map_agents_merge` during plan execution.
- Chat skills map to chat (`skills`) agents.
- Desktop skills map to desktop agents; worker mappings via
  `yaaif_desktop_skill_mapping_*`.
- Ambient graphs use workflow + ambient agents; chat orchestration skills map to
  the chat agent that should trigger the workflow.

## Hand-off

Report:

- Plan path
- Created / reused ids (agents, ambient agents, workflows, skills, MCP tools,
  approval strategies, desktop mappings)
- Skill↔agent mapping summary
- `yaaif_plan_verify` result
- How to smoke-test (chat phrase and/or ambient test trigger)

## Ground rules

- Propose before mutate; never auto-execute without approval
- Dry-run is encouraged when the plan is large or HITL/desktop is involved
- Prefer reuse over duplicate skills/workflows/agents
- Interview mode when vague; otherwise one clarifying question max
- Use only real MCP catalog tool names
- Delegate implementation details to `yaaif-create-mcp`, `yaaif-create-ambient`,
  and `yaaif-create-skill` — this skill owns orchestration and sequencing
- No monorepo required; write plan + drafts in the user workspace
- Never use S2S, desktop connection keys, or AI-gateway keys
- For MCP → platform APIs use `yaaif_api_key_*` (scoped API keys), not S2S
