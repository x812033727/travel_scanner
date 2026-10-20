# S53 R8｜兩句來源與書面畫面獨立差分覆核：PASS

2026-10-20 UTC。此結論只涵蓋 R8 精確稿的來源、逐句引證及書面分鏡；敘事雙盲、政策、R8 旁白與成片仍須另驗。

| 檔案 | SHA-256 |
| --- | --- |
| `brief.md` | `8e44f47693dd75ad0a7509ab0f495c06adcc2e614b8c8bc09a51559d7202a27c` |
| `research.md` | `2e61530c650852281402476041175154ee69c414daf7431d6aa0db352e7c3d22` |
| `claims.md` | `dcc27889e8302545758345327e86e65f64fb860f2e9fbe35586a3dd7907b847a` |
| `video.json` | `7a0b948c52db433c0cda958bb376c56c560b746a4550b07adf174f3493f6f06a` |
| `script.md` | `209c65b528aed2c36083588ed11c5be2869434571d405367bef2e1f1ef4a0d8d` |

我直接重開固定 1913 年 *San Francisco Relief Survey* 全文 `/tmp/s53-sf-relief/56217-0.txt`，原始位元組 SHA-256 `d627ed287d8a93b9c00225ea47dbdc4f97c36089a890192a602b993c3c185b72`，與研究表相符；不以作者摘要代替原文。[R L4972–4985](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L4972-L4985) 明說申請人證明已買或租舊金山地塊後才獲准自費搬屋，又記 1907 年六月清場要求。`s53003` 的「住戶先得找到能安放它的地」保守轉述這個前置條件；匿名公園工人指向待搬小屋的插畫屬場景示意，沒有指定某戶真實搬運法。

[R L10997–11008](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L10997-L11008) 明說 680 個家庭中 70 戶買地。`s53110` 用「這批已訪家庭」接 `s53105` 的 680 份較完整紀錄，卡片保留 `70 / 680`，沒有外推到全體小屋。兩處新台詞都比 R7 少重述，但敘事效果仍交由全新盲讀者判定。

其餘來源與書面畫面已有 [R7 獨立 PASS](r7-source-independent.md)，R8 的 `brief.md`、`research.md` 沿用 R7 雜湊。新 `video.json` 127 句與 `claims.md` 127 列 ID、順序及文字一致；`lint --slug curio-s53 --json` 為 **0 errors／1 warning**。警告是 1908 年三個不同事件明確唸年份，為避免 1907／1908 混淆保留。開場估 40.90–50.40 秒，正文最快估 489.97 秒，仍待實際 TTS 時長。
