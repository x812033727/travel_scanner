# S61 R9｜作者重述與避寒設問窄修交接

2026-10-22 UTC。**R9 是作者候選，尚待本版獨立史料／書面畫面覆核與兩份全新正式雙盲；本收據不是審核票。** R8 [獨立史料／畫面](r8-independent-source-visual.md) PASS；[正式雙盲 OR](r8-formal-merge-audit.md) 12／13 HOLD，共同 No 僅 `no_recap`：`s61123` 已講消防員知道瓦礫下有人受困，`s61059` 又說同一件事。這次沒有付費媒體。

## R8→R9 改動

- `s61123` 改為 Prince 固定全文 L924–930 描述的北面深紅天空與轟鳴火勢，讓這一鏡從首爆後的街道破壞推進至北區火勢；既有紅色天空與多處遠火的畫面提示詞逐項仍對應旁白。`s61059` 保留在第二次警報段，作為首次說明消防員知道瓦礫下有傷者、因而需要在火場接續工作的具體處境；不再與前段重複。
- `s61113` 保留老人及病弱者在寒風裡趕路的處境，但把問題改為「公地上的人，接下來能在哪裡暫避寒風？」；`s61081` 白帳與 `s61149` 整理出的教堂大廳回答可用處所。Prince L2051–2069 沒有記下每位老人或病弱者進了哪一頂帳棚，旁白不作這種分配主張。原來匿名年長者由成人扶著走向公地的畫面仍與前半句吻合。
- 單一讀者對 `s61015` 的伊莫號比利時救濟船前職提出岔線意見，正式 OR 的 `no_detour` 已通過。這筆歷史在 Prince L829–841 有據，直接刪除會耗掉 325 字／分鐘八分鐘門檻幾乎全部餘裕；與前後狹口、貨物句換寫又容易重述，因此 R9 不改該句，交由全新讀者判斷。
- 其餘 104 句旁白、96 個插圖提示、7 張資訊卡、20 組 `loops`、Prince 歸因與固定史料版本不變。

## 固定檔案與可逆差異

| 檔案 | R9 SHA-256 |
| --- | --- |
| `brief.md` | `75205d400dc05994097133ee45800161f816949e8d5658048909a2b8191a91f6` |
| `research.md` | `8fc6c82f22c352e5e4d336b2704eda9a9419dccf2896dbd970c5d16ffcaefdcf` |
| `video.json` | `005cc35734535c8a01ee46f7ee5dc1a3555d3b543d0fc3b42c0beda2812d97ce` |
| `script.md` | `e3f27c9da2b951fd744e9de48b2c64d665ef4f76cd6abaa4e323b43c5ebb9eb9` |
| `claims.md` | `37eb7bf2a039692d583e15b1e2e2aab477096ba47ee526fe8876a26e995df11c` |
| [任務票](../../../../tasks/open/2026-10-22-source-and-draft-s61-halifax-second.md) | `72c65406eb82552b0f4ec3bd7fadec7fc12fb12e6cbe7a4bb140cad5203626e9` |
| [r9-author-delta.json](r9-author-delta.json) | `d8de5784ea82872d1ac128a7f0400c7520c099eb7a42893d4bb94a83a05495e9` |

[r9-author-delta.json](r9-author-delta.json) 保存六檔 R8 PR 固定版至 R9 的逐塊舊／新行、零起算座標與 SHA，已驗證正向重放及反向還原。R8 基準為 `/tmp/s61-r8-pr-frozen/`；其中任務票已含根工作者補記的 R8 獨立及正式雙盲結果，SHA `906baac343188a0d9fc4e68e3e8403d9bae0719a709347aff55fc77d6e9b8472`。固定 Prince 原文仍為 GITenberg commit `befb706982ba1be631a52d4f686be301c2de7f34`、raw SHA-256 `97484e988437d13a4f5a72d5c2edbf1c594ea8dff4c5b239d8b17b7c62c29b52`。

## 作者機械檢查

重新產生 `script.md`，narrative 標記 `905b9da092703d23`。`VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s61 --json` 為 **0 errors、0 warnings**；106 句（含 3 句品牌片尾）、六章、20 組 `loops`、96 幅插圖與 7 張資訊卡。逐字比對 `video.json` 與 `claims.md` 的 103／103 個非片尾旁白，96／96 個插圖提示及 7／7 卡文字相同。以 325 字／分鐘，濃縮開場 **48.23 秒**，開場後至品牌片尾前正文 **487.13 秒（8 分 7.13 秒）**；以 250 字／分鐘，開場 59.53 秒、正文 604.73 秒。`npm run check:tasks` 驗證 2,094 份任務檔；舊認領與跨任務警告未改。

**下一步：**以本版固定雜湊請全新獨立工作者重核史料與書面畫面；兩名未看舊票的隔離讀者先取得同一正式 13 題，再盲讀並正式合併。沒有 TTS、原生圖、音樂、成片、上傳或實際 Studio 片尾連結。
