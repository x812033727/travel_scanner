本篇用一份固定長文件比較重複請求的快取觀察，分別執行 Interactions 的隱含快取與 generateContent 的手動快取。你會保存模型、文件雜湊、實際 token 用量與快取資源，辨識沒有命中、欄位缺失和快取過期。目標是做出能重查的實驗紀錄，而不是先假設開啟快取一定比較省錢。

## 準備：把 API 家族分開

先完成 [[47|API 入門]] 與 [[49|費用和額度]]。本篇固定 Python 與 google-genai 2.23.0；參考模型為 gemini-3.8-flash，仍需確認專案可用性。查證日官方明確區分兩套接口：Interactions 支援隱含快取，手動建立及管理 cache 則使用 generateContent。

下載包提供長文件、三個相同問題、用量表與操作程式。文件有五百段帶獨立編號的合成文字，不包含私人資料。它的字數不等於 token 數；是否達模型要求的快取門檻，要看當日文件與實際計數，不能只因文字檔很大就宣稱一定命中。

先設定自己的專案與成本上限。本篇的本機測試只驗證請求格式、快取 ID、用量欄位與清理呼叫，並未測得雲端節省比例。usage-log.csv 的實際輸入、命中與帳單欄位保持 not_run，沒有以固定假數字包裝成服務基準測試。

## 第一階段：固定輸入，建立可比較基準

打開 cache-lab/document.txt，確認每段識別碼與問題要求相符。程式使用 SHA-256 保存文件版本；比較前不要為了讓第二次答案更好而偷偷修改文件。模型、完整前綴、問題與輸出需求也要固定，否則差異可能來自輸入變更，而不是快取效果。

第一輪記為「第一次觀察」，不能直接稱為「未命中基準」。隱含快取由服務處理，相同內容可能已有可用快取；如果第一輪就回傳 cached tokens，應如實保留。沒有手動指定 cache，也不代表服務完全不會使用隱含快取。

| 實驗欄位 | 為何保存 | 常見誤判 |
| --- | --- | --- |
| 模型識別與文件雜湊 | 確認比較同一份輸入 | 改文件仍算同一次實驗 |
| 輸入與命中 token | 觀察回應中的計量 | 缺欄位當作零 |
| 輸出與思考 token | 區分生成部分 | 重複計算已包含的用量 |
| 保存期間與帳單 | 比較實際總成本 | 只看命中就宣稱省錢 |

先決定最多三次重複提問，完成後停止分析，不為了取得漂亮的命中率一直增加呼叫。若需要比較別的模型，建立另一組檔案與表格；價格與門檻也另查，不把不同模型的數字直接並列成結論。

## 第二階段：觀察 Interactions 隱含快取

implicit 路徑每次把相同文件放在提示詞前方，後面接同一問題。它使用 input 與 store=False，沒有建立 cachedContents，也沒有把 cache ID 塞進 Interactions 請求。這樣能清楚區分伺服器對重複前綴的處理與手動快取物件。

```powershell 三次隱含快取觀察
.venv/Scripts/python.exe 84/cache-lab/main.py implicit --live --output implicit-usage.json
```

查看每輪回應的 usage.total_input_tokens、total_cached_tokens、total_output_tokens 與 total_thought_tokens。程式將缺少的欄位保留為 null，cached 為零才表示回應明示沒有命中；null 代表沒有觀察值，不能拿它計算命中率或省下多少錢。

若命中 token 大於輸入 token，應先停止解讀並檢查欄位或 API 家族是否讀錯。本機測試會拒絕這種矛盾資料。你也應保存未命中的結果，因為短輸入、前綴不同、請求間隔或服務狀態，都可能影響快取是否可用。

## 第三階段：在 generateContent 建立手動快取

create 路徑另用 generateContent 的資源設定，將同一長文件放進 cache，示範保存時間為三百秒。建立前先寫入 create_uncertain，成功後保存 cache 名稱與服務回傳資訊。若請求逾時，先按名稱和時間核對資源，不立即重建，避免留下不知道的計費物件。

```powershell 建立與查詢手動快取
.venv/Scripts/python.exe 84/cache-lab/main.py create --live --ledger cache-ledger.json --output cache-created.json
.venv/Scripts/python.exe 84/cache-lab/main.py query --live --ledger cache-ledger.json --output explicit-usage-1.json
```

查詢時，文件已在 cache 裡，contents 只放問題，config 的 cached_content 指向 ledger 中的名稱。這條路的輸出用量來自 usage_metadata，與 Interactions 的 usage 不同。不要將 total_cached_tokens 的欄位名稱直接套進 generateContent 的物件。

每次實際查詢另存一個輸出檔，避免覆蓋上一輪。若要做三次比較，就手動執行相同命令並替換檔名；建立快取的費用與保存費用也要納入。三百秒只是本練習的存活設定，不是免費時間，也不是所有情況都適合的正式服務設定。

> 手動快取程式與隱含快取程式各自保存 API 家族，沒有共享 Interaction 歷史或把兩邊的物件混用。測到命中只能證明回應提供命中數，不等於帳單總額一定較低。

## 第四階段：核對成本、過期與清理

將兩條路的觀察整理到 usage-log.csv，記錄實際請求時間、文件版本、回應用量、快取保存期間與對應帳單項目。先核對這些欄位，再使用當日價目計算；沒有帳單或費率依據時，結果只能稱用量比較，不能寫成實際節省百分比。

快取命中會影響輸入部分，但模型仍可能產生不同長度的答案，思考和輸出也可能變動。比較時看相同任務的完整成本，不只挑最有利的一個 token 欄位。若帳單統計尚未更新，保留待核對，不把暫時沒有顯示金額當作免費。

故障練習是在快取到期後，對原 cache 名稱再發一次 query，保存真實錯誤類型與時間；不要透過重新建立同名快取讓錯誤消失。到期時間應看服務回傳資訊，不能只用本機時鐘猜測。這一步可能需要稍後再操作，等待本身不是已驗收。

完成觀察後執行 delete，指定本次 cache-ledger.json。若資源已到期而回傳不存在，核對 ID 與過期紀錄，再保存結果；若是權限或其他錯誤，不能一概當成清理成功。測試資料與帳單紀錄保留，API Key 不放入輸出檔。

```powershell 清理本次手動快取
.venv/Scripts/python.exe 84/cache-lab/main.py delete --live --ledger cache-ledger.json --output cache-deleted.json
```

最後寫下哪些輪次確實命中、哪些沒有、哪些資訊仍不足，以及比較是否包含保存費用。若要大量評測相同題目，接著讀 [[85|Batch 與部分失敗處理]]；需要把成本控制放進應用程式，則進入 [[86|文件助手交付]]。

## 常見問題

### 第一次請求命中快取，是測試出錯嗎？

不一定。第一次觀察不保證是服務的首次處理；保留回應用量，避免把它強制改標成未命中。

### store=False 是否代表不會快取？

不能如此推斷。Interaction 狀態儲存與隱含快取是不同設定，本篇分別說明並觀察。

### 快取命中數很高，可以直接說省了同樣比例嗎？

不能。還要考慮命中與未命中費率、輸出、保存時間及其他計費項目，最後以自己的實際帳單核對。
