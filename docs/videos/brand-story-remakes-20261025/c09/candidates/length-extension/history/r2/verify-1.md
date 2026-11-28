# C09 Patagonia｜長度增補候選 r2 獨立來源與書面配鏡查核

查核日：2026-10-25。查核者：`/root/c04_readiness`。本代理曾翻譯C09基底的PT／ID文字，也曾覆核其他語言；未撰寫中文基底或本長度增補稿。先前翻譯自校不作本次獨立來源證據；未讀或重判盲審／panel檔。

**結論：SOURCE PASS／WRITTEN VISUAL PASS。** 僅限下列精確候選r2輸入的115句及113景書面配鏡；不是正式採用或任何owner、片長、媒體、讀音關卡的批准。逐句與逐景完整結果保存在已綁定的獨立r2收據。

## 綁定輸入

| 檔案 | SHA-256 |
| --- | --- |
| video.json | `20e8fba7edd635d998465713223258cbf35159229c7a32af64c9b978a006b9d7` |
| script.md | `bb67306d4d7ee52f70ea7cc074a9c0137f98cccd73f7563f502309218db10c80` |
| narration-only.json | `fa1281f556f80c62510ee622c2faea80e18dd910354767da06ef352c43bd488a` |
| claims.json | `d70f43ecc30e6b45c5cdd229f63c72e2a2c934b8a9cfdc0c5bcb99a9934af22c` |
| reviews/source-r2-independent.json | `eaca4bfb38cbf557b2bfe183bf67334fbbc0dd9e2e321fb8e3c3692488c29b33` |

本目錄`script.md`是作者查核稿。另以原生純函數`screenplay(JSON.parse(video.json))`計算的UTF-8投影SHA-256為`641ffead66e0a4ab726965812e0e6d83881b67dc8397bc0f2739a17044646f77`（16505 bytes）。本次只計算，未寫入或批准正式canonical劇本。`claims.json`的作者PENDING標記未被修改；本檔與所綁獨立收據記錄來源查核結論。

## 接鏈與原件

| 獨立收據 | SHA-256 | 保留判定 |
| --- | --- | --- |
| history/r1/reviews/source-r1-independent.json | `cd9b53c9fd0c431c7dffe45e0ffb9600cb729a7671d950aa603f6f6f3c36c170` | r1共116句，115句來源PASS、le015來源HOLD；114景書面配鏡PASS。原HOLD原樣保留。 |
| reviews/source-r2-independent.json | `eaca4bfb38cbf557b2bfe183bf67334fbbc0dd9e2e321fb8e3c3692488c29b33` | r2共115句來源PASS、113景書面配鏡PASS；114句精確未改內容沿已驗綁定的r1 PASS，le015重新直接核原文。 |

r1四份主要輸入、四份支援輸入、12份基底來源鏈收據、五組原件HTML與段落快取，以及四份基底輸入和兩份基底收據的實際SHA均已與r1來源報告逐一核對。其餘未改主張承接的是精確來源證據，不沿用舊敘事、owner或片長判定。本輪未聲稱重新開網頁；重新讀取了保留的原件與快取。

來源代號及文件層次：

- S1：Chouinard／Frost，1967年具名器材文章。原件支持當時器材使用、攜帶、敲拔、回收與疲勞裂紋等有限敘述。
- S2：1972年型錄前言的全文重刊。以原前言的合適路線、優先試可拆楔塊、必要時固定岩釘及記入地方指南等條件為準，不寫成全面停售。
- S3：Galen A. Rowell的1973年型錄書評。書評引述的批評、作者觀察與其辯護立場各自保留；不轉成公司內部承認的動機。
- S4：Bernstein於1977年刊出的採訪。1977僅為刊年，未確認實際到訪年份；1973攀登、器材型錄規格及工廠所見保持各自時層。服裝收入不是利潤，模具費用與有時5至10年回本仍為當事人估算。
- S7：Patagonia於2012年所刊公司史回顧。1973服裝標籤的說法保留品牌回顧歸屬，不挪成更早的器材公司名稱。

原件URL在`video.json`；快取位置、原件bytes／SHA與27筆候選證據錨點的實核結果都列於獨立r2收據。

## r2差分與書面配鏡

- 全video物件只改le015旁白文字，並整景刪除le017；沒有新增句子或場景。旁白投影、作者稿、claims及來源表均同步，115筆ID／文字／順序／來源映射一致。
- le015改為「在東岸廣為流傳、由年長攀岩者寫的文字」，把地點限定於文字流傳，未指定作者出身或住處；移除「盡是」，保留經書評引述的「買不起的器材」與「不需要的說教」。
- S3原HTML獨立抽出的paragraph007與段落快取、r1錨點一致；段落文字SHA為`238447e2201fedb0eac6a89092885304e824904642fc47cbea27246139f3fb65`，原HTML SHA為`5e650b687a3c1d2d22905fe453b72b7fd059e3f02a7eb149e2f349553b2fd498`。該段支持反彈不只來自年輕人、東岸流傳的文字與年長作者，沒有支持東岸作者身分或全部內容皆如此的絕對量詞。
- le015仍是匿名年長讀者在通用書桌看空白冊子的概念圖；不重建真人、東岸現場、可讀歷史文字或真實事件。
- le017的圖書／帳篷／睡袋句及對應場景已從五份現行文字／映射輸入移除；這是編輯刪除，不改寫它在r1原有的來源PASS。
- 112個保留場景完整物件未改，le015場景僅旁白文字改動；113景的data／prompt／camera／visual均與r1保留項一致。當前112張插圖提示與一景片尾的書面配鏡全部PASS。
- 14組loops物件不變，28個端點均指向當前句ID；沒有已刪句或景的懸空引用。來源清單保留S4，其他現行主張仍使用它。未檢視任何生成影格或成片manifest。

## 逐句來源結果

下表全為已綁定r2收據的SOURCE PASS。CONFIRMED指證據支持有限表述；ATTRIBUTED指保留文章／回憶／書評／報導／品牌回顧的說話者與界線；PLAN是明示假想、問句、旁白反應、回收或CTA，不把它當成已發生的史實。混合句的意見仍是旁白意見。沒有未解除來源HOLD或現稿NOT FOUND句；以下不代表TTS、圖片、音軌或敘事批准。

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

本檔只證明綁定候選的來源與書面配鏡，不授予owner核准、預算核准、付費啟用或正式canonical採用。未驗證實際旁白時長、13分鐘目標、鉤子實際秒數、TTS、字典或外語讀音、音訊、生成圖、字幕時間、費用、素材沿用、clean配音資格、媒體QA、打包或發布。未用panel結果代替來源，也未重判兩位讀者。正式企劃與劇本應在root採用後依各自精確雜湊另送原生關卡。

本次只新增這份候選查核檔；未修改source、history、字典、正式canonical、原始收據、Git、provider或後台。
