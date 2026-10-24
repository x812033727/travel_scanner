# C09 Patagonia｜v8 本機試片準備狀態

狀態：**HOLD**。本頁只記錄不付費的專案轉檔與停線條件，並非試片、後台匯入或上架核准。

## 已核對

- 站主核准的 `script.md` 與凍結候選同位元組，SHA-256 `4445AD74BCAFBAC1DFCA65392199FEC89700C17AB8C01E665AC79DFFFC1AA3F7`。
- 現行 `visual-plan.json` 與已查核的 77 鏡候選同位元組，SHA-256 `2235EA304C240E78F6473183E45A63502500EE20F931107843C6AF3C5AD0BF5A`。77 個鏡頭 ID、旁白 ID／文字、模板、提示詞及字卡資料逐一相同；67 鏡插圖、10 張字卡。
- `node docs/videos/story-everyday-patagonia-c09/preflight-v8.mjs` 為唯讀漂移檢查；`node tools/video/cli.mjs lint --slug story-everyday-patagonia-c09` 為 0 errors、10 warnings。紙上正文 567.633 秒，不是實際語音長度。
- `video.json` 的 `category: explainer` 使已核准的 `stats` 字卡符合本機影片 schema；後台劇本匯入的系列分類仍為 `story`。這份本機專案不得當作後台分類更新來源。
- 衍生 `video.json` 對 10 張後製字卡只改觀眾可見的 `title`／`source`；10／10 數值、標籤、旁白與模板，及 67／67 插圖提示詞維持凍結候選。字卡修正把內部代碼與編輯備註留在候選和查核檔，畫面改用可讀的標題／來源；獨立覆核通過。凍結 `visual-plan.json` 位元組未動。

## 製作前須補

1. **舊工人防護：** 本機預檢不能阻止主機舊版 `story.mjs` 從章節工作檔重寫 77 句 `script.md`／`video.json`。系列維持 paused；另有[正常任務](../../../tasks/open/2026-10-24-guard-c09-v8-stale-worker.md)待協調共用程式路徑、審核工人保護，並完成主機讀回，才可解除暫停。
2. **成本與音訊：** 尚未有 C09 專屬單集預算帳本與舊費用歸因、全片可靠報價、站主整支付費核准，亦未量測正文語音是否至少 480 秒。這些條件完成前不得呼叫付費服務或購圖。
3. **媒體驗收：** 67 鏡提示詞的鏡頭景別主要為中文，現行 lint 因只辨識英文景別而警告；另有 1 鏡約 10.4 秒、5 段鉤子間隔、片頭濃縮與年份回述警告。生成後需實際檢查畫面與節奏，不能把 0 errors 當成成片合格。

本次沒有生成圖、旁白、配樂或成片，也沒有後台寫入、上傳、發布。
