---
id: 2026-09-28-video-1m-ai-agents
title: Million-views batch 3: what an AI agent actually is, what one costs to run, and the setting that keeps it from spending your money
status: in-progress
priority: P1
area: docs
owner: claude-opus-4-8
claimed_at: 2026-09-28T04:24:15Z
created_at: 2026-09-28T02:39:11Z
completed_at:
branch: claude/bold-noether-unopy8
depends_on: []
scope:
  - docs/videos/ai-agents-explained-what-they-cost
---

# Million-views batch 3: what an AI agent actually is, what one costs to run, and the setting that keeps it from spending your money

## Why

「AI 代理」是 2026 年英文市場長青高搜尋題（what is an AI agent、AI agent cost）。這支解釋代理跟聊天差在哪、為什麼每輪重讀歷史讓帳單暴增、委託前該問什麼，用一個五輪代理帳單的示意實算當記憶點。企劃 `docs/videos/ai-agents-explained-what-they-cost/brief.md` 已寫好。原本這個檔位是另一個題目，因不適合而換成本題。

## Definition of done

- [x] `brief.md` 寫好，聊天/流程/代理的區分、五輪帳單示意表、委託四問、英文包裝都在。
- [ ] 影片走完全自動路線到「可以上架」，站主上傳，英文配音已上傳。
- [ ] 實算表明確標為「示意，用來說明每輪重讀歷史的結構，不是產品實測」。

## Steps

- [x] 企劃：`brief.md` 已寫好，三個大綱選項、站主觀點、示範或實算、會過期的事實、英文包裝都在（`node` lint 的 outlineOptions 與 checkBrief 通過）。
- [ ] 站主在 `/admin/videos` 設定分頁存好「頻道立場」（若條號和 brief 的「套用立場」不同，改 brief 那一行即可）。
- [ ] 選大綱：`review-push --gate outline`；Jev 依立場挑，或站主選。
- [ ] 撰稿（sonnet）→ 換人查核（opus）→ 聽眾審稿 → `lint` 零錯誤。撰稿當天用瀏覽器重查「會過期的事實」表裡的每個官方頁。
- [ ] tts → check-audio → render → assemble → 五語 CC → `qa` 11 項 → 成片核准。
- [ ] package → 上架確認 → 站主上傳。
- [ ] **配音**：站主在影片頁勾 en（ja、ko、zh-CN 建議一併），工人做多語言音軌（英文市場是這批的重點，別漏勾）。
- [ ] 縮圖先出英文；一支對多語言掛不同縮圖等 `2026-09-28-video-localized-thumbnails` 落地。
- [ ] 撰稿時確認 Agents API 文件仍寫「一個任務呼叫模型多次、重複處理長歷史」「資料落地只支援美國、不支援 ZDR」；GPT-6 Sol 牌價（實算基準）重查。

## How to verify

```bash
node tools/video/cli.mjs lint --slug ai-agents-explained-what-they-cost
node tools/video/cli.mjs status --slug ai-agents-explained-what-they-cost --workdir <VIDEO_WORKDIR>
```

## Notes

- 這是「百萬點閱批次」的一支，總規劃在 `docs/videos/MILLION-VIEWS.md`。
- 目標市場是英文，中文旁白服務台灣；靠英文題目搜尋量＋多語言音軌衝點閱，靠站主觀點＋實算守 YouTube 非原創內容政策。
- 撰稿階段會往共用的 `docs/videos/lexicon.json` 加英文詞的唸法；那支檔全批共用，由產線集中處理，本票 scope 只含自己的資料夾，跑到撰稿時再協調（自動產線是單一工人依序做，不會六支同時搶）。
- 官方數字都以撰稿當天重查為準，brief 的「會過期的事實」列了每個要重查的網址。
- 常青題，不綁單一新聞；可搭任何新代理發布再推一波。
- 記憶點：同一件事「一次問答 0.06 vs 五輪代理 0.95」，差約 16 倍；那個能救命的設定是「預算上限」。

## Progress (2026-09-28, claude-opus-5-5)

Pipeline stages 1–4 done: `video.json` (option A, 7 chapters, ~8.4 min, hook at 0:18, lint 0/0), `claims.md` (c1–c8), `verify-1.md`. Two facts corrected in the check: the OpenAI quote slide now carries the docs' verbatim sentence, and the five-round bill says on screen that it assumes no cache hits (the docs say caching within a session can reuse earlier processing). Lexicon gained `Agents`. Remaining stages need the same owner setup as the price-war video; next is `review-push --slug ai-agents-explained-what-they-cost --gate outline`.
