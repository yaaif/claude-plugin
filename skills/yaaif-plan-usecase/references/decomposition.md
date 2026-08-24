# Use-case decomposition

Decide which YAA\F components a use case needs. Prefer the smallest set that
covers the outcome. Prefer **reuse** from `yaaif_catalog_overview` when an
existing agent, skill, MCP tool, or workflow already matches.

## Decision matrix

| Signal | Include |
|--------|---------|
| User asks questions / triages in chat; short MCP calls | **Chat skill** + chat agent (`agent_type: skills`) |
| Chat should start a long-running / multi-step process | **Chat orchestration skill** (`list_ambient_workflows` + `trigger_ambient_workflow`) + **ambient workflow** + workflow agent |
| Schedule, webhook, batch, or always-on processing | **Ambient workflow** (+ ambient agent + workflow agent) |
| Mid/late human gate | Ambient pattern **Linear + approval** (or branching with approval) |
| Batch detect then later clearance | Ambient pattern **Recon / resolve** (often two graphs) |
| Multi-route decisions in automation | Ambient pattern **Branching** |
| Single automated path | Ambient pattern **Linear** (default) |
| SAP GUI / local OS UI on a desktop worker | **Desktop skill** (`classification: desktop`) + desktop agent (`agent_type: desktop`) + **worker mapping** |
| Domain APIs not in MCP catalog | **MCP tools** first (`yaaif-create-mcp`), then skills/workflows that call them |
| Ambient graph has `approval` / HITL gate | **Approval strategy** (`yaaif_approval_strategy_create` + publish) before workflow install |
| Shared identity / formatting every chat turn | **Base / always-active** chat skill (rare; only if clearly needed) |
| Graph step needs dedicated LLM skill | **Ambient step skill** (`classification: ambient`) |

## Defaults (no open choices)

1. **Interactive-only + existing MCP tools** → chat skill + chat agent only. No ambient.
2. **Chat starts long-running work** → chat orchestration skill + one ambient graph + workflow agent + chat agent.
3. **Batch / schedule / HITL without chat** → ambient only (workflow + ambient agents). Add a chat skill only if operators need chat trigger or status.
4. **SAP GUI / local UI** → desktop skill + desktop agent + `yaaif_desktop_skill_mapping_set` after `yaaif_desktop_workers_list`.
5. **HITL ambient** → create/publish approval strategy; put `approval_strategy_id` on approval nodes.
6. **Missing APIs** → plan MCP tools before ambient/chat that depend on them.
7. **Overlap with catalog** → mark component as **reuse** with existing id/name; do not create duplicates.

## Agent types

| `agent_type` | Role |
|--------------|------|
| `skills` (default) | Chat agent that loads mapped chat skills |
| `workflow` | Host agent referenced by ambient agent configs |
| `desktop` | Home for desktop-classified skills |

Ambient install order (when ambient is in scope):

1. Workflow agent (`agent_type: workflow`)
2. Ambient agent (`yaaif_ambient_agent_create`, `agent_id` = workflow agent)
3. Ambient workflow graph + triggers
4. Optional chat orchestration skill mapped to a chat agent

## Skill classifications

| Classification | Use |
|----------------|-----|
| omitted / `general` | Normal chat routing |
| `desktop` | Desktop worker skills (+ `desktop_platforms` when SAP GUI) |
| `ambient` | Ambient step skills (path often under `…/ambient/…`) |

## Ambient graph authoring

When an ambient workflow is in scope, author a **step-only** `workflow_graph` (see `yaaif-create-ambient` patterns). Canvas category labels:

| Category | Types |
|----------|--------|
| ACTION | `tool_call`, `action`, `skill` |
| MESSAGE | `send_email` |
| BRANCH | `if`, `switch`, `merge` |
| WAIT | `wait` |
| HUMAN | `approval` (HITL, pauses), `hotl` (notifies and continues) |
| TERMINAL | `do_nothing`, `error` |

Engine phases (watcher / evaluator / guardian / orchestrator / recorder) are settings, not canvas steps. Do not put them on new graphs. Do not convert a skill-flow-only orchestrator into a `skill` node.

## Anti-patterns

- Ambient graph for a one-shot chat Q&A
- Chat skill that embeds a full multi-step batch job instead of triggering ambient
- Inventing MCP tool names not in the catalog
- Creating a new agent when an existing one with the right type already fits
- Using `yaaif_skill_map_agents` (replace) when `yaaif_skill_map_agents_merge` is safer
- Approval nodes without a published `approval_strategy_id`
- Desktop skills without worker mappings when workers are known
- Authoring watcher / evaluator / guardian / orchestrator / recorder (W→E→G→O→R) as the process
- Converting a skill-flow-only orchestrator into a `skill` node
