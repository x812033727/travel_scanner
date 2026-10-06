# 新聞自動化：主機上的操作與診斷

每個階段在做什麼、清單與啟用門檻的全文在 `docs/news-automation.md`；程式在 `apps/api/app/news_automation/`。這裡只放操作。

## 誰在跑

| 服務 | 做什麼 |
| --- | --- |
| `news-scheduler`（compose profile `news`） | 每分鐘：替到期的來源排掃描、把死掉的 job 標成失敗、重排孤兒候選、排每日清理 |
| `news-worker`（compose profile `news`） | `news` 佇列唯一的消費者，容器裡跑 `NEWS_WORKER_PROCESSES` 個 RQ worker（預設 3，2026-09-28 起）；同時跑幾個候選仍由後台的全域／每類並行數決定；一般 `worker` 不讀這個佇列。**只能有一個 news-worker 容器**：它啟動時會把所有處理中的候選判失敗重排 |
| `/admin/news` | 來源、設定、審查清單、執行紀錄、各類別的啟用門檻 |

`news` profile 沒起來時什麼都不會跑：後台按的「立即掃描」「重新執行」都停在 Redis 等 worker。確認兩個服務都在：`docker compose -f docker-compose.prod.yml ps --format '{{.Name}} {{.Status}}' | grep news`。部署腳本要帶 `--profile news` 才會每次一起重建（腳本不在 git 裡，確認用 `grep -- --profile /root/deploy-travel-scanner.sh`；少了就是主機變更，站主決定，走 skill `deploy`）。只手動起一次不夠：下次部署會重建別的服務、把它們留在舊映像。

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

**`settings_cli`**：輸出 `settings`（開關、模式、撰稿／查核／最終修改的供應商與模型、代審的開關 `judge_enabled` 與它的供應商和模型、三類的自動發布）、`default_models`、`keys_configured`（`openai`／`anthropic`／`minimax`／`gemini`／`jev` 只報 true/false；Claude 在「訂閱帳號」連線方式下只要主機 AI 帳號代理有設定就算 true）、來源總數與啟用數、`changes`、`blockers`、`applied`。旗標：`--enable`／`--disable`、`--writer-provider`、`--writer-model`、`--verifier-provider`、`--verifier-model`、`--editor-provider`、`--editor-model`、`--judge-enable`／`--judge-disable`、`--judge-provider`、`--judge-model`（模型給空字串＝回到該家預設）、`--apply`、`--actor-email`。四個角色都一樣：只換供應商、沒有同時給模型，那個角色的模型會回到新那一家的預設（和後台換供應商時一樣，`changes` 裡看得到 `<角色>_model: null`），因為原本存的模型 id 是舊那一家的。它會拒絕在這些情況打開掃描：撰稿、查核或最終修改那家沒有金鑰、任一家是 Gemini（它的 schema 轉換只留 `anyOf` 的第一項，寫不出新聞文章）、Jev 沒設定；代審那家只在代審開著（`judge_enabled`）時一起檢查，掃描關著時什麼都不檢查。它**永遠不碰**模式（影子／自動）與自動發布。代審的用法在下面「AI 代審」一節。

換撰稿、查核或最終修改的供應商、模型，或 prompt、政策版本，只會讓每個類別的一致率統計（天數、已標記筆數、和 Jev 的一致率，僅供參考）重新起算；模式和自動發布都不會被改（2026-09-25 站主拿掉影子門檻之後就是這樣）。換代審的供應商或模型連統計都不重算。

## 清單在哪個狀態、該做什麼

| 後台清單 | 狀態 | 意思 |
| --- | --- | --- |
| 待審查 | `manual_review`、`shadow_review` | 要人決定；側欄徽章只算這裡 |
| 需重寫 | `needs_redraft`、`failed` | 查核、語系審查、硬性檢查、引用網址或日期擋下、還沒成文章的；「重新執行」會花模型費用 |
| 缺證據 | `needs_evidence` | 只有 `lead_only` 頁面，沒有東西可引用；退件 |
| 已發布／已退件 | `published`／`rejected`、`duplicate` | 參考用 |

列上的「AI 交回」（待審查、需重寫）與「AI 結案」（已退件）是代審留下的，見下面「AI 代審」一節；沒有標記的還沒被它判過。

清單用 `?queue=` 與 `?page=` 記在網址上。批次退件在後台勾選多筆即可（每筆一個有稽核的退件）；用腳本在容器裡呼叫 `service.reject_candidate` 只在站主明確要求時做，而且要 Manual 模式（灌腳本進容器會被分類器擋）。

## 五語稿已寫好、卻被硬性檢查擋在「需重寫」的候選

2026-10-01 到 #1201（10-04）之間，每篇自動文章都因為一張已經不畫的流程圖被硬性檢查擋下；#1136 之前這種稿件只存在候選上（`needs_redraft`、`news_hard_checks_failed`、沒有文章、五語都在 `draft_bundle_json`）。「重新執行」和不帶旗標的 `backfill_cli` 都會整篇重寫，要用 `--resume-saved-bundles`：

```bash
cd /root/travel_scanner
# 只看：可以接著跑的候選、每篇在現行規則下還有哪些語系會被擋（hard_checks），乾淨的排前面
docker compose -f docker-compose.prod.yml exec -T api python -m app.news_automation.backfill_cli --since 2026-09-28 --resume-saved-bundles --limit 3
# 站主同意後才帶 --apply
docker compose -f docker-compose.prod.yml exec -T api sh -c 'python -m app.news_automation.backfill_cli --since 2026-09-28 --resume-saved-bundles --limit 3 --apply --actor-email "${ADMIN_EMAILS%%,*}" --reason "Resume after #1201"'
```

每篇記一筆 `news_candidate_resumed` 稽核，改成 `discovered`＋`news_resume_saved_bundle` 排進 news-worker。worker 不撰稿、不翻譯：先重做一次重複檢查（稿子放了幾天，期間可能已經有人發了同一件事），再跑硬性檢查、讀最終修改的紀錄、做 Jev 最後一關，最後發布。只花 Jev 呼叫（每篇約 6 次），不花撰稿模型。結果和一般第二階段相同：
- 發布（自動條件都成立）
- `news_hard_checks_failed`：文章已存，到文章編輯器修好後按重新查核
- `news_final_edit_hold`／`news_jev_final_hold`：文章已存，人看過後按五語發布
- `news_duplicate_uncertain`／`duplicate`
- `news_evidence_changed`：發布前重抓證據時，來源頁已經變了

標記在當機或 worker 被砍時會保留，重排後仍接著跑，不會重寫。

## AI 代審：待審查與需重寫交給模型判斷

站主 2026-10-06 的決定：稿子停進「待審查」或「需重寫」之後，由站主選的模型（代審，程式裡叫 judge，`apps/api/app/news_automation/judge.py`）代替站主回答那一次卡關：發布、退件、判定重複或不是重複、帶修改指示重寫，或附理由交回給站主。出貨時是關的。每種卡關它能答什麼、哪些規則不管模型怎麼答都成立，在 `docs/news-automation.md` 的「With AI review on」；這裡只放主機上會用到的。

**四個開關都開著它才動**：啟用掃描、自動模式、該類別的自動發布、代審自己的開關（後台新聞設定頁的「待審查與需重寫交給 AI 判斷」，欄位 `judge_enabled`）。模型在「AI 設定 › 各功能模型」的「代審模型」選，預設 Claude Opus 5.5。任何一個關著，它不判、也不發；回報重大錯誤會關掉該類別的自動發布，那一類的代審也跟著停。開不開是站主的決定。

```bash
cd /root/travel_scanner
# 看一個變更會怎樣（不寫）
docker compose -f docker-compose.prod.yml exec -T api python -m app.news_automation.settings_cli --judge-enable --judge-provider anthropic --judge-model claude-opus-5-5
# 站主同意後才寫
docker compose -f docker-compose.prod.yml exec -T api sh -c 'python -m app.news_automation.settings_cli --judge-enable --judge-provider anthropic --judge-model claude-opus-5-5 --apply --actor-email "${ADMIN_EMAILS%%,*}"'
# 關掉
docker compose -f docker-compose.prod.yml exec -T api sh -c 'python -m app.news_automation.settings_cli --judge-disable --apply --actor-email "${ADMIN_EMAILS%%,*}"'
```

`settings_cli` 不碰模式與自動發布，所以在影子模式、或該類別沒開自動發布時，開了代審也不會有動作。

| 清單 | 它會答的卡關 | 留給站主、它不碰的 |
| --- | --- | --- |
| 待審查 | `news_zh_draft_ready`、`news_duplicate_uncertain`、`news_jev_final_hold`、`news_ready_to_publish`、`news_final_edit_hold`（這一種只能退件或交回，不能發布） | `news_hard_checks_failed`、`news_evidence_changed`、站主確認過卻卡在翻譯或查核的、已經有文章而重新查核時被查核、語系審查或事件日期擋下的（不必有人確認過；到文章編輯器修好再按「重新查核」）、站主確認過又被最終修改擋下的 `news_final_edit_hold`（它不能發布、也不能把確認過的結案，沒有可判的）、`shadow_review` 與 `news_jev_manual` 的舊稿 |
| 需重寫 | `news_verification_failed`、`news_claim_source_invalid`、`news_event_date_invalid`、`news_locale_review_failed`，而且沒有文章、沒有人的決定 | `failed`、`news_not_eligible`（代審要求重寫、撰稿模型卻說不值得報導）、`news_hard_checks_failed`（#1136 之前的五語稿，走上一節的 `--resume-saved-bundles`） |

兩個清單都一樣：證據摘錄已經被 90 天清理清掉的稿子不交給它，沒有東西可以對照、也沒有東西可以重寫。

主機上要記得的幾件事：

- 每個卡關只答一次。答完留在原清單的，後台標「AI 交回」（理由在候選詳情的「下一步」）；被它退件或判定重複的在「已退件」標「AI 結案」，站主可以按「拿回來自己判斷」拿回原清單，拿回來的不會再被判。
- 模型作答的那幾分鐘裡，人按了任何按鈕、候選又跑了一次、或四個開關有一個被關掉，答案作廢，除了 run 之外什麼都不寫。
- 它核准繁中草稿後，候選以 `news_judge_approved` 回到 `discovered` 跑第二階段：最終修改、翻譯與語系審查、硬性檢查、Jev 最後一關、發布前的檢查全部照跑，任何一關都可能再把它擋下。它指示重寫的以 `news_judge_redraft` 回去重新起稿。兩個標記和 `news_reverify_requested` 一樣，當機、worker 重啟、訂閱帳號暫停時都保留。
- 重寫每篇一輩子最多兩次，到了上限直接交回，不再呼叫模型。它指示重寫、撰稿模型卻說不值得報導的（`news_not_eligible`）留在「需重寫」，一樣標「AI 交回」、算進交回的筆數。
- 它不寫人的決定（`human_decision`、`human_reason`、`human_major_error`）。判決是 `news_assessments` 裡 `assessment_type = 'judge'` 的列，稽核是 `news_candidate_judged`，發布多一筆 `news_candidate_judge_published`，站主拿回來是 `news_candidate_reopened_by_owner`。

### 舊稿要分批放行

稿子是在「把它停進卡關的那一次候選 job」結束時交給代審的，沒有任何掃描會回頭撿。所以開關打開之前就在清單裡的、進清單時有開關關著的、還有代審 job 掉了的（見診斷順序第 7 點），都要用 `backfill_cli` 的兩個旗標放行：`--judge-holds` 是「待審查」，`--judge-redrafts` 是「需重寫」。先乾跑，給站主看筆數，同意後一小批一小批放：

```bash
cd /root/travel_scanner
# 只看：什麼都不寫、什麼都不排
docker compose -f docker-compose.prod.yml exec -T api python -m app.news_automation.backfill_cli --since 2026-09-25 --judge-holds
docker compose -f docker-compose.prod.yml exec -T api python -m app.news_automation.backfill_cli --since 2026-09-25 --judge-redrafts
# 站主同意後放行一批：--apply 一定要帶 --limit，不需要 --actor-email 與 --reason
docker compose -f docker-compose.prod.yml exec -T api python -m app.news_automation.backfill_cli --since 2026-09-25 --judge-holds --limit 5 --apply
docker compose -f docker-compose.prod.yml exec -T api python -m app.news_automation.backfill_cli --since 2026-09-25 --judge-redrafts --limit 5 --apply
```

- `--since` 在這兩個旗標下是候選**建立**的日期（UTC），不是來源的發布日。
- 乾跑輸出：`held`（那個清單裡這類卡關的總數）、`eligible`（代審會被問到的）、`candidates`／`rows`／`by_hold`／`by_vertical`（這一批，最新的在前，受 `--limit` 限制）、`switches`（四個開關現在的值）、`excluded`（原因 → 各類別筆數）。`judge_enabled` 關著時多一個 `warning`，`eligible` 是 0，`--apply` 什麼都不排。
- `excluded` 的原因：`answered`（已經判過，或站主拿回來的）、`gate_off`（那個類別有開關關著，看 `switches`）、`legacy_bundle`（存著五語稿、沒有文章）、`evidence_expired`（證據摘錄被 90 天清理清掉）、`person_decided`（需重寫：列上有人的決定；待審查：站主確認過又被最終修改擋下的 `news_final_edit_hold`）；只在需重寫出現的有 `has_article`、`rewrite_cap`（已經重寫兩次）。
- `--apply` 只排代審的 job（`news-judge-<候選>-<retry>-<卡關>-backfill-<小時>`，跑 `run_judge`，逾時 30 分鐘），每篇一個；不改候選、不寫稽核、不排候選 job。輸出多 `queued` 與 `already_queued`。漏了 `--limit` 會直接結束並說明原因。
- 一次只能帶一個名單旗標：這兩個和 `--jev-quota-holds`、`--refetch-source`、`--resume-saved-bundles` 互斥，同時帶兩個 argparse 會以 exit 2 結束。
- 放一批、讀完判決、再放下一批。下一次 `--apply --limit N` 取的是還符合條件的最新 N 筆，判過的自然不在名單裡。同一個整點小時內重跑同一批是空跑（`already_queued`）。跨了整點再跑，還沒有判決的每一篇都會多排一個 job：前一個 job 正在問模型的，後到的自己讓開、不呼叫模型；前一個已經答完的，後到的什麼都不做；只有前一次呼叫失敗、正在等 30 分鐘後重試的，後到的會馬上再問一次，那次若又失敗，一樣算進三次失敗。

**不要用不帶旗標的 `backfill_cli` 去推代審的稿子。** 不帶旗標的那一個是把舊規則擋下的稿子以站主的名義重開成全新草稿（寫稽核與 `human_reason`、馬上排進 worker）。代審退件或交回過的列（`judge_decision` 有值）它會跳過，所以推不動；還沒判過的「需重寫」列有三種卡關原因和它的名單重疊，會被它整批重寫，繞過代審的修改指示與兩次上限。要把「需重寫」交給代審就用 `--judge-redrafts`；代審退掉的要翻案，請站主在後台按「拿回來自己判斷」。

## 診斷順序

1. **一篇都沒有**：`settings_cli` 看 `enabled`、`blockers`、`keys_configured`；`docker compose … ps` 看兩個 news 服務在不在；`/admin/news` 的來源看 `last_status`（`succeeded`／`partial`／`not_modified`／`failed`／`validation_failed`）與錯誤。
2. **候選卡在 `drafting`／`verifying`／`locale_review`／`jev_review`**：幾乎都是部署重啟把 worker 砍掉。news-worker 啟動時會把這些全部標成 `failed`（`news_processing_stale`，記一筆 `stale-recovery` run）並立刻重排；排程器對超過 70 分鐘的也做同樣的事（job 逾時 60 分鐘）。每個候選最多自動重排兩次，之後等人按「重新執行」。兩個並行名額都被卡住時其他候選只會一直延後。同一天多次部署，每次都會中斷一篇。
3. **很多候選退回 `discovered`、原因是 `news_jev_quota_paused`**：Jev 的每日呼叫預算（`jev_daily_call_budget`，預設 200，正式站 2026-09-27 起是 5,000，在「AI 供應商與金鑰」卡）在重複檢查用完了。這不是「重複不確定」，不會進人工審查：過了 00:00 UTC（台北 08:00）自動重排，當天在後台調高預算、還有額度時也會立刻重排。細節在 `docs/news-automation.md` 的「When Jev's daily budget is spent」。真的進人工審查的 `news_duplicate_uncertain` 是 Jev 有回答、分數落在 0.25–0.85 之間。
4. **撰稿全部失敗**：`keys_configured` 裡那家是 false（例如沒有 Anthropic 金鑰卻選了 Claude，又沒切到訂閱帳號）。
5. **`news_evidence_changed`**：來源頁在查核之後變了，原本的查核不能拿來發布。請站主在後台按「用最新來源重新查核」：重抓每一個證據頁、換掉存的摘錄與雜湊，已存的五語文章再跑一次查核、語系審查與 Jev 最後一關（`docs/news-automation.md` 的「The review queue」）；不想要就退件。代審核准發布、發布前的檢查卻發現來源變了的稿子也停在這裡，列上帶「AI 交回」，理由第一句會請站主先重新查核來源。
6. 要數各狀態筆數：唯讀 psql 在 auto 模式可能被當成 Production Reads 擋下；Manual 模式下簡單的 `select status, count(*) … group by status` 會過，或請站主開 `/admin/news` 看。
7. **代審開著，稿子卻沒有「AI 交回」、也沒有動**：先跑「舊稿要分批放行」的兩個乾跑。`switches` 裡有 false 就是那個開關；在 `excluded` 裡就看原因。稿子在 `eligible` 裡只表示這個卡關還沒有判決，不等於沒被問過：它的 job 可能還在排隊、正在問，或上一次呼叫失敗、正在等 30 分鐘後重試。放行之前先看候選「執行紀錄」裡的 `judge-*` run：有一筆還在 running、開始不到半小時的，是正在問；最後一筆是失敗（`subscription_*` 或其他錯誤，不是 `news_processing_stale`）的，是問過了、在等重試，這時再放行只是提早重問，失敗照樣算次數。沒有 run，或只有被切斷的（`news_processing_stale`）與答案作廢的（成功、metadata 是 `dropped`），就是現在沒有 job 在管它（進清單時有開關關著、開代審之前就在、代審 job 掉了，或作答時列被動過），照那一節分批放行。`docker compose -f docker-compose.prod.yml logs --since 2h news-worker` 裡，`could not be queued for the review judge` 是候選跑完卻排不進代審（候選 job 本身算成功，不會重試）；`news judge for candidate … failed` 是一次呼叫失敗。候選「執行紀錄」裡 `judge-zh-draft`／`judge-duplicate`／`judge-final`／`judge-redraft` 是代審的 run；帶 `news_processing_stale` 的是被切斷的：被重啟切斷的，news-worker 啟動時會把它標成失敗並替還該判的卡關重排一次（重排那一行 log 是 INFO 等級，news-worker 沒有調 log 等級，容器 log 通常看不到，以 run 為準）；沒有重啟、卻超過 31 分鐘還在 running 的（job 逾時 30 分鐘），或候選重跑之前留下的，由下一個來問同一篇的代審 job 標成失敗後接手。呼叫失敗的規則：回覆驗證失敗或輸入過大，立刻交回；訂閱帳號都滿或登出，30 分鐘後再問、不限次數；其他錯誤 30 分鐘後再問，同一個卡關第三次失敗就交回。交回的理由第一句是程式寫的，說明是哪一種。
8. **要讀代審的判決**：後台候選詳情的「下一步」與「判斷紀錄」。要數的話用唯讀 SQL（Manual 模式，一個呼叫一句）：`select verdict, count(*) from news_assessments where assessment_type = 'judge' group by verdict`；理由在 `reasons_json`，從後台讀比較穩。

## 金鑰與模型從哪裡來

新聞 job 用 `load_runtime_settings` 讀後台「AI 供應商與金鑰」卡（見 `ai-settings.md`），不是容器環境。撰稿與查核的下拉「預設」跟著後台 AI 設定走，「自訂…」接受 `[A-Za-z0-9._:-]{1,128}`。Claude 在「訂閱帳號」連線方式下改走主機的 AI 帳號（`ai-accounts.md`），單一階段最多等兩分鐘找空閒帳號，所有帳號都到上限就改用 MiniMax，run 上會記 MiniMax 的模型。
