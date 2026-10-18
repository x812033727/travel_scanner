# H05｜檔案圖片來源與授權查核

查核日期：2026-10-12。範圍：機票、尋回的贖金、領帶三張物證圖。三檔均已實際下載、以 `view_image` 看過像素，沒有修改、裁切、重繪或放大圖檔；尚未匯入影片素材表或完成影片中的呈現審查。圖片只存外部工作區。

結論：三張均可作本集檔案圖候選；首選機票及贖金，領帶作第三張。沒有當事人照片或通緝素描。贖金圖保留鈔票本身的印刷肖像，屬原始物證照片，不是生成的人像或貨幣。

## 共通授權依據與讀取紀錄

- 機票與贖金：今日直接讀取 Commons API 的 `imageinfo`、`extmetadata` 與檔案頁原始碼；兩頁均標作者 FBI、`Public domain`、`PD-USGov-FBI`、`Copyrighted=False`。機票另有 FBI 官方 Flickr 來源與既存 Flickrreview 通過紀錄；今日未把該歷史自動審核冒稱為重新查閱 Flickr。
- 領帶：直接取自 [FBI 案件頁](https://www.fbi.gov/history/famous-cases/db-cooper-hijacking) 內嵌圖片，頁面未列非聯邦機構的攝影署名。依 FBI 頁尾所連結的 [DOJ 著作權政策](https://www.justice.gov/legalpolicies)，未另行標示的 DOJ 網站內容屬公有領域；第三方作品例外。本次沒有把「任何 .gov 圖都能用」當成授權依據，也沒有另取 FBI 徽章作品牌標誌。
- FBI 案件頁、機票物件頁、[2007 年 FBI 檔案文章](https://archives.fbi.gov/archives/news/stories/2007/december/dbcooper_123107) 與 DOJ 政策均讀到正文；三個實際圖片下載皆 HTTP 200、`image/jpeg`。
- 領帶 `/view` 頁曾逾時，但案件頁正文及其實際內嵌圖片均已成功讀取。Commons `Cooper tie` 搜尋未找到合適的領帶授權頁，故不假填 Commons 授權模板。
- 外部證據目錄：`<home>/mokaair-work/videos/curio-h05/_audit/source-assets/`。其中 `commons-ticket-money.json` 留存 API 完整授權回應；`fbi-case.html`、`fbi-ticket.html` 留存官方來源；`downloads.json` 記載每檔實際請求／回應 URL、時間、尺寸、位元組與 SHA-256。圖片 URL 的 Commons 追蹤查詢參數只出現在下載收據；以下連結指向同一原檔。

## A01｜Dan Cooper 機票

| 欄位 | 查核結果 |
| --- | --- |
| 官方來源 | [FBI：D. B. Cooper Plane Ticket](https://www.fbi.gov/history/artifacts/d-b-cooper-plane-ticket) |
| 授權頁 | [Commons 機票檔案頁](https://commons.wikimedia.org/wiki/File:July_2016_D.B._Cooper_Plane_Ticket_(28379315406).jpg) |
| 原始來源指向 | [FBI 官方 Flickr 相片](https://www.flickr.com/photos/fbi/28379315406/)；本輪授權核對經 Commons API 與 FBI 物件頁 |
| 下載原檔 | [Commons JPEG](https://upload.wikimedia.org/wikipedia/commons/3/37/July_2016_D.B._Cooper_Plane_Ticket_%2828379315406%29.jpg) |
| 作者／授權 | Federal Bureau of Investigation（FBI）；公有領域，Commons `PD-USGov-FBI` |
| 日期 | 物件關聯事件為 1971-11-24；Commons 的照片日期欄記 2016-06-23 12:06。不得把此照片說成案發當天拍攝 |
| 尺寸／大小 | 2400 × 1369；1,395,429 bytes |
| 外部檔案 | `<home>/mokaair-work/videos/curio-h05/_audit/source-assets/ticket-original.jpg` |
| SHA-256 | `d0d8c89a2e3d584d3f0956e85079d1d65b902653d2b96d59fff1b932bdd4a7aa` |
| 像素審看 | 已看完整圖；工具顯示縮至 2048 × 1168，檔案本身未改。泛黃票券四周完整，姓名欄的 Dan Cooper、航空公司名、Seattle 與日期戳可辨識，無人臉 |

**建議用途：** 從票券上留下的名字切入；可在版面另加中文指示框，保留原圖文字。圖說用「以 Dan Cooper 名義購買的機票｜FBI／公有領域」。不能因此說 Dan Cooper 是已確認的真實姓名。票券上其他淡化手寫字不宜自行補寫或用 AI 修復。

## A02｜1980 年尋回的部分贖金

| 欄位 | 查核結果 |
| --- | --- |
| 官方內容佐證 | [FBI 案件頁](https://www.fbi.gov/history/famous-cases/db-cooper-hijacking) 與 [2007 年 FBI 檔案文章](https://archives.fbi.gov/archives/news/stories/2007/december/dbcooper_123107) 的物證圖說 |
| 授權頁 | [Commons 贖金檔案頁](https://commons.wikimedia.org/wiki/File:Money_stolen_by_D._B._Cooper.jpg) |
| 下載原檔 | [Commons JPEG](https://upload.wikimedia.org/wikipedia/commons/e/ef/Money_stolen_by_D._B._Cooper.jpg) |
| 來源沿革 | Commons 指向 FBI 舊文章 `dbcooper123107.html` 與舊合成圖 `tiemoney122607.jpg`；今日以仍可讀取的 FBI 官方檔案文章及現行案件頁交叉核對物件，未假稱重開舊失效網址或 Wayback 原圖 |
| 作者／授權 | FBI；公有領域，Commons `PD-USGov-FBI` |
| 日期 | 照片拍攝日期未記錄；1980 是尋回事件年份，不是已知的拍攝日期 |
| 尺寸／大小 | 1400 × 921；210,549 bytes |
| 外部檔案 | `<home>/mokaair-work/videos/curio-h05/_audit/source-assets/money-original.jpg` |
| SHA-256 | `f3e989c1f24e4204a3e8163e80b163c000e8af41ec98a78dbb15901ee8beab92` |
| 像素審看 | 已看 1400 × 921 全圖。淺色背景上排列破損鈔票、暗色成疊殘片與細碎紙片；可見部分面額、印刷肖像與序號片段，無現場人物 |

**建議用途：** 說明物證仍在、部分金錢被尋回。圖說用「1980 年尋回的部分贖金｜FBI／公有領域」。這是物證陳列圖，不能標成河岸挖掘當下；不能由畫面推算總張數、完整金額或落水時間。直接使用檔案照片，勿生成或補繪鈔票、序號，勿把暗色殘片自行定性為遭焚燒。

## A03｜留在機上的領帶

| 欄位 | 查核結果 |
| --- | --- |
| 官方來源 | [FBI 案件頁](https://www.fbi.gov/history/famous-cases/db-cooper-hijacking)；[2007 年 FBI 檔案文章](https://archives.fbi.gov/archives/news/stories/2007/december/dbcooper_123107) 亦有相同物證說明 |
| 實際圖片 | [FBI 領帶 JPEG](https://www.fbi.gov/image-repository/black-tie.jpg/@@images/image/large)；此為官方頁使用的 `large` 版本，未證實是最高解析度原圖 |
| 作者／授權 | FBI 提供，個別攝影者未署名；依官方頁未列第三方署名及 [DOJ 公有領域政策](https://www.justice.gov/legalpolicies) 採用，不填不存在的 CC 授權 |
| 日期 | 物件與 1971 年事件相關；本圖拍攝日期未記錄 |
| 尺寸／大小 | 768 × 616；106,481 bytes |
| 外部檔案 | `<home>/mokaair-work/videos/curio-h05/_audit/source-assets/fbi-black-tie.jpg` |
| SHA-256 | `52f8ad581b3932f1060809875c43cfb05df710d0b19006db0e39083ed8604449` |
| 像素審看 | 已看 768 × 616 全圖。黑色領帶斜放在淺色布面，頂部結形、整條領帶與金屬飾件均在框內，沒有手、人物、臉或現場背景 |

**建議用途：** 放在較小的檔案卡內，保留周邊留白，避免滿版放大使細節模糊。圖說用「留在機上的領帶｜FBI 檔案照片／公有領域」。已讀官方圖說支持領帶物證及其曾供 DNA 採樣；不能說樣本已證實屬於劫機者。正式字幕如需稱「夾式領帶」，另綁明寫 clip-on 的來源；本輪不以照片外形替這個結構細節作證。

## 採用順序與未納入項目

1. **機票：優先採用。** 解析度足夠，能直接呈現「留下名字」這個證據點。
2. **贖金：優先採用。** 可呈現實際尋回物，維持物證陳列圖的正確身份。
3. **領帶：可用，版面限縮。** 物件清楚但解析度較低；不必為補第三張而改用當事人肖像。

三張均建議保留「FBI／公有領域」來源標示並在說明欄連回原頁。未下載或採用通緝素描、通緝海報、嫌疑人肖像、論文圖表或降落傘袋；沒有把這些候選列為已完成像素審查。
