---
id: 2026-10-20-brand-story-netflix-x03
title: 製作 Netflix 郵寄 DVD 轉串流品牌故事 X03
status: open
priority: P1
area: docs
owner:
claimed_at:
created_at: 2026-10-20T10:42:12Z
completed_at:
branch: codex/brand-story-netflix-x03
depends_on: []
scope:
  - docs/videos/story-everyday-netflix-x03
  - tasks/open/2026-10-20-brand-story-netflix-x03.md
---

# Netflix X03：郵寄 DVD 還在成長時，為何開出電腦即看？

## Why

站主要求品牌故事逐支製作並在完成後開 PR。X03 是既有二十集之外的補充題，與 C01 Crocs、C02 特百惠、X01 Adobe Creative Cloud、X02 Domino’s 的核心反轉不同；本集只追 Netflix 從郵寄 DVD 與線上即看並行，到把串流列為核心策略、最後結束寄片的可查時間線。另一系列的 Blockbuster 拒買 Netflix 題講的是 2000 年收購談判，不是本集主線。

## Definition of done

- [ ] 四份 SEC 原始申報支撐六章主線與逐句史實，獨立代理按最終內容雜湊查核，兩位敘事讀者和 `lint` 通過。
- [ ] 在單支 US$25 硬上限內，完成至少八分鐘正文、30–60 秒濃縮開場、MiniMax `image-01` 插圖、配樂、5 秒片頭、21 秒片尾、1080p 試片與可關閉的繁中字幕。
- [ ] 完成音訊、畫面、格式、成本與來源 QA，交付上架包；正式品牌素材與 YouTube 可點片尾連結仍依站主／Studio 流程驗證。

## Steps

- [x] 建立四份 SEC 原件筆記、題材去重、製作簡報和六章 Treatment（X03 pipeline 第一階段）。
- [ ] 請獨立查核者複核原件引文、訂戶／寄送／觀看／營收單位與六章因果，留下綁定目前前製內容的收據。
- [ ] 寫繁中逐句稿、場景提示詞、至少八組伏筆、數字卡與 YouTube 文案，綁定定稿 SHA 做來源審查和盲讀。
- [ ] 在付費前跑整片 TTS、圖片和配樂乾跑，將語音、轉錄、查核、插圖、評審、重做、音樂和稅費合計守在 US$25 內。
- [ ] 生成媒體、檢查旁白、合成概念試片與字幕，完成整檔 QA、交接和 PR。

## How to verify

前製先核對 [`source-notes.md`](../../docs/videos/story-everyday-netflix-x03/source-notes.md) 的 SEC 連結、引文、年末訂戶數與不同計量範圍，並審閱 [`brief.md`](../../docs/videos/story-everyday-netflix-x03/brief.md) 及 [`treatment.md`](../../docs/videos/story-everyday-netflix-x03/treatment.md)。定稿後才建立 `video.json`、跑 `node tools/video/cli.mjs lint --slug story-everyday-netflix-x03` 和影片工具的付費乾跑；媒體完成後核對音訊、字幕、影格、解碼、台帳，並跑 `npm run test:docs-videos`、`npm run check:tasks`。

## Notes

2026-10-20：本分支從 `origin/main` 建立；**X03 pipeline 第一階段**已完成來源筆記、brief 與六章 Treatment，交給下一位製作者做獨立查核。X03 仍是**前製候選**，尚無完整逐句劇本、獨立查核收據、付費呼叫、媒體或上架核准。四份 Netflix SEC 10-K 已唯讀開啟並回 HTTP 200；2007 年寄出 DVD 總片數比 2006 年增 20%，但每名平均付費訂戶每月租片數下降，不能把後者歸因串流。2007 年末約 750 萬訂戶不可寫成 2007 年一月推出即看時的數量；2010 年「多數訂戶各自透過串流看的內容多於 DVD」不是營收占比；2023 年美國寄片收入與全球串流收入不能當相同市場分母比較。頻道即時影片清單在此雲端仍不可讀，僅能按儲存庫既有題庫去重。
