---
id: 2026-10-05-decide-the-source-cap-for-news
title: Decide the source cap for news maintenance updates, then add Apple 9/18 launch day and moda's TM4 completion release
status: open
priority: P3
area: docs
owner:
claimed_at:
created_at: 2026-10-05T08:30:59Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/guides/content/tech-news-apple-september-hardware-20260909.json
  - docs/tech-news-2026/research/tech-news-apple-september-hardware-20260909.json
  - apps/api/app/guides/content/tech-news-taiwan-matsu-cable-tm4-20260918.json
  - docs/tech-news-2026/research/tech-news-taiwan-matsu-cable-tm4-20260918.json
  - docs/news-2026-batch-4/check_article.py
  - docs/news-2026-batch-4/BRIEF.md
---

# Decide the source cap for news maintenance updates, then add Apple 9/18 launch day and moda's TM4 completion release

## Why

Split from `2026-09-19-multi-language-maintenance-update-for-two`。那張票要替兩篇五語系科技新聞各補一節，
馬祖那篇已在 PR 裡做完（換掉一條來源、五語同步、`check_article.py --full --assets` OK）；剩下的兩件事卡在同一條規則：
批次 4 的新聞 `sources` 最多 4 條（`docs/news-2026-batch-4/BRIEF.md`「至少 2 條、最多 4 條」，
`check_article.py` 以 `2 <= len(doc.sources) <= 4` 擋），而且每條都要同一個 `checked_on`。

1. **Apple 9/18 全球開賣**（`tech-news-apple-september-hardware-20260909`）。四條既有來源是四篇 9 月 9 日新聞稿，
   每一篇都獨自承載該產品的台灣售價與規格（2026-10-05 重抓確認：iPhone 18 Pro 稿 NT$44,900／NT$49,900、
   Series 12 稿 NT$13,900、Ultra 4 稿 NT$27,900、AirPods 5 稿 NT$4,490／NT$5,190，各只出現在自己那一篇），
   換掉任何一條都會刪掉有來源的事實；加第五條則違反上限。zh-TW 正文 2,987／3,000 字，也沒有空間。
2. **馬祖 TM4 的數發部完工啟用新聞稿**（`tech-news-taiwan-matsu-cable-tm4-20260918`）。2026-10-05 重抓數發部新聞發布列表時發現，
   9 月 18 日除了票指定的 5G 活動稿（20670，已加進文章）之外，還有一則
   「臺馬第四海纜完工啟用 數發部強化馬祖通訊韌性」（https://moda.gov.tw/press/press-releases/20658）：
   當天上午在連江縣白馬王公園舉行「臺馬第四海纜完工啟用典禮」、行政院長卓榮泰出席；採雙層鎧裝海纜、以埋設深度 2.5 公尺為目標；
   導入結合 AI 辨識與 AIS 的海纜自動預警；臺澎四號、澎金四號預計今年底前完工。這是這篇文章最該引用的一手來源，
   但四個位置已滿（中華電信公告、最新海纜狀況、6 月新聞稿、20670），換掉任一條都會刪掉現有正文的依據。
   PR 已把文章裡會被 20658 推翻的否定句都限縮成「中華電信的公告沒有寫」，FAQ 第五題也從「什麼時候正式啟用」改成只問
   「中華電信有公布臺馬第四海纜的商轉日嗎？」（PR #1267 審查後），所以現在不是錯的，只是少了這則。

規則衝突要在規則層解（原票 Notes），所以先要站主決定，再動文章。

## Definition of done

- [ ] 站主決定其一（用有選項的提問）：(a) 維護更新可以有第 5 條來源（或上限改成 N），`BRIEF.md` 與 `check_article.py` 一起改；(b) 上限不變，Apple 不補這一節（9/18 開始供貨已寫在文章裡，開賣稿只多了「全球直營店正式推出」與紐約 Apple Fifth Avenue 的場面），馬祖不引 20658；(c) 其他。
- [ ] 依決定更新兩篇（或結案說明為什麼不動），五語同步，`check_article.py <slug> --full --assets` 兩篇都 OK。
- [ ] 有改到內容的話：合併後 `guides-import --slug`（update，五語）、正式站驗證（主機 session，站主同意）。

## Steps

- [ ] 問站主 (a)／(b)／(c)。
- [ ] (a) 的話：`BRIEF.md` 寫明「維護更新」的例外與上限，`check_article.py` 的來源上限依同一規則放寬（只放寬更新，不放寬新稿），並在 `tools`／腳本自己的測試或 HANDOVER 留紀錄。
- [ ] Apple：來源 https://www.apple.com/tw/newsroom/2026/09/the-latest-iphone-apple-watch-and-airpods-lineups-arrive-in-stores-worldwide/ ，新小標「9 月 18 日：全球直營店開賣」，只寫開賣日與公告點名的機型；需要騰字數（zh-TW 2,987），而且文章已有五個小節，加一節要先併掉一節（`check_article.py` 要剛好 5 個 level-2；馬祖那篇的做法見其研究紀錄 `update_20261005`）。
- [ ] 馬祖：20658 進 `sources`，第四節「還有哪些沒寫」、callout 與 FAQ 第五題（現在問「中華電信有公布臺馬第四海纜的商轉日嗎？」，可改回讀者真正想問的「什麼時候正式啟用」）改寫成引用 9/18 完工啟用典禮；研究紀錄 `unverified_or_excluded` 裡 20658 那條移到 `verified_facts`。
- [ ] 四語翻譯（`docs/news-2026-batch-4/agents/tech/TRANSLATE.md` 的用語表）與逐語審稿。

## How to verify

```bash
cd apps/api
PYTHONUTF8=1 PYTHONIOENCODING=utf-8 ./.venv/Scripts/python.exe ../../docs/news-2026-batch-4/check_article.py tech-news-apple-september-hardware-20260909 --full --assets
PYTHONUTF8=1 PYTHONIOENCODING=utf-8 ./.venv/Scripts/python.exe ../../docs/news-2026-batch-4/check_article.py tech-news-taiwan-matsu-cable-tm4-20260918 --full --assets
PYTHONUTF8=1 PYTHONIOENCODING=utf-8 ./.venv/Scripts/python.exe -m app.guides.pack_cli lint --kind life --slug tech-news-apple-september-hardware-20260909
```

## Notes

- split from 2026-09-19-multi-language-maintenance-update-for-two（claude-opus-5-5-tech-news-maintenance，2026-10-05）。
- Apple 開賣稿 2026-10-05 實讀：HTTP 200、308,623 bytes；頁面日期列印「2026 年 9 月 18 日」、JSON-LD `datePublished` 2026-09-18Z、`dateModified` 2026-09-29T19:41:31Z。
  原票寫「台灣版發布日 09-19 台北」，今天的頁面沒有「台北」也沒有 9 月 19 日，以頁面為準並在研究紀錄寫明差異。
  正文的事實只有一句：「9 月 18 日星期五，Apple 在全球 Apple 直營店正式推出 iPhone 18 Pro 與 iPhone 18 Pro Max，以及 Apple Watch Series 12、Apple Watch Ultra 4 和 AirPods 5。」
  另一段講 Apple Trade In、Apple Card 分期、Apple Upgrade 等購買方式，是全球稿的翻譯，不代表台灣都有（Apple Card 台灣沒有），不要寫進台灣讀者的文章。
- 20658 的正文 2026-10-05 已讀過（HTTP 200、91,484 bytes），摘要記在馬祖研究紀錄的 `unverified_or_excluded`。
- 兩件事的共同教訓：五語系文章做維護更新，四條來源與 3,000 字都是硬上限，加一節還要先併掉一節。開這種票之前先看來源是不是每條都撐著正文。
