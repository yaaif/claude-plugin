---
name: yaaif-ops
description: Ops support — analyze session/ambient/desktop failures and optionally write a confirmed diagnosis back to YAAIF
---

Use the `yaaif-ops-support` skill. Authenticate if needed, collect a session_id /
ambient_run_id / desktop_run_id / request_id. When ambient_run_id is known, call
`yaaif_ops_diagnosis_list` first, then `yaaif_ops_analyze`, accounting for prior
findings. Print linked IDs + failures + next steps and `run_path` when present.
Fill a complete OpsDiagnosisRecord, present it to the user, and only after
explicit confirmation call `yaaif_ops_diagnosis_create` with `confirm=true`.
Do not invent percent-complete. Do not pause/stop/approve/reject/retry/heal/trigger.
