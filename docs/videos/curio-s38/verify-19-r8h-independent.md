# S38 R8h｜`pf004` 最後一次試畫前的獨立紙上覆核

2026-10-21 00:24 UTC。**PASS：只限 R8h 單景提示詞差分及史料／畫面規格；原生圖、整體分鏡與成片仍 HOLD。**我沒有撰寫 R8h 提示詞，亦沒有以本收據替站主審核網站卡片。

## 精確版本與差分

五份創作檔 SHA-256：`brief.md` `fa297d70e016d88ba1a59bd92476be22eda3eefc09f36b2d08c0c82ab114643b`，`research.md` `f838518cf2c4ab23de91021ae6024d9431f907866c14301466ca0a06bb3ecdfe`，`claims.md` `f9de8d2771b62cc327f4e599f002af8f3278cfb0f39dbed201e7fdc857201d42`，`script.md` `e59ec137e3de3871e3b0e5063d8f6504d3eb2adb5fe22265eb3faa3d613d5951`，`video.json` **`7e9eb1a2019bbf55727ac08c1bf273fc2fbf420223c6425083558afbfb9b0631`**。新 `visualHash` 為 **`1f353c19c4d07f47`**；lint 實測 0 error／0 warning。

我自行從 Git `HEAD` 取出 R8e `video.json`，解析與目前 R8h 比對，差分恰為 `pf004/005/006` 三個 `data.prompt`。`pf005/006` 的現值逐字等於 [R8f 結構化差分](verify-15-r8f-structured-diff.json)；`pf004` 依 [R8f→R8g](verify-17-r8g-structured-diff.json)與 [R8g→R8h](verify-18-r8h-structured-diff.json)兩筆差分逐字銜接，其餘解析後 JSON 完全相同。R8h 只把未試畫的 R8g `middle-aged`、短鬍及髮線說法換成「三十多歲的成年住戶、成熟面部」，沒有改敘事、來源、其他鏡頭、`look: cute-mystery`、風格／負面提示詞或品牌設定。R8g 並未購圖；前一張判退原圖屬 R8f。

## 紙上判定與原生 KEEP 界線

[D4b](research.md)記 1666 年 9 月 4 日佩皮斯在花園憂心辦公室及看火；[D5](research.md)到次日才確認住家與辦公室尚存。對「火最後有沒有燒到他的房子？」這句開場疑問，以一名成年住戶在花園指向**遠處**火光、屋子當下完整作概念景，與時序相容。佩皮斯當年 33 歲；「in his thirties」比 R8g 的 `middle-aged` 準確，也不把未經日記證實的鬍鬚或髮線畫成他的外貌。單一人物、單一指向動作、全身小人物及廣角景都符合系列單景規格；沒有往 prompt 塞畫風口令。

紙上 PASS 不證明花園有圍牆、磚屋與花園確切相對位置、天氣、服裝或真人相貌。下一張 1280×720 原生圖必須明顯是**成年人物**和完整寬景，火在屋頂**遠方**，沒有近景院內起火、近代住宅、童貌或攝影式柔焦。機器分數不能蓋過這些肉眼可見衝突；任一實質衝突即 REJECT。

## 停點與上限

私有 `STOP` 仍存在。R8f `pf004` 首試已 [REJECT](verify-16-r8f-native-stop.md)，因此 R8h `pf004` **最多剩一次 1 take + 1 judge**；本集 ledger 現為 **US$0.2355**，含舊 `pf003` 未解 US$0.0035 reservation，整集硬上限仍是 US$4.58。`pf005/006` 尚未試畫 R8f 新提示詞。若 `pf004` 再判退，保留 STOP，停止這一路線的後續購圖；即使通過，也須三景 3／3 native KEEP、另處理 `pf003` 預約並完成分鏡及網站卡片審核，才能考慮續畫。網站音訊卡依舊等待站主；本機委派核准不代表站主實際試聽。
