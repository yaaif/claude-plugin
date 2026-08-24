# API keys for MCP → platform APIs

Tenant-scoped opaque credentials (Admin UI: **API Keys**) for downstream systems — primarily MCP tool servers — calling YAA\F platform APIs.

These are **not** inbound MCP OAuth (`mcp:read` / `mcp:chat`), **not** platform S2S (`yaaif-platform-s2s`), **not** email `yeo-`, **not** AI-gateway `ygw-`, and **not** desktop connection keys.

## When required

| Channel | Needs API key? |
|---|---|
| Ambient `tool_call` (no user JWT) | **Yes** if MCP → context-store / approvals read / ambient HTTP / … |
| Desktop remote MCP outbound | Same as ambient |
| Chat (user JWT as `X-Upstream-Authorization`) | Prefer API key for least privilege; many MCP clients ignore upstream JWT |
| Chat→ambient local tools | **No** — session JWT / in-process |
| Email outbound | Use `yeo-` (separate product) |

## Bridge tools

| Tool | Purpose |
|------|--------|
| `yaaif_api_key_list` / `yaaif_api_key_get` | List / inspect metadata |
| `yaaif_api_key_create` | Mint + auto-import Credentials (`api_key`); plaintext once |
| `yaaif_api_key_update` | Name / scopes / allowlists / enabled |
| `yaaif_api_key_rotate` | New secret; same `credential_id` (bindings stay) |
| `yaaif_api_key_delete` | Revoke |
| `yaaif_api_key_bind_deployment` | `secret_env.YAAIF_MCP_PLATFORM_API_KEY` ← Credentials |

## Scopes (deny by default)

- `context_store:read` / `context_store:write`
- `approvals:read` (submit/decide/cancel blocked for API keys)
- `local_tools:list` / `local_tools:call`
- `ambient:read` / `ambient:trigger` (partner HTTP ambient — not chat local tools)
- `skills:read`
- `files:read` / `files:write` / `files:share`

Optional allowlists: `allowed_mcp_server_ids`, `allowed_context_plugins`, `allowed_workflow_ids`, `allowed_agent_ids`.

## Binding

1. **Preferred:** `yaaif_api_key_bind_deployment` → deployment `secret_env` → `YAAIF_MCP_PLATFORM_API_KEY`
2. **Alternate:** MCP server credential profile field_map `api_key` → `headers.X-YAAIF-Platform-Key` (not skill `credentials.yaml`)
3. Redeploy after `secret_env` bind so the pod receives the env

Never inject platform S2S client secrets into MCP deployments.
