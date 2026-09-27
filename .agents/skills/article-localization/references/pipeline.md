# 翻譯產線：`tools/article-localization/pipeline.py`

全文與欄位契約在 `tools/article-localization/README.md`；這裡是操作時要記得的部分。所有指令從 `<ROOT>` 跑，用 API 的 Python 環境（`uv run --project apps/api python ...`），否則沒有真的 `GuideDocument` 驗證器。

## 它做什麼、不做什麼

- 呼叫本機已用 **ChatGPT 帳號登入**的 Codex CLI 翻譯欄位與 SVG 文字；設了 API key 或自訂 provider 會被拒絕。子行程用 dotted config 覆寫關掉 MCP server，不改全域設定。
- 只寫 `work/<slug>/<locale>/` 的 job 目錄（預設在 `docs/article-localization/` 底下，`--work` 可改到 repo 外）。**不寫內容包、不寫 public 圖、不匯入、不發布。**
- `render.mjs` 用 repo 的 Playwright 與 Sharp 把 SVG 排版、出 raster 與預覽 PNG，可以縮字塞進原框，不改字、座標、形狀。

## 子指令

| 指令 | 用途 |
| --- | --- |
| `prepare` | 建 job：`source.json`、`fields.json`、`prompt.txt`、`output-schema.json`、`artifact-manifest.json` |
| `run` | 跑翻譯；`--workers` 1 到 3（預設 1）；`--retries` 0 到 2（預設 0，只重試明確認得的連線／502／503） |
| `status` | 看每個 job 的狀態 |
| `reset` | 明確重設某個 job，**必須** `--reason`；舊 receipt 與原因會留下 |
| `materialize` | 不呼叫模型，從 `translated-fields.json` 重建 document 與 SVG、重跑全部檢查；手改譯文後用；綁定前的舊 pilot job 升級時必須帶 `--reason` |
| `migrate-prepared` | 只給「prepare 過但從沒 attempt」的 job 補綁定；拒絕有 lock、有 attempt、失敗或額度狀態的 job |

選擇器：`--batch <id>`（baseline 裡的批次，最多 20 篇）或 `--slugs a,b`（最多 20）；`--locales en,ja,ko,zh-CN` 縮小語系。`--include-existing` 替已經有譯文的語系建「只翻圖」的 job，不重翻正文。

## 續跑、停止、失敗

- 重跑同一批：已驗證的 job 會重算雜湊後跳過。baseline 變了、和已 prepare 的輸入衝突，會拒絕而不是覆寫。
- **停**：建 `work/STOP`（或 `--stop-file` 指定的檔）。進行中的 CLI 呼叫會跑完並保留結果，不再開新 job。要再跑就刪掉那個確切的檔。
- **行程當掉**：`running.lock` 會留著。先確認 lock 裡的 PID 真的不在了，才刪**那一個** lock，然後 `reset` 受影響的 job。
- **額度或登入失敗**：排隊中的 job 全停，永不自動重試。額度真的重置之前不要 `reset` 被額度擋下的 job；沒有任何設定能繞過服務上限。
- **內容、schema、未知失敗**：一律人工看。要改譯文而不再呼叫模型：只改 `translated-fields.json`，再對那個 slug 與 locale 跑 `materialize`。`source.json`、`fields.json`、attempt 紀錄不准動。

```bash
uv run --project apps/api python tools/article-localization/pipeline.py reset --slugs example-slug --locales en --reason "Resolved the recorded transport failure"
uv run --project apps/api python tools/article-localization/pipeline.py materialize --slugs example-slug --locales en --reason "Apply reviewer corrections to translated-fields.json"
```

## 狀態的意思

- `translated`：欄位與 schema 檢查過（數字、URL、inline code 要保留；抄原文、佔位符、錯字體、超長會失敗；繁簡互抄會被字形檢查擋下）。
- `rendered`：自動排版檢查也過了。
- 兩者都**不是**審稿通過。`reviewed`、`editorial_review_complete`、`visual_review_complete`、`glyph_review_complete` 由獨立審稿者寫證據後才算；`assemble_bundle.py` 讀的是 job 目錄裡的 `review.json`，要有 `text_reviewed`、`visual_reviewed`、`glyph_reviewed` 都是 true，且 `document_sha256`、`artifact_manifest_sha256` 等於目前的 receipt。
- 沒有可編輯 SVG 的 raster 會列在 `raster_review_required`，不當成沒有字；審稿要在 `review.json` 的 `source_rasters` 寫明 `editorial_overlay: false` 與理由才能重用。
- 只有 raster 圖、正文已有譯文的語系會變成 `mode: review-only`、`status: pending_review` 的 job，不呼叫模型，但不會自己消失。

## artifact 綁定

每個 job 的 `artifact-manifest.json` 以位元組雜湊釘住所有輸入、attempt、譯文、document、圖與 render receipt，`receipt.json.artifact_manifest_sha256` 再釘住 manifest。任何檔案增刪改都讓續跑失效；只改 receipt 的狀態字不會讓 job 變成 rendered。重新渲染會改 render receipt 與 manifest 雜湊，即使文章與圖的位元組沒變，所以審稿要在最後一次渲染之後做，或重新比對位元組後才沿用。

## 站內連結與 credit

- 譯文裡連到四個已驗證公開路由（`/guides/howto`、`/destinations/hanoi`、`/destinations/singapore`、`/guides`）的連結會機械地換成目標語系；其他帶語系前綴的站內路由、別名、帶查詢或片段的變體會讓 materialize 停下來等人看。
- AI hero 的 credit 只認 `Mokaair · AI 生成示意圖`／`AI 生成，非實拍` 這一組：翻描述，但要保留 `Mokaair · ` 前綴與 AI 揭露；攝影師、授權、來源網址不動。

## 測試

```bash
uv run --project apps/api python tools/article-localization/test_pipeline.py
node --test tools/article-localization/artifact-integrity.test.mjs
node --test tools/article-localization/render-layout.test.mjs
uv run --project apps/api ruff check tools/article-localization docs/article-localization
```
