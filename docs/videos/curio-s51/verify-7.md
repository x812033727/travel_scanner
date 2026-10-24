# S51 R7｜兩組重述及事件章名的作者凍結

2026-10-20 UTC。R6 兩位全新隔離讀者的[正式合併裁決](review/r6-official-panel.md)為 **敘事 FAIL**：兩人共同指出 `cal105→cal106` 的啟航重述與 `cal034→cal060` 的漏收求救電文重述；B 另指出最後章名像結論。R7 是回應診斷的**作者候選**，不是新版獨立來源、畫面或敘事 PASS。R6 的來源／畫面差分原定覆核尚未完成，所以後續獨立審稿須涵蓋 **R5→R6→R7 全部差分**，不能只查本輪三處。

## R6 → R7 精確改動

| 位置 | R7 改動與史料界線 |
| --- | --- |
| `cal034` 與開場伏筆 | 刪除正文 `cal034`「後來鐵達尼號的求救電文，這間房沒有聽見。」及其一張夜間插畫；開場 `cal004` 的伏筆回收點由 `cal034` 改到 `cal060`。`cal033` 仍提出無人接班的疑問，讓故事沿船橋、燈光、火箭往前走，在真正發求救電文之後才給答案。 |
| `cal060` | 改為「沒有。還記得十一點半摘下的耳機嗎？求救電文來時，這裡沒人接收。」以具體耳機和時間點回呼 `cal004/032/033`，只在此處揭曉漏收求救電文。英國報告 G [L3340–3354](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L3340-L3354)記 Evans 十一點半休班，[L3182–3197](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L3182-L3197)記船方未收到求救訊號且唯一無線電員正在睡。`claims.md` 同步加 R03、R05 錨點；匿名空白信號紙插畫不變。 |
| `cal106` | 刪去緊接 `cal105` 重說的「加州人號此時才出發」，只留「夜裡那艘船早已不見；船名還能怎麼查？」作下一章的具體疑問。英國報告 G [L3484–3510](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L3484-L3510)記晨間另船、夜船燈影消失及約六點才得沉船消息；[L3525–3542](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L3525-L3542)記後來報告的船名歸納。日間無字海圖與船模型插畫提示詞不變。 |
| 末章章名 | 「距離沒定值，救援機會也無法回算」改為事件動作「調查對照船位與目測距離」。G [L3509–3550](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L3509-L3550)確實並列聲稱的船位、目測五英里及後來八至十英里估計；仍不把單一距離當定值。章內旁白、插畫與片尾「反事實救援人數無法回答」均未改。 |

`research.md`、其他 134 句與其書面提示詞、16 組伏筆的其他項目都未改。R6 的 135 景／137 句變為 R7 **134 景／136 句**，其中 **133 景正文 shot**；不以重述或留白補時。末章章名不算口播，重生劇本反映它。

| 內容檔 | R7 SHA-256 |
| --- | --- |
| `brief.md` | `5148d751b485260650d2d8661c5898ce0b85cec6284677527d271fa3384ace5a` |
| `research.md`（未改） | `039ca3ecc3f5099537e51e48d0f1788faf0bdf9c5d254f2ae64dd5ff89b56459` |
| `claims.md` | `ef7f985a542fd7ea52977b23477bf8464f4176bb1d6415efd71ce294996a48d0` |
| `script.md`（CLI 重生） | `76bb8c3669eab045363b4e726483085b0ef1cb3257e83268fa1a55196819517a` |
| `video.json` | `0efe5126f5f24edf08fdc75bf626b1000f0192e9e6a17d421b2d7dd871d4a081` |

作者本地核對：`claims.md` 與 `video.json` **136/136** 同 ID、同序、同字，CLI `screenplay(doc)` 與 `script.md` 逐位元相同；**133/133** 正文 `shot` 提示詞非空，伏筆 **16/16** 的 setup/payoff ID 存在且有序。`node tools/video/cli.mjs lint --slug curio-s51 --json` 為 **0 errors／0 warnings**；`git diff --check -- docs/videos/curio-s51` 通過。`estimateTimeline` 在 250／300／325 CPM 時首八景開場 **44.80／38.60／36.37 秒**，其後正文 **646.47／558.00／526.77 秒**；最快仍為 **8:46.77**。這些是文字估時，**不是 TTS 實長**。

**下一關：**另一位工作者按上表精確五檔和固定 G／B／A 原文核 R6 與 R7 的全部來源、逐句主張及書面畫面差分；兩名全新隔離讀者只讀 R7 劇本按固定 13 題盲評。政策、站台大綱／劇本、TTS、付費插畫、配樂、成片及上傳均未開始。
