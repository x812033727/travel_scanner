# S57 R3｜作者敘事窄修交接

2026-10-20 UTC。依 [R2 正式雙盲合併的 9／13 HOLD](r2-merge/summary.md)修訂。這份紀錄與 [R2→R3 零上下文完整差異](r3-author-diff.patch)是作者交接，**不是獨立史料、盲讀或政策 PASS**。差異檔 SHA-256：`c9779b759a51c6bc51bca23e08165ddcb62fe78d6f63ecad498958c078b64bf5`。

| 創作檔 | R2 SHA-256 | R3 SHA-256 |
| --- | --- | --- |
| `research.md` | `9663d4a0ea66b1fef3c6e3a0550b8b08cf169a68b1736ad6005d6408ac2cd667` | `9663d4a0ea66b1fef3c6e3a0550b8b08cf169a68b1736ad6005d6408ac2cd667` |
| `brief.md` | `911eb30d15273aa3ab5a57795e28e5a9c3fb4a8fa60059f3f152dc3eb578765a` | `7a68ed10261086ba13dbf1a85a87932eb8ad8a81723874c6abeb0df8490fe657` |
| `claims.md` | `5f03685898d9b256e9d3eaf0d7534efe3eaf4b9393f3ad86e418787ad1bb27f9` | `0f7e8278ac3482b79bd9013d29c187940f99869794f1fe7c241071511459c262` |
| `video.json` | `53ee5cd8a93ff5474ffbccbde47379c9872303a4d09442a1f1d699fb8d25b4ff` | `698b29027e4b57523d62e7bda8210e5f2dfc5910a6a1b2507f156fdd3b6088a0` |
| `script.md` | `604a4f10dbd6ac5b8c7602939a40f58252307a82810bd70d6c2d8b2a63fd29da` | `afc30e64b439c4d3ea783ab6a47b57f63b8c73c34ece00e85b3a4b46281c71f7` |

## 逐項修正與史料界線

| R2 盲讀點 | R3 改動 | 來源／界線 |
| --- | --- | --- |
| `chapters_link`：`s57164` 問日記由誰帶走，章首 `s57165` 卻先談信。 | `s57163–s57164` 改為出發前寫信與「交出日記前先完成什麼？」；下一章 `s57165` 首句直接答「三月十三日完成給班奈特的信」。`loops` 的 `s57164` payoff 改為 `s57165`，史丹利帶日記仍在 `s57167`。 | [Waller 編刊日記 L5864–81](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L5864-L5881)：13 日兩份文字、14 日出發與託日記。 |
| `payoffs`：`s57134` 問為何失貨，來源不能判動機。 | 問題改為「能找回一包短少的布嗎？」；`s57137` 以「日記記」限定追問後有人拿出一包藏布。 | [L5812–18](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L5812-L5818) 是李文斯頓的記述與指控；畫面不指定責任者，不補演未見對話。 |
| `payoffs`：`s57170` 問兩人都吃不下的原因，未回答。 | `s57169` 問史丹利能否準時出發；`s57170` 只說史丹利自述「滿腹心事」吃不下，`s57171` 保留他觀察李文斯頓**似乎**沒胃口，`s57172` 回答原定五點卻拖到八點。 | [Stanley 節錄出版書 S14360–73](https://github.com/GITenberg/How-I-Found-Livingstone--13-Travels-adventures-and-discoveres-in-Central-Africa-including-an-a__5157/blob/41828f7623e5ba1b0db0a4c96630bda15bb0b66e/5157.txt#L14360-L14373)；不把史丹利對自己的心情套在李文斯頓身上。 |
| `no_recap`：`s57094` 重複 `s57092`「暫保判斷」。 | `s57094` 改為隔天擬訪盧辛加的下一個行動，畫面同步轉到前方村路。 | [L5317–32](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L5317-L5332) 是當日寫下的**次日計畫**，故口播用「打算」，不說已完成訪問。 |
| `no_detour`：`s57139–s57143` 連唸物資清單。 | `s57139–s57150` 改以援助到手 → 補過失貨 → 有續行工具 → 還缺人手 → 等史丹利從海岸送來為因果線；僅點出布、船、藥箱，移除珠、銅線、鍋、襯衫的逐項清單。第七章名改成動作「史丹利把貨交給他」。 | 援助與候人手 [L5796–5810](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L5796-L5810)，計畫水路 [L5769–77](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L5769-L5777)。船「是未完水路的工具」屬作者以兩段文字合讀的功能說明，非後來路線已完成的證據。 |

另按 B 票建議，`s57004` 改問日記主人的去向，不在濃縮開場直接說出結局；首章改名「五道封印」。這兩項在 R2 正式 OR 合併本來是 Yes，僅作窄幅品質修正。

**精確範圍：**`video.json` 只改 24 景 ID：`s57001`、`s57004`、`s57094`、`s57134`、`s57137`、`s57139–s57150`、`s57163–s57164`、`s57169–s57173`。其中 23 句口播改動、兩個章名改動、14 個鏡頭提示詞改動；頂層僅 `loops` 的一個 payoff 與說明改動。其餘 165 景不變。`claims.md` 僅對應 23 個口播 ID 改列，`research.md` 不變。逐字 old/new、來源連結和提示詞均保存在[完整差異](r3-author-diff.patch)。

## 機械檢查與下關

- `node tools/video/cli.mjs script --slug curio-s57` 已重產劇本；`node tools/video/cli.mjs lint --slug curio-s57 --json`：**0 errors、0 warnings**，189 句、估時 **14.58 分鐘**。濃縮開場 **45 秒**，其後正文 2,697 漢字，按每分鐘 325 字約 **8.30 分鐘**；168／189 插畫鏡頭（88.9%）、21 排版卡、12 個 `loops`。5 秒固定片頭、21 秒全域片尾、固定版本來源與頻道連結保留在 `brief.md`／`video.json`。
- `claims.md` **189／189** 與 `video.json` 逐字對齊；`npm run test:docs-videos`：**236 pass／0 fail**；`npm run check:tasks`：exit 0，僅既有無關任務板警告。
- 本稿須新版本獨立史料／書面畫面覆核、兩位無前情讀者各自盲讀及正式合併後，才進入政策與付費媒體關卡。**TTS、插圖、配樂皆未執行。**
