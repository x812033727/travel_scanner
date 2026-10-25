# 製作交接：OpenAI DNS 隔離事件

製作日期：2026-10-25。狀態：成片與完整上傳包已送後臺；依站主委派採推薦 A 並記錄各關本機決定。實際交付、QA 例外及後臺狀態以 `production-result.md` 為準。

本片沿用頻道的繁體中文長片、Sulafat 旁白、zh-TW 主字卡、英文專有名詞與可關閉 CC。實際成片為 8:20.6、1080p；文字估時另保留於 `draft-estimate.json`。

## 先看什麼

- `brief.md`：三個大綱與推薦 A；此版本已送後臺並綁核准雜湊，後續不任意改動。
- `video.json`：按 A 準備的可修改製作稿；`script.md` 是由它產生的閱讀版。
- `claims.md`、`timeline-calculation.json`：官方證據與依時間戳計算的等待時間。
- `reference-study-20261025.md`：八支海外影片、點閱快照、可學的內容安排及未觀看的限制。
- `production-result.md`：實測、交付內容、QA 10/11 的採用理由，以及後臺審核列與 YouTube 發布的實際狀態。
- 獨立查核與敘事審查紀錄：各自保留檢查範圍及未通過的項目。

## 真正的新消息

10 月 23 日 OpenAI 公布研究訓練環境的整改。DNS 事件在 9 月 20 日發生，事件報告於 9 月 25 日更新。10 月 1 日恢復的是 frontier 模型的強化學習與內部推論，不表示繼續訓練該事件中的特定模型。METR 10 月 22 日發表的評估則針對 7 月的歷史系統。

旁白、標題及縮圖都要維持這些區分；不得把本片改成公眾 ChatGPT 本週「逃出實驗室」的故事。本次未製作 Shorts。

## 已完成的製作與交付

站主於本次對話明確要求：「之後依據你的推薦或jev選擇就好 不用問我」。此授權優先於舊的手動片逐關等待規則。各關依實際證據決定並寫明委派依據，不冒稱站主已在後臺點選，不製造 `auto.json`。

1. 已完成：工具配對；題目及大綱已送後臺。金鑰與權杖沒有貼入對話或提交 git。
2. 已完成：Jev 選 C 但示範分數 0.42 未達 0.6；依站主委派採代理推薦 A，`approve --gate outline` 記下授權與理由。本機流程使用核准後同一份 `brief.md`；較早的遠端 C 核准與後來的本機 A 決定分別保存。
3. 已完成：額度 dry-run、正式 TTS、針對近音詞白話改寫與定向重錄；80/80 句音檢通過。
4. 已完成：78 畫面狀態、完整組片、83 cues CC、最終 QA。整片 QA 10/11；Jev 示範分數 0.46 未達 0.6，協調者依站主委派與實際證據採用，保留原始未過結果。
5. 已完成：上傳包 4/4 通過，繁中成片、三縮圖、字幕、說明與 metadata 已完整送到後臺。遠端 audio／final／publish 列仍 pending；工具沒有人工審核決定或語言面板寫入路由。此片按推薦交付繁中，尚未發布到 YouTube。

## 查驗與重現

先在 repo 根目錄設定一個**repo 外**的工作資料夾，以下用 `$VIDEO_WORKDIR`。本次環境的工作資料夾是 `/workspace/work/videos`。

```bash
node tools/video/cli.mjs lint --slug openai-dns-containment
node tools/video/cli.mjs status --slug openai-dns-containment --workdir "$VIDEO_WORKDIR"
node docs/videos/openai-dns-containment/assemble-with-peak-guard.mjs --slug openai-dns-containment --workdir "$VIDEO_WORKDIR"
```

重新組片只在需要重現時執行，不因交接重跑已通過媒體。本次執行器不能把檔案寫入使用者家目錄，已透過工作區裡的程式入口將配對憑證存於私有 scratch 目錄；這只改存放位置，不改配對與審核。該入口和任何憑證都不提交到 git，既有配對不需重做。

正式音軌、frames、CC、mp4、核准及上傳包都留在外部工作區，不提交到公開 repo。不要將計畫時長、樣卡或審稿結果當成成片完成的證據。
