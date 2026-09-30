---
id: 2026-09-28-video-1m-free-vs-paid
title: Million-views batch 6: free vs paid AI plans 2026, is 20 dollars a month worth it, worked out
status: in-progress
priority: P1
area: docs
owner: claude-fable-5-1
claimed_at: 2026-09-30T03:40:59Z
created_at: 2026-09-28T02:30:47Z
completed_at:
branch: claude/video-1m-production
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

## Progress (2026-09-28, claude-opus-5-5)

Pipeline stages 1–4 done: `video.json` (option A, 10 chapters, ~8.1 min, lint 0/0), `claims.md` (c1–c12), `verify-1.md`. Claude and Gemini figures are confirmed on today's official pages. **Blocker before `tts`:** the ChatGPT figures (free tier 3 files a day, Go $8, Plus $20 with Codex, cancellation rules) come from the site article's 2026-09-13 check, because openai.com, chatgpt.com and help.openai.com return 403 from this environment. Recheck them in a browser, or run the independent verifier where OpenAI is reachable, and clear the PENDING rows in `claims.md`. One unverified line (every surface sharing one Claude quota) was replaced with the Pro page's own wording. Lexicon gained `Code`, `Flow`.

## Independent P1 audit (2026-09-29, codex-p1-video-review)

- Ownership takeover: normal claim refused the recent old claim; root independently confirmed PR #891 merged and no local worktree, branch, remote branch or open PR for `claude/bold-noether-unopy8`. The 4a7e/4f44 active video work concerns different slugs. Root authorized `--force` takeover on `codex/p1-task-audit`; unseen cloud uncommitted work cannot be excluded.
- Independently checked official source bodies and repaired factual contradictions, calculations and unsupported guarantees. Details: `docs/videos/free-vs-paid-ai-plans-2026/verify-p1-20260929.md`. Author verify-1 is not accepted as an independent review of this new hash.
- Scoped lint: 0 errors, 0 warnings. No brief, shared lexicon, account, media, TTS or paid-generation changes.
- First-round checkpoint: more than three fact changes required a second independent round; that round is now complete as recorded below. Production acceptance remains unfinished.

## Independent review handoff (2026-09-29)

- Second independent factual review completed by `codex-p1-news` / `audit_video`: `docs/videos/free-vs-paid-ai-plans-2026/verify-p1-20260929-round2.md`. All changed/removed groups and the random confirmed sample were rechecked against official sources; the current script needed no further factual changes. The latest `video.json` SHA-256 is recorded in that report after final line-ending normalization; earlier hashes remain historical checkpoints.
- The first-round report's unrelated Flash 3.8 API-promotion sentence was removed as a report-only correction, with a note. This did not alter the script, brief or approval hash.
- Fact checks and scoped lint are repository evidence only. The original incomplete DoD and production checklist remain unchecked: no TTS/audio, render, captions, languages, final QA, upload or player acceptance is inferred. Subscription prices/access must be checked again before actual narration/publication.
- Keep this ticket for unresolved listener/style and opinion/brief findings in both review reports. These include the opening's three-minute promise versus the 8.3-minute estimate, unqualified quality/free-sufficiency recommendations, and the unverified source-article CTA/update promise. Owner outline/channel-stance acceptance and the owner's production choice remain pending; this handoff authorizes no production, account, paid-generation or publication action.
- Release the review claim to `open` after recording validation, so the next authorized production/editorial session can claim this scope. No duplicate follow-up ticket is needed.
- Final validation with bundled Node **v24.21.0**: scoped lint exited **0**, **0 errors / 0 warnings**, 102 lines, 1,888 spoken units, estimated 8.3 minutes. The six-video receipt is preserved outside the repository at `C:/Users/x8120/.codex/tmp/p1-audit-20260929/six-video-lint-node24.json`.

## 2026-09-30 製作進度（claude-fable-5-1）

- 站主 2026-09-28 12:14 UTC 在 /admin/videos 選了大綱 **B**（同樣 20 美元），稿子重寫（sonnet）→ 查核一輪（59 確認、1 修正）→ 聽眾審稿（含把「重度使用者」那段拉回 brief 的立場）。
- 旁白：Gemini 標 21 句，Whisper 清 12 句，9 句改寫重錄；「十二萬八千」兩個轉寫都聽成兩萬八，改成「128K，也就是十二萬八千」加 `say` 才過；0 標記。
- 節奏 87 個狀態最長 13.6 秒；四語字幕翻譯＋審稿（en 19、ja 21、ko 12、zh-CN 0 處修正）。
- `qa` 起初 9／11：`facts` 讀的是 09-28 A 案的 `verify-1.md`（c2、c5、c12 在那份是 NOT FOUND）→ 今天的報告改名 `verify-1.md`；`links` chatgpt.com/pricing 對檢查程式 403 且價格本來就來自 learn.chatgpt.com，從 sources 拿掉。之後 11／11，成片關卡自動核准（39753d7931a0）；配音進行中。
