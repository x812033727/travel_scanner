# S48 R10｜`atl058` 音檢卡點的作者限縮改稿

2026-10-20 UTC。精確 R9 已有[獨立來源／書面畫面](review/r9-source-independent.md)、[兩位隔離讀者](review/r9-official-panel.md)、[全稿政策](review/r9-policy.md) PASS，但[正式完整音檢](verify-12.md)經兩次僅重錄 `atl058`，仍把「船上另見脆線」聽作「船上零件缺陷」；R9 音訊 **HOLD**。R10 只改這句的口播字串與主張同文，並重生 `script.md`。這是作者候選稿，**不是 R10 的來源、畫面、敘事、政策或音訊 PASS**；舊版網站卡、舊 WAV、舊版審核結果均不沿用。

| ID | R10 口播與改字原因 | 固定來源界線 |
| --- | --- | --- |
| `atl058` | 「兩截鐵絲都不能證明有人動手；材料脆斷的發現讓意外較可信，但鐵絲怎麼刺入仍不明。」避開已連續三輪被誤聽的「船上另見脆線」，將證據與推論拆成清楚的因果句。緊接的 `atl057` 已指明**船上儲放線圈**中的護線鐵絲有韌有脆；本句只從該觀察推論意外較可信，不把兩截破口鐵絲說成已查出來源。 | Russell [R3033–3044](https://github.com/GITenberg/The-Atlantic-Telegraph_40948/blob/ba499c6bc32adef8c8a91a306dcb2d54bf7e898d/40948-0.txt#L3033-L3044)、[R3572–3584](https://github.com/GITenberg/The-Atlantic-Telegraph_40948/blob/ba499c6bc32adef8c8a91a306dcb2d54bf7e898d/40948-0.txt#L3572-L3584)、[R4094–4105](https://github.com/GITenberg/The-Atlantic-Telegraph_40948/blob/ba499c6bc32adef8c8a91a306dcb2d54bf7e898d/40948-0.txt#L4094-L4105)：兩次鐵絲、當時的人為破壞猜疑，以及後來檢查船上儲線所得的脆斷觀察；沒有查定碎片刺入的原因。 |

`video.json` 相對 R9 僅 `atl058` 的 `lines[0].text` 改字；`claims.md` 只同步該列口播與版本狀態，`script.md` 由 CLI 重生。`brief.md`、`research.md`、其餘 101 句、99/99 個 `shot` 畫面提示詞、100 景 ID／順序、23 條伏筆與片尾維持 R9 精確內容。固定 Russell 原文檔 SHA `558efcc342df669e7387ffff818c104690e7ec910de49e795f996abf147ea750`，Field 原文檔 SHA `bee659b24ace56a5e1f7104a6a306e9325ccd9c864fc373ad35b0863c5a8c675`。

| R10 精確內容檔 | SHA-256 |
| --- | --- |
| `brief.md` | `7b4bc4b3f6970ac20ef9c2b9269d8a17cafacc87f2ccaf076806772b2e56ca8a` |
| `research.md` | `3d769826eff0fbfb939b35506e9eafb4166868a6c0709cb4bf234af4922dd19f` |
| `claims.md` | `5b0714fafe2d0537d03309aac08d1dff8de0656337223689b7033866a5ccbbf7` |
| `video.json` | `ae0c8fd27d8abf7cc3d1dc192640336d12e5a5919db28d7b658671db35821e10` |
| `script.md`（CLI 重生） | `182581f1a2f5c5eba79e3513bc0d6a8c79a6789360d6c86847068460cf515cdd` |

作者一致性檢查：全稿 **102/102** 句 ID 唯一，正文 **99/99** 列主張同 ID、同序、同字；`script.md` 與 `screenplay(doc)` 逐位元一致。99/99 畫面提示詞與 R9 同字且非空；23/23 伏筆 setup→payoff ID 存在且依序。`VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s48 --json` 為 **0 errors／0 warnings**；`npm run check:tasks` 驗證 2,124 票（其他票的既有提醒與本集無關），`git diff --check` 通過。`estimateTimeline` 在最快 325 單位／分估濃縮開場 **45.27 秒**、其後正文至片尾前 **531.70 秒（8:51.70）**；都是估值，非 R10 TTS 實長。新隔離盲讀用純旁白／固定題目 payload `/tmp/s48-r10-narrative-input.json` SHA `3cab3cdb31111cd60657bcf33f7255ba75845bc0a6edd28d4da0d635c6f15403`。

下一關：另一人對**精確 R10 五檔**、兩份固定原文及 `atl058` 的來源／書面畫面作獨立差分，並請兩位真正未讀 R10 的新讀者盲評。通過後重做全稿政策、網站精確劇本流程，僅重合成改句，再完整音檢至零旗標。作者沒有自行核發任何 PASS，沒有發動 TTS、音檢、政策、網站送審、插圖、配樂或成片。
