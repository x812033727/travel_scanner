---
id: 2026-10-22-c17-nalgene-treatment
title: Research C17 Nalgene brand story treatment and sources
status: in-progress
priority: P2
area: docs
owner: codex-c17-nalgene-treatment
claimed_at: 2026-10-22T18:52:30Z
created_at: 2026-10-22T18:52:18Z
completed_at:
branch: codex/brand-story-nalgene-c17
depends_on: []
scope:
  - docs/videos/story-everyday-nalgene-c17
---

# Research C17 Nalgene brand story treatment and sources

## Why

「日用品的意外轉身」C17 只有 20 題表的取證入口。須區分 Nalge 的 1949 年實驗器皿、原廠回憶中 1960 年代員工帶瓶健行、1970 年代中期才形成戶外消費品，以及 2008／2020 的材料變更；避免把品牌年齡當作戶外水瓶上市年、把公司回憶當同時期紀錄，或把現行材質倒填到舊瓶。

## Definition of done

- [ ] 六章 Treatment 有一條可講的因果主線、開場與每 30–45 秒具體鉤子、片頭片尾／畫面界線；未核准時不寫逐字稿或付費。
- [ ] 逐項來源矩陣將可直接讀的原廠／供應商原件連到 M01–M12，標清可說與不可推論，供另一代理獨立重開。
- [ ] 獨立來源審查綁 Treatment／矩陣雜湊後，才送站主審企劃方向。

## Steps

- [x] 查現有 20 題企劃、看板、PR 和工作樹，從系列分支另開 C17 工作樹並認領。
- [x] 讀一手頁與原發行者重刊新聞稿；保留 1949／1960s／mid-1970s／2008／2020 的口徑差異。
- [x] 寫 Treatment、來源矩陣並做機械檢查；提交草稿 PR。
- [ ] 派不同代理獨立逐項重開來源；必要時作者修訂並重核，再交站主企劃審核。

## How to verify

檢查兩個 Markdown 檔 SHA-256、`git diff --check`、`npm run check:tasks` 和草稿 PR head／label。獨立審查者需重開原始連結，不把此作者稿或先前 C01–C16 查核視為 C17 PASS。長度與插圖占比仍需逐字稿、TTS 和實際成片時間軸驗證。

## Notes

2026-10-23：未找到可直接讀出 Nalgene 販售節點的 1970 年代原廠型錄。NRS 開放 1976 起的掃描型錄索引，但尚未確定其中有該商品，不把索引當 Nalgene 上架證據。2008 當時公司的 BPA 停產公告由 Chemical Online 原文轉載，須標明載體。2020 公司新聞稿的「50% recycled」腳註為 ISCC mass-balance 分配；2024 Thermo Fisher 事實表較清楚，不能畫成每瓶實體一半回收料粒子。

2026-10-23 作者稿：`treatment.md` SHA-256 `D7B331C87E1C0904093E95877D75841EBBA495581A3040EDD7DC5C3AE854410F`；`source-matrix.md` SHA-256 `E2A475A1344ED3255E42D93A0542DB2ADA38E73EE2F52B0CDA926B608FEDADE7`。M01–M12 是待重核矩陣，不是 PASS。`npm run check:tasks` 通過（2075 張票，既有跨票警告）；`git diff --check` 通過。無付費、匯入或上架。

2026-10-23：已開[草稿 PR #1699](https://github.com/x812033727/travel_scanner/pull/1699)，base `codex/brand-stories-new-series-20261020`、標記 `no-auto-merge`；原作者輸入檔雜湊如上。下一手先派另一名代理逐項重開來源，查核後才問站主是否採用企劃。

2026-10-23 作者窄修：獨立審查在 `docs/videos/brand-story-independent-reviews/C17-nalgene-20261023.md` 對「1949 水瓶」說法錯置為 S2 標題提出 HOLD；已只把五處來源定位／後續查核提示改為「開頭導語」。新版 `treatment.md` SHA-256 `0451192DAA6EDF85CFD8721674511B6DBDBC671A73AC720B0BCEDFB9E14C1E07`；`source-matrix.md` SHA-256 `892041F854DCF4FBFFF37BFE90AC6B1AA02647CBD146CB2262F7A2E47FAC316E`，細節見同目錄 `author-repair-20261023.md`。M01 定位待另一代理依新版雜湊複核，尚未解除企劃 HOLD 或交站主採用。
