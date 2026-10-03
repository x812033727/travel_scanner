---
id: 2026-10-03-skills-what-the-ai-terms-release
title: Skills: what the AI-terms release taught about hubs, link baselines and the alias seed
status: done
priority: P2
area: docs
owner: claude-opus-5-5
claimed_at: 2026-10-03T14:43:48Z
created_at: 2026-10-03T14:43:40Z
completed_at: 2026-10-03T14:52:29Z
branch:
depends_on: []
scope:
  - .agents/skills/catalog-import/references/other-data.md
  - .agents/skills/content-pipeline/references/publish-runbook.md
---

# Skills: what the AI-terms release taught about hubs, link baselines and the alias seed

## Why

2026-10-03 發布 AI 名詞系列 107 包（紀錄在 `docs/ai-terms-series/releases/2026-10-03-batches-02-03.md`）時有幾件事 skill 沒寫：
`guides-aliases-seed` 每次都種三個來源，票預期 34 組、實際寫入 4,714 列，腳本沒有在數量上設關卡；
hub 要等新文章公開後才發；`links-check` 要比的是發現的集合而不是筆數；dry-run 分不出「已發布的更新」和「從沒發布過的草稿」。

## Definition of done

- [x] `publish-runbook.md` 寫了 hub 最後發、發布前後的 links-check 基準、怎麼確認 update 的文章本來就公開、匯入後的別名種子與數量關卡。
- [x] `catalog-import` 的 `other-data.md` 寫了別名種子的三個來源與先看 `inserted`。

## How to verify

`npm run test:tools && npm run check:tasks`

## Notes

- 只改 references，SKILL.md 沒動，所以 `.claude/skills` 的複本不用同步。
