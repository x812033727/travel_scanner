# 五部約兩小時漫劇｜製作企劃包

以每部百萬點閱為成效目標，採「前段有爽感、中段有翻轉、後段在乎人物選擇」的共同標準。這是五部原創故事的製作文件，不是五部已完成的影片；百萬點閱不作交付保證。

## 從這裡閱讀

| 製作順序 | 作品 | 核心吸引力 | 入口 |
| --- | --- | --- | --- |
| 1 | 喜宴未散，清算開始 | 婚禮拒簽、重生清算、姐妹信任 | [完整企劃](wedding-reckoning/README.md) · [40 集總綱](wedding-reckoning/outline.md) |
| 2 | 末班車上的第七個活人 | 假廣播、被漏算的活人、接受離別 | [完整企劃](seventh-passenger/README.md) · [40 集總綱](seventh-passenger/outline.md) |
| 3 | 這座城欠他一盞燈 | 真本事救援、父女信任、承認責任 | [完整企劃](city-owes-a-light/README.md) · [40 集總綱](city-owes-a-light/outline.md) |
| 4 | 朕不是你們的替死鬼 | 假女帝、糧務博弈、用行動取得支持 | [完整企劃](scapegoat-empress/README.md) · [40 集總綱](scapegoat-empress/outline.md) |
| 5 | 世人忘我，死敵記我 | 唯一記得自己的死敵、力量代價、重新認識 | [完整企劃](remembered-by-rival/README.md) · [40 集總綱](remembered-by-rival/outline.md) |

每部包含一份設定集、一份 40 集總綱、四份 10 集細綱、40 列連貫性表、三組標題縮圖構圖及上架文案。五部合計 **5 份設定集、200 集細綱、20 個篇章、15 組包裝方案**。

細綱逐集記錄開場、衝突、轉折、收尾、兩次具體回報、伏筆、張力、出場人物、場景，以及下集必須繼承的情報、道具和傷勢。不是用集名代替劇情。

## 共同製作標準

- 每部目標 120 分鐘，實際成片接受 115–125 分鐘；40 集，每集約 3 分鐘，四篇各 10 集。
- 16:9、1080p、cinematic-3d、hybrid；最多四成鏡頭使用動態片段，優先分給行動、重要表情與高潮。
- 台灣國語旁白與固定角色聲音；聲音目前是 casting 提案，先以正式主機的聲音池和試聽確認。
- 繁中燒錄字幕及 zh-TW/en/ja/ko/zh-CN 五語 CC；字幕在完整劇本與聲音時間軸確立後製作。
- 前四部 no-romance；第五部 dual-male-leads-subtext，羈絆以物件和行動呈現。
- 第一行鉤子目標 5 秒、估算不超過 8 秒；10 秒內進入衝突，30 秒內第一次具體回報，每集至少兩次。
- 約 30、60、90 分鐘改變局勢；最後 15 分鐘回收主線與情感。第 40 集可以是情感強烈的已完成翻轉，不增加續作懸案。
- 任意連續四集有伏筆回收，跨篇也算；回收可以是有具體答案的局部兌現，不能只在欄位填 ID。
- 每場戲改變情報、關係或處境。緊湊不是每秒吵鬧；角色作出重要決定時保留短暫安靜。

## 交給產線的方式

`series-request.json` 使用既有 SeriesIn 欄位。`setting.json`、`outline.json`、`chapter-01.json` 至 `chapter-04.json` 保留既有 body_md/body_json 結構；`documents.json` 集中六筆包含 kind/chapter_number 的待送件資料。

**檔案存在不代表後台作品已建立或審核已核准。** 本包不含會發出網路請求的匯入或開拍腳本，也不把本地編輯覆核塞入正式站 judge 充當線上批准。建立請求預設 hands_off=false，避免將資料檔誤當免關卡全自動開拍；即使如此，真正 POST 建立仍可能排入工人產生費用，應在實際開拍時才使用。

完成影片後，在合集 video.json 的 compilation 關閉 `chapter_cards`、`outro`，保持連續觀看；這兩個欄位不在 SeriesIn。仍保留 YouTube 章節，時間碼讀取實際時間軸，不能用每集三分鐘推算假時間碼。

其他操作細節見 [製作與交接](PRODUCTION.md)。所有音檔、圖片、字幕產物、影片與正式核准收據放 repo 外 VIDEO_WORKDIR；本目錄只有文字與結構資料。

## 檢查與重建

從 repository 根目錄執行：

```powershell
node docs/videos/series-plans/binge-five-20260928/build.mjs
node docs/videos/series-plans/binge-five-20260928/validate.mjs --require-reviews --write-report
node --test docs/videos/series-plans/binge-five-20260928/validate.test.mjs
npm run check:tasks
```

- [檢查報告](validation-report.json)：機械檢查與既有工人 documentProblem/retentionProblem 的實際結果。
- [第二輪覆核與修正](RECHECK.md)：本輪故事、人物知情範圍、通訊、場景與交接的修正；最新五份收據綁定來源雜湊。
- [首輪審查紀錄](REVIEW.md)：保留首次發現與修正，原始收據及當時來源已封存。修改 source 後必須重新覆核。
- [作者契約](AUTHORING.md)：欄位、節奏規則、原創及審查標準。

`source.mjs` 是單一編輯來源；修改後由 build 產生 Markdown、JSON、CSV 及 manifest。validate 預設只讀，`--write-report` 才寫報告。機械檢查不能證明故事一定好看，獨立編輯檢查不能證明實際配音或成片品質。

## 完成與後續界線

本包交付的是故事與製作規格，沒有產生 200 集完整台詞稿、圖片、TTS、影片、SRT 或成片縮圖，沒有登入 YouTube、建立後台作品或上架。實際留存、成本、聲線和 115–125 分鐘長度，需在媒體階段重新量測。

首部先做前三集約九分鐘校準，再逐部完成；不把五部同時送入付費生成。故事交付、媒體驗收、發布及百萬點閱各自記錄，不能互相代替。
