# C18 Fiskars｜獨立逐句來源與配鏡查核

審核日期：2026-10-23。審稿者：`codex-c18-independent-audit`。基底：作者 PR #1711 的 `ea46ff32b07a234e20e8e462ba8986e5150d3693`。結果：**HOLD，須由作者作下表的窄修，修改後只重核受影響句與配鏡。** 這是 85 句旁白對 M01–M12 原件、`source-notes.md`，以及同 ID 的 85 景 JSON 和章節 MD 所作的獨立查核；未修改作者四個輸入檔。它不是純旁白盲讀、站主劇本核准、TTS 實測、圖像驗收或付費授權。

## 綁定的四個輸入檔

| 檔案 | SHA-256 |
| --- | --- |
| `script.md` | `B390D5C43B080C71928F3A368BEBD75FD11FC8E814AB8B42E70B9846A3D358FB` |
| `source-notes.md` | `8D854E405A20888087ECBC0CB32CB6D337362746BEBA75311AF74CC7D510AD6B` |
| `visual-plan.md` | `BC228AE25FF6247B36AB3F54D4ADFF8D3986085F42110C5E09979875C2F66F63` |
| `visual-plan.json` | `7D30F6B09CB00093043E988348928527136B505D0A2C88AB46EBBDE4C37CAF48` |

任何一個輸入檔改字，本收據都不自動適用於新位元組。Hash 由獨立審核工作樹的檔案 bytes 計算，與作者預檢所列四值相同。

## 直接開啟的 M01–M12 原件

Fiskars 官網在網頁擷取器逾時；改以專案要求的 `Mokaair-editorial/1.0` User-Agent 直接抓原網址，以下 Fiskars HTML/PDF、Cision PDF、CIPO PDF 均回 HTTP 200，PDF 直接抽取相應頁文字。MoMA 館藏頁直接讀取。這些是公司／官方原件，不把較早的企劃 PASS 當作本次逐句查核。

| 矩陣 | 原件與本次核到的界線 |
| --- | --- |
| M01–M02 | [Fiskars 沿革](https://fiskarsgroup.com/about-us/our-story/)及[2024 年公司債券說明書](https://fiskarsgroup.com/wp-content/uploads/2024/01/Fiskars-Oyj-Abp-Listing-Prospectus-for-Fiskars-Corporations-EUR-200-million-sustainability-linked-notes.pdf) PDF 0-based p44：1649 鐵工坊；1832 餐具廠產品含剪刀；二戰後的結構改革是為適應大量生產，沒有戰後剪刀產量。 |
| M03–M04 | [2006 年公司年報](https://fiskarsgroup.com/wp-content/uploads/2021/08/fiskars_en_2006.pdf) PDF p6 與 [2017 年公司新聞稿](https://fiskarsgroup.com/news/press-release/innovation-and-creativity-fiskars-corporation-participating-in-the-new-land-of-technology-exhibition-as-corporate-partner/)：年報將 Bäckström 的橘柄剪刀起點放在 1967，說塑膠握柄使一般用剪刀「更便宜」；新聞稿說新研磨法與塑膠帶來新的人體工學。兩者都沒有剪切效率或**製作成本**測量。 |
| M05–M06 | [公司沿革](https://fiskarsgroup.com/about-us/our-story/)、[2006 年報](https://fiskarsgroup.com/wp-content/uploads/2021/08/fiskars_en_2006.pdf) p6、[2024 年說明書](https://fiskarsgroup.com/wp-content/uploads/2024/01/Fiskars-Oyj-Abp-Listing-Prospectus-for-Fiskars-Corporations-EUR-200-million-sustainability-linked-notes.pdf) p45，以及 [2017 年公司新聞稿](https://fiskarsgroup.com/news/press-release/innovation-and-creativity-fiskars-corporation-participating-in-the-new-land-of-technology-exhibition-as-corporate-partner/)：機器剩橘料、黑／紅／綠／橘試色及內部投票都是多年後的公司敘述；精確投票日期也只見後來新聞稿。另讀[公司 Fiskamin 展覽新聞稿](https://fiskarsgroup.com/news/press-release/orange-and-more-exhibition-celebrates-fiskamin/)：只說 Fiskamin 意外促成橘柄剪刀，不能據此斷言兩者同日或同一機器。本稿沒有這項額外推斷。 |
| M07–M08 | [2006 年報](https://fiskarsgroup.com/wp-content/uploads/2021/08/fiskars_en_2006.pdf) p6 清楚記產品線左手用款於 1972 推出，並談後續人體工學及製程改良；[公司沿革](https://fiskarsgroup.com/about-us/our-story/)和[2024 年說明書](https://fiskarsgroup.com/wp-content/uploads/2024/01/Fiskars-Oyj-Abp-Listing-Prospectus-for-Fiskars-Corporations-EUR-200-million-sustainability-linked-notes.pdf) p45 記 1977 美國剪刀廠。這不能推出全球第一把左手剪刀或此後全在美國製造。 |
| M09–M10 | [2003 年報](https://fiskarsgroup.com/wp-content/uploads/2021/08/Fiskars_2003_en_v1.pdf) p3／p12 說芬蘭 2003 年註冊；[2006 年報](https://fiskarsgroup.com/wp-content/uploads/2021/08/fiskars_en_2006.pdf) p6 說美國 2007 年 1 月註冊。[2014 公司加拿大新聞稿 PDF](https://mb.cision.com/Public/10696/CM_109706/94b40ab74060676f.pdf)也列芬蘭／美國年份。芬蘭、美國的登記簿與確切商品／標示範圍並未在本次原件組內；保留「公司年報記載」，不可借用加拿大範圍替兩地作證。該新聞稿的「上週」時間敘述與 CIPO 官方登記日不合，本稿採 CIPO 日期是對的。 |
| M11 | [加拿大 CIPO TMA877999 原始紀錄](https://ised-isde.canada.ca/cipo/trademark-search/pdf/1602003?lang=eng) p0：2014-05-15 註冊；商品是手動剪刀；標示是**登記圖中那把剪刀的特定握柄整個可見表面**所施用的橘色。不是橘色本身在所有商品、所有剪刀或所有國家的壟斷。 |
| M12 | [MoMA 藏品 306.1977](https://www.moma.org/collection/works/3250)：設計年段 1960–1967、這件實物 1976、材質塑膠與不鏽鋼，頁面目前標示未展出。它不是可指認的 1967 首件。 |

## 85 句與同 ID 畫面的覆核範圍

逐行讀了 85 句的「旁白／依據」，逐行對到 JSON 的同 ID `kind`、`text`／`prompt`，並按章核對 MD 摘要。其餘 ID 在上述來源與概念畫面邊界內未發現相反事實。每章結果如下；HOLD 的具體位置與修法在下一節。

| 章 | ID | 旁白／JSON | 插圖／後製卡 | 結果 |
| --- | --- | ---: | ---: | --- |
| 1 | c180101–c180108 | 8／8 | 8／0 | HOLD c180103–104；其餘配對相合。 |
| 2 | c180201–c180215 | 15／15 | 12／3 | M01–M02、年代卡及概念場景相合。 |
| 3 | c180301–c180316 | 16／16 | 15／1 | HOLD c180307–308；其餘 1967、技術與顏色懸念相合。 |
| 4 | c180401–c180416 | 16／16 | 15／1 | 公司回顧／投票明示歸屬；1972 左手用款正確。 |
| 5 | c180501–c180519 | 19／19 | 15／4 | HOLD c180511；其他年份和加拿大商品限制相合；未把橘色寫成銷量原因。 |
| 6 | c180601–c180611 | 11／11 | 9／2 | HOLD c180608；MoMA 的兩組年份、材質與未展出的畫面邊界相合。 |

### HOLD：請作者作窄修

| HOLD ID | 受影響句／畫面 | 原件差距與最小修法 |
| --- | --- | --- |
| H01 | `c180103`、`c180104` 旁白；同 ID 概念工坊／樣品桌畫面 | 開場先把後來的公司故事說成現場已知事實；「桌上」是畫面編排，不見於原件。第一句加「按 Fiskars 多年後的說法」；第二句改為「還有幾種不同顏色的樣品，等著被選」一類無真實桌面斷言。畫面可留概念插圖，但須與此歸屬一致，不當 1967 實拍重建。 |
| H02 | `c180307`、`c180308` 旁白及 `c180308` 計算紙畫面 | 年報只說壓鑄塑膠握柄使一般用剪刀更便宜，沒有明說**製作成本下降**或量測成本。把「製作成本」改為「一般用剪刀變得更便宜」，下一句改為「便宜多少，年報沒有給數字」；計算紙改成純概念剪刀對照或維持完全空白，不能暗示讀過成本帳。 |
| H03 | `c180511` 旁白及同 ID 通用剪刀畫面 | CIPO 說的是**圖中剪刀的特定握柄整個可見表面**，目前旁白省略「特定」與「整個」可能讓橘色局部或任意握柄也落入範圍。補齊這兩個限定。畫面是通用示意剪刀，不能讓觀眾誤當 CIPO 的登記圖；可換成後製範圍字卡，或在分鏡明示只是概念示意並避免描摹圖樣。 |
| H04 | `c180608` 旁白；同 ID 三張空白登記紙 | 芬蘭與美國來源只給註冊年份，未讀到其登記簿的具體範圍。不要把加拿大可核的商品／外觀限制概括為三地文件的已查結果。改成「各地登記要分開看；我們讀到的加拿大原件，明寫手動剪刀與特定握柄的橘色」一類限定；畫面可維持三份互不重疊的空白紙。 |

輕微措辭／提示詞清理，不列為額外 HOLD：`c180609` 的「一桶橘色塑膠」可改「一點橘色塑膠」，避免把機器剩料說成可量出的整桶；`c180214` 圖片 prompt 的「桌上沒有文字」宜改成正面物件描述「素面桌」，避免讓圖片模型收到「文字」字樣。這兩處不等於目前 prompt 要求生成可讀字。

## 結構、禁詞與後續關卡

- 85 個旁白 ID 與 85 個 JSON ID 按序完全一致，雙方重複 ID 均 0；MD 的六章數量與 JSON 一致，總計 **74 `shot`／11 `stats`**，最多連續 2 張卡。74／85 是**張數比例**，不證明插圖佔正文畫面時間 ≥70%。
- 74 個 `shot.prompt` 沒有品牌或設計師姓名、logo、商標圖樣、MoMA、歷史年份數字，沒有要求畫可讀字；所有文字卡均為後製 `stats`。圖片模型 `MiniMax image-01`，`look` 恰為 `{"preset":"cute-mystery"}`，沒有附加 style／negative。單一 prompt 用了否定式「沒有文字」（上節建議清理）。
- 開場末句 `c180108` 後預定 5 秒片頭；`c180611` 後預定 21 秒 v4 片尾與結束畫面連結位置，符合 [BRANDING.md](../../BRANDING.md) 的現行位置／長度。旁白不點名下一集。
- `c180302` 只講 1967 產品起點，不宣稱世界首創；`c180411` 將 1972 限於公司產品線；`c180505`／`c180507` 明說芬蘭／美國由公司年報記載；`c180517` 明說登記文件無法證明橘色造成銷量。上述方向可保留。
- 沒有實測 TTS：正文 ≥480 秒與插圖時間 ≥70% 仍待各自量測。兩位真正只讀旁白的盲讀、站主劇本核准、整支報價與付費批准都仍是後續獨立關卡；本收據不跨過任何一關。
