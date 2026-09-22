---
name: yaaif-ops-support
description: >-
  Operations support for LLM sessions, ambient workflow runs, and desktop
  executions: correlate IDs, analyze failures, pull telemetry, and optionally
  write a confirmed OpsDiagnosisRecord back to YAAIF. Never pause/stop/approve/retry.
---

# YAA\F operations support

```
Task Progress:
- [ ] 1. Auth + tenant
- [ ] 2. Collect seed ID(s)
- [ ] 3. List prior diagnoses (yaaif_ops_diagnosis_list) when ambient_run_id known
- [ ] 4. yaaif_ops_analyze (account for prior findings)
- [ ] 5. Telemetry drill-down (yaaif_ops_telemetry)
- [ ] 6. Fill OpsDiagnosisRecord (all fields)
- [ ] 7. Present draft → WAIT for explicit user confirmation
- [ ] 8. yaaif_ops_diagnosis_create(..., confirm=true)
- [ ] 9. Escalate with template (optional paste)
```

## Prerequisites

1. `yaaif-auth`
2. Prefer `yaaif_doctor` — confirm `ops_api` and `ops_telemetry` checks pass
3. Read [references/correlation.md](references/correlation.md)

## Hard rules

- Prefer `yaaif_ops_*` tools (and read-only list/get tools).
- **Never** call `yaaif_ambient_run_pause`, `resume`, `stop`, `approve`, `reject`, retry, trigger, heal, or mapping mutations.
- The **only** allowed write-back is `yaaif_ops_diagnosis_create` after the user explicitly confirms the draft (`confirm=true`).
- Do not invent other remediation API calls.
- Prefer `summary_only` (default on analyze) and avoid `include_raw` unless the operator holds `ops.support.raw`.

## Flow (fixed order)

1. Ask for any of: `session_id`, `ambient_run_id`, `desktop_run_id`, `request_id` (one is enough). Admin IDE handoffs usually already include `ambient_run_id`.
2. When `ambient_run_id` is known, call **`yaaif_ops_diagnosis_list`** first. Summarize prior diagnoses (who / when / title / top failure codes). Treat them as context: avoid repeating dead-end next steps that already failed; call out what changed since the last diagnosis.
3. Call **`yaaif_ops_analyze`** with the seed(s).
4. Note `partial_errors` (metrics/desktop/harness/`ops.support.raw`) but continue with available data.
5. Drill down with **`yaaif_ops_telemetry`** (preferred over per-resource aliases):
   1. `resource=insights` when `session_id` known
   2. `resource=flow_events` when `request_id` known
   3. `resource=events` / `messages` for session timeline/transcript
   4. `resource=desktop_logs` / `ambient_logs` when those run IDs are linked
6. Optionally: `yaaif_ops_session_get`, `yaaif_ops_ambient_run_get`, `yaaif_ops_desktop_run_get`.
   When an ambient run is linked, read `run_path` (Coverage / Path / current step / canvas URL). Do **not** say a leftover wait block is still waiting if run status is completed/running — run status wins. Never report fake percent-complete.
7. **File / extraction issues:** when the incident involves uploads or generated files, note `file_id` **and** `artifact_name` / `artifact_version` from session context or `yaaif_session_files_list` / `yaaif_file_artifact_versions` (read-only). Prefer artifact name + version when the same filename was overwritten across turns. Do not delete artifacts from ops flow.
8. Fill a complete **OpsDiagnosisRecord** (every field below). Present the draft to the user. **Wait for explicit confirmation** before calling `yaaif_ops_diagnosis_create` with `confirm=true`. If the user declines, skip write-back and still paste the escalation template.
9. After a successful write (or if skipped), report using the escalation template.

## OpsDiagnosisRecord (fill all fields)

| Field | Notes |
|-------|--------|
| `ambient_run_id` | Required |
| `session_id`, `desktop_run_id`, `harness_run_id`, `request_ids` | From analyze links (empty string / `[]` when unknown) |
| `intent` | `diagnose_failure` or `inspect_run` |
| `severity` | `error` \| `warning` \| `info` \| `ok` |
| `title`, `summary` | Short operator-facing headline + paragraph |
| `status_session`, `status_ambient`, `status_desktop`, `status_harness` | From analyze status snapshot |
| `failures` | Array (use `[]` when none); each item: source, severity, code, title, summary, causes[], resolutions[] |
| `next_steps` | Array (use `[]` when none) |
| `coverage_reached`, `coverage_total`, `path_executed`, `path_reached` | From `run_path` (0 when unknown) |
| `current_step_id`, `current_step_status`, `canvas_url` | From `run_path` |
| `diagnostics_version` | From analyze (e.g. `ops-diagnostics/1`) |
| `evidence_analyze` | `true` if analyze was called |
| `evidence_telemetry` | e.g. `["insights","ambient_logs"]` |
| `partial_errors` | Object (use `{}` when none) |
| `source` | `cursor` \| `vscode` \| `intellij` \| `codex` \| `claude-code` \| `admin_ui` |
| `ide_client` | Optional free text |
| `diagnosed_at` | Optional RFC3339; server sets actor identity from auth |

Actor fields (`diagnosed_by_*`) are set by the server from the authenticated user — do not invent them.

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
- Prior diagnoses: <count> (latest: <when> by <who> — <title>)
- Files (if relevant): file_id=… artifact_name=… version=…
- Written to YAAIF: yes|no (diagnosis_id=…)

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
