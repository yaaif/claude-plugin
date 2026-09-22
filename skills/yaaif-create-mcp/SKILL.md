---
name: yaaif-create-mcp
description: >-
  Scaffold a YAA\F MCP server. HTTP servers deploy via mcp-deployments
  (docker_compose or kubernetes_gitops). Command/stdio servers publish to the
  desktop Package Registry from a local codebase. Mint/bind scoped API keys when
  the MCP calls platform APIs. For customer/partner workspaces without monorepo access.
---

# Create MCP tools and deploy on YAA\F

```
Task Progress:
- [ ] 1. Auth + tenant
- [ ] 2. Choose HTTP deploy vs command/stdio package
- [ ] 3. Design tool contracts
- [ ] 4. Scaffold / implement
- [ ] 5a. HTTP: image + yaaif_mcp_deployment_*
- [ ] 5b. Command: yaaif_desktop_tool_package_publish
- [ ] 6. Register / install onto workers
- [ ] 7. API key (if MCP → platform APIs)
- [ ] 8. Verify catalog
```

## Prerequisites

`yaaif-auth` completed.

## Choose transport

| Runtime | Path |
|---------|------|
| Streamable HTTP / SSE (container URL) | Deployment-service below |
| Local command / stdio on a desktop worker (`.exe`, `node`, `python`) | [references/desktop-packages.md](references/desktop-packages.md) |

Command MCP (SAP GUI, Node stdio): **do not** `yaaif_mcp_deployment_create`. Inspect then publish:

1. `yaaif_desktop_tool_package_inspect` (`source_dir` absolute)
2. `yaaif_desktop_tool_package_publish` (`mode` `add` \| `update` \| `upsert`)
3. Worker lifecycle: `yaaif_desktop_tool_package_worker_status` → `yaaif_desktop_tool_package_install` / `_upgrade` / `_uninstall`
4. Registry delete: `yaaif_desktop_tool_package_delete` (does not uninstall from workers)

## Preflight (HTTP only)

1. `yaaif_deployment_settings_status` — confirm docker / gitops / kubernetes / agent health
2. `yaaif_deployment_settings_get` — note `default_deployment_method`
3. For **kubernetes_gitops**: require **gitops** healthy before deploy; warn if **kubernetes** is degraded (secrets/logs may fail)
4. See [references/deploy-methods.md](references/deploy-methods.md)

## Design

Write short contracts (name, description, inputs). Names become catalog names — keep them stable snake_case. See [references/templates.md](references/templates.md).

Decide whether tools call **YAA\F platform APIs** (context-store, approvals read, ambient HTTP, local-tools, skills read, files). If yes, plan a scoped **API key** (not platform S2S). See [references/api-keys.md](references/api-keys.md).

## Scaffold

`yaaif_mcp_scaffold` with kebab `name` (no `-mcp-service` suffix), `language` `go`|`python`, and absolute `workspace_root`.

Implement tools, build/push an image the customer's deployment-service can pull.

## Full deploy

1. `yaaif_mcp_deployment_create` (`auto_register` + `auto_import_tools` true)
   - Omit `deployment_method` to use tenant default from settings, or set `docker_compose` / `kubernetes_gitops`
   - `transport_type`: `STREAMABLE_HTTP` (default) or `SSE` — never raw `HTTP`
   - K8s: prefer `endpoint_mode=docker_name` (auto Service DNS); `custom` + `endpoint_host` only when needed
2. `yaaif_mcp_deployment_deploy`
3. Poll `yaaif_mcp_deployment_status` (`phase`, `status_stages`, `generated_endpoint`, `kubernetes_namespace`)
4. Logs: `yaaif_mcp_deployment_logs` (auto-routes compose `/logs` vs k8s `/k8s/logs`)
5. K8s only: `yaaif_mcp_deployment_k8s_status` (pod + Deployment)
6. `yaaif_mcp_deployment_register` if needed

## Day-2 lifecycle

- `yaaif_mcp_deployment_update` then `yaaif_mcp_deployment_redeploy`
- `yaaif_mcp_deployment_stop`
- `yaaif_mcp_deployment_delete` (`cascade_agent` default true)

## API key (when MCP calls platform APIs)

Ambient/desktop tool calls often have **no user JWT**, so MCP pods must carry their own scoped credential:

1. `yaaif_api_key_create` with least scopes (typically `context_store:read` + `context_store:write`; add `approvals:read` only if needed)
2. Prefer allowlist `allowed_mcp_server_ids` when the server id is known
3. `yaaif_api_key_bind_deployment` with `credential_id` from create `binding_hints` + `deployment_id` (`redeploy: true` when safe) — or `yaaif_mcp_deployment_redeploy`
4. Do **not** put `YAAIF_PLATFORM_S2S_*` / desktop connection keys / AI-gateway keys into MCP env
5. Alternate binding: skill/tool field_map `api_key` → `headers.X-YAAIF-Platform-Key`

Plaintext from create/rotate is shown **once** — bind immediately; do not paste into skill files.

Skip this section when the MCP only talks to external systems and never calls YAA\F APIs (and email outbound already uses `yeo-` keys, not these API keys).

## Fallback

`yaaif_mcp_link_or_create` against an already-running endpoint; optional `yaaif_mcp_server_refresh`. Still mint/bind an API key if that endpoint calls platform APIs. Use when deployment-service is unavailable or the MCP runs outside YAA\F-managed compose/GitOps.

## Verify

`yaaif_mcp_tools_list` — confirm exact tool names before wiring skills/workflows.
`yaaif_desktop_tool_packages_list` — confirm command MCP packages in the Package Registry.
`yaaif_api_key_list` — confirm credential linked when platform calls are in scope.
