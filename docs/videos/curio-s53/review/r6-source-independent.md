# S53 R6｜六句語音改稿的史料與書面畫面獨立覆核：HOLD

2026-10-20 UTC。此覆核只適用以下五檔。R5 的 [逐句獨立覆核](r5-source-independent.md)曾對其餘句子及書面提示詞 PASS；本次重新開原文，審 R6 改過的六句。**史料／時間線 HOLD 一句 `s53096`，書面畫面 PASS**；尚不能拿此稿進政策或新語音關卡。

| 檔案 | SHA-256 |
| --- | --- |
| `brief.md` | `8e44f47693dd75ad0a7509ab0f495c06adcc2e614b8c8bc09a51559d7202a27c` |
| `research.md` | `2e61530c650852281402476041175154ee69c414daf7431d6aa0db352e7c3d22` |
| `claims.md` | `72b5c0a33b0cf119193a6a6aa6edd6fc70819d5aedc915d8f3b0b00e4cfad152` |
| `video.json` | `429789688823f0162d5153d88b759baba7943ca8bb2e8c70191c9d478e66411e` |
| `script.md` | `f6810742591e4a713f9431d06d6895126d5491c14ba15d14ef51c39bec45faf5` |

重新下載固定提交的 [1913 年《San Francisco Relief Survey》全文](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt)，原始位元組 SHA-256 `d627ed287d8a93b9c00225ea47dbdc4f97c36089a890192a602b993c3c185b72`，與研究表相符。它是 1913 年機構調查編纂，不是 1906 年當日逐筆原檔。R6 相較 R5 的 `video.json` 逆向換回六句可逐位元重現舊 SHA `2d9e0036e03712028890b4c9af01d776f13394baabefb7cb389b8bb6b6c28f1d`；`claims.md` 同法重現 `6a0a1f315fb21baeec5665d0996a97be17b62239b1f72abe5ca93a3b26dab5a5`。新 `script.md` 是工具按新分鏡重新產生，尾端內容雜湊亦隨文字變；127 句與 claims 逐句對齊。`lint --slug curio-s53 --json` 為 0 errors、0 warnings。

| 句子 | 核對 |
| --- | --- |
| `s53003` | 原文 [L4983–4987](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L4983-L4987) 記 1907 年 6 月要求 8 月 17 日清走廣場小屋；開頭已標 1907 年 6 月，「那年夏天」合理。廣場小屋鏡頭對位。 |
| `s53014` | [L4848–4865](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L4848-L4865) 明寫先有帳篷、雨季將至才決定建小屋。「暫時躲雨、休息」是帳篷的普通用途，沒有把它說成長期或完善安置；無字帳篷示意合適。 |
| `s53070` | [L4983–4987](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L4983-L4987) 的 squares and parks 支持清場範圍；無字多區塊地圖不硬畫位置。 |
| `s53096` | **HOLD。** [L5011–5018](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L5011-L5018) 記慈善機構搬修從 **1907 年 7 月**直到 **1908 年 6 月下旬**。本句說「直到**那年**六月下旬」，但本章及其相鄰句未先標 1908 年，前面最明確的年份為 1907 年，會把終點誤聽成開始前的 1907 年 6 月。改為「直到**一九〇八年六月下旬**」即可；搬修部分小屋的主語與書面修繕鏡頭本身正確。 |
| `s53099` | [L10502–10520](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L10502-L10520) 記訪查員到搬屋後給出的 1,137 個地址尋屋，取得 680 份較完整資料；「尋找家庭」沒有說全找到，無字地址簿畫面也不冒充實物。 |
| `s53129` | 同一 [L10502–10520](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L10502-L10520) 區分 680 份完整紀錄與另知 23 起地租扣屋；提問讓下句回答，不把 23 放入 680。未完成訪查頁畫面合適。 |

修訂 `s53096` 並同步主張／劇本後，請按新雜湊做時間線差分覆核；R5 舊音訊及政策回條均不適用於新稿。
