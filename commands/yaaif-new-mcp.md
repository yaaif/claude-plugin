---
name: yaaif-new-mcp
description: Scaffold, deploy, and register MCP tools on YAA\F
---

Use the `yaaif-create-mcp` skill. Ensure auth first.

- **HTTP MCP:** preflight `yaaif_deployment_settings_status` → contract → scaffold → image → `yaaif_mcp_deployment_*` (compose or kubernetes_gitops) → if MCP calls platform APIs: `yaaif_api_key_create` + `yaaif_api_key_bind_deployment` → verify catalog (or `yaaif_mcp_link_or_create` fallback). Never put platform S2S into MCP pods.
- **Command/stdio MCP** (desktop Package Registry): `yaaif_desktop_tool_package_inspect` on the local codebase → `yaaif_desktop_tool_package_publish` (`add` / `update` / `upsert`) → `yaaif_desktop_tool_package_install` / `_upgrade` / `_uninstall` on workers. Registry delete is `yaaif_desktop_tool_package_delete`. Do not docker-deploy command MCP.
