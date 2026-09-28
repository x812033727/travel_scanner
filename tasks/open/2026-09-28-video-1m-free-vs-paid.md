---
id: 2026-09-28-video-1m-free-vs-paid
title: Million-views batch 6: free vs paid AI plans 2026, is 20 dollars a month worth it, worked out
status: in-progress
priority: P1
area: docs
owner: claude-opus-4-8
claimed_at: 2026-09-28T04:24:17Z
created_at: 2026-09-28T02:30:47Z
completed_at:
branch: claude/bold-noether-unopy8
depends_on: []
scope:
  - docs/videos/free-vs-paid-ai-plans-2026
---

# Million-views batch 6: free vs paid AI plans 2026, is 20 dollars a month worth it, worked out

## Why

「is ChatGPT Plus worth it」「free vs paid AI」是常青高搜尋題。這支從「你最常撞到哪種額度」出發（ChatGPT 每天 3 檔、Claude 每 5 小時、Gemini 32k 上下文），用五種使用者情境與入門方案價格表給建議，不下單一結論。企劃 `docs/videos/free-vs-paid-ai-plans-2026/brief.md` 已寫好。

## Definition of done

- [x] `brief.md` 寫好，免費版限制表、入門方案價格表、五種情境、付費前三件事、英文包裝都在。
- [ ] 影片走完全自動路線到「可以上架」，站主上傳，英文配音已上傳。
- [ ] 三家方案價格與免費版限制在撰稿當天以官網重查。

## Steps

- [x] 企劃：`brief.md` 已寫好，三個大綱選項、站主觀點、示範或實算、會過期的事實、英文包裝都在（`node` lint 的 outlineOptions 與 checkBrief 通過）。
- [ ] 站主在 `/admin/videos` 設定分頁存好「頻道立場」（若條號和 brief 的「套用立場」不同，改 brief 那一行即可）。
- [ ] 選大綱：`review-push --gate outline`；Jev 依立場挑，或站主選。
- [ ] 撰稿（sonnet）→ 換人查核（opus）→ 聽眾審稿 → `lint` 零錯誤。撰稿當天用瀏覽器重查「會過期的事實」表裡的每個官方頁。
- [ ] tts → check-audio → render → assemble → 五語 CC → `qa` 11 項 → 成片核准。
- [ ] package → 上架確認 → 站主上傳。
- [ ] **配音**：站主在影片頁勾 en（ja、ko、zh-CN 建議一併），工人做多語言音軌（英文市場是這批的重點，別漏勾）。
- [ ] 縮圖先出英文；一支對多語言掛不同縮圖等 `2026-09-28-video-localized-thumbnails` 落地。
- [ ] 重查 ChatGPT（Go/Plus/Pro）、Claude（Pro/Max）、Gemini（AI Plus/Pro/Ultra）方案頁與免費版限制；台幣定價一律「以登入後為準」。

## How to verify

```bash
node tools/video/cli.mjs lint --slug free-vs-paid-ai-plans-2026
node tools/video/cli.mjs status --slug free-vs-paid-ai-plans-2026 --workdir <VIDEO_WORKDIR>
```

## Notes

- 這是「百萬點閱批次」的一支，總規劃在 `docs/videos/MILLION-VIEWS.md`。
- 目標市場是英文，中文旁白服務台灣；靠英文題目搜尋量＋多語言音軌衝點閱，靠站主觀點＋實算守 YouTube 非原創內容政策。
- 撰稿階段會往共用的 `docs/videos/lexicon.json` 加英文詞的唸法；那支檔全批共用，由產線集中處理，本票 scope 只含自己的資料夾，跑到撰稿時再協調（自動產線是單一工人依序做，不會六支同時搶）。
- 官方數字都以撰稿當天重查為準，brief 的「會過期的事實」列了每個要重查的網址。
- 不談 API 價格（那是批次第 1 支）；這支只講訂閱方案。
- 記憶點：先用滿免費版兩週再決定；卡的地方決定你付哪一家。
