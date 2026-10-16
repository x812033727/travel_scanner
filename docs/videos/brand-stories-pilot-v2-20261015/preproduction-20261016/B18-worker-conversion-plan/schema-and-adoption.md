# B18：實際欄位與採用邊界

實作以 `source-pins.json` 的 repository 檔案 bytes 為準；不聲稱正式機目前版本。本文件未建立工具或建議直接改 production state。

## 六章與逐字稿

| key / 未來檔案 | v2 段落 | 原鏡範圍 | v2 units |
| --- | --- | --- | ---: |
| hook.json | H01–H03 | S001–S007 | 188 |
| origin.json | O01–O04 | S008–S022 | 317 |
| idea.json | I01–I04 | S023–S040 | 388 |
| engine.json | E01–E05 | S041–S062 | 508 |
| turn.json | T01 / T01a / T02–T04 | S063–S092 | 578 |
| now.json | N01–N03 | S093–S103 | 315 |

檔案預期位於 work `story/chapters/`，本目錄未建立這些檔案。title 可取 v2 六章既有章名，不拿「開場／結論」代替事件。段落是編輯單位，不直接當一條 TTS line。新 line 保留每個字、標點及順序，逐段重建必須等於 v2；所有替換需另有受審 adaptation，不在轉換時順手改稿。JSON `speaker` 不需要，只有旁白。

## 欄位對照

| 原資料 | Native／sidecar | 注意 |
| --- | --- | --- |
| paragraph.id、CID | sidecar provenance | Native line ID 使用其允許字元與受配置 ID；不能以 paragraph ID 冒充一整段都已查核。 |
| narration_refs.start/end_utf16 | sidecar + `scenes[].lines[]` | 先重切v2，再建立文字與範圍的可逆映射；46舊片段失配、2需重新定位。 |
| chapter key／title | `{key,title,scenes,claims,loops}` | `readChapterAnswer` 將 title 裁30字；提示要求20字，採既有短章名。 |
| `illustrated_still` | `template:"shot"`；data.prompt / camera / visual:"still" | camera 取原 `Wide shot, pan right` 的 move `pan right`；鏡位保留在原 prompt。不改鏡位語義、不加新畫風。 |
| generic character | data.characters（已登記cast才填） | 場景仍只一名匿名人物做一個可見動作，非白石／博志實錄。角色不在cast不得虛構登記。 |
| 16 number_or_source_card | **可選 native `title`**：title=card.text，subtitle=card.scope，tag=card.source | `TEMPLATE_SPECS.title`及renderer明確讀這三欄；不使用未讀的 kicker/source。所有16組已做資料型態 probe，尚無像素QA。 |
| 9 post_source_overlay | 暫留 sidecar，明列待適配 | `readChapterAnswer` 不保留，shot renderer不會因這個原欄位自動顯示。必須保留「兩說分屬來源／博志回憶／1985製造與2021認定／另存板片／2023報導」等限制。 |
| image_asset_key | sidecar 的共用契約 | writer parser會捨棄任意額外鍵，不能據此聲稱圖片只買一次或已共用。後續需accepted file SHA、prompt/model/size/seed/negative/cast與實際鏡頭綁定。 |
| C-* 與 sources[]／facts[] | scene-level scalar `source`／`fact`；`claim`、`id`、`verdict` | 65清單只提出待查細項；不要把段落多來源／多fact任取第一個。每個新claim一個真scene，跨鏡可再拆成窄claim；全UNCHECKED。 |
| loops段落arrays | canonical `{setup:lineID,payoff:lineID,what}` + 全窗口sidecar | composer只保留setup→payoff順序有效的單一line；每setup只能一列。H02三問不可共用同一setup。 |
| N03最後三句／同圖三鏡 | 原方案保留，outro適配待明確化 | writer提示要求now最後有 `now-outro`、承載三句；舊方案是S101–103三張still，同一圖片另作camera。轉換不能默默捨棄原視覺或重念三句；技術方案待受審。 |
| intro5／outro21／末16連結 | 品牌動畫與結束畫面配置 | 不算正文，不塞進lines當停頓；目前是規格，非已完成媒體或連結。 |

### Card 的兼容性不能混為一談

`tools/video/automation/story.mjs:569` 的 `readChapterAnswer` 只收 shot／末章outro，遇 title 直接回 problem；這次以純記憶體 probe 實際確認。`composeStory`（約708行）則照章檔保留 template/data；`tools/video/templates/templates.mjs` 的 title 可以畫出 text、scope、source 三欄。因此不需先假定要開發新「數字卡」模板，但**普通 writer 通道不能接這些卡**。若後續 listener／lint修稿回到 writer reader，卡片仍有被拒收的風險；作者章採用方案須處理完整後續流程，不只證明一次 compose 可過。

`cuteStoryVisualProblems` 把 title/chapter/outro 當框架排除分母。因此使用title adapter時，必須另外以真內容鏡頭計算插畫比例與連續卡片，不能利用排除規則聲稱過關。原87/103約84.5%可作對照；v2完成後重新計數≥70%、卡片連續≤3、同camera不得連3鏡。來源代碼 S0/S2 是內部索引，畫面以原發布者名稱呈現；替換表保留原標籤以便逆查，不露內部failed-fetch註記。

## 來源與 claims 邊界

來源index保留原順序：0=J-Net21，1=日本機械學會，2=發明協會，3=Wikipedia（參考）。v2審稿中的 Ishino S3/S4 是**該審稿自己的代號**，絕非 worker source index3/4。T01a 可用現有index2的給茶原文；若實際pageReader拿不到段落，保持待取證，不能靠 plan.supports 或HTTP200導航頁假通過，也不擅加代理。

`fact:null` 是來源段落裡新增的可查細節，包含1947遷居、約三成、訂單超產能、博志回憶、1960二店、萬博位置／300日圓套組、1971/74給茶、競爭店型。它不是「不必查」。原 source-map 的 broad fact index 只是段落候選，不能把不在 must_verify 裡的細節塗成已驗。

20／50／300日圓各指不同時期與餐品；240家和約250家口徑不混；撲克牌與名片各自歸屬；1962是實用新案而非泛稱專利；1978只到期，不加商標開放；1985機器和另存早期板片分開；2023預估／報導店數有時點。上述限制要同時落入字稿、claims、數字卡及畫面。

## 可審的採用順序

1. 以本計畫為輸入，在新目錄完成v2六章、字卡／疊字／loops／line及scene映射。原稿、原board、原row和所有舊收據保持。
2. 使用固定的 worker code 與真lexicon做離線compose、lint、shot_reading、重建與視覺檢查；真錯誤保留，不塞null字典或寫假report。輸出一套可獨立審的章稿和新 hash。
3. 受審的runtime row要明確選擇與H02一致的hook候選；其他章point逐一比對v2的章界，特別是engine已不含完整曝光／240家回收、turn現在含萬博與給茶。現有point可作背景，不能讓再次writer把已審稿改回舊章界。若需改point，另作有限metadata候選及來源審查；本次不改它。
4. 審閱**作者章稿採用路徑**。`draftStory` 寫series/brief與空章狀態；`advanceStory` 遇章未written或檔案缺失會writer。單純匯入row、把Markdown放文件夾，甚至只拷貝六JSON都不能保證採用既有字稿。需要專門且受審的、精確來源雜湊綁定方案，處理STOP／lease／hold／來源漂移／現存媒體與run receipts／重複套用／備份與回復，不從本地偽造auto或章完成旗標。
5. 經當前授權／成本範圍核對後，才啟動真checker／listener／narrative。B18仍由 `PILOT_SCRIPT_REFERENCES` 綁原frozen script；獨立讀者比較實際六章＋五份canonical文件＋真narrative收據，明確審v2適配與frozen對齊後才有資格另簽script-review。
6. 媒體與發布依既有關卡；這份計畫不設定重試上限、不清counter、不產生PASS、不碰正式狀態。

本目錄的下一步是第1項免費離線轉換，並非現在執行第4–6項。
