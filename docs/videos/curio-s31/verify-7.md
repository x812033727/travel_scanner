# S31 R5a｜媒體前兩景提示詞修正（七）

2026-10-20。R5 的全新文稿盲讀回執 `/tmp/curio_s31_r5_fresh_blind_seal.md` 以 script SHA `332c875a835f89b428c124f578c380079976b9e35b396d098b086a56ba08cef2` 完成官方 13 題，**13/13 YES**。後續獨立來源／分鏡回執 `/tmp/curio_s31_r5_source_visual_audit.md` 重取四份固定全文，核對 97/97 逐句來源與 96/96 靜圖提示詞，沒有主張或對齊錯誤，留下 ly021、ly049 兩個非阻擋的畫面精度提醒。此回執驗的是 R5 video SHA `4a0d0bc19c5b2ebbf6982a58a6c1331b6527b6fca4d02a5230e15edeae74c754`；不把 R5a 的新 video hash 稱為已獨立核過。

## R5a exact hash

| 產物 | SHA-256 |
| --- | --- |
| script.md | `332c875a835f89b428c124f578c380079976b9e35b396d098b086a56ba08cef2`，與 R5 完全相同 |
| video.json | `930b04118fc8eaab69a904e986a5888322d0d942247535f1567e347bd0a4bf11` |
| claims.md | `83063009c6fec93840e0e6043118f7ed2df691b3e38651bc1590f12ad0ec2127`，與 R5 完全相同 |

只改 `video.json` 兩個仍圖 prompt：

- ly021：把單一回程騎者換成遠處數騎剪影，貼近杜牧「數騎漁陽探使回」，不添人名、站名或送荔枝的身分。
- ly049：移除音樂廳內有人接荔枝籃的交付畫面，只畫樂師放下樂器與無字曲卷；《新唐書·禮樂志》只把南方進荔枝與曲名聯在同一段，沒有記廳內交收。

本地核對：`VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s31` 為 0 errors、0 warnings；script、claims、video 的 97/97 ID 與字串仍相同，正文 96/96 為 still，10 條前向 loop 不變。全文仍估 9.3 分鐘、正文約 8 分 30 秒。R5a 尚待按**新 video SHA** 確認這兩景提示詞，再由製作門檻決定音訊；沒有製作配音、插圖、配樂或成片。
