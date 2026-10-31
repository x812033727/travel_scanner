# S51 R13｜史料、逐句主張與書面畫面獨立覆核

2026-10-20 UTC。對 [R13 作者凍結](r13-author-freeze.md)所列精確五檔重新計算雜湊，並獨立讀固定版英國 1912 年調查全文。判定：**史料 PASS、逐句主張 PASS、書面畫面 PASS**。本結果只涵蓋 R13 差分與檔案一致性，不代替兩位新讀者的敘事盲評、網站／政策核准、真實音訊或生成插畫驗收。

| 檔案 | 獨立 SHA-256 |
| --- | --- |
| `brief.md` | `8d81d79cc4afb75337109b61fe889064c78c122f59f1460fb8d192611d9d06d8` |
| `research.md` | `039ca3ecc3f5099537e51e48d0f1788faf0bdf9c5d254f2ae64dd5ff89b56459` |
| `claims.md` | `5ba86e4169c913ae65c3d746a7e0282d26c00c6fb1b0d29631efdbcbb929a8ae` |
| `script.md` | `d5678e54517e05d0e1ab2649931df359714e456aa1826c892d9b8d64d44cfc3a` |
| `video.json` | `62fd1d7c79bde69183d67b1dbcb0c4e0ba0cb714f750f17af65cf95ab8ef15b3` |

固定來源 [G，英國調查全文](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt)的本地原文 SHA-256 是 `5ac8c66266f84fb1fd01f50aab93044526c369df0d876c7e24dd20451f0053bd`，與 `research.md` 登記一致。G [L3420–3427](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L3420-L3427)寫吉布森約 00:20 先見遠船後甲板白色燈光；這是後續火箭前的目擊，不是火箭。新 `cal074` 的「更早些時候」、實習生、甲板白光均相符。提示詞只畫一名泛用年輕實習生在夜間船橋向遠船甲板燈看，無可讀文字、可辨人像或錯置的火箭。

G [L3427–3440](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L3427-L3440)記火箭、史東約 01:10 透過通話管報見五枚白火箭，以及他與吉布森的後續陳述。新 `cal075` 說史東見白火箭接連升空，並用問句接 `cal076` 的回報，來源支持、未把他的證詞升格成對船長記憶的證明。該景只畫無字證詞頁與匿名文書，沒有把火箭數、船距或具名人物畫成史實圖像。這是書面提示詞覆核，生成結果仍須看圖。

`cal082` 和 `cal087` 已從 `video.json`、`claims.md`、`script.md` 一起刪除；16 組伏筆沒有引用已刪 ID。`cal081` 保留吉布森摩斯燈未獲答，`cal083–086` 接新見三枚、證詞界線與告知船長的新動作；`cal088` 記他約 02:05 報八枚及摩斯無答，與 G [L3435–3465](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L3435-L3465)相符。刪句後沒有形成跨段錯接。兩句新 `cal074/075` 都與 `claims.md` 同字、有具體來源錨點。

獨立解析得 `video.json` 132 句（正文 `cal...` 129 句、片尾 `cal999a–c` 3 句）；129 句正文與 `claims.md` 逐句 ID／順序／文字一致，`script.md` 與 `screenplay(video.json)` 逐位元一致。129 張 `shot` 的提示詞均非空；`look.preset` 為 `cute-mystery`，來源與頻道 URL 在說明欄。CLI `lint --slug curio-s51 --json` 為 **0 errors／0 warnings**，`git diff --check` 通過。`brief.md` 明示 R13 尚需新盲讀、政策／站台與真實音訊；未宣稱已出片。

下一步：兩位未見作者與本覆核的讀者只讀固定 R13 劇本與 13 題，正式合併；若過關，再綁政策／網站劇本卡、合成必要的變動句並完整檢查 132 句音訊到零旗標。新版插畫、配樂、成片仍未放行。
