# S51 R11｜六句配音修詞的獨立來源與書面畫面覆核

2026-10-20 UTC。對 [R11 作者凍結](../verify-12.md)的精確五檔，**六句口播史料 PASS；逐句主張錨點窄 HOLD（`cal099`）；書面畫面窄 HOLD（`cal021`）**。兩個缺口都可只改文字／一景提示詞，不必擴大情節；修後應重凍結並由另一人驗新差分。這份查核沒有代替兩名新讀者的盲讀、政策、網站核准、真實音訊或生成圖片驗收。

| 固定檔 | 本次獨立 SHA-256 |
| --- | --- |
| `brief.md` | `ad22f35f5d9ff6a17e055f27b4b6eaaf921f22856b15445531db5a4caf087837` |
| `research.md` | `039ca3ecc3f5099537e51e48d0f1788faf0bdf9c5d254f2ae64dd5ff89b56459` |
| `claims.md` | `ce27dbd797c995ca367316f67b4ca0136cb21988bc9c1b84a07be842012abf8f` |
| `script.md` | `b0aed4b7b269130a717b290386b32f095b55c8a94a444db27221b1d2bf7f2c8e` |
| `video.json` | `02205af4ef7b94393c57307fd25209054f96f1f6148d60b6d73df746b55f2556` |

三份固定原文的本地檔重算為 G `5ac8c66266f84fb1fd01f50aab93044526c369df0d876c7e24dd20451f0053bd`、B `58062b750f1737ac908af48f3ec81016353404631978dc419138a5a2ef7a5ce9`、A `d9ab71205530a5df41dddf74090e598fcc4de06efba9eb234bffa07f20a61a1f`，與 `research.md` 固定值相同。`video.json` 所列三條固定版原文連結於本次 GET 均回 HTTP 200。R10→R11 差分為六句口播、同六格主張文字／錨點，以及 `cal099` 一景提示詞；沒有其他景、章、伏筆或設定變更。

| ID | 原文逐行核對及裁決 |
| --- | --- |
| `cal021` | [G L3338–3342](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L3338-L3342)明說船長到 Evans 房間詢問附近船隻，且 Evans 只說他**認為**鐵達尼號在附近。新句「船長於是去問無線電員」對。 |
| `cal049` | [G L3163–3168](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L3163-L3168)記 CQD 求救；[L3182–3195](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L3182-L3195)記白色火箭。此句只是從不明船燈引出下一章「還有什麼訊號」的問題，沒有說加州人號收到電文。 |
| `cal073` | [G L3182–3193](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L3182-L3193)明指 Boxall、`about eight rockets`；新句保留「英國調查報告說」及「大約」，未把八枚當逐一可驗的整數。 |
| `cal096` | [G L3470–3480](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L3470-L3480)逐字列 Stone 再保證「all white」，同時寫明與船長證詞矛盾；前兩句 `cal094/095` 已明指史東，新句「他再次保證」仍歸於史東自己的版本，沒有消去歧異。 |
| `cal099` | [G L3478–3491](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L3478-L3491)在 **L3479** 稱 Stewart 是 `chief officer`，L3483–3491 記他四點接 Stone 的班、聽到火箭回報；新句「接班的大副」史實成立。**錨點 HOLD：**`claims.md` 目前只直達 L3483–3491，欠 L3479 這個職務根據；應擴為 L3478–3491 或另添 L3478–3480。 |
| `cal120` | [G L3525–3543](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L3525-L3543)明列調查用碰撞、火箭、船影消失的時序推論所見船，距離則按 Lord 估測與報告另估；新句明說「推測／估」，只是提問，沒有把當夜辨認或五英里定值說成事實。 |

**書面畫面：**`cal099` 從泛稱值班水手改 `one chief officer listens near a bridge doorway`，對上 G L3479、L3483–3491 的史都華接班與報告，夜間／黎明前也合理；此一景 PASS，仍待真圖驗收。`cal021` 仍是「白天調查桌，匿名文書把兩個船模分開」，但 R11 口播已從抽象船橋做法改為船長夜間**實際走到 Evans 房間**。前後 `cal020/022` 都是當夜船橋／無線電室，白天桌景會把事件剪到事後調查，**書面畫面窄 HOLD**。最小提示詞可為：`Medium shot inside a 1912 cargo steamship wireless cabin at night, one shipmaster steps through the doorway toward a blank message slip on a desk, dim cabin lamplight`；一人一動作、無可讀字，且不畫可辨的 Lord 肖像。

**形式與後續界線：**獨立解析 `video.json` 得 134 句，正文 131 句與 `claims.md`、`script.md` ID／順序／字句逐字一致，另有片尾三句；131 個 `shot`、0 張卡、16 組 setup/payoff 均依序存在。CLI `lint --slug curio-s51 --json` 為 **0 errors、0 warnings**。R11 最快 325 CPM 文字估時為濃縮開場 36.37 秒、正文 8:38.60；R10 舊 WAV 的實測時長不可拿來放行 R11。企劃已指定開場後原創五秒片頭、21 秒片尾與最後 16 秒的兩推薦框／訂閱圈，說明欄已有三份固定史料和頻道連結；上述動畫、可點元素與音訊都還沒有在此版成片驗收。`brief.md` 開頭仍把 R9 寫為作者候選，說明欄仍有「獨立史料覆核待完成」的狀態句；修版／網站送審前需更新，不可把舊狀態當最新結論。

**放行條件：**作者只修 `cal099` 來源錨點、`cal021` 書面提示詞及過時交接文字，重凍結五檔；另一人獨立核新差分。同版兩名新讀者、完整政策、網站劇本卡、六句新 TTS 與 134 句零旗標音檢均尚待，故插圖、配樂、成片仍 HOLD。
