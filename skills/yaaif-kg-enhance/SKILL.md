---
name: yaaif-kg-enhance
description: Enhance the Context Store knowledge graph by discovering missing relationships between existing catalog nodes, proposing them for approval, and applying approved batches. Use when the user asks to enhance, enrich, or find missing links in the Entity Graph. Not for skill-authoring plans (use yaaif-kg-skill-plan).
---

Call every Context Store tool through `yaaif_local_tool_call` with `name` set to the tool and the tool's fields under `arguments`. Surface tool errors verbatim and never simulate a result. If a `context_kg_*` call fails because the tool is unavailable, stop and say Context Store tools are not mounted on agent-service (CONTEXT_STORE_BASE_URL and the Context Store plugin must be active).

## Goal

Find new relationships between existing catalog IDs (`object_type:`, `mcp_tool:`, `mcp_server:`, `dimension:`, `metric:`) and add them as AI enrichment edges after the user approves. Never propose `skill:` nodes. Optional `concept:` nodes are allowed only when they label a discovered relationship, each needs at least one bridge triple to an existing catalog ID (`APPLIES_TO`, `ENABLES_OBJECT_TYPE`, `USES_TOOL`, `USES_SERVER`, `USES_FIELD`), and at most 3 per proposal. Prefer triples only.

Copy node IDs from tool output (`node_id`). Never invent IDs or plant/demo codes. Preferred predicates: `REFERENCES`, `READS_OBJECT_TYPE`, `WRITES_OBJECT_TYPE`, `BELONGS_TO_SERVER`, `HAS_DIMENSION`, `HAS_METRIC`, `RELATED_TO`. Every triple endpoint must already exist in the graph. Tag AI edges with `source: ai_enrichment` and a short rationale in metadata.

## Start

Ask once for `enrichment_mode` (`durable` survives Rebuild, `ephemeral` is wiped on the next Rebuild), default `durable`, and an optional scope (type, MCP server, field). Then start scanning with no further confirmation. Pass `enrichment_mode` to propose and apply.

## Phases

Call `context_kg_set_run_phase` on entering each phase so the Entity Graph page shows progress.

1. `scanning`: read `context_kg_get_data_model`, `context_kg_get_mcp_metadata`, `context_kg_get_type_navigation`, `context_kg_get_snapshot`, and use `context_graph_search`, `context_graph_neighbors`, `context_graph_query`, `context_graph_path` as needed. Look for FK-like fields without `REFERENCES`, tools without object-type edges, and types that share keys but lack navigation. Report real counts and 2-5 candidate gaps (subject, predicate, object).
2. `proposing`: call `context_kg_propose_enrichments` with the triples and a summary. Read `floating_ai_node_count`, `catalog_bridge_count`, and skill-node counts from the response. If `floating_ai_node_count > 0`, any `skill:` node appears, or unknown IDs were rejected, revise and re-propose. Do not ask for approval on an invalid proposal.
3. `awaiting_approval`: set the phase, show the proposal as a short list with the counts, and ask the user to approve, narrow the scope, or cancel. Stop and wait. On cancel set `done`.
4. `applying`: only after explicit approval, call `context_kg_apply_enrichments` with the `proposal_id` in batches of at most 25 nodes or triples. Summarize after each batch and continue while `remaining_*` is above 0.
5. `verifying`: call `context_kg_get_enrichment_diff`, summarize new edges, confirm floating and skill AI node counts are 0, set `done`, and tell the user to refresh the Entity Graph page.

## Rules

Additive only; never delete platform seed edges. Never claim completion without an apply after approval. Keep replies short: phase, bullets, next action.
