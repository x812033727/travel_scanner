# A01 round14 來源邊界與敘事回收候選 — HOLD

這是從 [round13](../A01-round13-loop-candidate/README.md) 產生的隔離離線候選。`build.mjs` 先用 round13 manifest 核對六章、series 與 source map 的 SHA-256，再依 [`delta.json`](delta.json) 改**兩句旁白、三筆 loop 和 series 企劃的四個精確片語**。其餘 106 句、79 鏡及四章 JSON 的內容沒有改；round13 和更早的檔案原樣保留。這不是已匯入正式機的稿件、審稿收據或影片。

| 問題 | round14 處理 | 來源界線 |
| --- | --- | --- |
| 片頭問「那只箱子後來去了哪裡」，原回收說「開場那只」進入館藏；這把 1928 年旅行示意箱與館藏物件當成已核實的同一件。 | `hook-07/y9b6` 改問那家人的自製輪子箱是否**有一只**留到今天；`origin-06/83ew` 回答館藏保存安妮塔的**一只**自製輪子箱。hook／origin 的 `y9b6` loop 和兩章企劃文字同步縮小指認範圍。 | [溫尼特卡歷史學會的館藏文章](https://www.winnetkahistory.org/gazette/before-her-time-anita-willets-burnhams-rolling-suitcase/)把物件 2005.26.576 標作「Anita Willets-Burnham’s 1927 suitcase」，並記述 1928–1930 年旅行使用自製輪子箱；文章**沒有明確說館藏品就是那次旅途中畫面所指的同一只**。[館方 2010 年藏品紀錄](https://www.winnetkahistory.org/gazette/from-the-curator-fall-2010/)也只確認家族捐藏包含安妮塔的輪子箱。口播不說 1927 是製作年，不把示意插畫當實物重建。 |
| `origin` 的 `6h2q` loop 把「四腳輪**和繩子**」標成在 `3zkh` 回收，但那句只說四腳輪；繩子在下一句。 | payoff 從 `3zkh` 移到緊接的 `idiy`，待四腳輪與繩子都講完才回收；起問與兩句旁白不改。企劃同步指明回收位置。 | [Sadow 接受 ABC News 訪談](https://abcnews.com/Travel/suitcase-wheels-turns-40-radical-idea-now-travel/story?id=11779469)分別記述機場輪板、四個腳輪與繩子；此輪不加新機械構造。 |
| 繼承的 origin 企劃寫「不寫丈夫意見、講學或 1933 遊記支線」，與已存在的 `origin-r12-01/02/03` 三句相反。 | 精確改為保留館方轉述的旅前發問、丈夫反應、旅後巡迴講旅行故事；不另展開 1933 年出書支線。三句正文不變。 | [溫尼特卡歷史學會的館藏文章](https://www.winnetkahistory.org/gazette/before-her-time-anita-willets-burnhams-rolling-suitcase/)提供這三段記述；它們仍須逐句獨立覆核。 |

來源核對日期：2026-10-16。Winnetka 文章由官方搜尋頁的完整索引文字讀取；站點直接開啟曾逾時，故物件與旅程的同一性更不能推定。ABC 訪談當日可直接讀取。

`node build.mjs --write` 只在本資料夾寫候選六章、series、source map、validation 和 manifest；`--check` 逐位元組重算。機械預覽：79 鏡／108 句、0 lint error、41 warnings、0 cute-story 規則錯誤。新改的 `hook-07` 靜圖約 10.7 秒，仍有畫面停留與節奏風險。正文文字估計在每分鐘 250／300／320 units 下分別是 653.4／558.1／530.3 秒；320 的結果仍低於 540 秒下限，250 的結果距 660 秒上限不到 7 秒。**這些不是 TTS 實測，也不能據此宣布片長合格。**

本機完整 `npm run test:docs-videos` 在 Node 24.13.0 下為 **283／284**：唯一失敗是未改動的 `imported-long-languages/runner.test.mjs` runtime 打包子程序在 Windows 以 `3221226505` 且無 stderr 結束；單獨重跑同檔仍是同一失敗。改用本機隨附的 Node 24.19.0 對**該一測試**重跑為 **1／1 PASS**。這組測試從第四個企劃片語修正前開始；修正後另有本候選的 `--write`／`--check` 和逐欄位差異檢查通過，不能把整套測試記為全綠。

兩句更動的 claim/source map 判定維持 `PENDING`／`PENDING_INDEPENDENT_REVIEW`。還需要另一位審查者對 round14 精確內容做史料、聽感和敘事覆核，重新跑正式 verifier/listener/panel，量 TTS，完成圖片與成片觀看。round9 的敘事 FAIL 仍是歷史結果；本地 lint 通過不能代替新 panel PASS。正式機 A01 的詞典鏈、寫入協調、媒體安全與預算關卡也仍須另行處理。本候選不授權主機寫入、付費工作、B18／後五集或 YouTube 上傳。
