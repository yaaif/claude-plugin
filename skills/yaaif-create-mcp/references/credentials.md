# Credentials for external systems and MCP tools

Use Credentials and MCP server credential profiles for external-system secrets. Use the separate scoped API-key flow only when an MCP server calls YAA\F platform APIs.

## Safety rules

- Credential values are write-only. Never ask the bridge to echo a value, put one in a skill/SKILL.md, or commit one to a repository.
- Do not author skill-pack `credentials.yaml`. Skills carry only a credential profile name reference.
- Do not use platform S2S secrets, desktop connection keys, AI-gateway keys, or an MCP-to-platform API key as a general external-system credential.
- Pass secret-bearing tool arguments through the IDE's protected input flow or the YAAIF CLI's `@FILE`/stdin JSON input, not shell history.

## External HTTP MCP server

1. `yaaif_credential_create` with the external credential `kind`, `display_name`, `values`, and `scope` (`tenant_wide` or `personal`). The response contains metadata and key names, never values.
2. `yaaif_mcp_server_create` with the endpoint and `header_mappings`. Each mapping names a header, `credential_id`, optional `credential_key`, and optional `value_prefix` such as `Bearer `.
3. `yaaif_mcp_server_refresh` to discover tools.
4. `yaaif_credential_list` verifies metadata only; `yaaif_mcp_server_get` verifies the server and discovered tools.

For an existing server, `yaaif_mcp_link_or_create` remains available, but prefer `yaaif_mcp_server_create` when headers must come from Credentials rather than literal server configuration.

## Tool argument injection

Create a connection/profile on the MCP server, then map credentials into its slots:

1. `yaaif_mcp_credential_profiles_list` and `yaaif_mcp_credential_mappings_list` to inspect the current revision and mappings.
2. `yaaif_mcp_credential_profile_upsert`:
   - `credential_bindings[]`: `binding_name`, optional expected `credential_kind`, and `field_map` from credential keys to logical fields.
   - `arg_injection`: maps a binding's logical fields to arguments on exact full tool names.
   - `inject_all_tools`: optional helper for one `{argument: logical_field}` map across tools that declare those arguments.
   - `credential_audience`: `shared`, `personal_ok`, or `personal_required`.
   - `expected_revision`: use the current revision; creation defaults to 0. Retry with a fresh read after a conflict.
3. `yaaif_mcp_credential_mapping_upsert` for each profile slot:
   - Empty `skill_id` and `principal_id`: tenant default, normally a `tenant_wide` credential. Ambient calls use this server default.
   - `skill_id`: skill-specific mapping.
   - `principal_id`: personal mapping for a user.
4. Re-list the profile and mappings and run a non-destructive tool smoke where possible.

Example logical flow: a credential key `password` → profile logical field `password` → tool argument `password`. The skill names the profile; it never contains the credential id's value or the password.

## YAA\F platform API access is different

If the MCP server itself calls YAA\F APIs, continue with [api-keys.md](api-keys.md): create a least-privilege `yaaif_api_key_*`, bind its returned credential id to the deployment, and redeploy when safe. External-system Credentials and YAA\F API keys can coexist on one server, but they are not interchangeable.
