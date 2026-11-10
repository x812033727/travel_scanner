# S61 R4｜作者敘事修訂交接

2026-10-22 UTC。**R4 是作者候選，待另一名工作者重查史料與書面畫面，並待兩名新讀者各自盲讀；本收據不是放行。** R3 史料與書面畫面獨立審查曾 PASS；[R3 正式雙盲合併](r3-formal-merged-narrative.json)為 11／13、HOLD，兩名讀者共同否決 `chapters_link` 和 `no_recap`，B 另否決 `no_toc`、`one_thread`、`no_detour`。本次只修這些具體敘事問題，沒有進入付費媒體製作。

## R3→R4 改動

- 預告開場結尾由一艘法國船駛入狹口，第二章首句立即讓伊莫號從港內迎面開出；各章首句接續上一章未解的船火、火藥庫威脅、砲兵隊行動、分區搜救及第二聲結果。章名均為正在發生的事件。開場 56.6 秒，第一章後接 5 秒頻道動畫，片尾維持 21 秒動畫及最後 16 秒 Studio 可點連結預留。
- 船隻碰撞到首爆只交代一次約二十分鐘；首爆對街區的損壞與當時未充分示警，接到第二次警報時街上傳警與移往公地的反應。以 Prince 有明文支持的船隻被推往碼頭、電線桿折斷、鐵片穿屋頂等事實推進首爆後果，沒有用一組抽象清單代替行動。
- 消防正副長罹難後由市政官員接手指揮，其他消防員在第二警報中仍留守；砲兵隊自願灌水海軍造船廠內的火藥庫。只稱「一支砲兵隊」，不指定其軍種隸屬、不虛構命令、火距或供水細節。Prince 對未再爆炸的歸因留到最後明說，避免先講結局再講一次。
- 警報解除後的段落縮成搜救者先找家人、同處重找、約五小時後分區並記錄的具體變化，緊接公地的人在白帳、教堂或住家獲得暫住。刪去 R3 的電報、鐵路及較長收容支線，留下第二次警報對街上人群與救援的直接後果。刪去 R3 章縫重述及警報結果的重複句。20 組 `loops` 重新指向實際設問與新答案。
- `claims.md` 按 96 句更新；新增損壞細節錨到 Prince 固定全文 L940–948。`research.md` P04 增列同一錨點的可說範圍。84 個原創 `cute-mystery` 插圖提示逐一與旁白對齊，不畫可讀的原始警報、官方地圖或可識別個案。

## 固定檔案與可逆差異

| 檔案 | R4 SHA-256 |
| --- | --- |
| `brief.md` | `a81dcaa8a7feb3f2a75259bda56ed729480f7e27bd9487e4128d8791133df0ef` |
| `research.md` | `e3799cf194fce4c554821f62af1df4b2f7d692ff82fbede8ab8abb88c7d89646` |
| `video.json` | `9a76f8880c75a04ef1322ac7264323ffb92b7dd8e648a1ffa992212f4c7d72a6` |
| `script.md` | `c677b03f9c45c8f4d3d788d73381253e4bb574cb9e420c136b8761cbb9658650` |
| `claims.md` | `cf2b078766c170b3f5bb214b40a6109915745f7c53c173b87520aa42a4d9ab25` |
| [任務票](../../../../tasks/open/2026-10-22-source-and-draft-s61-halifax-second.md) | `d7c39b772363482cac9bb7592c56debda8fa6685c2d2ea8964aa2053a805e38d` |
| [r4-author-delta.json](r4-author-delta.json) | `1f61ed01e838f5d664864a444f502e8cec46546e44542fd2ea7b8593faa2aff2` |

`r4-author-delta.json` 記六檔逐塊的舊／新行、座標和 SHA；已從固定 R3 版正向重放到上表 R4，亦從 R4 逆向還原 R3。Prince 固定全文仍是 GITenberg commit `befb706982ba1be631a52d4f686be301c2de7f34`，raw SHA-256 `97484e988437d13a4f5a72d5c2edbf1c594ea8dff4c5b239d8b17b7c62c29b52`。再生劇本標記 narrative `4c030902579953d3`、speech `7b10b0174719e61d`。

## 作者機械檢查

`VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s61 --json`：**0 errors、0 warnings**；96 句、七章、20 組設問、84 個插圖鏡頭、9 張資訊卡。工具估全片 9.3772 分鐘；濃縮開場 56.6 秒，開場後至片尾前正文 488.97 秒，超過 8 分鐘。逐字核對 96／96 句的 `video.json`、`script.md`、`claims.md`，以及 84／84 個不重覆插圖提示詞與證據表。`npm run check:tasks` 通過 2,417 件任務檔驗證；其他任務既有逾時／範圍警告未改。Prince raw SHA 重查一致。

**下一步：**獨立史料／書面畫面覆核和兩名新讀者的盲讀，再由非作者正式合併。沒有 TTS、插圖、音樂、音檢、成片、上傳或實際 Studio 連結。
