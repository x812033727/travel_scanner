# S46 R11｜單句片尾來源與書面畫面差分覆核

2026-10-20 UTC。**旁白來源 PASS、書面畫面 PASS**，限下列精確 R11 檔案。作者的[改稿紀錄](../verify-20.md)與本次覆核分開；R10 的[獨立原著／畫面全文審核](r10-source-independent.md)只涵蓋未改內容，不能代 R11 新句簽核。

| 檔案 | SHA-256 |
| --- | --- |
| `brief.md` | `464c142a08b419cb1f30c6235629de7714589476d19c3b83a9f26cd04586c8f7` |
| `research.md` | `605e33a88488746102c4658f73462a3c906ba1ec67b8e0b1040eee2ed6ec50c9` |
| `video.json` | `f59ec9508ce6f5d61f867e2d2a74c74166a3bde4282b4153c9b71f07469f752b` |
| `script.md` | `3cc22cc5b69a782a420a78396f715bc22670dddfda3cf3c7ddacaa352df7194a` |
| `claims.md` | `947e5afe656da6df441a4d053e895944342584d3c43c23caa729cbb0aba4d609` |

以已提交的 R10 `77eca448` 為基線，`git diff` 顯示 `video.json`、`script.md`、`claims.md` 僅 `bkw999c` 口播換字與劇本尾端版本碼變動；`brief.md`、`research.md`、119 句其他旁白、所有畫面提示詞、資料卡、縮圖、片尾 `data.cta` 都未改。R11 新句「原著固定版連結放在說明欄，方便核對她的記述」是**可查的內容承諾**：`video.json.youtube.description` 確實列出 1895 Blackwell 自傳的固定 GITenberg commit URL，也列頻道 URL；沒有憑此稱已取得學生決議或院長信的獨立原件。歷史內容及 1895 原著引段維持 R10 審查界線。

`video.json` 的 120 句 ID、順序與 `script.md`／`claims.md` 逐字對齊；`lint --slug curio-s46 --json` 是 **0 errors、1 warning**，warning 為片尾口播不直接說訂閱，畫面訂閱 CTA 仍在。片尾畫面內容與本句的固定連結承諾沒有矛盾，前段提示詞也未更動，所以書面畫面差分 PASS。此審核**不判定** Jev 對 R11 的政策分數，也不代表兩名新讀者、站台、配音或成片核准；R10 sponsored .34 的 FAIL 對 R11 失效，需重測。
