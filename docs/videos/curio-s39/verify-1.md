# S39 R1 作者查核與獨立覆核交接

日期：2026-10-20。**本頁是作者自查，不是獨立盲讀通過報告，也不是語音／插圖開工核准。**

## 本版鎖定

| 檔案 | SHA-256 |
| --- | --- |
| `video.json` | `cfd7ffda2bdfb98e7cd6d0ad9a909878ee92f3fcbabf4aa18a96c4276797e344` |
| `script.md` | `ede55e6eb8a7873c2b962c33176312e8bd4c2efcfb2bfaab6c74374f3d2e4d64` |
| `claims.md` | `dad89de8f2f224ccdc251a521e19ede70985ba9e6fd7d98d6911af5cace193f1` |

原文版本／SHA-256 均在 [research.md](research.md)。PerseusDL Suetonius 拉丁原文第 82.2 節逐字有 `etsi tradiderunt quidam`、`καὶ σὺ τέκνον`；GITenberg Thomson/Forester 譯本的腳註 97 才推測拉丁語 `Et tu Brute!`，此兩層不能混寫。Plutarch A. H. Clough 編英譯《Caesar》《Brutus》與莎士比亞第三幕已從固定全文重開；Plutarch 未核希臘原文，影片只用該英譯支援敘事動作及沒有該句台詞的觀察。

## 作者自查結果

- `video.json` 共 90 張 `shot`，正文插圖比例 100%，無連續文字卡；`cute-mystery`、Sulafat、標準配樂設定、19 個 `loops` 齊備。插圖只用人物角色、空白文件、舞台與古代場景作示意；不要求模型寫希臘文／拉丁文、不畫血傷、遺體或可辨識的人名。作者已逐景檢視 90 個提示詞，**仍須獨立畫面覆核及生成後視覺檢查**。
- `lint --slug curio-s39 --json`：0 error／0 warning；估 9:44，全片共 93 句。開場章結束約 00:40，片尾章起約 09:25，估正文 **8:45**；實際旁白生成後需再依時間軸確認至少 8 分鐘。
- `script --slug curio-s39` 已從同版 JSON 生成；`claims.md` 對應 93 句，作者逐項對照 [research.md](research.md)。關鍵界線：`cs032` 袍被扯時先喊，不把 `cs039` 的第一刀呻吟擴張成整天失語；`cs051` 是 Suetonius 引介的希臘語傳說，不是確定臨終錄音；`cs056–061` 的 Plutarch 兩篇同作者，不能當兩位目擊者；`cs073–075` 的拉丁語腳註屬後編者；`cs082–084` 分清 Decimus 與 Marcus。
- 工具只做 **dry run**：91 句 TTS 請求，約 2324 billable characters、Gemini 本月免費額度顯示足夠；MiniMax 90 張插圖，首次約 US$1.22，最多三次嘗試的圖片上限 US$3.65。按同系列配樂約 US$0.08 預留，**整集圖＋樂建議上限 US$3.73**，實際仍以送單前報價為準。未生成付費媒體。
- `npm run test:docs-videos`：236/236 通過；`npm run check:tasks`：exit 0，僅其他既有任務的 stale／scope 重疊警告。

## 下一關

1. **全新上下文的讀者**只取 `node tools/video/cli.mjs narrative --slug curio-s39` 產出的劇本與正式十三題，先密封回答，不先看本頁、來源或作者說明。特別量 `no_recap`、`chapters_link` 與末章是否仍繞回已給的答案。
2. 另一位獨立查核者以本頁 SHA 鎖定 `video.json`，對 [research.md](research.md) 固定來源逐句覆核 93 句及 90 個提示詞；查是否把拉丁語腳註寫進古文、把兩位 Brutus 混成一人、把 Plutarch 英譯冒稱希臘原文、或把舞台畫面偽裝成史實。
3. 兩關皆通過且 R1 雜湊不變，才可進行本地委託的劇本／音訊關卡；仍需旁白逐句 ASR 與媒體支出上限記錄，才開圖。若改劇本，重生成 `script.md`、重跑 lint、重做新版本獨立閱讀。
