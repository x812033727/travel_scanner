# 補語系踩過的坑

每條後面是出處，細節去那裡讀。

## 來源與基準

- **公開 API 的文件帶傳輸欄位。** `version`、`published_at`、`modified_at` 沒拿掉就算雜湊，得到的是錯的值；batch009 第一版的所有 job 因此作廢重綁。（`tasks/done/2026-09-21-localize-seoul-airport-tmoney-batch009.md`）
- **舊 worktree 的內容包比 main 舊**，別拿來當翻譯來源；一律從正式站的已發布版本或新快照開始。（同上）
- **原文本身有錯最花時間。** batch009 被獨立審稿退了三輪（v4、v5、v6 都 0/8 通過），每輪都是原文的事實或圖解問題；desk-cable 的原文把「標記」連到 AI Token 文章。翻譯前先讀原文、先修原文，別在譯文裡偷偷修。
- **修已公開的原文要收據。** 發布器預設拒絕改已公開的文字；要一起發布就走 `source_correction.py`，收據綁新舊雜湊與 pointer。（`tasks/done/2026-09-21-authorize-reviewed-source-corrections-in-localization.md`）
- **原文 SVG 本身也會裁字、壓線。** batch009 的 Incheon 圖在 zh-TW 就把標籤裁掉；只動 `<text>` 節點，路徑、形狀、1600×900 不動，並記下新舊雜湊。

## 產線與 bundle

- **部署後內容包的原始位元組可能與 bundle 不同**（欄位順序、預設值序列化），batch008 的 dry-run 因此在寫入前停下；現在以 `ArticlePack` 驗證後的內容比對（PR #642）。其他任何文件或 metadata 差異仍會停。（`tasks/done/2026-09-22-compare-deployed-localization-packs-by-validated.md`）
- **合併與部署之間 main 往前走了**：batch018 第一次部署在執行前就停下，重新核對新的合併內容與 CI 才部署。發布前一定再匯出一次快照、再比一次。（`docs/article-localization/releases/batch018/README.md`）
- **CI 的 release-safety 以前只看工具目錄**，純內容 PR 或 API／migration 改動不會跑 PostgreSQL 發布測試；已把 `apps/api/**` 與 npm manifest 加進觸發條件。本機的 PostgreSQL skip 不能當成發布安全的證據。（`tasks/done/2026-09-23-localization-release-ci-content-api.md`）
- **失敗的 publish 階段用同一個 state 目錄重跑**，journal 會對帳；換新目錄等於丟掉重複保護。
- **`publish_bundle.py` 不看 `publish_holds.json`**；那個檔只擋 `guides-import --publish`。要擋某篇就別把它放進 bundle。
- `migrate-prepared` 不碰任何有 attempt 或失敗狀態的 job；舊 pilot job 要用 `materialize` 加 `--reason` 升級，然後每個語系重新渲染、重新審稿。

## 翻譯品質（審稿抓到的嚴重項）

- **rich_paragraph 兩段 inline 之間少空格**：前端直接相接，en 會印出 `andlabel`；en 與 ko 都犯過。審稿與機械檢查都要看 inline 的邊界。
- 字面誤譯：「手腳」譯成 legs/feet；日文「急折」譯成「急に折り曲げ」（變成「突然地」）。
- 標題要對齊內文小標的譯法；審稿者常把標題疑慮放在另一欄，協調者要記得處理，SVG 的 `<title>` 一起改。
- 日文、韓文、en 裡的漢字錯字（北竹／北竿、不存在的韓文音節）交給 `translation_checks.py`；它有合理的誤報（台灣地名、引用的中文標題），要讀清單。
- 英文比原文長很多、觸發 `text_length` 警告是正常的，不為消警告刪字。

## 環境

- **auto 模式分類器擋「把腳本灌進正式站容器」**，包括 `export_snapshot.py` 與 `publish_bundle.py`；換寫法重試會被當成繞過。這是 Claude 改走路線 B 的原因。
- Windows 上 Playwright 的 `chromium-*/chrome-win64/chrome.exe` 可能啟動失敗（WinError 14001 side-by-side）；改用同版本的 `chromium_headless_shell-*` 當 `CHROMIUM_BIN`。
- 重導向的 stdout 在 Windows 可能是 cp1252；讀寫中文 JSON 的 Python 一律 `PYTHONUTF8=1`（`pipeline.py` 自己會 reconfigure）。
- 舊的翻譯票卡在 `review`、scope 與你重疊時，`tasks claim` 會拒絕；確認沒有人在寫、PR 已合併後才用 `--force`，而且不要改那張舊票。（batch009、PR #642 的票都遇過）
- 本機的工作目錄與證據目錄在 repo 外；`docs/article-localization/` 底下產生的 `work/`、`baseline.json` 等沒被 git 忽略，`git add -A` 會把它們帶進 PR。

## 驗收

- HTTP 200 不等於正文完整：過去的批次逐語檢查正文、圖、圖說、credit、canonical、hreflang、同語系站內連結，桌面與手機 viewport 各一。手機上的寬圖解是置中截圖，完整標籤以桌面與本機渲染為準；這是 viewport 驗收，不是實機。
- sitemap 要把分頁讀到終止游標（batch024 是 1000＋1000＋16），確認新網址都在 XML 裡。
- 公開限流：驗證腳本循序、間隔 1.3 秒以上。
