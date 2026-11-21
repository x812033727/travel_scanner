# Doraemon remake R1作者提交包

新slug：`story-adapt-doraemon-after-fujiko-remake-20261025`。這是作者候選，不是獨立SOURCE、說故事、念法、實聲、影像、owner、預算或製片通過收據。

可重播來源在`rows-r1.json`與`build-candidate.py`；研究三檔已固定SHA，build遇研究漂移會停止。從repo根目錄執行：

```bash
python docs/videos/brand-story-remakes-20261025/doraemon/build-candidate.py
node docs/videos/brand-story-remakes-20261025/doraemon/build-image-reuse-plan.mjs
node docs/videos/brand-story-remakes-20261025/prepare-runtime.mjs /workspace/work/brand-story-20261025/doraemon-submission-root /workspace/work/brand-story-20261025/doraemon-audit/media doraemon
node docs/videos/brand-story-remakes-20261025/runtime-cli.mjs /workspace/work/brand-story-20261025/doraemon-submission-root lint --slug story-adapt-doraemon-after-fujiko-remake-20261025 --json
```

這些只重播來源、初始化／讀取本片immutable字典與免費正常lint；沒有付費、後台或owner操作。既有immutable字典只有一個version，不可刪除重建。runtime與media均在repo外，media另在runtime外。`build-image-reuse-plan.mjs`只呼叫純`Stage.imageKey`，沒有`Stage.image`、狀態讀回或live cache證明。

`native-author-lint-r1.json`保留最後一次完整正常lint，包括所有soft warnings。前置免費schema嘗試與cadence修訂前後的原收據在`/workspace/work/brand-story-20261025/doraemon-audit/free-lint-attempt-*.json`；它們不算fresh native讀者輪次。`pre-cadence-author-working/`保留刪相鄰重述前的作者版本。最終freeze記原生精確units、149行、鏡頭、loops、四個核心SHA及全部保護結果。

本片固定13分鐘；實聲body720–840秒包含開場與voiced CTA，排新增5秒片頭與21秒v4片尾。3368 native spokenUnits低於約3500的容量目標，不能當實聲證明，也不靠調慢、插停頓或重複填長。原生估計加入預設行／鏡頭間隔，仍有片長soft warning；實聲量測後才可判斷是否達標。繁中試燒+CC，後續八語en/ja/ko/es/pt/id/vi/th與乾淨主片按正常流程待製。

原片及9份相關舊原件的bytes保護、42筆原下載與搜尋快取的SHA檢查在`protected-inputs.json`。舊付費媒體本機不可讀，不聲稱已保全。D03第三回起接手敘述仍是官方對談搜尋快取，origin HTTP503；2017回憶、完整書頁與附件的可讀範圍照錨點限定。新增A01–A07作者錨點只引用既有raw，不改研究三檔。

獨立US$25精確帳戶／全片quote／protected admission未建立；新片不借舊帳戶或歷史批准。所有SOURCE／fresh native雙讀者／念法／實聲／影像／owner均pending。`author-freeze-r1.json`只有作者完整性意義。
