---
id: 2026-09-28-video-1m-ai-agents
title: Million-views batch 3: what an AI agent actually is, what one costs to run, and the setting that keeps it from spending your money
status: blocked
priority: P1
area: docs
owner: claude-fable-5-1
claimed_at: 2026-09-30T03:40:38Z
created_at: 2026-09-28T02:39:11Z
completed_at:
branch: claude/video-1m-production
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

## Independent P1 audit (2026-09-29, codex-p1-video-review)

- Ownership takeover: normal claim refused the recent old claim; root independently confirmed PR #891 merged and no local worktree, branch, remote branch or open PR for `claude/bold-noether-unopy8`. The 4a7e/4f44 active video work concerns different slugs. Root authorized `--force` takeover on `codex/p1-task-audit`; unseen cloud uncommitted work cannot be excluded.
- Independently checked official source bodies and repaired factual contradictions, calculations and unsupported guarantees. Details: `docs/videos/ai-agents-explained-what-they-cost/verify-p1-20260929.md`. Author verify-1 is not accepted as an independent review of this new hash.
- Scoped lint: 0 errors, 0 warnings. No brief, shared lexicon, account, media, TTS or paid-generation changes.
- First-round checkpoint: more than three fact changes required a second independent round; that round is now complete as recorded below. Production acceptance remains unfinished.

## Independent review handoff (2026-09-29)

- Second independent factual review completed by `codex-p1-audit`: `docs/videos/ai-agents-explained-what-they-cost/verify-p1-20260929-round2.md`. It rechecked changed/removed claims and sampled confirmed claims, independently recalculated the five-round illustration, and corrected residual title/description/generalization wording. The latest `video.json` SHA-256 is recorded in that report after final line-ending normalization; earlier hashes remain historical checkpoints.
- Fact checks and scoped lint are repository evidence only. The original incomplete DoD and production checklist remain unchecked: no TTS/audio, render, captions, languages, final QA, upload or player acceptance is inferred. Prices and product-specific limits must be checked again before actual narration/publication.
- Keep the original ticket for unresolved listener/style and opinion/brief findings in both review reports, owner outline/channel-stance decisions, and actual published article CTA/link verification. The owner's production choice remains pending; this handoff authorizes no production, account, paid-generation or publication action.
- Release the review claim to `open` after recording validation, so the next authorized production/editorial session can claim this scope. No duplicate follow-up ticket is needed.
- Final validation with bundled Node **v24.21.0**: scoped lint exited **0**, **0 errors / 0 warnings**, 105 lines, 1,958 spoken units, estimated 8.6 minutes. The six-video receipt is preserved outside the repository at `C:/Users/x8120/.codex/tmp/p1-audit-20260929/six-video-lint-node24.json`.

## 2026-09-30 製作進度（claude-fable-5-1）

- `review-pull` 發現站主 2026-09-28 12:15 UTC 已在 /admin/videos 選了大綱 A（稿子本來就照 A 寫）。
- 聽眾審稿（41 句改寫、16 句新增）→ 旁白合成 → `check-audio`：Gemini 標 15 句，本機 Whisper（faster-whisper medium，venv `~/whisper`，PyAV 19 要拿掉 `metadata_errors`、`PYTHONUTF8=1`）清掉 8 句，剩 7 句改寫重錄後 0 標記 → 旁白關卡自動核准。
- 節奏：真實時間軸有 7 個畫面超過 15 秒，拆場景後 86 個狀態、最長 13.0 秒；render／assemble 乾淨；四語字幕各經翻譯與第二個模型審稿（en 10、ja 16、ko 18 處修正，zh-CN 0）。
- `qa` 11／11，成片關卡自動核准（final.mp4 97b9e5e7d87f）；en／ja／ko 配音 `--line-by-line` 進行中。

- 2026-09-30 晚（claude-fable-5-1）：en／ja／ko 配音都塞進時間軸並逐句檢查：en 0 標記（「cache」一直被聽成 cash，改說 stored context；表格列縮成 "150,000"）、ko 0、ja 剩 2 句（cs5g、8dan，兩個轉寫都聽對，只差 ＝ 的讀法與 申込／申し込み 寫法）。`package` 4／4（metadata.json 0a04ce931276）→ 上架確認自動核准 → 語言卡（en、ja、ko 配音＋四語 CC）已送出、等站主。剩下的是站主的事：照 `upload/UPLOAD.md` 在 Studio 上傳成私人、在「語言」頁加三條配音音軌並在語言卡按「已在 Studio 上傳配音」、在「可以上架」卡貼網址與上架時間。本機工作區 `C:/Users/x8120/mokaair-work/videos/<slug>/`（`upload/`、`dubs/<語系>.m4a`）。
