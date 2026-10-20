# 品牌故事製作接續｜2026-10-20

本次已完成影片工具配對與正式狀態唯讀盤點，並把 A01 r47 六章製作包整理成逐句旁白表與逐鏡表。站主最新選擇先交付 PR 與問題清單，詳見 [ISSUES.md](ISSUES.md)。**目前是離線交接，沒有新增音訊、插畫或成片。** 既有劇本、來源、念法與獨立審稿均未改寫。站主本次指示可使用影片工具權杖配對、繼續製作並送 PR；本匯出本身不代替實際製作的查核、預算或採用關卡。

## 可直接使用的資料

| 檔案 | 用途 |
| --- | --- |
| [A01-narration-cues.tsv](A01-narration-cues.tsv) | 六章 52 句原文、場景與句子 ID、54 筆待查主張的對應；不是時間字幕 |
| [A01-shot-list.tsv](A01-shot-list.tsv) | 50 場景的原提示詞、運鏡、主張對應；其中 49 個是靜態插畫 shot，不代表要新買 49 張 |
| [live-status.json](live-status.json) | 已配對 API 的限範圍狀態快照，含現有 QA 例外與語言結果；不是完整主機盤點 |
| [capture-live.mjs](capture-live.mjs) | 透過配對憑證只做 GET，匯出必要狀態；不保存權杖或完整審核 payload |
| [production-status.json](production-status.json) | 上游檔案 SHA-256、逐章數量、實際未通過的關卡與 12 項待決發布資料差異 |
| [build.mjs](build.mjs) | 完全離線、可重跑的匯出與一致性檢查；不呼叫供應商、不匯入、不寫核准 |

原始檔是 [r47 六章交接包](../brand-stories-pilot-v2-20261015/preproduction-20261016/A01-worker-handoff-r47-canonical-20261019/README.md)，其 manifest SHA-256 為 `3edb9c375bcef6b01adc4e7bd14eec3757dd907d16a175247f8468a063465fb2`。兩位既有讀者對 r47 敘事均通過；既有轉換審查也通過。這些結果只涵蓋各報告列出的離線範圍，54 個主張仍全是 PENDING，不能據此生成 worker 的已查核或已聆聽收據。

## 接續次序

1. **配對與唯讀現況已完成。** 正式站 `https://mokaair.com` 的影片工具 login 使用裝置配對；站主只在後台核對短碼並按允許，權杖不貼聊天、不放 Git。雲端可透過 CLI `main` 的 `home` 參數把私有憑證存到 `/workspace/.private-video-tool/.mokaair/video-tool.json`，後續 CLI 也使用同一參數，不修改系統 HOME。這條路徑在 checkout 外；不要把它加入 PR 或製作包。
2. **核對已存在的工作。** `brand-stories-adapt` 的 B25、A41、A42、C21、B26 在既有工作票已有正式匯入及開拍紀錄；README 開頭的「尚未匯入」是較早狀態。先讀回每集階段、阻塞原因及花費，不能從這台新建的空白開發資料庫推論正式站沒有影片。作品同時製作數曾設為 2，五集都完成後按原決定恢復 1；沒有現況證據時不改設定。
3. **A01 使用精確 r47。** 新近驗證的編輯包為 50 場景、52 句、8 組伏筆，零 lint errors、39 warnings；六章包零 errors、38 warnings。必須使用受保護的採用流程並綁定實際來源查核／聆聽收據，不能直接覆寫正式工作區，不能捏造 `auto.json` 已完成狀態。12 項發布欄位差異詳見 JSON 引用的 metadata-delta，日期不能冒充本次新查核日。
4. **先列完整批次價格，再做付費生成。** 本次讀回 B18 v2 的專用上限是 US$5，不擅自調高。含既有支出、保留額、文字、配音、圖片、judge、轉錄、配樂與有上限的重試，每片合計不超過 US$25。49 個 shot 是場景數；正式素材重用狀態、角色設定圖、重畫次數與單價尚未讀回，故本包不給虛構總價。付費前照 brand-story 技能一次呈現整批張數及總額。
5. **量實際旁白。** 此 A01 compact 版本的獨立目標是正文 420–480 秒。250／275／300 CPM 的場景模型估計為 450.4／414.1／383.0 秒；其中 275 CPM 低於下限。估計不代替音訊；不能減慢語速、補空白或重述湊長度，不能拿片頭片尾算正文。其他品牌故事仍依其各自規格，不套用 A01 例外。
6. **看片與後續集數。** 圖像固定 MiniMax `image-01`、精確 `{"preset":"cute-mystery"}`；既有匿名示意圖提示詞原封保留。完成音訊及圖像 QA 後仍須站主看成片。B18 依既有規定等 A01 成片、帳本及看片通過才進正式製作；新五集與已開拍改編五集的既有指示各自保留。語言由站主在成片後選擇。

## 本次連線狀態

2026-10-20 已透過專案既有裝置流程完成配對，權杖僅保存在 checkout 外私有目錄，不入 Git。以工具權杖成功讀回正式設定、媒體狀態、影片清單與審核；以 GitHub REST 成功建立 [PR #1609](https://github.com/x812033727/travel_scanner/pull/1609)，保留 `no-auto-merge`。早期 curl CONNECT 403、GitHub GraphQL Forbidden 均保留在工作紀錄，但已不能當成目前所有 API 不可達的結論。環境設定草稿另保存了兩個目的地主機，未據此宣稱已發布。

目前缺少的是正式工人的章稿、時間軸與媒體工作檔存取，不是影片工具配對。站主已選擇先交付本 PR／問題清單；沒有匯入、正式設定變更、重試工作、付費生成、上傳或自動合併。

## 驗證

從 repository 根目錄執行：

```bash
node docs/videos/brand-stories-pilot-v2-20261015/preproduction-20261016/A01-editorial-candidate-20261019-r47/build.mjs --check
node docs/videos/brand-stories-pilot-v2-20261015/preproduction-20261016/A01-worker-handoff-r47-canonical-20261019/build.mjs --check
node docs/videos/brand-stories-resume-20261020/build.mjs --check
npm run check:tasks
```

更新匯出只跑最後一支 builder、不加 `--check`。它逐字比對章檔與合成稿的旁白／畫面資料，確認 54 個主張完整對應，並固定上游兩個 manifest hash；任何上游版本改動須明確重新檢視，不靜默採用。這些命令不驗證實際音訊、畫面或正式站。

配對已完成的環境若要更新唯讀快照，可執行：

```bash
NODE_USE_ENV_PROXY=1 node docs/videos/brand-stories-resume-20261020/capture-live.mjs --credential-home /workspace/.private-video-tool
```

此指令會更新 live-status.json 的觀察時間與狀態，需檢視差異；不會修改正式站。不要把憑證檔複製到 repository。
