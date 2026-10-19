# Requirements and setting selection

Inspect current effective settings before interviewing. Ask only for missing constraints: intended behavior and affected agents/channels; sensitive data and allowed destinations; permitted tools/actions and approvals; latency, spend and execution budgets; memory/retention needs; false-positive tolerance and escalation paths.

Record a mapping of requirement → authorized source → supported setting → proposed value → validation evidence → acceptance example. Ask about conflicting requirements instead of resolving them silently. Use installed-version docs and the harness settings catalog; report unsupported requirements explicitly.

Use policy CRUD and revisions for guardrail content, exceptions for narrowly scoped and expiring permitted bypasses, and rollouts for staged enforcement. Never propose a broad bypass merely to make a failed execution pass. Inspect protected guards and exception limits first. A preset is a starting point, not certification of legal compliance.

Harness defaults apply to chat, ambient, desktop and email where the installed backend supports each setting. Inspect agent overrides and environment fallbacks before changing tenant defaults. Budget changes must state their cost and over-limit implications. Preserve unrelated settings. Use runtime adoption only after reviewing which existing overrides it removes.

Preview all operations before live changes. Backend normalization is included for harness changes; lifecycle operations show their command arguments and before snapshot because derived effects are verified at apply. Do not describe command previews as complete simulations. Keep rollback snapshots private in the client state directory.
