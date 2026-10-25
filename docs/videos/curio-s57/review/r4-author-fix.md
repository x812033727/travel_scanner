# S57 R4｜作者窄修與凍結交接

2026-10-20 UTC。這是**作者候選稿**，不是獨立史料或敘事 PASS，也不是語音、插圖、配樂或成片放行。[R3 獨立來源覆核](r3-source-independent.md)因 1872 年 2 月補給事件倒序 HOLD；[R3 正式雙盲合併](r3-merge/summary.md)為 10／13 HOLD，兩票共同未過 `chapters_link`、`payoffs`、`no_recap`。本次只修這些斷點，並縮短 A 讀者指出的湖行岔題；完整逐行變更封存於 [R3→R4 差異](r4-author-diff.patch)。

| 檔案 | R3 SHA-256 | R4 凍結 SHA-256 |
| --- | --- | --- |
| `research.md` | `9663d4a0ea66b1fef3c6e3a0550b8b08cf169a68b1736ad6005d6408ac2cd667` | `9663d4a0ea66b1fef3c6e3a0550b8b08cf169a68b1736ad6005d6408ac2cd667` |
| `brief.md` | `7a68ed10261086ba13dbf1a85a87932eb8ad8a81723874c6abeb0df8490fe657` | `50b4f5f48f9ef82b18f25ff8f681014bd658cb45955101e109574658f34de139` |
| `claims.md` | `0f7e8278ac3482b79bd9013d29c187940f99869794f1fe7c241071511459c262` | `07c3d2ea5ea29d7d7ce68deb020c09b72a0dd424cfe548224a32039473e30b72` |
| `video.json` | `698b29027e4b57523d62e7bda8210e5f2dfc5910a6a1b2507f156fdd3b6088a0` | `bf2d6d429fca78f3a66620b114ee8333b4f91d2e37262a25d24fedac3ea1d4a8` |
| `script.md` | `afc30e64b439c4d3ea783ab6a47b57f63b8c73c34ece00e85b3a4b46281c71f7` | `a375377e0ced91d83be01650bb4e55fb6845de4e463d542302938d3de58fe6ce` |

差異檔 SHA-256：`3949fbc36b759db7bb0cb5857d8486726cfe54ff66ed76f8f13bf81fd2e7c134`。`research.md` 未更動；兩份來源固定版本與版本層級仍見該檔及 [R3 來源報告](r3-source-independent.md)。

## 修訂範圍

- **2 月時序及畫面：**`s57137` 只說追問時有人提到舊布的去處，畫面仍是待查的貨倉；`s57139` 明指 **18 日**史丹利新援助先到，[L5796–5804](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L5796-L5804)；`s57142` 明指 **19 日**收到藥箱與藥品，[L5806–5810](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L5806-L5810)；`s57143` 才明指 **20 日**有人拿出藏布，並在這句才畫已找回布包，[L5812–5818](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L5812-L5818)。`brief.md` 第七章與 `claims.md` 同步；`s57144` 用回顧語氣說布追回**前**已把新援助視為續行本錢。`s57138` 的問題由 `s57139` 作答；`s57134` 布包線由 `s57143` 作答。沒有推定誰偷取貨物。
- **章節銜接與可回答的提問：**`s57011` 直接把 1871 年晚秋的回溯接到開場「兩人分路」；`s57034` 刪去史料無從回答的「若援助沒到，能撐多久」，改由 `s57035–s57036` 揭示來者是蘇西；`s57089–s57091` 改問岸上說法隔天是否仍相同，以翌日相反觀察回收，沒有替水系下現代地理結論。
- **重複與岔題：**`s57067` 留史丹利出版對話中「還要六七個月」的**自估**，`s57072` 留身後編刊日記中的**續行決定**；`s57156` 留計畫，`s57157` 轉向史丹利去海岸的實際分路。刪除 `s57088,s57095,s57096,s57099,s57102,s57103` 六個低因果景及對應 claims；`s57098` 合併北行發燒與恢復，`s57101` 讓尚未解決的缺貨引向下一章。沒有把李文斯頓當時關於尼羅河源的信念改作已證實事實。

逐字更動的口播 ID（claims 同步）：`s57011,s57034,s57067,s57087,s57089,s57090,s57098,s57101,s57137,s57138,s57139,s57142,s57143,s57144,s57157`。另改 10 個書面插圖 prompt：`s57034,s57067,s57087,s57089,s57098,s57101,s57137,s57138,s57143,s57157`。`loops` 更新 `s57009`／`s57061` 的 payoff 指向 `s57072`，`s57138` 指向 `s57139`，新增 `s57134→s57143`。章名未改，`script.md` 由新版 `video.json` 重新產生。

## 驗證與後續關卡

- `node tools/video/cli.mjs lint --slug curio-s57 --json`：**0 errors／0 warnings**，183 句，估算 14.22 分鐘；口播與 claims **183／183 逐字一致**。正文漢字 2,632 個，按 325 字／分約 **8.10 分鐘**；保留 30–60 秒濃縮開場、第一章後 5 秒片頭、21 秒片尾卡與 13 條預告／回收線。163 個可愛懸疑畫面／183 景＝**89.1%**，另 20 張資訊卡。
- `npm run test:docs-videos`：**236 pass／0 fail**。`npm run check:tasks`：exit 0，僅既有無關舊任務提示。
- **待獨立重審：**R4 五檔需重新做來源／書面畫面覆核、兩位新讀者獨立盲讀與正式合併；R3 的 HOLD 或更早 PASS 均不自動適用。未執行付費語音、插圖、配樂，未聲稱任何人工核准。
