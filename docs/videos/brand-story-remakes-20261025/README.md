# 後台品牌故事：10/25 新規則重製

依站主「參考1844、從C03開始、完成就接下一個、採推薦設定、預設八語」持續製作。**目前完成的是來源、劇本、書面分鏡和部分八語文字；本批尚無生成音訊、插圖、配樂或影片，付費請求為0。** 最新逐項證據見 [status.json](status.json)。

C03企劃與劇本已核准並匯入。正式TTS曾執行，但在供應商派送前被既有 `video_budget_preproduction_hold` 擋下；現有影片工具權杖有效，不需重貼。精確新版帳戶、受保護啟用、全片費用及正式v4素材仍缺可操作的管理員／製片主機讀回，具體操作資料見 [C03製片入場交接](c03/production-entry.md)。未改帳本、停線或slug前綴繞行。

| 題目 | 當前文字／書面分鏡 | 後台／八語 |
| --- | --- | --- |
| [C03 Moleskine](c03/README.md) | 來源PASS、原生兩讀者合併PASS | 企劃／劇本核准已匯入；1144句TEXT_PASS |
| [C04 泡泡紙](c04/README.md) | 來源PASS、原生合併PASS | 劇本核准、企劃pending；880句TEXT_PASS |
| [C05 金鳥](c05/README.md) | 核准基底保留；材料旅程R9待來源差分；原生合併HOLD時間線 | 基底776句TEXT_PASS，排除未採用候選 |
| [C06 Play-Doh](c06/README.md) | R3來源PASS、原生合併PASS | 新企劃／劇本pending；1304句TEXT_PASS；[分類及正式八語設定待管理權限](c06/protected-admin-settings.json) |
| [C07 Dr. Martens](c07/script.md) | R3修窄來源並刪物流支線，待新審核 | 未送新卡、未翻譯 |
| [C08 龜甲萬](c08/script.md) | R4待來源差分；原生合併仍HOLD重述 | 未送新卡、未翻譯；正文容量風險保留 |
| [C09 Patagonia](c09/README.md) | R7來源PASS、兩位全新讀者合併PASS，已採用 | **新的企劃／劇本均pending**；新版824句TEXT_PASS |
| [C10 OXO](c10/history/r1/script.md) | R1來源／書面配鏡PASS；原生合併HOLD開場及重述 | 未送新卡、未翻譯 |

C03／C04／C05基底／C06／C09當前稿共 **4928句八語文字**已完成獨立校對及官方合併；數字排除候選和草稿。這些是未定時文字，沒有SRT、配音、語言輪、媒體QA或上傳資格。各集原始答案、必修、精確修正及獨立重查均保存。兩讀者依原生規則合併：必要項只有兩位皆答no才失敗；單人保留意見不刪、不改成一致同意。

C09當前video SHA `aed95981…`、官方劇本SHA `02f091ca…`，新劇本review `6a441762-8d88-45b7-adff-78b5c3ef1260`、新企劃 `5199b233-c1ee-4970-ae11-af9115cbbde9` 均已真實讀回pending。舊核准基底、760句舊譯文和失敗採用／rollback鏈在[基底封存](c09/history/baseline-before-length/)及候選history，舊批准不適用新稿。後台stage欄表示下一關名稱，不能用它推定核准或媒體完成。

原始[盤點](batch.json)為22筆品牌故事、19筆未上YouTube、18個題目。龜甲萬原版與short-v8為同題，均保留；[53份舊來源雜湊](original-preservation.json)全數未變。當前已有五題來源及敘事合併PASS，其餘13題含正在寫稿／審核的C07、C08、C10，詳見[接續順序](execution-order.json)。不為集數缺號新增題目，非C系列仍保留在原佇列。

製作規格依[10/25決定](../channel-review-20261025-story-series/README.md)、[品牌故事流程](../../../.agents/skills/brand-story/SKILL.md)與[PR1844](https://github.com/x812033727/travel_scanner/pull/1844)：目標13分鐘，**實聲正文須720–840秒**；開場具觀眾利害、有來源數字及具體場景；每章對觀眾說話、有旁白反應；30–45秒實質鉤子、至少8組有實際新答案的回收。字數、估計時間線和dry-run均不算時長通過；偏短稿不得靠慢播、停頓或警語填長。

插畫用image-01與唯一look `{"preset":"cute-mystery"}`，正文至少70%內容相關插畫、最多連續3張必要字卡；英語匿名概念prompt不得有品牌／真人名、logo或可讀文字。台灣說書旁白、繁中燒錄及CC、濃縮開場後5秒正式片頭、21秒正式v4片尾；layout d縮圖採黃字黑邊主標與白副標。書面配鏡PASS不等於生成圖驗收。

各集 `video.json` 是機器稿；作者 `script.md` 與 `claims.md` 保留逐句來源，官方 `writeScreenplay` 另產生runtime劇本；後台實收投影保存在 `backend-script.md` 並有SHA。禁止混用作者與官方劇本雜湊，也不以產生投影為由覆寫查核原件。

[prepare-runtime.mjs](prepare-runtime.mjs)可明列選集在倉庫外初始化正常不可變字典及官方劇本，不產生owner核准、不帶舊auto.json。已有核准的C03／C04／C05／C09執行目錄不可用它覆寫；C09換稿採精確來源、查核、原生合併及0error預檢的獨立採用程序。runtime helper遇既有批准會停止以便核對。[runtime-cli.mjs](runtime-cli.mjs)只交給官方CLI，不解除保護。

接續關卡：精確稿件審核 → 正式全片帳戶與報價 → TTS實測和聽檢 → 插畫驗收 → 正式片頭片尾、配樂、組片及字幕 → 完整解碼QA與站主看片 → 上傳包。各集clean-master只有[衍生配方與metadata檢查](c09/variants/clean-master/README.md)，須另有實際clean輸出、全片QA和當前final批准才符合配音入場，不能借燒字幕版本的批准。

此前文件影片測試236項、收集契約2項、原生i18n測試12項均通過，任務檢查2178份通過；本輪各稿機械檢查與文字搬入結果依綁定收據保留，不拿過去測試代替新稿實聲／圖像驗收。來源快取及公用參考影片在倉庫外，下載原件不算生成製片素材。所有付費保護及正式看片關卡維持有效。
