# S51 R3｜固定來源、逐句主張及書面畫面獨立差分覆核

2026-10-20 UTC。**旁白史料 PASS、六景書面畫面 PASS；整份來源包暫列 HOLD，僅因 `claims.md` 的 `cal061` 漏列船橋值班／火箭段落錨點。**這是作者凍結後的獨立文字查核，不是兩名敘事讀者的正式盲評、生成圖驗收、站台核准或媒體完成。

我直接重讀三份固定電子轉錄，並與 [R1 完整來源覆核](r1-source-independent.md)、[R2 書面畫面 HOLD](r2-visual-independent.md)及 [R3 作者凍結](../verify-3.md)比對。`/tmp/s51-independent-sources/british-report.txt` SHA-256 `5ac8c66266f84fb1fd01f50aab93044526c369df0d876c7e24dd20451f0053bd`；`beesley.txt` `58062b750f1737ac908af48f3ec81016353404631978dc419138a5a2ef7a5ce9`；`gracie.txt` `d9ab71205530a5df41dddf74090e598fcc4de06efba9eb234bffa07f20a61a1f`。它們是固定電子轉錄，不冒稱原件逐頁掃描。原著與旁白的 R1 PASS 適用於未改的句子；下表只對 R3 改句重新判斷。

| 凍結檔 | SHA-256 |
| --- | --- |
| `brief.md` | `82a2e4a3d7a240dd0f249eeeec3b3dffdf1446d9eb049432320e72fe6b6a1023` |
| `research.md` | `039ca3ecc3f5099537e51e48d0f1788faf0bdf9c5d254f2ae64dd5ff89b56459` |
| `claims.md`（待補一個錨點） | `d711c1f0279e8fa7a2cf1d29683b0ba1540767fc4b5d5bfe8a8cbe179add111b` |
| `script.md` | `734cf4d7c474cd24a7dba87db738d07575654cbbd4ec84ad7006a7ff4b795a40` |
| `video.json` | `70aa784c4f6175e557e3addd6550e2c0068047bac85e0a3a9690a81b1b855226` |

## 十二句改稿的原文核對

| ID | 直接原文與裁決 |
| --- | --- |
| `cal032–033` | [G 3340–3351](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L3340-L3351) 記 Evans 23:30 下班；[G 3192–3197](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L3192-L3197) 明記船上只有一名 Marconi 員、睡著而未收求救。分成休班與無人接班兩句，PASS。 |
| `cal059–061` | 同一 [G 3192–3197](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L3192-L3197) 支持未收求救電文；[G 3420–3442](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L3420-L3442) 支持**船橋仍有人值班**且後來看到白火箭。旁白 PASS。但 `claims.md` 的 `cal061` 只連研究 R05；R05 的 G 3163–3197、3525–3528 沒寫船橋值班與目擊，須補 **R07** 作雙錨點，見下節。 |
| `cal075–076` | [G 3427–3434](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L3427-L3434) 記 Stone 自稱約 01:10 以 voice pipe 報五枚白火箭，Lord 反問是否公司訊號；「會。他拿起通話管」按 Stone 證詞層級回答，PASS。 |
| `cal083–084` | [G 3435–3440](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L3435-L3440) 記 Gibson 又見三枚，[G 3450–3465](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L3450-L3465) 記 Stone 吩咐報總數、Gibson 自稱下樓告知船長。新版明說「吉布森後來說，有報到；但那只是他的證詞」，不將爭議通報當定論，PASS。 |
| `cal088/090–093` | [G 3450–3481](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L3450-L3481) 記 Stone 指示 Gibson 報八枚和摩斯未答、Gibson 自稱約 02:05 告知船長，Lord 則只記一枚、不記後續；[G 3525–3536](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L3525-L3536) 說證詞矛盾、Titanic 約 02:20 沉沒。`cal088` 的「他說自己把……一併報給船長」是 Stone 交辦內容和 Gibson 自稱告知的合併轉述，仍保留自述語氣；不逐字誤稱 Gibson 留下了報話全文。`cal093` 不從衝突證詞推斷 Lord 當夜已知船名，PASS。 |
| `cal111` | [G 3525–3537](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L3525-L3537) 把 Titanic 發射約八枚與 Californian 看見八枚作對照，且這是正式調查**推論**；新版說調查把數量對上，PASS。 |

## 六景 R2→R3 提示詞差分

| 景 | 書面畫面裁決 |
| --- | --- |
| `cal040–041` | **PASS。**已移除 R2 無來源的 `light shutter`，改由事後日間證據桌的無字船模相對固定視角轉向，讓模型輪廓可能遮住部分甲板燈；這符合 [G 3390–3393](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L3390-L3393) 的**可能**解釋，沒有宣稱真的有人操作遮燈器或全船熄燈。 |
| `cal064` | **PASS。**畫單枚白色求救火箭從緊急艇旁固定座升空、在空中散成白色星點，與 [G 3182–3187](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L3182-L3187) 相符；未畫手持彩色煙火或把約八枚放同一時刻。 |
| `cal104–105` | **PASS。**約 06:00 收到沉船消息及開始穿冰區出航見 [G 3498–3501](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L3498-L3501)。`early morning daylight` 只示意早晨，沒有再斷言此刻是第一道曙光。 |
| `cal133` | **PASS。**[G 3207–3219](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L3207-L3219) 明記 Carpathia 04:10 接上首艇時 `just daylight`；新版 `first daylight` 修掉 R2 的 `before dawn`。船員與繩梯是救援動作的卡通示意，並非本固定原文證實的**確切登船器具**；實際圖若呈現成「已認證原船細節」仍須另拒。 |

比對 `/tmp/s51-r1-video.json` 與 [R2 的 75 景精確差分表](../verify-2.md#精確提示詞差分)，每列 R1 舊詞吻合；R2→R3 只有上述 **6 個 `data.prompt`** 再改，其餘 69 個 R2 修景和未列的 62 景提示詞不變。R1→R3 只 **12 句旁白**改詞（ID 如上），場景其他欄位未變。`video.json`／`claims.md`／`script.md` 的 **140/140** ID、順序與字面一致，互不重複；137/137 正文景為有非空提示詞的 `shot`。`lint --slug curio-s51 --json` 是 **0 errors、0 warnings**。此為書面提示詞 PASS，尚未生成或目視驗收原生圖。

**唯一須修的來源錨點：**`claims.md` 的 `cal061` 現寫 `[研究 R05]`；該句「可是船橋還有人值班，夜空裡快出現另一種信號」的第一半由 G 3420–3442／研究 **R07** 支持，第二半由 R05 的無線電休班情境與 R07 的火箭連接。請只改該格為 `[研究 R05、R07]`，不動口播、研究固定原文或提示詞，重算 `claims.md` 雜湊，再由另一位覆核者核對這一格的差分。**在此之前不將整份來源包標成 PASS。** R1 敘事 FAIL 仍須兩位對精確 R3 `script.md` 作真正隔離、只讀劇本的正式新盲評；沒有 TTS、付費圖、配樂、成片、上傳或 Studio 可點片尾元素。
