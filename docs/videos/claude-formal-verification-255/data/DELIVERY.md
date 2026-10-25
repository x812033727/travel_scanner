# 本片實跑資料

兩個例子是本片原創教學碼。guard與loop各自有完整0..255輸入，兩個獨立程式不能當串接漏洞。

原始實跑的manifest.json（九檔）與loop-manifest.json（五檔）均對原始work目錄逐一核對SHA及大小，14/14一致。編譯後guard-demo與loop-demo執行檔不放公開repo；原manifest保留它們實際SHA，公開的delivery-manifest.json另記哪些檔案有隨附，不把缺檔當已交付。

在具備Python、GCC及SymPy的環境，可從此目錄執行`python run_demo.py`與`python run_loop_demo.py`。Runner會重新編譯、更新結果與manifest，求解時間、路徑及二進位SHA可能不同；先保留這份原始快照，再重跑。沒有執行Rocq、SMT或vendor checker。

本輪結果為guard改用uint16_t總長或n<8後，全256例符合應且只應接受0..7的契約；loop改用uint16_t計數器後全256例返回n+1。完整程式、CSV／JSON與求解器輸出均在此，不靠圖卡代替實際數據。
