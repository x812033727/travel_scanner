# 稽核證據索引

這些檔案是 2026-10-08 對原交付物的重新檢查，**不是正式 QA／核准紀錄**。
主要結論與限制見 [AUDIT.md](../AUDIT.md)。

| 檔案 | 覆蓋範圍與方法 |
| --- | --- |
| `media_audit.json` | 300 檔 ffprobe、SHA-256、全長音訊 EBU R128；60 MP4 的封包、IDR 與 x264 設定。含工具命令、規則與限制。 |
| `content_audit.json` | 全 60 集 180 題的實際選播證據、30 題問題、明確建議句 ID、136 個過長靜態狀態與流程缺項；含來源 hash。 |
| `caption_metrics.json` | 從倉庫直接 import `parseSrt`／`checkCues` 對 300 SRT 執行；zh-Hant/zh-Hans 映射至 zh-TW/zh-CN。`failedFiles` 是低階檢查欄位，不代表跑過正式 qa；CPS 依現行 QA 是警告。 |
| `player_caption_audit.json` | 字幕、代表性畫面與縮圖、播放器的已確認缺陷／通過／未驗證項目。 |
| `browser_results.json` | localhost Chromium 的正常音軌控制與缺音軌回復、切集速度／名稱檢查。 |
| `caption_switch_results.json` | 切集造成字幕累積的瀏覽器重現狀態。 |
| `frame_metrics.json` | 5,723 個 Day02–60 字卡依原字型度量重算換行，配合抽取實際影格觀察；不是逐格看完所有影片。 |

JSON 內的工作區路徑、`player/*.png` 及 ffmpeg 原始 log 指向外部稽核環境，
不是應該存在於 Git 的產品檔案。二進位截圖、影音與完整原始量測 log 留在
`airport_series/recheck/`，不打包成「通過上架」證據。

兩種字幕錯誤必須分開理解：獨立 SRT 沒有時間重疊，但播放器的 TextTrack
切集時殘留舊 cues，導致不同集譯文同時顯示。機械行寬／讀速檢查也不等於
翻譯品質、逐句語音轉寫或實際 YouTube 字幕顯示都已驗證。

來源快照有獨立的 [provenance.json](../source-snapshot/provenance.json)。
原型的 `script_ready` 等欄位只是歷史值；本目錄的失敗／缺證據結論優先。

保存驗證已逐檔比對 487 份來源與複本 SHA-256；486 份完全一致，只有 Day01
私人預覽網址按 manifest 遮除。JSON 均可解析，文件相對連結可解析，未納入
影音或私有部署識別碼。原始 SRT 的空白也按原樣保存：`git diff --check`
會在 63 份歷史字幕報 1,155 個行尾空白；不清掉空白後再宣稱逐位元組相同。
排除這批歷史 SRT 後，新增文件與 JSON 的 diff whitespace 檢查通過。
