# S51 R12｜主張錨點與當夜分鏡的作者限縮修補

2026-10-20 UTC。[R11 另一位工作者的獨立覆核](r11-source-independent.md)判六句口播史實 PASS，主張錨點 `cal099` 與書面畫面 `cal021` 各窄 HOLD。本 R12 只修該兩處、過時的企劃交接文字與說明欄製作狀態；**134 句旁白逐字未變**。本稿仍只是作者候選，不以作者自檢代替新版獨立覆核。

| 修訂 | 依據與界線 |
| --- | --- |
| `cal099` 主張欄的英國調查 G 直達範圍由 L3483–3491 擴至 [L3478–3491](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L3478-L3491)。 | L3479 說史都華是 `chief officer`，L3483–3491 說他四點接史東的班並聽到夜間火箭報告；口播「大副」與該主張各有直接錨點。 |
| `cal021` 的書面提示詞改為夜間 1912 年貨輪無線電室，唯一船長走入門口，朝桌上空白訊息紙走。 | [G L3338–3342](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L3338-L3342)明記船長去問無線電員 Evans。提示詞只畫一人一動作、無可讀文字、無可辨船長肖像；保留 `cute-mystery` 固定 look。 |
| `brief.md` 第一段與「後續」改成 R10→R12 的實際關卡；YouTube 說明欄刪去已過時的「獨立史料覆核及成片製作仍待完成」，仍標來源截至日期。 | R10 舊稿雙盲及政策 PASS、舊版音訊六旗標 HOLD；R11 口播史實 PASS、兩處窄 HOLD；R12 需新差分覆核與新讀者。說明欄保留三份固定史料及頻道連結。 |

| 內容檔 | R12 SHA-256 |
| --- | --- |
| `brief.md` | `bb05d19ee6b76dc6936fb1b7dcd6e87fc7fb53f8dd17a045a261e2332da7f323` |
| `research.md`（未變） | `039ca3ecc3f5099537e51e48d0f1788faf0bdf9c5d254f2ae64dd5ff89b56459` |
| `claims.md` | `8e98eb79a0c5e02ffcd7e42cf4a9a53616495e24d7e8be789092eb494d140191` |
| `script.md`（R11 起逐位元未變） | `b0aed4b7b269130a717b290386b32f095b55c8a94a444db27221b1d2bf7f2c8e` |
| `video.json` | `a1596b39b227cb34b63babe5fd1689d38f66475a3cda59e51c0676d0b4c87b3c` |

作者本地檢查：`claims.md`、`video.json` **134/134** 同 ID、同序、同文；`screenplay(doc)` 與 `script.md` 逐位元一致；**131/131** 正文 `shot` 提示詞非空、**16/16** 伏筆有序；`node tools/video/cli.mjs lint --slug curio-s51 --json` 為 **0 errors／0 warnings**，`git diff --check` 通過。最快 325 CPM 文字估時仍為開場 **36.37 秒**、正文 **8:38.60**，未當作新版實測音訊。

下一步由**另一位工作者**按上述五檔及固定英國調查原文核 R11→R12 差分；兩位全新讀者只讀未變的 R11/R12 `script.md` 做 13 題盲評。新版政策、網站劇本卡綁定和六句重錄／完整 134 句零旗標音檢仍未做；插畫、配樂、成片均 HOLD。
