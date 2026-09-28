# AI 真的可以？Shorts 實作與試片

繁體中文、台灣一般觀眾、不出鏡；在現有 Mokaair 頻道用真實 AI 實驗說故事。90 天 1,000 萬公開觀看是挑戰目標，不是保證。完整 15 題、120 個時段與每週選題方式見 [campaign/README.md](campaign/README.md)。

三支 MP4 的本機路徑、技術驗證與待完成事項見 [2026-09-28 交付收據](delivery-2026-09-28.md)。

## 可執行的本機流程

在 repo 根目錄先執行 `npm ci`。需要 Node 22+、ffmpeg（含 libx264）、ffprobe 與 Playwright Chromium；Windows ARM64 可用已安裝的 Edge。產物必須在 repo 外。

本次完整測試使用 Node 24.19.0。這台機器的 Node 24.13.0 執行既有工具測試會崩潰；請使用已驗證的較新 runtime，不要把程序崩潰當成測試通過。

```powershell
node tools/video/shorts/cli.mjs validate --file docs/videos/ai-shorts/pilots/shorts-receipt-total.json
node tools/video/shorts/cli.mjs build --file docs/videos/ai-shorts/pilots/shorts-receipt-total.json --workdir C:/Users/x8120/mokaair-work/shorts
node tools/video/shorts/cli.mjs build --file docs/videos/ai-shorts/pilots/shorts-poster-blind.json --workdir C:/Users/x8120/mokaair-work/shorts
node tools/video/shorts/cli.mjs build --file docs/videos/ai-shorts/pilots/shorts-prompt-check.json --workdir C:/Users/x8120/mokaair-work/shorts
node --test tools/video/shorts/*.test.mjs
```

預設本機試片聲音為 Windows 的 `Microsoft Hanhan Desktop`（zh-TW），不發送雲端語音請求，沒有新增 API 費。這不是正式頻道的 Gemini Sulafat；站主可以先聽試片再決定是否換聲音。其他系統傳入 `--audio-dir`：依腳本各 narration 片語依序提供 `000.wav`、`001.wav` 等，程式會轉為 48kHz mono PCM 並以實際長度產生字幕。外部語音成本保留未知，由費用表記錄；不視為免費。

每次執行各自建立新目錄，避免失敗重建混用上次成功收據。CLI 回傳完整成片目錄與秒數。產物包括 `upload/final.mp4`、繁中 SRT、直式封面影格、兩個標題、說明、SHA-256 manifest、上傳清單，以及 contact sheet、逐句時間軸與技術檢查。章節與五語字幕不套進這個繁中 Shorts 流程。

## 格式與驗證

「原來如此事務所」從長片切出的 Shorts（第 2 版的 `line: "cut"`、`series: "sothatswhy"`，圖是長片的關鍵影格）走 `from-episode` 指令，說明在 [`../so-thats-why/README.md`](../so-thats-why/README.md) 的 Shorts 一節。

新腳本沿用 pilots 三份 JSON 的 schema_version 1：slug、series（daily/blind/prompts）、兩個 titles、description、experiment_summary、limitations、evidence、scenes。每場景有 headline、narration 短句陣列；可加 body、big、note、asset。asset 必須在 evidence 列表，路徑相對於本資料夾；每項 evidence 必須綁 SHA-256。

- 固定 1080×1920、30 fps、25–55 秒、H.264/AAC。聲音超時就修改稿子，不裁掉旁白。
- 文字與字幕放在預留安全區；程式檢查溢出與缺圖，仍需真人在手機／Shorts 預覽中確認介面遮擋。
- 逐片語合成／匯入語音，字幕使用真實取樣長度對齊，尾端補至整格；音訊一次編碼，避免逐段 AAC 拼接漂移。
- 兩次 loudnorm，目標 −14 LUFS、−1 dBTP；成品再測，檢查影音長度、格數與編碼。
- 開始即固定已驗證的 evidence bytes；HTML 禁 script/iframe/object/embed、停用 JS 並封鎖所有網路請求。
- package 一律標為 owner-review-required。技術檢查不是聽審，不會設定公開或排程。

在工作基底或某個 slug 目錄放 `STOP`，流程完成手上單位後停止。原始證據不可重寫；新實驗建立新條件／新檔案後重新綁定。

## 實測的範圍

[experiments/protocol.json](experiments/protocol.json) 保存完整請求、答案與限制。兩個 fresh-context 子代理各回答一次，每則請求包含收據、三題與海報。精確後端模型版本未由工具提供，不假設品牌型號，也不是六次獨立測試。

兩組收據都得 275 元，三題都得 162 元、270 元、11:20。海報是原創 HTML/CSS，兩版四項文字皆齊全；它們不是影像生成評比。腳本如實呈現相同結果，不挑選失敗範例。原始回答和 HTML 均已留存；渲染只統一字型。

## 成本、排程與觀看數

正式首支公開當天才設定 campaign 的第 1 天。下面的日期只是命令範例，不代表頻道已發布。

```powershell
node tools/video/shorts/cli.mjs track-init --dir C:/Users/x8120/mokaair-work/shorts-tracking --start 2026-09-28
node tools/video/shorts/cli.mjs report --dir C:/Users/x8120/mokaair-work/shorts-tracking
```

init 不覆寫既有資料。從 Studio 匯出的原檔留在 repo 外，依 campaign README 映射到 metrics.csv；缺值留在待補資料檔，不可填零或假裝已取得私人 Analytics。尚無資料時報告顯示 no_metrics。比較以最早 7–9 日快照為準，每支至少 1,000 engaged views、每系列至少 5 支，否則顯示樣本不足。YouTube 的公開觀看與 engaged views 分別記錄。

成本表含已確認、預留與未知費用；未知阻止新增付費工作。每 30 天上限 NT$3,000，達 NT$2,400 停止新增付費實驗，保留完成既有作品的餘額；首三支共 NT$300。所有這些都是內部經營規則，不是演算法門檻。

## 交付邊界

這批完成的是產線、企劃、真實小實驗與可審試片。真人聽審、YouTube Studio 私人上傳、公開排程、近90天頻道基準匯出，以及發布後24h/72h/7d數據仍各自需要完成，不能從本機測試推定已完成。英文影片的搜尋線索與實際可讀原片，已在 sources.json 分開記錄。
