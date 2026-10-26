# 可攜練習包：先看成品，再準備相符CLI

`output/followup-report.html`、CSV與Parquet是已完成的實物，無需帳號可讀。資料為原創虛構教學fixture，不是真業務或公共統計；完整條件和排序在`sql/03-followup.sql`。

此小包刻意不附77MB執行檔或24MB官方壓縮包。下列重跑步驟適用已具備Python3與curl的Linux amd64，CLI只解到此資料夾，不安裝系統服務。先讀DuckDB MIT、相關CLI程式與`run_demo.py`／SQL，再執行。下載為固定官方2.0版本、正常editorial UA，先核SHA才解開：

```sh
mkdir -p bin sources
curl -L --fail --max-filesize 52428800 \
  -A 'Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)' \
  'https://github.com/duckdb/duckdb/releases/download/v2.0.0/duckdb-cli-linux-amd64.tar.gz' \
  -o sources/duckdb-cli-package.raw
printf '%s  %s\n' \
  'c6507206baf7793c6013dbd82368469a45f20dc0e17a6f92f204602f652ed2bc' \
  'sources/duckdb-cli-package.raw' | sha256sum -c -
tar -xzf sources/duckdb-cli-package.raw -C bin
python -B run_demo.py
```

本輪真的下載／校驗／執行了這個固定版本；上面的curl版是給重跑者的完整取檔方式，本輪HTTP工具採Python urllib並保存收據，不假稱另外以curl做過獨立下載測試。只有`python -B run_demo.py`和記錄中的精確CLI命令是已執行紀錄。

要只看同一查詢的兩種印法：

```sh
./bin/duckdb -no-init -no-agent :memory: -f sql/01-preview.sql
./bin/duckdb -no-init -agent :memory: -f sql/01-preview.sql
```

`-no-init`略過個人預設初始化檔；`:memory:`為這次臨時資料庫。完整匯出SQL內另關閉自動擴充安裝／載入。沒有任何帳號／API key、遠端服務或生產資料庫操作。跨平台相容性、模型推理、費用／token節省與舊資料庫升級未測。

[manifest.json](manifest.json)只核對本正式可攜子集的文件SHA；沒有沿用會列出未附PNG／完整CLI原始碼的舊kit manifest。[verify_demo.py](verify_demo.py)可核對已產出的CSV／保留Parquet讀回、JSON行與顯示標記；它不重新解碼Parquet，也不證明任意查詢或AI回答都正確。重跑會更新本包自己的輸出／時間紀錄，不改系統或其他資料。本次正式建檔只複製並靜態核對原產物，未執行上述下載或重跑命令。
