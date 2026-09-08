---
name: yaaif-ops
description: Read-only ops support — correlate and analyze session/ambient/desktop failures
---

Use the `yaaif-ops-support` skill. Authenticate if needed, collect a session_id /
ambient_run_id / desktop_run_id / request_id, call `yaaif_ops_analyze`, and report
linked IDs + failures + next steps. When an ambient run is linked, also print
`run_path`: Coverage (`reached/total`), Path (`executed/reached`), current step,
and the Admin UI canvas URL. Do not invent percent-complete. Do not call any
mutating ambient/desktop tools.
