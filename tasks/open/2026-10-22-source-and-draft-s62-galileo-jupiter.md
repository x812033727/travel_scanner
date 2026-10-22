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
- [x] Parent workflow obtained independent source and picture audit, two blind story reads, and the recommended A choice with exact-hash local outline/script approval under the owner's standing instruction; website hand-pushed cards remain pending and no personal owner reading is claimed.
- [ ] Resume Sulafat TTS when Gemini daily capacity returns; inspect audio, then quote the whole episode and inspect native art before storyboard or final cut is claimed.

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

R5 [獨立史料／書面畫面覆核](../../docs/videos/curio-s62/review/r5-independent-source-visual.md) **PASS**：114 句、110 圖、4 卡對齊固定史料，lint 0／0。全新正式隔離讀者 A 11／13、B 10／13；[正式 OR 合併](../../docs/videos/curio-s62/review/r5-formal-merge-audit.md) **12／13 HOLD**，兩人共同 No 僅 `no_recap`：`s62057/58` 連續兩句重複同一光點幾小時後顯現。官方 CLI 重播 exit 1。R6 應只修此重述且保留來源界線與 325 CPM 正文至少八分鐘，再由新兩人重評；本輪不進 TTS 或付費圖。

R6 作者版已凍結於 [R6 收據](../../docs/videos/curio-s62/review/r6-author-single-recap-repair.md)：`s62058` 改講 1 月 12 日東西兩點各離木星兩角分、後出細點貼近的原書新資訊；開場只問稍晚隊形，不先講細點必顯，1 月 10 日不再問不可確證的去向。5 個可逆 JSON leaf 與文字差分已保存。`video.json` SHA `9551bab89a03d91dc29afd103bdc383541fde1b10d8fb3b7de0eb218cbb6a7ad`、`script.md` SHA `0816b0a91b5b4e22571db7cf04b350b121dd56e364a57637f228a1d3f9d8a3c3`、`narrative_hash` `12dee2d6e454e303`；lint 0／0、325 CPM 正文 8.232 分鐘。R6 待新獨立來源／書面畫面覆核及兩位全新正式盲讀，沒有任何媒體核准。

R6 兩位全新正式隔離盲讀 A、B 各 12／13；[正式 OR 合併](../../docs/videos/curio-s62/review/r6-formal-merge-audit.md)仍 **12／13 HOLD**，共同 No 只剩 `no_recap`：`s62004` 開場雲遮一月九日，正文 `s62041` 再說相同雲遮而未明示回呼。官方 CLI 重播 exit 1。R7 應具體回呼開場那夜或換新史料事件，再重新核來源與盲讀；R6 未進媒體。

R7 作者定點改稿已凍結於 [R7 收據](../../docs/videos/curio-s62/review/r7-author-cloud-callback-repair.md)：`s62041` 點名「回到開場那夜」，接住作者想核對木星是否走錯卻沒有九日新位置的問題；`s62042` 改指原書觀測圖直接由八日接十日，保留真實的證據空格。R6→R7 只有 2 句旁白及 `s62042` 的 G04／G05 行錨更新。`video.json` SHA `1c811dfb9561248e314f0a39a3510386a6188322521f2d1e6c403e03ab81de95`，`script.md` SHA `c638b0d28cfbf6b398cd3bb541160685403bf3936fcd1613bc958921623e4326`，`narrative_hash` `edc7d2005d74f93c`；lint 0／0、325 CPM 正文 8.254 分鐘。R7 待全新獨立來源／書面畫面覆核和兩位正式盲讀，不進 TTS 或付費圖。

R7 [獨立史料／書面畫面審查](../../docs/videos/curio-s62/review/r7-independent-source-visual.md)有條件 **HOLD**：114／114 句史料對齊、109／110 圖稿通過，唯一 `s62065` 把一月十五日第三時辰的夜景寫成午後光線。R8 [作者一景修訂](../../docs/videos/curio-s62/review/r8-author-night-light-repair.md)只換這個提示詞及同列主張畫面為燭光和窗外冬夜，`video.json` 1 個 leaf 可逆，114 句、`script.md` SHA `c638b0d28cfbf6b398cd3bb541160685403bf3936fcd1613bc958921623e4326` 與敘事雜湊 `edc7d2005d74f93c` 均未改。R8 `video.json` SHA `c9f249ab7210fa4fb2cf2ac5206c57735ee19efcf0e846414bcfc06bb0745ace`，`claims.md` SHA `50f4b272576e90e3a172fd996fc27995223cd32cf0163264308109e6a3833c73`；lint 0／0，325 CPM 正文仍 8.254 分鐘。R8 待新獨立書面畫面審查與兩位全新正式盲讀，不進媒體。

R8 [獨立史料／書面畫面重驗](../../docs/videos/curio-s62/review/r8-independent-source-visual.md) **PASS**：`s62065` 改為與原書「一月十五日夜間第三時辰」一致的燭光／窗外冬夜；114 句、110／110 個提示詞、4 卡、134 個行錨對齊，lint 0／0。兩位全新正式隔離盲讀 A **11／13**（單票 No `no_toc/no_recap`）、B **13／13**；[官方逐題 OR 合併及獨立 CLI 重播](../../docs/videos/curio-s62/review/r8-formal-merge-audit.md) **13／13 PASS**、exit 0。A 對 `s62041` 結構語及 `s62104` 重述 `s62051` 的疑慮保留供站主審稿，不是雙人共同 No。下一步為站主選擇／核准大綱與劇本，之後才可依系列流程報整集媒體預算與各關卡；目前沒有 TTS、原生插圖、配樂、渲染或上傳。

R8 [製作關卡與語音停點](../../docs/videos/curio-s62/review/r8-production-gate-and-tts-hold.md)：依站主既有「推薦的決定就好不用問」授權選 A，精確 `brief.md` SHA `5941ebf974ad…` 與 `script.md` SHA `c638b0d28cfb…` 各送一次網站審核卡，並在本機透明記錄代行核准；網站卡仍 pending，未聲稱站主親讀。新增 [QA 事實入口](../../docs/videos/curio-s62/verify-1.md)承接獨立 114／114 句、110／110 圖及雙讀者 13／13。正式 lint 0／0；一次性網站政策預檢 PASS。TTS dry-run 114 句／2,514 計費字元，MiniMax dry-run 110 圖、三輪最多約 US$4.46，音樂需等 timeline 再報。唯一一次真實 TTS 呼叫回 Gemini busy／用量上限 exit 4，無 timeline、音檔或 journal；**不立刻重試**，預計 2026-10-22 07:05 UTC 之後單次重查服務再續。沒有原生圖、音樂、成片或上傳。
