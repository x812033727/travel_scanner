# 證據路徑與教材身分

[claims](claims.md)與原始review保持原bytes，其scratch別名由[evidence-path-map.json](evidence-path-map.json)對應本episode檔案。

- 本片畫面使用的可讀SQL與舊工作區重跑紀錄：[demo](demo/)及[runlogs](runlogs/)。
- 真正公開根目錄的9條`./duckdb`命令、raw與實際輸出：[public-run](public-run/README.md)，對應[新ZIP](duckdb-public-fixtures.zip)。42entries／26,889B，SHA74064ba70799606bf6c8fbc970109bfad26d0d8a02b73e2c5691534678b9fdf2。
- [data](data/README.md)是先前研究快照，命令根目錄／檔名為舊`./bin/duckdb`方案；其variant portable SQL當時明示未執行。原檔不覆寫，不拿舊路徑冒稱目前公開9命令。
- [原創HTML報告](data/output/followup-report.html)是先前實際產物，可連到歷史完整檔。新42entry ZIP沒有HTML，兩個產物不混稱同一包。
- `../fifth-demo/input/fixture-description.json`對應[data/input/fixture-description.json](data/input/fixture-description.json)；同前綴的artifact-verification／results對應[data](data/)。原始舊fifth-followup-kit.zip只保留身分，不作目前下載包。
- 原作者重做程式在[authoring](authoring/)，保留原觀測路徑供查證，不是在episode根目錄可直接執行的公共入口；請依public-run README的完整CLI命令重做。

官方大HTML／原始shell.cpp／77MB CLI／24MB官方archive／symlink不入本episode；[來源身分](sources/identity-index.json)與HTTP收據保存URL、時間、SHA。原始完整capture仍在既有研究scratch，不假稱本輪新GET。原創素材CC0、DuckDB MIT、官方文稿各自歸屬。
