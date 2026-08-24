---
name: yaaif-ops-support
description: >-
  Strictly read-only operations support: analyze LLM sessions, ambient workflow
  runs, and desktop executions by ID; correlate those IDs; pull telemetry
  evidence; summarize failure reasons. Never pause/stop/approve/retry.
---

# YAA\F operations support (read-only)

```
Task Progress:
- [ ] 1. Auth + tenant
- [ ] 2. Collect seed ID(s)
- [ ] 3. yaaif_ops_analyze
- [ ] 4. Telemetry drill-down (yaaif_ops_telemetry)
- [ ] 5. Escalate with template
```

## Prerequisites

1. `yaaif-auth`
2. Prefer `yaaif_doctor` — confirm `ops_api` and `ops_telemetry` checks pass
3. Read [references/correlation.md](references/correlation.md)

## Hard rules (RO)

- Use only `yaaif_ops_*` tools (and read-only list/get tools).
- **Never** call `yaaif_ambient_run_pause`, `resume`, `stop`, `approve`, `reject`, retry, trigger, or mapping mutations.
- Do not invent remediation API calls.
- Prefer `summary_only` (default on analyze) and avoid `include_raw` unless the operator holds `ops.support.raw`.

## Flow (fixed order)

1. Ask for any of: `session_id`, `ambient_run_id`, `desktop_run_id`, `request_id` (one is enough).
2. Call **`yaaif_ops_analyze`** with the seed(s).
3. Note `partial_errors` (metrics/desktop/harness/`ops.support.raw`) but continue with available data.
4. Drill down with **`yaaif_ops_telemetry`** (preferred over per-resource aliases):
   1. `resource=insights` when `session_id` known
   2. `resource=flow_events` when `request_id` known
   3. `resource=events` / `messages` for session timeline/transcript
   4. `resource=desktop_logs` / `ambient_logs` when those run IDs are linked
5. Optionally: `yaaif_ops_session_get`, `yaaif_ops_ambient_run_get`, `yaaif_ops_desktop_run_get`.
   When an ambient run is linked, read `run_path` (Coverage / Path / current step / canvas URL). Do **not** say a leftover wait block is still waiting if run status is completed/running — run status wins. Never report fake percent-complete.
6. **File / extraction issues:** when the incident involves uploads or generated files, note `file_id` **and** `artifact_name` / `artifact_version` from session context or `yaaif_session_files_list` / `yaaif_file_artifact_versions` (read-only). Prefer artifact name + version when the same filename was overwritten across turns. Do not delete artifacts from ops flow.
7. Report using the escalation template below.

## Escalation template

```markdown
## Incident
- Seed: <kind>=<id>
- Links: session=… ambient=… desktop=… harness=… request=…
- Status: session=… ambient=… desktop=… harness=…
- diagnostics_version: …
- Coverage: 8/20 reached
- Path: 7/8 finished on this path
- Current step: <id> WAITING|FAILED|RUNNING
- Canvas: <admin_ui_canvas_url>
- Files (if relevant): file_id=… artifact_name=… version=…

## Top failures
1. `<code>` — <summary>
2. …

## Next steps
1. …
2. …

## Evidence pulled
- analyze: yes
- telemetry: insights|flow_events|logs|none
- files: versions|list|none
- partial_errors: …
```

## Hand-off

Paste the filled template. Keep it short; attach raw JSON only if requested.
