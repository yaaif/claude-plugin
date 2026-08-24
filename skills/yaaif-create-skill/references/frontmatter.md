# SKILL.md frontmatter (YAA\F)

```yaml
---
name: my-skill
description: >
  What the skill does and when to use it (trigger vocabulary).
---
```

Platform also accepts tool wiring via API fields:

- `tools`: string list of MCP tool names
- `allowed_tools`: same names (prefer both when creating via API)
- `classification`: e.g. `general`

Rules:

- Never invent tool names
- Prefer snake_case catalog names exactly as registered
- Keep descriptions outcome-oriented for routing
