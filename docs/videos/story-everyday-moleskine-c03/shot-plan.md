# C03 Moleskine｜插畫、剪點與全片成本前檢

狀態：**已產圖、待畫面重組**。20 段稿有 94 句；現有 TTS 時間軸含停頓約 609 秒，其中 02–20 段純語音 481.25 秒。本表原本的各章時間仍是拍攝前分配，實際剪點須以時間軸為準。81 個插畫景已完成付費嘗試；逐圖審查後，本版 `video.json` 改為 67 張插畫、27 張本機字卡，尚未完成字卡渲染或成片驗收。媒體帳目與停線見[製作前報價及增補](production-quote.md)。

## 故事與畫面界線

本集追問「1997 年才成立的品牌，怎麼讓一種更早存在的無名筆記本變成全球商品？」六章依 `hook → origin → idea → engine → turn → now` 推進。[品牌自己的倫理文件](https://www.moleskine.com/en-no/code-of-ethics.html)明列 1997 年品牌成立、2007 年公司取得 Moleskine 名稱；[D’Ieteren 2017 簡報第 31–38 頁](https://dieterengroup.imgix.net/documents/presentations/general_presentation_april_2017_0.pdf)提供創業、產品與通路節點；[D’Ieteren 2025 全年業績](https://dieterengroup.imgix.net/press-releases/20260310_FY-2025-Results_EN_FV.pdf)及[2026 上半年業績第 9 頁](https://dieterengroup.imgix.net/press-releases/20260909_Press-release_H1-2026-results_EN_FV-with-appendix.pdf)供當代營運章使用。這些是分鏡取證入口，仍需由另一位查核者逐項核定最終稿件。

歷史人物使用過的是**相似的無牌筆記本形式**，不是 1997 年後的 Moleskine 商品；不畫梵谷、畢卡索、海明威、Bruce Chatwin 的肖像或近似造型。[品牌 heritage 頁](https://www.moleskine.co.jp/en-jp/the-world-of-moleskine/our-heritage/)轉述 Chatwin 在《The Songlines》談 1986 年法國製造商關閉的故事；該段若入旁白須歸給品牌所轉述的 Chatwin，插畫僅作閱讀與購書情境示意，不重建法國工廠、店主或他的旅程。2025 年品牌資產減值是會計估值，不畫成消費者棄用或公司倒閉；2026 上半年銷售回升也不畫成已全面復甦。

## 正文鏡頭容量

所有正文插畫為 `visual: "still"`，MiniMax `image-01`，`look: {"preset":"cute-mystery"}`；不添加 `style` 或 `negative`。插畫搭配緩慢推近、橫移或停留；生成影片 clip **0 張**。開場濃縮後放既定 5 秒片頭，正文末三句之後接既定 21 秒片尾；兩者不算下表正文時長，也不拿來補足至少 8 分鐘的旁白。

| 章 | 原估正文時間 | 插畫 | 後製字卡 | 可畫的動作、伏筆與來源界線 |
| --- | ---: | ---: | ---: | --- |
| 1 `hook`：一部「古老」筆記本上市 | 0:40 | 4 | 2 | 一位匿名逛書店的人拿起素面黑色筆記本；上市日期與歷史線索用來源字卡，不畫真實股票代號或會場。 |
| 2 `origin`：一本書留下的空缺 | 1:25 | 6 | 6 | 匿名讀者與旅人的插畫保留；舊本外形、1995 年再製與商標前的提問改用字卡，不把 1986 年的 Tours 工廠畫成目擊實錄。 |
| 3 `idea`：空白本成為「待寫的書」 | 1:43 | 12 | 4 | 書店與批發貨架的插畫保留；書店定位、2005／2010 批發據點與補貨風險分別標明來源或編輯示意。批發據點不是自營門市。 |
| 4 `engine`：名字與通路變成投資標的 | 2:21 | 19 | 3 | 匿名會議室與通路插畫保留；2007 年公司名、後續商品延伸、2013 年上市市值及 2016 年直營店數分別呈現，不重建真實交易。 |
| 5 `turn`：新主人接下通路成本 | 1:55 | 12 | 6 | 汽車業務、商品擴張與直營成本改以字卡呈現；2016 年簽約、2017 年完成及下市、紙本銷售占 81% 各用其正確時間與口徑。 |
| 6 `now`：故事要繼續被買單 | 2:08 | 14 | 6 | 保留符合語意的素面本與貨架插畫；2025 年減損的非現金性質、2026 上半年營業結果和結尾的產品／通路推論用字卡，不以空店或熱賣景暗示來源沒說的結果。 |
| **合計** | **原估 10:12；TTS 時間軸約 10:09** | **67** | **27** | **94 個場景，插畫 71.3%；最長連續字卡 2 張。** |

本版保留 **67 張**插畫和 27 張字卡，插畫占 67／94＝71.3%，高於至少 70% 的畫面要求；最長連續字卡 2 張，低於最多 3 張的限制。這是 14 張已生成圖出現錯誤物件、假文字／標誌、人體異常或多次評審失敗後的局部改版，原圖與帳本仍保存。旁白、21 條懸念回收與語音時間軸未改；字卡渲染、聯絡表視覺檢查和最終節奏仍須驗收。

## 給圖片模型的構圖示例

畫風只由 `look` 指定；每個 prompt 只寫景別、時地、**一位匿名人物做一件事**、焦點與中性光線。人物正面或四分之三側面，不借歷史人物容貌。下列文字不送入姓名、品牌名、商標、年份、可讀文件、標誌、`cartoon` 等風格詞；時間、名稱、來源、數字均留給後製卡。插畫是內容示意，不是檔案照片或真實現場重建。

| 章 | `image-01` prompt 示例 |
| --- | --- |
| `hook` | `Medium shot in a generic bookshop, one anonymous customer facing three quarters toward camera while lifting a plain black pocket notebook from a shelf, blank book spines around it, soft ceiling light.` |
| `origin` | `Medium shot at a simple reading table, one anonymous traveler facing camera while turning a page in an unmarked book, a plain closed pocket notebook nearby, diffuse window light from the left.` |
| `idea` | `Medium shot in a modest design workroom, one anonymous maker facing camera while comparing a plain black notebook with an unmarked paper sample, a clear tabletop, soft overcast window light.` |
| `engine` | `Wide shot in a generic station bookshop, one anonymous shopkeeper placing a stack of plain pocket notebooks on a low shelf, blank signs, soft overhead light.` |
| `turn` | `Medium shot in a small stationery shop, one anonymous employee facing camera while arranging plain notebooks beside unmarked writing tools, blank display panels, neutral lamp light.` |
| `now` | `Medium shot in a modern generic bookshop, one anonymous customer facing camera while opening a plain notebook to empty pages, a modest shelf of notebooks behind, soft ceiling light.` |

逐鏡表要交錯遠、中、近景，以及室內、戶外與少量夜景；同一運鏡不得連續三張。圖像評審通過後，只因與旁白矛盾、假可讀文字／商標、人物解剖錯誤或照片／3D／油畫／黑邊等漂移而重畫。遇到三次仍失敗的景，先簡化動作或重用同章且語意相符的已過圖；不能大量改成卡片而失去插畫比例。

## US$25 整片停線的原始預算

下表保留**拍攝前 83 景／每景最多三次**的原核准預算，不是目前待生成張數或實際帳單。圖片單次 US$0.0035、圖片評審單次 US$0.01 是當時前檢使用的目錄單價；實際支出以媒體帳本和[報價增補](production-quote.md)為準。已過圖片必須重用，不因局部修訂重買全片。

| 項目 | 暫定最壞範圍 | US$ 預留上限 |
| --- | --- | ---: |
| MiniMax 插畫 | 249 次 × 0.0035，向上取整 | 0.88 |
| 圖片評審 | 249 次 × 0.01 | 2.49 |
| 無人聲配樂 | 一首；正文建議 `light, curious, a little mysterious, no vocals`，`gain_db: -20`、`duck_db: -10` | 0.08 |
| 台灣口音旁白、必要的局部重錄、轉錄與聽核 | 以定稿字數／正式服務報價重新核算；不可假定免費 | 2.50 |
| 撰稿、逐來源查核、敘事盲評及其他文字模型 | 只為未通過的章節局部重做；正式 token 價格待查 | 9.00 |
| 未拆帳費、失敗呼叫與價格變動 | 未知結果先停並對帳，不盲重送 | 10.05 |
| **整片預留合計** | **本片全部付費項目不得超過 US$25** | **25.00** |

正式版開畫之前，先凍結稿件與鏡頭、取得本集整批張數和 `tts`／`keyframes`／`music` 乾跑、核對實際帳本、供應商餘額及可重試上限，再讓站主一次核准整片。若服務不提供文字／語音的可控美元上限，預留金額就只是停止條件，不能當成本保證。每次付費請求前以「已花＋待結算＋下一次最壞費用」核對 US$25；超額、餘額不明或先前付費結果不明就停止。概念片頭片尾不算正式品牌素材；聲音、插畫、最終成片、字幕、站主看片、私人上傳及 Studio 片尾可點元素分別驗收。
