---
name: yaaif-kg-skill-plan
description: Propose an ordered skill-authoring plan grounded in the Context Store knowledge graph and hand chosen steps to skill authoring. Use when the user asks which skills to build from the catalog or wants a plan from the Entity Graph. Not for applying graph enrichments (use yaaif-kg-enhance).
---

Call every Context Store tool through `yaaif_local_tool_call` with `name` set to the tool and the tool's fields under `arguments`. Surface tool errors verbatim and never simulate a result. If a `context_kg_*` call fails because the tool is unavailable, stop and say Context Store tools are not mounted on agent-service.

## Goal

Produce a 2-8 step plan of new `SKILL.md` packs that fulfils the user's intent, each step grounded in existing catalog IDs. Never write `skill:` nodes into the graph and never call `context_kg_propose_enrichments` or `context_kg_apply_enrichments`.

Copy IDs from tool output (`object_type:`, `mcp_tool:`, `mcp_server:`, `dimension:`, `metric:`, optional `concept:`). Never invent IDs.

## Flow

1. If the intent is not in the request, ask one short question for it (and optional scope or seed node ID).
2. Scan with `context_kg_get_snapshot`, `context_kg_get_data_model`, `context_kg_get_mcp_metadata`, then `context_graph_search`, `context_graph_neighbors`, `context_graph_query` to find anchors that match the intent. Gaps with catalog tools or types but no skill become plan steps. If an existing skill already covers a gap, say so instead of proposing a duplicate.
3. Call `context_kg_propose_skill_plan` with `intent`, `summary`, and `steps[]`, each with `step_id`, `proposed_skill_id`, `title`, `summary`, `node_ids` (at least one existing ID), and optional `suggested_tools` and `rationale`. `proposed_skill_id` must be path-like under `tenant/` or `yaaif/` with lowercase hyphen or slash segments, unique in the plan, and never a bare name. If the tool rejects unknown `node_ids`, fix them from tool results.
4. Present the stored plan as a short table: step, proposed skill ID, summary, node IDs. Use `context_kg_get_skill_plan` to re-read it.
5. Ask which steps to draft or whether to revise. For a revision, re-run `context_kg_propose_skill_plan`. For a chosen step, use `context_kg_skill_plan_step_brief` to get its brief and continue with the `yaaif-create-skill` skill.

Keep replies short.
