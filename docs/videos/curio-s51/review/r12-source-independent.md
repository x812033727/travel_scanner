# S51 R12｜主張錨點與當夜書面畫面的獨立差分覆核

2026-10-20 UTC。[R11 獨立覆核](r11-source-independent.md)留下的兩處窄 HOLD，對 [R12 作者凍結](r12-author-freeze.md)的精確五檔均已解除：**旁白史料 PASS、逐句主張 PASS、書面畫面 PASS**。這是書面審核，沒有替代新讀者敘事、政策、網站卡、實際音訊或生成圖像驗收。

| 檔案 | 獨立重算 SHA-256 |
| --- | --- |
| `brief.md` | `bb05d19ee6b76dc6936fb1b7dcd6e87fc7fb53f8dd17a045a261e2332da7f323` |
| `research.md` | `039ca3ecc3f5099537e51e48d0f1788faf0bdf9c5d254f2ae64dd5ff89b56459` |
| `claims.md` | `8e98eb79a0c5e02ffcd7e42cf4a9a53616495e24d7e8be789092eb494d140191` |
| `script.md` | `b0aed4b7b269130a717b290386b32f095b55c8a94a444db27221b1d2bf7f2c8e` |
| `video.json` | `a1596b39b227cb34b63babe5fd1689d38f66475a3cda59e51c0676d0b4c87b3c` |

**差分邊界：**`research.md` 和 `script.md` 位元組與 R11 相同。把 R12 `claims.md` 唯一的 `cal099` 來源格還原到 L3483–3491，重得 R11 claims SHA `ce27dbd797c995ca367316f67b4ca0136cb21988bc9c1b84a07be842012abf8f`。把 R12 `video.json` 的 `cal021` 提示詞與 YouTube 說明欄還原到 R11，重得 R11 video SHA `02205af4ef7b94393c57307fd25209054f96f1f6148d60b6d73df746b55f2556`。`brief.md` 對已過時的 R9 狀態和後續步驟各改一段；沒有其他劇情、景、聲線、伏筆或設定改動。

- **`cal099` 主張錨點 PASS：**固定英國調查 G L3479 寫 `chief officer (Mr. Stewart)`，L3483–3491 接著記 Stewart 四點接 Stone 的班、聽取其火箭回報。R12 直達 [G L3478–3491](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L3478-L3491)同時覆蓋「大副」職務與事件，並保留此為調查整理證詞的界線。
- **`cal021` 書面畫面 PASS：**固定 [G L3338–3342](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L3338-L3342)記船長約十一點到 Evans 房間詢問附近船隻。新提示詞只畫一位泛用船長在夜間走入貨輪無線電室，桌上是空白紙，與口播「船長於是去問無線電員」及前後夜景相合；沒有畫可辨 Lord 肖像、第二人對話或可讀電文。`cal099` 的 `one chief officer` 景仍與來源相合。真實 MiniMax 畫面尚未產生，這只是書面可行性。
- **交接／連結 PASS：**`brief.md` 清楚區分 R10 舊劇本的來源、雙盲與政策 PASS，R10 音訊六旗標 HOLD，以及 R11 修詞與 R12 差分仍待後續關卡；YouTube 說明欄已移除過時的「獨立史料覆核待完成」，仍說明卡通示意、固定史料與頻道來源。此處沒有假稱 R12 政策、音訊或成片通過。三條固定史料 URL 已於 R11 實測 HTTP 200，來源 URL 沒改。

獨立逐句解析得 `video.json` 134 句，其中正文 131 句與 `claims.md`、`script.md` ID／順序／文字相同，片尾三句另外相同；131 個正文 `shot` 有提示詞、16 組伏筆有序。CLI `lint --slug curio-s51 --json` 為 **0 errors、0 warnings**。本次 `narrative --json` 的 UTF-8 旁白字串 SHA 為 `21f60ba546c6d8339262b50ddcd748dbdd97020ea6ce8a891b6c8825a9bc72c3`，與已存 R11 盲讀 A 的同版字串 hash 完全一致；兩位 R11 新讀者若均綁同一劇本／旁白 hash，其判斷可沿用至 R12，不必因來源錨點和提示詞改動重新盲讀。正式合併、精確 R12 政策／網站重綁和只重錄六句後的完整 134 句零旗標音檢仍須完成，插圖、配樂與成片仍 HOLD。
