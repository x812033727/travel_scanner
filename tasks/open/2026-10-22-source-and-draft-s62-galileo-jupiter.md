---
id: 2026-10-22-source-and-draft-s62-galileo-jupiter
title: Source and draft S62 Galileo Jupiter observations episode
status: in-progress
priority: P2
area: docs
owner: codex-s62-new-episode
claimed_at: 2026-10-22T01:25:25Z
created_at: 2026-10-22T01:25:22Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/curio-s62
---

# Source and draft S62 Galileo Jupiter observations episode

## Why

The channel needs a new history episode after S61. A single night of Galileo's 1610 observation of Jupiter shows fewer light points than the later four-point record, so the story needs a fixed primary account that separates what he saw each night from his guesses and later inference. The author package must be independently reviewable before any paid voice or illustration work.

## Definition of done

- [x] S62 has a distinct A/B outline and a recommended A story, with a 30–60 second condensed opening, more than eight minutes of body at the conservative 325 CPM estimate, and the fixed 5-second intro and 21-second outro plan.
- [x] A fixed edition of Galileo's published account has a raw SHA-256, line anchors, limitations, and a one-to-one claim and visual map for every narration line.
- [x] The author candidate `video.json` and generated `script.md` pass the video lint with zero errors and zero warnings, use 70%+ unique original illustration prompts, and leave no fabricated video ID or paid-media receipt.

## Steps

- [x] Check S01–S61 briefs, topic index, and active tasks for overlap; choose a separate historical puzzle.
- [x] Pin and read the 1610 `Sidereus Nuncius` text through the 1880 Carlos translation and write the source boundary in `research.md`.
- [x] Draft `brief.md`, `video.json`, `claims.md`, generated `script.md`, and the author freeze for independent reviewers.
- [ ] Parent workflow obtains an independent source and picture audit, two blind story reads, and the station owner's choice and script approval before any media production.

## How to verify

From `/workspace/travel_scanner`:

```bash
sha256sum /tmp/curio-s62-sidereal.txt
VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s62 --json
npm run check:tasks
git diff --check
```

The first SHA must be `74fc9b817b64bc33415c6a44100c30f48952bc531d380682e5f4f1a26cc56fb5`. The fixed raw URL, commit and line map are in `research.md`; `/tmp` is a disposable local cache and not a Git deliverable.

## Notes

The episode follows 7 January–2 March 1610 and asks why Galileo sometimes counted three, sometimes two, sometimes four nearby points. His 10 January idea that one point was behind Jupiter remains attributed as his guess. The Carlos footnote that calls these objects “satellites” is editorial and does not become Galileo's original wording. The star diagrams are represented by tool text cards; image prompts are original illustrative actions, not exact sky reconstructions. The current R3 author binding, changes, SHA list and pending independent gates are in `docs/videos/curio-s62/review/r3-author-narrative-source-repair.md` and `r3-author-structured-diff.json`; R1/R2 receipts remain in the same folder. R2 source audit and two editorial diagnostics prompted R3; R3 independent source recheck and two new formal blind reads are still pending. No TTS, image, music, rendering, upload or payment was attempted.

R3 [獨立史料／書面畫面覆核](../../docs/videos/curio-s62/review/r3-independent-source-visual.md) **PASS**：114／114 句、110／110 圖稿與固定原文對齊，R2 四處來源／器材問題已修；lint 0／0。兩位先拿到固定正式 13 題再只讀劇本的全新盲讀者，[A](../../docs/videos/curio-s62/review/r3-formal-blind-a.receipt.json)與[B](../../docs/videos/curio-s62/review/r3-formal-blind-b.receipt.md)均 9／13；[正式 OR 合併](../../docs/videos/curio-s62/review/r3-formal-merge-audit.md)仍 **9／13 FAIL**，共同 No 為 `no_spoiler/payoffs/no_recap/no_detour`，官方 CLI 重播 exit 1。R4 須定點修開場提前揭露、缺點回收、計數重述與英譯連結旁白岔題；重凍結後再交新兩人，不進 TTS 或付費圖。

R4 作者修訂與可逆差分已凍結在 [R4 收據](../../docs/videos/curio-s62/review/r4-author-opening-payoff-repair.md)：預告改問十日隊形，首夜只見三點的問題由十三日四點回收並明說身份／原因無法回推；十七日貼近後顯出仍明確標為作者猜測；刪兩句計數重述，說明欄連結不再口播。新 G15 錨定作者邀人接算周期的原書段落。R4 `video.json` SHA `abed73ef3b14dcfc1b8ff1804f0234919d2f03cffa70a0b4c901a72ce6b14f92`，`script.md` SHA `8343a4f903fe4b405b1e6364cd67737ed7f3aead625b5fe713bf91c873c05c14`，`narrative_hash` `dc5b230a7d70f26b`；lint 0／0，325 CPM 正文 8.301 分鐘。等待全新獨立來源／畫面審查和兩位正式盲讀，不進 TTS 或付費圖。

R4 [獨立史料／書面畫面覆核](../../docs/videos/curio-s62/review/r4-independent-source-visual.md) **PASS**：114 句、110 圖、4 卡逐項核對，lint 0／0。兩位新正式隔離讀者 A 11／13、B 8／13；[正式 OR 合併](../../docs/videos/curio-s62/review/r4-formal-merge-audit.md) **11／13 HOLD**，共同 No 為 `payoffs/no_recap`，官方 CLI 重播 exit 1。R5 須刪合併不明點的重述、處理尾段未回答問題及正文回收，維持首夜究竟少哪一點無法確認的史料界線；新稿重核前不進媒體。

R5 作者稿已凍結在 [R5 收據](../../docs/videos/curio-s62/review/r5-author-payoff-recap-repair.md)：1 月 23 日改問作者如何解釋而由遮擋猜測直接回答；首夜身份不明只說一次，1 月 24 日改講實際新角距；片尾命名插段改為原書最外側點的謹慎半月試估，最後的問題由作者邀其他天文學家續測立即回收，結尾不再丟新問句。R5 `video.json` SHA `e7d14243eefff747d94ed2f28193ab93c0af97646b2ff55de935161c7643067a`，`script.md` SHA `2d92a72e535f03b53c70c3aa3b52c218c035c1ee53eb1ca82d3d0a802a6cc091`，`narrative_hash` `85c4d37cd19c407a`；lint 0／0、325 CPM 正文 8.235 分鐘。等待新的獨立來源／畫面審查及兩位正式盲讀，不進 TTS 或付費圖。
