# Publishing `@yaaif/platform-mcp` (Claude / Codex prerequisite)

The Claude Code plugin does **not** bundle MCP source. Marketplace and
`npx` installs start:

```text
npx -y @yaaif/platform-mcp@1.3.1 --client claude
npx -y @yaaif/platform-mcp@1.3.1 --install --client claude
```

That package is built from
[`cursor-plugin/packages/mcp`](https://github.com/yaaif/cursor-plugin/tree/main/packages/mcp).
Until it is on the public npm registry, Claude and Codex marketplace installs
cannot start the bridge. As of this writing `npm view @yaaif/platform-mcp`
returns 404.

## Publish checklist (npm org access required)

1. Authenticate to npm with publish rights on the `yaaif` scope:

   ```bash
   npm login
   npm whoami
   ```

2. From a cursor-plugin checkout:

   ```bash
   cd packages/mcp
   npm test
   npm run build
   npm publish --access public
   ```

   Confirm:

   ```bash
   npm view @yaaif/platform-mcp version
   ```

   Expected: `1.3.0` (or the version pinned in this repo’s [`.mcp.json`](../.mcp.json)).

3. Keep this plugin’s `.mcp.json` pin in lockstep with the published version.
   Do not bump the pin until `npm view` reports that version.

4. Smoke-test:

   ```bash
   claude --plugin-dir /path/to/claude-plugin
   ```

   Then `/yaaif-platform:yaaif-doctor`.

Full Cursor-side notes:
[`cursor-plugin/docs/npm-publish.md`](https://github.com/yaaif/cursor-plugin/blob/main/docs/npm-publish.md).

## Local development before npm publish

Point `.mcp.json` (or a local override) at the monorepo build instead of npx:

```json
{
  "mcpServers": {
    "yaaif": {
      "command": "node",
      "args": [
        "/path/to/yaaif-platform/integrations/cursor-plugin/packages/mcp/dist/cli.js",
        "--client",
        "claude"
      ]
    }
  }
}
```

Build first: `cd integrations/cursor-plugin/packages/mcp && npm install && npm run build`.
Do not commit a machine-local path to this repository.
