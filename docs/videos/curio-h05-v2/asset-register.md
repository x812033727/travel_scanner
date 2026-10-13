# H05 v2｜三張原件素材登記

2026-10-14。供新稿 `curio-h05-v2` 的 `assets[]` 與照片卡使用。原始下載、權利查核及像素檢視記錄在 2026-10-12 的舊稿底稿 [research-assets.md](research-assets.md)；本次從舊工作目錄逐檔複製原 JPEG，沒有重編碼或修改像素。三個舊檔及新檔均以 `Get-FileHash -Algorithm SHA256` 分別驗證，結果與下表 SHA、檔案大小逐項相符。

**v2 外部工作根目錄**：`<home>/mokaair-work/videos/curio-h05-v2/`。下列 `path` 均相對此目錄，三張新檔目前均可找到。複製來源是舊目錄 `<home>/mokaair-work/videos/curio-h05/stock/`，舊檔保持原樣；圖片不進 Git。每張以完整原件框入 `photo`，caption／credit 由版型另加，不能燒進、修補或 AI 重畫原圖。使用照片卡的版面縮放不等於改動來源檔；正式渲染仍需核對全圖與署名沒有裁掉。

## A01 機票

| 登記欄位 | 值 |
| --- | --- |
| `path` | `stock/d0d8c89a2e3d584d3f0956e85079d1d65b902653d2b96d59fff1b932bdd4a7aa.jpg` |
| `source` | Federal Bureau of Investigation (FBI), via Wikimedia Commons — July 2016: D.B. Cooper Plane Ticket |
| `author` | Federal Bureau of Investigation (FBI) |
| `license` | Public domain (PD-USGov-FBI) |
| `url` | https://commons.wikimedia.org/wiki/File:July_2016_D.B._Cooper_Plane_Ticket_(28379315406).jpg |
| 官方物件頁 | https://www.fbi.gov/history/artifacts/d-b-cooper-plane-ticket |
| 原圖 URL | https://upload.wikimedia.org/wikipedia/commons/3/37/July_2016_D.B._Cooper_Plane_Ticket_%2828379315406%29.jpg |
| SHA-256 | `d0d8c89a2e3d584d3f0956e85079d1d65b902653d2b96d59fff1b932bdd4a7aa` |
| 規格 | 2400×1369，1,395,429 bytes；JPEG |
| 卡片 caption／credit 建議 | 「以 Dan Cooper 名義購買的機票」／「FBI／公有領域」 |

**用途：** 1971年購票用名與案件通稱對照。姓名欄實際可讀。照片日期欄是2016-06-23，不說1971當天拍攝；Dan Cooper不等於已確認真名。不補字、不生成複製票、不把票券商標拿來當節目背書。說明欄保留機構、檔名、授權與來源連結。

## A02 尋回的部分贖金

| 登記欄位 | 值 |
| --- | --- |
| `path` | `stock/f3e989c1f24e4204a3e8163e80b163c000e8af41ec98a78dbb15901ee8beab92.jpg` |
| `source` | Federal Bureau of Investigation (FBI), via Wikimedia Commons — Money stolen by D. B. Cooper |
| `author` | Federal Bureau of Investigation (FBI) |
| `license` | Public domain (PD-USGov-FBI) |
| `url` | https://commons.wikimedia.org/wiki/File:Money_stolen_by_D._B._Cooper.jpg |
| 官方內容佐證 | https://archives.fbi.gov/archives/news/stories/2007/december/dbcooper_123107 |
| 原圖 URL | https://upload.wikimedia.org/wikipedia/commons/e/ef/Money_stolen_by_D._B._Cooper.jpg |
| SHA-256 | `f3e989c1f24e4204a3e8163e80b163c000e8af41ec98a78dbb15901ee8beab92` |
| 規格 | 1400×921，210,549 bytes；JPEG |
| 卡片 caption／credit 建議 | 「1980 年尋回的部分贖金」／「FBI／公有領域」 |

**用途：** 河岸章及 2.9% 實算旁的原件；開場的河岸預告不提前展示鈔票。這是破損鈔票的陳列照，不是發現現場；拍攝日期不明。保留鈔票印刷肖像及序號原樣，不能補繪、換額、調換序號或由可見殘片數推估總量。暗色殘片不自行判成燒毀；照片也不證明錢的漂流、入水、埋入時間。2.9% 由 FBI 的 5,800／200,000 金額計算，不能從照片讀出。

## A03 領帶

| 登記欄位 | 值 |
| --- | --- |
| `path` | `stock/52f8ad581b3932f1060809875c43cfb05df710d0b19006db0e39083ed8604449.jpg` |
| `source` | Federal Bureau of Investigation (FBI) — D.B. Cooper case evidence, black tie |
| `author` | Federal Bureau of Investigation (FBI); individual photographer not credited |
| `license` | Public domain — FBI/DOJ website material, no third-party credit indicated |
| `url` | https://www.fbi.gov/history/famous-cases/db-cooper-hijacking |
| 權利依據 | https://www.justice.gov/legalpolicies （FBI頁尾連結；保留第三方作品例外） |
| 實際圖片 URL | https://www.fbi.gov/image-repository/black-tie.jpg/@@images/image/large |
| SHA-256 | `52f8ad581b3932f1060809875c43cfb05df710d0b19006db0e39083ed8604449` |
| 規格 | 768×616，106,481 bytes；JPEG；官方 `large` 版本，不冒稱最高解析度原圖 |
| 卡片 caption／credit 建議 | 「留在機上的領帶」／「FBI／公有領域」 |

**用途：** 說明留在機上的物件與後來取樣，宜框內呈現、少量運鏡，避免滿版過度放大。領帶及金屬飾件完整，不裁切頂端或尾端。無個別攝影者署名，故不虛構攝影人名；未另核明clip-on文字來源前不靠外形加此斷言。DNA取自領帶，不能配畫成已證明屬於劫機者或某名嫌疑人。

## 照片呈現與交接核對

- 原生照片框、caption 與 credit 可渲染在原圖外；不對來源 JPG 去背、補繪、修字或重新儲存。三張均為實際物證檔案照，畫面不要套「AI重建」；相鄰情境插圖則應依全片揭露維持示意身份。
- 三張原檔不含當事人人臉；A02的貨幣印刷肖像是官方檔案內容。沒有核准嫌疑人臉、FBI素描、漫畫書封、品牌標誌或新科學圖表。
- `assets[]` 的 path／author／license／source／url 應完整保留，說明欄列三項來源；Commons兩圖的授權頁與FBI原件來源不能只剩搜尋頁。領帶權利來自官方供圖及所連結政策，不假填CC授權。
- 圖片至少各呈現一次；同一原檔可因新的證據用途再次引用，但不當作新增獨立來源。照片間以插圖或原生卡片分隔；姓名欄、殘鈔全貌與領帶邊緣需在運鏡起／中／末仍可辨識。
- 原件登記不等於最終視覺通過；待完整稿、正式卡片預覽及成片抽格各自留下實際檔案／SHA判讀。
