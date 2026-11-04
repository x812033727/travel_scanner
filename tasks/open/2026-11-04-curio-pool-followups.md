---
id: 2026-11-04-curio-pool-followups
title: 奇聞檔案局素材池：候補補來源與待站主決定的題案組合
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-11-04T06:05:16Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/history-curiosity/pool
---

# 奇聞檔案局素材池：候補補來源與待站主決定的題案組合

## Why

奇聞檔案局素材池（`docs/videos/history-curiosity/pool/`）在 #1986 做到第二十批（revision `2026-11-02-curio-pool-761`：入選 761、題案 106、可成片 104 組題案＋534 個單集），站主 2026-11-04 同意合併。原票 `tasks/done/2026-11-01-curio-topic-pool.md` 結案時還有兩類事沒做完：

1. 37 題候補還缺兩個可讀來源，或還有待查的關鍵點，各題 notes 寫了缺什麼；
2. 覆核者建議、但要把既有單集壓短或改動既有題案的題案組合，一直沒排，等站主決定；相關的章節題先轉了 Shorts。

## Definition of done

- [ ] 站主對下列每一組題案組合都有決定（排、不排、撤回），素材池照決定重建。
- [ ] 能補到來源的候補升為入選或維持候補，理由寫進批次或重查檔。

## Steps

- [ ] 請站主決定以下組合（都在 pool `README.md` 各批的「覆核建議、但這批沒有排的題案」）：
  - T96（N1141＋N1743）、T107（N1723＋N1966）：已排，站主不同意就照各自的撤回條件撤回；
  - 第十八批：N2022＋N141、N2025＋N1344、N2087＋N1563（N1563 已在 T92）；
  - 第十九批：N2122＋N922、N2144＋N647、N2206＋N2202、N2224＋N1442、N2183＋N727；N2208＋N2083（N2083 還在候補）；
  - 第二十批：N2263 接進 T64、N2243 接進 T90 或 T10、N2283 接進 T94、N2324 接成 T98 第三章、N2305＋N1124（N1124 是 Shorts）。
- [ ] 站主同意的組合：章節題從 Shorts 移回長片（`UNSHORT`），寫題案，重建（流程見 pool `README.md`〈續接〉）。
- [ ] 候補補來源：從 `index.html` 篩「候補」，逐題看 notes；常見阻擋是 loc.gov、HathiTrust、Gallica、Hemeroteca Digital Brasileira 的機器驗證或 403，不繞過。
- [ ] 題案的實際試讀（目前片長只是素材估計）。

## How to verify

```bash
node --test tools/video/curio/pool/pool.test.mjs
node tools/video/curio/pool/cli.mjs build && node tools/video/curio/pool/cli.mjs check
node tools/video/curio/pool/cli.mjs index   # 跑兩次，第二次 0 writes
```

## Notes

- 原票的 Notes 有每一批的數字與做法；pool `README.md` 有各批覆核改掉的重點與站主的決定。
- NewspaperSG 的文章要先按「同意使用條款」才能讀全文，代理沒有替站主同意；1909 年曼谷 "Ghost of Windmill Road" 那則若站主願意同意可以再查。
- 越南能讀到的材料前幾批已用得差不多（第二十批只收到 2 題）。
