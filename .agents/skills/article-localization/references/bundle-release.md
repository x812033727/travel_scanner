# 路線 A：快照、baseline、bundle、發布

腳本都在 `docs/article-localization/`，各自的 docstring 是權威；`tools/article-localization/README.md` §Reviewed release flow 是總覽。`<BASELINE>`、`<JOBS>` 同 SKILL.md；bundle 與 journal 的 state 目錄放 `<WORK>`（repo 外），`releases/<batch>/` 只放紀錄。

## 1. 正式站快照 → baseline

每一批都從**當下部署版本**的唯讀快照開始，不重用舊的 `baseline.json`：repo 或資料庫一漂移，舊雜湊就錯。

```bash
# 唯讀：把腳本從 stdin 送進正式站 api 容器，輸出存成 docs/article-localization/ 底下的 production-baseline.json
MSYS_NO_PATHCONV=1 <SSH> "cd /root/travel_scanner && docker compose -f docker-compose.prod.yml exec -T api python -" < docs/article-localization/export_snapshot.py > <SNAPSHOT>
# 從 <ROOT>：讀 production-baseline.json，寫 baseline.json 與 source-differences.json（固定寫在 docs/article-localization/ 底下）
uv run --project apps/api python docs/article-localization/build_baseline.py
```

- 灌腳本進正式站容器，auto 模式的分類器會擋，而且換寫法重試會被當成繞過；要嘛切 Manual 讓站主逐次核准，要嘛把一行指令交給站主跑。Claude 在 2026-09-24 因此改走路線 B。
- 快照裡有資料庫獨有、repo 沒有內容包的文章時，`build_baseline.py` 會拒絕（`Export database-only articles first`）。
- **翻譯前先讀 `source-differences.json`**：正式站與 repo 不同時，builder 以正式站的文件為準，差異要逐項判斷（後台改過的、repo 較新但沒發布的）。
- 批次最多 20 篇，id 是 `batch-001` 這種；每篇釘住內容包、文件、資料庫、圖檔雜湊，還有 `locale_provenance`（`repository-only`、`database-draft`、`database-published`）。

## 2. 翻譯、渲染、審稿

見 `pipeline.md`。審稿者在每個 job 目錄寫 `review.json`，綁 `document_sha256`、`artifact_manifest_sha256`、每張圖的雜湊。

## 3. 組 bundle

```bash
uv run --project apps/api python docs/article-localization/assemble_bundle.py --baseline <BASELINE> --work <JOBS> --slug <S1> --slug <S2> --output <WORK>/bundle-<batch>
```

- 每篇要有五個語系的文件；既有語系的完整正文保留；新譯文裡的站內文章連結變成「看發布狀態」的 ArticleInline，譯文不會連到別語系的私人草稿。
- 只複製雜湊釘住、審過的圖；寫 `release-manifest.json`，印出 `manifest_sha256`。**記下這個值，之後每一步都用同一個。**
- 選用旗標：`--prior-manifest`（前一批的 manifest，hub 依賴要用）、`--source-correction-review`（原文修正收據，見 §6）、`--repository-preservation-review`（見 §6）。都可重複。
- hub 文章是 `gemini-guide`、`claude-code-tutorials`、`ai-terms-index`；它們等所有依賴的課程公開後才發布。

## 4. 安裝進 repo（內容 PR）

```bash
uv run --project apps/api python docs/article-localization/install_bundle.py --bundle <WORK>/bundle-<batch> --baseline <BASELINE> --manifest-sha256 <SHA> --work <JOBS>
```

只改內容包與 public 圖，不匯入、不發布。durable journal 記下每個目的檔的前後位元組，中斷可冪等續跑；每個 job 的 receipt 綁 journal、job、artifact manifest、review 與安裝的檔。證據有變或不完整就拒絕。安裝完開內容 PR（翻譯票的 scope），等 CI 綠、合併。

## 5. 部署之後發布

1. 部署含內容 PR 的版本（skill `deploy`；已經有就不必）。Codex 的批次用分階段驅動，從 prepare 到最後一個內容階段持有暫停檔，規則在 `ops/release/README.md`。
2. **再匯出一次快照**，部署的來源版本、可見性、雜湊、語系狀態或 manifest 授權任何一項變了就停。
3. 在正式站 API 環境裡，同一個 bundle、baseline、manifest SHA、state 目錄、actor、`--deployed-root`，依序跑四個階段：

```bash
python publish_bundle.py --bundle <BUNDLE> --baseline <BASELINE> --manifest-sha256 <SHA> --deployed-root <APP_ROOT> --state-dir <STATE> --actor-id <ADMIN_UUID> dry-run
# 接著把 dry-run 換成 drafts、publish-articles、publish-hubs，其餘參數一字不改
```

- 只接受 PostgreSQL；每個階段都重算 `--deployed-root` 裡內容包與所有 manifest 圖的雜湊。內容包原始位元組不同但 `ArticlePack` 驗證後相同（欄位順序、預設值序列化）可接受（PR #642）。
- 用既有的編輯服務、serializable transaction、row 與 advisory lock、版本與文件雜湊、durable intent journal（`<STATE>/journal.json`）。repo 獨有的文章保持五個私人草稿；公開文章只發布被授權的語系。
- 失敗會印 `{"status": "stopped", ...}` 到 stderr、exit 1：**用同一個 bundle 與 state 目錄重跑**就會對帳，不會重複產生版本。不要換新的 state 目錄。
- 既有文件只准改圖的 `src`；要改已公開的文字只能靠 §6 的收據。
- 這條路不讀 `apps/api/app/guides/publish_holds.json`（那個檔只擋 `guides-import --publish`）。

## 6. 原文修正與 repo 保留

- `source_correction.py`：翻譯時發現**已公開**原文要改。收據放 bundle 的 `reviews/<slug>-<locale>.json`，含完整的舊公開文件、舊草稿與公開版本的雜湊與版本、修正後雜湊、RFC 6901 pointer 的 `before`／`after`；`/sources` 可整個陣列替換，pointer 不能重疊；原文 SVG 的新舊雜湊列在 `assets`。發布前重算全部雜湊，文章被改過或隱藏就拒絕。batch009 用過（PR #637）。
- `repository_preservation.py`：repo 裡某個**沒被選進這次發布**的語系有審過的描述要保留在完整內容包，但不匯入也不發布。收據放 `reviews/<slug>-<locale>-repository-preservation.json`。

## 7. 進度報告與驗收

```bash
uv run --project apps/api python docs/article-localization/report_progress.py --baseline <BASELINE> --work <JOBS> --output <WORK>/progress --bundle <BUNDLE> --journal <STATE>/journal.json --browser-evidence <BROWSER_JSON>
```

寫 `progress.json`、`progress.csv`、`progress.md`。它不從檔案存在推論完成；瀏覽器證據 schema 要每個 slug×locale 有 `document_sha256`、`manifest_sha256`、`published_version`、`url`、七個 checks（body、images、canonical、hreflang、links、desktop、mobile）與至少一個雜湊釘住的證據檔。過去批次的公開驗收：五語網址、桌面＋手機、頁首與圖解截圖逐張看、sitemap 分頁全讀、每張公開圖位元組比對。

## 測試（CI 的 `article-localization.yml` 跑同一組）

```bash
uv run --project apps/api pytest -q -o asyncio_mode=auto docs/article-localization/test_build_baseline.py docs/article-localization/test_assemble_bundle.py docs/article-localization/test_install_bundle.py docs/article-localization/test_report_progress.py
RUN_INTEGRATION_TESTS=1 uv run --project apps/api pytest -q -o asyncio_mode=auto docs/article-localization/test_publish_bundle.py
```

本機沒有 PostgreSQL 時整合測試會 skip；那不是發布安全的證據，要看 PR 上 release-safety job 的實際結果。
