# 英、韓、西縮圖：手機文字可讀性

本次只調整三張外語縮圖短句與韓文副標的斷行；完整成片、旁白、字幕、標題說明與114句翻譯保留。原生手機字高目標仍為320px寬圖上的24px，沒有降低門檻。

| 語言 | 舊原生估計 | 新原生估計 | 實際完整圖 | 實際320px畫面 |
| --- | ---: | ---: | --- | --- |
| en | 23px | 27px | [英文JPEG](en.jpg) | [英文手機圖](en.phone320.png) |
| ko | 22px | 34px | [韓文JPEG](ko.jpg) | [韓文手機圖](ko.phone320.png) |
| es | 23px | 26px | [西文JPEG](es.jpg) | [西文手機圖](es.phone320.png) |

以上字高是原生 `thumbnailChecks` 的估計值，並非瀏覽器實測字型大小。三張實際1280×720 JPEG及各自320×180瀏覽器截圖已由ROOT觀看；canonical圖檔與已閱預覽逐位元組一致，文字沒有裁切，韓文 `같은` 已不再被拆開。見[ROOT實際檢視](root-canonical-thumbnail-review.json)。

- 英文：`File / Usable?`，維持兩個英文字，詢問檔案能否使用。
- 韓文：`쓸 수 / 있나?`，保留原本能否使用的問句；副標把 `와셔 하나, 파일 둘,` 與 `같은 요구` 分成兩行，僅以換行取代空格，字詞與標點一致。
- 西文：`Archivo / ¿Sirve?`，保留檔案能否使用的問題。

正常metadata-only sheet與merge使用新的獨立工作目錄，保留原有完整114句worksheet。正常 `render --thumbnails-only` 重畫八語，其他五語JPEG與舊檔逐位元組相同；原畫面狀態、快取、聯絡表、繁中縮圖、主片、音訊、CC及歷次state記錄保留，只有frame manifest的語言縮圖欄位與一筆正常render歷史更新。見[三語實際metadata差異](actual-three-metadata-corrections.json)、[八語實際輸出與估計](actual-eight-thumbnails.json)、[程序真實結束碼](canonical-process-exit.json)。

舊[完整QA報告](../native-final-QA.json)仍為10/11、整體false；47項字幕速度與3項舊縮圖的歷史提醒原樣保留。本次獨立圖片檢查沒有重跑或取代完整QA，也不構成旁白、成片、語言批次或上架包核准。經當前音檔完整聽校的八語M4A仍為0/8。

本次處理手機文字可讀性；右側漸層版面維持原設計，整體縮圖品質與CTR未另評估。

台北2026-10-27 04:02，三張新圖已附到[本片後台](https://mokaair.com/zh-TW/admin/videos?video=kimi-k31-3d-delivery)的同一筆待審紀錄；正常工具完整下載全部17個附件，ROOT逐檔核對所有位元組與SHA-256。[真實交付收據](actual-backend-thumbnail-delivery.json)保留結果，[正常附件清單](normal-final17-review-files.json)與[完整下載驗證](root-final17-binary-readback.json)可逐項核對。原14個附件、完整payload、九語現行metadata、未通過的完整QA與站主選擇均保持原值；新圖不代表八語配音或語言批次已完成。
