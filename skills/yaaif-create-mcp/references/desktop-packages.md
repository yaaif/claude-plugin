# Command-based MCP tool packages (desktop)

HTTP MCP servers deploy with `yaaif_mcp_deployment_*` (compose / Kubernetes).
**Stdio / command** MCP servers (SAP GUI, local Node stdio, Windows executables)
are published to the Admin UI **Package Registry** and installed onto desktop
workers.

Do **not** docker-deploy a command MCP.

## Decide

| Server talks over | Install with |
|-------------------|--------------|
| Streamable HTTP / SSE on a URL | `yaaif_mcp_deployment_*` |
| Local process (`python`, `node`, `.exe`) on a worker PC | `yaaif_desktop_tool_package_*` |

## Optional manifest

Put `yaaif-tool-package.json` at the codebase root to pin registry fields:

```json
{
  "tool_key": "sap-gui.mcp",
  "version": "1.0.0",
  "display_name": "SAP GUI MCP",
  "description": "Command-based MCP server for SAP GUI desktop automation.",
  "interpreter": "",
  "command_args": [],
  "capabilities": ["mcp"],
  "timeout_seconds": 120,
  "entrypoint": "sap-gui-mcp-stdio.exe",
  "platform": "windows",
  "artifact": "dist/sap-gui-mcp-stdio.exe"
}
```

Without a manifest the bridge infers `tool_key` from the directory / pyproject /
package name (`sap-gui-mcp-service` → `sap-gui.mcp`), env from `.env.example`
(skipping `DESKTOP_WORKER_LOG_DIR` / `LEASE_RUN_ID`), and prefers a `dist/`
binary when present.

## Publish

1. `yaaif_ensure_session`
2. `yaaif_desktop_tool_package_inspect` with absolute `source_dir` — review
   `tool_key`, `interpreter`, `entrypoint`, `platform`, warnings
3. `yaaif_desktop_tool_package_publish`
   - `mode`: `add` (fail if exists), `update` (fail if missing), `upsert` (default)
   - `platform`: `windows` | `macos` | `linux`
   - `artifact_path`: prebuilt zip/tar.gz/exe when you already built one
4. Optional worker lifecycle:
   - `yaaif_desktop_workers_list`
   - `yaaif_desktop_tool_package_worker_status`
   - `yaaif_desktop_tool_package_install` / `yaaif_desktop_tool_package_upgrade`
   - `yaaif_desktop_tool_package_uninstall` (removes from the worker only)
5. `yaaif_desktop_skill_mapping_set` after the tool is present on the worker

Python Windows tools (SAP GUI): build a standalone exe first (PyInstaller), then
publish so the worker does not need `uv`/Python. Source zips are a last resort.

## Update / remove

**Registry (catalog):**
- Metadata only: `yaaif_desktop_tool_package_update`
- New archive from the same codebase: `yaaif_desktop_tool_package_publish` `mode=update`
- Delete the catalog entry: `yaaif_desktop_tool_package_delete`

**On a worker:**
- Status: `yaaif_desktop_tool_package_worker_status`
- Install: `yaaif_desktop_tool_package_install` `{ package_id, worker_id }` (or `worker_ids`)
- Upgrade to the current registry version: `yaaif_desktop_tool_package_upgrade`
- Uninstall from the PC: `yaaif_desktop_tool_package_uninstall` `{ package_id, worker_id }`

List/get: `yaaif_desktop_tool_packages_list` / `yaaif_desktop_tool_package_get`.
`yaaif_catalog_overview` includes `desktop_tool_packages`.
