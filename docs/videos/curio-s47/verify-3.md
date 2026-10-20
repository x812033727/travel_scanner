# S47｜R2 敘事退稿與 R3 作者修訂

日期：2026-10-20。[R2 獨立來源與書面畫面差分](review/r2-source-independent.md)對 [R2 五檔固定 SHA](verify-2.md)判 **PASS**，但兩位真正新讀者在同一版上的 [A 報告](review/r2-blind-a.md) 11/13、[B 報告](review/r2-blind-b.md) 10/13。兩人共同把必答 `no_recap`、`chapters_are_events` 判 **No**：`wr019→wr020` 緊接著重說一分鐘約十二匹馬力；`wr096→wr097` 緊接著重說上午四趟；「兩支槳，三種麻煩」是題目桶，非發生的事件。B 還把 `no_spoiler` 判 **No**，因開場 `wr006/007` 先說出後段 12 秒及四趟。故 **R2 敘事 FAIL**；R2 的來源 PASS 不能移用給 R3，也沒有站台劇本核准。

R3 只沿 1902 年動力機設計、引擎與傳動軸、12 月 14 日坡上試飛、17 日四趟、當晚電報的一條時序窄修；保留固定 W/N 來源與 57／59 秒的歸屬界線。

| R3 改動 | 作者的來源及敘事界線 |
| --- | --- |
| `wr006/007` 及 `loops` | 開場改問救生員能否拍到**平地離軌**、給父親的電報把最長飛行寫成幾秒，不先報第一趟 12 秒或全天四趟。`wr006→wr063` 回收按快門，`wr007→wr092` 回收電報的 57 秒；其餘引擎、斷軸、山坡試飛與大風鉤子仍留著，開場不變成章節表。相機在畫面只**待拍**，不預演已拍得的照片。[W790–811](https://github.com/GITenberg/The-Early-History-of-the-Airplane_25420/blob/85d336f5a53986caf06e063025ca8189980962f3/25420.txt#L790-L811)、[N1613–1623](https://github.com/GITenberg/Wright-Brothers-National-Memorial-North-Carolina_57725/blob/063e08af43aae0605c0ad9f32f5ed08fa771fc29/57725-0.txt#L1613-L1623)。推薦 A 的開場企劃同步修正；B 仍是備選，網站尚未選案。 |
| `wr020` | `wr019` 已給馬達 16／12 匹測試值，下一景改給**機器連人容許重 750 或 800 磅**的新決策，不再立即重複 12 匹及原先 8 匹。這是 Orville 的後述，不說成現場秤重；畫面改成尚在組裝的翼架而非無來源的具體加厚動作。[W580–587](https://github.com/GITenberg/The-Early-History-of-the-Airplane_25420/blob/85d336f5a53986caf06e063025ca8189980962f3/25420.txt#L580-L587)。 |
| `wr087/088`、`wr096/097` | 陣風景直接推進機器被掀起的新事件，不再再次報四趟。片尾前 `wr096` 換成 NPS 小冊描述的**後續報導誤傳距離與時間、幾乎沒採電報資料**；只把它歸於小冊作者，不冒充逐份查過報紙。印刷桌為無可讀字的卡通示意。`wr097` 才用一次句子回收標題的「照片是第一瞬間、上午共有四趟」，並補首趟與四趟的分別引文。[W856–867](https://github.com/GITenberg/The-Early-History-of-the-Airplane_25420/blob/85d336f5a53986caf06e063025ca8189980962f3/25420.txt#L856-L867)、[N1625–1631](https://github.com/GITenberg/Wright-Brothers-National-Memorial-North-Carolina_57725/blob/063e08af43aae0605c0ad9f32f5ed08fa771fc29/57725-0.txt#L1625-L1631)。 |
| 八個事件章名 | 目錄所見章名改為第一個具體動作／發現：「兄弟選定雙槳」、「十二月十七日北風刮起」、「威爾伯正午再次起飛」、「兄弟發出報喜電報」等，不用枚舉題目或只稱文件內的秒數。章名改動不增加史實或口播字數。 |

## R3 凍結候選

| 檔案 | SHA-256 |
| --- | --- |
| [brief.md](brief.md) | `cc9cb908ea78b0e3e00402f2927744cdd8bf63572a3677ef9c56bec1d165a4ab` |
| [research.md](research.md) | `493d6bf8e73d9832c05300b2c9643e7e53c1448ac2215c54e2f32f9ad10fa357` |
| [script.md](script.md) | `d4572e39a9f08d5bbeaab8b3c81354e3a5877d8b85682d11fb72599759e361ff` |
| [video.json](video.json) | `9d97c4e50fbca0c3cc5854f45e147ddf4a3f4dc89ca38453990425454a1cdd7d` |
| [claims.md](claims.md) | `5a416f85fb3bf78646bf31e6edeef7327bd9e08c4eac3c664c61c9bd8176ac3c` |

R3 作者機械檢查：已從上表 `video.json` 重新生成 `script.md`；97/97 正文 `shot`，100/100 句（含三句片尾）與 `claims.md` 按 ID、順序及口播逐字一致；112 個固定 W/N 行號連結有效；13 組伏筆前後 ID 有效。`lint --slug curio-s47 --json` 為 **0 errors／0 warnings**；`git diff --check` 無格式錯誤。開場以 250 單位／分鐘含景間停頓估 **56.57 秒**，以更快的 325 單位／分鐘估 **45.4 秒**；後者正文 `wr009` 至片尾前為 **489.3 秒（8:09.3）**，前者為 **608.87 秒（10:08.9）**。純口播正文 2161 單位按 250 單位／分鐘為 **518.64 秒（8:38.6）**。這些是靜態估算，**不是 TTS 實測**；原創 5 秒片頭、21 秒片尾及最後約 16 秒推薦／訂閱框仍是製作規格，未組片或啟用可點連結。

R3 **須由另一人作新的來源及書面畫面差分審核，並由兩位全新、互不相見的讀者在上表精確 SHA 各評官方 13 題**。A 僅是本機推薦；S47 尚無網站大綱／劇本核准，也沒有付費語音、原生插圖、配樂、成片或上傳。
