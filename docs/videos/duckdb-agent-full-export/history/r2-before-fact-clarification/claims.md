# 第五片draft claims

狀態：R2作者自核對的scratch主張表；此R2尚未獨立審稿／Jev或TTS。來源video.json SHA256：1a267cb77e4d3eeddffc850dca6616c68a3c66afcaed38576b6e776a3ca62bf2

| ID｜等級 | 主張／教學內容 | 證據 | 範圍 | 場景 |
|---|---|---|---|---|
| c1｜RUN／作者資料 | 原創1200筆虛構配送fixture、作者確定性程式；非公司／個資／公共統計或獨立產品回應。 | demo/input/parcels.csv; ../fifth-demo/input/fixture-description.json; run_operations.py | 不冒稱來源為真業務、AI失敗或站主職業經驗。 | parcel-table-start, running-followup-task, input-is-still-there, input-columns, input-status-count |
| c2｜RUN | 同一2.0查詢資料仍1200筆；一般與agent皆顯示前後40列，agent明列1160省略。 | runlogs/human-preview.stdout.txt; runlogs/agent-preview.stdout.txt; public-run/public-run-results.json | 顯示省略不是查詢／儲存資料遺失。一般模式也已有列數提示。 | forty-visible, missing-question, input-is-still-there, find-the-omission, human-footer, agent-omitted, same-result-different-view, copy-limit-question |
| c3｜RUN／故意錯字 | 作者故意actual_day錯字；兩模式均報欄位不存在，agent錯誤物件列actual_days候選。 | demo/typo.sql; runlogs/human-typo.stderr.txt; runlogs/agent-typo.stderr.txt; public-run/public-run-results.json | 不是觀察到的AI失誤，也不是只有agent能發現錯誤。 | typo-question, field-name-question, human-error, intentional-typo, valid-json-fields, repair-the-name |
| c4｜RUN | 完整主清單480筆；獨立標準函式庫條件核對與Parquet讀回逐列相符。 | demo/output/late-followup.csv; demo/output/parquet-readback.csv; demo/replay-results.json; ../fifth-demo/artifact-verification.json; public-run/public-run-results.json | 僅支持本例交付完整性，不是任意查詢／AI正確性證書。 | export-question, read-exported-count, actual-export-count, full-content-comparison, source-predicate-check |
| c5｜RUN／作者契約 | 主需求是status=delivered且actual_days>promised_days；在途不列為已送達延遲，空白不是零天。 | demo/setup.sql; demo/followup.sql; demo/input/parcels.csv | 不偷換成所有在途包裹狀態或真配送政策。 | running-followup-task, input-columns, define-the-followup, explicit-input-types, inspect-columns, apply-both-conditions, where-is-complete |
| c6｜CITED＋本地呈現 | agent模式調整CLI回覆：緊湊Markdown、明示省略／結果摘要和JSON錯誤；不內含AI模型。 | https://duckdb.org/docs/2.0/clients/cli/agent_mode.html; runlogs/agent-preview.stdout.txt; runlogs/agent-typo.stderr.txt | 本地沒有模型推理／產品前後測；機制卡標官方、實際輸出卡標RUN。 | release-time, mode-role, bounded-choice, force-human, force-agent, same-result-different-view |
| c7｜RUN | 完整可讀SQL、-no-init、臨時資料庫與兩種模式命令；同一固定2.0 binary。 | run_operations.py; demo/setup.sql; demo/preview.sql; runlogs/human-preview.command.json; runlogs/agent-preview.command.json; public-run/public-run-results.json | shell卡換行為可照寫形式，連續反斜線只作shell續行；沒有假終端輸出。 | force-human, force-agent, same-preview, explicit-input-types, run-followup, run-readback, run-variant |
| c8｜RUN | 本例960已送達、240在途；在途actual_days空白。 | runlogs/followup.stdout.txt; demo/input/parcels.csv; public-run/public-run-results.json | 虛構fixture規則，不推論真業務分布。 | inspect-columns, input-status-count |
| c9｜RUN資料＋實算 | P0002為3天承諾／4天實際／晚1天；P0005在途空白；P0001為3／3準時。 | demo/input/parcels.csv; demo/output/late-followup.csv; demo/output/due-or-late.csv; public-run/public-run-results.json | 手算與輸出同一筆，不另造外部案例。 | read-one-parcel, compute-days-late, in-transit-example, on-time-example, first-delivered-late, on-time-enters-variant |
| c10｜RUN | 主清單選parcel_id、route、兩種天數、days_late，按parcel_id升冪；COPY保留相同條件。 | demo/followup.sql 第9–22行; demo/output/late-followup.csv; public-run/public-run-results.json | 不把顯示列數上限塞進匯出查詢。 | where-is-complete, selection-and-order, repair-the-name, copy-csv-whole, copy-where |
| c11｜RUN＋條件推導 | 嚴格大於排除剛好準時；大於等於代表另一個包含剛好準時的需求。 | demo/followup.sql; demo/variant.sql; demo/variant-results.json | 變式另命名，不能把720筆都稱晚到。 | on-time-example, new-requirement-consequence, different-deliveries |
| c12｜RUN／輸出契約 | 本次stderr為startup文字＋一行合法JSON錯誤；需取JSON行解析，整stream不符合單一JSON物件預期。 | runlogs/agent-typo.stderr.txt; verification.json; public-run/public-run-results.json | consumer預期不同不等於DuckDB輸出壞JSON；沒有真第三方consumer故障主張。 | stderr-contract, valid-json-fields, repair-the-name |
| c13｜RUN | COPY匯出完整480筆CSV；HEADER保留欄名；檔案讀回count=480。 | demo/followup.sql; runlogs/followup.stdout.txt; demo/output/late-followup.csv; public-run/public-run-results.json | CSV／SQL／COPY是既有能力，非2.0首創。 | copy-limit-question, copy-csv-whole, copy-where, copy-destination, copy-parquet-whole, run-followup, read-exported-count, actual-export-count, first-delivered-late, tail-of-output |
| c14｜RUN | 相同選欄／條件／排序匯出Parquet，再讀成CSV逐列一致。 | demo/readback.sql; demo/output/late-followup.parquet; demo/output/parquet-readback.csv; demo/replay-results.json; public-run/public-run-results.json | 沒有Parquet效能／壓縮比較，亦不假稱格式是新功能。 | copy-parquet-whole, handoff-question, read-parquet-back, run-readback, full-content-comparison |
| c15｜RUN | 同一2.0一般／agent模式，相同條件都得到480主清單；差在回覆方式。 | runlogs/human-followup.stdout.txt; runlogs/followup.stdout.txt; demo/replay-results.json; public-run/public-run-results.json | 不是2.0對1.5，沒有成本／速度或模型優劣基準。 | bounded-choice, same-version-same-answer |
| c16｜RUN | 主清單路線R2、R3各240；CSV末端包含P1191、1194、1198、1199及對應值。 | runlogs/followup.stdout.txt; demo/output/late-followup.csv; public-run/public-run-results.json | 頭尾／摘要不代替全量核對，數字只屬此fixture。 | tail-of-output, route-summary-query, route-summary-result |
| c17｜RUN／產物 | 主CSV、Parquet、完整SQL及原創HTML／教材包均已存在，可交付並追條件。 | demo/output/late-followup.csv; demo/output/late-followup.parquet; demo/followup.sql; ../fifth-demo/output/followup-report.html; ../fifth-demo/output/fifth-followup-kit.zip; public-run/public-run-results.json | 教材檔已存在，尚無本片公開下載URL；不捏造公開上傳或成片紀錄。 | different-deliveries, handoff-pack, keep-the-rule |
| c19｜CITED | agent模式10/9介紹，10/21隨2.0正式release；CSV／SQL匯出為既有能力。 | https://duckdb.org/2026/10/09/agent-mode.html; https://duckdb.org/2026/10/21/announcing-duckdb-200; sources/duckdb-release.json | 不是首次能讀CSV，未測全部2.0新增功能。 | release-time, existing-file-tools |
| c20｜編輯選擇／作者方法 | 這份練習在新目錄比較同版兩模式，不變更既有資料庫。 | brief.md; demo/replay-results.json; run_operations.py | 不是舊資料庫升級、表格產品比較或全面採用建議。 | bounded-choice |
| c23｜方法範圍 | 作者固定fixture與確定性SQL；未測模型推理、token／費用、跨版效能、server或升級。 | demo/replay-results.json; run_operations.py; ../fifth-demo/results.json | agent名稱不等於已運行AI模型；輸出bytes不換算成本。 | bounded-choice |
| c24｜RUN需求變式 | 同資料將>改>=，另存剛好準時或晚到720筆，其中240筆days_late=0；P0001入選。 | demo/variant.sql; demo/variant-results.json; demo/output/due-or-late.csv; public-run/public-run-results.json | 這是明示新需求，不說原480錯，也不把720都叫延遲；檔名due-or-late的精確範圍仍是已送達且actual>=promised。 | change-the-requirement, new-requirement-consequence, due-or-late-rule, run-variant, variant-members-question, variant-result, on-time-enters-variant, different-deliveries |

## 輸入、動作、預期與實際

同一原創1200筆CSV，主條件為已送達且實際天數大於承諾；預期每筆遵守該契約。R1已真執行的公開根目錄./duckdb命令與raw收據固定不動；480筆主清單及720筆需求變式逐欄oracle、240筆零差值、兩模式CSV與Parquet讀回結果均沿用已驗證產物。R2只讀取既有材料核對，不重新執行SQL或重包ZIP。

## R2主張差異

21項定義保留，五欄ID／等級、主張、證據、範圍、場景完整保留。移除json-stream-question與consumer-expectation兩景後，c12仍由本次stderr取合法JSON行、辨認錯字／候選並修正原表欄位的實際操作使用；場景列表依當前順序精確重算。全部主張文字、證據與範圍保持R1，不新增事實、不刪必要合法JSON／混合訊息界線，也沒有任何未用定義。

## 窄修範圍

在途個案用剛剛的狀態條件作點名回呼，再給該筆排除結果；HEADER之後改成讀回時核對欄位順序的新動作。錯誤訊息不另設consumer解析問題，而是略過本次啟動文字、取合法JSON行、讀出錯字與候選、補正欄位並接回主清單。六章、章首、年份、三個開場預告與全部完整命令不變。

## 仍待驗

R1兩位fresh原判為12／13及11／13且false，原始NO完整保留；本R2尚待root的新fresh讀者及正常獨立審查，不自造未來分數。原生lint不是敘事或成片通過；自然配音、say試聽、卡片render及實際媒體長度尚未完成。

## 進度

R2為64景／111句、六章；此表實際21項。原始資料、SQL、公開命令、所有raw輸出、重跑proof及新舊ZIP不動；本輪不操作正式repo、共享lexicon、任務、後臺、付費、TTS或媒體。
