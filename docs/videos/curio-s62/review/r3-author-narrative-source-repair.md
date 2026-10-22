# S62 R3｜作者合併退修與固定稿

2026-10-22 UTC。**作者候選，尚待 R3 獨立來源／畫面複核與兩位全新正式盲讀。** R2 的 [史料與畫面覆核](r2-independent-source-visual.md) 暫緩四處；兩份 [A](r2-isolated-blind-a.md)、[B](r2-script-diagnostic-b.md) 敘事診斷同為 10／13，均指出章界遠星問題沒有立即承接、可見點數反覆解說、鏡筒來歷偏長。A／B 因讀取邊界不算正式雙盲，本輪也不把它們當成核准。

## 這一輪修了什麼

- `s62006` 取消無來源的對焦旋鈕；`s62070` 用逐夜空白觀測頁取代不明制式鐘錶，同時刪去重複的可見點數總結；`s62091` 也撤掉未見於來源的沙漏。
- `s62106` 在 `claims.md` 把不存在的 G15 改為 G14，仍連 G14 的獻辭原文 L361–377。`s62112` 改成只承諾一份固定 1880 年 Carlos 英譯連結，`youtube.description` 和 `brief.md` 同步收窄；沒有新增未核實的 1610 年原文掃描連結。
- s62009–15 將荷蘭傳聞壓到必要的鏡筒來歷，餘下直說鏡中清晰度、近點可能黏合與角距測量。s62038 用開頭明確回接換邊事件。s62069–71、s62079、s62084、s62087、s62103 以原書下一次具體觀測或不同猜法，取代重複的概括句。
- s62089 留下「拿固定星相比」的問題；下一章 s62090 立刻拿木星東邊的固定星作參照，再講同夜可見數，s62093–96 以 11 角分的原書間距與隔夜整組靠近解答。新增的 1 月 16 日觀測已補進 G08 固定原文錨點 L1371–1398。

## 精確可逆差分與雜湊

[r3-author-structured-diff.json](r3-author-structured-diff.json) 列出 R2→R3 的 `video.json` **38 個完整 leaf before／after**，包括旁白、畫面、章名、loop 與說明欄；R2 雜湊 `c892fdcc0b33b4c8b88b6aff42a0f75feee0970a14ee41c3ac09230f2e3bedaf`，R3 雜湊 `396e78030054ee6f8a4dca15c83be8e4361dd6530bb1c8b99e75cdb3e2922ebf`。文檔及生成物的完整檔案雜湊如下；R2 可由上輪凍結稿或差分反向重建。

| 檔案 | R2 SHA-256 | R3 SHA-256 |
| --- | --- | --- |
| `brief.md` | `408e8c7c32fc7d9fde8c1673c68a7ccbe6589db6ef0bedf4c35f8e5c3c016225` | `3351f74d2d1df831f63eae41f3c243cc27e507f6d6853247178f056f349ea382` |
| `research.md` | `45b936aa4c89a75914cbc40d06597838aa54e4fbe3f264127d8bade03655fe7c` | `fc83424c3a0def641449cd17ad50b7d854412d70ad15de0afaf9fad30cd74795` |
| `video.json` | `c892fdcc0b33b4c8b88b6aff42a0f75feee0970a14ee41c3ac09230f2e3bedaf` | `396e78030054ee6f8a4dca15c83be8e4361dd6530bb1c8b99e75cdb3e2922ebf` |
| `script.md` | `c2f48c96f63502846fc9c19223ac3bd04b85e87396e137153f1af207b48b2df9` | `e8f1179f11184dea4eedabddc30f6820305e2c0ef709f061b26484961d622110` |
| `claims.md` | `ed731c603d600fe99f8e9f487df1804b35c9ea34bdbb6e71708a1930f571dea2` | `2f57e934e6f85febcd7aea7080d2c188141d7000cf40cd8c2c41d5dbf4cca550` |
| `r3-author-structured-diff.json` | — | `3d1416a2825aaf5bd84bb3551c6f29984edb5ddb0c5ff9b770cdc97822eb53ed` |

固定英譯原文 raw SHA-256 仍是 `74fc9b817b64bc33415c6a44100c30f48952bc531d380682e5f4f1a26cc56fb5`。`script.md` 由 `node tools/video/cli.mjs script --slug curio-s62` 重產，新的 narrative hash `fafdb295c59584bd`。

## 檢查與交接

`VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s62 --json` 為 **0 error、0 warning**。114 句、110 張不重複插圖提示、4 張資訊卡、最長連續 1 張卡、7 章、13 組提問回收；250 CPM 的濃縮開場 46.8 秒、正文 10.169 分鐘，325 CPM 正文 8.243 分鐘。片頭固定 5 秒放在濃縮開場後，片尾固定 21 秒且最後 16 秒才有 Studio 的真可點元素；兩段均未算入正文。

下一步是另一位來源／畫面覆核者重驗上述改動，兩位未接觸本輪討論的新讀者只看同一 R3 版劇本作正式敘事盲讀，然後才考慮站台選案／劇本及任何付費媒體。R3 沒有 TTS、插圖、配樂、渲染、上傳或真影片 ID。
