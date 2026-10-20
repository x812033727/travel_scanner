# S51 R9｜船橋值班重述的作者限縮刪修

2026-10-20 UTC。[R8 獨立來源、主張與書面畫面](review/r8-source-independent.md)對精確 R8 五檔判 PASS；兩位全新隔離讀者的[正式合併敘事裁決](review/r8-official-panel.md)卻共同判必答 `no_recap` No，均指出 `cal061` 重說 `cal015` 已交代的船橋有人值班。R9 是對該診斷的**作者候選**，不是新版獨立來源、畫面或敘事 PASS。

只刪 `cal061` 一句、一景和一列主張；沒有把相同資訊換句話重講。`cal060` 仍明確回呼十一點半摘下的耳機，說明無線電求救未接到；`cal062` 直接轉到鐵達尼號的白色求救火箭，`cal074` 才說加州人號值班員目見白光。英國調查 G [L3182–3197](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L3182-L3197)和 [L3420–3442](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L3420-L3442)仍分別錨住這兩層，沒有把調查推論寫成船長當夜親認船名。原 `cal061` 的瞭望鏡插畫提示詞隨景刪除。刪去一個非桌面景使畫面多樣性檢查的桌面占比越過三分之一，因此只把 `cal060` **後來日間**證據桌提示詞的 `desk` 改為同義 `table`；空白訊號紙和其餘書面場景不變。`brief.md` 首段同步記 R8 結果及 R9 待覆核狀態；`research.md`、旁白其餘 133 句、聲線、16 組伏筆和片尾均未改。沒有付費媒體或網站呼叫。

| 內容檔 | R9 SHA-256 |
| --- | --- |
| `brief.md` | `ad22f35f5d9ff6a17e055f27b4b6eaaf921f22856b15445531db5a4caf087837` |
| `research.md`（未改） | `039ca3ecc3f5099537e51e48d0f1788faf0bdf9c5d254f2ae64dd5ff89b56459` |
| `claims.md` | `640575ed6604e891accedb8d3febac8091c830f99d42e3740719975716e27f6b` |
| `script.md`（CLI 重生） | `5a874c0efa3e321a8d17a868d20ba2790128ffa79bc86cae3d8ba740c245ff80` |
| `video.json` | `4f2b24cfbc81e403c0f76c436cdfbb839d2a90affec72701b30701388e022777` |

作者本地檢查：`video.json` 的 134 句 ID 唯一，`claims.md` 與 JSON **134/134** 同 ID、同序、同文；CLI `screenplay(doc)` 與 `script.md` 逐位元一致；**131/131** 正文 `shot` 提示詞非空，**16/16** 伏筆 setup/payoff ID 仍存在且依序。`lint --slug curio-s51 --json` 回報 **0 errors／0 warnings**，`git diff --check` 通過。`estimateTimeline` 在 325 CPM 時，首八景開場 **36.37 秒**、其後正文至片尾前 **516.60 秒（8:36.60）**；是文字估時，**不是 TTS 實長**。本稿仍超過八分鐘最低線。

**下一關：**另一位工作者按上表精確五檔獨立核刪句及 `cal060` 書面畫面差分，兩名真正隔離的新讀者只讀 R9 `script.md` 做固定 13 題盲評。R8 來源 PASS、R9 作者自檢都不能代替新版合併敘事 PASS；政策、站台、TTS、插畫、配樂與成片尚未開始。
