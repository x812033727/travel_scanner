---
id: 2026-10-03-release-ai-terms-batches-02-03
title: AI 名詞系列發布：第二、三批 24 篇、第一批 81 篇的摘要、總索引與 50 詞速查
status: done
priority: P2
area: docs
owner: claude-opus-5-5
claimed_at: 2026-10-03T14:03:53Z
created_at: 2026-10-03T12:04:01Z
completed_at: 2026-10-03T14:17:42Z
branch:
depends_on:
  - 2026-10-03-ai-terms-series-batch-02
  - 2026-10-03-ai-terms-series-batch-03
scope:
  - docs/ai-terms-series/releases
---

# AI 名詞系列發布：第二、三批 24 篇、第一批 81 篇的摘要、總索引與 50 詞速查

## Why

PR 合併並部署後，正式站要發布：第二批 14 篇、第三批 10 篇新文章，第一批 81 篇（含 5 篇沿用舊網址的）加了摘要與 `ai-terms` 以外的變動，
以及 `ai-terms-index`、`ai-glossary-50-terms` 的連結與摘要。要站主同意才能動正式站。

## Definition of done

- [x] 站主同意發布（有選項的提問）。
- [x] `guides-import --dry-run` 帶全部 slug，計畫是 24 新增、83 更新（81 篇＋索引＋速查），其他 unchanged。
- [x] 先 `--publish` 24 篇新文章與 81 篇第一批；確認公開後最後才發 `ai-terms-index` 與 `ai-glossary-50-terms`。
- [x] `guides-links-rebuild`、`guides-links-check --locale zh-TW`；`guides-aliases-seed --dry-run` 再正式跑（新別名 34 組）。
- [x] `verify_public.py --sitemap` 逐頁驗證；再 dry-run 應全 unchanged。發布紀錄寫在 `docs/ai-terms-series/releases/`。

## Steps

- [x] 照 `.agents/skills/content-pipeline/references/publish-runbook.md` 與 skill `deploy`。

## How to verify

見 publish-runbook；`ai-term-world-model`、`ai-term-reward-hacking` 連到 `ai-term-reinforcement-learning`，三篇同一批發。

## Notes

- slug 清單：`docs/ai-terms-series/catalogue.json`（81）、`batch-02/catalogue.json`（14）、`batch-03/catalogue.json`（10），加兩個 hub。
- 2026-10-03 發布完成，紀錄在 `docs/ai-terms-series/releases/2026-10-03-batches-02-03.md`。
- 「新別名 34 組」不準：`guides-aliases-seed` 每次都把名詞別名、字尾關鍵字、系列課程關鍵字三個來源一起種，
  正式站之前只有 307 列，這次寫入 4,714 列（多數是從沒種過的系列關鍵字）。下次跑之前先看 dry-run 的 `inserted`。
- `ai-term-grounding` 連到還沒發布的 `gemini-api-search-grounding-citations`，`links-check` 多一筆 `missing`，那篇發布後自己會好。
