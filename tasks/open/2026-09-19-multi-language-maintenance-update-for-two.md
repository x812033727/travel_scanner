---
id: 2026-09-19-multi-language-maintenance-update-for-two
title: Multi-language maintenance update for two five-locale tech articles (Matsu 5G showcase, Apple 9/18 launch day)
status: open
priority: P3
area: docs
owner:
claimed_at:
created_at: 2026-09-19T18:39:21Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/guides/content/tech-news-taiwan-matsu-cable-tm4-20260918.json
  - apps/api/app/guides/content/tech-news-apple-september-hardware-20260909.json
  - docs/tech-news-2026/research/tech-news-taiwan-matsu-cable-tm4-20260918.json
  - docs/tech-news-2026/research/tech-news-apple-september-hardware-20260909.json
---

# Multi-language maintenance update for two five-locale tech articles (Matsu 5G showcase, Apple 9/18 launch day)

## Why

新聞批次 4.6（`2026-09-19-news-batch-4-6-news-since`）原本要「更新既有文章」兩則：馬祖 5G 示範補進
`tech-news-taiwan-matsu-cable-tm4-20260918`、Apple 9/18 全球開賣補進 `tech-news-apple-september-hardware-20260909`。
兩位更新代理各自完成了一手來源的重抓與逐句核對，但 `check_article.py --full` 都以同樣三個**結構性**理由失敗，不是內容錯誤：

1. 兩篇 zh-TW 正文都已頂在 3000 字上限（2975／2987），任何真正的新增都超字數。
2. sources 上限 4 條且 `checked_on` 須一致；保留既有 4 條再加一條今天核對的來源，兩個規則同時破。
3. 兩篇都是五語系文章（4.5／4.2 批），`--full` 要求 en／ja／ko／zh-CN 的區塊與來源鏡像 zh-TW；4.6 只做 zh-TW。

4.6 的 DELTA-4-6 第 8 條「只加一節、既有不動、--full 要過」在這兩篇上互斥。批次協調者親自重跑 checker 確認後**還原了兩篇的改動**，
把代理的 diff（含逐句 verbatim 引文與研究紀錄的 `update_20260920` 區塊）存在該 session 的 scratchpad
`news46/deferred-updates/<slug>.diff`（session 38aef1c9…）。scratchpad 不保證存活，所以下面記下重做所需的最少資訊。

## Definition of done

- [ ] 兩篇各加入新一節並翻成 en／ja／ko／zh-CN，`check_article.py --full --assets` 全過
- [ ] 為騰出字數，精簡既有正文或把一條舊來源換成新來源（決定要寫進研究紀錄），不刪事實
- [ ] `guides-import --slug` 兩篇（匯入時為 update，五個語系）、正式站驗證

## Steps

- [ ] 馬祖：來源 https://moda.gov.tw/press/press-releases/20670（2026-09-18；三家電信各一個應用：中華電信「AI數位文化科技應用」、遠傳「五官鏡」5G 智慧醫療、台灣大「Smart Campus 智慧校園大可能」），新小標「同日在馬祖：數發部與三大電信展示 5G 應用」
- [ ] Apple：來源 https://www.apple.com/tw/newsroom/2026/09/the-latest-iphone-apple-watch-and-airpods-lineups-arrive-in-stores-worldwide/ 「最新 iPhone、Apple Watch 與 AirPods 系列產品登陸全球 Apple 直營店」（事件日 2026-09-18；台灣版發布日 09-19 台北），新小標「9 月 18 日：全球直營店開賣」，只寫開賣日與公告點名的機型
- [ ] 四語翻譯（照 4.2／4.5 的 TRANSLATE.md）與逐語審稿，或站主決定只補 zh-TW 並接受四語 parity 例外（要改 checker 或改規則，另議）

## How to verify

```bash
apps/api/.venv/Scripts/python.exe docs/news-2026-batch-4/check_article.py tech-news-taiwan-matsu-cable-tm4-20260918 --full --assets
apps/api/.venv/Scripts/python.exe docs/news-2026-batch-4/check_article.py tech-news-apple-september-hardware-20260909 --full --assets
```

## Notes

- 兩位更新代理都沒有為了通過而刪既有來源或倒填 `checked_on`，這是對的；規則衝突要在規則層解，不在單篇硬湊。
- 「更新五語系舊文章」與「只做 zh-TW 的新批次」是兩種不同的工作；日後再遇到，先看目標文章的語系數與字數再決定要不要放進批次。
