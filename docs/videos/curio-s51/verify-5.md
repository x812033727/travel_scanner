# S51 R5｜調查報告日期與結尾回收的作者凍結

2026-10-20 UTC。R4 [獨立來源覆核](review/r4-source-independent.md)僅 `cal107` 時序窄 HOLD：英國調查 5 月 2 日已開庭，正式報告是 7 月 30 日。R4 兩位全新只讀劇本的[讀者 A](review/r4-fresh-panel-a.md)、[讀者 B](review/r4-fresh-panel-b.md)均因 `cal135` 的「回到開頭」與已說過的事件重述，判 `one_line`、`no_toc`、`no_recap` 為 No；A 亦判結尾 `payoffs` 為 No。R5 是回應這兩項的**作者候選**，不是獨立 PASS。

## 對 R4 的精確改動

| 位置 | R4 | R5 |
| --- | --- | --- |
| `cal107` 旁白 | 「幾個月後，英國正式調查逐一對照船橋證詞。」 | 「到了七月底，英國正式調查報告逐一對照船橋證詞。」 |
| `cal135` 旁白 | 「回到開頭：求救電文沒進來；白火箭的通報，也沒有讓加州人號起航。」 | 「史東說，船長要他繼續打摩斯，有新消息再派實習生來；當下沒有起航指示。」 |
| `cal136` 旁白 | 「還記得史東說船長叫他續打摩斯嗎？那能看見決策，不能證明船長當夜認出鐵達尼號。」 | 「還記得船長說自己只記得一枚嗎？兩份證詞對不上，仍不能證明他當夜認出鐵達尼號。」 |

`cal107` 的 `claims.md` 同列固定 [G L143–166](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L143-L166) 報告日期、[G L205–210](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L205-L210) 5 月開庭及研究 R11 的證詞對照。畫面由公開聽證桌改成**後來日間報告桌**，無字頁與無標記冊，不把 7 月報告畫成 5 月開庭。

`cal134→135` 現直接回答通報後的節點；`cal135` 增加前文未說的「有新消息再派實習生來」指示，僅歸於**史東證詞**，由固定 [G L3428–3435](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L3428-L3435) 支持；未起航另由研究 R13 的正式結論支持，不推論船長心態。`cal136` 用船長一枚與史東五枚的具體矛盾回呼，保留不能證明當夜辨認船名的界線。`cal135` 書面畫面用匿名日間桌上無字的通話管、訊號燈及信差剪影符號卡；`cal136` 原本的兩頁無字證詞示意未改。伏筆仍 16 組，僅 `cal008` 的回答點改至 `cal135`，並更新 `cal008`、`cal134` 的描述。企劃頂端同步 R5 待覆核狀態；`research.md`、固定 G/B/A 來源位元組與其他 135 景提示詞未改。

| 內容檔 | R5 SHA-256 |
| --- | --- |
| `brief.md` | `dc63da9f3e730abe8dcc07e76a44cae1cd62ff0c9e6f246a55d1b858cdd2be38` |
| `research.md`（未改） | `039ca3ecc3f5099537e51e48d0f1788faf0bdf9c5d254f2ae64dd5ff89b56459` |
| `claims.md` | `88f1611b379dd230564aa44938439f818f31de6d227b3667bdf6e65e48028cfa` |
| `script.md`（CLI 重生） | `dcebb60865b561b5b38b5bb163fdd18b9961dbb26e1676903f47167fc4abba8d` |
| `video.json` | `1e8feed428c617ced77d251a328f1b75ba8d498cf103e11bee51720a6ee59b22` |

本地核對：`claims.md` 與 JSON **140/140** 同 ID、同序、同文，CLI `screenplay(doc)` 與 `script.md` 逐位元相同；**138 景**中正文 **137/137** 個 `shot` 均有非空提示詞，片尾三句仍在。`node tools/video/cli.mjs lint --slug curio-s51 --json` 為 **0 errors／0 warnings**。`estimateTimeline` 在 250／300／325 CPM 時，首 8 景開場為 **44.80／38.60／36.37 秒**，其後 129 景正文為 **662.23／571.80／539.90 秒**；最快仍為 8:59.90，這不是 TTS 實長。5 秒原創片頭、21 秒共用片尾及最後 16 秒 Studio 兩個影片連結和訂閱圈仍按 `brief.md` 製作計畫，尚未合成或點測。

**下一關：**另一位工作者按本表**精確五檔 hash**獨立核 `cal107` 日期／畫面及 `cal135/136` 的證詞、畫面與主張差分；兩名真正隔離的新讀者只讀此版 `script.md` 按固定 13 題盲評。不得把作者自檢當成來源或敘事 PASS。站台大綱／劇本、TTS、付費插畫、配樂、成片和上傳均未完成。
