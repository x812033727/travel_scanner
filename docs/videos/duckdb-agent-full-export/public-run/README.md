# 完整配送清單教材：公開根目錄重做

本教材是原創1200筆虛構配送資料與確定性作者SQL，非真公司／個資／公共統計；沒有獨立AI產品或模型測試。原創fixture、SQL、文字與紀錄採CC0-1.0，DuckDB另採MIT。

解壓後，以這個README所在的根目錄為目前工作目錄。另從DuckDB官方取得適合自己平台的2.0 CLI，依其MIT授權使用。這份實際紀錄只測Linux amd64的v2.0.0 (Cyanoptera) d54cbbe3df；不承諾其他OS已實測。Linux範例把可執行檔放在根目錄，名稱為duckdb。執行檔／symlink／官方壓縮包不在教材內。

這輪工作區用symlink ./duckdb指向已驗官方同版本CLI，再執行以下原樣命令。公開路徑不是只改字，raw記錄在runlogs/，完整核對結果在public-run-results.json。跨平台的檔名與可執行方式可能不同，以下是本輪Linux實際命令。

setup.sql明確停用extension自動安裝／載入；每個查詢用臨時資料庫並略過初始化檔。先執行preview，再執行故意錯字示範；typo兩條預期exit1且不產生查詢結果。其餘命令預期exit0。輸出目錄demo/output/已在教材中；再次執行會重產生其中教學檔案。

## 完整原樣命令

```sh
./duckdb --version
```

```sh
./duckdb -no-init -no-agent :memory: -f demo/preview.sql
```

```sh
./duckdb -no-init -agent :memory: -f demo/preview.sql
```

```sh
./duckdb -no-init -no-agent :memory: -f demo/typo.sql
```

```sh
./duckdb -no-init -agent :memory: -f demo/typo.sql
```

```sh
./duckdb -no-init -agent :memory: -f demo/followup.sql
```

```sh
./duckdb -no-init -no-agent :memory: -f demo/followup.sql
```

```sh
./duckdb -no-init -no-agent :memory: -f demo/readback.sql
```

```sh
./duckdb -no-init -agent :memory: -f demo/variant.sql
```

## 核對與自行改需求

完整SQL在demo/。followup.sql的主條件是status='delivered' AND actual_days>promised_days，交付480筆；先比較模式時，兩者使用同一版本和同一SQL。40是1200筆原表的顯示列數，1160 omitted只是沒有顯示，不是資料遺失。

CSV與Parquet含包裹代號、路線、承諾天數、實際天數、晚到天數，按包裹代號升冪。readback.sql讀回Parquet並存成CSV，與主CSV逐bytes相同；public-run-results.json另以標準函式庫逐列核對所有欄位及原始條件。

variant.sql把>改>=，另存due-or-late.csv；得到剛好準時或晚到720筆，其中240筆差值為0。不包含早到；不把這720筆全叫延遲。原480筆檔案保持。修改自己的需求時，同時改比較條件與目的檔名，再執行、核對。

agent-typo.stderr.txt第一行是啟動文字，第二行才是一個合法JSON物件。整個stderr不是單一JSON文件；讀取程式要先辨認訊息行，再解析JSON行。這是讀取契約的區分，不是DuckDB產生壞JSON，也不代表真第三方工具已故障。

完整輸入／SQL／輸出／raw紀錄的SHA在public-kit-manifest.json。SHA是核對檔案身份，不是AI正確性、速度、token或費用測試。
