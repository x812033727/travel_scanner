# C05 R13：開場共圖候選

**未採用，待新來源／書面配鏡查核及兩位全新讀者；下一次實際 native panel 為 12。** 本資料夾沒有本候選的 verify、owner 核准、實聲或圖片。R12 parent、其 864 句八語、已存在的核准紀錄與 runtime 都保持原樣。

把 R12 的 `c07o04` 兩個問題拆成 `c07o04`（連雨的花）及 `c05h04b1`（點火後成分的位置）。其餘 107 句及既有場景順序完全不變；R12 的 1957 順序修正保留。第二預告的 loop 在 `c07u04` 第一個真答案回收，後面的 `c05le013` 保留 6–8mm／約250°C細節。

兩對中性概念圖與完整生成參數對照見 [image-reuse-plan.json](image-reuse-plan.json)：花籃／空竹簾不先畫供熱結果，燃端／相鄰未燃香體不先畫揮散箭頭、數字或成分流向。兩端同 prompt、camera、原生 composed prompt 及 1K／2K image key。本機只重算純函式，**沒有生成圖，沒有驗過實圖共用**。

正式執行先生成合格 payoff，再核 live cache 與真檔 SHA 存在，才調 teaser 命令；cache miss 必須停，避免 CLI 另派付費圖片。兩端仍各經原生 judge，最終包括裁切衍生檔的 manifest／實檔 SHA 都須相同；失敗不能用近似重畫或假 manifest 代替。

109句、107景、106插畫加1個outro、6章、36 loops；整份旁白仍為3041 spoken units。真實自然語速正文720–840秒仍未知。記憶體原生檢查0 errors、0 cadence warnings、最長估景10.6秒；23 warnings中16項是新候選兩行的八語過期／缺漏，另外7項軟提醒保留。這不改動現行R12翻譯，也不把864舊句當109行候選的當前翻譯批准。

[history/r12](history/r12/) 保存採用中的R12原件、來源／敘事收據、作者資訊與其檔案manifest；舊判定只屬原SHA。新增拆句使官方劇本SHA改變，不能沿用R12 pending review或BASE approved記錄。本候選通過新的來源、敘事及實際情境預檢後，仍需控制採用、精確新審核及拆句補譯；本作者未執行任何一項。

[`build-candidate.mjs`](build-candidate.mjs)只從固定R12 snapshot重建候選，讀取真實C05不可變字典於記憶體預檢，禁止改parent、runtime、媒體與批准。作者凍結SHA見[author-freeze-r13.json](author-freeze-r13.json)，逐物件差分見[revision-edits.json](revision-edits.json)。付費、供應商、後台、Git與媒體操作均0。
