# S54 R6｜固定來源與書面畫面獨立差分覆核

2026-10-20 UTC。**PASS**，僅限本頁精確五檔的來源、逐句主張與書面畫面；敘事盲評、政策、實際圖像及音訊另驗。我未撰寫 R6 稿。

| 檔案 | SHA-256 |
| --- | --- |
| `research.md` | `57f24b58a1d407825f71fcd389576ae0ae77e6a547d87b5e1ca8be17863557fa` |
| `brief.md` | `9ee29f8d25d0c3044c2b42e6d3b8982c3f9426b81cef06998d1a4ad25432c4fe` |
| `claims.md` | `a10df345472a8a8f94f9f0ca1dba709211b2a364a70c9ac879b4e6eaff2399dd` |
| `video.json` | `b29d73b97759d575d58c6934c06b2bf8c673c0c60a58330e330518f2b4e5e332` |
| `script.md` | `33ae45c7addd0088918128a5711969c128bbe4b692743b71cc5703f16deb73ef` |

我從固定 Git 提交重新下載 [希爾回憶錄第一卷全文](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt)，位元組 SHA-256 `3bdf96943eea935aec86101874f15aa8f60d518db1437902da52b446f006f939`，與研究檔及 R5 獨立覆核相同。這是希爾事後回憶及其日記轉錄，旁白保留歸屬，並不稱作郵局逐站原始帳。

| R5 HOLD 項目 | R6 獨立對讀 |
| --- | --- |
| `s54071` | [H L13049–13059](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt#L13049-L13059) 轉錄 Bokenham 說 *not more than one letter in twenty* 上秤。新版「每二十封信，**最多**只有一封得上秤」準確保留上限；秤的概念插圖沒有另加比例。 |
| `s54118` | [H L13328–13359](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt#L13328-L13359) 從 5 月開售與准用轉入倫敦收件所未配發；主張列已直接附上 P10 的 13354–13359 行。畫面改為匿名職員移動**無字封包／分發板**的概念示意，顯示分發動作，沒有提前展示短缺、杜撰真實文件或指定歷史人物。 |
| `s54120→s54121` | `s54120` 問希爾聽到何種配發消息時，只畫闔上的無字庫存簿；`s54121` 才用空供應架回答，與 [H L13354–13359](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt#L13354-L13359) 及旁白順序一致。 |

R5 的 [獨立覆核](r5-source-independent.md) 已將其餘主張與書面畫面逐項對讀固定來源；R6 作者凍結記錄的改動集中在上表三景，`research.md` 未改。再次對比現稿，148 個正文場景的 ID／口播字串與 148 個 `claims.md` 列**逐列一致**，22 組 loops 留存；`lint --slug curio-s54 --json` 為 **0 errors、0 warnings**。R6 剩餘敘事效果仍須由未讀過此稿的兩位讀者獨立盲評。
