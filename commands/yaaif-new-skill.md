---
name: yaaif-new-skill
description: Create a YAA\F skill and load it into the tenant catalog
---

Use the `yaaif-create-skill` skill. Ensure auth via `yaaif-login` first.

If the prompt includes `skill_id`, stay in Claude Code (do not open Admin UI URLs)
and maintain that skill. Otherwise author and load a new skill with bridge
tools (`yaaif_skill_create`, enable, map, refresh).
