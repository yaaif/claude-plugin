# YAAIF Platform (Claude Code plugin)

When the user asks to work with YAAIF (skills, MCP tools/deployments, ambient workflows):

1. Ensure session first: prefer `/yaaif-platform:yaaif-login` / `/yaaif-platform:yaaif-doctor`, or `yaaif_ensure_session` (`login_if_needed: true`, optional `profile_id` / `tenant`). Use `yaaif_platform_use` for hosted/local-hybrid/local. Set tenant by name/slug/uuid via `yaaif_set_tenant`. Confirm with `yaaif_whoami`.
2. Prefer the bundled `yaaif_*` MCP bridge tools for platform mutations. Do not invent REST paths or tool catalog names. The bridge runs with `--client claude` and stores state under `~/.yaaif/claude`.
3. This plugin works without the yaaif-platform monorepo — write packs in the user workspace and load via bridge tools.
4. For multi-capability use cases (chat + ambient + desktop, or unclear split), start with `/yaaif-platform:yaaif-plan` (`yaaif-plan-usecase`): write a plan, wait for approval, then create a Scenario (`yaaif_agent_spec_create`) and execute. Do not jump straight to a single create skill. To create or maintain a Scenario (Agent Spec) — including Admin UI **Open in Claude Code** with a `spec_id` — use `/yaaif-platform:yaaif-scenario` and `yaaif_agent_spec_*`. Sync with `/yaaif-platform:yaaif-sync-scenario`.
5. Install order for packs: persist the Scenario first → MCP deploy/register (preflight `yaaif_deployment_settings_status`; compose or kubernetes_gitops) → scoped API key + bind (`yaaif_api_key_*` when MCP calls platform APIs) → agents → approval strategy (if HITL) → ambient agent/workflow → chat/desktop skills → `yaaif_skill_map_agents_merge` → desktop worker mappings → test-trigger / `yaaif_plan_verify`. Pass `spec_id` + `slot_key` on creates so objects bind to the scenario.
6. Skill frontmatter `tools` / `allowed-tools` must use real registered MCP tool names only.
7. Chat→ambient skills must include `list_ambient_workflows` and `trigger_ambient_workflow`.
8. Prefer `yaaif_skill_map_agents_merge` over replace. Use `yaaif_plan_dry_run` before large executes.
9. Never use S2S secrets, desktop connection keys, or AI-gateway keys for this plugin. For MCP → platform APIs use tenant **API keys** (`yaaif_api_key_create` / bind) — not S2S.
10. Do **not** author skill-pack `credentials.yaml`. Bind SAP/API secrets on the **MCP server credential profile** (field_map + arg_injection); skills only store a profile name ref. Ambient calls use the server default profile.

## Admin UI handoffs

YAAIF Admin UI **Open in Claude Code** launches `claude://code/new?q=…` (Claude Desktop app) with context such as `spec_id`, `skill_id`, `agent_id`, or `workflow_id`. When that context is present:

- Stay in Claude Code. Do not open Admin UI or browser URLs for the same object.
- Invoke the matching bundled skill (`/yaaif-platform:yaaif-scenario`, `/yaaif-platform:yaaif-create-skill`, `/yaaif-platform:yaaif-create-ambient`, or agent APIs) and maintain the selected catalog object — do not create duplicates.

Admin UI omits `repo` / `cwd` because it cannot know each developer's local clone path. Run `claude` once in your project directory if you want future `repo=` handoffs from other tools.
