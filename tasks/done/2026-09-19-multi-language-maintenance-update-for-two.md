---
id: 2026-09-19-multi-language-maintenance-update-for-two
title: Multi-language maintenance update for two five-locale tech articles (Matsu 5G showcase, Apple 9/18 launch day)
status: done
priority: P3
area: docs
owner: claude-opus-5-5-tech-news-maintenance
claimed_at: 2026-10-05T07:24:13Z
created_at: 2026-09-19T18:39:21Z
completed_at: 2026-10-05T08:35:42Z
branch: claude/tech-news-maintenance
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

- [x] 馬祖：加入新一節並翻成 en／ja／ko／zh-CN，`check_article.py --full --assets` OK
- [ ] Apple：加入新一節並翻成四語 → 移到 `2026-10-05-decide-the-source-cap-for-news`（四條來源都撐著正文，加第五條要站主改規則）
- [x] 馬祖：為騰出字數精簡既有正文、把一條舊來源（新聞發布列表頁 372）換成新來源 20670，決定寫進研究紀錄 `update_20261005`，沒有刪有來源的事實
- [ ] `guides-import --slug tech-news-taiwan-matsu-cable-tm4-20260918`（update，五個語系）、正式站驗證：publish after merge (coordinator, owner consent)；Apple 那篇隨 follow-up 票

## Steps

- [x] 馬祖：來源 https://moda.gov.tw/press/press-releases/20670（2026-09-18；三家電信各一個應用：中華電信「AI數位文化科技應用」、遠傳「五官鏡」5G 智慧醫療、台灣大「Smart Campus 智慧校園大可能」），新小標「同日在馬祖：數發部與三大電信展示 5G 應用」
- [ ] Apple：來源 https://www.apple.com/tw/newsroom/2026/09/the-latest-iphone-apple-watch-and-airpods-lineups-arrive-in-stores-worldwide/ 「最新 iPhone、Apple Watch 與 AirPods 系列產品登陸全球 Apple 直營店」（事件日 2026-09-18；台灣版發布日 09-19 台北），新小標「9 月 18 日：全球直營店開賣」，只寫開賣日與公告點名的機型 → 移到 `2026-10-05-decide-the-source-cap-for-news`
- [x] 馬祖四語翻譯（照 `docs/news-2026-batch-4/agents/tech/TRANSLATE.md` 的用語表）
- [ ] 馬祖四語的逐語審稿：翻譯與撰稿是同一個代理，獨立的逐語審稿交給這個 PR 的審查階段（PR 內文列了要審的區塊）

## How to verify

```bash
apps/api/.venv/Scripts/python.exe docs/news-2026-batch-4/check_article.py tech-news-taiwan-matsu-cable-tm4-20260918 --full --assets
apps/api/.venv/Scripts/python.exe docs/news-2026-batch-4/check_article.py tech-news-apple-september-hardware-20260909 --full --assets
```

## Notes

- 兩位更新代理都沒有為了通過而刪既有來源或倒填 `checked_on`，這是對的；規則衝突要在規則層解，不在單篇硬湊。
- 「更新五語系舊文章」與「只做 zh-TW 的新批次」是兩種不同的工作；日後再遇到，先看目標文章的語系數與字數再決定要不要放進批次。
- 2026-10-05（claude-opus-5-5-tech-news-maintenance）：馬祖那篇做完，Apple 那篇與一個新發現拆到 `2026-10-05-decide-the-source-cap-for-news`。
  - `check_article.py` 要剛好 5 個 level-2 小節，所以「加一節」其實是「併一節再加一節」：原第四節（海纜清單，標題本來就有「還有哪些沒寫」）
    吸收原第五節「官方到現在還沒有說的事」的兩段（併成一段、否定句限縮到中華電信的公告），原第五節的列表頁快照那段刪除，新第五節是 5G 活動兩段。
    zh-TW 2,975 → 2,983。其餘刪減都是重複句或措辭，逐條記在研究紀錄 `update_20261005.what_changed`。
  - 換掉的是 `press-releases/372`（新聞發布列表頁）：它在正文只撐「9 月 18 日查核時列表頁未見對應公告」一句。2026-10-05 重抓，
    列表上 9 月 18 日有兩則：20670（5G 活動）與 **20658「臺馬第四海纜完工啟用 數發部強化馬祖通訊韌性」**——那句話已經不成立，所以連同那段一起拿掉。
  - 20658（完工啟用典禮、行政院長出席、雙層鎧裝、埋深 2.5 公尺、AI＋AIS 預警）才是這篇最該引的來源，但四個位置已滿，換掉任一條都會刪事實。
    文章裡會被 20658 推翻的否定句（「官方文件都沒有寫纜線規格」等）都限縮成「中華電信的公告沒有寫」；要不要引 20658 交給 follow-up 票。
  - Apple：四篇 9 月 9 日新聞稿各自是該產品台灣售價的唯一來源，沒有一條能換；開賣稿頁面日期是 9 月 18 日（不是票上寫的 9/19 台北）。
  - 圖解沒重畫：SVG 上畫著 caption「查核日 2026 年 9 月 18 日」，四格內容 10-05 仍成立，所以 diagram caption 五語都沒動。
