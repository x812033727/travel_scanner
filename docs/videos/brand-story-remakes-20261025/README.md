# 後台品牌故事：新規則重製

依站主「參考1844、從C03開始、完成就接下一個、採推薦設定、預設八語」持續製作，並依追加指示套用 [PR1860](https://github.com/x812033727/travel_scanner/pull/1860) 的正式片頭片尾取得流程。**11集來源、書面分鏡及原生敘事合併通過；11集共9,544句八語文字通過。實際故事音訊、插圖、配樂、影片及付費請求仍為0。** [逐項狀態](status.json)與[接續順序](execution-order.json)綁定各集當前檔案雜湊。

正式站全頻道 v4 套件 `mokaair-brand-package-v4-endscreen` 已下載並安裝，package SHA `416c8768d4d29f2e746a0c019d2d598ec367cbb66b0ff996841c523651a63e88`。兩檔均1080p30，實SHA、150／630格與完整影音解碼通過：**開場濃縮後5秒片頭、最後21秒片尾**。這是兩份重用製片素材，並非生成故事媒體。[正式取得、影音QA及操作指南](branding-pr1860/README.md)與[必要包規則](branding-pr1860/required-branding.json)已落地；[preflight](branding-pr1860/preflight.mjs)在缺檔、錯包、版本不符或無法比對正式站時停止。每次真正合成前須重跑；尚無逐集production pin、timeline或組片。

C03正式TTS曾執行，在供應商派送前被 `video_budget_preproduction_hold` 拒絕。影片工具權杖有效，不需重貼；仍缺精確新版帳戶、各片US$25上限的受保護啟用、實際歷史帳本及全片報價。正式branding取得已解阻，不能繼續把它列為製片阻塞。[C03入場交接](c03/production-entry.md)與[目前停線](production-hold.json)保存具體待辦；沒有借原slug帳戶、改前綴或移除保護。

| 題目 | 當前來源／書面分鏡／敘事 | 後台與八語文字 |
| --- | --- | --- |
| [C03 Moleskine](c03/production-entry.md) | 原生合併PASS；共圖書面計畫PASS | 企劃／劇本核准已匯入；1,144句TEXT_PASS |
| [C04 泡泡紙](c04/production-entry.md) | 原生合併PASS；共圖書面計畫PASS | 企劃／劇本核准已匯入；880句TEXT_PASS |
| [C05 金鳥](c05/production-entry.md) | R13及實際第12輪原生合併PASS | 新企劃／劇本pending；872句TEXT_PASS，107句／語繼承原完整校對、2句／語另作獨立delta校對 |
| [C06 Play-Doh](c06/production-entry.md) | 原生合併PASS；共圖及story category delta PASS | 企劃／劇本核准已匯入；1,304句TEXT_PASS |
| [C07 Dr. Martens](c07/production-entry.md) | R10來源／分鏡及實際第9輪合併PASS | 新企劃／劇本pending；八語TEXT_PASS |
| [C08 龜甲萬](c08/production-entry.md) | R9及實際第9輪合併PASS；視覺delta另查 | 企劃／劇本核准已匯入；1,016句TEXT_PASS；後台語言選擇仍空 |
| [C09 Patagonia](c09/production-entry.md) | R7來源／分鏡及合併PASS；視覺delta另查 | 新企劃／劇本核准已匯入；824句TEXT_PASS |
| [C10 OXO](c10/production-entry.md) | R7來源／分鏡及實際第6輪合併PASS | 企劃／劇本核准已匯入；944句TEXT_PASS，後台語言選擇仍空 |
| [C11 UCC](c11/production-entry.md) | R6來源／共圖計畫及實際第5輪合併PASS | 新企劃／劇本pending；八語TEXT_PASS |
| [C14 CamelBak](c14/production-entry.md) | R6來源／共圖計畫及實際第5輪合併PASS | 新企劃／劇本pending；八語TEXT_PASS |
| [C15 FriXion](c15/production-entry.md) | R5來源／共圖計畫及實際第3輪合併PASS | 新企劃／劇本pending；八語TEXT_PASS |
| [C19 Seven Bank](c19/research-original.md) | R5來源delta PASS；fresh native5待審，R1–R4完整保存 | 未送新卡、未翻譯、未生成媒體 |
| [C20 Zippo](c20/research-original.md) | R1來源PASS／敘事HOLD已封存；R2重新整理終身保證主線 | 未送新卡／翻譯，原68檔保全，實際返還點火不作聲稱 |

[原始全批共圖查核](opening-teaser-image-audit.md)保留發現缺口當時的快照；[當前逐稿核對](opening-teaser-plan-reconciliation.json)證明11集20個事件預告已有來源核對的書面共圖計畫。實際圖片尚未生成，不能稱實圖共用已驗收。正常回收圖先做一次，預告呼叫前只讀核對原生cache key與實檔SHA；缺cache停止，不觸發第二次付費生成。每對須獨立驗圖，最終manifest及檔案SHA仍須一致。

9,544句為當前11集的未定時文字，排除舊基底、候選和未審草稿；各語metadata、章名、逐句文字與獨立校對鏈保存。C05 R13的16條新增譯句以獨立delta審查接續原107句／語全量校對，未冒稱重讀全部109句。純視覺換稿的語意校對以明列舊source SHA的rebind收據繼承，原始校對檔不改。這些均不是定時SRT、配音、語言輪或上傳資格。

原生兩讀者必要項只有兩位對同一項皆答no才失敗；單人保留意見完整保留。各輪HOLD、未審版本、raw答案、隔離輸入及來源SHA不覆寫。正式核准只適用其精確canonical劇本；視覺採用時的批准檔不變檢查與其後真實核准匯入分開留證。後台stage表示下一關，不能據此推定核准或媒體完成。C03／C04／C05使用合法legacy renderer卡片，後台分類仍story；官方report-only只為未分類卡填分類，實讀證明未覆寫既有owner選擇。

[原始盤點](batch.json)為22筆品牌故事、19筆未上YouTube、18題，非目前新增卡片後的後台總數。龜甲萬原版與short-v8為同題；[53份原稿SHA](original-preservation.json)未變。C19、C20後仍保留Seiko、Garmin、Dyson、行李箱、哆啦A夢五題，不為C系列缺號發明集數。

製作目標13分鐘，**真實TTS正文720–840秒**，口徑含冷開場及有聲CTA，只排額外26秒片頭片尾。[原生計時口徑](duration-measurement-scope.json)區分規劃分項與全程計時。字數或估計時間線不是實聲通過；短稿不能靠慢播、沉默或重述填長。C07／C11／C14／C15刪除重述後的規劃長度風險保留，需來源與實聲再核對。

畫面採MiniMax image-01、唯一look `{"preset":"cute-mystery"}`，正文至少70%相關插畫、最多連續3張必要字卡；英語匿名prompt不含品牌、真人名、logo、可讀字及版權角色。台灣說書旁白、繁中燒錄及CC，layout d縮圖黃字黑邊主標／白副標。clean-master目前只有[衍生配方及metadata檢查](c09/variants/clean-master/README.md)，每個實際clean輸出仍須自己的完整QA及當前final核准。

[prepare-runtime.mjs](prepare-runtime.mjs)僅初始化明列集數的正常字典及官方劇本；已有批准的執行根不可覆寫。受控採用保留原核准、字典、語意校對及失敗回退鏈。[runtime-cli.mjs](runtime-cli.mjs)只交給官方工具，不解除付費保護。來源快取、公共研究影片與正式branding原件在倉庫外，Git只收文字證據。

[C07容量研究](c07/duration-capacity-research.md)與[C11容量研究](c11/duration-capacity-research.md)已完成，新材料仍不足以在目前敘事範圍自然補足13分鐘；現稿與八語保留，後續須明確重定可證敘事範圍再寫，不降低時長標準。Seiko與Garmin原始研究完成，Seiko R1撰寫中；Dyson、行李箱及Doraemon原始研究已接續。
