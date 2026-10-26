# C11 UCC：新規則重製

R6精確稿已通過[獨立來源／書面配鏡與規劃共圖](reviews/source-r6-independent.json)、[兩位全新讀者原生合併](reviews/narrative-r5.json)與[正常不可變字典情境預檢](reviews/canonical-lint-r6.json)。actual native panel5屬作者R6，合併PASS保留A單人no_recap意見及B13yes，不冒充全票通過。80句、78景，其中77個插畫景與1個outro；whole narration 2276 spokenUnits，實聲未知，字量有明顯偏短規劃風險，沒有13分鐘時長PASS。

來源video SHA `03817277b5c79f45c6064a082ac9a23279b9b11b289cd091cb2261a212d5d38b`；官方writeScreenplay SHA `4011ea915073e7ae6bc5a796eb06aff337020bdd0e946c73d76b2d85065af005`。作者[附來源劇本](script.md)與[實際送後台官方投影](backend-script.md)分開保存。原[作者brief](brief.md)及其來源／共圖綁定完全不改；[送審brief](submission/brief.md)只補單一A原生欄位，取自已審稿。送審前副本與差分收據見[保全](history/r6-before-submission/brief-preparation.json)。

企劃 `ee93f101-d27e-4980-82e6-d2f89d07cacc`、劇本 `e57b1958-8d93-44d3-b203-1098c5af4a81` 已由官方CLI送審並在 `2026-10-26T00:20:28.472Z` 真實讀回pending；實際分類story，未綁原集或series，沒有新owner批准。後台stage「outline approved」是下一步名稱，不能當作已批准。[正式卡](https://mokaair.com/zh-TW/admin/videos?tab=drama&video=story-everyday-ucc-c11-remake-20261025)。

[八語文字](i18n/README.md)目前只有每語80句／6章的原生來源worksheet，未翻譯或審讀；目前後台locales為空、無決定時間。預設八語已授權，[具體設定](protected-admin-settings.json)需要合法content.manage身分套用並讀回，未假造native languages.json。

[免費預檢](preflight-inputs.json)：78個TTS請求、2588計費字元；77圖景，每景最多含首次3次，目錄估圖像費US$1.04／最多3.12，非全片報價。原生lint0errors、3個soft warnings保留。付費請求與生成媒體均0。

[共圖sidecar](image-reuse-plan.json)只是規劃，已保存至runtime production-handoff，沒有已驗圖或真實檔SHA。原生CLI不會強制兩景共用，cache缺失仍可能派送新的付費生成；操作者須在預告命令前核實際已驗cache、精確key和檔案，缺件或不同就停止，不能自動worker或另買相似圖冒充共圖。兩端實際選中及裁切後檔案SHA、各context驗收與ledger尚待。

[clean-master](variants/clean-master/derivation.json)只有未執行配方，燒錄旗標是唯一差異，原生hash與0error檢查通過，尚待獨立metadata審查。沒有clean影片、QA、final或dub資格。實際製作見[production-entry.md](production-entry.md)。
