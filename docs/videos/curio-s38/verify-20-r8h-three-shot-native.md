# S38 R8h｜三景窄範圍原生圖驗收與停點

2026-10-21 00:27 UTC。**`pf004`、`pf005` 原生 KEEP；`pf006` 原生 REJECT，整集繼續 STOP。** 此處的兩張 KEEP 是逐張查核的插畫，並非 1666 年目擊影像、站主網站分鏡核准或已完成影片。

## 固定版本、界線與帳本

- 三次指名景試畫均對應 `video.json` SHA-256 **`7e9eb1a2019bbf55727ac08c1bf273fc2fbf420223c6425083558afbfb9b0631`**、`visualHash` **`1f353c19c4d07f47`**，先完成 [R8h 精確紙上覆核](verify-19-r8h-independent.md)及逐景 `--takes 1 --dry-run`。每次只暫停私有 `STOP` 執行一個指定景，再由外層 `EXIT` trap 恢復；結束後實測 `STOP` 存在。`pf003` 從未送出，`pf007–111` 未開畫。
- 開始前 ledger US$0.2355，其中舊 `pf003` US$0.0035 reservation 未解；整集 image、judge、music 累計硬上限 **US$4.58** 不變。三次 image + judge 各 US$0.0135，現 ledger **US$0.2760**：16 張 image、14 次 judge、1 首 music，含同一筆未解 reservation。網站音訊卡仍等待站主；本機委派決定不能等同親耳試聽。
- 原始工具輸出留在私有 `/tmp/curio-s38-r8h-pf004-last-pilot.log`（SHA-256 `66ba621fd6470290415ec1b479aeaa5a04911ce84479d685b2bc0dfdeeff5e1b`）、`/tmp/curio-s38-r8h-pf005-pilot.log`（`4aed814940071bb5805c5ece1612ebd4cc0198c7a6af2b4026d72f2410bb3ff1`）及 `/tmp/curio-s38-r8h-pf006-pilot.log`（`dd671a21f95f1ab2bedf4702af76af1b4121effcabae934498354b618c60f026`）。`pf004` 首次 R8f 判退圖另留私有 `review/r8f-pf004-rejected.jpg`，SHA `153d7687e6f0c0d8074d720e3ced300115025f26918e4af6a195611f313d1070`。

## 原生 1280×720 圖片判定

| 景 | 原生圖／manifest 選圖 SHA-256 | 機器與肉眼結果 |
| --- | --- | --- |
| `pf004` | 原圖 `a7e03fc464f40ce1b22e8b3f40447021e78f4afcfa41ee25b6f47817dcb1f771`；選圖 `pf004-1-trim.jpg` **`82efccf4b92bc59da94688527fd43e9347ad45d271b048e0877a8f3337bb7921`** | Judge 9.29／10 PASS，`needs_review=false`。我直接看選圖：人物顯然成年、在圍牆邊指向屋頂後的遠火，房屋尚完整，畫風是平面卡通。人物下半身被牆遮住，未做到提示詞的全身景，但懸念與來源沒有被改寫；磚屋與庭園只作概念示意，不標成佩皮斯家的精確重建。**KEEP。** |
| `pf005` | 原圖 `9d59c8ae90ef164a52e65ff53a0f3a1243288159324bf235417cc52e796bbbe0`；選圖 `pf005-1-trim.jpg` **`34ff83a651a59ba9383091d33151ca4bce62c9d04d6f65bd4bc75dbf55e8c52c`** | Judge 9.29／10 PASS，`needs_review=false`。原圖是一位明顯成年讀者在燭旁看空白頁，沒有已挖回起司、可讀假文字或現代辦公椅；領口與手勢未完全照提示詞，亦非日記原件或佩皮斯肖像。作「日記有沒有交代？」的概念景 **KEEP**。 |
| `pf006` | 原圖 `e955a70fc2119877fc519ff43ed8d60584fd35cd332880dbd336a94601d1a9f0`；判退圖 `pf006-1-trim.jpg` **`a87978e35d8cfb9355ca75969aca21a5082f701da2887dc3503a36471320a78f`** | Judge 8.41／10 FAIL，`needs_review=true`：3D 感、人物在窗內而非探窗、黑邊、非側面。我直接看原生圖：女僕仍明顯童貌，坐在室內，火光像貼在窗外，與 9 月 2 日成年女僕叫醒佩皮斯看遠火的示意不合。**REJECT**；私有 `review/r8h-pf006-rejected.jpg` 留同 SHA。 |

工具因本容器欠缺對應 Playwright Chromium 未建立 contact sheet；以上判斷直接讀原生 JPEG，不能把 contact sheet 失敗當成已通過，也不應只靠機器總分。

## 下一關

先只修 `pf006` 的 `data.prompt`，保留全系列 `look: cute-mystery`，不在單景寫 `cartoon`、`vector`、色盤或負面風格。新作者須核對 D2a 固定日記、成年女僕、遠火、單人單動作，再由**未撰詞者**做精確差分紙上覆核。`pf006` 至多再 **一次 1 take + 1 judge** 原生重試；如仍 REJECT，維持 STOP，不因兩張 KEEP 就續開後面一百餘景。`pf003` 的不明 reservation 須獨立對帳，不得算作免費圖片或直接清除。即使三景 3／3 KEEP，仍須新的整體分鏡關卡、30–60 秒濃縮開場補足，以及網站站主的實際審核，才可完成此集。
