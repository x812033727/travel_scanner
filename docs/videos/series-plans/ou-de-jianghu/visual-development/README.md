# 《偶的江湖》角色美術前期

2026-10-08，依站主「開始」「繼續」補齊《偶的江湖》首集的美術、分鏡、風險、預算與交接，**前期可審包已形成**。沿用 9 張概念候選及 27 張獨立畫像，新增角色動畫參照、場景／道具參照、可重建的 v3／v3.1 文字動態分鏡，以及外部原圖隔離匯入證據。站主明確接受「保留目前華麗古裝與細緻人物風格」；這不等於個別素材採用、正式 look／plan 核准或已開拍。

本輪入口：[美術定調及接受紀錄](art-direction/README.md)、[九人畫像與圖冊索引](episode1-portraits/README.md)、[27 張獨立視圖](episode1-portraits/independent-views.md)、[角色動畫參照](animation-reference/README.md)、[場景與道具參照](scene-prop-design/README.md)、[P0–P7 可審包 v3](episode-plan/preproduction-package-v3.md)、[外部匯入合約與實證](import-contract/README.md)、[資產與開拍交接](handoff/README.md)。

角色動畫參照已交付 **74 張新增用途候選**（九人各 8 張，共 72 張，另 2 張九人同尺度板），再沿用 9 張正面全身，共 **83 項參照用途**。保留修訂及中間板共90個PNG檔，包含89張唯一生成圖與1個同圖別名；沿用正面不重算新增。數量、版本及候選狀態見 [角色參照媒體收據](animation-reference/media-receipt.json)。場景／道具包另有29張latest、40張raw；所有候選仍待正式採用。

閱讀順序：

下列造型規格、製作清單及來源清冊保留建票時快照；其中「尚未生成／specified_not_generated／media_generated_in_this_task=false」描述當時狀態。最新交付以各批收據及 [139張候選整合清冊](handoff/asset-manifest.json) 為準，不把舊快照當成目前圖片數。

1. [角色造型規格](character-design.md)：人物外觀錨點、輪廓配色、服裝狀態與不可提前揭露的細節。
2. [畫像與動畫參照製作清單](production-list.md)：分批角色、每人交什麼圖、製作及验收方式。
3. [來源綁定清冊](asset-inventory.json)：24 位角色聯集、16 種命名造型、現有集鏡使用與 SHA-256；這是前期清冊，不是 runtime manifest。

## 本次查到的現況

| 項目 | 2026-10-08 倉庫快照 |
| --- | --- |
| 故事設定 | `setting.json` 20 位主要人物 |
| 共用製作角色表 | `production/cast.json` 19 人、16 種 `shot_looks` |
| 合併人設範圍 | 24 人：第一季 23 人，褚無常正臉留第二季；第一集黑風另列效果參照 |
| 第一集實際入鏡 | 9 人，包含玄門長老與洛青衍 |
| 已有稿件 | 第 1–7 集；第 8 集角色準備已進共用表，劇本工作仍有既有票 |
| 沿用角色圖 | 9 張概念 latest，保留修訂共 14 PNG；27 張獨立視圖 latest，保留三張半身舊版共 30 PNG。兩組共 36 張用途候選，不計入新增參照需求 |
| 新增參照 | 角色動畫參照74張新latest＋9張沿用正面，83項用途；保留90個PNG檔＝89張唯一生成圖＋1同圖別名。場景／道具29張latest、40張raw。修訂與淘汰版本保留，不能以檔案總數充交付數 |
| 圖片核准與尺寸 | 共同畫風已接受，個別素材採用及正式 look 仍待決定。獨立視圖的 18 張半身／全身低於建議尺寸；原件尺寸逐張記錄，未自行放大或以工程通過代替美術採用 |
| 分鏡與動畫預演 | v3：455 鏡、4 字卡、23:23.533，完成原速全長播放及全部卡面觀察；v3.1 只補首／末格文字顯示，另完成 23 卡獨立複看，未冒稱第二次全長觀看 |
| 外部 PNG 接入 | `look import --image … --source …` 已實作；9 張既有全身原圖已在隔離 workbase 建立 pending 候選，0 次 fetch，無 judge／choice／approval，正常 runtime 尚未採用 |
| 工程驗證 | 匯入、keyframes、series-store、review 及 automation/series 相關 229 測試通過；不代表全庫測試全綠、部署完成或角色圖已核准 |

來源見 `asset-inventory.json` 的 `source_files`，本批再次核對 12 檔 SHA；文字稿與共用角色表目前同角色物件一致。清冊與製作清單保留前期規格快照，生成狀態以最新媒體收據為準。v3 工作提案與原 e001 分開保存，來源及產物 SHA 見審閱包；獨立播放的工具間隙、補看範圍及 v3.1 限制見 [觀看紀錄](episode-plan/cold-review-independent.md)。`production/README.md` 的「14 人」過期敘述已納入交接；本輪不改原持有人正在做的 `production/` 或 e001。

## 已補入共用任務佇列的 8 張票

下表保留八項工作。美術方向及外部匯入工程已結案；首集的前期文件與候選資產已有可審交付。仍要求正式採用、原生核准或下游實測的票保留待辦，不能用票未結案反推前期包未製作，也不能以文件完成宣稱已開拍。

| 工作 | 交付與先後 |
| --- | --- |
| [1. 開拍前置包](../../../../../tasks/open/2026-10-08-ou-de-jianghu-preflight-plan.md) | P0–P7 可審包、逐鏡覆寫、風險裁定、343 組鏡位、完整分項預算、v3／v3.1 與三鏡小樣計畫已完成；待對具體包作正式決定，不寫假 lock |
| [2. 三位主角美術定調](../../../../../tasks/done/2026-10-08-ou-de-jianghu-art-direction.md) | 已完成方向接受、三人候選比較、獨立實圖審查和提示／SHA保存；前置包未鎖定下的有界概念製作理由記於票內 |
| [3. 第一集 9 人畫像](../../../../../tasks/open/2026-10-08-ou-de-jianghu-episode1-portraits.md) | 已生成並實看 27 張獨立候選、保存修訂與 SHA；待個別採用及最終尺寸決定，並沿用於新增參照 |
| [4. 第一集動畫參照](../../../../../tasks/open/2026-10-08-ou-de-jianghu-animation-reference.md) | 已交付 74 張新增候選：各角色 5 個單獨角度、表情板、動作板、細節板及兩張同尺度板；加 9 張沿用正面共 83 項用途，生成／修訂／實看及 SHA 收據齊，仍待正式採用 |
| [5. 後續角色及 16 種狀態](../../../../../tasks/open/2026-10-08-ou-de-jianghu-supporting-looks.md) | 第一季餘下 14 人、命名造型與隱藏身份細節；依第 2 張票，可分批，不阻塞第一集 |
| [6. 場景與道具參照](../../../../../tasks/open/2026-10-08-ou-de-jianghu-scene-prop-design.md) | 29 張最新候選、40 個原始 PNG 已生成並實看，含空間／光色／道具／受控局部及455鏡索引；紙窗近景、棋盤及事件前後狀態限制已留記 |
| [7. 外部設定圖匯入能力](../../../../../tasks/done/2026-10-08-ou-de-jianghu-external-look-import.md) | 工程完成，相關229測試通過；9原圖隔離 pending 匯入／去重／SHA實證齊。真實 judge、選圖、正式 look 及正常 runtime 接線仍須取得實際證據 |
| [8. 資產鎖定與試播交接](../../../../../tasks/open/2026-10-08-ou-de-jianghu-visual-handoff.md) | 可審包、資產／匯入收據及三鏡試播執行次序已成文件；正式採用後才接正常關卡與既有試播，不把隔離測試當正式製作 |

目前交付到首集前期可審包；後續順序為 **整包與素材正式採用 → 正常 look／plan 關卡 → TTS／聽審 → 關鍵影格／storyboard → a02-s035～s037 連續三鏡動畫小樣 → 接回既有試播**。本輪沒有執行付費 TTS、關鍵影格、judge 或影片生成，也沒有擴做全季。

## 與既有工作的接點

- [第 1 集 Hailuo 試播](../../../../../tasks/open/2026-10-04-clip-route-pilot-comparison.md)已涵蓋整集製作、匯入與成本實測，保持為下游唯一試播票。既有 Hailuo 路線意向保留，報價、帳號與匯入能力在執行時重驗，不另開三家比價。
- [第 8 集劇本](../../../../../tasks/open/2026-10-06-ou-de-jianghu-e008-script.md)持有人占用 `production/`；[傳單知情問題](../../../../../tasks/open/2026-10-05-ou-de-jianghu-ep8-leaflet-knowledge.md)仍是劇情待決事項，美術工作不代替答案。
- **本輪未修改既有試播票的 `depends_on`**。第 8 張新票明列接線待辦；取得原持有人交接後才更新其依賴／checklist，不能宣稱這裡的文件已機械阻擋其他工人。不得讓新票反向依賴試播完成，造成循環。

## 能力與完成狀態

`tools/video/media/look.mjs` 已新增正式外部候選匯入入口：`look import --image PNG --source JSON`。`--file` 仍指專案 JSON，不是圖片參數；不帶 `--judge` 時只離線保存原圖、來源收據與 pending manifest，不生成、不上傳、不選用或核准。9 張首集全身原圖的 [隔離匯入收據](import-contract/pending-staging-receipt.json) 已驗證這条路徑，正常工作目錄及正式 look 尚未因此採用。

正常 `sheetPrompt` 仍讀基底 `appearance`／`sheet_prompt`；`keyframes.mjs` 每角色讀一張已選的基底圖。`shot_looks` 仍是當鏡外觀文字覆寫，多角度、表情、道具及場景包不會因存入磁碟就自動全數送給模型。已核准基底跨集共用沿原有 `series-store.mjs`，沒有另造第二套核准庫。

「候選圖片已生成」「參照包可審」「9 圖隔離 pending 匯入」「正常 look 已核准」「關鍵影格真正引用」「動畫小樣實看接受」分別記錄。這輪存在的是工具真實產出的隔離 pending manifest；沒有捏造 judge、choice、approval，也不把任務檔或229項工程測試當作圖像採用證明。原生 readiness 尚缺的核准與媒體是正式製作階段的前提，並非把已完成的 P0–P7 規劃文件一律算成未完成。

未來變更臉、服飾錨點或 palette 時先列受影響角色／造型／鏡頭與成本，再依既有變更單處理。清冊另綁造型來源 SHA，因目前原生 `lookHash`／`sheetKey` 不含 `shot_looks`；這只是前期檢查約束，不是已實作的新管線保證。
