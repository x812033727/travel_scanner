# dots 製作交接

持久製作工作區：`C:/Users/x8120/mokaair-work/dots-series/`。

任務：`2026-10-03-dots-complete-course`；分支：`codex/dots-complete-course`。

已固定的決定：繁中 16 課＋總目錄、真實截圖逐步教學、Google／Slack、生活與工作六應用、不要求程式基礎、全套驗收後一次推出。影片正文每支至少八分鐘，YouTube 公開採站主 Studio 流程。

待完成狀態以 `ACCEPTANCE.md`、工作區 `STATE.md` 與驗收收據為準。尚未公開前，17 個 slug 的 publish hold 必須保留。既有帳號私有內容與原有工作不能作示範資料或停止測試。

2026-10-04：17 篇候選內容、16 份文字製作包、六套合成素材已完成，沒有音訊或成片。真實拍攝逐項交接見 `CAPTURE-LIST.md`。原始 Chrome 控制中斷後，站主指定改用內建瀏覽器；Cua 的 AX wrapper 逾時，既有 browser handle 的 `tabs.get` 加 `playwright.domSnapshot`、locator 和 `tab.screenshot` 曾可用。後續沿用這些有文件的入口，避免重新啟動建立流程。內建瀏覽器的新示範 dot 已命名「讀書會小幫手」、選擇 Teal，略過 Google 與本機連線；02 兩版合成提示的真實回述通過，完整操作與影片節奏仍待驗。原始位置／識別碼只保存在外部證據，不放公開素材。初次背景建議可能帶出已連線外掛的私人專案；公開素材只取合成練習及局部設定對話框。UI 的「新對話」會回普通 ChatGPT；接續 dots 請回已驗證的示範 dot 網址。最後返回時分頁控制再度逾時，03 canonical 尚未成功送出，不要假定該課已完成。

相關驗證：內容包、工具合約、API pipeline、lint:web、typecheck:web、check:i18n、build:web、六項 dots UI 檢查通過，最終桌面／手機總目錄再驗通過。Node24.19完整 `test:tools` 共1475項：1467通過、5失敗、3略過；Hook失敗單獨重跑通過，另四項為POSIX假媒體工具及Windows symlink權限需求，其後查新 origin/main，相關修正已由 `2026-10-03-assemble-test-portable-tool-boundary` 與 `2026-10-03-anime-input-test-windows-junction` 落地，本票未保留重複待辦。不宣告全CI綠燈。

實作中發現：另一張活躍票宣告占用整個 `apps/api/tests`。本票未越界修改該目錄。現有 `test_guide_series.py` 的 registry 清單有固定預期；增加 dots 系列需要協調該檔一行預期更新，或等待占用票釋放後再完成。新增獨立驗證放在本票自己的 tooling 目錄。

交接前已保留內建瀏覽器示範分頁並復原其暫時 viewport。Chrome 舊 viewport 的復原請求因 debugger 已中斷而無成功確認；下次恢復 Chrome 控制時讀回並復原。原始 screenshots 仍留在 repo 外；02 的操作紀錄為 `reviews/lesson02-capture-log.json`，不能把部分回述當作連接、排程或整課完成。P2 路徑覆核已關閉：兩套 Python 共 34 案例中 32 通過、2 個 Windows 檔案 symlink 案例略過；七個獨立真實 junction 越界測試皆為零外部讀寫／安裝。
