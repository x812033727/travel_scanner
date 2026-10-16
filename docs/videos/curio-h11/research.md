# H11 伏尼契手稿：研究更新

- 查核日：2026-10-16（Asia/Taipei）；基準 `a77a9416d`。
- 舊題庫唯讀參考：`949bb91fc85d41a53633d056062b27d87651e9d5:docs/videos/history-curiosity/topic-checks/H11.md`。本次不沿用舊「checked」代替新查核。
- 狀態：**原大綱與補格式版大綱均已讀回 A 核准，每集 US$6／五集 US$30 估算停手上限已授權。正式劇本為本機草稿，待獨立史料與十三題覆核、站主劇本核准；未啟動付費製作。**。正式劇本已在本機起草，尚未獨立核准。
- 手動請求使用 `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`。下列「已讀」指取得並閱讀相應正文，不是只看到 HTTP 成功或搜尋標題。

## 來源登錄與實際存取

| ID | 來源與網址 | 本次實際結果 | 支持範圍／限制 |
| --- | --- | --- | --- |
| H11-S01 | Beinecke Library，[現行館藏介紹](https://beinecke.library.yale.edu/beinecke/collections/beinecke-cipher-voynich-manuscript) | 正文已讀；HTTP 200。舊 highlights 網址轉往此頁。 | 館藏、1912 年購藏及 1969 年進 Yale 的沿革、未知文字與插圖類型。頁面仍有晚 15／16 世紀的描述；不能拿它抹去材料檢測結果。館方也不替所有民間解讀主張逐件背書。 |
| H11-S02 | Beinecke，[MS 408 舊館藏目錄](https://pre1600ms.beinecke.library.yale.edu/docs/pre1600.ms408.htm) | 正文已讀；HTTP 200 | 102 葉羊皮紙、含折頁等書目資料。舊植物辨識與作者／年代推測不採用；不要把一葉當一頁。 |
| H11-S03 | University of Arizona 供稿、Daniel Stolte，[2011 年定年報導的 Phys.org 刊載版](https://phys.org/news/2011-02-experts-age.html) | 正文已讀；HTTP 200，署名及 Provided by University of Arizona 可見 | 2009 年定年工作、羊皮紙 1404–1438 年的結果，並區別材料與墨水的測定。這是大學供稿的刊載版，不是假稱原站仍可開，也不是本次親讀完整實驗報告；不把取樣的確切日期另行定案。 |
| H11-S04 | Montemurro／Zanette，[2013 年統計研究](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0066344)，PLOS ONE | 摘要、正文與結論已讀；HTTP 200 | 作者從長距離字詞分布主張有與語言相符的組織性；不是提出逐字翻譯或確定語種。 |
| H11-S05 | University of Bristol，[2019-05-16 聲明](https://www.bristol.ac.uk/news/2019/may/voynich-manuscript.html) | 正文已讀；HTTP 200 | 校方前一天發布相關解讀研究消息，收到專業疑慮後撤下新聞稿，待進一步驗證。**新聞稿撤下不等於期刊論文撤稿**。 |
| H11-S06 | Lisa Fagin Davis，[2024-09-08 多光譜研究者紀錄](https://manuscriptroadtrip.wordpress.com/2024/09/08/multispectral-imaging-and-the-voynich-manuscript/) | 正文已讀；HTTP 200 | 2014 年拍攝的十頁影像於 2024 年完整公開；早前已有部分細節發表。首頁邊緣三欄字母與可能的 Marci 筆跡是作者研究解讀，非全體學界定論，也不是全文密鑰。 |
| H11-S07 | Yale News，[2025-02-21 研究介紹](https://news.yale.edu/2025/02/21/deciphering-mysterious-manuscript) | 正文已讀；HTTP 200 | Claire Bowern 介紹語言與抄寫研究，提到辨認出五名抄寫者；正文意義仍未確定。本次沒有獨立重做筆跡分類，不把五名抄寫者改成五名已知姓名的作者。 |
| H11-S08 | Michael A. Greshko，[2025 年 Naibbe 論文](https://www.tandfonline.com/doi/full/10.1080/01611194.2025.2566408) | 搜尋索引可讀摘要／導言；正文開啟失敗，手動 HTTP 403 | **沒有完整論文閱讀收據**。僅以索引定位研究，模型描述另以 S09 作者 README 核對；不聲稱本次已重現其統計或逐表審閱。 |
| H11-S09 | Greshko，[作者程式庫](https://github.com/greshko/naibbe-cipher)及[實際取得的 README](https://raw.githubusercontent.com/greshko/naibbe-cipher/main/README.md) | GitHub 網頁工具開啟失敗；raw README 手動 HTTP 200，全文已讀 | 作者描述能以拉丁文／義大利文產生多項統計特徵相似的可解密文本；此模型不是把 MS 408 原文翻譯出來。這次沒有執行程式或測試論文數值。 |

### 開啟失敗，不能當成本次已驗證的來源

| 網址 | 本次結果 | 處理 |
| --- | --- | --- |
| [University of Arizona 原始新聞網址](https://news.arizona.edu/story/ua-experts-determine-age-of-book-nobody-can-read) | 原站 HTTP 404／工具無法開正文 | 改讀大學供稿的 S03 刊載版，明示來源身分。 |
| [Yale 數位掃描館藏](https://collections.library.yale.edu/catalog/2002046) | 網頁工具 403；手動 HTTP 202 但正文空白 | 未宣稱逐頁檢視原掃描；書目資料用 S01／S02。影片若要使用照片仍須再取圖及查權利。 |
| [NSA 的 Voynich PDF](https://www.nsa.gov/portals/75/documents/about/cryptologic-heritage/historical-figures-publications/publications/misc/voynich_manuscript.pdf) | 網頁工具因約 25 MB 檔案限制失敗；手動 HTTP 403 | 未讀完整 PDF；Friedman／1944 年密碼小組細節不進這次大綱，也不採舊標題「連二戰高手都讀不出一個字」。 |

## 必須分開的結論

1. **羊皮紙年代與書寫年代**：S03 給的是材料的放射性碳定年。不能直接改寫成「文字證實寫於 1404–1438」；S01 的舊書目年代也不能推翻檢測對象不同的結果。
2. **未知文字與完全沒有可讀字**：正文的系統未確定，不代表頁邊所有拉丁字母、後加註記或人名都不可辨認。因此題目不承諾「一個字都沒人懂」。
3. **規律與翻譯**：S04 是統計推論；S09 是可產生相似特徵的模型。兩者都沒有直接讀出原稿的意思，彼此也不能簡化成誰徹底推翻誰。
4. **新聞稿與論文**：Bristol 撤下的是新聞報導，不能變成「論文遭撤稿」「作者造假」。本集呈現校方修正訊息的事件，不評斷研究者人格。
5. **新影像與密鑰**：S06 顯露的是物件與閱讀史的線索；Marci 的筆跡比對屬研究者提出的判讀。三欄字母不等於原作者解碼表。
6. **五名抄寫者與五名作者**：S07 可支持研究者辨識多種筆跡；不能推到五人的姓名、分工、動機或每人發明一種語言。

## 更新範圍

- 新納入 2024 年多光譜影像、2025 年 Yale 研究介紹與 Naibbe 作者資料，使本集不止停在 2019 年新聞事件。
- 截至 2026-10-16，本次打開的館方及研究者來源沒有提供可把全文連續讀出的公認結果。這是本次來源範圍，不是宣稱查遍所有 2026 年出版品。
- 2025 年 Naibbe 論文正文尚未取得；若正式劇本需要超出 README 的實驗細節，必須先取得全文，否則維持「作者提出的生成模型」這個範圍。
- 皇帝購買價格、Roger Bacon、John Dee 等早期歸屬說法來源間有歷史推測差異；本案不靠這些支線製造神祕感。

## 圖像與人物規則

- `look: { "preset": "cute-mystery" }`；MiniMax `image-01` 原創插圖，至少 70%，連續卡片最多 3 張。紙上文字由後製加入，插畫不生成可讀古文或假譯文。
- Wilfrid Voynich（1930 年去世）已超過 70 年，可依外觀描述畫歷史卡通；Marci 等若選用也需核對年代與身分。提示詞不用人名。
- Bowern、Davis、Greshko 及現代研究人員不畫本人；用無指涉的研究職務角色、操作儀器的手部及書頁物件，不能假配其原話。
- 本次未核准任何照片為公有領域。網頁、MSI 檔案可下載、要求署名或程式碼授權，都不自動符合系列的照片規則；若用照片須另外逐張查證。
- 所有物理操作只作內容插畫，不是請觀眾自行對古書施藥或取樣的教學。取樣由專業館藏與實驗室人員處理。

## 覆核與後續

- 已完成大綱層級的主張與來源取得層級獨立覆核，包含 S03 刊載版、S06 作者初步判讀、S08 未取得全文；不代替正式劇本十三題審核。
- A／B 均不承諾本集破解未知語言；正式劇本前再刷新館方及新研究消息。

## 正式稿刷新與證據範圍（2026-10-16）

S03 大學供稿、S04 原論文、S06 研究者紀錄、S09 作者 README 再次取得並閱讀。正式稿新加入比較文本及 f.70v1 背面透字個案，逐句對應 C16、C17。S08 受限全文未新增取得；仍未執行 Naibbe 模型，模型流程圖只能標作者所提做法示意，不可放偽造的實測輸出。

核准與費用依 [batch decision](../curio-next-five-20261016/decision-20261016.json)。新版大綱雜湊已核准（[收據](../curio-next-five-20261016/format-decision-20261016.json)）；劇本／配音／圖像／交付審核分開。

## 第 1 輪敘事修訂查核

重新開啟 S04 原論文，讀到 Introduction 的轉寫敘述、Results 與 Methods 的等長分段／分布信息量做法。新增 C18 仍據已讀 S03，C19 據已讀 S06，徒手材料限制據已讀 S09；沒有把受限 S08 全文補稱已讀。獨立盲評第一輪未過；此處只記作者修訂，等待重新獨立覆核。
