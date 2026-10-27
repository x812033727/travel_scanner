# DuckDB 原始終端輸出的無損近拍

本目錄保存當次 Root 真正執行的單次 producer 與獨立 PNG 解碼器文字副本。正式渲染仍走 tools/video 原生 screenshot／render；沒有新引擎、語音供應商或全域設定。裁切素材與影片留在 repo 外，未提交媒體。

普通 ffmpeg 僅從已驗原始 PNG 截取兩個固定視窗，不縮放素材像素、不重畫或重排數字／文字；兩個裁切 PNG 的全部 RGBA 位元組與獨立解碼的原圖視窗完全相等。原生卡片按版型放大顯示這些無損素材，與「裁切本體沒有縮放」分開。

兩處目標是一般模式1200 rows (40 shown)／5 columns，以及代理模式1160 rows omitted和前後P0020／P1181。真1920×1080與480×270視覺檢查只接受這些原始英文目標；代理圖最上緣P0017局部裁掉的限制保持，不聲稱全部資料列或整片畫面通過。來源標記為原創視窗局部、2026-10-27重現及虛構fixture2026-10-25。

111句、全部八語文字、claims、聲音、speech38cf及scriptb917／narrativeffa6不變；舊核准stale、worker check missing、兩份12/13 false和全部失敗／未知／快取／上限保持。Helper永久marker已消耗，副本不是可以重播的續作工具。先前版本固定於同分支前一commit4964d8753270b587c7c8b07cd1e33d0a39beb162；當輪完整前態與變更前可變檔另存repo外B/before，未遞迴複製history。
