# S55 R5｜隔離盲評官方合併

2026-10-20 UTC。兩位新讀者分別凍結 [A](r5-isolated-blind-a.md)、[B](r5-isolated-blind-b.md) 及各自的 [A JSON](r5-isolated-blind-a.json)、[B JSON](r5-isolated-blind-b.json)，均對應同一 `script.md` SHA-256 `323ed25718b4f20d1fa5dd8fa9311d7afe1810b5418e1615688528510c9fcd21`。原始判斷沒有修改。A 為 11 Yes／2 No，B 為 10 Yes／3 No。

本次使用 `panelVerdict` 和 **官方 `mergePanelVerdicts` 的任一讀者 Yes 即通過該題**規則。因此 `chapters_link` 雖由 B 判 No，A 的 Yes 使它在官方合併中為 Yes；B 的異議仍原樣保存在收據。兩人都判 No 的必答題只有 `no_recap`、`no_detour`。正式結果 **FAIL，11/13 Yes**。

| 官方題目 | A | B | 合併 |
| --- | --- | --- | --- |
| `scene_first` | Yes | Yes | **Yes** |
| `no_spoiler` | Yes | Yes | **Yes** |
| `one_line` | Yes | Yes | **Yes** |
| `no_toc` | Yes | Yes | **Yes** |
| `chapters_link` | Yes | No | **Yes** |
| `open_loops` | Yes | Yes | **Yes** |
| `payoffs` | Yes | Yes | **Yes** |
| `no_recap` | No | No | **No** |
| `chapters_are_events`（參考題） | Yes | Yes | **Yes** |
| `outro_no_next` | Yes | Yes | **Yes** |
| `opening_hooks` | Yes | Yes | **Yes** |
| `one_thread` | Yes | Yes | **Yes** |
| `no_detour` | No | No | **No** |

**編修依據：**A 指出 `s55064`／`s55066`／`s55069`／`s55075`／`s55085`／`s55089` 重說十月仍受繩束縛，且 `s55016` 已解答八月空球後，`s55017`–`s55039` 花過長時間走完製氣、群眾、落地及鄉民傳聞。B 指出 `s55050`–`s55053` 連續重述富蘭克林沒有目擊動物試驗，並認為 `s55134`–`s55137` 的熱氣／氫氣成本和未來比較打斷安全落地到信件日期謎題的進程。B 另認為 `s55063`→`s55064`、`s55114`→`s55115` 的章首只重述繩索或報乘員姓名，沒有立刻推進上章問題。R6 作者也會處理此少數異議，無須把官方合併結果誤寫成第三個 No。

## 可重算收據

兩份原始 JSON 的證據敘述有行號但非逐字引句，B 有三題只給整段敘述。為符合 CLI 的引句格式，[稽核檔](r5-isolated-merge-audit.json)保留原始檔 SHA、原判斷和正規化版本；正規化只用原判據中的第一個場景 ID 換成 R5 同 ID 的逐字旁白。B 的 `one_line`、`chapters_are_events`、`one_thread` 無場景 ID，分別補了代表性原文 `s55010`、`s55026`、`s55116`。**13 題 Yes／No 一項未改**；原判據仍以兩份原始 JSON 為準。

以 [合併答案](r5-isolated-merged-answers.json)執行：

`VIDEO_WORKDIR=/tmp/curio-s55-r5-isolated-merge node tools/video/cli.mjs narrative --slug curio-s55 --answers docs/videos/curio-s55/review/r5-isolated-merged-answers.json --json`

CLI 依必答 No 預期退出 **1**；[CLI verdict](r5-isolated-cli-verdict.json)與合併 13 題相符，[CLI receipt](r5-isolated-cli-receipt.json)是 round 1、`passed: false`、`failed: ["no_recap", "no_detour"]`，其 script check hash 為 `17953cf34cf5e80464acff39f4343e9bc2237a72a88bb4c9ab4e724b0eadf16b`、panel 規則 SHA-256 `5d71fef2cf3831dc33c0c32b2b297f633c47bfe41fbad18865ae08ed0c91cb75`、panel narration SHA-256 `64fad885a9bce9e07486cb04c9ce557d98b3d4473187c55e699fb275bdc06132`。

| 歸檔原件 | SHA-256 |
| --- | --- |
| A Markdown | `faa78d44694612bc92346b9fd368ecb92f04f6ac838615e7b9e83a594442a661` |
| A JSON | `31be23e7fb506eb3707ad3c83f1cb1c3dff375e60b840f4c7058166e3d98d1e0` |
| B Markdown | `4635dc777d4b27c82365dc7341a3058c06cc2cc484cad3d3f761bffcc56b1576` |
| B JSON | `4479a6fb238b384c228c38932d6eeea3def200b3ee8402ce0fbfdcde3d45b2d4` |
| Merge audit | `533691a606a984bfa3bc9c53dfa3465e47bca7e8b783a73c01c12607515f07da` |
| Merged answers | `b561c7c837f1f0224fbe61f1548d6af5c723c1243e4b5b9447ee0886132ad72c` |
| CLI verdict | `583beb242c1493d4d29074a3b6c46addabe4a761b60e8a78b7d58fb71a6d30fe` |
| CLI receipt | `0b1a6eb553586a68aafdd7479acc9989764ce91be50082d7075f427009a426d8` |

這份 R5 FAIL 不修改作者檔或媒體；修稿需新 SHA 與兩位新讀者獨立盲評。
