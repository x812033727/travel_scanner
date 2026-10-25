# C09 Patagonia｜站主核准 v8 逐鏡方向

現行正式逐鏡資料是 [visual-plan.json](visual-plan.json)，與[核准前凍結候選](reviews/visual-plan-v8-candidate-2235ea30.json)的原始位元組相同，SHA-256 `2235EA304C240E78F6473183E45A63502500EE20F931107843C6AF3C5AD0BF5A`。JSON 內的 `status: UNAPPROVED` 是凍結當時的文字；站主後續核准見[精確核准收據](reviews/owner-v8-approval-20261024.md)。

這版有 **77 句／77 鏡**：67 張 MiniMax `image-01` 匿名概念插圖方向、10 張後製字卡，連續字卡最多 2 張，`look` 精確為 `{ "preset": "cute-mystery" }`。每鏡 ID、旁白、提示詞和字卡內容以 JSON 為準。獨立[逐句來源與配鏡覆核](reviews/source-visual-v8-independent-20261024.md)為 77／77 PASS；文字預檢不等於生成圖驗收。

前一版 85 鏡的原文已[逐位元組保留](reviews/visual-plan-v5-85-historical.md)，SHA-256 `3BB7E74622BF10EA6E29983C0713857823C0E5F725ADDB07D6D294E292019636`，不能與目前 77 句 `script.md` 混用。

`video.json` 是由精確候選轉出的本機機器稿，僅額外加入四句配音念法，並把十張後製字卡的畫面標題／來源註記改成觀眾可讀文字；所有字卡數值、標籤、旁白及插圖方向不變。原始內部來源代碼仍保存在凍結 `visual-plan.json` 和來源查核檔。獨立重核這項字卡差異已通過。執行 `node docs/videos/story-everyday-patagonia-c09/preflight-v8.mjs` 可唯讀檢查來源與 77 鏡專案是否漂移。紙上正文 567.633 秒與插圖時間占比 88.073% 均未經實際配音或渲染驗證。系列保持 paused；站主已核准[整支本機試片 US$25 上限](reviews/owner-paid-pilot-approval-20261024.md)，但預算與工人防護仍未過關，不得啟動工人、付費生成、後台匯入、上傳或發布。
