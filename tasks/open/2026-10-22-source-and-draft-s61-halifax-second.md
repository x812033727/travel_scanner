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
- [ ] Independent source and written-visual review, two fresh blind narrative readers, formal merge and policy gate accept the frozen script. R9 source/written-visual and formal narrative checks now PASS; policy remains pending.
- [ ] Owner/site audio review, native illustrations, music, final long cut and Short, package QA and actual Studio end-screen links are complete.

## Steps

- [x] Check S01–S60 and the topic index for overlap; reject Carrington because direct 1859 sources were inaccessible here, and reject S48's 1858 Atlantic-cable story as overlap.
- [x] Pin Samuel Henry Prince's 1920 Halifax field study to GITenberg commit `befb706982ba1be631a52d4f686be301c2de7f34`, raw `37580.txt` SHA-256 `97484e988437d13a4f5a72d5c2edbf1c594ea8dff4c5b239d8b17b7c62c29b52`; keep it clear that Prince's book itself combines his observations and cited descriptions.
- [x] Draft `brief.md`, `research.md`, `video.json`, `script.md`, `claims.md` and author handoff under `docs/videos/curio-s61/`.
- [x] Self-check every written picture against its own spoken line, then lint: 0 errors, 0 warnings; R9 has 106 lines, 96 illustrated shots and 7 information cards. At fast 325 CPM its first chapter is 48.23 seconds and post-opening body is 487.13 seconds; at 250 CPM the body is 604.73 seconds.
- [x] Independent R1 source/visual review found a naval-affiliation error; R2 author corrected it and another worker independently PASSed the fixed Prince attribution and all changed written visuals on frozen hashes.
- [x] Two isolated R2 blind readers and formal merge found shared narrative failures (`no_toc`, `chapters_link`, `payoffs`, `no_recap`, `no_detour`), despite R2 source/visual PASS.
- [x] R3 author repaired the narrative on new hashes, added P14 for source-bound rescue organization, and kept prompt/claim alignment and lint 0/0.
- [x] R3 independent source/visual review PASSed after a citation-only P14 extension through Prince L2023; formal R3 dual-blind merged 11/13 and held on shared `chapters_link` and `no_recap` (one reader also flagged `no_toc`, `one_thread`, `no_detour`).
- [x] R4 author rewrote chapter seams, removed repeated details, shortened relief/shelter to consequences of the warning, and kept the final Prince attribution source-bound.
- [x] R4 independent source/visual PASSed, but fresh formal dual-blind narrative OR merged 11/13 and held on shared `no_recap` and `no_detour`; reader A additionally flagged a missed injured-evacuee payoff.
- [x] R5 author moved the no-second-blast answer immediately after the all-clear, trimmed after-alert rescue/shelter to five lines with explicit opening callbacks, removed duplicate warning/return lines, and added fixed-text first-blast and early-aid details to keep the body over eight minutes.
- [x] R5 independent source/visual review isolated one error at `s61130` (two groups wrongly merged into one); R5 blind diagnostics were not valid formal votes and flagged payoff/repetition issues.
- [x] R6 author repairs the two-group source error, cuts repeated beats, pins additional Prince details to each new line and written visual, and freezes an exact reversible R5→R6 delta.
- [x] R6 independent source/visual reviewer PASSed 103 factual lines, 96 written visuals and 7 cards; two new official isolated blind readers each marked 11/13, with formal OR 12/13 HOLD solely on common `no_recap`.
- [x] R7 author substitutes new sourced actions for repeated s61028/31 and s61054/61 beats, reworks the opening and Common shelter payoff, replaces the s61059 recap card, and fixes direct source anchors at s61008 and s61026. Freeze exact R6→R7 reversible delta and lint 0/0.
- [x] R7 independent source/visual review held one unsupported citywide-alarm word; R8 author removed it, and the new independent source/visual reviewer PASSed frozen R8.
- [x] Two new official isolated R8 blind readers froze separate 13-question votes before CLI; formal OR merged 12/13 HOLD solely on shared `no_recap`.
- [x] R9 author replaces `s61123`'s repeated rubble fact with Prince's crimson northern sky and roaring fire, retaining `s61059` as the first trapped-injured fact; `s61113` asks where the Common crowd shelters without assigning one tent to a named subgroup. Freeze an exact reversible R8→R9 delta and lint 0/0.
- [x] Obtain fresh independent source/visual and formal dual-blind reviews of frozen R9 before any media spending; both PASS on R9 hashes.
- [x] Refresh the outline's stale stage line, select recommended A under the owner's standing choice authorization, send site outline/script review cards, record local exact-hash proxy approvals and add `verify-1.md` as the QA index to the independent R9 fact check.
- [x] Run one policy preflight and TTS/image dry-runs on frozen R9; preserve the site's `sponsored=0.31` policy FAIL and avoid another paid judge call. Quote 96 shots at about US$3.89 for up to three native takes; music quote needs TTS timeline.
- [ ] Resolve the site policy false positive after PR #1664 is deployed or obtain an explicit site-owner policy decision; synthesize voice when Gemini daily quota recovers, measure and inspect it, then fix the whole episode media cap before opening art.

## How to verify

From repository root: `VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s61 --json`; `VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs script --slug curio-s61`; `npm run check:tasks`. The R9 author lint returned 0 errors/0 warnings, 106 lines, 11.3556 estimated minutes at the tool's standard pace. Compare `claims.md` line text against `video.json` and the fixed text before any approval.

## Notes

2026-10-22: The GITenberg fixed copy was downloaded through the GitHub API to `/tmp/s61-halifax-prince.txt` and its SHA-256 checked. The book's preface (L90–110) says it is a social study, not a complete disaster history; Prince says he participated in Halifax rescue (L766–773). It records the powder-magazine warning (L951–974), crowd/army movement (L1356–1406), and attributes the absence of a second explosion to an entire artillery battery volunteering to flood the magazine in the naval yard (L1824–1836). The candidate explicitly attributes that causal claim to Prince; no independent military action log was obtainable in this task. It does not name a precise order, valve, distance, death toll from the warning, or identifiable survivor in art.

The source-rich fallback replaced 1859 Carrington: ADS and Wikisource were blocked by this environment's proxy 403, while GitHub search yielded later summaries but no fixed 1859 astronomy and telegraph first-person pair. S48 already covers the 1858 Atlantic cable. No paid TTS, MiniMax, judge, music, website approval, final video or YouTube upload has been performed for S61. Brand intro/outro assets and the actual clickable links are planned only; they are not outputs of this author draft.

2026-10-22 R2 independent [source/visual PASS](../../docs/videos/curio-s61/review/r2-independent-source-visual.md): video SHA-256 `800a8c7476bee77fad9b97e8a23e5b7e26007cfcf32e5ee471db371257fec134`, no claimed navy affiliation for the volunteer battery, naval yard retained only as the magazine location; six repaired prompts omit unsupported hose operations. R2 lint 0/0. The R2 formal dual-blind merge held on five shared narrative failures. R3 removes the numbered exposition, makes chapter starts answer preceding questions, pays off fire proximity and who assumed command, defers the no-second-blast finding until the end, and replaces the rail/telegraph inventory with Prince’s assigned-area search account (P14). R3 independent source/visual PASSed after the P14 L2023 citation repair, but formal dual-blind merged only 11/13 and held on chapter linkage and repeated facts; one reader also flagged the broad relief/shelter detour. R4 fixed opening and closing seams and anchored new port and warning details to Prince; independent R4 source/visual PASSed, but formal dual-blind merged 11/13 and held on repetition and the post-alert rescue/shelter detour. R5 answers the second-blast question immediately after the all-clear, leaves only five short source-bound callback lines afterward, and uses additional Prince details of blast damage, communication loss and first aid to preserve an eight-minute body. Fresh R5 review is pending; no media gate is approved.

R5 [獨立史料與書面畫面覆核](../../docs/videos/curio-s61/review/r5-independent-source-visual.md)判 **史料 HOLD 僅 `s61130`**：Prince L1363–1365 分別說有人跑向店鋪、原在店裡的人跑回家；稿中「先…又…」誤合為同一群人。其餘 96 句、87 圖與 7 卡通過紙審，須窄修兩群人的台詞後重核。R5 [盲讀 A](../../docs/videos/curio-s61/review/r5-isolated-blind-a.receipt.json)與[盲讀 B](../../docs/videos/curio-s61/review/r5-isolated-blind-b.receipt.json)只保留編輯診斷：正式題目未在原始答題前交付；A 11／13 自訂檢查、B 後綁正式題目 11／13 並指出 `payoffs/no_recap`，**都不計正式票**。R6 須先修來源及重述／回收，再把固定 13 題先交兩名未看舊票的隔離讀者；媒體仍待。

2026-10-22 R6 作者依 R5 HOLD 將 `s61130` 明確改為「有人跑向店鋪；店裡的人則趕回家」，避免合併兩群人。前半段增加 Prince 固定全文裡的戰時船隊、蒙布朗號與伊莫號載貨差別、首次示警缺口、爆炸對城堡／列車的衝擊，以及最初醫療船、訪客和本地居民不同的救援起點；撤離段加入手稿裡孩子、臥床者、仰望天空者的處境，片尾明確以解除通報後的白帳與教堂大廳回收「何處暫停」。緊接安全通報說明第二次爆炸沒有發生，仍把砲兵隊灌水的因果歸於 Prince，而不冒稱核實軍方紀錄。R6 完整檔案與可逆差異見 [作者交接](../../docs/videos/curio-s61/review/r6-author-narrative-repair.md)，待全新獨立覆核；無付費媒體。

R6 [獨立史料與書面畫面覆核](../../docs/videos/curio-s61/review/r6-independent-source-visual.md) **PASS**：103 句史實旁白、96 個畫面提示及 7 卡均對齊固定 Prince 原文，lint 0／0、325 CPM 正文估算 8 分 4.7 秒。兩個 claims 直連錨點可於下版補準，事實已有固定原文支持。全新正式隔離盲讀 A、B 各 11／13；[OR 合併](../../docs/videos/curio-s61/review/r6-formal-merge-audit.md) **12／13 HOLD**，共同 No 僅 `no_recap`：A 指 `s61028/31` 都講瓦礫阻路，B 指 `s61054/61` 都講消防員留守。R7 應刪重述或改為新動作並保持八分鐘正文，再重新雙盲；未進媒體。

2026-10-22 R7 作者把 `s61031` 改為首爆後消防員迅速回應警報，`s61054` 改為整支隊伍自願處理火藥庫的行動、`s61055` 才依 Prince 揭示砲兵隊身份，`s61059` 改為瓦礫下傷者尚待消防員協助，讓 `s61061` 留守成為下一個行動而非重述。開場 `s61005` 留待揭曉的搜救問題，不提前揭露工具與留守；`s61113` 改問老人與病弱者抵達公地後何處避寒，以片末白帳回收。`s61008` 的親身參與直連 Prince L766–773，`s61026` 木板直連 L1363–1370。R7 [作者交接](../../docs/videos/curio-s61/review/r7-author-narrative-repair.md)只保存修訂與機械檢查，**獨立 R7 史料／畫面及全新正式雙盲尚未進行**；無付費媒體。

2026-10-22 R7 [獨立史料與書面畫面覆核](../../docs/videos/curio-s61/review/r7-independent-source-visual.md)對全部 96 個插圖提示及 7 卡判 PASS，但史實 HOLD 僅 `s61031`：Prince L1963–1968 寫消防員回應 general alarm，未證警報遍及全城。R8 作者只刪去該句、research P09 與 claims 同一過強的地理範圍，重產 script 並固定可逆差分；R8 新雜湊須重新獨立史料審查及兩份全新正式盲讀，仍未進媒體。

2026-10-22 R8 [獨立史料／書面畫面覆核](../../docs/videos/curio-s61/review/r8-independent-source-visual.md)在固定 video SHA-256 `47860fcf1347bc549dcabeb2630f5a9e63bbbcd7a40c629ceafb16570f96ccb5`、script SHA-256 `00f9734108f68b0093a3c7791fe4b0974a376cb963cbc772c1ed92cc61c11b04` 上 **PASS**；103／103 句有固定錨點，96 圖／7 卡紙審 PASS，lint 0／0，325 CPM 正文 486.20 秒。兩份全新正式隔離盲讀 [A](../../docs/videos/curio-s61/review/r8-isolated-blind-a.md) 11／13（No `no_recap/no_detour`）、[B](../../docs/videos/curio-s61/review/r8-isolated-blind-b.md) 10／13（No `one_line/payoffs/no_recap`）；[正式 OR 合併](../../docs/videos/curio-s61/review/r8-formal-merge-audit.md) **12／13 HOLD**，共同 No 唯 `no_recap`：`s61059` 重述 `s61123` 已講的瓦礫下傷者與消防員知情。R9 需消重並維持八分鐘正文；單讀者的伊莫號前職岔線與老人病弱者避寒回收亦可檢查。未進媒體。

2026-10-22 R9 作者依 [R8 正式合併](../../docs/videos/curio-s61/review/r8-formal-merge-audit.md)的共同 `no_recap` HOLD，把 `s61123` 改為 Prince L924–937 直接描述的北面深紅天空與轟鳴火勢，使 `s61059` 的瓦礫下待救傷者成為第一次講出的火場需求。`s61113` 保留老人病弱者在寒風中趕路的處境，改問公地上的人**可在哪裡暫避寒風**，由後段軍方白帳及教堂大廳回收可用處所，不暗示每名老人病弱者被安排進同一頂帳棚。`s61015` 的比利時救濟船前職有固定來源；因刪除後在 325 字／分鐘只剩約一秒長度餘裕、同範圍替換易重述，這輪保留待獨立讀者判斷。R9 作者 [交接](../../docs/videos/curio-s61/review/r9-author-narrative-repair.md)記錄完整新雜湊與可逆差分；新獨立史料／畫面及兩份正式盲讀仍待，未進媒體。

2026-10-22 R9 [獨立史料與書面畫面](../../docs/videos/curio-s61/review/r9-independent-source-visual.md)在新固定雜湊上 **PASS**，103／103 史實旁白、96／96 插圖提示、7／7 資訊卡均可追溯，lint 0／0。兩位全新隔離讀者各自於 CLI 前凍結原始 13 題票，均 **13／13 YES**；[正式 OR 合併](../../docs/videos/curio-s61/review/r9-formal-merge-audit.md) **13／13 PASS**，官方 CLI 重播 exit 0。政策、站主審核、旁白與影片仍待，這次未呼叫付費媒體。

2026-10-22 R9 [製作前關卡收據](../../docs/videos/curio-s61/review/r9-production-gate-policy-hold.md)：網站 Jev 選推薦 A（1.00）；依站主「用推薦的決定就好不用問」授權，本機對大綱與劇本精確雜湊代行核准並各送站台待審卡，沒有冒稱站主親讀／親聽。新增 [verify-1.md](../../docs/videos/curio-s61/verify-1.md)作正式 QA 史料入口。一次政策預檢因本站「訂閱奇聞檔案局」自家 CTA 被算 `sponsored=0.31>0.30` 而 FAIL，屬待修政策判斷，不能聲稱 PASS；不重送 Jev 或為降分改史料稿。TTS dry-run 106 句／2,668 字元、Sulafat ready；96 圖 MiniMax 三輪上限報約 US$3.89，音樂報價待 timeline。S60/S62 的同網站 Gemini 429 顯示每日額度疑已用完，S61 本輪不再送第三次實際語音，預定 07:05 UTC 之後先重查再單次試。**本集仍 0 圖／0 judge／0 音樂／無 TTS、無成片；完整媒體上限未固定。**
