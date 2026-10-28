# 六章操作製作規劃

全部為原創紙底教學卡；未render、未付費、未正式登記。每個操作引用保存的SQL或實際輸出，不造產品對話。

| 估計位置 | 場景 | 版型 | 操作／證據 | 主張 |
|---|---|---|---|---|
| 00:00 | parcel-table-start | big | 原創虛構教學資料 | c1 |
| 00:05 | running-followup-task | big | 同一份練習表的查詢狀態 | c1, c5 |
| 00:09 | forty-visible | big | 顯示內容仍有省略 | c2 |
| 00:14 | missing-question | big | 先分清資料與顯示 | c2 |
| 00:18 | typo-question | big | 相同欄位需求會收到什麼回覆 | c3 |
| 00:23 | export-question | big | 清單另存後，還要讀回 | c4 |
| 00:28 | one-running-task | big | 保留同一份清單的規則 | c1, c4 |
| 00:34 | input-is-still-there | big | 省略的是顯示，不是紀錄 | c1, c2 |
| 00:45 | input-columns | table | 本地操作2026-10-25｜DuckDB2.0｜虛構資料 | c1, c5 |
| 00:55 | mode-role | compare | 官方agent文件｜2026-10-25 | c6 |
| 01:06 | force-human | code | 可照寫命令｜同一固定DuckDB2.0二進位 | c6, c7 |
| 01:17 | force-agent | code | 可照寫命令｜同一輸入與同一2.0版本 | c6, c7 |
| 01:27 | find-the-omission | big | 從回覆中定位顯示範圍 | c2 |
| 01:32 | same-preview | code | preview.sql 第1–3行／全3行｜本地2.0 | c7 |
| 01:41 | human-footer | quote | 本地2.0一般模式輸出節錄｜runlogs/human-preview.stdout.txt | c2 |
| 01:51 | agent-omitted | quote | 本地2.0代理模式原文｜runlogs/agent-preview.stdout.txt | c2 |
| 02:00 | same-result-different-view | table | 本地操作2026-10-25｜DuckDB2.0｜虛構資料 | c2, c6 |
| 02:10 | define-the-followup | big | 把需求寫成可執行條件 | c5 |
| 02:21 | explicit-input-types | code | setup.sql 第5–9行／全9行｜本地2.0 | c5, c7 |
| 02:30 | inspect-columns | code | followup.sql 第1–4行／全24行｜本地2.0 | c5, c8 |
| 02:39 | input-status-count | table | 本地操作2026-10-25｜DuckDB2.0｜虛構資料 | c1, c8 |
| 02:49 | apply-both-conditions | big | 依同一份表逐項判斷 | c5 |
| 02:55 | read-one-parcel | table | 本地操作2026-10-25｜DuckDB2.0｜虛構資料 | c9 |
| 03:04 | compute-days-late | table | 本地操作2026-10-25｜DuckDB2.0｜虛構資料 | c9 |
| 03:14 | in-transit-example | table | 本地操作2026-10-25｜DuckDB2.0｜虛構資料 | c9 |
| 03:23 | where-is-complete | code | followup.sql 第9–15行／全24行｜本地2.0 | c5, c10 |
| 03:34 | voice-the-rule | big | 兩個條件必須同時成立 | c5, c10 |
| 03:45 | selection-and-order | code | followup.sql 第9–15行／全24行｜本地2.0 | c10 |
| 03:55 | strict-greater | compare | 本地操作2026-10-25｜DuckDB2.0｜虛構資料 | c5, c11 |
| 04:05 | on-time-example | table | 本地操作2026-10-25｜DuckDB2.0｜虛構資料 | c9, c11 |
| 04:14 | field-name-question | big | 條件寫對後，還得使用真正欄位 | c3 |
| 04:20 | intentional-typo | code | typo.sql 第1–3行／全3行｜本地2.0 | c3 |
| 04:31 | human-error | quote | 本地2.0一般模式stderr｜runlogs/human-typo.stderr.txt | c3 |
| 04:39 | valid-json-fields | table | 本地操作2026-10-25｜DuckDB2.0｜虛構資料 | c3, c12 |
| 04:50 | stderr-contract | table | 本地操作2026-10-25｜DuckDB2.0｜虛構資料 | c12 |
| 05:02 | consumer-expectation | big | 混合訊息流，不是壞JSON | c12 |
| 05:14 | repair-the-name | table | 本地操作2026-10-25｜DuckDB2.0｜虛構資料 | c3, c10, c12 |
| 05:23 | copy-csv-whole | code | followup.sql 第9–15行／全24行｜本地2.0 | c10, c13 |
| 05:35 | copy-where | code | followup.sql 第9–15行／全24行｜本地2.0 | c10, c13 |
| 05:46 | copy-destination | code | followup.sql 第9–15行／全24行｜本地2.0 | c13 |
| 05:58 | copy-parquet-whole | code | followup.sql 第16–22行／全24行｜本地2.0 | c13, c14 |
| 06:07 | read-exported-count | code | followup.sql 第23–24行／全24行｜本地2.0 | c4, c13 |
| 06:18 | actual-export-count | quote | 本地2.0 exported_rows原文｜runlogs/followup.stdout.txt | c4, c13 |
| 06:28 | same-version-same-answer | big | 模式改顯示，沒有改篩選答案 | c15 |
| 06:38 | handoff-question | big | 確認內容，而不只看副檔名 | c14 |
| 06:45 | read-parquet-back | code | readback.sql 第3–6行／全6行｜本地2.0 | c14 |
| 06:55 | first-delivered-late | table | 本地操作2026-10-25｜DuckDB2.0｜虛構資料 | c9, c13 |
| 07:05 | tail-of-output | table | 本地操作2026-10-25｜DuckDB2.0｜虛構資料 | c13, c16 |
| 07:16 | route-summary-query | code | followup.sql 第5–8行／全24行｜本地2.0 | c16 |
| 07:26 | route-summary-result | table | 本地操作2026-10-25｜DuckDB2.0｜虛構資料 | c16 |
| 07:35 | full-content-comparison | big | CSV與Parquet讀回結果相符 | c4, c14 |
| 07:46 | preview-versus-file | compare | 本地操作2026-10-25｜DuckDB2.0｜虛構資料 | c2, c4, c17 |
| 07:57 | change-the-requirement | big | 同一份資料，修改一個比較條件 | c24 |
| 08:02 | due-or-late-rule | code | variant.sql 第2–8行／全10行｜本地2.0 | c24 |
| 08:13 | variant-result | table | 本地操作2026-10-25｜DuckDB2.0｜虛構資料 | c24 |
| 08:25 | on-time-enters-variant | table | 本地操作2026-10-25｜DuckDB2.0｜虛構資料 | c9, c24 |
| 08:30 | handoff-pack | table | 本地操作2026-10-25｜DuckDB2.0｜虛構資料 | c17 |
| 08:40 | upgrade-question | big | 先選適合自己工作的用法 | c19 |
| 08:47 | release-time | table | 官方發表與release日期｜2026-10-25核對 | c6, c19 |
| 08:54 | existing-file-tools | big | 讀CSV、SQL查詢與匯出原本就有 | c19 |
| 09:02 | pick-the-tool | compare | 編輯選擇｜非表格工具比較實測 | c20 |
| 09:14 | agent-mode-fit | big | 給自動讀取者清楚的訊息 | c6, c15, c20 |
| 09:26 | lts-is-a-promise | big | 至少到2027年10月 | c21 |
| 09:38 | storage-condition | table | 官方2.0 migration文件｜2026-10-25 | c22 |
| 09:50 | bounded-choice | big | 保留原本的工作與資料庫 | c20, c22 |
| 10:01 | format-is-not-correctness | big | 同版模式對照不等於效能評比 | c15, c23 |
| 10:13 | author-demo-scope | big | 沒有獨立模型或產品前後測 | c1, c23 |
| 10:25 | keep-the-rule | outro | 完整清單，附上完整規則 | c17, c20 |

冷開場先留在同一配送查詢，三個未答時刻用實際任務回收。第六章包含正文outro，不另起第七章。刪除尾聲通用完整prompt；完整選欄、條件、排序與COPY已在操作時呈現和口述。

原生估計總長637.367秒；冷開場34.967秒；保守另排除冷開場及正文outro後590.600秒。正式正文規定只排外加頻道片頭片尾；這裡額外保守估算是留製作餘量，不改正式口徑。實際自然TTS仍未完成。
