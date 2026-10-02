# 借來的黎明｜動漫企劃包

誤入瑟曦亞的維修學徒，與巡行醫師、負罪軍人及守林者，一起追查文明轉嫁的休止債，建立能讓人活下去的退場方法。

本包依本次對話的原創企劃與兩輪補正整理，分類為 **`anime`（動漫）**，畫風預設為 **`anime-2d`（日式2D動畫）**。共 **10季、每季12集、全劇120集**，封閉結局。分類對應 [PR #1110](https://github.com/x812033727/travel_scanner/pull/1110)，這個獨立內容PR不重複其migration、API、UI或翻譯修改。

## 閱讀順序

1. [設定集](setting.md)：世界規則、四大勢力、人物、長線謎團與不可逆代價。
2. [十季總綱](outline.md)：由地方救援到世界退場的升級與真相曲線。
3. 分季細綱：每集兩段高張力、賭注、後果、埋梗回收與人物已知資訊。
4. [連貫性與伏筆帳](continuity.md)、[逐集狀態CSV](continuity.csv)。
5. [獨立覆核](review.md)：實際檢查範圍、修正與製作限度。

| 季 | 集數 | 細綱 |
| --- | --- | --- |
| 1 | 1–12 | [陌生爐火](season-01.md) |
| 2 | 13–24 | [潮路上的名字](season-02.md) |
| 3 | 25–36 | [灰隘關的誓言](season-03.md) |
| 4 | 37–48 | [救人的森林](season-04.md) |
| 5 | 49–60 | [四國燃冬](season-05.md) |
| 6 | 61–72 | [失錨者的長路](season-06.md) |
| 7 | 73–84 | [真正的冬天](season-07.md) |
| 8 | 85–96 | [黎明以前的人們](season-08.md) |
| 9 | 97–108 | [分擔黎明](season-09.md) |
| 10 | 109–120 | [借來的黎明](season-10.md) |

## 來源與格式

[plan.json](plan.json)保存分類、原定時長、影片預設與製作支援差異。[setting.json](setting.json)、`season-01.json`～`season-10.json`是細綱來源；[authoring-contract.json](authoring-contract.json)定義人物ID、伏筆ID與共同規則。

前36集依對話中已定事件復原為一致的結構大綱，未宣稱逐字保存未在本次工作區落地的舊稿。後84集直接整合後續規劃與補正。全包是設定、總綱與分集細綱，**尚不是120份22分鐘逐場台詞腳本**。

每集 `high_tension` 有前、後半兩項具體事件、受威脅的人與延續後果。`setups`／`payoffs`引用長線謎團；`general_payoffs`記錄已完成的局部任務或關係行動，避免為每四集的回報硬提早揭露古代真相。`state`分開時間、已知資訊、人物狀態、證據與後續接續。五段 `tension`是企劃評分，不是觀眾反應或實測時間。

## 已整合的補正

- 降載只減少新增負荷；具名載體真正停工、休耕或休養，才算償債。
- 解除強制調度與超授權轉債，保留必要散熱、回流與維生設施。
- 北錨災難有緩衝、回流、熱壓與結構毀損因果；沈澈不持政治主權鑰匙。
- 歸零令符合載體相容限制，人體療債不轉給森林；歸零的是外區配額。
- 奧倫與上司、國家各自負責；維爾、魯格與伊瑟爾案件分別收束。
- 第七季跨完整一年；兩小時危機採本地並行，主線約四年八個月。
- 返鄉是真正安全可選的路；沈澈先決定留下，窗口再自然到期。
- 原界訊息需探針、接應與回覆時間；沒有任意手機連線或時間倒流。
- 古代已有改革嘗試，第88集改為保管權衝突，降低反覆坍塌套路。
- 北錨不復原、死者不復活、傷殘保留，尾聲仍需數代還債，仍有人拒絕原諒。

## 製作支援差異

原定每集正文約22分鐘，播出時段約30分鐘。OP/ED預算約3分鐘，其餘時段留給播出包裝、預告或廣告配置；不靠停頓、重複旁白或拉慢剪輯湊正文。

目前 `SeriesIn` 普通漫劇只接受1–8分鐘，`anime`分類不會擴大此限制。現有 `custom`題材還要求每集兩個爽點；本劇的悲劇與群像節奏未假填這些欄位。工人篇章檢查另要求末段張力≥4，本劇第120集在兩段張力後安穩收束，末段保留2。

因此本包的 `ready_for_import` 為false，沒有可直接POST的 `series-request.json`；[documents.json](documents.json)僅提供 `body_md`／`body_json`文件形狀，不能冒充核准或排程。將來製作時，須先具備#1110分類、長篇時長與相符敘事政策，見[後續製作支援任務](../../../../tasks/open/2026-10-02-anime-long-episode-support.md)。不得改用`story`或`flat-explainer`繞過限制，也不將作品縮成三分鐘短漫劇。

將來每集 slug為`borrowed-dawn-e001`～`borrowed-dawn-e120`，其`video.json`與首次送審報告沿用`plan.json.video_defaults.category = anime`。後台作品的`kind`仍是`series`，影片`format`仍是`drama`，分類與格式各有用途。

## 本機重建與驗證

在repository根目錄執行；指令只讀寫這個企劃目錄，不呼叫模型、正式站、匯入API或媒體供應商：

```bash
node docs/videos/series-plans/borrowed-dawn/build.mjs
node docs/videos/series-plans/borrowed-dawn/build.mjs --check
node docs/videos/series-plans/borrowed-dawn/validate.mjs
node --test docs/videos/series-plans/borrowed-dawn/validate.test.mjs
npm run check:tasks
```

`build`從JSON來源產生設定集、總綱、分季Markdown、文件包、連貫CSV與SHA256 manifest。修改來源或覆核後重建；`--check`會在衍生檔與來源不符時失敗。`validate`檢查集數、引用、兩段張力資料、埋回排程、結局與原定規格；這不能證明22分鐘劇本完整、真人觀看張力、媒體品質或法律上的原創。

本次成果供獨立PR審閱，未建立後台作品、匯入、啟用工人、生成媒體、排程或發布。
