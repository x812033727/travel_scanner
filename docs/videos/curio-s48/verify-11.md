# S48 R9｜三句音檢卡點的作者限縮改稿

2026-10-20 UTC。精確 R8 經[獨立來源／書面畫面](review/r8-source-independent.md)、[兩名隔離讀者](review/r8-official-panel.md)、[全稿政策](review/r8-policy.md) PASS，但[正式完整音檢](verify-10.md)經兩輪限縮重錄仍標 `atl038/058/095`，故 R8 音訊 **HOLD**。以下 R9 僅是作者針對易混口播的候選修訂，**不是新稿的來源、畫面、敘事、政策或音訊 PASS**；R8 舊版站台劇本卡仍 pending，核准和 WAV 均不沿用。

| ID | R9 口播與改字原因 | 固定來源界線 |
| --- | --- | --- |
| `atl038` | 「開場船員正回收電纜：清晨指示光又滑出刻度，他們得把壞段帶上船修補。」保留明確回呼開場與故障→回收因果，改掉連續被轉寫錯的「船首」「起因是」。 | Russell [R3680–3815](https://github.com/GITenberg/The-Atlantic-Telegraph_40948/blob/ba499c6bc32adef8c8a91a306dcb2d54bf7e898d/40948-0.txt#L3680-L3815)記 8:00 指示光越出刻度，船員決定收回故障段重新接續；此句不預說稍後斷落。 |
| `atl058` | 「兩截鐵絲都不能證明有人動手；船上另見脆線，讓意外損傷較可信，刺入原因仍不明。」以「讓」取代反覆被聽作「這是」的「這使」，縮短到無畫面延長警告，並清楚分開破口碎片與**船上儲線**的脆斷觀察。 | Russell [R3033–3044](https://github.com/GITenberg/The-Atlantic-Telegraph_40948/blob/ba499c6bc32adef8c8a91a306dcb2d54bf7e898d/40948-0.txt#L3033-L3044)、[R3572–3584](https://github.com/GITenberg/The-Atlantic-Telegraph_40948/blob/ba499c6bc32adef8c8a91a306dcb2d54bf7e898d/40948-0.txt#L3572-L3584)、[R4094–4105](https://github.com/GITenberg/The-Atlantic-Telegraph_40948/blob/ba499c6bc32adef8c8a91a306dcb2d54bf7e898d/40948-0.txt#L4094-L4105)分別記兩次鐵絲、當時猜疑與後來的船上儲線脆斷；沒有查出每截進入破口的確切原因。 |
| `atl095` | 「這本書另引倫敦《旁觀者》報導：愛爾蘭端的光點不再亂跳，開始按固定間隔傳訊。」接上 `atl094` 的菲爾德著作，避免再次讀易被誤轉為「費爾德」的名字，仍將愛爾蘭端觀察明確歸給**另一份報導**，不是畫家 Dudley 的船上觀察。 | Field 後出著作引用 *London Spectator* [F9693–9719](https://github.com/GITenberg/The-Story-of-the-Atlantic-Telegraph_34765/blob/6b50b44d3cd2f3f1831e2c1a8fa052f53c51a4cd/34765.txt#L9693-L9719)：光點由不穩定轉為連貫，開始按固定間隔傳送訊號。 |

只改 `video.json` 這三句 `lines[0].text` 與 `claims.md` 同 ID 口播、首段版本狀態，再用 CLI 重生 `script.md`。`brief.md`、`research.md`、其餘 99 句、**99/99 個 shot 提示詞**、100 景 ID／順序、系列畫風、23 條 `loops` 與片尾不變。固定 Russell 原文檔 SHA `558efcc342df669e7387ffff818c104690e7ec910de49e795f996abf147ea750`，Field SHA `bee659b24ace56a5e1f7104a6a306e9325ccd9c864fc373ad35b0863c5a8c675`。

| R9 精確內容檔 | SHA-256 |
| --- | --- |
| `brief.md` | `7b4bc4b3f6970ac20ef9c2b9269d8a17cafacc87f2ccaf076806772b2e56ca8a` |
| `research.md` | `3d769826eff0fbfb939b35506e9eafb4166868a6c0709cb4bf234af4922dd19f` |
| `claims.md` | `6b06bbd35985438a99f1dd49e57e312f373de025ba25437fa1899d0925b6e4b6` |
| `video.json` | `4e64c126dc5ffda252e89a74540563ee42899aae0e7d857aeceb4a8d58fd76bb` |
| `script.md`（CLI 重生） | `0636abf65f316f7f0556e82ecd203583a915c8370d49b2cf9e55191efbab05c3` |

作者一致性檢查：`video.json` 102/102 句 ID 唯一，`claims.md` 102/102 列同 ID、同序、同字，重生 `script.md` 與 `screenplay(doc)` 逐位元一致；99/99 提示詞非空且與 R8 逐字相同；23/23 伏筆 setup→payoff ID 存在且依序。`lint --slug curio-s48 --json` **0 errors／0 warnings**，`git diff --check` 通過，`npm run check:tasks` 驗證 2,124 票（其他票的既有提醒不屬本集）。`estimateTimeline` 在最快 325 單位／分估濃縮開場 **45.27 秒**、其後正文至片尾前 **531.33 秒（8:51.33）**；250 單位／分正文 **662.93 秒**，兩者都是估值，非 R9 TTS 實長。全新盲讀用純旁白／固定 13 題 payload `/tmp/s48-r9-narrative-input.json` SHA `c8065a8e417a36dd2b7ea5cd833583cec1b8951d893cc00383c8837cca987fb3`。

下一關：由另一位工作者對**精確 R9 五檔**、兩份固定原文與三句旁白及書面畫面作獨立差分；兩名真正未讀 R9 的新讀者各只讀同版 `script.md` 完整盲評。若均通過，再重做完整 R9 政策與站台劇本流程，只合成改句並完整音檢至零旗標。作者沒有發動 TTS、音檢、政策、網站送審、插圖、配樂或成片。
