# S54 R16｜正式敘事合併與同版 Jev 政策

2026-10-20 UTC。**正式敘事 13／13 PASS；同版 Jev 政策 PASS。** 這是配音前的書面關卡，不證明 R16 音訊、生成插圖、成片或站主核准。本輪沒有改創作五檔、合成語音或其他媒體。

## 精確輸入

| 凍結檔 | SHA-256 |
| --- | --- |
| `brief.md` | `e45d0256fba6f068d0bbfc7614edf0444ed88156d850b64aa59f03644f680a0f` |
| `research.md` | `8bd0b5be9efe77b440b3677ba60b26fa97e9b6de47e8fcfc7b3f6284796eb6ae` |
| `claims.md` | `0477d725ca08d22589a7287b521d3738db75f2aa5033a5c9e414de8634a4ff1f` |
| `video.json` | `1f030f6c5f58a9d09919f9fb0b6f716e64f14b468c8735ce29987ece2ad6dc02` |
| `script.md` | `538c59b6e861b789a1bbd6ddd4609ee1a47edaac5ea6e98d41bee9ae677e162d` |

五檔在正式合併前、Jev 請求前和回覆後均重算為上表值，與 [R16 作者凍結](../r16-author-oral-repair.md)、[獨立史料及書面畫面 PASS](../r16-source-independent.md)相符；來源回條 SHA `c169c65a341b6ff3deddd082802dfac7299d9d4a3e4494482df2e9f1d31173a8`。

## 兩張原票與官方 OR 合併

兩位隔離讀者對同一 `script.md` 的原始 [A 票](blind-a.raw.md)與 [B 票](blind-b.raw.md)逐位元複製保留，SHA 分別為 `9e84a46c60693559a7952b6d4c342a7122f49d688683a28fa34ac9c6b17dab83`、`068b3f00c060df25877c7533b7c5465b9cf47042b634cb3cf7dac565f8e62e4d`。將各 13 題的原判斷照序轉成有逐句引文的 [A JSON](ballot-a.json)與 [B JSON](ballot-b.json)，SHA 分別為 `d4fc8f7b3bf6ab8f1c96186e5a192020acf50f2e3a400617b9a9305f6f307aa0`、`a30b7a7199f819dd4a85fc53e383d1ec5a76253feaa2a39c17a040f2d305cfc4`。程式核對 JSON 票別、13 題順序、每張原票明記的 script SHA 與每則引文行 ID；未改讀者原判。

官方 `panelVerdict` 對 A 與 B 各判 **12／13 yes**：A 在 `payoffs` 投 no，認為開場的具體信件付款疑問沒有被點名回收；B 在 `no_spoiler` 投 no，認為 `s54007` 已揭露後段才說的命令反轉。完整理由見原票，兩個異議均保留在 [合併稽核](merge-audit.json)，SHA `6eb1973f112562673fce53da672b5f11d2f5d6c3aa1c5240e580bf3e78b6502d`。`mergePanelVerdicts([A,B])` 的固定 **OR** 規則使每題至少有一位讀者給有行 ID 的 yes，正式結果 **13／13 yes、0 required fail、0 advisory fail**；這不表示兩項異議已經消失或 A、B 各自改判。

[合併答案](merged-answers.json) SHA `388bc2643250ed70b5be6d30d811e9a525d698a47d5fa35880955f5a4271f036` 交給 `node tools/video/cli.mjs narrative --slug curio-s54 --answers docs/videos/curio-s54/review/r16-merge-policy/merged-answers.json --workdir /tmp/s54-r16-merge-work --json`；CLI exit 0。原樣歸檔的 [CLI 回條](merged-narrative-cli-receipt.json) SHA `6ae759cd34e4c28114388805be358994791aa88b96e4498360b08626b8da768c`：`passed:true`、`failed:[]`、`advisory:[]`、round 1；[CLI verdict](merged-narrative-cli-verdict.json)亦保留。`panel_rules_sha256` 為 `5d71fef2cf3831dc33c0c32b2b297f633c47bfe41fbad18865ae08ed0c91cb75`，本版 `panel_narration_sha256` 為 `8d3baaaf5bd612ee3732c0c059130d89099063ebfe1737b592a4362b746a2bfa`。暫存工作目錄刻意與共享配音工作目錄分開；完整雙讀者明細在合併稽核，CLI 回條記錄同版合併答案的官方執行結果。

## 同版 Jev 政策

正式敘事及來源關卡 PASS 後，用本版完整 `video.json` 與 `brief.md` 的 `policyRequest({doc, brief})` 組 [唯一請求原文](policy-request-body.json)，SHA `42acac53f70f5cc8e258940a754af1fcbe76a117a698d9a35a9ad375fe87b225`；旁白 **3,536** 字元、站主觀點 **72** 字元。[送前中繼資料](policy-request-meta.json)記五檔與關卡 SHA，[送出意圖](policy-send-intent.json)阻止自動重試。透過倉庫的 `automationClient` 對網站 `/api/video/automation/judge/policy` **只送一次 POST**，HTTP **200**；[原始回覆](policy-response.raw.json) SHA `5bf1cdc02bc68a5e2f49799baba13dc97d9d81dbf1a44e4b8b48281530690d5a`，經 `policyVerdict` 得 [判定回條](policy-receipt.json) SHA `d8d3859bb3b268dcab42486d13ea504e730387155e5c4e3422059407b283831b`。網站解說題組 `passed:true`：立場 `0.73`、示範不適用、建議 `0.01`、業配 `0.28`。請求與回條沒有儲存憑證。

`node tools/video/cli.mjs lint --slug curio-s54 --json` 為 **0 errors、0 warnings**；`npm run test:docs-videos` **236／236 通過**，`npm run check:tasks` 通過。下一關才能按 R16 精確雜湊做新語音和完整音檢；舊 R15 語音、ASR 或政策回條不能移作 R16 音訊 PASS。
