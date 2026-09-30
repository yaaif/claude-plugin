---
name: yaaif-requirements
description: >-
  Write a customer requirement analysis, functional specification, technical
  specification, and an estimate with timeline for a YAA\F Scenario, then store
  them as downloadable file-registry documents. Use when the user asks for a
  requirement analysis, FS, TS, functional spec, technical spec, estimate, or
  project timeline, or when Admin UI Open in Claude Code selected a spec_id for
  that work.
---

# Customer requirement documents

Produce four markdown documents for one Scenario and attach them so the
Scenario side panel can download them. The Claude Code plugin does not invent a
second spec store. Tools stay `yaaif_agent_spec_*`.

```
Task Progress:
- [ ] 1. Auth + tenant
- [ ] 2. Select or create the scenario
- [ ] 3. Read requirements, slots, and segments
- [ ] 4. Draft the four documents and wait for confirmation
- [ ] 5. Store each document and upsert REQ-* rows
```

## Prerequisites

Run `yaaif-auth` first (`yaaif_ensure_session`, `login_if_needed: true`).
Confirm tenant with `yaaif_whoami`.

If the prompt includes `spec_id`, stay in Claude Code. Do not open Admin UI URLs.
Load that Scenario with `yaaif_agent_spec_get`.

If there is no `spec_id`, call `yaaif_agent_spec_list`, reuse a match, or
create one with `yaaif_agent_spec_create` before writing documents.

## Documents

Write these kinds, in order. Each is markdown. The functional spec and
technical spec must cite the same totals as the estimate.

1. `requirement_analysis` — problem, actors, in-scope and out-of-scope work, assumptions, and acceptance criteria. Filename `requirement-analysis.md`.
2. `functional_spec` — behavior, business rules, exceptions, and a short pointer to the estimate totals. Filename `functional-spec.md`.
3. `technical_spec` — architecture, integrations, data, non-functionals, and the same estimate pointer. Filename `technical-spec.md`.
4. `estimate_timeline` — assumptions and exclusions, role-based person-days, a phased calendar, milestones, dependencies, and risks that move dates. Filename `estimate-timeline.md`.

Show the drafts to the user and wait for confirmation before storing them.

## Store

For each confirmed document call `yaaif_agent_spec_file_put` with `spec_id`,
`kind`, `title`, `filename`, and the full markdown `content`. A second put of
the same kind replaces the downloadable file.

Then upsert each requirement with `yaaif_agent_spec_upsert_requirement` so the
Requirements tab matches the analysis. Use `expected_version` from the latest
`yaaif_agent_spec_get`.

Confirm with `yaaif_agent_spec_files_list`. Tell the user the four documents
are on the Scenario overview for download.

Do not leave the documents only in chat. The file-registry link is the
customer copy.
