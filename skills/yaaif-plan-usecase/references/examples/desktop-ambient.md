# Example plan: desktop + ambient

Use when SAP GUI / local UI work runs on a desktop worker, optionally coordinated with ambient.

```markdown
# YAA\F use-case plan: SAP GUI post goods issue

- **Slug:** sap-gui-pgi
- **Status:** proposed

## 1. Use case summary

Operator asks in chat to post goods issue; desktop worker runs SAP GUI steps; ambient records completion.

## 2. Intent capture

| Field | Value |
|-------|-------|
| Outcome | PGI posted in SAP; run logged |
| Triggers | chat |
| Sync vs async | desktop sync; ambient record async optional |
| HITL | no (or supervisor approval before post) |
| Systems | SAP GUI MCP |
| Desktop GUI | yes — Windows worker |

## 4. Components

- MCP: sap-gui tools (reuse or deploy)
- Agents: chat (skills) + desktop + optional workflow
- Skills: desktop skill classification:desktop; optional chat orchestration
- Desktop mappings: yaaif_desktop_skill_mapping_set after listing workers

## 6. Install order

1. MCP (sap-gui) if needed
2. Create desktop + chat agents
3. Create desktop skill + optional chat skill
4. yaaif_skill_map_agents_merge
5. yaaif_desktop_workers_list → yaaif_desktop_skill_mapping_set
6. Optional ambient record workflow
7. yaaif_plan_verify
```
