---
id: 2026-10-20-curio-s44-primary-source-preproduction
title: Curio S44 primary source history episode preproduction
status: in-progress
priority: P2
area: docs
owner: codex-s44-script
claimed_at: 2026-10-20T10:55:24Z
created_at: 2026-10-20T09:24:37Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/curio-s44
---

# Curio S44 Broad Street pump and cholera source preproduction

## Why

John Snow's 1855 firsthand account says the Broad Street pump handle was removed on 8 September 1854, while new fatal attacks were already falling. The usual one-action cure story therefore needs a source-bound correction. Build an 8–10 minute single-investigation history episode that follows his questions, records, exceptional households and cautious conclusion. Only this ticket and `docs/videos/curio-s44` are in scope; S41/S43 and shared topic-bank files belong to other workers.

## Definition of done

- [x] Independently checked, fixed 1855 source text and A/B site-readable outline; source boundaries distinguish observation from inference. Scene-level claims wait for the owner's outline choice.
- [x] One estimated 8-minute-plus narration body with 30–60 second condensed opening, installed-branding plan, at least 70% illustration shots, source/channel links and a one-Short draft; real duration remains for audio measurement.
- [x] Two independent exact-script blind reads and an independent full source/visual review plus exact-version deltas; local lint and tests pass; scope-only commit and push.
- [x] Hand off the **outline** to the manual site gate; site chose A at 2026-10-20 10:36:26 UTC. Script site gate and paid TTS/art/music remain downstream of exact-script checks and script approval.

## Steps

- [x] Search S01–S43 and H/M/P/U/L topic bank for the same Snow/Broad Street story; create and claim S44 scope.
- [x] Reopen and independently verify pinned GITenberg transcription and map image; record exact line ranges and evidentiary limits.
- [x] Draft parser-ready A/B brief and submit the outline to manual review; **pending owner**.
- [x] After owner choice, draft scene-by-scene claims, script and shot plan; run local checks.
- [x] Freeze exact hashes for two source-isolated narrative readers and separate source/visual reader, then record receipts.
- [x] Submit outline through supported manual site gate; site approved A at 2026-10-20 10:36:26 UTC.
- [x] Push only S44 files and this task file (`21fe9dd475927f552747188a646c0a18fbe49cf5`).

2026-10-20 A 案後續：`review-pull --gate outline` 讀回網站於 10:36:26 UTC 選 A、核准原 `brief.md` SHA。現行 v5 `video.json` SHA `6572e05b1deb0ba86bbb7b3aea507e04ca8bc51af9af41e7432d9defd866c16c`，`script.md` SHA `0b5053192d0ca3747811bb789dbde224bc83ba8307708b61f89843d075a37651`，逐版獨立來源／畫面查核和先前失敗盲讀的精確收據見 `docs/videos/curio-s44/verify-1.md`。93 正文景（83 圖／10 卡）、39 秒濃縮開場、約 8:34 後續故事正文、18 伏筆、一支 8 景 Short 草案；lint 0 error／1 中性片尾口播警告。獨立讀者對舊版 `snow032` 過度歸於家屬供詞、後續酒廠回收和重複口播的問題均促成具體修訂；完整 v2 史料／視覺查核、v3–v5 精確差分及兩位現版全新盲讀均已通過；網站 script gate 已送審且仍 pending。TTS 僅 dry-run 96 句／約 2,200 字元；圖 83 張 × 最多 3 次約 US$3.36，加配樂約 US$0.08，**媒體費用仍 US$0**。`test:docs-videos` 236/236、`check:tasks` 2113 valid。

2026-10-20 11:34 UTC 完稿關卡：v5 `video.json`、`script.md` 維持上列 SHA；完整 v2 史料／視覺查核和 v3、v4、v5 精確差分均 PASS（v5 根節點獨立收據 `/tmp/s44-v5-root-independent-source-visual-delta.md` SHA `327cc5ee52320a310bc917fdbb747802e309f2529f3050f9c1d5feb4be447db2`）。兩位互不共用 S44 背景的全新讀者各給 13/13 yes，官方本地 narrative 合併紀錄 SHA `e76849d1b0da85cc0f1a8cb100cfa629185ace2828d62354bd1844c4acb02988`，`readers:2`；細節見 `verify-1.md`。站台 `review-push --gate script` 已提交精確稿，狀態 `pending`，`review-pull` 回 `waiting for the owner` exit 3；**尚非核准**。未執行 S44 TTS、付費圖片、配樂、成片或上傳，媒體費 US$0。

## How to verify

Compare pinned source SHA-256 to `research.md`; reopen every linked line range. Run `VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s44`, the narrative check, `npm run test:docs-videos` and `npm run check:tasks`. Use site report-only preflight before manual outline push; `pending owner` is not approval.

## Notes

2026-10-20: Independent new task claim `codex-s44-source`. Initial dedup search found only incidental cholera in S26, no Snow or Broad Street episode. Proposed title question: 「1854 年醫生拆掉水泵把手，真的立刻止住霍亂？」 Fixed source is John Snow, *On the Mode of Communication of Cholera*, enlarged second edition (1855), GITenberg commit `6a27453cc0bb85c3fc125c5e13900c8f3a8b48db`, raw `72894-0.txt` SHA-256 `3f3e71972f603e5fa50a0e71045afffa994ae38a86a8912dda3e90c8babb37af`. Snow's own attack table and text at lines 1655–1767 say attacks had fallen before the handle was removed and he could not decide if the well still carried active cholera; preliminary chapter at 1344–1545 supplies his field investigation. Site/paid media not started.

2026-10-20 outline handoff: Two independent read-only scouts re-fetched the exact Snow text; one also checked the 1855 printed map image and the other checked S01–S43 plus H/M/P/U/L bank for overlap. They corroborated the hard boundaries: Snow's first edition was 1849, the later map includes deaths through 30 September, the 616-case table counts **fatal attacks** with partly inferred onset, the 8 September handle removal followed a descending curve, and Snow could not prove its instantaneous effect or the contamination route. Exact citations are in `docs/videos/curio-s44/research.md`. Brief parser finds complete A/B; `review-push --report-only` succeeded, `--gate outline` returned Jev A 1.00 but **pending owner**, and `review-pull` returned `waiting for the owner` (exit 3). Bound brief SHA `44f332d8c1a4d50550c4ba17927964523ed0a7a2fc0a2ebf5227fba898ff63de`; details in `docs/videos/curio-s44/verify-site-gates.md`. A local R0 scene draft was moved to `/tmp/s44-preoutline-draft-20261020/` and was deliberately not committed: lint found unresolved names and cadence warnings, and no narrative or full source/visual check exists. Do not use it for site script or media. Next action after the owner picks A or B: write and fully audit that exact script, then submit manual script gate. No paid media or media assets for S44.

2026-10-20: Source/outline/site receipt scoped commit `21fe9dd475927f552747188a646c0a18fbe49cf5` is on the shared remote branch. A concurrent worker's push returned a ref-lock race to this worker, but `git ls-remote` then read back this exact SHA from the remote. No S41/S43 files were staged in this commit.
