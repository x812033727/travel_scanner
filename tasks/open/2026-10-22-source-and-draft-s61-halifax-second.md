---
id: 2026-10-22-source-and-draft-s61-halifax-second
title: Source and draft S61 Halifax second-blast warning episode
status: in-progress
priority: P2
area: docs
owner: codex-s61-new-episode
claimed_at: 2026-10-22T00:45:06Z
created_at: 2026-10-22T00:45:03Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/curio-s61
---

# Source and draft S61 Halifax second-blast warning episode

## Why

The owner asked to keep making new Curio history episodes. S61 asks why people in Halifax heard a warning of a **second** explosion after the 1917 harbour blast, and what the fixed 1920 relief participant's study actually proves about the fire-threatening naval magazine and its treatment. Do not turn a warning into an explosion or claim a complete independent military inquiry has been checked.

## Definition of done

- [x] A source-bound, distinct author candidate has a pinned full text, A/B outline, 106 spoken lines, line-level claims, 30–60-second condensed opening, 8–12-minute estimated body, music and end-screen plan, and zero-error/zero-warning video lint.
- [ ] Independent source and written-visual review, two fresh blind narrative readers, formal merge and policy gate accept the frozen script.
- [ ] Owner/site audio review, native illustrations, music, final long cut and Short, package QA and actual Studio end-screen links are complete.

## Steps

- [x] Check S01–S60 and the topic index for overlap; reject Carrington because direct 1859 sources were inaccessible here, and reject S48's 1858 Atlantic-cable story as overlap.
- [x] Pin Samuel Henry Prince's 1920 Halifax field study to GITenberg commit `befb706982ba1be631a52d4f686be301c2de7f34`, raw `37580.txt` SHA-256 `97484e988437d13a4f5a72d5c2edbf1c594ea8dff4c5b239d8b17b7c62c29b52`; keep it clear that Prince's book itself combines his observations and cited descriptions.
- [x] Draft `brief.md`, `research.md`, `video.json`, `script.md`, `claims.md` and author handoff under `docs/videos/curio-s61/`.
- [x] Self-check every written picture against its own spoken line, then lint: 0 errors, 0 warnings; R6 has 106 lines, 96 illustrated shots and 7 information cards. At fast 325 CPM its first chapter is 48.03 seconds and post-opening body is 484.70 seconds; at 250 CPM the body is 601.57 seconds.
- [x] Independent R1 source/visual review found a naval-affiliation error; R2 author corrected it and another worker independently PASSed the fixed Prince attribution and all changed written visuals on frozen hashes.
- [x] Two isolated R2 blind readers and formal merge found shared narrative failures (`no_toc`, `chapters_link`, `payoffs`, `no_recap`, `no_detour`), despite R2 source/visual PASS.
- [x] R3 author repaired the narrative on new hashes, added P14 for source-bound rescue organization, and kept prompt/claim alignment and lint 0/0.
- [x] R3 independent source/visual review PASSed after a citation-only P14 extension through Prince L2023; formal R3 dual-blind merged 11/13 and held on shared `chapters_link` and `no_recap` (one reader also flagged `no_toc`, `one_thread`, `no_detour`).
- [x] R4 author rewrote chapter seams, removed repeated details, shortened relief/shelter to consequences of the warning, and kept the final Prince attribution source-bound.
- [x] R4 independent source/visual PASSed, but fresh formal dual-blind narrative OR merged 11/13 and held on shared `no_recap` and `no_detour`; reader A additionally flagged a missed injured-evacuee payoff.
- [x] R5 author moved the no-second-blast answer immediately after the all-clear, trimmed after-alert rescue/shelter to five lines with explicit opening callbacks, removed duplicate warning/return lines, and added fixed-text first-blast and early-aid details to keep the body over eight minutes.
- [x] R5 independent source/visual review isolated one error at `s61130` (two groups wrongly merged into one); R5 blind diagnostics were not valid formal votes and flagged payoff/repetition issues.
- [x] R6 author repairs the two-group source error, cuts repeated beats, pins additional Prince details to each new line and written visual, and freezes an exact reversible R5→R6 delta.
- [ ] Have two new isolated blind readers and a new independent source/visual reviewer assess frozen R6, then follow media gates before spending.

## How to verify

From repository root: `VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s61 --json`; `VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs script --slug curio-s61`; `npm run check:tasks`. The R6 author lint returned 0 errors/0 warnings, 106 lines, 11.2989 estimated minutes at the tool's standard pace. Compare `claims.md` line text against `video.json` and the fixed text before any approval.

## Notes

2026-10-22: The GITenberg fixed copy was downloaded through the GitHub API to `/tmp/s61-halifax-prince.txt` and its SHA-256 checked. The book's preface (L90–110) says it is a social study, not a complete disaster history; Prince says he participated in Halifax rescue (L766–773). It records the powder-magazine warning (L951–974), crowd/army movement (L1356–1406), and attributes the absence of a second explosion to an entire artillery battery volunteering to flood the magazine in the naval yard (L1824–1836). The candidate explicitly attributes that causal claim to Prince; no independent military action log was obtainable in this task. It does not name a precise order, valve, distance, death toll from the warning, or identifiable survivor in art.

The source-rich fallback replaced 1859 Carrington: ADS and Wikisource were blocked by this environment's proxy 403, while GitHub search yielded later summaries but no fixed 1859 astronomy and telegraph first-person pair. S48 already covers the 1858 Atlantic cable. No paid TTS, MiniMax, judge, music, website approval, final video or YouTube upload has been performed for S61. Brand intro/outro assets and the actual clickable links are planned only; they are not outputs of this author draft.

2026-10-22 R2 independent [source/visual PASS](../../docs/videos/curio-s61/review/r2-independent-source-visual.md): video SHA-256 `800a8c7476bee77fad9b97e8a23e5b7e26007cfcf32e5ee471db371257fec134`, no claimed navy affiliation for the volunteer battery, naval yard retained only as the magazine location; six repaired prompts omit unsupported hose operations. R2 lint 0/0. The R2 formal dual-blind merge held on five shared narrative failures. R3 removes the numbered exposition, makes chapter starts answer preceding questions, pays off fire proximity and who assumed command, defers the no-second-blast finding until the end, and replaces the rail/telegraph inventory with Prince’s assigned-area search account (P14). R3 independent source/visual PASSed after the P14 L2023 citation repair, but formal dual-blind merged only 11/13 and held on chapter linkage and repeated facts; one reader also flagged the broad relief/shelter detour. R4 fixed opening and closing seams and anchored new port and warning details to Prince; independent R4 source/visual PASSed, but formal dual-blind merged 11/13 and held on repetition and the post-alert rescue/shelter detour. R5 answers the second-blast question immediately after the all-clear, leaves only five short source-bound callback lines afterward, and uses additional Prince details of blast damage, communication loss and first aid to preserve an eight-minute body. Fresh R5 review is pending; no media gate is approved.

R5 [獨立史料與書面畫面覆核](../../docs/videos/curio-s61/review/r5-independent-source-visual.md)判 **史料 HOLD 僅 `s61130`**：Prince L1363–1365 分別說有人跑向店鋪、原在店裡的人跑回家；稿中「先…又…」誤合為同一群人。其餘 96 句、87 圖與 7 卡通過紙審，須窄修兩群人的台詞後重核。R5 [盲讀 A](../../docs/videos/curio-s61/review/r5-isolated-blind-a.receipt.json)與[盲讀 B](../../docs/videos/curio-s61/review/r5-isolated-blind-b.receipt.json)只保留編輯診斷：正式題目未在原始答題前交付；A 11／13 自訂檢查、B 後綁正式題目 11／13 並指出 `payoffs/no_recap`，**都不計正式票**。R6 須先修來源及重述／回收，再把固定 13 題先交兩名未看舊票的隔離讀者；媒體仍待。

2026-10-22 R6 作者依 R5 HOLD 將 `s61130` 明確改為「有人跑向店鋪；店裡的人則趕回家」，避免合併兩群人。前半段增加 Prince 固定全文裡的戰時船隊、蒙布朗號與伊莫號載貨差別、首次示警缺口、爆炸對城堡／列車的衝擊，以及最初醫療船、訪客和本地居民不同的救援起點；撤離段加入手稿裡孩子、臥床者、仰望天空者的處境，片尾明確以解除通報後的白帳與教堂大廳回收「何處暫停」。緊接安全通報說明第二次爆炸沒有發生，仍把砲兵隊灌水的因果歸於 Prince，而不冒稱核實軍方紀錄。R6 完整檔案與可逆差異見 [作者交接](../../docs/videos/curio-s61/review/r6-author-narrative-repair.md)，待全新獨立覆核；無付費媒體。
