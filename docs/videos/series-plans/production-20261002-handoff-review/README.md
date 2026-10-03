# 十部漫劇：配音交接與素材保存再覆核

本輪延續十部、400 集的來源與製作流程檢查。未合成配音、音效、動畫或影片，
也沒有試聽、成片核准或上架。中文 zh-TW 先定案，日／韓／英的角色音軌與
各自量測 CC 仍是後續製作計畫；對白與旁白不燒進畫面。

## 確認並修正的製作指示

| 作品與集數 | 修正 | 來源 |
| --- | --- | --- |
| city-owes-a-light E13 | 簡訊傳到中繼點，由陳勳回報；E14–15 才由鄭茵複誦。受困值班員仍無配音。 | source.mjs:3056 |
| reload-first-day E23 | 客觀鏡頭播放晚照原聲錄音，其他人聽得見；晚照主觀聽覺只抽掉這條錄音，回客觀恢復。 | chapter-3.mjs:49–50 |
| reload-first-day E25 | 只有真周嶼敲錶三下；假者手腕不動、無敲聲。真方擋擊後才出現沉重氣息，不提前暴露真假。 | chapter-3.mjs:81、84 |

只改這三集的 hero_shot.sound / voice_notes 及兩份製作覆核說明，十部故事
source hash 均未改。其餘角色與情節不新增台詞。全十部 705 筆離線試音／非語音
計畫、110 組實際聲線狀態可建立；逐集 audio_cues 的說話者均在來源出場清單。
這些是待試聽的材料，不能用文字計畫代替實際聲音辨識。

## 錄音接受必須指向實際 take

原流程重錄同字、同秒數的配音時，旁白 WAV 已變，timeline.json 卻不變，
舊 audio approval 仍顯示通過。模擬語音重現證實此缺陷，沒有呼叫真實服務。

現在每句 `timeline.lines[].audio_sha256` 及
`timeline.audio_evidence.narration_sha256` 綁定實際 WAV；檔案格式、樣本數與
雜湊必須相符。音訊核准、狀態、後台審核同步與後續合成使用同一驗證。
重錄使舊聽審失效；缺檔或替換實檔先停止。ASR 的 `check.lines[id].clip` 也必須
對到當前 take，舊結論不能自動套用。這仍不能代替母語聽審。

成片 `checks.narration_sha256` 另綁合成時的旁白。即使新配音已重新聽審，
舊成片也不能被當作已重新混音；worker、直接 QA、package 與 final 送審都檢查。

舊時間軸可用 `tts --refresh-evidence` 由當前快取錄音離線重建證據，不需要
token、不送付費 POST。快取缺漏或來源不符會拒絕，不能藉 metadata 重建取得核准。
重新綁定後仍要重新聽審；既有 current evidence 與實檔不符時不能自動掩蓋。

## 中文後續語言需要留下素材

原 `tidy` 只看網站當下的語言選擇；中文已上架、當次 locales={} 時，七天後
可能刪掉乾聲、旁白、畫面主版、clips 與 build 音效，讓後續外語只能重做。

來源綁定的 `video.json.localization_plan` 和工作區
`localization-retention.json` 現在記錄後續 ja／ko／en 的素材保留要求。
舊集數也可由 `series.json.production.profile` 辨認；其合集保留相應素材。
空語言選擇、滿保留天數、skipped 或 dropped 狀態都不解除這個已承諾的交付。
損壞標記先保留，普通無此計畫的投影片仍沿用現有清理規則。

目前只實作保留，不實作自動解除或歸檔。明確驗證歸檔及站主解除介面另列
`tasks/open/2026-10-02-localization-media-archive-release.md`，不能手改完成旗標刪素材。
保留來源不表示已建立完整多角色外語 dub 或 M&E 輸出引擎。

## 後台與驗證證據

- [backend-verification.json](./backend-verification.json)：兩部新增完整六文件的
  v4 待審修訂，共 12 筆；180 筆 v1–v3 歷史保留。其餘八部 v3 不變。
  正常後台 serializer 的最新內容逐份匹配，重放為 unchanged；未驗瀏覽器畫面。
- [independent-review.json](./independent-review.json)：另一代理的來源與 runtime
  覆核，分開記錄作者測試與獨立判定，不冒稱自我獨立審。
- 本輪兩批 source/generated-file validators 與 production-check/build 均通過。
  全工具測試與獨立片長收據的最終結果以本目錄 validation.json 為準。
  完整工具首輪有七個舊情境缺少新的實際音檔證據；補齊合成 WAV 與混音雜湊，
  保留原斷言後定向重跑。首輪與重跑分開記錄，不冒稱第二次全套執行。
  LF 發布位元組另經獨立續審，六個純換行綁定更新，原封存收據未改。

正式站只更新這兩部待審文件。全域生成設定、核准、集數與發布保持原狀，
本輪 runtime 修正尚未部署。來源 SHA 為已提交的
`e06a741053372f123fc11f43c12a1c9f18ffaea7`；資料更新前另做可列目錄的 PG 備份。

## 實際影片仍須接受的項目

中文人名、角色辨識、受傷與年齡聲線、主客觀聽覺、敲擊及錄音線索、手機外放
與 mono 混音、實際 CC 揭密落點、口型與分鏡節奏，都要用中文試音及代表 pilot
確認。六部的未成年入鏡路徑仍待另外驗證，不能因文字檢查通過直接放量。
Wedding／Train 的舊完整故事覆核收據未偽造更新；前輪 source-review-delta 證據
保留，正式完整覆核關卡仍依實際新讀稿更新。百萬觀看保持目標，不作保證。
