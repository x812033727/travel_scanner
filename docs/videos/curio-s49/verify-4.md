# S49 R4 作者單句修復凍結（待獨立覆核與新雙盲）

2026-10-20。依 [R3 獨立來源與書面畫面覆核](review/r3-source-independent.md) 的唯一來源 HOLD，窄修 `moon129`；該覆核報告 SHA-256 為 `47438b6e8bb77fa602924fa09322a7be4d854b9c9c934bef2486b9b1c3ccb671`。本頁是作者收據，不把 R3 書面畫面 PASS 或本次自檢寫成 R4 獨立 PASS。R2 正式雙盲 FAIL 亦保持原結論。

## 精確差分

`moon129` 原句「他明說，報紙摘句都取自那本一八五九年重印書。」把交叉比對結果說成 Jacoby 自己的直接宣告。R4 改為「把雅各比的各報引句逐一對照，也都能在重印書裡找到。」`claims.md` 同列 Jacoby J4178–4205 的各報引句和 Locke 名下重印本 L2092–2120 的相同摘句。J4178–4182 明說的是騙局正文引文來自稀有重印書、該書也收各報意見；R4 旁白只陳述這兩份固定文字逐句對照的結果。

`moon128` 的來源提問與 `moon130` 的原報頁面界線均未改，`moon129` 的書面畫面提示詞亦未改。`video.json` 只有這一句旁白異動；`claims.md` 只有此列旁白及錨點異動；`script.md` 由 CLI 重生。`brief.md`、`research.md`、影片說明欄固定連結、開場、其餘正文、`loops`、片頭片尾計畫和兩份固定來源均未改。未產生或呼叫任何媒體、網站或 Studio，也沒有提交 commit。

## 精確 SHA-256

| 輸入或交付檔 | SHA-256 |
| --- | --- |
| Locke 固定文字 `/tmp/s49-moon-hoax-62779.txt` | `3ca0bc9b6fc5c50b090d61bf2049e925d22dd1cdef2b443a282f7fdc5749e654` |
| Jacoby 固定文字 `/tmp/s49-jacoby-53396.txt` | `f5ab32e64e7ea3735ff90fb000ae8cc82dddea594e0de0c6be30b30f94485029` |
| `brief.md`（未改） | `48c3dc196b668c3ce3d58b4b3ffc26973262eb450587abfcc39d10d421057568` |
| `research.md`（未改） | `9476f53555e51da2471a72f75249e7e5fc8ed4ce3e30627578ce86cf4198c327` |
| `claims.md` | `8434bb5e2a25382d8a766759aa782ef529e0e891c44863f571bc58bc7a31d060` |
| `script.md` | `da1dca236ce6b26d4785177f018d945df76f4fd1e149b547b808b3408d6e350d` |
| `video.json` | `7c26a60db37f4e2cb866f2491a44e18dd5c458373f39677d4b350288a3578131` |
| 由本版 `video.json` 渲染的完整盲讀旁白文字 | `66a36ba46caddc16fe24ec5c8a0974947f8a9af5ed7333997b36ef23ac560f4e` |

`narrative_hash`：`f4600fdd2b712f00`；`script_hash`：`05f4220f329de5273dda8fc011a253235ae1699d7a0b4e7ed839dfc1ff261f10`。以上五份交付檔的 SHA 是新一輪查核與盲評的綁定版本；不得沿用 R3 的 PASS／HOLD 判定或 R2 的盲讀答案。

## 一致性與時間

- `VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs script --slug curio-s49` 已重生；`lint --slug curio-s49 --json` 為 **0 errors、0 warnings、135 lines**。逐句機械比對：132 個編號景與 `claims.md` 的旁白及 `shot` 提示詞完全一致；含片尾的 135 句與 `script.md` 逐字相同。`git diff --check` 通過。
- 文字保守估時按 325 spoken units／分：濃縮開場 **167 單位／30.8 秒**，正文 **2,642 單位／8 分 08 秒**，片尾旁白 59 單位。Lint 排景估時計 **13:45**，首個正式章節起於 **00:48**；兩者都不是 TTS 或成片實測。
- 保留 **11 組 `loops`**；132 個編號景為 **125 `shot`、7 `big`**，書面插圖占 **94.7%**。原版 5 秒片頭及 21 秒片尾仍是包裝計畫。

**下一關：**請另一位覆核者只針對 R4 `moon129` 的新措辭、雙來源錨點及相鄰 `moon128`／`moon130` 的語意銜接，按上表精確雜湊重核；再用此版本產新敘事 payload，交兩位全新隔離讀者回答固定 13 題。在新結論前不啟動 TTS 或圖片。
