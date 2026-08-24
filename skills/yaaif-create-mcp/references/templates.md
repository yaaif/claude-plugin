# MCP templates

Official scaffolds (public):

- Go: https://github.com/yaaif/mcp-server-templates-go
- Python: https://github.com/yaaif/mcp-server-templates-py

`yaaif_mcp_scaffold` clones these into the user's workspace under `mcp-servers/<name>-mcp-service/`.

Typical HTTP MCP path: `/mcp`
Typical container port: `8080`

For domain data persistence on YAA\F, prefer context-store (`CONTEXT_STORE_BASE_URL`) rather than a private DB when integrating with the platform.
