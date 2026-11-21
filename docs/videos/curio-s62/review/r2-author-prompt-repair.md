# S62 R2｜插圖提示詞補強與作者交接

2026-10-22 UTC。R1 凍結稿見 [r1-author-freeze.md](r1-author-freeze.md)。**R2 仍是作者候選，獨立覆核尚未開始。** R1 的 110 張插圖描述已有不同的動作與道具，但不少缺少明確場所和光源；R2 讓畫師知道人物所在的空間、天空或室內的光從何處來，並把結尾不合時代的影片播放器／訂閱磚示意換成手中空白來源卡與觀測本。天文點數、日期、來源圖仍交由四張後製資訊卡，不讓插圖冒充精確星圖。

## 精確、可逆的變更

[r2-author-prompt-delta.json](r2-author-prompt-delta.json) 逐景列出 R1 與 R2 的 110 個完整 `data.prompt` 字串。產生後曾把 R2 這 110 個欄位還原為 R1 的值再做整份 JSON 比對，結果完全相同；其餘所有 `video.json` 欄位，包括 114 句旁白、13 組回收、來源、資訊卡與順序，都沒改。`claims.md` 的畫面提示欄同步更換；逐句旁白、來源行號與 `script.md` 未改。

| 檔案 | R1 SHA-256 | R2 SHA-256 |
| --- | --- | --- |
| `brief.md` | `408e8c7c32fc7d9fde8c1673c68a7ccbe6589db6ef0bedf4c35f8e5c3c016225` | 相同 |
| `research.md` | `45b936aa4c89a75914cbc40d06597838aa54e4fbe3f264127d8bade03655fe7c` | 相同 |
| `video.json` | `99498eb7a102528d26c0fe380ac27b981c34565a6f7f52a4e2669947855e3932` | `c892fdcc0b33b4c8b88b6aff42a0f75feee0970a14ee41c3ac09230f2e3bedaf` |
| `script.md` | `c2f48c96f63502846fc9c19223ac3bd04b85e87396e137153f1af207b48b2df9` | 相同 |
| `claims.md` | `55688b91c8dbc90e6e721ffb589b4015b65035a5b5b14d5ef6945c27a50852ec` | `ed731c603d600fe99f8e9f487df1804b35c9ea34bdbb6e71708a1930f571dea2` |
| `r2-author-prompt-delta.json` | — | `df6f04c1649bbc87a994ab8065e9bbef39ad9f173555f9c43c9ae9674fafa2e2` |

1610 年出版原書／1880 年 Carlos 英譯固定 raw SHA-256 仍是 `74fc9b817b64bc33415c6a44100c30f48952bc531d380682e5f4f1a26cc56fb5`。`script.md` 的 narrative hash 仍是 `c2bc39b577bae410`。

## R2 機械檢查與下一步

- `VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s62 --json`：**0 error、0 warning**。114 句、110 張唯一插圖、4 張工具卡、最長連續一張卡、13 組提問回收、7 章。
- 250 CPM：開場 46.8 秒、正文 10.126 分鐘；325 CPM：開場 37.8 秒、正文 8.209 分鐘。固定 5 秒動畫片頭接在濃縮開場後，固定 21 秒 `v4-endscreen` 的最後 16 秒才由 Studio 放可點元素，均不佔正文估算。
- 逐句對照已在 R1 核對 114／114，R2 更換的 110／110 個 prompt 也同步寫入逐句表；獨立史料與畫面覆核及兩位新讀者盲讀仍待執行。任何下一輪稿件改動須重新固定雜湊與受影響的檢查。
- 本輪沒有 TTS、付費插圖、配樂、渲染、上傳或可點影片連結。
