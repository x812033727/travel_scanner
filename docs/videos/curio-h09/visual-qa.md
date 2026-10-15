# H09 分鏡文字獨立檢查

- 結果：**PASS（生成前文字分鏡）**
- 檢查日期：2026-10-15（台北時間）
- 原文字分鏡 `video.json` SHA-256：`4797571A473BD2F608EF0A40E95A989B4B51231BA208A88C30044653A1D7E7A1`
- `script-draft.md` SHA-256：`361ECEA6E3FFDF8283F7B3C1C325E1C9B83FA122E67AACB3C637A41BDCA11F83`
- 範圍：對照草稿旁白、場景文字、卡片、插畫提示詞、主張標記、來源與影片說明；未檢查實際生成圖片、音訊或成片。

## 對照結果

1. 草稿的 95 個有行 ID 的旁白行，依序串接後與 `video.json` 的 100 個音段逐字一致；僅忽略空白，合計 2,649 個字元。B18、F05、F06、F07、F08 五行各拆成雙場，沒有增刪旁白文字。
2. 全片 100 場：92 個 `shot` 插畫鏡頭、7 張 `big` 字卡、1 個 `outro`。92 個 `shot` 都有提示詞；固定畫風為 `cute-mystery`。所有場景引用的 `H09-Cxx` 均可在 `claims.md` 找到。
3. 2026 年現場時序一致：10 月 13 日先踏查 Taraia 沙洲；10 月 14 日已用無人機查看 Taraia，並以磁力儀和側掃聲納展開潟湖調查，資料仍待分析。水力探針直接接觸與後續清淤仍寫成計畫，不作為已完成事項。
4. `video.json` 的來源清單與 YouTube 說明納入[普渡大學 2026-10-14 現場公告](https://www.purdue.edu/newsroom/2026/Q4/earhart-expedition-update-underwater-survey-of-taraia-object-begins/)，明確說尚未公布 Taraia 物件鑑定結果。
5. 畫面提示以模糊潟湖影像、空白器材、未解讀儀器畫面及條件式對照呈現；沒有把 Taraia 畫成已確認的飛機或挖掘成果。2024 年豪蘭附近的深海岩石與 Taraia 潟湖目標分開。

## 配音讀法修正後的綁定

與上一版 `video.json` SHA-256 `F3159462A1B030FE197E2B35D552D6AE74B3EF40587B6C4ACDAE2842AE2766D2` 比對，唯一修改是音段 `h1j3jy6q` 的 `say` 覆寫：刪掉重複的「研究團體」，改為「這些殖民地文件的抄本和掃描，是後來由提加研究團體公布的。」場景 ID、`text`、提示詞、卡片及主張標記均未改。工具 `narrativeHash` 前後同為 `c86a4a4f74475bcd`，`visualHash` 前後同為 `3baa6d38a808fbad`，因此上述文字分鏡 PASS 仍適用；`speechHash` 則由 `bcd031d4d477c8f2` 改為 `31ed2734d0317ba9`。正式 `script.md` 的 speech footer 也已隨之重產，舊劇本關卡若綁舊檔案雜湊，須以後台讀回確認目前核准狀態。

## 限制與後續

本次 PASS 只適用於上述原版檔案雜湊所指的文字分鏡，不代表實際插畫已驗收。插畫生成後仍須逐張檢查是否遵守不預先宣告發現的提示；成片及發布前須重查普渡大學與 ALI 的最新公告。如畫面、旁白 `text` 或來源內容改動，本次檢查需重做。

## 2026-10-15 七鏡付費小樣與提示詞修訂

首輪只產出 7／92 鏡、11 次圖片與 11 次評審；媒體帳本記錄 US$0.1485，預留額為零。`low-fuel-warning`、`uncertain-broadcasts` 各三輪均被評審標為 `needs_review`。人工逐張冷看也發現 `itasca-waits` 水手似乎浮在船外、`radio-0843` 手部與人物比例不自然、`radio-silence` 手勢偏離耳機、`search-plane-island` 的飛機有擬人眼睛及可見乘員；這些鏡頭即使評審顯示 pass，也不視為人工驗收通過。舊版小樣保留作診斷證據，本集 `STOP` 暫停檔仍在。

只改六鏡的 `data.prompt` 構圖：`itasca-waits`、`low-fuel-warning`、`radio-0843`、`radio-silence`、`uncertain-broadcasts`、`search-plane-island`。後兩鏡改用另一座 1930 年代電台的木殼接收機與遠距俯視的海軍水上飛機，避開多餘人物和擬人飛機；不在提示詞重複系列畫風或調色。修訂後 `video.json` SHA-256 為 `C8EA0BB8352FFEE86A2B7D113D1256C86321045EE39C18A8D8E94381A70B5075`，已核准 `script.md` SHA-256 仍為 `7294FD9410349DCBA89347631DF46A551C8A6C570A58983BE11E58A073FA41D5`。獨立複核確認六鏡與原旁白及主張相符；其餘 86 鏡提示詞、旁白正文與固定 `cute-mystery` 風格未改。`lint` 為 0 錯誤、原有 3 項敘事啟發式警告。新版須重新付費產圖並逐張冷看，尚無新版插畫 PASS，也尚未送分鏡關卡。
