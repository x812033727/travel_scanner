# S48｜R3 敘事修訂與再審交接

2026-10-20 UTC。R2 的[獨立史料／書面畫面覆核](review/r2-source-independent.md)通過，但兩位全新讀者的[合併敘事判定](review/r2-narrative-merged-reported.md)為 **FAIL**：共同未通過 `no_spoiler`、`chapters_link`、`no_recap`。個別回報為 [A 8/13](review/r2-narrative-a-reported.md)、[B 10/13](review/r2-narrative-b-reported.md)；原始逐題 JSON 未保留，這裡只記轉交的摘要，不補造讀者引文或 CLI 收據。R2 的史料 PASS 綁舊雜湊，**不能移作 R3 通過**。下表是作者修稿和本機檢查，R3 仍須另一人做獨立史料／書面畫面差分與兩名新讀者盲讀。

| 固定稿 | R2 SHA-256 | R3 SHA-256 |
| --- | --- | --- |
| [brief.md](brief.md) | `c4a7a6fb51dcfc59429b834047cfbb657f2c73dd0e2c254ca018e4bf00af84d4` | `be0db246ddf465d5cb148d1d7643786f032e95035ba136d060b2f19eb56c03d4` |
| [research.md](research.md) | `67f286745510347b2ad8ce1dcb4bd2cbf46634a8c6574c0360bc4e089c0b7f53` | `359bac565ba26f6452b10dac75f4a6687b5280e32ff72f5da948a2065354b57d` |
| [video.json](video.json) | `431f19fcf13bc325df7de65678fcc6d34368becb946a722ca931e9a3786032f3` | `e9fcb7144a5b4c79438a256ae2d2775fd1cf77e0e405a038da7d63f3b77b1786` |
| [script.md](script.md) | `4cacc1bc8e130373d0783dad3382209be4fbbbc04a69b38b86221b294d53e898` | `77f1aed38bdfef8523ea0c795f2ba9630980f887e4122cb40390d770e6f366a8` |
| [claims.md](claims.md) | `f85eae29e70897fadc62e07bd13348443ee2faaccc739f3a593ff447586e7054` | `8e139d4ed30a15e2635cf873613853f6ff2138684bccfad88992f13ed1043cbc` |

原始兩份固定文字 SHA 未變：Russell `558efcc342df669e7387ffff818c104690e7ec910de49e795f996abf147ea750`，Field `bee659b24ace56a5e1f7104a6a306e9325ccd9c864fc373ad35b0863c5a8c675`；本機重新核對下載檔位元組。來源行號與見證層次見 [research.md](research.md)。

## R2 敘事 FAIL 的逐點修訂與作者史料自查

| 段落 | R3 改動 | 自查依據或界線 |
| --- | --- | --- |
| `atl004→023`、`atl006→077` | 開場停在七月壞線待查、隔年船朝浮標駛近；不先說鐵線碎片或海面見線。英語畫面提示詞只描述連續護套、浮標與抓鉤繩，不以否定提示詞提及待揭曉物。 | 第一段壞線實在 7 月 25 日收回後發現碎片：[Russell R3020–3050](https://github.com/GITenberg/The-Atlantic-Telegraph_40948/blob/ba499c6bc32adef8c8a91a306dcb2d54bf7e898d/40948-0.txt#L3020-L3050)；8 月 17 日才肉眼見線，總約五分鐘、斷時即沉：[Field F9440–9472](https://github.com/GITenberg/The-Story-of-the-Atlantic-Telegraph_34765/blob/6b50b44d3cd2f3f1831e2c1a8fa052f53c51a4cd/34765.txt#L9440-L9472)。開場甲板工作桌是卡通示意，不能當原始照片或獨立證物紀錄。 |
| `atl007–010` | 開場最後仍問沉線能否通對岸，正文首句明說 1865 新線為重建中斷通訊，才回到 1858 曾通、9 月失訊的舊線。 | 1858 已有訊息交換及失去可讀訊號：[Russell R1280–1413](https://github.com/GITenberg/The-Atlantic-Telegraph_40948/blob/ba499c6bc32adef8c8a91a306dcb2d54bf7e898d/40948-0.txt#L1280-L1413)；不宣稱 1866 是首次跨洋通訊。 |
| `atl033–035/036/041/057` | `atl034` 改成兩小時換班監看，`atl057` 後來才講 Russell 在船上儲放線圈看到護線脆斷；`atl036` 加入靠岸用線轉移，`atl035` 的里程問句由 `atl041` 的 1,186 英里回答。 | 調任水槽工人、志願監看人兩小時輪班見 [Russell R3585–3615](https://github.com/GITenberg/The-Atlantic-Telegraph_40948/blob/ba499c6bc32adef8c8a91a306dcb2d54bf7e898d/40948-0.txt#L3585-L3615)；靠岸用線從主水槽移到船尾見 [R3633–3650](https://github.com/GITenberg/The-Atlantic-Telegraph_40948/blob/ba499c6bc32adef8c8a91a306dcb2d54bf7e898d/40948-0.txt#L3633-L3650)；1,186 英里與 9:58 切線見 [R3768–3774](https://github.com/GITenberg/The-Atlantic-Telegraph_40948/blob/ba499c6bc32adef8c8a91a306dcb2d54bf7e898d/40948-0.txt#L3768-L3774)；脆線是**船上存線盤**的觀察，見 [R4093–4103](https://github.com/GITenberg/The-Atlantic-Telegraph_40948/blob/ba499c6bc32adef8c8a91a306dcb2d54bf7e898d/40948-0.txt#L4093-L4103)。船上猜破壞不等於已查出兇手。 |
| `atl081→082` | 問另一船帶回哪一段，答此前抓斷的約兩英里殘段；新的長度與來源資訊區分它和仍通往愛爾蘭的完整舊線。 | Field 後出敘事 [F9510–9530](https://github.com/GITenberg/The-Story-of-the-Atlantic-Telegraph_34765/blob/6b50b44d3cd2f3f1831e2c1a8fa052f53c51a4cd/34765.txt#L9510-L9530)。 |
| `atl098–100/atl999a` | 按時間講續鋪後 36 小時暴風、Field 所引 Cyrus Field 在暴風中收到家訊、9 月 7 日第二條線到岸；片尾改問觀眾何時才敢確認，刪重述撈線程序。 | [Field F9720–9750](https://github.com/GITenberg/The-Story-of-the-Atlantic-Telegraph_34765/blob/6b50b44d3cd2f3f1831e2c1a8fa052f53c51a4cd/34765.txt#L9720-L9750)。家訊屬 Cyrus Field 引文，Henry M. Field 並非因此成為全程船上目擊者；也不推論此後永不故障。 |
| `atl027/037` 書面畫面 | 原提示詞殘留的 `pointer` 改為鏡面反光點與無數字刻度。 | Russell 描述 Thomson 光點儀器：[R2865–2924](https://github.com/GITenberg/The-Atlantic-Telegraph_40948/blob/ba499c6bc32adef8c8a91a306dcb2d54bf7e898d/40948-0.txt#L2865-L2924)。全份 `video.json` 已無 `pointer`／`needle` 英文詞；原生圖仍須另看。 |

## 本機驗證與未完成關卡

`node tools/video/cli.mjs script --slug curio-s48` 重生 R3 [script.md](script.md)；`lint --slug curio-s48 --json` 為 **0 errors／0 warnings**。逐列比對 [claims.md](claims.md) 與 JSON：**103/103 句一致**；100 張規劃插圖 `shot`、20 條懸念、11 章。開場口播及畫面提示詞檢查無提前揭曉碎片／見線的字眼，也無針式電流計用詞。以上是作者的機械和史料自查，沒有替代獨立讀者判斷。

`estimateTimeline` 含停頓、**不等於合成語音實長**：

| 語速（單位／分） | 30–60 秒開場 | 不含片頭／片尾的正文 | 三句片尾 | 全旁白 |
| --- | ---: | ---: | ---: | ---: |
| 250 | 55.4 秒 | 10:55.6 | 15.4 秒 | 12:06.4 |
| 300 | 47.4 秒 | 9:20.6 | 13.2 秒 | 10:21.2 |
| 325 | 44.5 秒 | 8:45.8 | 12.4 秒 | 9:42.7 |

原創 5 秒片頭**規劃**接在濃縮開場後；`v4-endscreen` 片尾**規劃** 21 秒，最後 16 秒放兩個推薦框與訂閱圈，私人上傳後才可在 Studio 設可點連結。這些動畫、連結、TTS、音訊驗收、MiniMax 原生插畫、組片與上架均尚未製作；本交接不聲稱 R3 獨立史料／畫面或雙盲 PASS，也不聲稱站台 A 案／劇本已核准。任何改字或改提示詞須重新凍結五檔 SHA，再做獨立差分與兩名**全新**讀者的官方 13 題盲讀。
