# A01 round16 起源章企劃對齊候選 — HOLD

此資料夾直接從已追蹤的 [round14](../A01-round14-source-bound-loop-candidate/README.md) 建立，沒有納入未追蹤的 round15 畫面提示詞候選，也沒有改動 round14。`delta.json` 只替換 `series.plan.chapters[origin].point` 的一段話，使企劃與既有旁白的「1928 年旅前發問 → 兒子製箱 → 拉箱出發 → 一家六口旅程」順序一致。六章 79 景／108 句、主張、loop、來源表、聲音與估計片長均未更動。

替換前的企劃說「片頭動畫後明確從 1928 年出發開始」，但既有第一句 `origin-r12-01/r12o01` 先引述安妮塔在旅前提出搬行李的問題，`origin-03/csdd`／`9ij6` 才講輪子與把手，`origin-01/zc7k` 之後才出發，`origin-01b/6b28` 才帶出一家六口。新企劃明確接回開場的提箱難題，沒有添加歷史事件、人物傳承或產圖細節。

`node build.mjs --write` 只在本資料夾產生六章、series、source map、validation 與 manifest；`node build.mjs --check` 重算並逐位元組比對。builder 先核 round14 manifest 與所有基底檔的 SHA-256，再要求唯一變更是 `origin.point` 的一個精確片語；完整 compose、lint 與 cute-story 畫面檢查另寫入 `validation.json`。`manifest.json` 釘選基底、delta、六章、series、來源表、驗證報告與旁白雜湊。

本候選 `manifest.json` SHA-256：`2f44419c43c64a2ea3762dd5d2053bb0febefcfd055f057e9c940c6c6d6249df`；`delta.json` SHA-256：`6ffc9a4f087009fc51bdcf20c5926db74db38ccdee4ee82552c7c208b00fc0ae`。基底 round14 manifest SHA-256：`9c2b6a69360c0f701fb28043e2e1179b6cda83c6e90a91253e14224b66245162`。`--check` 得 79 景／108 句、0 lint error、41 warning、0 cute-story error；250／300／320 units 每分鐘的正文估時計為 653.37／558.10／530.30 秒，這些都不是 TTS 實測。

本機另啟動 `npm run test:docs-videos`，Windows Node 測試工人持續約五分鐘未輸出測項結果；因本輪僅修正企劃文字，已中止這項可選的整套測試，**不能記為全綠**。`node --check build.mjs`、`build.mjs --write` 與 `--check` 均通過。

**HOLD：** 這是離線企劃文字對齊，不是正式機 A01 實稿、新一輪真實 verifier／listener／全片敘事審核、獨立整稿審查、`story/reviews/script-review.json`、TTS 實測或成片。round9 的 `chapters_link`／`payoffs`／`one_thread` 仍保留為歷史 FAIL；此候選不能宣布 PASS。後續仍要對精確整稿完成來源與敘事覆核，經真實主機流程讀回結果；不得憑本候選寫主機、啟動付費旁白／插畫／影片、匯入 B18 或後五集、上傳 YouTube。
