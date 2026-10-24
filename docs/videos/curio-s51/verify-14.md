# S51 R14｜音訊查核 PASS；網站聆聽待審

2026-10-20 UTC。[R14 作者稿](review/r14-author-freeze.md)、[獨立史料與書面畫面](review/r14-source-independent.md)、[雙盲正式敘事 13/13](review/r14-official-panel.md)、[完整解說政策](review/r14-policy.md)均綁劇本 SHA-256 `d8d8a8c726a4849bb2320af9556a63b32e40f99076adc42f1833f481de2e8fbf`。本地大綱／劇本委派決定綁精確 SHA；站台 `review-pull` 仍顯示 `script: waiting for the owner`。

TTS dry run 顯示現稿 132 句中 **10 句須新合成**，其餘 **122 句沿用**既有合格語音快取；實際首輪付費 10 次／201 字。首輪 `check-audio` 現稿 132/132 有 `cal096` 一旗標（「他再次」被聽成「他再一次」）；只重錄這句一次，18 字。再驗全稿 **132/132、0 旗標**：116 逐字相合、13 同音／語助差異、3 由 Jev 判可接受。第二輪只需新轉錄 1 句，0 次 Jev 新呼叫。這是現稿全稿語音檢查，不沿用 R10 舊結論。`check.json` 還保留兩句已刪除的 R10 舊行 `cal082`／`cal087`，統計只計現稿 132 個 ID。

| 量測 | 結果 |
| --- | --- |
| `narration.wav` SHA-256 | `6ec4d04de19d0bb5863da639cde62e89e9176be5817df5f795e5cc77addbcc95` |
| `timeline.json` SHA-256 | `4d10fe3d81cca38382231511e87a0ec2c5fb4925bfaee60e3f0f93bacc0767eb` |
| `review/check.json` SHA-256 | `f0f58ea85ea0434ff5e2ee8e62b2cefe32c7ef15bc134fa4fe871544b5faede8` |
| 全旁白 | 719.97 秒／11:59.97，30 fps；`ffprobe` 719.966667 秒 |
| 開場濃縮 | 47.63 秒（`cal001`–`cal008`） |
| 正文 | **658.80 秒／10:58.80**（`cal009`–`cal136`），高於 8 分鐘下限 |
| 片尾旁白 | 13.53 秒；成片另用既定 21 秒 `v4-endscreen` 包裝 |

`review-push --gate audio` 已送到站台：CLI 明示此片非主機工人自動核准影片，回覆 **audio submitted for review (pending)**。網站人工聆聽／劇本卡批准仍待站主；沒有製作插圖、配樂或成片，也沒有 YouTube 發布。若修改劇本，這些精確雜湊關卡須重驗。
