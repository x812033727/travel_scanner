# S61 R9｜正式雙盲敘事合併

2026-10-22 UTC。**兩位全新隔離讀者各 13／13；正式逐題 OR 合併 13／13 PASS。** 這是固定 R9 劇本的敘事判定；[獨立史料與書面畫面](r9-independent-source-visual.md)亦已 PASS。這份紀錄不表示站主已聽旁白、看過生成原圖或核准成片。

兩位讀者各自先看官方 13 題（SHA-256 `15cfd34356840ae8036c91bc9d8b29f210be52aa761f28379a2bd9ed263fa5ad`），只看凍結 `script.md`（SHA-256 `e3f27c9da2b951fd744e9de48b2c64d665ef4f76cd6abaa4e323b43c5ebb9eb9`），在執行官方 CLI 或讀取舊票前凍結原票。兩份原票的 13 項證據均帶有腳本中的台詞 ID 及原文；我以現版 `video.json`（SHA-256 `005cc35734535c8a01ee46f7ee5dc1a3555d3b543d0fc3b42c0beda2812d97ce`）重新呼叫倉庫的 `panelVerdict`、`narrativeRecord` 與 `narrativeReviewMatches`，逐位元比對各自官方紀錄，全部一致。

| 讀者 | 原票 SHA-256 | 官方綁定紀錄 SHA-256 | 結果 |
| --- | --- | --- | --- |
| [A](r9-isolated-blind-a.receipt.md) | `b796935f2f96f75cd2e203adc9a8f5837548732b49e0667ebee5d6fa83bf3122` | `6200e5439459844883e313f8dbc65020f0bdee2f0c3570e35c359edce6666b21` | 13／13，exit 0 |
| [B](r9-isolated-blind-b.receipt.json) | `f08ee94eb719796f4f0adaf89557e66561c299de049dbb04635b757682e0be26` | `02493ba716006733431d294b539b446940d1cc1ecb118e6b1eb32b4ebd95a3df` | 13／13，exit 0 |

`mergePanelVerdicts` 產出的 13 題皆 `yes_readers=2`，沒有必答失敗或建議失敗。[正式合併答卷](r9-formal-merged-answers.json) SHA-256 `38242f96c3e35b5e57ae866e638eddd3b7c503011d2db6a932edb7c3d1f8e079`；保留兩位原票的[正式合併紀錄](r9-formal-merged-narrative.json) SHA-256 `c66cf387c52b1f5d29ed93a64903756df5ee0d5bff008abeb7c8df3d31e9d875`，`round=9`、`passed=true`。共同綁定 `narrative_hash=905b9da092703d23`、`script_hash=d223d8285664b3408ab86e641dc0d548bf779c449e75c5d6258b4bf92506eda6`、`panel_rules_sha256=5d71fef2cf3831dc33c0c32b2b297f633c47bfe41fbad18865ae08ed0c91cb75`、`panel_narration_sha256=0ad2b1316ce246f6d4508c3f0109db29ef7daa16b637271cb3087c98b561e923`。

用合併答卷在全新工作目錄 `/tmp/s61-r9-formal-merge-official` 重播官方 `narrative --slug curio-s61 --answers docs/videos/curio-s61/review/r9-formal-merged-answers.json --workdir /tmp/s61-r9-formal-merge-official --json`，exit **0**、stderr 空、[stdout](r9-formal-merge-cli.stdout.json)顯示 13／13 PASS。其[原生紀錄](r9-formal-merge-cli.official-narrative.json)的答法、證據與四項綁定一致；新工作目錄的原生 round 是 1，正式合併標 R9 的 9。`s61123` 已不再先講後面 `s61059` 的瓦礫受困細節，`no_recap` 得到兩位 YES。之後若劇本或規則改動，這次票不能移用。

本關卡沒有呼叫付費媒體，也沒有產生 TTS、插圖、音樂、影片、Short 或 YouTube 連結；下一步是政策與媒體前置檢查。
