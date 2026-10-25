# C09 Patagonia｜長度增補候選 r4 獨立來源與書面配鏡查核

查核日：2026-10-25。查核者：`/root/c04_readiness`。本代理曾翻譯C09基底PT／ID，未撰寫中文基底或長度增補稿；先前翻譯自校不作來源批准。未讀或判定blind／narrative投票檔。

**結論：SOURCE PASS／WRITTEN VISUAL PASS。** 本版是精確純刪除差分：114句及112景全部承接已驗綁定的r3 PASS。唯讀完整情境native lint為0 errors、63 warnings；這些都不是owner、實際語音時長、媒體或字典讀音批准。

## 綁定輸入

| 檔案 | SHA-256 |
| --- | --- |
| video.json | `8fc4ada68f086f68532f3c317606018273f9d291885e2833795bfc14efab1aad` |
| script.md | `f9cae91c7b169ef557eefcf7f9568414a175f4b440d05d193f5e5be70a36e533` |
| narration-only.json | `f13a4111a9c320ac3670e3acc0f11498babe514bafc00cab60c22b29013dba31` |
| claims.json | `181c1a6440b2c65fe7b5bcd54ccca0870c4d5341b0df7566cb4eba3802b5b999` |
| brief.md | `30a02deddc6ddce34ce62ea08399c7a1c6fb0530fbfc3bc29f86105212bba6f2` |
| series.json | `3cf3abd89411bfb22f0026fca30cfae009741843b829ce2dc20f13d6a9e06bdd` |
| reviews/source-r4-independent.json | `9dfa60def21cfd1898a17bf8047173e306597f0e372cff50aec6df42c8f5885d` |

本目錄script.md為作者查核稿。原生純函數`screenplay(JSON.parse(video.json))`的UTF-8投影SHA-256實算為`cdeede0df739f2b0e258da5cd351a218327d412b65309c0a80ed0f9a8b6a9822`（16225 bytes）；只計算，未寫入正式canonical或授予劇本核准。claims作者PENDING欄位未改。

## 純刪除差分與接鏈

- r3來源收據在history/r3原樣保留，SHA為`f8edf98a6ff1f157266c13dad1b8ca3969b212dfb48f5f6b429d65b6012ff48f`；舊verify SHA為`3e0ca92293fb98e00e1d9305557949941c16de77ad07e71384321ec86f29c43f`。四份主要及四份支援r3輸入SHA均與歷史檔相符，r2來源PASS、mechanical HOLD及r3機械檢查快取也已重新核綁，未改寫歷史。
- 全video物件只刪除c09le-shot-020、c09le-shot-021及各自le020、le021句。其餘114句物件、112個完整景物件、開場、95個原始句ID、全部保留prompt及其他video頂層資料均與r3逐物件相同；沒有新句或改寫。
- 旁白投影與claims陣列等於r3陣列只過濾這兩筆；作者稿與來源表只更新版本標頭並移除對應兩列。四者與video的114筆ID、文字、順序及來源映射一致。刪除是編輯決定，不把兩筆原有PASS改成來源不足。
- 14組loops物件不變，28端點都指向現稿；縮圖與書面source shot引用有效。五份現行分鏡／來源輸入中沒有被刪句或景的懸空引用。
- 木板的前文c09r090、試放動作le019及繩環說明c09r091均保留，接回c09r092服裝標籤問題；標籤前文c09r093仍在。現行句子不依賴被刪的形狀／尺寸細目。此項只核引用與來源依賴，不判敘事品質。
- 來源清單保留S4，其他現行主張仍使用它；S4:009亦仍支援le014及c09r079。26筆現行候選段落錨點、五組原件HTML／段落快取、12份基底來源鏈與基底輸入／收據SHA已實核一致。沒有新主張，未聲稱另行重新開網頁或全文重讀全部原件。
- S1的1967具名器材文章、S2的原1972前言、S3於1973刊出的Rowell書評、S4於1977刊出的採訪、S7於2012刊出的品牌回顧仍各守文件時層與說話者界線。少用岩釘不等於停售；1977不是確認到訪年；收入不是利潤，模具回本是當事人估算。le015／le022的東岸流傳地、年長作者及經書評引述的批評完全未改。

## 原生機械檢查

本代理以唯讀loadProject載入目前BASE canonical（video SHA `875eaca7ba51de28a9e2a198dfd8070325aabec91b58bb7cb903731415fb233a`、script SHA `0547060346e7d6194d9bd096bcc19bb4e0166dde28fd292543ff3f047cf216d1`），保留初始化293詞字典及完整情境，只在記憶體替換候選doc、brief、series，獨立重跑原生lintProject／checkBrief。0 errors、63 warnings，與root保存的canonical-lint-r4收據綁定輸入及計數一致；三個必填section非空，唯一選項A。warnings及估算不作敘事、語言、實際時長或媒體批准。

## 逐句來源結果

下表114筆均為已綁定r4收據的SOURCE PASS，分類承接未改的r3表。CONFIRMED支持有限表述；ATTRIBUTED保留文章、回憶、書評、採訪或品牌回顧歸屬；PLAN為明示假想、問句、旁白反應、回收或CTA，不把它當史實。無未解除來源HOLD或現稿NOT FOUND句。

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

本次只新增r4獨立收據及此候選verify檔；未改BASE、canonical、中文文案、字典、history、其他reviews、Git、provider或後台。
