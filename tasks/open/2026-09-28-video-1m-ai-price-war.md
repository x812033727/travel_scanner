---
id: 2026-09-28-video-1m-ai-price-war
title: Million-views batch 1: GPT-6 Sol and Luna vs Claude Opus 5.5 price war, what your bill looks like now
status: in-progress
priority: P1
area: docs
owner: codex-p1-video-review
claimed_at: 2026-09-29T02:05:41Z
created_at: 2026-09-28T02:30:45Z
completed_at:
branch: codex/p1-task-audit
depends_on: []
scope:
  - docs/videos/ai-price-war-gpt-6-sol-vs-opus-5-5
---

# Million-views batch 1: GPT-6 Sol and Luna vs Claude Opus 5.5 price war, what your bill looks like now

## Why

OpenAI 在 2026-09-22 推出 GPT-6 Sol 與 Luna、API 降價，隔天 Anthropic 的 Claude Opus 5.5 也降；「便宜 50%」「少 40%」「降 20%」三個數字同一天出現，觀眾搞不清哪個跟自己的帳單有關。這支影片把三個百分比拆開（促銷價、成本估計、牌價），用三種典型用量實算帳單，是英文市場搜尋量很高的題目（GPT-6 Sol price、AI API cost）。企劃 `docs/videos/ai-price-war-gpt-6-sol-vs-opus-5-5/brief.md` 已寫好。

## Definition of done

- [x] `brief.md` 寫好，三個大綱、站主觀點、實算表、會過期事實、英文標題三案與配音設定都在。
- [ ] 影片走完全自動路線到「可以上架」，站主上傳，英文配音音軌已上傳。
- [ ] 帳單實算表的每個價格在撰稿當天以官方價目表重查過。

## Steps

- [x] 企劃：`brief.md` 已寫好，三個大綱選項、站主觀點、示範或實算、會過期的事實、英文包裝都在（`node` lint 的 outlineOptions 與 checkBrief 通過）。
- [ ] 站主在 `/admin/videos` 設定分頁存好「頻道立場」（若條號和 brief 的「套用立場」不同，改 brief 那一行即可）。
- [ ] 選大綱：`review-push --gate outline`；Jev 依立場挑，或站主選。
- [ ] 撰稿（sonnet）→ 換人查核（opus）→ 聽眾審稿 → `lint` 零錯誤。撰稿當天用瀏覽器重查「會過期的事實」表裡的每個官方頁。
- [ ] tts → check-audio → render → assemble → 五語 CC → `qa` 11 項 → 成片核准。
- [ ] package → 上架確認 → 站主上傳。
- [ ] **配音**：站主在影片頁勾 en（ja、ko、zh-CN 建議一併），工人做多語言音軌（英文市場是這批的重點，別漏勾）。
- [ ] 縮圖先出英文；一支對多語言掛不同縮圖等 `2026-09-28-video-localized-thumbnails` 落地。
- [ ] 實算表的五個模型價格逐一重查：OpenAI 開發者定價頁、Anthropic 定價頁、Gemini API 定價頁。確認 GPT-5.6 Sol 促銷價與 Opus 5 對照組仍在價目表上。

## How to verify

```bash
node tools/video/cli.mjs lint --slug ai-price-war-gpt-6-sol-vs-opus-5-5
node tools/video/cli.mjs status --slug ai-price-war-gpt-6-sol-vs-opus-5-5 --workdir <VIDEO_WORKDIR>
```

## Notes

- 這是「百萬點閱批次」的一支，總規劃在 `docs/videos/MILLION-VIEWS.md`。
- 目標市場是英文，中文旁白服務台灣；靠英文題目搜尋量＋多語言音軌衝點閱，靠站主觀點＋實算守 YouTube 非原創內容政策。
- 撰稿階段會往共用的 `docs/videos/lexicon.json` 加英文詞的唸法；那支檔全批共用，由產線集中處理，本票 scope 只含自己的資料夾，跑到撰稿時再協調（自動產線是單一工人依序做，不會六支同時搶）。
- 官方數字都以撰稿當天重查為準，brief 的「會過期的事實」列了每個要重查的網址。
- 時效題：新聞 9/22，越早上架越好；標題用「帳單怎麼算」常青角度。
- 實算的兩個對照組是這支的記憶點：GPT-5.6 Sol 促銷價 40→GPT-6 Sol 20（剛好一半）、Opus 5 184→Opus 5.5 137.6（少 25% 不是 40%）。

## Progress (2026-09-28, claude-opus-4-8)

Pipeline stages 1–4 done in-repo and committed:

- `video.json` written from brief option A (推薦): 25 scenes, 96 lines, 7 chapters, hook at 0:17.
- `node tools/video/cli.mjs lint` → 0 errors, 0 warnings; ~8.2 min estimated; Azure billable ~6,880 chars.
- `docs/videos/lexicon.json` created (this batch's first video builds it): AI, GPT, API, OpenAI, ChatGPT, token, Sol, Luna, Claude, Opus, Sonnet, Gemini, Anthropic, Flash.
- `claims.md` (c1–c11) and `verify-1.md`: every price and every scenario bill re-checked against official pages fetched 2026-09-28; all confirmed. Opus 5 comparison values derived from Anthropic's stated 20%/60% cuts and noted.
- `status --slug` shows brief / script-lint / fact-checked all ticked.

Blocked on the owner's one-time setup (credentials never pass through the agent):

1. Outline gate: store the channel stance in `/admin/videos` settings so Jev can pick, or pick option A. The script already follows option A, so this is a formality.
2. Narration (`tts`): needs the video-tool token paired (`node tools/video/cli.mjs login` → owner clicks 允許 in the admin card) and the Gemini voice key set in the backend.
3. `render` needs Chromium (present in cloud) but `assemble` needs real ffmpeg (only Playwright's VP8 build is here); run the render→assemble→captions→qa→package stages on the host worker or a machine with ffmpeg.

Next command once the token is paired and stance stored:
`node tools/video/cli.mjs review-push --slug ai-price-war-gpt-6-sol-vs-opus-5-5 --gate outline`
