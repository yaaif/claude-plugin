---
name: yaaif-docs
description: >-
  Answer questions about how the current YAAIF version works. Use when the user
  asks about product behavior, admin screens, plugins, skills, workflows, or
  getting started. Read the docs shipped with this installation.
---

# YAAIF product docs

```
Task Progress:
- [ ] 1. Search the current docs
- [ ] 2. Read the matching page
- [ ] 3. Answer from that page
```

## Steps

1. Call `yaaif_docs_search` with the user's question. Omit `version` so the tool
   uses the docs shipped with this installation.
2. Call `yaaif_docs_page` with the best matching `slug`.
3. Answer from that markdown. Say which docs version the tool returned.
4. If search returns no match, say the current docs do not cover it. Do not
   invent product behavior.

## Done when

The reply cites the docs version and the page slug, and the wording follows that page.
