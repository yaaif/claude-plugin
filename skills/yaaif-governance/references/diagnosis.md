# Failure analysis and remediation

Collect session_id, request_id, ambient_run_id or desktop_run_id. Read existing diagnosis records, then use `yaaif_ops_correlate`, `yaaif_ops_analyze` and authorized telemetry. Respect `ops.support.raw`; do not request raw data merely because summaries exist.

Classify the cause: policy rejection, harness limit or continuation behavior, model output, tool/schema/authentication error, infrastructure failure, or invalid business input. Cite relevant event identifiers and current policy/override sources. Separate evidence from hypotheses and identify missing evidence.

For a policy remedy, explain the original intent, why the failure conflicts with it, the smallest change that preserves it, and likely effects on permitted and forbidden examples. Include regression examples that should continue to be blocked. Use `yaaif_governance_inspect` with `resource=dry_run` and a typed `evaluation` sample, or `resource=replay_start` followed by `resource=replay` with the returned job ID, where available and report when no representative evaluation was run.

If the cause is outside governance, explain the appropriate fix without changing policy. Never disable enforcement or expand tool access as a default recovery. Do not pause, resume, stop, retry or approve executions here. Save a diagnosis only through the existing confirmed diagnosis workflow when the user requests it.
