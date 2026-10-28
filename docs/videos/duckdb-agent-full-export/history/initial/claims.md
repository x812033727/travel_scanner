# 第五片draft claims

狀態：作者自核對的scratch主張表，未獨立審稿／Jev或TTS。以video.json當前內容為準。

| ID｜等級 | 主張／教學內容 | 證據 | 範圍 | 場景 |
|---|---|---|---|---|
| c1｜RUN／作者資料 | 原創1200筆虛構配送fixture、作者確定性程式；非公司／個資／公共統計或獨立產品回應。 | demo/input/parcels.csv; ../fifth-demo/input/fixture-description.json; run_operations.py | 不冒稱來源為真業務、AI失敗或站主職業經驗。 | parcel-table-start, running-followup-task, one-running-task, input-is-still-there, input-columns, input-status-count, author-demo-scope |
| c2｜RUN | 同一2.0查詢資料仍1200筆；一般與agent皆顯示前後40列，agent明列1160省略。 | runlogs/human-preview.stdout.txt; runlogs/agent-preview.stdout.txt | 顯示省略不是查詢／儲存資料遺失。一般模式也已有列數提示。 | forty-visible, missing-question, input-is-still-there, find-the-omission, human-footer, agent-omitted, same-result-different-view, preview-versus-file |
| c3｜RUN／故意錯字 | 作者故意actual_day錯字；兩模式均報欄位不存在，agent錯誤物件列actual_days候選。 | demo/typo.sql; runlogs/human-typo.stderr.txt; runlogs/agent-typo.stderr.txt | 不是觀察到的AI失誤，也不是只有agent能發現錯誤。 | typo-question, field-name-question, intentional-typo, human-error, valid-json-fields, repair-the-name |
| c4｜RUN | 完整主清單480筆；獨立標準函式庫條件核對與Parquet讀回逐列相符。 | demo/output/late-followup.csv; demo/output/parquet-readback.csv; demo/replay-results.json; ../fifth-demo/artifact-verification.json | 僅支持本例交付完整性，不是任意查詢／AI正確性證書。 | export-question, one-running-task, read-exported-count, actual-export-count, full-content-comparison, preview-versus-file |
| c5｜RUN／作者契約 | 主需求是status=delivered且actual_days>promised_days；在途不列為已送達延遲，空白不是零天。 | demo/setup.sql; demo/followup.sql; demo/input/parcels.csv | 不偷換成所有在途包裹狀態或真配送政策。 | running-followup-task, input-columns, define-the-followup, explicit-input-types, inspect-columns, apply-both-conditions, where-is-complete, voice-the-rule, strict-greater |
| c6｜CITED＋本地呈現 | agent模式調整CLI回覆：緊湊Markdown、明示省略／結果摘要和JSON錯誤；不內含AI模型。 | https://duckdb.org/docs/2.0/clients/cli/agent_mode.html; runlogs/agent-preview.stdout.txt; runlogs/agent-typo.stderr.txt | 本地沒有模型推理／產品前後測；機制卡標官方、實際輸出卡標RUN。 | mode-role, force-human, force-agent, same-result-different-view, release-time, agent-mode-fit |
| c7｜RUN | 完整可讀SQL、-no-init、臨時資料庫與兩種模式命令；同一固定2.0 binary。 | run_operations.py; demo/setup.sql; demo/preview.sql; runlogs/human-preview.command.json; runlogs/agent-preview.command.json | shell卡換行為可照寫形式，連續反斜線只作shell續行；沒有假終端輸出。 | force-human, force-agent, same-preview, explicit-input-types |
| c8｜RUN | 本例960已送達、240在途；在途actual_days空白。 | runlogs/followup.stdout.txt; demo/input/parcels.csv | 虛構fixture規則，不推論真業務分布。 | inspect-columns, input-status-count |
| c9｜RUN資料＋實算 | P0002為3天承諾／4天實際／晚1天；P0005在途空白；P0001為3／3準時。 | demo/input/parcels.csv; demo/output/late-followup.csv; demo/output/due-or-late.csv | 手算與輸出同一筆，不另造外部案例。 | read-one-parcel, compute-days-late, in-transit-example, on-time-example, first-delivered-late, on-time-enters-variant |
| c10｜RUN | 主清單選parcel_id、route、兩種天數、days_late，按parcel_id升冪；COPY保留相同條件。 | demo/followup.sql 第9–22行; demo/output/late-followup.csv | 不把顯示列數上限塞進匯出查詢。 | where-is-complete, voice-the-rule, selection-and-order, repair-the-name, copy-csv-whole, copy-where |
| c11｜RUN＋條件推導 | 嚴格大於排除剛好準時；大於等於代表另一個包含剛好準時的需求。 | demo/followup.sql; demo/variant.sql; demo/variant-results.json | 變式另命名，不能把720筆都稱晚到。 | strict-greater, on-time-example |
| c12｜RUN／輸出契約 | 本次stderr為startup文字＋一行合法JSON錯誤；需取JSON行解析，整stream不符合單一JSON物件預期。 | runlogs/agent-typo.stderr.txt; verification.json | consumer預期不同不等於DuckDB輸出壞JSON；沒有真第三方consumer故障主張。 | valid-json-fields, stderr-contract, consumer-expectation, repair-the-name |
| c13｜RUN | COPY匯出完整480筆CSV；HEADER保留欄名；檔案讀回count=480。 | demo/followup.sql; runlogs/followup.stdout.txt; demo/output/late-followup.csv | CSV／SQL／COPY是既有能力，非2.0首創。 | copy-csv-whole, copy-where, copy-destination, copy-parquet-whole, read-exported-count, actual-export-count, first-delivered-late, tail-of-output |
| c14｜RUN | 相同選欄／條件／排序匯出Parquet，再讀成CSV逐列一致。 | demo/readback.sql; demo/output/late-followup.parquet; demo/output/parquet-readback.csv; demo/replay-results.json | 沒有Parquet效能／壓縮比較，亦不假稱格式是新功能。 | copy-parquet-whole, handoff-question, read-parquet-back, full-content-comparison |
| c15｜RUN | 同一2.0一般／agent模式，相同條件都得到480主清單；差在回覆方式。 | runlogs/human-followup.stdout.txt; runlogs/followup.stdout.txt; demo/replay-results.json | 不是2.0對1.5，沒有成本／速度或模型優劣基準。 | same-version-same-answer, agent-mode-fit, format-is-not-correctness |
| c16｜RUN | 主清單路線R2、R3各240；CSV末端包含P1191、1194、1198、1199及對應值。 | runlogs/followup.stdout.txt; demo/output/late-followup.csv | 頭尾／摘要不代替全量核對，數字只屬此fixture。 | tail-of-output, route-summary-query, route-summary-result |
| c17｜RUN／產物 | 主CSV、Parquet、完整SQL及原創HTML／教材包均已存在，可交付並追條件。 | demo/output/late-followup.csv; demo/output/late-followup.parquet; demo/followup.sql; ../fifth-demo/output/followup-report.html; ../fifth-demo/output/fifth-followup-kit.zip | 尚未登記或公開上傳；正式下載URL由root完成後加入，不捏造連結。 | preview-versus-file, handoff-pack, keep-the-rule |
| c19｜CITED | agent模式10/9介紹，10/21隨2.0正式release；CSV／SQL匯出為既有能力。 | https://duckdb.org/2026/10/09/agent-mode.html; https://duckdb.org/2026/10/21/announcing-duckdb-200; sources/duckdb-release.json | 不是首次能讀CSV，未測全部2.0新增功能。 | upgrade-question, release-time, existing-file-tools |
| c20｜編輯建議 | 一次性表格篩選／反覆交付固定查詢的取捨，先在新練習目錄試用。 | brief.md; demo/replay-results.json | 不是表格產品實測、速度優勢或全面升級建議。 | pick-the-tool, agent-mode-fit, bounded-choice, keep-the-rule |
| c21｜CITED | 2.0為LTS，官方支援承諾至少到2027年10月。 | https://duckdb.org/2026/10/21/announcing-duckdb-200 | 維護承諾不是本地相容性測試；未外推精確終止日。 | lts-is-a-promise |
| c22｜CITED | 2.0新預設格式不可給舊版讀；既有舊格式可由2.0讀寫並保留格式。 | https://duckdb.org/docs/2.0/operations_manual/migration.html | 未實測現有資料庫升級／回滾，不以LTS推立即升級。 | storage-condition, bounded-choice |
| c23｜方法範圍 | 作者固定fixture與確定性SQL；未測模型推理、token／費用、跨版效能、server或升級。 | demo/replay-results.json; run_operations.py; ../fifth-demo/results.json | agent名稱不等於已運行AI模型；輸出bytes不換算成本。 | format-is-not-correctness, author-demo-scope |
| c24｜RUN需求變式 | 同資料將>改>=，另存剛好準時或晚到720筆，其中240筆days_late=0；P0001入選。 | demo/variant.sql; demo/variant-results.json; demo/output/due-or-late.csv | 這是明示新需求，不說原480錯，也不把720都叫延遲；檔名due-or-late的精確範圍仍是已送達且actual>=promised。 | change-the-requirement, due-or-late-rule, variant-result, on-time-enters-variant |

## 輸入、動作、預期與實際

同一原創1200筆CSV，主條件為已送達且實際天數大於承諾；預期每筆遵守該契約。可讀SQL重做後480筆逐列等於研究版本與獨立oracle，Parquet讀回一致。兩模式相同條件結果一致；顯示方式不是主條件正確性的原因。變式明示改成包含準時，實際720筆，另存檔名。

## 與企劃不同的地方

依root最新steering採六章、35秒估計冷開場；正文outro歸第六章。刪除尾段完整泛用AI提示，完整SQL與修改已在操作當下呈現／口述，避免回顧重述。加入同資料>到>=的實際需求變式，支撐觀眾自己修改後核對的能力。沒有擴成另一資料集或模型比較。

## 我懷疑但沒動的事

原生lint不等於教學含金量／敘事盲評。兩模式得到同一480，新增特性的優勢限呈現與結構，不能聲稱改顯示提升分析能力。開場手動錯字不是不可預期的AI失敗；主例核心為新模式的真實回覆。需要root／Jev如實評估選題價值，未將作者自評當獨立審查。發音say為scratch建議，尚未試聽。

## 進度

已寫68景／121句、六章；來源刷新、可讀SQL重做與需求變式完成。原生lint結果另存，未paid／後臺／正式register／task／TTS／render。
