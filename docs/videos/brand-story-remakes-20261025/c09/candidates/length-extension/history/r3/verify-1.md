# C09 Patagonia｜長度增補候選 r3 獨立來源與書面配鏡查核

查核日：2026-10-25。查核者：`/root/c04_readiness`。本代理曾翻譯C09基底PT／ID，未撰寫中文基底或長度增補稿；先前翻譯自校不作來源批准。未讀或判定blind／narrative投票檔。

**結論：SOURCE PASS／WRITTEN VISUAL PASS；原生完整情境mechanical lint為0 errors。** 僅適用以下精確候選r3的116句、114景及書面結構；不是owner、實際時長、媒體或字典讀音批准。原r2來源PASS與mechanical HOLD均保留在history/r2，未改寫。

## 綁定輸入

| 檔案 | SHA-256 |
| --- | --- |
| video.json | `8c5372ff05c00e1b0f1ec3c0da57bf038ccda1d880a4cb03f4af2e9e539532f1` |
| script.md | `a229e4672bc208df3478db2a357e446f797d7431e635741a3acdc9c8bbb8fc55` |
| narration-only.json | `2659eb74072eff48b707ed85596d84f34fc0e55877fca1afcfe63d6ca3736876` |
| claims.json | `235a6cf12ad18bdffd196d45b1691bbaca8f888b191957cae4f427cde4e24159` |
| brief.md | `5eaf102ca8d913cd9e09f39a5f38cbda247da45c6e1cc4cf6276969ea4ccf69a` |
| series.json | `3cf3abd89411bfb22f0026fca30cfae009741843b829ce2dc20f13d6a9e06bdd` |
| reviews/source-r3-independent.json | `f8edf98a6ff1f157266c13dad1b8ca3969b212dfb48f5f6b429d65b6012ff48f` |

本目錄script.md為作者查核稿。原生純函數`screenplay(JSON.parse(video.json))`的UTF-8投影SHA-256實算為`cc719ed726c44fdca30b2368e00d2e526604d83849cf0785b1140916ea1ef153`（16554 bytes）；只計算，未寫入正式canonical或授予劇本核准。claims作者PENDING欄位未改。

## 精確差分與來源界線

- r2四份主輸入與四份支援輸入SHA、來源收據、舊verify及原mechanical四錯誤記錄均與history/r2相符；原r2來源收據SHA為`eaca4bfb38cbf557b2bfe183bf67334fbbc0dd9e2e321fb8e3c3692488c29b33`，原verify SHA為`e7ade83ed8c1cddef73bfd7b0b7787d396a8b5ead7c5131287b038b5bcb75681`。五組原件及段落快取、12份基底來源鏈與基底輸入／收據bytes也已重新驗綁。
- r3將原le015拆成le015的書評、東岸流傳與年長作者歸屬，以及緊接的le022原有批評；114句保留文字未改，沒有刪句。其餘video頂層、全部113個保留景的data及14組loops未改；新增景le022緊接le015，28個loop端點均有效，le017仍已刪除。
- S3 paragraph007原HTML抽文與段落快取逐字一致。原HTML SHA：`5e650b687a3c1d2d22905fe453b72b7fd059e3f02a7eb149e2f349553b2fd498`；段落文字SHA：`238447e2201fedb0eac6a89092885304e824904642fc47cbea27246139f3fb65`。
- 「那位作者」緊承le015的年長文字作者；「東岸」只限定文字廣為流傳的地點，不指定作者出身或住處。批評仍由Rowell書評引述，非Rowell本人或公司自白；沒有恢復「盡是」絕對化，也沒有新增因果或財務動機。
- le015仍是匿名年長讀者看空白冊子的概念鏡頭；le022是匿名年長讀者指向空白冊子、旁有合上的錢包。錢包只作負擔得起與否的概念物件，不指真實作者、交易、財務情況或可讀史料。其餘112個完整景物件精確未改；116句、114景均PASS。
- video、旁白投影、作者稿、claims及來源表的116筆ID／文字／順序／來源映射一致；28筆候選錨點hash均實核。S1具名1967器材文章、S2原1972前言、S3於1973刊出的書評、S4於1977刊出的採訪、S7於2012刊出的品牌回顧仍保持文件時層。1972少用不是停售，1977不是確認到訪年；服裝收入不是利潤，模具回本仍為當事人估算。

## 原生機械檢查

本次以唯讀loadProject載入目前BASE canonical（video SHA `875eaca7ba51de28a9e2a198dfd8070325aabec91b58bb7cb903731415fb233a`、script SHA `0547060346e7d6194d9bd096bcc19bb4e0166dde28fd292543ff3f047cf216d1`），保留已初始化293詞字典、translations及其他情境，只在記憶體替換候選doc、brief與series，呼叫原生lintProject。0 errors，65 warnings仍保留為警告，不作敘事或語言批准。
brief的問題、一句答案、站主觀點均為非空獨立二級標題，唯一選項為A；核心問答與觀點未改。原生分鏡估算le015為8.933秒、le022為6.3秒，解除原r2單景13.267秒超過12秒的機械錯誤。這些是TTS前估算，不是實際音訊、正文時長或13分鐘目標已過。機械檢查快取與SHA列於source-r3獨立收據。

## 逐句來源結果

下表全為已綁定r3收據的SOURCE PASS。CONFIRMED指證據支持有限表述；ATTRIBUTED保留文章、回憶、書評、採訪或品牌回顧的歸屬；PLAN是明示假想、問句、旁白反應、回收或CTA，不把它當史實。舊表類型保留，新增le022為ATTRIBUTED。無未解除來源HOLD或現稿NOT FOUND句。

| 句ID | 結果 | 證據代號 |
| --- | --- | --- |
| c09r001 | ATTRIBUTED | S1 |
| c09r002 | PLAN | S2、S4 |
| c09r003 | PLAN | S2 |
| c09r004 | CONFIRMED | S2 |
| c09r005 | PLAN | S3、S4 |
| c09r006 | PLAN | S1–S4 |
| c09r007 | PLAN | S2、S4 |
| c09r008 | PLAN | S4 |
| c09r009 | ATTRIBUTED | S4 |
| c09le001 | ATTRIBUTED | S4 |
| c09r010 | ATTRIBUTED | S4 |
| c09r011 | PLAN | S4 |
| c09r012 | ATTRIBUTED | S4 |
| c09r013 | ATTRIBUTED | S4 |
| c09le002 | ATTRIBUTED | S4 |
| c09le003 | ATTRIBUTED | S4 |
| c09r014 | ATTRIBUTED | S4 |
| c09r015 | ATTRIBUTED | S4 |
| c09r016 | ATTRIBUTED | S4 |
| c09r017 | ATTRIBUTED | S4 |
| c09r018 | PLAN | S4 |
| c09r040 | ATTRIBUTED | S4 |
| c09le004 | ATTRIBUTED | S4 |
| c09le005 | ATTRIBUTED | S4 |
| c09r041 | CONFIRMED | S2、S4 |
| c09r043 | ATTRIBUTED | S4 |
| c09r019 | ATTRIBUTED | S4 |
| c09r020 | ATTRIBUTED | S4 |
| c09r021 | ATTRIBUTED | S4 |
| c09r022 | ATTRIBUTED | S4 |
| c09r023 | ATTRIBUTED | S4 |
| c09r024 | ATTRIBUTED | S4 |
| c09r025 | CONFIRMED | S1、S4 |
| c09r026 | CONFIRMED | S1 |
| c09r027 | CONFIRMED | S1 |
| c09le006 | ATTRIBUTED | S1 |
| c09r029 | ATTRIBUTED | S1 |
| c09le007 | ATTRIBUTED | S1 |
| c09le008 | ATTRIBUTED | S1 |
| c09le009 | ATTRIBUTED | S1 |
| c09le010 | ATTRIBUTED | S1 |
| c09r030 | ATTRIBUTED | S1 |
| c09r044 | ATTRIBUTED | S4 |
| c09r045 | ATTRIBUTED | S4 |
| c09r031 | CONFIRMED | S1、S2 |
| c09r032 | CONFIRMED | S2 |
| c09r033 | ATTRIBUTED | S2 |
| c09r034 | ATTRIBUTED | S2、S4 |
| c09r035 | PLAN | S2、S4 |
| c09r036 | PLAN | S2、S4 |
| c09r037 | ATTRIBUTED | S4 |
| c09le011 | ATTRIBUTED | S1 |
| c09r038 | PLAN | S2 |
| c09r039 | PLAN | S2、S4 |
| c09r042 | PLAN | S2 |
| c09r046 | ATTRIBUTED | S4 |
| c09r047 | ATTRIBUTED | S2 |
| c09r048 | ATTRIBUTED | S2 |
| c09r049 | ATTRIBUTED | S2 |
| c09r050 | ATTRIBUTED | S2 |
| c09r051 | PLAN | S2 |
| c09r052 | PLAN | S2、S3 |
| c09r053 | ATTRIBUTED | S2、S3 |
| c09r054 | ATTRIBUTED | S2 |
| c09r055 | ATTRIBUTED | S2 |
| c09r056 | ATTRIBUTED | S2 |
| c09r057 | ATTRIBUTED | S2 |
| c09r058 | PLAN | S2、S3 |
| c09r060 | ATTRIBUTED | S2、S3 |
| c09r061 | ATTRIBUTED | S2、S3 |
| c09le012 | ATTRIBUTED | S4 |
| c09le013 | ATTRIBUTED | S4 |
| c09le014 | ATTRIBUTED | S4 |
| c09r062 | ATTRIBUTED | S3、S4 |
| c09r063 | ATTRIBUTED | S3、S4 |
| c09r064 | PLAN | S3 |
| c09r065 | ATTRIBUTED | S2 |
| c09r068 | PLAN | S2、S3 |
| c09r069 | PLAN | S2、S3 |
| c09r070 | PLAN | S3 |
| c09r071 | ATTRIBUTED | S3 |
| c09r072 | ATTRIBUTED | S3 |
| c09r073 | ATTRIBUTED | S3 |
| c09r074 | ATTRIBUTED | S3 |
| c09le015 | ATTRIBUTED | S3 |
| c09le022 | ATTRIBUTED | S3 |
| c09le016 | ATTRIBUTED | S3 |
| c09r075 | PLAN | S3 |
| c09r076 | ATTRIBUTED | S3 |
| c09r077 | ATTRIBUTED | S3 |
| c09r078 | PLAN | S3、S4 |
| c09r079 | ATTRIBUTED | S4 |
| c09r080 | ATTRIBUTED | S4 |
| c09r082 | PLAN | S4 |
| c09r093 | ATTRIBUTED | S7 |
| c09r084 | PLAN | S2、S4 |
| c09r085 | ATTRIBUTED | S4 |
| c09r086 | ATTRIBUTED | S4 |
| c09r087 | ATTRIBUTED | S4 |
| c09r088 | ATTRIBUTED | S4 |
| c09r089 | ATTRIBUTED | S4 |
| c09le018 | ATTRIBUTED | S4 |
| c09r090 | ATTRIBUTED | S4 |
| c09le019 | ATTRIBUTED | S4 |
| c09r091 | ATTRIBUTED | S4 |
| c09le020 | ATTRIBUTED | S4 |
| c09le021 | ATTRIBUTED | S4 |
| c09r092 | PLAN | S4 |
| c09r095 | ATTRIBUTED | S4 |
| c09r096 | ATTRIBUTED | S4 |
| c09r097 | ATTRIBUTED | S4 |
| c09r098 | ATTRIBUTED | S4 |
| c09r100 | PLAN | S2、S4 |
| c09r102 | PLAN | S2、S4 |
| c09r103 | PLAN | S2、S3 |
| c09r104 | PLAN | 編輯 |

## 範圍限制

本檔不授予owner／預算核准、付費啟用、正式canonical採用、字典念法、實際旁白時長、13分鐘目標、鉤子實際秒數、TTS、音訊、生成圖、字幕時間、素材沿用、clean配音資格、媒體QA、打包或發布批准。未讀、重判或使用blind／narrative投票代替來源；未將lint估算當實測。

本次只新增r3獨立收據及此候選verify檔；未改BASE、canonical、中文文案、字典、history、舊收據、Git、provider或後台。
