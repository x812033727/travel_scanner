# 後台合集：勾選集數、一鍵合併上架（設計）

2026-10-18 起草。站主要的流程：

1. 在 `/admin/videos` 勾選幾集（例如《種田娶妻打天下》第 1–5 集）。
2. 按一個鍵，依序接成「頻道片頭 → 所選各集 → 片尾（含 end screen 連結的版面）」。
3. 每集已經有的各語言 CC 與配音音軌，跟著時間軸一起合併，不必另外翻譯或配音。
4. 合併好的成片出現在後台，照一般流程上架 YouTube。

這份寫要加哪些東西、為什麼這樣選。現況是 2026-10-18 讀程式碼得到的，行號是當天的。

## 現況：哪些能直接用，哪些不行

| 項目 | 現況 | 出處 |
| --- | --- | --- |
| 合集 | 已有，但只接自動產線的作品：集數固定從 `VideoDramaSeries` 來，slug 寫死成 `<series>-full`，沒有「挑任意影片」的入口 | `docs/videos/BINGE.md`；`apps/api/app/video_automation/series.py`（`start_compilation`、`finish_compilation`）；`tools/video/automation/compilation.mjs` |
| 接片 | `tools/video/compile/` 會拿掉每集自己的片頭片尾，用 `-c copy` 接起來，再把頻道片頭片尾包在整支外面；各語言 CC 依每集起點位移後合併（`mergeEpisodeCaptions`） | `tools/video/compile/cli.mjs`、`plan.mjs` |
| 配音 | **合集從來不合併配音**；而且產線的 `dub` 只接受旁白一個聲音，多角色的漫劇被擋 | `docs/videos/DUBS.md`；`admin_service.py` 的 `_dub_allowed` |
| 片頭片尾 | 頻道片頭 5 秒；片尾 21 秒，最後 17 秒是 end screen 的版面。連結本身要在 Studio 從範本影片匯入，Data API 不能設定 | `docs/videos/BRANDING.md`；`tools/video/branding/outro.mjs` |
| 匯入的集數 | `tools/video/cli.mjs import` 只上傳 **720p 預覽**、封面與 `captions_zh-TW`。1080p 原檔只在站主電腦上；也沒有工作區、`approvals.json`、`timeline.json` | `tools/video/import/import.mjs` |
| 規格 | 匯入的集數是 24 fps（e015 是 23.917 fps）、約 -16 LUFS；產線與片頭片尾是 30 fps、-14 LUFS，**不能直接 `-c copy` 接** | 量到的 |
| 主機 | `video-worker` 有 ffmpeg，記憶體上限 5 GB，只能寫 `video_work`；API 容器沒有 ffmpeg | `docker-compose.prod.yml` |
| 後台介面 | 影片列表沒有多選；合集的下載只認系列合集（`compilation_slugs()`） | `apps/web/components/admin-video-browser.tsx`；`admin_service.py` |

## 決定（代理建議，站主 2026-10-16 說有問題照建議走）

1. **1080p 原檔要放上伺服器**，按鈕才能在後台直接用，不靠站主電腦開著。
   - `import` 多上傳一個 `master` 角色：原本的 1080p 成片，每集 85–160 MB，在單檔上限 2.5 GB 之內。
   - 已經匯入的集數，補傳一次 `master`。
2. **在主機的 `video-worker` 組合集**。所有輸入先統一成 1080p、30 fps、-14 LUFS（重新編碼一次，不用 copy），再接頭尾。
   - 24→30 fps 用補影格的重取樣，不用畫面插值，避免動畫變形。
3. **順序固定**：頻道片頭 → 勾選的各集（照勾選後排好的順序）→ 頻道片尾。
   - 每集的內容不剪；每集一個章節，章節標題是「第 N 集」。
   - 片頭片尾用該影片釘選的 branding 包（`branding.json`），與單集同一套。
4. **語言**：某個語言只有在**每一集都有**時才合併；缺一集就整個語言跳過，並在後台寫明跳過的原因。
   - CC：沿用 `mergeCaptions` 的位移方法，片頭的長度要算進去。
   - 配音：每集的 `dub_<locale>` 接起來；片頭、章節卡、片尾的位置補靜音，片尾的配樂照 `wrapAudio` 混進去。
5. **標題與說明**自動產生，站主可以改：
   - 標題：`<系列名> 第a–b集 | CC字幕`（站主 2026-10-17 定的格式）。
   - 說明：每集一行，加上章節時間。
   - 封面：預設用系列的季封面（一季一張、不放字、所有語言共用）。
6. **綁定各集版本**：記下每集 `master` 的 SHA-256。之後只要有一集重新匯入，合集就標成過期，要重做。
7. **上架照現有流程**：final 審核 → package → publish 審核，之後在 Studio 手動上傳或用 API 同步。
   - 多語音軌與 end screen 仍要在 Studio 手動設定；end screen 從範本匯入，起點是「片長 − 17 秒」。
8. **多角色漫劇的配音另外開一張票**：本機做好各集的 en／ja／ko 配音與 CC，用 CLI 掛到已經匯入的影片上（`dub_<locale>`、`captions_<locale>`）。
   - 站主規定：**等繁中確認之後才做**。合集功能本身不依賴這張票，有就合併，沒有就跳過。

## 要做的票（依序）

| # | 票 | 範圍 | 完成的樣子 |
| --- | --- | --- | --- |
| 1 | 匯入帶 1080p `master` | `tools/video/import/`、`apps/api/app/video_reviews/`（新角色、大小、型別） | `import` 會上傳 `master`；`--master-only` 可以替已經匯入的影片補傳；後台的檔案清單看得到 |
| 2 | 合集請求 API | `apps/api/app/video_reviews/`（或新的 `video_compilations/`）、一支 migration | `POST /admin/videos/compilations {title, episodes[], intro, outro}` 建一筆請求；工人用 `next`、`start`、`done` 取件；請求記下各集 master 的 SHA |
| 3 | 工人組合集 | `tools/video/compile/`（泛化成「任意 mp4 加字幕加配音」）、`tools/video/automation/` | 統一規格、包頭尾、合併 CC 與配音、寫章節與 youtube metadata，再 `review-push` final；下載與 VPS 上傳程式也認得這種合集 |
| 4 | 後台介面 | `apps/web/components/admin-video-browser.tsx`、BFF | 列表可以多選，拖曳排序，有標題、片頭、片尾的開關，按「建立合集」後看得到進度；完成後出現在影片列表，可以下載和審核 |
| 5 | 已匯入漫劇的多語配音 | `tools/video/import/` 的 `--languages` | 已做：`import --from DIR --languages` 把資料夾的 `description.<l>.txt`、`<l>.srt`、`dub.<l>.m4a` 照站主在語言面板勾的部件送成一批 `languages`（hand_pushed，綁定網站上最新的那份匯入成片；配音長度和成片差超過 0.5 秒就不送）。送出後要換成片：只剩這個指令送的、站主還沒核准的語言批次時，一般 `import` 照樣可以換，再送一次 `--languages` 取代舊批次；站主核准過就要走換版流程 |

1 是 3 的前提，2 和 4 可以平行做。5 獨立，不擋前面四張。

## 風險

- **重複內容**：單集和合集都上傳的話，YouTube 可能判定成重複使用的內容。合集要有章節、片頭片尾，說明裡寫清楚是連看版。
- **主機資源**：一季合集可能超過 1 小時。暫存空間需要來源的 1.5 倍再加 2.5 GB；記憶體上限 5 GB，要串流處理、不整支載入。
- **成本**：主機重新編碼一次的 CPU 時間。一季 60 集約 90 分鐘，估計要幾十分鐘的編碼。
