# Ops correlation cheat sheet

## Seed → expands to

| Seed | Typical links |
|------|----------------|
| `ambient_run_id` | `session_id` (run.session_id), `desktop_run_id` (context.workflow_last_skill_desktop_run_id) |
| `session_id` | `ambient_run_id`, `desktop_run_id` on flow-session summary |
| `desktop_run_id` | payload `session_id` / `ambient_run_id` / `request_id` / harness ids |
| `request_id` | flow events → session + `llm_call_id`s |

## RO API (agent-service)

- `GET /api/ops/correlate`
- `GET /api/ops/analyze`
- `GET /api/ops/sessions/:session_id`
- `GET /api/ops/ambient-runs/:run_id`
- `GET /api/ops/desktop-runs/:run_id`
- `GET /api/ops/desktop-runs?session_id=`

## Permissions

Caller needs `agent.sessions.read` or `agent.ambient.read`. Desktop/metrics slices may return `partial_errors` if the token lacks control-plane / metrics rights.

## Failure sources

- `ambient` — ported ambient-run-diagnostics rules
- `session` — tool/response/error counts + execution_reason_code
- `desktop` — status/error on worker run
