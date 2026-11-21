# H07-v2 製作狀態（2026-10-18）

這是 H07《鐵面人》的隔離重製稿。原版 `curio-h07` 的檔案、已付費素材與影片網址不變；原版審核不核准本版的新雜湊。`build-video.mjs` 從原版稿產生本版的 `video.json`，明列刪鏡、改字與新增鏡頭，並核對所有沿用的句子 ID 與文字；它另會比對已核准的 `script.md` 旁白，但不會覆寫劇本。正式劇本由 `tools/video/cli.mjs script` 維護。原版兩輪覆核保留於 `../curio-h07/verify-1.md`、`../curio-h07/verify-2.md`。

## 目前可驗的製作結果

- 93 景／93 句，含正文 92 景與 outro 1 景。正文規劃 65 張 `shot` 插畫、27 張排版卡；插畫比例為 65／92（70.7%）。原版 59 張插畫不符合本版 `cute-mystery` 系列畫風，不能直接當新圖驗收。
- 劇本沿同一條證據線，分清 1669 年多熱密令、1698 年無名囚犯入獄登記、1703 年黑絲絨死亡補記與後世「鐵面人」傳說。馬提歐里仍是候選人；不宣稱已證實本名或鐵製面具。
- 站主於 2026-10-18 同意只刪重複揭露入獄登記的 `7c22ba05` 句與鏡。重建後，獨立史料複核通過、13 題敘事盲評全過；收據為本版 `verify-2.md` 與 `narrative-answers.json`。其後兩張姓名拼讀鏡頭改為來源卡、五個畫面提示詞修正，獨立差異覆核見 `verify-3.md`；插畫驗收再定向修正 13 鏡的畫面提示，紀錄見 `keyframe-qa-1.md`、`keyframe-qa-2.md`、`keyframe-qa-3.md`。93 句旁白與其 ID 均未改，正式 `script.md` SHA-256 仍為 `6BC0B08064685C1A79C63685F314924AFF0BB1ACB6572723DF5EE6D40EC48D29`；目前 `video.json` SHA-256 為 `F0060544216F7084C26677743BAE6AB139BBA6CA7D89836DB618791030D23502`。三語譯文也刪除舊句，其餘 93 句與中文來源相符。
- 最新 `lint` 為 0 error、1 warning：機械估算約 8.9 分鐘，略低於 9–11 分鐘目標；旁白時間軸以 30 fps 實測正文（不含 outro）531.2 秒／8:51.2，全段 537.43 秒／8:57.4，已過正文八分鐘門檻。2026-10-18 的 `tts` 執行紀錄為 93 次請求規劃、其中 **21 句實際新合成**、533 計費字元；21 個新 WAV 合計約 116.39 秒。`check-audio` 首輪對 93 句做 Gemini 轉寫並呼叫 Jev 1 次，留下 21 句旗標；快取重跑沒有新增付費請求。其後離線 Whisper 複核 21 句並再呼叫 Jev 1 次，排除 7 句辨識偏差，餘 14 句供站主試聽；這一輪沒有新增 Gemini 轉寫。
- **65／65 張**插畫已正式選定，三頁聯絡表已生成；`keyframes/manifest.json` SHA-256 `830A745FF07093365D8CD252A4E0D1EF1B948CA1086F47B6F72C407F4328C1F7`，機械評審 `needs_review` 為 0，定向修圖已逐張人工複核。媒體帳本累計 118 張成功圖片、117 次評審、1 筆終止失敗的圖片請求，圖片及評審伺服器估價共 **US$1.5795**。站主核准的**合計估算停手上限仍為 US$6**，含繁中音訊／QA、插畫及後台選定的三語配音／QA。外部 `review/spend-ledger.json` 以 US$0.50 預留已執行繁中音訊與 QA、以 US$2.50 預留三語配音與 QA，另保守計入失敗圖片最多 US$0.0035，暫估未分配 **US$1.4170**。這些不是供應商實際發票或帳戶餘額；若有新增付費階段，須先核對。
- 分鏡卡已於 2026-10-18 10:01 UTC 依上述 manifest 雜湊從 `/admin/videos` 讀回核准。`render` 首次畫出 28 個排版狀態、0 重用；`clips` manifest 為 65 個靜圖鏡頭、0 付費動畫秒數。以 `--intro-after-condensation` 合成的 `final.mp4` 有 16,903 影格、563.43 秒（約 9:23.4）、1920×1080／30 fps、H.264／AAC 立體聲；片頭插入第 1,670 格（55.67 秒），響度 -14.1 LUFS，SHA-256 `9B059CC58B3AA236558A895F96C3E443CA53CF3A0EFE086A6F3042BA746ADD72`。`checks.json` 為 `ok: true`、`problems: []`。
- 繁中、英、日、韓字幕分別有 99、103、109、107 個 cue，`captions/manifest.json` 各語均為 0 problems；英語 `0231d434` 已縮短以符合時槽。三語縮圖只調整標題斷行後重繪，28 個排版狀態全部重用；本機成片 `qa` 為 **11／11 通過**。手動 `qa` 與後續 `review-push --gate final` 各呼叫 Jev 政策判讀一次，共兩次，已納入外部費用預留。`final.mp4` SHA `9B059CC5…ADD72` 已於 2026-10-18 10:37 UTC 從後台讀回核准。站主在語言面板為 en／ja／ko 各勾選標題說明、字幕與配音，選擇時間為 10:37:54 UTC，已同步至工作目錄 `languages.json`。三語各 93 句配音、首輪轉寫及音訊差異 QA 已完成；站主逐語試聽並接受，收據見 `dub-qa-1.md`。

## 仍須通過的關卡

21 句繁中旁白已在前一版劇本核准後合成，兩套轉寫後音訊 QA 尚有 14 個旗標；站主已於 2026-10-18 試聽並回覆「旁白可以」。後續視覺提示修訂只改 `video.json`，未改已核准的 `script.md`；本機 `approvals.json` 的劇本核准仍綁定 `6BC0B080…0EC48D29`。`timeline.json` SHA `D43D89BA…98670DF` 的最新版音訊卡已由站主核准，並以 `review-pull --gate audio` 讀回。65 張插畫已驗收，綁定 manifest SHA `830A745F…28C1F7` 的分鏡卡已核准且讀回。**SHA `9B059CC5…ADD72` 的成片與 11／11 QA 已送至後台 final 卡並讀回核准。** 四語上傳包 `package` 檢查 4／4 通過，`upload/metadata.json` SHA `CE7D19F6…86236A` 的 `publish` 卡已核准並讀回。`languages` 卡 `6d0daec9-2789-4673-92d4-e8dfbc5f6074` 已送出，目前等站主完成 Studio 三語音軌上傳後再按「已上傳配音」。私人 Studio 上傳、新影片網址、四語播放核對與公開仍是獨立事項；站主表示稍後自行操作 Studio。任一完成標記都不得代替下一關的雜湊收據。

本機再次執行 `npm run test:docs-videos` 為 214／215；唯一失敗仍是無關的 `imported-long-languages/runner.test.mjs` 子程序退出，這次退出碼為 `3221226505` 且沒有輸出，並非 H07 斷言失敗。先前定向重跑該測試時前段用例通過，後三例因 C 槽 `ENOSPC` 失敗；H07 的 `lint`、十三題 `narrative`、`check:tasks` 與 `git diff --check` 均通過。C 槽在其他任務的測試暫存期間曾降至約 0–0.6 GiB，轉檔前量測約 3.8 GB 可用，現已完成 1080p 成片；已找到 11 個舊安裝器暫存候選，但 `Remove-Item` 被自動核准審查以 `blocked by policy` 拒絕，沒有繞過或刪除。後續重編或測試前須再量可用空間。

新成片採 `history-curiosity` 系列與 `cute-mystery` 畫風。第一章濃縮從 `0:00` 開始，合成時已明確使用 `--intro-after-condensation`，片頭在 55.67 秒插入；本機 `_branding/current.json` 未指定 `intro_at`，後續重編仍須明確指定。片尾使用 v4 endscreen；branding pin、字幕時間軸、三語配音與本機成片 QA 已核對。
