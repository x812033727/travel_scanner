# B18 v2：離線 worker 章稿轉換計畫

日期：2026-10-16。作者：`codex-a01-repair-editor`。範圍是已審文字的轉換規劃，**尚未建立正式六章、匯入、執行 worker 或生成媒體**。本目錄不授權付費、正式環境寫入或發布。

## 現在可用的材料

- v2 `candidate.md`：`bdade1f5c207517d0a57edb18f372905a40c67ec8193aecdfa10e2f2847bdc9b`。
- v2 `paragraphs.json`：`a27492b74b84f4bd1e10ce9eeb83ef53a58e38fbb8544b58357034533877525a`。24 段、2294 units；v2 獨立文字複審已保存於相鄰目錄，資格只涵蓋文字。
- 原 103 鏡 storyboard：`6e0ea8861c0ad795aa7d4c523cfe751a134b9a71273b699b3bc6c5e922a101b9`，仍綁原 2729 units 稿，不能當成 v2 分鏡。原稿、v1 HOLD、103 鏡收據均保留。
- 已獨立審過的 hook row 候選在 `../B18-worker-hook-candidate/`；本次核對 `episodes/B18.json` 與 `stories.json` 仍是舊 hook point。新候選的 row review 不等於已套用、也不涵蓋新六章。

## 本次交付

| 檔案 | 用途 |
| --- | --- |
| [conversion-plan.json](conversion-plan.json) | 24 段全文逐字、章別、原鏡範圍、CID、來源界線；六章、16 卡、9 疊字、共用圖片及 loops 的轉換安排 |
| [paragraph-map.md](paragraph-map.md) | 人工閱讀的 24 段對照表 |
| [shot-impact.json](shot-impact.json) | 全 103 個原鏡與 UTF16 字段在 v2 的存留／重切狀態；保留原 prompt、camera、卡片與圖片鍵 |
| [claim-checklist.json](claim-checklist.json) | 65 個待查子主張：原文定位、單一 source／fact 候選、來源限制；全為 UNCHECKED，scene 尚未綁定 |
| [schema-and-adoption.md](schema-and-adoption.md) | 實際 worker parser／composer／renderer 的欄位差異與採用順序 |
| [source-pins.json](source-pins.json) | 30 個來源／規則／實作檔的 repo 相對路徑與 SHA256 |
| [verify.mjs](verify.mjs)、[verification.json](verification.json) | 可重跑的唯讀驗證與本次結果；不呼叫 writer、verifier、listener 或媒體服務 |

本次沒有重查官方網頁；來源支持依已保存的 v2 獨立複審與原 source-map 做**規劃索引**。這份清單的作者不能自行把它簽成正式事實審查。

## 精確影響範圍

相對原長稿，9 段改過：`O01/O02/O03/I04/E03/E05/T01/T01a/T03`；其餘 15 段逐字相同。103 個舊 narration refs 中，55 個在舊位置仍逐字相同，2 個可找到唯一的新位置，46 個文字已改／刪，須重新分配。**這不是承諾維持103鏡**；唯一可重定位也只是文字候選，聲畫銜接仍要檢查。

原分鏡為 87 張插畫位置、16 卡、9 個來源／限制疊字，82 個規劃圖片鍵。新版本須依真旁白重切，保留必要事實與範圍，不為保留鏡數增加停頓。圖片鍵只代表意圖，目前沒有可沿用的已驗收媒體檔。

## 正式離線章稿仍差什麼

1. **重切文字與鏡頭。** 對9段重排鏡頭與時間、逐字重建24段；新 line ID／scene ID 必須和原 paragraph、CID、來源及畫面有可逆映射。
2. **完成視覺欄位轉換。** 16卡的三個文字欄可用原生 `title` 資料結構保存，但一般 writer parser 拒絕此模板；9 個 `post_source_overlay` 不會由原生 `shot` 自動顯示。需明確且受審的 adapter，不能丟掉來源限制或把假字幕塞進 AI 圖。
3. **把65個子主張綁到真 scene。** 目前是查核清單，不是正式 claims。O03 訂單量／離職分別綁 S2／S0；I02 撲克牌／名片分開歸屬；超出 must_verify 的細節要可讀來源段落。新 rows 全部 UNCHECKED。
4. **確定 loops、片尾與圖片共用。** H02 三問使用三個 setup line ID；保留完整回答窗口。N03 的原三鏡同圖方案與 writer 要求的 `now-outro` 要有明確適配，不能重複或丟失最後三句。三組回呼的實際檔案同一性仍待媒體階段。
5. **確定採用入口與 runtime plan。** 普通 import 只匯入企劃，會重新撰稿；目前沒有從本目錄安全採用作者六章的正式入口。新 row／series、章稿採用器及其邊界須另作受審成果，這份計畫不寫 auto 狀態、不借用 A01 安裝器的授權。
6. **新稿的實際工具與獨立審查。** 轉完後才跑官方 compose、lint、cute、shot_reading、真 lexicon、卡片／疊字呈現檢查與獨立全文／來源覆核。舊103鏡的工具結果不能覆蓋新稿。

這六項是離線章稿工作的下一步，沒有要求先查帳戶餘額。真正開始 worker 查核及付費製作的授權、每片限額與執行機制由 root 既有工作處理；本目錄不能取代它們。

## 時長與後續驗收

2294 units、250–230 units/min 推算旁白 **550.56–598.43秒（9:11–9:58）**；包含 hook，另加5秒片頭及21秒片尾為 **576.56–624.43秒（9:37–10:24）**。這是字數估算；沒有本稿的 TTS、逐鏡≤12秒或成片實測。engine／turn 章的估長較長，實際聽稿再判，不以慢播、灌字或停頓補時。

正式執行後仍需真逐章查核／聽眾審稿／全片敘事、新 frozen-reference script-review、音訊及畫面 QA、可開關繁中 CC、5+21秒動畫與末16秒連結驗證、站主觀看。原 frozen `scripts/B18.md` 的 SHA 與舊審查不改。

重跑（從任意工作目錄，參數為 repository root）：

```powershell
node docs/videos/brand-stories-pilot-v2-20261015/preproduction-20261016/B18-worker-conversion-plan/verify.mjs --root .
```

驗證程式只讀取檔案並輸出 JSON；若來源 drift 會失敗，不自動改 pin 或重簽。
