# Example plan: chat-only triage

Use when the operator only needs interactive MCP Q&A in chat (no ambient, no desktop).

```markdown
# YAA\F use-case plan: Vendor FAQ triage

- **Slug:** vendor-faq
- **Status:** proposed

## 1. Use case summary

Chat agent answers vendor-status questions using existing MCP tools.

## 2. Intent capture

| Field | Value |
|-------|-------|
| Outcome | Fast answers on vendor status in chat |
| Triggers | chat |
| Sync vs async | sync |
| HITL | no |
| Systems | existing MCP catalog |
| Desktop GUI | no |

## 3. Catalog reuse

Reuse MCP tools already registered; create one chat skill + map to default chat agent.

## 4. Components

- MCP: reuse
- Agents: reuse chat agent (skills)
- Ambient: none
- Skills: create `vendor/faq-triage` (chat)
- Approvals: none
- Desktop mappings: none

## 6. Install order

1. [x] MCP — skip (reuse)
2. [x] Agents — reuse
3. [ ] Skills — create + enable
4. [ ] Map — yaaif_skill_map_agents_merge
5. [ ] Verify — yaaif_plan_verify
```
