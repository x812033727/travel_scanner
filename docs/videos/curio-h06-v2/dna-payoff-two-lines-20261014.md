# H06 v2｜兩句 DNA 比對回扣修稿與免費預檢

> **本頁為後續盲審 FAIL 的歷史快照；現行文案與雜湊見[最後一行免費窄修](dna-payoff-last-line-20261014.md)。**本頁的 `[v226]` 曾提前說出排除公主身分，與片尾答案重複；舊盲審答案和正式 FAIL 紀錄均保留。

日期：2026-10-14。本補記接續[無重錄刪句補記](no-recap-two-scene-addendum-20261014.md)。該稿在新一輪獨立 11 題盲審得到 **10 YES／1 NO**；唯一未過 `payoffs`，因 `[fa8j]`「沒有對上」未指明是與誰比對，字面上還可能與較早兩份檢體彼此相符的 `[4yw7]` 衝突，而 `[v226]` 未點名回到開場的身分問題。原答 `narrative-answers-after-cut.json` 與正式 `review/narrative.json` round 15 FAIL 原件均在本次修改前另行複製；不把前次結果當成新版通過。

## 站主指定的精確修稿

| Line | 舊句 | 本次正式句 |
| --- | --- | --- |
| `fa8j` | 開頭那兩份檢體，結果卻沒有對上。 | **但和皇后已知的母系參照相比，這兩份檢體都沒有對上。** |
| `v226` | 所以比對能支持線索，卻不能獨自鎖定本名。 | **回到開場那兩份檢體：比對能排除公主身分，卻不能獨自鎖定另一個本名。** |

其餘 99 句及 82 個 scene、chapter、模板和來源標註不變。`fa8j` 明說與皇后已知母系參照不符；`v226` 點名回扣開場問題，並區分排除公主身分與無法單靠這種比對確證另一個本名。這兩層結論的來源界線仍見 [claims.md](claims.md) c09、c19–c20。為讓較長的 `v226` 在**估時**中不超過八秒同一畫面，只把該句 `pause_after_ms` 由預設 300 ms 設為 0；場景交界原有 700 ms 停頓仍在。這是時窗調整，並未改指定句文或增加鏡頭。

| 綁定 | 本次值 |
| --- | --- |
| 正式 `video.json` SHA-256 | `16514ac30170a5700dbf061707a70e717ff450825ae9d75e84568ec99f151f15` |
| 正式 `script.md` SHA-256 | `f2b6f92c71504a5446fc47f2359e4fc9561f1f25c0f0359a6ae8e15e7fc7a5a1` |
| narrative／speech／visual hash | `4c6c61e2ee9e6e48`／`8fb82d587c3b464e`／`373e3953f50e6b1c` |
| 純盲審 `blind-payload.json` SHA-256 | `03eb4017f5f606fb5c0dddbd973d5f44e39b6977b57ad4d5a072509d76c32b32`；僅 narration 與 11 問，沒有答案 |
| 未核准混合投影 `timeline-projected-unapproved.json` SHA-256 | `846f1a825ed8b4f92fa436f99077dd2f9e631886864024c51f1f7151361f79ef` |

## 時窗與來源檢查的限度

這次**沒有合成新音訊**。投影取其他 99 句現有 WAV 的精確樣本數，僅把新 `fa8j`、`v226` 依工具預設語速估為 264,960、345,600 樣本；因此 14,677 格／30 fps＝**489.233 秒（8:09.23）**只是未核准估算。planned `shot` 7,464／14,677 格＝**50.8551%**，比 50% 的整格門檻多 125 格；98 畫面狀態、最長 8.0 秒、平均 5.0 秒，`cadenceProblems=[]`，敘事機械檢查 0 errors／0 warnings。`v226` 第二個原生卡狀態估計約 7.9 秒，貼近八秒邊界；兩句每句各一次 TTS 後，必須以真實 WAV 重算時窗、字幕與 shot 比例，超過八秒即重新設計畫面停留，不能以估算當成成片合格。planned shot 也須實際生圖、審圖與組片後另驗。

本次外部隔離目錄為 `<home>/mokaair-work/videos/curio-h06-v2/review/dna-payoff-two-lines-20261014T054116Z/`。`before/` 和 `before-receipt.json` 保存修改前稿件、上一版 payload／投影／收據、舊兩句 WAV 雜湊及 round 15 FAIL 原件。`before-receipt.json` SHA-256 `f26a7879eb9922348653cf7f22b7babf7284cac55e9b5e20af39014cac9c976e`，原答 SHA-256 `e7bacf1f087e581b4825965b12c311b309e32309abe43b03ea0125a10bb10656`，FAIL 紀錄 SHA-256 `5ecfdc9dbdf0b0f11069fe5a03c7c308ef00560c57cf3a058d205e596abc6bc1`。同目錄的 `postflight-receipt.json` 記錄改稿後雜湊與免費檢查。本輪只備妥新盲審輸入；盲審、兩句 TTS、正式時間軸重綁、站主音訊核准及畫面關卡均未完成。沒有呼叫 judge、TTS、付費生圖或後台。
