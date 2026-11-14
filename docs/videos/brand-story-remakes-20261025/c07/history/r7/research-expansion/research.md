# C07｜R4篇幅材料增補研究

**研究容量HOLD：目前未找到足以在同一修理旅程新增600–800有效spokenUnits的材料。** 這是本輪探索尺度，不是已證實聲缺口。沒有撰寫新中文旁白、重跑native或修改R4。已把可取得的原件、影片讀取缺口與不同實鞋／工法的界線保存；不以報告長度或來源數量冒充可講時長。

## 時長口徑更正

依根任務確認的tools/video/core/duration.mjs，原生body以**整份未加頻道bookends的實際旁白timeline**為準，包含冷開場和有聲CTA；只排除另外加上的5秒intro與21秒outro。凍結R4的既有native文字總計為2668units；after-opening2526與strict2430只是額外規劃分項，不能拿來當官方duration基準。尚未製作真TTS，不能由這些算術判為已知時長不足，實際還需補多少目前為null。以下600–800／700只是這輪研究探索目標，不能轉述為製作必須補足的已測缺口。

## 目前能用多少

既有38.144秒授權示範內，新辨認出三個尚未在R4詳寫的微動作：車線前拉出長線、接底前棒料式加料工具接觸露出的底層、穿帶前朝桌上獨立鞋墊形部件噴灑。它們都有實際原片bytes與原尺寸影格，能在原示範內保留順序；保守編輯規劃約80–160新增units，沒有寫成旁白或實測。若只與本輪探索目標比較，距600–800的材料尺度約440–720，距偏好700約540–620；這些數字不是實聲時長或實際必補量。不能把一秒內的手部移動拆成多句重述來撐到700。

另取得SoleHeeled一個1460Mono修理案例，包含拆舊底、保留中底、安裝Vibram底、鞋內貼補片、壓回外側鬆皮及黑色含色鞋油整理，共有六個可辨動作／結果節點及一個初始鞋況節點，並抓取及目視八張Before／After原圖。它可作另一個完整的修理店自述案例，整案約300–500units只是保守規劃，**不是往目前R4直接追加的淨新增量**。那是澳洲Donnybrook另一雙鞋，接底工法也不同，沒有已證回到顧客腳上的記錄。把它與目前七月顧客、英國授權熱接示範說成一雙鞋，會破壞一條時間線與來源界線。

## 既有原片的新細節

原件：`drmartensrepairs.com/pages/how-it-works`內的公開示範；原下載URL及SHA見收據。這輪只把既有原件逐位元複製到length-research，沒有假稱重新HTTP下載。原件31,960,486bytes、SHA`f5a6acd16fed47470947b6f19f47ad582dda14615324cd598197a31d2c891c74`；ffprobe容器38.144秒，影像串流38.125秒／24fps／915frames。來源影片不是本集生成媒體，沒有以音訊作證。

| 節點 | 原件時間 | 實際可見的新動作 | 不能推論 |
|---|---|---|---|
| E01 | 8.25–9.20s；detail8.4 | 手持鞋身旁拉出長的一段線，之後切到機針工位 | 線長、張力測試、材料、目的或實際工時 |
| E02 | 14.80–15.65s；detail15.2 | 帶長棒料的手持加料工具靠上露出的底層；待接的新底放旁邊 | 膠料化學、牌型、固化時間或接合強度；不能由此改寫整雙鞋無膠／有膠 |
| E03 | 26.60–27.25s；detail26.9/27.1/27.2 | 朝桌上的黑色鞋墊形部件噴灑，另一片在旁 | 特定品牌、抗菌配方、除味效果或新鞋墊；沒有看見的裝回動作也不補寫 |

新細節必須仍讀作同一段**獨立示範**，不是七月評論者的實鞋。13.6秒右機頭接觸仍不能改稱砂帶。650°C及接底不使用黏著劑原文只限PLC描述的熱接接底程序，不是從新影格量測出來，也不代表鞋內、底層或全鞋所有工序。

## 新取得的修理師原件

### A｜Donnybrook的1460Mono案例：有用，但不能拼進英國原鞋

URL： https://soleheeled.com.au/case-studies/dr-martens-boot-resole-and-tear-repair

HTTP200；原HTML167,238bytes；SHA`c2b242fabbfd186cb7c629bfb21974993cb207358eb220a0affddfc9315bf0e8`。頁面顯示發布2024-03-17、結構化modified2026-10-05；兩者是文章日期，不是已證修理日。照片URL內的數字亦不得充當拍攝日期。

實際段落021交代顧客地點、1460Mono、鞋面撕裂及底近脫落。023–024交代切除舊外底至原中底下緣，並把新Vibram底黏到原中底。034交代在前掌外側撕裂處內面加皮補片、黏住內裡後再壓黏外側鬆皮。041交代含黑色顏料的鞋油與補回部分褪色。照片01/02、03/04顯示底形改變；05/06顯示裂口區域；07/08顯示整體表面。八張原圖逐一取bytes、SHA並目視，仍可見折痕與修補區紋理，不能說全新無痕。

這是具歸屬的修理店第一人稱案例，不是原廠認證工法或獨立耐久測試。內面補片在腳趾區，不是把英國服務「後跟內裡換新皮」擴成全鞋內裡。照片不證明隱藏補片的安裝工序、顧客收貨或後續穿著；文中輕量、柔韌、耐久比較未取得測試，未採為可用性能結論。

### B｜Coburg中底裂開案例：記錄取捨與做不到的結果

URL： https://soleheeled.com.au/case-studies/dr-martens-boot-resole-midsole-repair

HTTP200；原HTML153,495bytes；SHA`561882a4dd5e8c54ece2b43d56ab183035cf1ecfba9404f853386b9dfba2f683`。顯示發布2024-02-20、modified2025-01-02，實際修理日未建立。段落024、030–031說明修理既有中底、處理右靴後方大裂口、移去受損材料、封合後重新黏回鞋面，再接新橡膠底；修理店明說受損範圍使外觀無法完全無縫。這是另一雙鞋，不能和A或R4混成同件；「cosmetic stitching」是該店文案，不得反向否定PLC對原廠沿條縫線結構的說明。

### C｜Stafford加中底／Solovair案例：方法不同

URL： https://soleheeled.com.au/case-studies/dr-martens-boot-solovair-resole

HTTP200；原HTML158,258bytes；SHA`d9384f161e39f93bc5b5cf708cf6797fab572376d2c87d1df569493ab0dd25be`。原件顯示發布2024-05-22、modified2026-10-11，不能沿用搜尋列表的另一日期。024–025說明切去舊底、把全長中底縫入footbed，再作為Solovair新底的平整基底。不能稱原廠底／英國授權工法，亦不能把該店關於rand不好拆的概括句用來否定授權示範的拆沿條。此例不同於A/B/R4，未計作同一旅程增量。

## 原訪談與品牌案例：已開原件，但沒有足夠流程容量

- Micro-Fresh的2023-05-31原Q&A，具名JamieWhitehouse，原HTML52,077bytes／SHA`e0337ab470e660c8c5384cd904b017403cf4756afaf934d966426537c0faf473`。029–030談翻新VivoBarefoot與DrMartens供下一位使用者，033談detectorpen展示。來源是供應商商業訪談，並無實際測試protocol、對照組、樣本數、閾值或結果；也沒有證明原示範噴瓶就是此產品。不能寫成同一顧客的抗菌／臨床／除味或安全實測。
- 2025年報原PDF9,966,532bytes／SHA`6212be3c41d434a725da281b92c3db308e068e3194ef679d0bb7e98b5bbfd1f0`，PDF70／印68短述一位母親修復90年代童靴供孩子穿、相隔30年。只有品牌自述的結果，沒有具名人、逐步工序或已證送回的紀錄；不同實鞋不能拿來填目前成人靴的結尾。年度商業數字不採。

## 長版原片的取得缺口

| 原件候選 | 目前狀態 | 還缺什麼 |
|---|---|---|
| https://www.youtube.com/watch?v=Yjsy98EiOx0 ｜ShoeHealer送往授權服務後的實物檢視 | executor代理CONNECT403；web原頁open亦失敗。只取得搜尋發現資訊 | 原始完整影片、實際片長、完整逐字／時間段與可見回程物件；未取得前零可用容量 |
| https://www.youtube.com/watch?v=f0x9-aHiW-0 ｜TheKeyCobbler修復原片 | web原頁open失敗；同YouTube來源已知不可讀，未改走替代代理 | 原片bytes／片長／實際工法與顧客界線 |
| https://www.youtube.com/watch?v=WBlrCxZeSwY ｜TheKeyCobbler原底單元修理候選 | 搜尋線索，未取得原片 | 同上，不能由標題推測已用哪種工法 |
| https://www.drmartens.com/uk/en_gb/made-to-last | HTTP403，只保存拒絕頁bytes | 原廠頁面與實際影片；不把商業製作新聞當已看原片 |
| https://www.soleandtrail.co.uk/collections/dr-martens-solovair-repairs | HTTP200但導到/password | 原修理頁內容，沒有越過密碼門 |

ShoeHealer自有首頁與修理頁已取原HTML，其一般fullrebuild選項不能證明影片中那雙DrMartens做了換cork／shank／heelstack，不把報價表當實際顧客選擇。BootRepairCompany首頁、品牌入口及官方Linktree也已開原件，沒有找出可下載的另一支長版修理片。搜尋收斂於上述直接相關線索，沒有繼續擴到一般鞋履年表或產品清單。

## 建議交接

若維持目前R4的一雙顧客靴與授權示範結構，只能先保留三個微動作候選，**不能宣稱找到700 units的新材料**。真正需補多少應等完整無bookends的TTS timeline實測；不因strict分項較小而強接另一雙鞋或工法。最有用的下一份缺件是ShoeHealer原片，因為它可能有具名修理師對一雙送修實物的前後檢查；需先取得並完整看過，再決定能否取代部分既有案例，不能靠搜尋描述直接改稿。若改採澳洲案例，必須整體重做來源與工法界線，不能在同一雙鞋上同時套用「拆換新沿條熱接」與「保留中底黏Vibram」。

本研究沒有改動R1–R4、history、原研究、原舊集或immutable字典，沒有新增中文稿、native／source／敘事PASS、verify、媒體或owner批准。所有保護hash、HTTP／原件／cache／圖片／source-video detail收據在source-receipts.json；逐主張英文研究命題與限制在claims.json。

研究claims SHA：`a1cb2a5fcad36b9baa9c485043d314289df9758fda7123e2e9c50ac2381c1104`；source-receipts SHA：`f4f5564d0c6b8b496eea6ea8793e5f53f88ccabca8927a6690f4d86b152f8afb`。
