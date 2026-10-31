# S51 R7｜R5 至 R7 史料與書面畫面獨立差分覆核

2026-10-20 UTC。對下列**精確 R7 五檔**，**旁白史料 PASS、逐句主張 PASS、書面畫面 PASS**。R6 作者的來源差分尚未有獨立簽核，因此本次從 [R5 獨立基線](r5-source-independent.md)往後逐景核 **R5→R6→R7 全部改動**，並直接重讀固定原文；作者 [R6](../verify-6.md)／[R7](../verify-7.md)自檢僅供找改動，不作證據。這是文字和提示詞審核，不是新讀者的敘事裁決，也不是生成圖片的驗收。

| 精確 R7 內容檔 | SHA-256 |
| --- | --- |
| `brief.md` | `5148d751b485260650d2d8661c5898ce0b85cec6284677527d271fa3384ace5a` |
| `research.md` | `039ca3ecc3f5099537e51e48d0f1788faf0bdf9c5d254f2ae64dd5ff89b56459` |
| `claims.md` | `ef7f985a542fd7ea52977b23477bf8464f4176bb1d6415efd71ce294996a48d0` |
| `script.md` | `76bb8c3669eab045363b4e726483085b0ef1cb3257e83268fa1a55196819517a` |
| `video.json` | `0efe5126f5f24edf08fdc75bf626b1000f0192e9e6a17d421b2d7dd871d4a081` |

重新核對三份固定轉錄本原始位元組：英國正式調查 G `/tmp/s51-independent-sources/british-report.txt` SHA `5ac8c66266f84fb1fd01f50aab93044526c369df0d876c7e24dd20451f0053bd`；Beesley B `beesley.txt` SHA `58062b750f1737ac908af48f3ec81016353404631978dc419138a5a2ef7a5ce9`；Gracie A `gracie.txt` SHA `d9ab71205530a5df41dddf74090e598fcc4de06efba9eb234bffa07f20a61a1f`。原文版次與固定 Git 連結均列在 [research.md](../research.md)。G 是報告歸納與證詞摘要，不把兩者混作當夜共同目擊；B 和 A 只在各自能親見的範圍用作目擊，兩人的事後推測沒有變成旁白定論。B [L2636–2659](https://github.com/GITenberg/The-Loss-of-the-S.-S.-Titanic--Its-Story-and-Its-Lessons_6675/blob/98d777343615ef35522ca8e04e451ec5d7f37eb3/6675.txt#L2636-L2659)還明說蓄意忽略應暫緩判斷；A [L597–649](https://github.com/GITenberg/The-Truth-about-the-Titanic_67584/blob/a2cbb33f09c5ce0ff00a78581a56cb6756967c42/67584-0.txt#L597-L649)的船長心態與距離說法是事後解讀。

## R5→R6→R7 來源差分

| ID | 獨立核對 |
| --- | --- |
| `cal034` 刪除、`cal060` 改句 | G [L3340–3354](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L3340-L3354)記 Evans 約 **23:30** 休班，G [L3182–3197](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L3182-L3197)直記加州人號未收到鐵達尼號的求救電文，唯一無線電員睡去；A [L605–615](https://github.com/GITenberg/The-Truth-about-the-Titanic_67584/blob/a2cbb33f09c5ce0ff00a78581a56cb6756967c42/67584-0.txt#L605-L615)還記「put the ’phones down」。R7 `cal060` 首次把漏收說明放在求救電文已發出後，具體回呼 `cal004` 摘下的耳機；`claims.md` 同列 R03／R05，並未把無線電艙無人推成船橋無人。刪 `cal034` 沒有刪掉來源必要事實；`cal004→cal060` 的伏筆順序有效。 |
| `cal106`、`cal108/110/111/112` | G [L3484–3510](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L3484-L3510)先記夜船燈影消失、清晨又來一船，約 **06:00** 得沉船消息才啟航；R7 `cal106` 留下船名疑問，沒有再重說前句的啟航。G [L3525–3542](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L3525-L3542)在報告歸納裡以停船時刻、約八枚白火箭及時段、02:40 燈影通報對照 02:20 沉沒；`cal108/110/111/112` 都按這些事件說，`cal111` 明以「報告認為」標示數量對得上的層級，沒有抹掉值班員五枚與船長一枚的證詞差。`cal114` 才說報告據此**認定**船名，沒有寫成船員當夜知道。刪 `cal109/113` 只合併相鄰重述，不漏掉原文條件。 |
| `cal135/136` | G [L3428–3435](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L3428-L3435)以 **Stone 說法**寫船長讓他續打摩斯、有新消息就派實習生報；R6 新 `cal135` 保留前述未說過的實習生細節，並只說這段回話**沒有起航指示**，沒有推斷 Lord 動機。G [L3473–3481](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L3473-L3481)明記船長只記得一枚與 Stone 五枚的矛盾，支援未改的 `cal136` 限制。G [L5670–5681](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L5670-L5681)另記最終未嘗試前往；不拿這個後見結果證明每句當夜對話。 |
| `cal137` 刪除、`outro` | G [L3543–3550](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L3543-L3550)認為若及時航行**可能**救下多人，沒有可證的反事實救援人數；新 `cal999a`「究竟能救多少人，史料無法回答」恰當。片尾短卡「能救多少人，無法回算」與正文 `cal132` 的調查「未嘗試」分工，沒有把可能救下多人寫成確定人數。刪 `cal137` 只移除預先重說片尾的句子。 |
| `cal121` 章名 | G [L3509–3550](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L3509-L3550)並列自報船位、Lord 目測約五英里與報告的八至十英里估計；R7「調查對照船位與目測距離」是事件章名，沒有替距離設單一真值。正文未改。 |

## 書面畫面及整體對齊

R5→R7 的唯一**留存**提示詞改動是 `cal106` 後續日間證據桌的 `desk`→`table`，仍是匿名研究者、無字海圖與無標記雙船模型；沒有畫成當夜船員已知船名、可讀虛構原件或定值航圖。`cal034/109/113/137` 四景與提示詞隨口播刪除。`cal060` 的日間空白訊號紙為後來整理證據的示意，非宣稱當夜實有一張可讀紙；`cal108–112` 的時刻卡、無字計數物與漸暗燈光圖只表示**報告的後來比較**，不精確重建聽證、火箭顆數或兩船位置。`cal135` 留存的通話管／燈／信差剪影三張無字符號卡沒有指名人物、捏造回話文字或 Lord 肖像；片尾卡留空救援人數。其餘提示詞與 R5 基線一致；這是**書面**驗收，生成後仍須原尺寸逐張看。

我獨立解析 `video.json` 的 **136/136** 個 ID 唯一台詞、`claims.md` **136/136** 同 ID／同序／同文，並用 CLI `screenplay(doc)` 與 `script.md` 逐位元比較；**133/133** 個 `shot` 提示詞非空，**16/16** 條 setup/payoff 指向存在且有序的台詞。`lint --slug curio-s51 --json` 為 **0 errors、0 warnings**，`git diff --check` 通過。`estimateTimeline` 在 325 單位／分的首八景為 **36.37 秒**、其後正文 **526.77 秒（8:46.77）**，只是文字估時，真實 TTS 尚未合成。`video.json` 的 YouTube 說明仍稱獨立查核待完成，成片前須依最新關卡結果更新並重綁檔案雜湊，不能直接用這份前製說明上傳。

**裁決：R7 旁白史料 PASS；逐句主張 PASS；書面畫面 PASS。** 只對上表精確五檔有效。兩位全新隔離讀者的同版敘事審查、政策、站台、配音、生成插畫和成片均待後續各關完成。
