# 六章操作製作規劃：R1

全部為原創紙底教學卡；本稿未render、未付費。正式題目已由root登記；本輪只改scratch。操作引用保存的SQL及公開根目錄實際命令／輸出，不造產品對話。

| 估計位置 | 場景 | 版型 | 操作／證據 | 主張 |
|---|---|---|---|---|
| 00:00 | parcel-table-start | big | 原創虛構教學資料 | c1 |
| 00:05 | running-followup-task | big | 同一份練習表的查詢狀態 | c1, c5 |
| 00:12 | forty-visible | big | 顯示內容仍有省略 | c2 |
| 00:17 | missing-question | big | 先分清資料與顯示 | c2 |
| 00:21 | typo-question | big | 相同欄位需求會收到什麼回覆 | c3 |
| 00:26 | export-question | big | 清單另存後，還要讀回 | c4 |
| 00:31 | input-is-still-there | big | 省略的是顯示，不是紀錄 | c1, c2 |
| 00:42 | release-time | table | 官方發表與release日期｜2026-10-25核對 | c6, c19 |
| 00:50 | mode-role | compare | 官方agent文件｜2026-10-25 | c6 |
| 01:02 | existing-file-tools | big | 讀CSV、SQL查詢與匯出原本就有 | c19 |
| 01:10 | bounded-choice | big | 只比較回覆模式，不變更既有資料庫 | c6, c15, c20, c23 |
| 01:22 | input-columns | table | 本地操作2026-10-25｜DuckDB2.0｜虛構資料 | c1, c5 |
| 01:33 | force-human | code | 公開教材根目錄｜Linux2.0實跑｜反斜線為shell續行 | c6, c7 |
| 01:43 | force-agent | code | 公開教材根目錄｜Linux2.0實跑｜反斜線為shell續行 | c6, c7 |
| 01:54 | find-the-omission | big | 從回覆中定位顯示範圍 | c2 |
| 02:00 | same-preview | code | preview.sql 第1–3行／全3行｜本地2.0 | c7 |
| 02:12 | human-footer | quote | 公開教材Linux2.0實跑｜runlogs/human-preview.stdout.txt | c2 |
| 02:22 | agent-omitted | quote | 公開教材Linux2.0實跑｜runlogs/agent-preview.stdout.txt | c2 |
| 02:33 | same-result-different-view | table | 本地操作2026-10-25｜DuckDB2.0｜虛構資料 | c2, c6 |
| 02:44 | define-the-followup | big | 把需求寫成可執行條件 | c5 |
| 02:55 | explicit-input-types | code | setup.sql 第5–9行／全9行｜本地2.0 | c5, c7 |
| 03:05 | inspect-columns | code | followup.sql 第1–4行／全24行｜本地2.0 | c5, c8 |
| 03:16 | input-status-count | table | 本地操作2026-10-25｜DuckDB2.0｜虛構資料 | c1, c8 |
| 03:27 | apply-both-conditions | big | 依同一份表逐項判斷 | c5 |
| 03:32 | read-one-parcel | table | 本地操作2026-10-25｜DuckDB2.0｜虛構資料 | c9 |
| 03:41 | compute-days-late | table | 本地操作2026-10-25｜DuckDB2.0｜虛構資料 | c9 |
| 03:50 | in-transit-example | table | 本地操作2026-10-25｜DuckDB2.0｜虛構資料 | c9 |
| 04:00 | where-is-complete | code | followup.sql 第9–15行／全24行｜本地2.0 | c5, c10 |
| 04:10 | selection-and-order | code | followup.sql 第9–15行／全24行｜本地2.0 | c10 |
| 04:22 | on-time-example | table | 本地操作2026-10-25｜DuckDB2.0｜虛構資料 | c9, c11 |
| 04:32 | field-name-question | big | 條件寫對後，還得使用真正欄位 | c3 |
| 04:39 | human-error | quote | 公開教材Linux2.0實跑｜runlogs/human-typo.stderr.txt | c3 |
| 04:48 | intentional-typo | code | typo.sql 第1–3行／全3行｜本地2.0 | c3 |
| 05:01 | valid-json-fields | table | 本地操作2026-10-25｜DuckDB2.0｜虛構資料 | c3, c12 |
| 05:13 | json-stream-question | big | 同一份錯誤輸出還包含另一種訊息 | c12 |
| 05:22 | stderr-contract | table | 本地操作2026-10-25｜DuckDB2.0｜虛構資料 | c12 |
| 05:35 | consumer-expectation | big | 混合訊息流，不是壞JSON | c12 |
| 05:49 | repair-the-name | table | 本地操作2026-10-25｜DuckDB2.0｜虛構資料 | c3, c10, c12 |
| 06:00 | copy-limit-question | big | 修好欄位後，完整查詢準備寫檔 | c2, c13 |
| 06:06 | copy-csv-whole | code | followup.sql 第9–15行／全24行｜本地2.0 | c10, c13 |
| 06:19 | copy-where | code | followup.sql 第9–15行／全24行｜本地2.0 | c10, c13 |
| 06:30 | copy-destination | code | followup.sql 第9–15行／全24行｜本地2.0 | c13 |
| 06:42 | copy-parquet-whole | code | followup.sql 第16–22行／全24行｜本地2.0 | c13, c14 |
| 06:53 | run-followup | code | 公開教材根目錄｜Linux2.0實際執行的完整命令 | c7, c13 |
| 07:00 | read-exported-count | code | followup.sql 第23–24行／全24行｜本地2.0 | c4, c13 |
| 07:12 | actual-export-count | quote | 公開教材Linux2.0實跑｜runlogs/agent-followup.stdout.txt | c4, c13 |
| 07:23 | same-version-same-answer | big | 模式改顯示，沒有改篩選答案 | c15 |
| 07:34 | handoff-question | big | 確認內容，而不只看副檔名 | c14 |
| 07:41 | read-parquet-back | code | readback.sql 第3–6行／全6行｜本地2.0 | c14 |
| 07:54 | run-readback | code | 公開教材根目錄｜Linux2.0實際執行的完整命令 | c7, c14 |
| 08:01 | first-delivered-late | table | 本地操作2026-10-25｜DuckDB2.0｜虛構資料 | c9, c13 |
| 08:10 | tail-of-output | table | 本地操作2026-10-25｜DuckDB2.0｜虛構資料 | c13, c16 |
| 08:22 | route-summary-query | code | followup.sql 第5–8行／全24行｜本地2.0 | c16 |
| 08:34 | route-summary-result | table | 本地操作2026-10-25｜DuckDB2.0｜虛構資料 | c16 |
| 08:46 | full-content-comparison | big | CSV與Parquet讀回結果相符 | c4, c14 |
| 08:58 | source-predicate-check | big | 標準函式庫逐筆套條件，另核對全部代號 | c4 |
| 09:11 | change-the-requirement | big | 同一份資料，修改一個比較條件 | c24 |
| 09:19 | new-requirement-consequence | big | 改的是交付需求，不是修正舊清單 | c11, c24 |
| 09:28 | due-or-late-rule | code | variant.sql 第2–8行／全10行｜本地2.0 | c24 |
| 09:40 | run-variant | code | 公開教材根目錄｜Linux2.0實際執行的完整命令 | c7, c24 |
| 09:47 | variant-members-question | big | 同一份原表，只修改這個比較符號 | c24 |
| 09:53 | variant-result | table | 本地操作2026-10-25｜DuckDB2.0｜虛構資料 | c24 |
| 10:05 | on-time-enters-variant | table | 本地操作2026-10-25｜DuckDB2.0｜虛構資料 | c9, c24 |
| 10:15 | different-deliveries | big | 同一原表，完整結果隨需求改變 | c11, c17, c24 |
| 10:27 | handoff-pack | table | 本地操作2026-10-25｜DuckDB2.0｜虛構資料 | c17 |
| 10:39 | keep-the-rule | outro | 完整清單，附上完整規則 | c17 |

冷開場前四句包含可聽到的年份／動作，三個未答時刻停在結果之前。新聞與模式用途移到任務起點，試用範圍只講一段；末章承接新需求，不另開升級故事。中段保留JSON整串解析與存檔會否截短兩個實際問題，完整條件只口述一次，後續點名回呼。第六章包含正文outro，不另起第七章。

原生估計總長652.333秒；冷開場31.300秒；保守另排除冷開場及正文outro後608.033秒。正式正文規定只排外加頻道片頭片尾；這裡額外保守估算是留製作餘量，不改正式口徑。實際自然TTS仍未完成。
