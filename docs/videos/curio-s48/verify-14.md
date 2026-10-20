# S48 R10｜正式敘事、政策、精確劇本卡與完整音檢

2026-10-20 UTC。R10 的[獨立來源／書面畫面差分](review/r10-source-independent.md)為 PASS；兩名隔離讀者 A/B 對同一精確旁白各答 **13/13 yes**。A 綁 CLI 旁白字串 SHA `8f502054c869ba711fbe90b1a6bdf8343980298ebbb878a1c21471e0dcd2b79a`，B 綁 `script.md` 檔 SHA `182581f1a2f5c5eba79e3513bc0d6a8c79a6789360d6c86847068460cf515cdd`，兩者都與現行稿相符。官方 `narrative --answers` 亦通過 **13/13**；[合併敘事收據](review/r10-official-panel.md)保存逐題引文、A/B 回條雜湊和 CLI 紀錄。

| R10 精確內容檔 | SHA-256 |
| --- | --- |
| `brief.md` | `7b4bc4b3f6970ac20ef9c2b9269d8a17cafacc87f2ccaf076806772b2e56ca8a` |
| `research.md` | `3d769826eff0fbfb939b35506e9eafb4166868a6c0709cb4bf234af4922dd19f` |
| `claims.md` | `5b0714fafe2d0537d03309aac08d1dff8de0656337223689b7033866a5ccbbf7` |
| `video.json` | `ae0c8fd27d8abf7cc3d1dc192640336d12e5a5919db28d7b658671db35821e10` |
| `script.md` | `182581f1a2f5c5eba79e3513bc0d6a8c79a6789360d6c86847068460cf515cdd` |

站台先由 `review-push --report-only` 回報；讀回 `category=explainer`、`format=drama` 後，完整 **3,145 字元**旁白只送一次 Jev。`questions=explainer`、**PASS**：stance 0.73、demo 不適用、advice 0.01、sponsored 0.08。請求 SHA `532a059c1160fbf07c802ecd1c3c8c33d31e4063fde21a93d2f5e13b5e8ee784`；私有防重送紀錄和原樣回條在工作目錄，公開去憑證[政策回條](review/r10-policy.json) SHA `fc6864b9416e42f87d5b3e2a8668ecd92c7f0df6d5cda9f25acc53af113e14e1`，另有[文字摘要](review/r10-policy.md)。精確 R10 劇本卡已 `hand_pushed`；網站讀回 `status=pending`，`review-pull` 回「waiting for the owner」。本機 `approvals.json` 另記站主常設推薦偏好下的**委派編輯選擇**，綁同一 R10 SHA；這不是網站核准。

`tts --dry-run` 顯示 **102** 個請求中只有 `atl058` 待合成，約 **39 billable characters**。實跑 Gemini Sulafat 只合成該句 **1 件／39 字元**、重用 **101 件**；未強制重錄其他句。合成前核對現用 R9 檔與下表已封存的 `r9-redo2` 檔逐位元同 SHA：

| 舊 R9 私有封存 | SHA-256 |
| --- | --- |
| `review/narration-r9-redo2.wav` | `8a1a0818b8286e66c52db984c0a50251edce355c47af09bdc8490a55fcafe585` |
| `review/timeline-r9-redo2.json` | `c8e1ba488992ad44291cf5cb0fd69c3999517a589d076751bc1dd7c000a3fc22` |
| `review/check-r9-redo2.json` | `e2ed5e19b891cd34afaa720966cd60fb4b15dc92f1bbccb0866488b1367e98d7` |
| `review/check-flags-r9-redo2.json` | `a7745c52b8c7767ea0a50f9d754b99609fcc3ee1b2652060714dd4678812cf88` |
| `review/atl058-r9-redo2.wav` | `a688dff817f4caff579883ebe3a5ae7feaf83a91f5a4b2b1abfaea8141b4d622` |

新 R10 私有封存位於 `/workspace/.video-work/curio-s48/review/`：

| R10 新結果 | SHA-256 |
| --- | --- |
| `narration-r10-first.wav` | `d638c1b9dc9b9a4165b8adddfd6f873fba6de16cc3b5e9b26f730659de00878c` |
| `timeline-r10-first.json` | `a0c87443f00d78a97a683548dc0d262c1e8919e57ee54e0fa43fd0e1947f61d4` |
| `atl058-r10-first.wav` | `5c7a69663f4e6a13cd98b8195e71a356e19b4d66aaa4852867ab6009dd9654eb` |
| `check-r10-first.json` | `9f3f8b49826f90abef0b9edcc116e38ea9ff5d23f34ed7a7f026b7f53e5ce09b` |
| `check-flags-r10-first.json` | `7e3ef8b4c102a9260d2557635f4e0e15956e821fd08d86167fa967eabeeca70a` |

正式 `check-audio --slug curio-s48` 完整檢查 **102/102 句，0 旗標**：80 句逐字吻合、18 句僅同音字或語助詞差異、4 句沿用先前 Jev 合格判斷。本輪只新轉寫 `atl058` 一件、沒有新 Jev 呼叫；該句轉寫為「兩截鐵絲都不能證明有人動手，材料脆斷的發現讓意外較可信，但鐵絲怎麼刺入仍不明。」並被判 `exact`。實測濃縮開場 **54.77 秒**、正文自 `atl009` 至片尾前 `atl999a` **10:57.30**、全旁白 **12:06.20**。**R10 音訊檢查 PASS**；網站劇本卡仍 pending，音訊網站核准、插畫、配樂與成片尚未進行。
