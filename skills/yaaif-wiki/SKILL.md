---
name: yaaif-wiki
description: >-
  Search and explain the tenant Wiki and Common Wiki, inspect page provenance,
  review proposals, and inspect rebuild previews/runs without modifying knowledge.
---

# Inspect YAA\F Wiki knowledge

```
Task Progress:
- [ ] 1. Auth + tenant
- [ ] 2. Search or inspect graph/proposals/rebuilds
- [ ] 3. Read supporting pages and sources
- [ ] 4. Answer with citations and current status
```

## Rules

- This workflow is **read-only**. Do not create/edit/merge/verify pages, approve/reject proposals, start/cancel rebuilds, or change settings. Use Admin UI for those actions.
- Wiki reads require `agent.memory.read` and remain subject to page visibility and the caller's data-class clearance.
- Distinguish `common` (independently supported common knowledge), `shared` (tenant-visible), and `mine` (the current user's pages). Never imply that a page is common merely because it is shared.
- Cite page slugs, versions and returned source references. Do not invent provenance or treat a rebuild preview as a running job.

## Search and read

First call `yaaif_features`. If `wiki` is `permission_denied`, request `agent.memory.read`; if `unavailable`, upgrade api-server instead of retrying Wiki calls.

1. `yaaif_wiki_pages_list` with `q`, optional `type`, `status`, `scope`, `min_confidence`, `sort`, `limit`, and `offset`.
2. `yaaif_wiki_page_get` for backlinks, outgoing links, sources and versions.
3. `yaaif_wiki_graph` for relationship context (`center`, `hops`, `rel`, `skills`, `scope`).
4. `yaaif_wiki_common_status` when the question is about Common Wiki coverage or distillation.

## Review and rebuild inspection

- `yaaif_wiki_proposals_list` / `yaaif_wiki_proposal_get`: inspect proposed and current text; do not decide the proposal.
- `yaaif_wiki_rebuild_preview`: explain what a rebuild would do; it does not start one.
- `yaaif_wiki_rebuild_latest`, `yaaif_wiki_rebuild_runs_list`, `yaaif_wiki_rebuild_get`: report run status and activity without cancelling.

OpenCode exposes only page search/get, graph, and Common status to preserve its tool budget. Other specialized inspection remains available in the other IDE bridges and through `yaaif tools call` / `yaaif wiki …`.

## Done when

The answer identifies the pages/graph/run used, distinguishes facts from proposals or previews, and leaves all knowledge and jobs unchanged.
