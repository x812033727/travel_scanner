---
id: 2026-09-28-video-1m-google-vids-free
title: Million-views batch 4: Google Vids makes AI video free with Gemini Omni 1.1, limits and a worked example
status: in-progress
priority: P1
area: docs
owner: codex-p1-video-review
claimed_at: 2026-09-29T02:12:28Z
created_at: 2026-09-28T02:30:46Z
completed_at:
branch: codex/p1-task-audit
depends_on: []
scope:
  - docs/videos/google-vids-free-ai-video-omni-1-1
---

# Million-views batch 4: Google Vids makes AI video free with Gemini Omni 1.1, limits and a worked example

## Why

2026-09-23 起任何 Google 帳號能在電腦版 Google Vids 免費用 Gemini Omni 1.1 生成影片，是高搜尋量的時效題（free AI video、Gemini Omni）。這支示範怎麼做一段，並講清楚四個界線（額度、只在電腦、SynthID 浮水印、只供 Vids 內用），額度部分兩份官方頁不一致（6 支 vs 50 支），影片兩個都列。企劃 `docs/videos/google-vids-free-ai-video-omni-1-1/brief.md` 已寫好。

## Definition of done

- [x] `brief.md` 寫好，流程 steps、四界線、兩份官方頁額度不一致的處理、英文包裝都在。
- [ ] 影片走完全自動路線到「可以上架」，站主上傳，英文配音已上傳。
- [ ] 額度數字在撰稿當天以兩份官方說明頁重查，仍不一致就兩個都列。

## Steps

- [x] 企劃：`brief.md` 已寫好，三個大綱選項、站主觀點、示範或實算、會過期的事實、英文包裝都在（`node` lint 的 outlineOptions 與 checkBrief 通過）。
- [ ] 站主在 `/admin/videos` 設定分頁存好「頻道立場」（若條號和 brief 的「套用立場」不同，改 brief 那一行即可）。
- [ ] 選大綱：`review-push --gate outline`；Jev 依立場挑，或站主選。
- [ ] 撰稿（sonnet）→ 換人查核（opus）→ 聽眾審稿 → `lint` 零錯誤。撰稿當天用瀏覽器重查「會過期的事實」表裡的每個官方頁。
- [ ] tts → check-audio → render → assemble → 五語 CC → `qa` 11 項 → 成片核准。
- [ ] package → 上架確認 → 站主上傳。
- [ ] **配音**：站主在影片頁勾 en（ja、ko、zh-CN 建議一併），工人做多語言音軌（英文市場是這批的重點，別漏勾）。
- [ ] 縮圖先出英文；一支對多語言掛不同縮圖等 `2026-09-28-video-localized-thumbnails` 落地。
- [ ] 重查 Google 說明頁：規格（24fps、720p/1080p、3-10 秒）、額度兩頁數字、上傳影片的地區限制、旁白 coming soon。

## How to verify

```bash
node tools/video/cli.mjs lint --slug google-vids-free-ai-video-omni-1-1
node tools/video/cli.mjs status --slug google-vids-free-ai-video-omni-1-1 --workdir <VIDEO_WORKDIR>
```

## Notes

- 這是「百萬點閱批次」的一支，總規劃在 `docs/videos/MILLION-VIEWS.md`。
- 目標市場是英文，中文旁白服務台灣；靠英文題目搜尋量＋多語言音軌衝點閱，靠站主觀點＋實算守 YouTube 非原創內容政策。
- 撰稿階段會往共用的 `docs/videos/lexicon.json` 加英文詞的唸法；那支檔全批共用，由產線集中處理，本票 scope 只含自己的資料夾，跑到撰稿時再協調（自動產線是單一工人依序做，不會六支同時搶）。
- 官方數字都以撰稿當天重查為準，brief 的「會過期的事實」列了每個要重查的網址。
- 不放實際生成的影片片段（使用範圍未定）；用投影片版型描述流程。
- 記憶點：關分頁前要先把生成片段插進 Vid，否則消失。

## Progress (2026-09-28, claude-opus-5-5)

Pipeline stages 1–4 done: `video.json` (option A, 11 chapters, ~8.2 min, lint 0/0), `claims.md` (c1–c11), `verify-1.md`. Two facts corrected: the usage-scope quote is now the help page's verbatim sentence, and the quota chapter no longer calls the 6-clip figure a personal-account limit (the page labels it Workspace Individual; default is 500 seconds; the generation page says most users get 50). Follow-up filed for the site article: `google-vids-quota-recheck`. Lexicon gained `Lite`, `Vid`, `Individual`. Remaining stages need the owner setup; next is `review-push --slug google-vids-free-ai-video-omni-1-1 --gate outline`.
