# 新聞自動化：主機上的操作與診斷

每個階段在做什麼、清單與啟用門檻的全文在 `docs/news-automation.md`；程式在 `apps/api/app/news_automation/`。這裡只放操作。

## 誰在跑

| 服務 | 做什麼 |
| --- | --- |
| `news-scheduler`（compose profile `news`） | 每分鐘：替到期的來源排掃描、把死掉的 job 標成失敗、重排孤兒候選、排每日清理 |
| `news-worker`（compose profile `news`） | `news` 佇列唯一的消費者；一般 `worker` 不讀這個佇列 |
| `/admin/news` | 來源、設定、審查清單、執行紀錄、各類別的啟用門檻 |

`news` profile 沒起來時什麼都不會跑：後台按的「立即掃描」「重新執行」都停在 Redis 等 worker。確認兩個服務都在：`docker compose -f docker-compose.prod.yml ps --format '{{.Name}} {{.Status}}' | grep news`。部署腳本要帶 `--profile news` 才會每次一起重建（`docs/news-automation.md` 的「Switching it on」第 1 步仍寫著腳本只帶 `--profile hotspots`，以主機上的腳本為準；少了就是主機變更，站主決定，走 skill `deploy`）。只手動起一次不夠：下次部署會重建別的服務、把它們留在舊映像。

## 兩個主機 CLI

都在 api 容器裡跑，不帶 `--apply` 就只看不寫。`--actor-email` 取容器 `ADMIN_EMAILS` 的第一位，用單引號包 `sh -c` 讓展開發生在容器裡、不印出來：

```bash
cd /root/travel_scanner
# 來源：驗證 apps/api/app/news_automation/sources.json 裡的每個來源，什麼都不寫
docker compose -f docker-compose.prod.yml exec -T api python -m app.news_automation.sources_cli
docker compose -f docker-compose.prod.yml exec -T api sh -c 'python -m app.news_automation.sources_cli --apply --actor-email "${ADMIN_EMAILS%%,*}"'

# 設定：只看
docker compose -f docker-compose.prod.yml exec -T api python -m app.news_automation.settings_cli
# 看一個變更會怎樣（不寫）
docker compose -f docker-compose.prod.yml exec -T api python -m app.news_automation.settings_cli --enable --writer-provider minimax --verifier-provider minimax
# 真的寫
docker compose -f docker-compose.prod.yml exec -T api sh -c 'python -m app.news_automation.settings_cli --enable --writer-provider minimax --verifier-provider minimax --apply --actor-email "${ADMIN_EMAILS%%,*}"'
```

**`sources_cli`**：`--file` 可換檔（預設 `sources.json`）。輸出 JSON 的 `sources[]` 每筆有 `action`（`create`／`update`／`unchanged`），乾跑時多 `valid`／`error`；`not_in_file` 列出資料庫有、檔案沒有的來源（不動它們）；`summary` 有四個計數。`--apply` 走和後台一樣的 service（驗證、稽核列）；驗證不過的來源仍會寫進去，但是停用、`last_status=validation_failed`、帶原因，讓後台清單看得到試過什麼。驗證是從主機實際抓：有的站會對主機 IP 回 4xx、有的 robots 不允許，那是來源的事，不是 CLI 壞了。

**`settings_cli`**：輸出 `settings`（開關、模式、撰稿與查核的供應商與模型、三類的自動發布）、`default_models`、`keys_configured`（`openai`／`anthropic`／`minimax`／`gemini`／`jev` 只報 true/false；Claude 在「訂閱帳號」連線方式下只要主機 AI 帳號代理有設定就算 true）、來源總數與啟用數、`changes`、`blockers`、`applied`。旗標：`--enable`／`--disable`、`--writer-provider`、`--writer-model`、`--verifier-provider`、`--verifier-model`（模型給空字串＝回到該家預設）、`--apply`、`--actor-email`。它會拒絕在這些情況打開掃描：撰稿或查核那家沒有金鑰、任一家是 Gemini（它的 schema 轉換只留 `anyOf` 的第一項，寫不出新聞文章）、Jev 沒設定。它**永遠不碰**模式（影子／自動）與自動發布。

**換撰稿或查核的供應商、模型、prompt 或政策版本，會把每個類別打回影子模式、門檻時鐘歸零**。改之前讓站主知道這個代價。

## 清單在哪個狀態、該做什麼

| 後台清單 | 狀態 | 意思 |
| --- | --- | --- |
| 待審查 | `manual_review`、`shadow_review` | 要人決定；側欄徽章只算這裡 |
| 需重寫 | `needs_redraft`、`failed` | 查核、語系審查、硬性檢查、引用網址或日期擋下、還沒成文章的；「重新執行」會花模型費用 |
| 缺證據 | `needs_evidence` | 只有 `lead_only` 頁面，沒有東西可引用；退件 |
| 已發布／已退件 | `published`／`rejected`、`duplicate` | 參考用 |

清單用 `?queue=` 與 `?page=` 記在網址上。批次退件在後台勾選多筆即可（每筆一個有稽核的退件）；用腳本在容器裡呼叫 `service.reject_candidate` 只在站主明確要求時做，而且要 Manual 模式（灌腳本進容器會被分類器擋）。

## 診斷順序

1. **一篇都沒有**：`settings_cli` 看 `enabled`、`blockers`、`keys_configured`；`docker compose … ps` 看兩個 news 服務在不在；`/admin/news` 的來源看 `last_status`（`succeeded`／`partial`／`not_modified`／`failed`／`validation_failed`）與錯誤。
2. **候選卡在 `drafting`／`verifying`／`locale_review`／`jev_review`**：幾乎都是部署重啟把 worker 砍掉。news-worker 啟動時會把這些全部標成 `failed`（`news_processing_stale`，記一筆 `stale-recovery` run）並立刻重排；排程器對超過 70 分鐘的也做同樣的事（job 逾時 60 分鐘）。每個候選最多自動重排兩次，之後等人按「重新執行」。兩個並行名額都被卡住時其他候選只會一直延後。同一天多次部署，每次都會中斷一篇。
3. **很多「重複不確定」進人工審查**：Jev 的每日呼叫預算（`jev_daily_call_budget`，預設 200，在「AI 供應商與金鑰」卡）用完時，重複檢查一律回答不確定。
4. **撰稿全部失敗**：`keys_configured` 裡那家是 false（例如沒有 Anthropic 金鑰卻選了 Claude，又沒切到訂閱帳號）。
5. **`news_evidence_changed`**：證據雜湊永遠不會更新，這種候選重跑也發不出去，只能退件。
6. 要數各狀態筆數：唯讀 psql 在 auto 模式可能被當成 Production Reads 擋下；Manual 模式下簡單的 `select status, count(*) … group by status` 會過，或請站主開 `/admin/news` 看。

## 金鑰與模型從哪裡來

新聞 job 用 `load_runtime_settings` 讀後台「AI 供應商與金鑰」卡（見 `ai-settings.md`），不是容器環境。撰稿與查核的下拉「預設」跟著後台 AI 設定走，「自訂…」接受 `[A-Za-z0-9._:-]{1,128}`。Claude 在「訂閱帳號」連線方式下改走主機的 AI 帳號（`ai-accounts.md`），單一階段最多等兩分鐘找空閒帳號，所有帳號都到上限就改用 MiniMax，run 上會記 MiniMax 的模型。
