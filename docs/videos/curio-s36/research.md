# S36｜1919 年波士頓糖漿災難：一手來源可行性查核

查核時間：2026-10-20 04:38–04:40 UTC。**結論：暫緩前製。** 這份文件記錄的是此雲端能否重開並固定原始資料，並非事故史實定稿。目前沒有成功取得可讀的 1919 年當代報刊、事故調查、法庭紀錄或可信的完整校錄，因此無法支撐逐句查核的八分鐘以上單線故事。未寫 `brief.md`、劇本、分鏡；未呼叫付費圖像或語音工具。

## 來源重開收據

查核方法：對下列入口執行 `curl -L -sS --max-time 8 -o /dev/null -w '%{http_code} %{errormsg}\n' '<URL>'`；各次都在連線代理階段回 `curl: (56) CONNECT tunnel failed, response 403` 和 `000 CONNECT tunnel failed, response 403`，**未讀到站方內容**。入口只代表待查的來源類型，不表示已確認該站館藏有此案的特定文件。

| 欲取得的一手材料 | 此次測試入口 | 此雲端結果 | 能否當本集證據 |
| --- | --- | --- | --- |
| 1919 年報刊原版或 OCR | [美國國會圖書館報紙查詢](https://www.loc.gov/newspapers/?fo=json&q=Boston+molasses+1919)、[Chronicling America](https://chroniclingamerica.loc.gov/) | 兩入口均 CONNECT 403；未取得報紙頁、日期或 OCR | 否；連館藏命中都未核實 |
| 波士頓地方館藏的報刊／檔案 | [Boston Public Library](https://www.bpl.org/) | CONNECT 403；未取得目錄或原件 | 否 |
| 州政府事故或司法原件 | [Massachusetts 官方入口](https://www.mass.gov/) | CONNECT 403；尚未定位具體案卷 | 否 |
| 可能收錄的公有領域掃描 | [Internet Archive](https://archive.org/)、[Google Books](https://books.google.com/) | 兩入口均 CONNECT 403；尚未找到可確認的書卷／頁碼 | 否 |

GitHub API 此雲端可用，因此另以 `gh search code` 搜尋 `"Boston molasses" 1919`、`"molasses tank" "Boston" "1919"`、`"molasses flood" "newspaper"`、`"Hugh W. Ogden" "molasses"`、`"Molasses Tank" "January" "1919"`，均回 `[]`。放寬到 `"United States Industrial Alcohol Company"`、`"Purity Distilling Company"` 時有程式碼資料集、維基來源或現代敘述，未見可辨識的當代報刊、事故報告或證詞原文。此為**目前搜尋命中**的紀錄，不能推論全網沒有原件。唯一較像 OCR 資料庫的 [Chronicling America OCR downloads 固定版本](https://github.com/sclayton29/Chronicling-America-OCR-downloads/tree/2334170ff7249d00dc5933ca23dc01a0a5b788a5/text-files) 可重開，但該目錄只有 0 byte 的 `placeholder.txt`，沒有 1919 年文本。它只證明此路不通，不能當史料。

## 尚待逐項核對的主張

以下是這題常見、製片時會用到的**待查主張**，不是本紀錄確認的事實：

| 主張／問題 | 必須找到的原始支撐 | 本次判定 |
| --- | --- | --- |
| 1919 年 1 月 15 日的事故時序、地點、槽體與街道上發生的事 | 可辨期數、頁碼的當日／翌日報紙；現場調查或庭訊原文 | 未取得，不能排逐分鐘戲劇線 |
| 死亡人數常傳為 21、受傷人數常傳為約 150 | 同一統計口徑的官方最終名單／當代報告；若用翌日報紙，須標明只是當時暫報 | 未取得；不能在旁白或封面當定數 |
| 糖漿流速常傳為 35 mph（約 56 km/h） | 有量測、推算或目擊引述出處的原件及方法 | 未取得；不能把流傳數字畫成實測速度 |
| 儲槽容量、當時儲量、波高與波及面積 | 設計／營運／調查紀錄，並區分容量與事發當下儲量 | 未取得；不能混用不同數字 |
| 事故原因是結構與檢修問題、發酵壓力、或遭人破壞？ | 調查與庭審的雙方主張、工程證據及最後裁判 | 未取得；不能用後世轉述替代爭點與裁斷 |

## 停拍門檻與恢復條件

現在連同一份可固定版本的一手敘事原件都沒有。八分鐘以上影片需要按時間追蹤現場、救援、調查及爭議；只憑後世摘錄會把暫報傷亡、傳說中的流速和事故成因混成確定的故事。故 S36 停在題目卡，不進企劃／劇本／媒體製作。

恢復時先取得**至少一份**可在此雲端重開、附版次／期數／頁碼的當代報刊或官方調查／庭審全文，保存固定 URL 與全文 SHA-256；再另尋獨立一手資料交叉核對傷亡及成因，逐項追流速數字的來源。若只能重開後世作品，仍維持暫緩。
