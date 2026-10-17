# B18 v2：六章作者候選（僅離線）

日期：2026-10-16。作者：`codex-a01-repair-editor`。**六章原生資料形狀與本機合稿已完成；尚未獨立審查、匯入或完成任何 worker 關卡。** 沒有付費、主機、模型或媒體 API 呼叫。本目錄不授權下一階段執行。

## 已完成

- v2 24段、2294編輯units逐字保留，標點、順序與段落都可從99個native line完整重建。原文SHA：candidate.md `bdade1f5c207517d0a57edb18f372905a40c67ec8193aecdfa10e2f2847bdc9b`；paragraphs.json `a27492b74b84f4bd1e10ce9eeb83ef53a58e38fbb8544b58357034533877525a`。
- 真六章在 [chapters/](chapters/)，96鏡：77插畫、19原生title卡。實際內容鏡頭插畫比例80.21%，連續卡片最多2張；沒有利用title模板被cute lint排除分母來假稱達標。
- 65個scene-level主張全部 **UNCHECKED**。每項原文quote完整落在所綁scene，沒有跨鏡主張。source索引保留原0/1/2；沒有把Ishino誤作worker source3。
- `i2`／`i8`把規劃清單的寬泛fact3收窄成 `fact:null`：附近工廠協作、試作機專名不全在must_verify原句中，必須讀來源段落。原must_verify與來源順序完全不改；兩項metadata差異在mapping明列。
- 11個有效line-ID loops；H02三問各有不同setup，保留完整payoff段落及line窗口。三組預告／回收仍有完全相同prompt、camera、圖片鍵，但沒有任何實際圖片檔。
- 16原卡全部保留其數字／文字與scope。9個來源疊字使用支援的title欄位呈現，沒有把文字加進AI插畫prompt。
- 原生 `composeStory`、`advanceStory` 的**純本機relint**、完整 `lintProject`、cute檢查確實執行：**0 errors**；保存的真lexicon未改。`shot_reading`：77鏡、0 traps。這些是格式／工具結果，不是事實、敘事或成片PASS。
- 原稿、原103鏡、worker rows、編譯stories、所有原收據與實作檔保持；43個input SHA前後一致。

## 對103鏡的精確適配

8鏡退出當前候選：`S013/S017/S036/S064/S067/S069/S074/S082`；原完整物件仍在mapping的retired_original_shots，沒有刪除來源檔。v2已縮掉的旁枝不以空鏡或停頓補回。

3張原插畫位置變成來源卡：`idea-s032`（魚鱗板名稱）、`engine-s061`（博志暑假回憶）、`now-s095`（1985製造／2021認定及另存板片）。原prompt、camera、圖片鍵與理由全部保留。另將 `S101` 拆成 `now-s101`／`now-s101b`，保留同一圖片鍵；新增後製drift運鏡，不增任何旁白。

| 原疊字位置 | 現在實際顯示的native卡 | 呈現界線 |
| --- | --- | --- |
| S028／S029 | idea-s027 | J-Net21／發明協會各自記載；兩個示意插畫仍保留，旁白各自歸屬不改 |
| S032 | idea-s032 | 魚鱗板（ウロコ）與原三來源 |
| S035 | idea-s033 | 約十年試作與原日文試作機名，材料比較插畫仍在S035 |
| S037 | idea-s038 | 博志的回憶與推測，不當成工廠主證詞 |
| S061 | engine-s061 | 博志回憶的暑假幫忙 |
| S095／S096 | now-s095 | 製造年／認定時使用中／另存早期板片分清；S096仍畫分離板片 |
| S097 | now-s098 | 2023報導引述調查、2022實績與2023當時預估 |

來源S0/S1/S2改成發布者名稱，原標籤保存於mapping。19卡均以真正 `TEMPLATE_SPECS.title`／`slideHtml`確認欄位有效且文字存在於HTML；**尚未驗像素版面、手機可讀性或疊字移位的視覺節奏**。請獨立review這些顯示位置，不把HTML保字當成最終畫面驗收。

## 時長與真警告

官方`spokenUnits`為2285，與編輯2294的9字差額是官方regex不計「〇」，不是刪字。默認timeline估正文 **647.4秒（10:47.4）**，另加5＋21秒動畫約 **673.4秒（11:13.4）**。正文包含hook；包含工具預設的99條line間隔、95個鏡間隔與尾部時間，沒有手加pause、慢播或無聲scene。字數直接估550.56–598.43秒與此timeline的差異，不可拿來假稱TTS實測。

最大估鏡長10.23秒（字卡now-s095）；最大插畫鏡10.2秒（hook-s004）。實際合成時長與約10分鐘目標仍待確認，不能因本機lint無錯就稱已交付約10分鐘成片。

全部30條warning保留於 `compose-lint-evidence.json`：

- 3段open-loop偵測間隔110／144／110秒，以及「二〇二三年」出現3次。這些需要真實全文敘事審查；本次為逐字轉換，未增設問或改年份。
- 原prompt的generic／neutral／focal共詞；末三句沿用同圖、因S101拆鏡成四個位置，被判三次近似畫面。這是原同圖收尾意圖，是否節奏成立仍待實看。
- hook-s004超10秒的提示；18條角色漫劇craft警告不適用於旁白品牌故事，不因此加角色對話或把卡片改成動畫劇。
- 12 tags 的發布包提示未處理；不改原worker row。

## 接手檔案

- [mapping.json](mapping.json)：完整paragraph→line→scene→CID→claim/source/fact、原視覺與改動、疊字位置、共圖、loops、退役鏡。
- [remaining-work.json](remaining-work.json)：哪些只待獨立review、哪些是worker採用阻擋、哪些是未開始的媒體工作。
- [compose-lint-evidence.json](compose-lint-evidence.json)：官方合稿／lint／cute、30真warning、估時、writer parser結果。
- [card-adapter-evidence.json](card-adapter-evidence.json)、[shot-reading-evidence.json](shot-reading-evidence.json)：真原生模板及鏡位讀法檢查。
- `synthetic/docroot/docs/videos/story-conveyor-belt-sushi-v2/`：官方合出的video.json、script.md、claims.md和series/brief；沒有verify-1、narrative或script-review。
- `synthetic/LOCAL-FIXTURE-NOT-PRODUCTION-STATE.json`：只為離線relint的fixture，**不得拿去當正式auto狀態或改written／counter的授權**。
- [input-pins.json](input-pins.json)、[output-pins.json](output-pins.json)、[handoff-pins.json](handoff-pins.json)：來源、初次建置輸出與最終交付雜湊。
- [verify-offline.mjs](verify-offline.mjs)、[verification.json](verification.json)：從當前repo重讀inputs、重建24段與官方lint的唯讀重跑。

```powershell
node docs/videos/brand-stories-pilot-v2-20261015/preproduction-20261016/B18-authored-chapters-candidate/verify-offline.mjs --repo .
```

`build-offline.mjs` 只允許新輸出目錄，重跑需提供 `--repo`、`--out` 與本包 `fixtures/lexicon.json`；不覆蓋本候選。voice與lexicon都是已保存fixture，未讀取主機目前設定。

**正式採用仍有明確阻擋：**普通writer parser會拒絕五章的title卡，也會捨棄自訂共圖鍵。原compiled hook point及其他章界尚未對齊本稿，作者章採用／後續listener路徑仍須另作受審方案；最後三句保留四個still位置，尚未解決writer要求now-outro與此同圖方案的適配。這份候選不能直接投入自動產線。真checker/listener/narrative、新pilot實稿review、付費授權及限額、TTS、圖片、成片與站主觀看仍待辦。
