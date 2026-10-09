---
name: yaaif-new-file-workflow
description: Create a custom file extraction workflow on YAA\F (runs when an upload finishes extraction)
---

Use the `yaaif-create-file-workflow` skill. Ensure auth first. Clarify the event(s), the scope
(`agent_id` or `filter_contains`), whether to load the extracted text/tables, the custom tool steps
and the reply text; preview with `yaaif_file_workflow_template`; install with
`yaaif_file_workflow_create` under an ambient agent; test with a real upload and the file's
processing timeline.
