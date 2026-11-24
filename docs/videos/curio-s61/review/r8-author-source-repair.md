# S61 R8｜作者一詞史料修正交接

2026-10-22 UTC。**R8 是作者修訂，尚待本版獨立史料／書面畫面覆核及兩份全新正式雙盲；本收據不是審核票。** R7 [獨立史料／書面畫面覆核](r7-independent-source-visual.md) HOLD 僅 `s61031` 的「全城警報」；全部 96 個插圖提示及 7 張卡片通過該輪紙審。

Prince 固定全文 [L1963–1968](https://github.com/GITenberg/Catastrophe-and-Social-ChangeBased-Upon-a-Sociological-Study-of-the-Halifax-Disaster_37580/blob/befb706982ba1be631a52d4f686be301c2de7f34/37580.txt#L1963-L1968) 說消防員首爆後回應 *general alarm*，沒有給出地理覆蓋範圍。R8 在 `video.json` 的 `s61031`、由 CLI 再生的 `script.md`、逐句 `claims.md`、`research.md` P09 和任務現況敘述中，僅把「回應全城警報」改成「回應警報」。舊 R7 作者收據和差分保留原樣，作為 R7 當時版本的可逆記錄；本收據取代其過強用詞。其他旁白、畫面提示、卡片、章節、循環、來源固定版本及 [brief.md](../brief.md) 均未修改。

| 檔案 | R8 SHA-256 |
| --- | --- |
| `brief.md`（未改） | `ef67f56b4d384015edc9eeaea3640946ff0c4c9b778a2a587adb190c43004a65` |
| `research.md` | `4ccf2c0aae5aa5f3bb27ee56641f6092aa79bc6d2165d6cbfdecbb582a48ddba` |
| `video.json` | `47860fcf1347bc549dcabeb2630f5a9e63bbbcd7a40c629ceafb16570f96ccb5` |
| `script.md` | `00f9734108f68b0093a3c7791fe4b0974a376cb963cbc772c1ed92cc61c11b04` |
| `claims.md` | `1e632d8f0884ca20829b49cc443610633fca028c20cc521232f6dffb86ccc4d8` |
| [任務票](../../../../tasks/open/2026-10-22-source-and-draft-s61-halifax-second.md) | `290b00655a4c8ffbef5f9be91e8ab33df4c1bb061d3eb1c2495f188be87e708e` |
| [r8-author-delta.json](r8-author-delta.json) | `2fa82207d665d87c86f4e27f895c7f58ceb1be381edbf73a826ba1719e8cebef` |

[r8-author-delta.json](r8-author-delta.json) 保存六檔 R7→R8 逐塊舊／新行、零起算座標與 SHA，已驗證正向重放及反向還原；R7 基準六檔在 `/tmp/s61-r7-frozen/`。固定 Prince 原文仍為 GITenberg commit `befb706982ba1be631a52d4f686be301c2de7f34`，raw SHA-256 `97484e988437d13a4f5a72d5c2edbf1c594ea8dff4c5b239d8b17b7c62c29b52`。

`VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s61 --json`：**0 errors、0 warnings**；106 句、20 組 `loops`、96 幅插圖與 7 張資訊卡。機械比對 `video.json` 和 `claims.md` 旁白 103／103、插圖提示 96／96、卡片文字 7／7 均一致。按較快 325 字／分鐘，濃縮開場 48.23 秒、開場後至品牌片尾前正文 **486.20 秒（8 分 6.20 秒）**；250 字／分鐘，開場 59.53 秒、正文 603.53 秒。`npm run check:tasks` 驗證 2,094 份任務檔，既有跨任務與舊認領警告未改。

**下一步：**在這組新雜湊上請獨立來源／書面畫面審讀與兩名未看舊票的隔離讀者先取得正式 13 題，再各自盲讀並正式合併。沒有付費 TTS、圖片、音樂、評審、成片、上傳或實際 Studio 片尾連結。
