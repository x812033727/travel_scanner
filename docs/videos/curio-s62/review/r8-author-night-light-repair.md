# S62 R8｜一景夜間光線作者退修

2026-10-22 UTC。**R8 作者候選；獨立書面畫面重驗及兩位全新正式 13 題盲讀待辦，不可用於付費媒體。** [R7 獨立來源／畫面審查](r7-independent-source-visual.md)核對 **114／114** 句旁白及史料行錨通過，書面畫面 **109／110** 通過；唯一 HOLD 是 `s62065` 說一月十五日入夜而提示詞寫午後光線。固定 Carlos 英譯 [L1374–1378](https://github.com/GITenberg/The-Sidereal-Messenger-of-Galileo-Galilei--13-and-a-Part-of-the-Preface-to-Kepler-s-Dioptrics__46036/blob/6672b6c62a0f30e9bb9b84410ef48c6698c37ea5/46036-0.txt#L1374-L1378)明載當晚第三時辰、四點皆在木星西側。

## 唯一畫面修訂

`s62065` 的 `data.prompt` 將 `overcast afternoon light across his hands` 換成 `soft candlelight on his hands, dark winter night beyond the window`。畫面仍是無字筆記本與窗外四個淡光點的原創示意；燭光只作符合時段的場景光源，不宣稱有當年現場影像或伽利略實際持燭的證據。`claims.md` 同一列畫面欄逐字同步。其餘 **109** 個提示詞、4 張卡、114 句旁白、來源錨點、排序、loops、旁白設定與說明欄均逐位元未改。

## 可逆差分與綁定雜湊

[R7→R8 結構化 JSON 差分](r8-author-structured-diff.json)只有 `scenes[64].data.prompt` **1 個** leaf before／after；正向逐葉重播與反向還原精確得到兩版完整 `video.json`。[JSON 封裝的文字 unified diff](r8-author-text-diff.json)只修改 `claims.md` 的 `s62065` 畫面欄；取出 `patch` 欄後 `git apply -R --check` 通過。

| 檔案 | R7 SHA-256 | R8 SHA-256 |
| --- | --- | --- |
| `brief.md` | `5941ebf974ad67a9926d0b56311389fd8f820d14d47f31b3e55f1b1eb31b3021` | `5941ebf974ad67a9926d0b56311389fd8f820d14d47f31b3e55f1b1eb31b3021` |
| `research.md` | `7322d7269bfaba82a78cfde904fc94a65915e01dc3e0307a9e2ed6f0e92b62cb` | `7322d7269bfaba82a78cfde904fc94a65915e01dc3e0307a9e2ed6f0e92b62cb` |
| `video.json` | `1c811dfb9561248e314f0a39a3510386a6188322521f2d1e6c403e03ab81de95` | `c9f249ab7210fa4fb2cf2ac5206c57735ee19efcf0e846414bcfc06bb0745ace` |
| `script.md` | `c638b0d28cfbf6b398cd3bb541160685403bf3936fcd1613bc958921623e4326` | `c638b0d28cfbf6b398cd3bb541160685403bf3936fcd1613bc958921623e4326` |
| `claims.md` | `8cac2b796808afc29fe600c758d84a046342c7a89e7520fc4dfa512b5477f5e3` | `50f4b272576e90e3a172fd996fc27995223cd32cf0163264308109e6a3833c73` |
| `r8-author-structured-diff.json` | — | `3c1c086fcd393d4591302dee1a5ff9f68ae4af182c4064276b3278678e4167ba` |
| `r8-author-text-diff.json` | — | `c385b5f8353289a02088a2427614c5f7cd518c7f08c53a99ebaec41bf678ea40` |

固定 Carlos 英譯 raw SHA-256 仍為 `74fc9b817b64bc33415c6a44100c30f48952bc531d380682e5f4f1a26cc56fb5`。`script.md` 和 `narrative_hash` **`edc7d2005d74f93c`**、`speech_hash` **`5611a33a9a3fd52a`**完全不變，因此 250 CPM 開場 **46.53 秒**、正文 **10.181 分鐘**，325 CPM 開場 **37.63 秒**、正文 **8.254 分鐘**的文字估算不變。

官方 `lint --slug curio-s62 --json`：**0 error、0 warning**；114／114 旁白與逐句主張同字、每句有固定行錨，110 張插圖提示互不重複，4 張資訊卡最多連續一張。沒有虛構影片 ID、TTS、插圖、配樂、渲染、上傳或付款。請另一位獨立畫面審查者重驗 `s62065`，並以凍結 R8 檔案交兩位全新敘事盲讀者；R7 的史料審核與本作者修改不合併成 R8 的正式 PASS。
