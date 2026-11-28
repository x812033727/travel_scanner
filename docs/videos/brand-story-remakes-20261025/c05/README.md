# C05 金鳥 R13 新規則重製

已採用[109句R13](video.json)，來源、書面配鏡／共圖計畫及兩位全新讀者的原生第12輪合併均PASS；讀者A單人one_line/no_recap意見完整保留，讀者B13yes，不改成一致同意。實際字典情境lint0errors，16個拆句翻譯過期／缺漏提示仍屬本輪真實待辦。

原c07o04拆為兩個未揭結果預告，其餘107句原話與史實不變。[同圖計畫](image-reuse-plan.json)只記完整request/cache/實檔SHA後驗流程，尚無生成圖。source、正式劇本與舊批准的[採用收據](adoption-r13.json)分別綁定：來源773836e4…；官方劇本3f2f19c4…。原批准檔SHA ef6e1cae…原封保留，不適用新canonical。

[新版企劃與劇本](backend-status.json)已透過正式工具免費送審並讀回pending，分別為3f9e948c-8a95-43de-bbb9-d06d45a4cb2a、7eda9d94-62a3-4cd2-9bfe-5cdc48341126。送審format使用[submission/brief.md](submission/brief.md)，原來源綁定brief不改；原R12在送R13之前已讀到script approved，該決定只屬67bd2b41…而不能借給R13。R12完整來源、官方劇本、864句八語、審查與clean舊配方在[完整封存](history/before-teaser-r13/)。

現行[八語文字](i18n/README.md)待每語2句delta，其餘107句與metadata完整承接，但未宣稱109句已全current TEXT_PASS。已存正式八語三parts原選擇與原決定時戳，不是實際配音資格。

[製片交接](production-entry.md)仍被精確新版預算帳戶、歷史費用／全片報價及受保護啟用、正式v4來源等入場要求擋住。實聲正文720–840秒未量測，3041 spokenUnits不是時長PASS。免費預檢107 TTS請求／3454字元，106圖景的目錄估價US$1.43／最多3次US$4.29，不是全片報價或泛US$200授權。clean-master只有未執行配方，尚待獨立metadata覆核及正式生成後的完整QA／final。

本輪不重綁原episode、不修改budget guard、不自批准、不建立auto.json。付費、生成音訊／插圖／配樂／影片與YouTube變更均0。父層build-candidate.py為舊稿歷史入口，勿重跑覆寫；目前凍結producer在candidates/teaser-image-plan/build-candidate.mjs，重建候選後仍要按精確SHA受控採用。
