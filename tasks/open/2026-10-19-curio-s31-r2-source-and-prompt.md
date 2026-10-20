---
id: 2026-10-19-curio-s31-r2-source-and-prompt
title: Curio S31 source and prompt corrections through R5a
status: blocked
priority: P2
area: docs
owner: codex-root
claimed_at: 2026-10-20T00:31:30Z
created_at: 2026-10-19T23:59:38Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/curio-s31
---

# Curio S31 source and prompt corrections through R5a

## Why

Independent source/visual gate [verify-2.md](../../docs/videos/curio-s31/verify-2.md) blocked S31's frozen script SHA `72eb00f5f0f05268dc9125705c3e75eaea98b8b933e2471fb42cf6e28762826c` before audio. The opening linked Du Mu's poetic horse to a later history's relay; the fruit timing could read as additive; Bai Juyi's held fruit and elderly likeness, anachronistic history copyist, written place cards, and a jar for `荔枝煎` asserted details the sources do not give. Make a new source-safe R2 package and review it anew.

## Definition of done

- [x] Script, claims and still prompts remove the blocked source assertions and visual specificity, while keeping the story body above eight minutes.
- [x] Fresh context-isolated official 13-question narrative panel and independent source/visual audit pass for R5 script/claims; R5a changes only two prompts, which the coordinating agent independently rechecked against the exact new video SHA. Lint remains 0 errors/0 warnings.
- [x] R2–R5a handoffs record exact script/video/claims SHA values and state audio and paid media remain unstarted.

## Steps

- [x] Revise the blocked narration and prompts, regenerate `video.json`, `claims.md`, `script.md`; compare all 97 IDs and rerun lint.
- [x] Bind R5's 13/13 narrative seal to the unchanged R5a script and recheck the two amended still prompts against R5a's new video SHA before media production.
- [x] Commit and push scoped S31 changes without touching other agents' staged files.

## How to verify

`VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s31`; `node tools/video/cli.mjs script --slug curio-s31`; `node tools/video/cli.mjs narrative --slug curio-s31 --answers <new-blind-answers> --workdir <new-blind-workdir>`; compare 97 lines in script/claims/video; independently read all still prompts against pinned texts; `npm run test:docs-videos`; `npm run check:tasks`.

## Notes

R2 script SHA `d6e2825bb35adbb7bd2b101821b27b4fe32394f7d8e35b166c594a3b9179089e` received a fresh official blind panel: 12/13 YES, blocked solely on repeated recap at ly063/066 and ly054–057/090, ly083/091. The sealed receipt is `/tmp/curio_s31_r2_narrative_blind.md`. R3 removes those repetitions by advancing Bai's text at ly066 and making ly090–ly092 an on-page erase action; R3 script SHA `cfc5a32d15d7e5cca20f972aca6dfdb2810a96fe8791d23c70da2188d20dfb5a`, video SHA `a5fdecb15ee4e4eb273db018ec3b6db6a30c4ed27d37d2c315460bf477b527a7`, claims SHA `addcf78f2ded2e3a8778b7c59b176151a15742c09de52ea9803534c53a03f72f`. Lint 0/0, 97 scenes including outro, 96 still prompts, 10 matched loops. No TTS, image generation, music or assembly.

R3 fresh context-isolated official panel again yielded 12/13 YES, with only `no_recap` NO: ly037/038 immediately repeated the unchanged-taste arrival fact, and ly052/053 restated Guangzhou tribute. The sealed receipt is `/tmp/curio_s31_r3_fresh_narrative_blind.md`. R4 makes ly038 flip back to Du Mu's palace scene and ask whether the history joins it; ly053 now puts the two records together and searches for a shared shipment mark. R4 script SHA `899dd8510fbd1a45e0596682df38c6ea18600c356681369ff2ffbde36d56c592`, video SHA `8ebe96c889a8bb20d0d2e341864e7d037232eed0da015df035a924c3c8cd0a86`, claims SHA `eae4a0838b10184975ec50e747934db18659befc67c8eba9a761b73d88fd970b`; the pending review conditions are recorded in [verify-5.md](../../docs/videos/curio-s31/verify-5.md). No media has been made.

R4's independent narrative panel passed 13/13, but the subsequent primary-text and 96-prompt audit blocked on an invented birthday banquet at ly045, a palace-receipt cue at ly037, and a smell/taste mismatch at ly077; it also noted ly016/ly021 precision and missing `NBG` citations at ly076/ly078. R5 applies all corrections and is frozen in [verify-6.md](../../docs/videos/curio-s31/verify-6.md): script SHA `332c875a835f89b428c124f578c380079976b9e35b396d098b086a56ba08cef2`, video SHA `4a0d0bc19c5b2ebbf6982a58a6c1331b6527b6fca4d02a5230e15edeae74c754`, claims SHA `83063009c6fec93840e0e6043118f7ed2df691b3e38651bc1590f12ad0ec2127`. Lint 0/0, 97 aligned lines, 96 still prompts, 10 loops, body above eight minutes; fresh reviews pending. No TTS, image generation, music or assembly.

2026-10-20 00:32 UTC：R5 新讀者劇本盲讀 **13/13**，四份固定來源重取相同 SHA，97/97 主張與 96/96 圖提示均覆核。R5a 只將 `ly021` 單騎改成數騎、`ly049` 刪去無據的音樂廳收果；主代理核對 diff 並獨立查兩景與原文。新 video SHA `930b04118fc8eaab69a904e986a5888322d0d942247535f1567e347bd0a4bf11`；劇本及 claims SHA 未變。正式 `narrative --answers` 依盲讀封存行號證據通過，A 案 outline 與 exact script 已依站主概括授權本機核准；`tts --dry-run` 報 97 句／2,167 字元，語音合成已啟動。見 [verify-8.md](../../docs/videos/curio-s31/verify-8.md)。

2026-10-20 00:45 UTC：97 個 TTS 請求合成完成；`timeline.json` 17,968 frame／30 fps，全片 598.933 秒，正文從 `ly010` 1,478 frame 到 `ly097` 17,771 frame，**543.1 秒／9 分 03.1 秒**。逐句 `check-audio` 正在跑，未清零不批准圖。MiniMax `keyframes --dry-run --takes 3` 對 96 張 still 報首輪約 US$1.30、最多三輪 US$3.89；600 秒配樂預估 US$0.08，**整集插圖加音樂硬上限 US$3.97**，依站主持續採推薦方案委託預先記帳。開畫仍需音訊零旗標、共用時窗餘額與逐張人眼覆核。

R5 fresh blind panel sealed 13/13 YES on the unchanged script SHA. Independent receipt `/tmp/curio_s31_r5_source_visual_audit.md` re-downloaded four pinned full texts and found 97/97 claims supported, 96/96 prompts checked, with nonblocking cautions at ly021 (one rider versus several in the poem) and ly049 (implied in-hall basket handover). [verify-7.md](../../docs/videos/curio-s31/verify-7.md) records prompt-only R5a: script and claims SHA stay as above; new video SHA `930b04118fc8eaab69a904e986a5888322d0d942247535f1567e347bd0a4bf11`, lint 0/0, 97/97 unchanged, 96 still, 10 loops. Only the two revised prompts need independent recheck against this exact new video hash before audio. No media has been made.

2026-10-20 R6 **spoken-line revision**, after two `tts --redo` rounds left 18 `check-audio` flags on R5a audio. Edited IDs: `ly004`, `ly006`, `ly008`, `ly009`, `ly013`, `ly017`, `ly019`, `ly020`, `ly022`, `ly023`, `ly032`, `ly039`, `ly040`, `ly058`, `ly076`, `ly077`, `ly081`, `ly082`. Changed narration and matching claims only, plus `ly019` statement voice direction; all 96 still prompts, source URLs and 10 loops are unchanged. Regenerated script; lint 0 errors/0 warnings; 97/97 scene/claim rows aligned; body text 1,997→2,033 code points (latest prior audio body 546.3 seconds after redos). Exact hashes: script `60613153b84425c19ee6abe31a74a46a874a1691599e1cdee5059be1fd9f42b0`, video `28adf661838a0c0feb87865a1638795b75edc2d5477de8e3d8b8a6d7e450bc07`, claims `aaa50b3a3fc6aa66ab35bd1476186bba984380004e20ec5299a779052575d59f`. Independent R6 official blind panel **13/13 PASS** and separate pinned-source / all-prompt audit **PASS**; evidence and the self-formulated first reader caveat in [verify-9.md](../../docs/videos/curio-s31/verify-9.md). The old audio approval is stale. **Next:** local delegated R6 script approval, new TTS, full audio recheck; no images before zero unresolved flags and a current quote. Image-plus-music ceiling remains US$3.97.

2026-10-20 02:37 UTC：R7 僅將 R6 兩輪補錄仍有旗標的四句換成較清楚口語。新獨立官方盲讀 **13/13**，固定四份全文與四句定點來源／提示詞覆核通過；本機委託精確稿核准後只新合成四句。全片 `check-audio` **97/97、0 旗標**，正文實測 **9:11.37**。網站音訊卡已提交、仍 pending；配樂實支 US$0.08，96 圖最多三次 US$3.89，整集圖樂上限 US$3.97。另一次畫面年代預檢指出末段現代鉛筆與古裝場景混用，**在 prompt-only 修正和獨立重查前不得開圖**；詳 [verify-10.md](../../docs/videos/curio-s31/verify-10.md)。

2026-10-20 03:14 UTC：39 景 prompt-only 修正末段現代地圖桌、唐代戲劇景衣著和離鏡交接手，獨立定點覆核對現行 video SHA `66332b5b87fe2b3a3c26774398cb072b5e7838e066b35686a082f61365429372` **PASS**，lint 0／0；劇本／音訊不變，仍未畫圖。詳 [verify-10.md](../../docs/videos/curio-s31/verify-10.md)。

2026-10-20 R8 開畫前逐鏡強化：相對 R7 精確版只改 **76/96 個 `scenes[].data.prompt`**，`video.json` 新 SHA `0b5e8dcc054c880127e49efd0ec0dd58f86f77c0a50530f2e094b2b8d0fbe762`；script/claims/research、97 句及音訊不變。另一名獨立審查者對**新 SHA 全 96 景**與固定來源逐鏡重查 **PASS**，lint 0／0，3-take dry-run 96 景均在上限內；圖樂最高 US$3.97，目前只有既支音樂 US$0.08，沒有付費圖片。生成後仍須原尺寸驗收。詳 [verify-11.md](../../docs/videos/curio-s31/verify-11.md)。

2026-10-20 單支 `from-episode` Short 草稿已備：以杜牧詩、《新唐書》兩段和白居易原序辨明荔枝來路仍不可畫成完整驛線。八景均指向本集既有長片鏡位；格式／六拍／單支檢查零問題。這是零付費撰寫者自查，尚無長片網址及插圖 keyframe，不能製作或宣稱完成短片；詳 [shorts.json](../../docs/videos/curio-s31/shorts.json) 及 [short-verify-1.md](../../docs/videos/curio-s31/short-verify-1.md)。音訊站台 gate 仍 pending。

2026-10-20 R9 原尺寸畫面止損：首 49 景的 22 張機器 PASS 中，人工只有 `ly018` 可直接留用，5 張待覆核；經 25 景 source-safe prompt 審查後，最後再將 `ly001` 空門、`ly006` 雙空白道具、`ly014` 無人紅塵各付費試畫一次。三張都獲機器 9.29 PASS，**原尺寸 0/3 KEEP**（門洞／門柱多幼童、路程紙缺失），達到預先設定的停止條件。`STOP` 已恢復，帳本 US$0.853／US$3.97、零預留；所有 26 個未驗證 prompt 差異僅封存補丁，正式 `video.json` 回復 R8 已提交 SHA `0b5e8dcc054c880127e49efd0ec0dd58f86f77c0a50530f2e094b2b8d0fbe762`。**不要再對 S31 付費生成**；先提出可控 2D 示意圖加少量後製來源卡的替代方案，證明至少 68/96 正文鏡頭仍是有效插畫、最多連卡三張，再重做來源／敘事與分鏡審核。詳 [verify-12.md](../../docs/videos/curio-s31/verify-12.md)。長片、片頭片尾、Short 成片及上傳包仍未完成；先轉投其他來源與畫面可行的集數。
