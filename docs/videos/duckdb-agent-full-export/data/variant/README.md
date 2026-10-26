# 變更需求：剛好準時或晚到

原480筆規則是`status='delivered' AND actual_days>promised_days`。本對照先明確改需求，才將`>`改成`>=`：選出已送達且剛好準時或晚到的720筆，其中240筆`days_late=0`。提前2天和在途空值不入選；不能簡稱一般意義的「所有準時」。[新檔](output/due-or-late.csv)沒有覆寫原[嚴格晚到480筆](../output/late-followup.csv)。

原始input與episode的[input/parcels.csv](../input/parcels.csv)bytes完全相同。獨立標準函式庫逐欄與排序重算720筆；新檔10,852 bytes，SHA256 `fe709f321f03e1334e9ed1ee2b48ded4a5458382a8eff6c1d6af464ce105cf8c`。三組`days_late`為0／1／2各240；R1／R2／R3各240。方法與限制見[獨立核對](../../reviews/variant-artifact-review-20261025.md)。

[variant.sql](variant.sql)、[setup.sql](setup.sql)、[run_variant.py](run_variant.py)、[結果](variant-results.json)及[精確日誌](runlogs/variant.command.json)為原始scratch檔案的原樣保存。原RUN從`fifth-draft`以`../fifth-demo/bin/duckdb`執行，exit0並輸出720；原始cwd／argv沒有改成未執行過的新路徑。此舊helper不直接當可攜子集的啟動器。

供重跑者的[variant-portable.sql](variant-portable.sql)只調整本episode相對路徑並內聯同一setup；完整型別、`>=`、五欄、排序和COPY均保留。這個衍生路徑版本在正式建檔時**未執行**，不另寫成功收據。先按[上層KIT](../KIT-README.md)取得並核對固定CLI，再從`data/`執行：

```sh
./bin/duckdb -no-init -agent :memory: -f variant/variant-portable.sql
```

它只寫`variant/output/due-or-late.csv`，不是`output/late-followup.csv`。原創SQL／fixture／程式沿用[CC0](../LICENSE-ORIGINAL.txt)，DuckDB另按[MIT](../sources/duckdb-license.raw)。本次複製／獨立CSV核對未重新執行DuckDB或呼叫AI產品。
