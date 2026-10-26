# 單句事實澄清後：衍生物自核

當前source `7d150fc4e8a818e80560c80e4a392e93699666571c3647d4471b4222bcfb0726`；claims `cc38eeb8634eaa45c2a46c981bb1f7b0c9fca034158647437c1de0de8fd79191`。這不是story R3，額外敘事改寫次數為0。root已套用唯一V1-F1：rxjg由「剛剛分組的完整檔，路線二和路線三各有兩百四十筆。」改成「剛剛按原規則分組，路線二和路線三各有兩百四十筆。」。本次沒有寫入video.json或claims.md。

先把這一個text還原再逐物件比較，結果與before-fact-clarification完全一致；另外110句文字與全部非text欄位、數字、卡片、命令、metadata、章名、loops都未改。此句現在對應followup.sql以FROM parcels加原predicate做GROUP BY的實際查詢，沒有把它稱為匯出CSV再分組。

更新的是當前旁白稿、scene plan、原生估時／schema／lint／收據、current source input receipt、verification及handoff／manifest。r1-*及r2-*是各自原始SHA的歷史記錄，不以7d重綁；reader5／6的raw／native只保存檔案SHA，原13 booleans與歷史1a綁定不改、不重新評分。

before-fact-clarification的133列manifest全核對；固定98檔與第五原始demo93檔皆不變。公開./duckdb完整命令、兩組480／720全量資料與240零差值、重跑proof、新ZIP74064…全部保持，沒有執行SQL、重包ZIP或刷新官方來源。

native schema0錯誤，lint0errors／0warnings，source與claims綁7d／cc38。64景／111句／2282原生口語單位，估計總628.200秒、cold 31.300秒；保守另排cold與outro後583.900秒。沒有TTS、音檢、render、paid或後臺；這些估計不是實際媒體驗收。

build_draft.py／build_r2.py及review_r2.py保留為歷史R2生成器，重跑會重建1a，不能拿來覆蓋root的7d事實澄清。當前只讀刷新入口是refresh_fact_derivatives.py或finalize_draft.py。
