# 2026-10-09 改寫與靜態畫面審查

## 這次完成的內容

單一案例：官方 first-mod 工具呼叫計數器。順序為看見效果、分清角色、理解事件、載入前檢查、三個檔案、操作與核對、改字與歸零、下一步。五張原創 SVG 沿用同一版面，沒有沿用原片的多套生活比喻。

新版 `video.json` SHA-256：
`7e079be13727705f983319e9ef5f4ebf21e5a82a69187a40babcbc05994b9521`

原始來源快照 SHA-256：
`bd703aad6591a898ecbb46a824b76cfa2a5cdab05a856a857b8dbb50fad6103c`

139 句旁白、68 場景、93 個畫面狀態。現有估算器給出約 10:07，最長單張 10.9 秒、平均 6.5 秒。這是撰稿／節奏估算，不是媒體測量；最終語音與正文長度仍須重新量測。

## 審查與修正

獨立閱讀審查先修正四處：畫面上的一行文字是 Mod 的結果；計數從模組載入後累積；單次工作比較前後差值；模組 JS 環境與 Bash 指令沙盒的範圍分開說清楚。`script.md` 與 JSON 旁白逐句一致。

獨立靜態審查查看全部 93 個狀態的接觸表及 10 張放大畫面，未發現文字裁切或重疊。它另外抓到「只顯示 0→1，旁白卻先說兩次」的不同步；已改為 mc005 說第一次增加、mc006 配 1→2。四張大字卡縮短標題，避免「狀態、需要、出現、顯示」拆行。結尾改成簡短可執行的下一步，估計 9.9 秒。

靜態重繪結果：93 個狀態，版面問題 0、估計超時問題 0。畫面保留「示意」「官方文件」「預期」等來源界線；沒有偽造的終端輸出或本機執行成功。

最後差異只將查詢指令卡縮成「指令在哪？先查載入」以避免拆詞，沒有修改旁白或計數邏輯。主協調者已重繪並放大檢查該張；最終預覽 `review.json` 綁定上述新雜湊。

## 本機交付位置

以下是本次工作機的實際檔案位置，不是公開媒體連結：

- 逐張畫面與旁白：`C:/Users/x8120/mokaair-work/mods-clarity-20261009/preview/storyboard/index.html`
- 狀態、雜湊、版面與估計節奏：同目錄 `review.json`
- 畫面：同目錄 `frames/`；原始 SVG 在本 repo 的 `assets/`
- 完整原稿與核准快照：`C:/Users/x8120/mokaair-work/mods-clarity-20261009/source/`
- 官方來源／版本紀錄：同工作根目錄 `research/FACTS-AND-DEMO.md`
- 未執行 Mod 的原因與隔離工具收據：同工作根目錄 `demo-evidence/STATUS.md`

完整轉場 render 在 13 個狀態後由本次工作寫入 STOP，保留快取；之後以同一個 renderer 的靜態模式繪完全部狀態。靜態 preview 不會寫成正式 frames manifest、音訊或 final 核准。瀏覽器互動檢查連續逾時，故此紀錄不宣稱已在瀏覽器完成翻頁操作；圖像本身已逐張審查。

## 程式檢查

使用 bundled Node 24.19，沒有更新全域 Node 或 Claude CLI。

- 影片 lint：0 errors、0 warnings。
- 提示詞與 register：27/27 通過。
- 針對性 automation 檢查：6/6 通過，包含既有翻譯提示雜湊、settle 與停頓行為。
- 影片文件測試：199/199 通過。
- 文件測試收集檢查：2/2 通過。首次失敗是新範例的巢狀 `.test.ts` 被當成正式測試；現改為 `.test.ts.example` 並記錄準備方式，未更動測試排除規則。
- 完整 tools 測試沒有得到通過結論：遇到既有 Windows `ERR_UNSUPPORTED_ESM_URL_SCHEME (c:)`，隨後沒有進度；已停止本次測試 runner。對應既有票 `2026-10-07-windows-video-test-imports`。
- reference comparison 個別重跑仍因 Windows ffmpeg 的 `--range 4-6` 輸出零影格失敗；與既有票 `2026-10-07-windows-reference-comparison-ffmpeg` 一致，相關程式未被本次修改。沒有將此失敗當成通過或暫時負載問題。
- 任務格式檢查通過；已有的過期 claim 警告另列在日誌。`git diff --check` 通過。

完整測試日誌位於同工作根目錄的 `test-tools.log`、`test-docs-videos.log`、`check-tasks.log`。提示詞測試不證明生成品質；靜態畫面審查也不證明播放與音訊品質。

## 接續製作

下一階段記錄於 `tasks/open/2026-10-08-mods-tutorial-revision-production.md`。本輪沒有付費語音／圖片生成、後台匯入、上傳或發布。原片有另一份英文配音 producer lease，程序存活狀態未確認；保留原片來源、媒體與核准。新稿需自己的來源綁定、旁白、ASR／音訊審查、成片與字幕檢查、後台雜湊讀回及適用核准。

自動核准審查拒絕了隔離 CLI 的 `--version`／`plugin validate`／`plugin test` 組合執行，唯一理由為 `blocked by policy`。沒有改用其他路徑重試；`demo/` 只交付可讀來源和待執行測試範本。
