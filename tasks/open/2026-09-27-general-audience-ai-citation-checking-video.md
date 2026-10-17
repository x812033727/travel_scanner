---
id: 2026-09-27-general-audience-ai-citation-checking-video
title: General audience AI citation checking video
status: blocked
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-09-27T15:26:42Z
completed_at:
branch: codex/ai-citation-completion-20261007
depends_on: []
scope:
  - docs/videos/ai-citation-check
---

# General audience AI citation checking video

## Why

有連結的 AI 回答仍可能把來源說反。以明確標示的錯誤示意回答，逐步核對 Anthropic 官方原文，教一般觀眾檢查引用。

## Definition of done

- [ ] 8–12 分鐘繁中影片、縮圖與五語字幕通過產線檢查，完整上傳包可交站主。
- [x] 示意回答與真實來源清楚標示，獨立查核完成。

## Steps

- [x] 查重並打開官方來源，建立可回查的三步查核示範。
- [x] 完成 brief、video.json、claims 與查核交接。
- [ ] 完成聲音、畫面、字幕、品管與上傳包。

## How to verify

`node tools/video/cli.mjs lint --slug ai-citation-check`；成片再跑 `qa`、`package`、人工逐段檢查。

## Notes

### 2026-10-07 actual continuation

Free blind offline Whisper actually closed with exit 0 at 10:15:58 UTC: exact 143-file order and every input WAV digest unchanged. Comparison only followed the frozen blind transcripts; 97 exact, 24 sound-equivalent and 22 unresolved ASR differences. Fourteen need priority listening; eight other differences have current digest-matching native transcripts that mechanically match. offline-audio-review-20261007.md records movie timestamps and limits. This establishes no native/Jev/owner approval.

Current reviewable movie: `<home>\mokaair-work\ai-teaching-continuation-20261007\render-preview\ai-citation-check\final.mp4`, 18,596 frames / 10:19.867, SHA-256 fdc4afbcee830e7990805c89dbf0424fc067efc62d6a295abd17f66354410ca5. The actual second native assembler closed with exit 0 at 09:58:09Z; -14 LUFS / -1 dBFS, 108 slide samples, zero assembly problems. This is an unapproved local draft.

The original 143 Mandarin lines and all raw WAVs are unchanged. Visual-only corrections produce 67 states, maximum 14.933s, and clear the lower subtitle area. Eleven foreign-text corrections were independently reviewed across all 572 entries and actual five-language SRTs, with zero caption problems. Fresh primary sources, full metadata bytes, SHA-bound language, visual and artifact reviews are retained in docs/videos/ai-citation-check. Start with continuation-receipt-20261007.md; current metadata-draft-20261007.json is a native composer draft, not upload/metadata.json.

Paid check-audio remains held: 68/143 primary transcript rows, no completed judge loop or audio approval. The exact ci037 request key 5f7cbb48ab7a326474e12293c3748be97720963d6bdbf619f3177362a929c037 is still sent without a retained answer. Canonical STOP and original journal remain preserved. Local/host read-only audit found no durable answer retrieval. A duplicate-charge retry decision was requested only after the actual draft was ready; absence of a reply authorizes no resend/reset.

Free native diagnostic QA: 9/11, native result 3. Narration is unapproved; policy deliberately unrun with absent diagnostic credentials and GET/HEAD-only fetch. This does not establish an actual account/token failure or an 11-item pass. The actual upload package, final/publish approval, owner language selection, full watching/listening, Studio operation and publication remain pending; keep both combined completion checkboxes unticked.

The partial native summary also incorrectly counts five unmatched transcripts with null judge scores as judged_fine. It was not submitted; separate ticket 2026-10-07-audio-review-distinguishes-transcripts-awaiting-a records the free reproducible defect. Historical 2026-09-28 completion notes below are not retained current media evidence.

示範錯誤句是編輯刻意製作，不宣稱為真實模型輸出。2026-09-27 已打開 Anthropic 官方 Reduce hallucinations 頁與 Building effective agents 頁。前者要求引用能回查，並說這些方法不能完全消除錯誤。

文字包在 `docs/videos/ai-citation-check/`。`lint` 0 錯 0 警、預估 9.9 分鐘（143 句）；四語 `.todo.json` 已生成於 repo 外 `<home>\mokaair-work\videos\ai-citation-check\i18n\`。獨立 `verify-1.md`、大綱核准、翻譯審稿、TTS、成片及上傳包仍未完成；`status` 逐項顯示缺口。

2026-09-27 獨立查核已寫入 `verify-1.md`：Anthropic 官方文件現頁 HTTP 200，必要短引文、限制與示意標示一致；`lint` 重跑為 0 錯 0 警。音訊、畫面、字幕與上架包仍待完成。
2026-09-28：五語字幕經獨立交叉審稿；兩句顯示過快的英、日文字幕已縮短，五語 SRT 無速度警告。繁中旁白 10:22；36 張字卡與縮圖已目視檢查。成片、品管、審核與上架包仍待完成。
2026-09-28：改寫五句並同步五語字幕，獨立覆核後重錄；`check-audio` 143/143 句、零標記。新版成片 18,749 影格、約 10:24、-14 LUFS，`lint` 零錯誤零警告。站主大綱核准、正式站審核、11 項品管及待上架包仍待完成。
- 2026-10-04 board sweep (claude-opus-5-5-incomplete-tickets, approved by the owner): the claim by codex-video-review (since 2026-09-27T15:48:03Z) was stale and is released so it stops locking its scope. Landed: #867. Still open: 8–12 min video, thumbnail and five-language subtitles pass pipeline checks; complete upload package handed to ; Finish audio, visuals, subtitles, QA and upload package (render, 11-item QA, owner outline approval, productio.

2026-10-07 continuation: fresh main, open PRs and 25 worktree changes were checked before the new claim. The original source files remain frozen. The actual production outline review `948b2d65-6c71-4a62-a338-6fb4f5fd3de9` is approved; native `review-pull --gate outline` verified the brief hash and recorded outline A locally. Media and durable command receipts live outside Git in `<home>\mokaair-work\ai-teaching-continuation-20261007\`. The 2026-09-28 media completion notes are historical and do not prove that those files still exist or have current QA.
