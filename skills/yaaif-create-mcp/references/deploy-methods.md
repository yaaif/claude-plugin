# MCP deployment methods (compose vs Kubernetes GitOps)

Both methods use the same bridge tools. Deployment-service branches on `deployment_method`.

## Preflight

1. `yaaif_deployment_settings_status`
2. `yaaif_deployment_settings_get` — note `default_deployment_method`

| Component | Needed for compose | Needed for kubernetes_gitops |
|-----------|--------------------|---------------------------|
| docker | Healthy | Optional |
| gitops | Optional | **Required** (repo dir configured in Admin) |
| kubernetes | Optional | Recommended (secrets + `/k8s/*` status/logs) |
| agent_service / api_server | Register / credentials | Same |

Plugin settings tools are **read-only**. Configure GitOps repo / kube enablement in Admin → Deployment service.

## Field matrix

| Field | docker_compose | kubernetes_gitops |
|-------|----------------|-------------------|
| `deployment_method` | `docker_compose` | `kubernetes_gitops` |
| `endpoint_mode` | `docker_name` (compose DNS), or `localhost` / `custom` | Prefer `docker_name` → auto Service DNS; `custom` + `endpoint_host` only if needed |
| `transport_type` | `STREAMABLE_HTTP` or `SSE` | Same |
| `secret_env` | Injected into compose env | Upserted as K8s secrets (needs k8s client) |
| `registry_credential_id` | docker login before pull | ImagePullSecret |
| Namespace / overlay | N/A (`compose_file_path`) | Auto (`kubernetes_namespace`, `gitops_overlay_path`) — not create inputs |

## Happy path

```
settings_status → create → deploy → status (poll) → logs → [k8s_status] → register → api_key_bind
```

### Poll hints

- `phase`: `deploying` → `running` (or `sync_pending` / `failed`)
- `status_stages`: deployment_requested → deployment_added → …
- `generated_endpoint`: catalog registration target
- K8s: `kubernetes_namespace`, then `yaaif_mcp_deployment_k8s_status`

### Logs

`yaaif_mcp_deployment_logs` auto-routes:

- compose → `GET …/logs`
- kubernetes_gitops → `GET …/k8s/logs`

## Day-2

| Action | Tool |
|--------|------|
| Change image/env/secrets | `yaaif_mcp_deployment_update` → `yaaif_mcp_deployment_redeploy` |
| Force rollout | `yaaif_mcp_deployment_redeploy` |
| Stop | `yaaif_mcp_deployment_stop` |
| Delete | `yaaif_mcp_deployment_delete` (`cascade_agent` default true) |

## When to use `yaaif_mcp_link_or_create`

- MCP already running outside deployment-service
- Local/dev endpoint only
- Deployment-service / GitOps not available for the tenant

Still use `yaaif_api_key_*` if that MCP calls platform APIs.
