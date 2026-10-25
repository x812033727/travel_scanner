# 製作交接：OpenAI DNS 隔離事件

製作日期：2026-10-25。狀態：大綱已送後臺；工具已配對，依站主委派採推薦 A 並記錄本機核准，正在推進正式媒體。

本片沿用頻道的繁體中文長片、Sulafat 旁白、zh-TW 主字卡、英文專有名詞與可關閉 CC。目標 8–12 分鐘；所有文字估時都不是實際音軌或影片長度。

## 先看什麼

- `brief.md`：三個大綱與推薦 A；此版本已送後臺並綁核准雜湊，後續不任意改動。
- `video.json`：按 A 準備的可修改製作稿；`script.md` 是由它產生的閱讀版。
- `claims.md`、`timeline-calculation.json`：官方證據與依時間戳計算的等待時間。
- `reference-study-20261025.md`：八支海外影片、點閱快照、可學的內容安排及未觀看的限制。
- 獨立查核與敘事審查紀錄：只證明各自檢查的範圍，不代表媒體與上架品管已完成。

## 真正的新消息

10 月 23 日 OpenAI 公布研究訓練環境的整改。DNS 事件在 9 月 20 日發生，事件報告於 9 月 25 日更新。10 月 1 日恢復的是 frontier 模型的強化學習與內部推論，不表示繼續訓練該事件中的特定模型。METR 10 月 22 日發表的評估則針對 7 月的歷史系統。

旁白、標題、縮圖及 Shorts 都要維持這些區分；不得把本片改成公眾 ChatGPT 本週「逃出實驗室」的故事。

## 尚缺的實際步驟

站主於本次對話明確要求：「之後依據你的推薦或jev選擇就好 不用問我」。此授權優先於舊的手動片逐關等待規則。各關依實際證據決定並寫明委派依據，不冒稱站主已在後臺點選，不製造 `auto.json`。

1. 已完成：工具配對；題目及大綱已送後臺。金鑰與權杖沒有貼入對話或提交 git。
2. 已完成：Jev 選 C 但示範分數 0.42 未達 0.6；依站主委派採代理推薦 A，`approve --gate outline` 記下授權與理由。後臺該張卡仍是 pending，沒有冒稱後臺已批准；本機流程使用核准後同一份 `brief.md`。
3. 執行 TTS dry-run 查看字數、設定與額度，再合成、檢查聲音並處理問題。
4. 旁白審核後製作完整畫面、合成、CC 與 QA。實際時長須重新確認達頻道下限；不能靠靜音、慢播或重複撐長。
5. 成片審核後產生上傳包；其他語言由站主逐支勾選。最後由站主在 YouTube Studio 上傳與決定公開。

## 可接續的命令

先在 repo 根目錄設定一個**repo 外**的工作資料夾，以下用 `$VIDEO_WORKDIR`。本次環境的工作資料夾是 `/workspace/work/videos`。

```bash
node tools/video/cli.mjs lint --slug openai-dns-containment
node tools/video/cli.mjs status --slug openai-dns-containment --workdir "$VIDEO_WORKDIR"
node tools/video/cli.mjs login
node tools/video/cli.mjs review-push --slug openai-dns-containment --gate outline --workdir "$VIDEO_WORKDIR"
node tools/video/cli.mjs review-pull --slug openai-dns-containment --workdir "$VIDEO_WORKDIR"
node tools/video/cli.mjs tts --slug openai-dns-containment --dry-run --workdir "$VIDEO_WORKDIR"
```

這段列的是標準工具命令，不代表已執行或已授權任何關卡。本次執行器不能把檔案寫入使用者家目錄，配對會透過工作區裡的程式入口將憑證存於私有 scratch 目錄；這只改存放位置，不改配對與審核。該入口和任何憑證都不提交到 git。

正式音軌、frames、CC、mp4、核准及上傳包都留在外部工作區，不提交到公開 repo。不要將計畫時長、樣卡或審稿結果當成成片完成的證據。
