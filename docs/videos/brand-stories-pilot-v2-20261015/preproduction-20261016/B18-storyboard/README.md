# B18 免費分鏡準備

只在本機 Temp 製作，不改 frozen script、worker row、repo 或主機。

- 103 畫面槽，87 插畫、16 卡；預計 82 個不同圖，含3組hook共圖與尾聲三句共圖。尚未生成圖片。舊報價91張暫保留為保守上限假設；本包數量待獨立覆核再更新報價，沒有新增支出授權。
- 原全文2729計數單位，24段原ID、字句、順序完全重建。完整六章body含hook估654.96–711.91秒，加26秒動畫680.96–737.91秒；尚未實錄，慢端超過540–660秒的worker band，不能以舊300字／分推算保證9:06。
- 原row的hook預告為轉角／1958守生意／1978；本稿實際H02為轉角＋1958／1970萬博／1978。這裡照凍結稿作分鏡，沒有改row；正式章稿轉換前須窄對位／獨立review，不能把舊row收據當新版本審核。
- 原文沒有新增事實。CID以C-段ID作來源指標，來源與限制來自原製作註及已存在的獨立全文收據；不假造CONFIRMED。
- 三組hook setup/recovery同prompt、camera、image_asset_key；正式模型參數與accepted image SHA仍待綁。尾聲三句同圖採不同後製camera，不能當自動cache命中，正式轉換要共用既有檔案。
- 數字/來源卡只含必要資訊；正式chapter reader目前對卡片支援仍要依實作核驗，本包不是可直接匯入的worker章JSON。
- source_pins用repository_root相對路徑；工具報告只使用相對檔名。checks為離線編輯檢查，不是實稿panel、TTS、媒體或owner通過。

## 重建

在repo根以Node執行本目錄build-prep.mjs並傳repo根目錄。--prepare只重建原文切片；完整執行讀visual-design.mjs並用repo的shot_reading檢查。沒有供應商呼叫。
