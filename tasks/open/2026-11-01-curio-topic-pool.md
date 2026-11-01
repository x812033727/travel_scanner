---
id: 2026-11-01-curio-topic-pool
title: Curio topic pool: dedup, sources, merge thin topics, themes
status: in-progress
priority: P2
area: docs
owner: claude-opus-curio-pool
claimed_at: 2026-11-01T14:56:04Z
created_at: 2026-11-01T14:56:03Z
completed_at:
branch: claude/curio-topic-pool
depends_on: []
scope:
  - docs/videos/history-curiosity/pool
  - tools/video/curio/pool
---

# Curio topic pool: dedup, sources, merge thin topics, themes

## Why

站主 2026-11-01：照原來如此事務所的素材池（PR x812033727/travel_scanner#1971）幫奇聞檔案局也建一個自己的池，用來增加題目。要求一樣：
- 做好去重與來源整理；
- 太薄或無聊的題合併或淘汰；
- 影片不要為了片長硬湊。

片長站主定為「≥8 分鐘都可以」（不必硬撐 13 分鐘）。

題庫原本散在幾個地方：
- `topics.json`（224 題）與 `topics-fg.json`（61 題）；
- 已製作的 `curio-*` 目錄；
- S37–S63 只在 `origin/codex/curio-*` 分支上；
- W 軸 19 支只寫在 migration 文件裡。

這些地方都沒有工具讀，來源只在各題的 topic-check 表格裡；`topics.json` 也跟實際成片脫節。

## Definition of done

- [ ] `docs/videos/history-curiosity/pool/` 能 build 出：
  - 去重後的核心題；
  - 每個原 ID 的合併、淘汰、轉出或 Shorts 理由；
  - 來源反查；
  - 8–13 分鐘的題案；
  - 可搜尋的頁面。
- [ ] 已製作或製作中的題鎖定：只當去重對象，不能被併掉或淘汰。
- [ ] 第一批約 40 題新題，每題至少兩個可讀來源，經非作者覆核。
- [ ] `node --test tools/video/curio/pool/pool.test.mjs` 與 `cli.mjs check` 通過。

## Steps

- [x] 工具：照 PR 1971 的 core/history/render/store/cli/semantic 改成 curio 版。
- [x] 抽出分支上的 S 軸集數、W 軸清單、原來如此池的核心題（跨系列查重）。
- [x] 第一輪編輯處置（作者）。
- [ ] 非作者覆核編輯處置。
- [ ] 第一批新題研究（6 個研究代理）與非作者覆核。
- [ ] 題案、selection、build、頁面實看、PR。

## How to verify

```bash
node --test tools/video/curio/pool/pool.test.mjs
node tools/video/curio/pool/cli.mjs check
node tools/video/curio/pool/cli.mjs index && node tools/video/curio/pool/cli.mjs index   # 第二次 0 writes
```

## Notes

- 不改 `topics.json` 與 `topics-fg.json`：它們在 `2026-10-18-curio-s-axis-pilot-s01-red` 與 `2026-10-26-merge-curio-f-and-g-topics` 的 scope 裡。處置要寫回題庫，等這張票合併後另開票。
- PR 1971 的 `sectionFor` 會把 `/topic-checks/` 當成多題共用檔，對 curio 一題一檔的格式會回傳空字串、默默丟掉所有網址。curio 版改成整檔讀。
- 詞面相似對 curio 的標題幾乎抓不到真重複：L04／M01 只有 0.30，跟雜訊同分。本機語意近鄰（PR 1971 釘版的 MiniLM）才找得到，例如 U30 與 S49 同一題、M02 與原來如此的 X2020 同一題。語意分數只是給編輯讀的候選，不會自動合併。
