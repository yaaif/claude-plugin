---
name: yaaif-scenario
description: >-
  Create or maintain a YAA\F Scenario (Agent Spec): segments, architecture
  slots, bindings, workflow_design, coverage, and bidirectional catalog sync.
  Use when the user asks to create a spec/scenario, keep it in sync with live
  objects, sync objects from the spec, or Admin UI Open in Claude Code selected a
  spec_id.
---

# Create and maintain a YAA\F scenario

A **Scenario** is the Admin UI name for a platform **Agent Spec**. APIs and
tools stay `yaaif_agent_spec_*` / `/api/agent-specs`. The spec is the system of
record for spec-driven development. Claude Code plugin creates/updates bind with
`spec_id` + `slot_key` and the platform records those object changes back into
the spec (`catalog_objects`, slot names, `workflow_design`). Use explicit sync
when you need to pull or push the whole inventory.

```
Task Progress:
- [ ] 1. Auth + tenant
- [ ] 2. Select or create the scenario
- [ ] 3. Load spec + coverage
- [ ] 4. Apply create or maintain work through the spec
- [ ] 5. Sync spec ↔ objects, then coverage / optional adopt + publish
```

## Prerequisites

Run `yaaif-auth` first (`yaaif_ensure_session`, `login_if_needed: true`).
Confirm tenant with `yaaif_whoami`.

## Mode A — selected spec (Admin UI / Open in Claude Code)

When the prompt includes `spec_id` (and usually `slug` / `name`):

1. Stay in Claude Code. Do **not** open Admin UI or browser URLs for the scenario.
2. `yaaif_agent_spec_get` with that `spec_id` (id or slug).
3. `yaaif_agent_spec_readiness`, `yaaif_agent_spec_coverage` and, if useful, `yaaif_agent_spec_processing`.
4. Summarize: name, version, status, revision, mapped/drifted slots, readiness blockers, and `workflow_design`.
5. Ask what to change only if the request is vague. Otherwise apply the asked
   maintenance:
   - Every write includes the loaded `expected_version`. On `409`, reload and
     explicitly merge/reapply; never silently overwrite a concurrent edit.
   - Identity / story: `yaaif_agent_spec_update` or `yaaif_agent_spec_update_segment`
   - Requirements / architecture: `yaaif_agent_spec_upsert_requirement` and
     `yaaif_agent_spec_upsert_slot` (bulk replacement requires `replace_all`)
   - Bind reuse: `yaaif_agent_spec_bind` (`source` defaults to `agent_spec`)
   - New catalog objects: create via existing skills/tools **with** `spec_id` +
     `slot_key` so they bind automatically
   - Graphs: edit `workflow_design` (or create workflow with `spec_id` and omit
     `workflow_graph` to seed), then preview/apply a to-objects sync
   - After object-side edits, preview first with `yaaif_agent_spec_sync_preview`
     then explicitly apply with `yaaif_agent_spec_sync_apply`
   - Make this spec the inventory only through `yaaif_agent_spec_adoption_preview`
     then `yaaif_agent_spec_adopt`
   - Record passed evidence for every `must` requirement; refresh readiness,
     publish, then transition to `active`
6. Finish with `yaaif_agent_spec_readiness` + coverage. Do not create a second spec for the
   same slug.

## Mode B — create a new scenario

If there is no `spec_id`:

1. `yaaif_agent_spec_list` (`q` from the use-case name). Reuse if a match exists.
2. For a multi-capability use case, invoke the `yaaif-plan-usecase` skill and
   create the spec immediately after plan approval.
3. Otherwise create now with `yaaif_agent_spec_create`:
   - `slug` kebab-case, unique in the tenant
   - `name`, `description`
   - `segments` from the use-case story (overview, architecture, benefits; include
     `workflow_design` when ambient graphs are planned)
   - `slots` from the intended catalog objects (`kind` + `expected_name` +
     `slot_key`)
4. Store `spec_id`. Every later create (`yaaif_agent_create`,
   `yaaif_ambient_workflow_create`, `yaaif_skill_create`, MCP deploy, approval
   strategy) must pass `spec_id` + `slot_key`.
5. After creates, preview/apply catalog sync, attach verification evidence, and
   check readiness before publishing or activation.

## Mode C — sync spec ↔ objects

When the user asks to keep the scenario in sync, use this skill and:

1. Resolve `spec_id` (prompt, list, or last selected scenario).
2. `yaaif_agent_spec_get` + readiness + coverage.
3. Direction (always preview before applying):
   - **from objects** (default): live catalog → spec
     (`yaaif_agent_spec_sync_preview`, then `yaaif_agent_spec_sync_apply`). Use after Claude Code plugin changes to
     skills, agents, workflows, or MCP servers.
   - **to objects**: spec → live catalog
     (`yaaif_agent_spec_sync_preview`, then `yaaif_agent_spec_sync_apply`). Use after editing `workflow_design`
     or slot `expected_name`. Skill pack files are not overwritten.
4. Report updated slots, applied objects, skipped items, and remaining drift.

## Ground rules

- Prefer **reuse** of existing agents / skills / workflows / MCP tools; bind them.
- Never invent MCP or local tool names. Discover via catalog / local-tools first.
- Chat→ambient skills still need `list_ambient_workflows` and
  `trigger_ambient_workflow`.
- Do not hardcode tenant business copy into YAA\F core services; keep it in
  skills / MCP tools / this spec’s segments.
- Credentials stay on MCP server profiles, not skill-pack `credentials.yaml`.
