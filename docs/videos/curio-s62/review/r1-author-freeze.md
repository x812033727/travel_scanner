# S62 R1｜作者候選與固定稿

2026-10-22 UTC。**作者候選，尚待獨立史料、敘事、畫面覆核及站台核准。** 題目為 1610 年伽利略逐夜觀察木星旁小光點，解釋為何有時數到三個、有時兩個、有時四個。S01–S61 brief、題庫與現有任務未見同題；S52 只在 1769 年庫克觀測金星凌日時提木星衛星食作計時背景。

## 固定來源與稿件

主要來源為 Galileo，*Sidereus Nuncius*（1610），Edward Stafford Carlos 1880 年英譯帶註版本；GITenberg commit `6672b6c62a0f30e9bb9b84410ef48c6698c37ea5`，raw `46036-0.txt` SHA-256 `74fc9b817b64bc33415c6a44100c30f48952bc531d380682e5f4f1a26cc56fb5`。逐夜錨點、譯者註解界線及目前證據不足的地方見 [research.md](../research.md)。這是 1610 年作者公開出版的敘述，不是當夜原始手稿或獨立複測；片中把 1 月 10 日「可能被木星遮住」及 1 月 23 日的相似說法留作他的猜測。

| 檔案 | SHA-256 |
| --- | --- |
| `brief.md` | `408e8c7c32fc7d9fde8c1673c68a7ccbe6589db6ef0bedf4c35f8e5c3c016225` |
| `research.md` | `45b936aa4c89a75914cbc40d06597838aa54e4fbe3f264127d8bade03655fe7c` |
| `video.json` | `99498eb7a102528d26c0fe380ac27b981c34565a6f7f52a4e2669947855e3932` |
| `script.md` | `c2f48c96f63502846fc9c19223ac3bd04b85e87396e137153f1af207b48b2df9` |
| `claims.md` | `55688b91c8dbc90e6e721ffb589b4015b65035a5b5b14d5ef6945c27a50852ec` |

`script.md` 由 `node tools/video/cli.mjs script --slug curio-s62` 生成，narrative hash `c2bc39b577bae410`。七章、114 句、13 組提問回收；110 張原創插圖的 prompt 彼此不同，另有 4 張後製資訊卡，插圖占 96.49%，資訊卡最多連續一張。第一章濃縮開場估 46.8 秒；在 250 CPM 估算下正文 10.126 分鐘，在較快的 325 CPM 估算下正文仍有 8.209 分鐘。實際時長待合成後量測；這些估算均不含 5 秒品牌片頭與 21 秒品牌片尾。

作者機械核對：114／114 句與逐句主張表完全相同，110／110 個 shot prompt 與逐句表完全相同，4／4 張資訊卡標題相同，每句有固定來源行號連結。`VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s62 --json` 為 **0 error、0 warning**。`npm run check:tasks` 驗證 2,417 件任務檔案後 exit 0，輸出的逾時認領及其他路徑交疊警告與 S62 無關；`git diff --check` exit 0。

## 交接與尚待完成的關卡

- 由另一位工作者逐句核對固定原書／英譯、114 句斷言、110 張插圖提示及 4 張卡。尤其要檢查 1880 年譯者的 `satellite` 腳註沒有被冒作 1610 年作者的原話，以及插圖沒有冒充精確觀測星圖。
- 兩位新讀者盲讀同一雜湊版本並走正式敘事合併檢查。任何稿件修改都要重做此雜湊清單與受影響的審核。
- 站台選案和劇本核准後才合成語音；插圖先由定稿張數及 dry-run 報價決定整集上限。長片通過後才做 Short、私人上傳、真實影片 ID、Studio 可點元素和連結。
- 預定 30–60 秒開場後插入固定 5 秒動畫片頭；固定 21 秒 `v4-endscreen` 片尾的最後 16 秒留兩個推薦影片元素及訂閱元素。這份候選沒有語音、插圖、配樂、成片、上傳或付費媒體呼叫。
