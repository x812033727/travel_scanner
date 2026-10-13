# 影片產線：每支影片的語言與上架（設計）

2026-09-27 起草。前提是 [`DESIGN.md`](DESIGN.md) 的四語 CC、[`DUBS.md`](DUBS.md) 的配音音軌（怎麼塞回時間軸、Studio 怎麼上傳）、[`HANDS-OFF.md`](HANDS-OFF.md) 的「可以上架」與 YouTube API 兩步，以及票 `2026-09-24-video-youtube-sync`（T8）。這份寫：一支影片的「語言」是什麼、站主在哪裡選、工人怎麼只做選了的、上架怎麼等語言做好。教學與漫劇都適用；有角色說話的漫劇的配音是第二期，分類是觀念解說（`explainer`）、只有旁白說話的漫劇可以配音（[`DUBS.md`](DUBS.md) §已知限制）。票的 id 是 `2026-09-27-video-languages-*`，加上改寫的 `2026-09-26-video-dubs-worker` 與 T8。

## 一句話

每支影片先只做繁體中文。成片核准之後，站主在影片頁決定要不要加語言、加哪幾種、每種加什麼（標題與說明、CC、配音）。決定了、做好了，才排上架；上架之後還可以再加。

## 站主的要求（2026-09-27）

| 站主說的 | 這份怎麼做 |
| --- | --- |
| 目前教學應該要有多種語言的方式 | 一支影片可以掛三種語言（en、ja、ko；zh-CN 在 2026-10-09 拿掉，見文末「歷史」），每種語言有三個部件：標題與說明、CC、配音 |
| 製作好繁體中文版後，再讓我決定要不要製作哪些多國語言 | 語言面板在成片核准後出現；預設什麼都不勾；設定分頁的「語言預設」只是預先勾選 |
| 決定後再發布 | 「可以上架」要等語言決定了、選了的部件都做好或有跳過的原因，才排上架時間 |
| 多國語言指的是不同語言的標題跟 CC 還有語音等 | 三個部件各自可選；縮圖 YouTube 不能分語言，所以沒有這一項 |

配音「每支影片選、不是全域設定」是 2026-09-27 早先的決定（`DUBS.md` §每支影片的選擇），這份把它擴成三個部件。

## 現況

- `caption_locales` 是全域設定，每支影片自動出五語 CC 與五語標題說明（`package` 的 `description.<語系>.txt`），沒得選。
- 配音每支勾（`video_projects.dub_locales`、`DubLanguages`），但只管配音。
- 「可以上架」在上傳包核准後就出現，跟語言沒有先後：五語 CC 已經在包裡，配音是事後的另一張卡。
- YouTube 端：標題說明（`localizations`）與 CC 由 T8 用 API 補；配音只能在 Studio「語言」頁手動上傳（沒有 API）；縮圖沒有分語言的功能。

## 一支影片的語言

| 部件 | 做什麼 | 誰上 YouTube |
| --- | --- | --- |
| 標題與說明（`metadata`） | 翻標題、說明本文、標籤、章節名；`i18n-sheet` 本來就有這些欄位 | T8 的 `videos.update` `localizations`；T8 沒好之前站主在 Studio 手填 |
| CC（`captions`） | 翻每一句；有配音時字幕跟配音的時間軸（`DUBS.md`） | T8 的 `captions.insert`；T8 沒好之前站主上傳 `.srt` |
| 配音（`dub`） | 同一個頻道聲音唸翻譯（`DUBS.md` 全套：視窗、加速、縮短、Jev） | 只能站主在 Studio「語言」頁上傳 |

依賴：配音要先有 CC 的翻譯；勾了配音會自動連 CC 一起做（面板上會勾起來且不能取消）。標題與說明可以單獨勾。漫劇的配音只開給分類是觀念解說（`explainer`）的漫劇，它只有旁白一個聲音；其他漫劇的配音是第二期（多角色要每個角色一個外語聲音，`DUBS.md` §已知限制），面板上灰掉。2026-10-01 起新漫劇對白全為可開關 CC，正片不燒字幕；這次十部先完成 zh-TW，再製作 ja／ko／en 配音與各自 CC，[製作規格](series-plans/production-20261001/profile.json) 的多角色多語狀態仍為待實作。

### 資料模型

| 在哪裡 | 內容 |
| --- | --- |
| `video_projects.locales` | JSON，`{"en": {"metadata": true, "captions": true, "dub": false}, "ja": {…}}`，只列有勾的語言；預設 `{}` |
| `video_projects.locales_decided_at` | 站主第一次儲存語言面板的時間（含「只出繁體中文」）；`null` 就是還沒決定 |
| `video_projects.dub_locales` | 不再讀寫；遷移把它搬進 `locales`（三個部件都 true），欄位留著不刪（同 `subscription_max_usage_percent` 的做法） |
| 遷移 | 已在 YouTube 上的、或 `dub_locales` 非空的影片，`locales_decided_at` 設成遷移時間；其餘留 `null`，站主要決定一次 |
| `PUT /admin/videos/{slug}/languages` | `{"locales": {…}}`；只收 en、ja、ko；勾 dub 就強制 captions；分類不是觀念解說（`explainer`）的漫劇拒收 dub（422 `video_locales_dub_not_for_drama`）；寫 `locales_decided_at`（第一次）與 audit `video_locales_set`；已放棄的影片拒絕。取代 `PUT …/dubs` |
| `ProjectSummary`／`ProjectOut` | 帶 `locales`、`locales_decided_at`、`languages`（每個語言每個部件 `ready`｜`working`｜`skipped: <原因>`｜`uploaded`，伺服器從還算數的 `languages` 審核算出：等站主的與已核准的，舊到新，後面的批次蓋過前面的；被退回、被取代的不算）；工人從既有的影片清單就看得到。2026-10-10 起多兩欄 `dub_retries`、`dub_retry_blocked`（下面「跳過的配音再做一次」） |
| 審核 gate `languages` | 取代 `dubs`（`Gate` 留著 `dubs` 讓舊列讀得出來，CHECK 加 `languages`）。payload `{ locales: { en: { metadata: "ready", captions: "ready", dub: "ready" }, ja: { …, dub: "skipped", reason } } }`，檔案：說明欄 `.txt`、字幕 `.srt`、音軌（role `dub_<locale>`，m4a、mp3 或 wav，照配音做出來的格式），加上當下的 `metadata.json`（role `metadata`）與綁定核准來源的語言清單（role `languages_manifest`，雜湊就是審核的 content hash；YouTube 同步只收有這兩份的批次，見 [`APPROVED-LANGUAGE-PACKAGE.md`](APPROVED-LANGUAGE-PACKAGE.md)）。配音做好的語言，那一格旁邊還可能有 `kept_lines`（句子 id 的陣列：重錄塞不進視窗、沿用原本那次錄音的句子，`DUBS.md` 的 `--keep-fitting`）。**沒有配音的批次伺服器直接核准**（沒有站主要做的事）；有配音的等站主在 Studio 上傳後按「已上傳」 |
| `video_projects.dub_retries` | JSON（不是 jsonb），預設 `{}`，migration 0131。每個語言一筆，只留最新的那次「再做一次」要求與它怎麼結束，見下面「跳過的配音再做一次」 |
| 設定分頁 | `caption_locales` 與 `drama_caption_locales`（[`DRAMA-FLOW.md`](DRAMA-FLOW.md)）改成「語言面板預先勾選」：只影響面板打開時勾了什麼，不會自己做任何語言 |

### 後台：語言面板

在影片頁「進度」下面、審核卡片上面，取代 `DubLanguages`，成片核准後才出現（之前顯示一行「成片核准後可以選語言」）：

| 語言 | 標題與說明 | CC | 配音 |
| --- | --- | --- | --- |
| 英文 | ☐ | ☐ | ☐ |
| 日文 | ☐ | ☐ | ☐ |
| 韓文 | ☐ | ☐ | ☐ |

三顆鈕：「照預設勾選」（設定分頁的預先勾選）、「只出繁體中文」（存空的 `locales`，寫 `locales_decided_at`）、「儲存」。每一格旁邊顯示狀態：製作中、已完成、跳過（原因）、已上傳（配音）。上架後面板還在，多勾就再做一批；取消勾選只對還沒送上 YouTube 的部件有效，已經送上去的要站主自己在 Studio 刪，面板會這樣寫。配音那一格顯示「跳過」時，下面多一顆「再做一次」與這個要求走到哪裡的說明（下面「跳過的配音再做一次」）。

`languages` 的審核卡片列每個語言三個部件的狀態、下載連結（說明欄、字幕、音軌）、Studio「語言」頁的步驟（`DUBS.md` §站主要做的事）；有配音時一顆「我已經在 Studio 傳好這些配音」結案；卡片先寫明網站沒辦法替站主上傳音軌（YouTube 沒有這個 API），這顆鈕只記下站主說傳好了，面板那格顯示「你說已上傳」。音軌裡有沿用原本錄音的句子時（批次的 `kept_lines`），下載連結後面多一行：幾句、哪幾個句子 id，用的是 Jev 聽起來和稿子不一樣的那一版，因為重錄塞不進時間；批次只帶 id，頁面對不到是哪一句、第幾秒，所以那一行請站主上傳前把整條音軌聽一遍。

**站主確認過的音軌不會變回「已完成」。** 每一批都把勾了的語言全部重列一次，所以後來的批次（多勾一個語言、再做一次）會把別的語言已經上傳的音軌再寫成 `ready`。伺服器記下每個語言在已核准批次裡的音軌 SHA-256：等站主的批次裡同一個語言的音軌是同一個檔（同一個 SHA-256），那一格照舊讀成 `uploaded`、顯示「你說已上傳」；檔案不一樣才是「已完成」，也就是新的、要再上傳的那一條。卡片本身還是把每條音軌都列出來，哪一條是新的要看面板。這一批要不要等站主的規則沒有變：裡面只要有一條 `ready` 的配音就等站主按鈕。

### 跳過的配音再做一次（2026-10-10）

工人放棄的配音在面板上是「跳過（原因）」。在這之前沒有路可以再試：選擇沒變，儲存什麼都不寫；取消再勾，舊批次仍然說它跳過，工人也不會再碰。現在那一格有「再做一次」。這一節是網站這一側（存什麼、端點、那一格顯示什麼）；工人檢查什麼、清掉什麼、要花什麼在 [`DUBS.md`](DUBS.md) §再做一次。

**存什麼。** `video_projects.dub_retries` 每個語言（en、ja、ko）一筆，只留最新的一次要求：

```json
{"ja": {"id": "0d3b7c1e-6f0a-4c59-9d57-0d6a3f1c2b11",
        "status": "requested",
        "requested_at": "2026-10-10T12:40:03.118203+00:00",
        "requested_by": "<user uuid>",
        "replaced_reason": "k7p2 does not fit its window even at 1.15x after 2 shortening rounds",
        "estimated_characters": 6120,
        "taken_at": null, "finished_at": null, "reason": null}}
```

| `status` | 意思 | 配音那一格讀成 | 怎麼離開 |
| --- | --- | --- | --- |
| `requested` | 站主按了，等工人下一輪。什麼都還沒動：跳過還在、沒花錢 | `skipped`（照舊） | 工人接手或拒絕；滿 24 小時沒人接就讀成 `expired` |
| `expired` | 不存。讀的時候 `requested` 超過 24 小時就是它；資料庫裡仍是 `requested` | `skipped` | 再按一次 |
| `taken` | 工人說要接、網站確認了。從這一刻起工人才清掉跳過、開始花錢 | `working`（頁面寫「尚未完成」） | 只有答案能結束它：一筆語言批次，或工人的拒絕。沒有計時 |
| `made` | 帶著這條音軌的批次進來了，而且那一批算數（等站主或已核准） | `ready`，站主按鈕後 `uploaded` | 結束 |
| `skipped` | 再做了一次還是做不出來，批次帶著這一次的原因 | `skipped` | 結束，可以再按 |
| `refused` | 沒有做出新的音軌：工人拒絕並附原因，或重做出來的批次和先前被退回的那一批一模一樣（原因是網站寫的固定句子） | `skipped` | 結束，可以再按 |

`ProjectSummary` 與 `ProjectOut` 的 `dub_retries[語言]` 是讀出來的樣子：`id`、`status`（含 `expired`）、`open`（`requested` 還沒過期，或 `taken`）、`stalled`（還開著，而且要求超過 30 分鐘沒人接，或接手超過 2 小時沒結果）、`requested_at`、`taken_at`、`finished_at`、`reason`、`replaced_reason`（按下去那時的跳過原因）。只有現在勾著配音、而且存著要求的語言才有這一筆。後台與工人讀的是同一份 JSON；工人只用 `id`、`status`、`open`。

**部件狀態只多一條規則。** 存著 `taken` 的語言，配音讀成 `working`，不管批次怎麼說。所以接手之後清理工作區會等（[`AUTOMATION.md`](AUTOMATION.md) §清理工作區），還沒上架的影片也會離開「可以上架」，直到結果進來。`requested` 不改任何狀態：舊版工人看不到要求時什麼都不會發生，要求滿 24 小時自己結束。

**端點。** `POST /api/v1/admin/videos/{slug}/languages/{locale}/dub/retry`（瀏覽器經 `/api/travel/admin/videos/…`），沒有 body，`locale` 只收 en、ja、ko（其他是 422），權限 `content.manage`，成功回 200 與 `ProjectOut`。它只記一筆要求、讀一次語音用量，不做任何事。依序檢查，第一個不過的就回：

| 順序 | 情況 | 回應 |
| --- | --- | --- |
| 1 | 沒有這支影片 | 404 `video_project_not_found` |
| 2 | 影片已放棄 | 409 `video_project_dropped` |
| 3 | 這個語言已經有一筆開著的要求 | 200，原樣回傳：不多記 audit、不再檢查額度（路由每次都會先讀一次用量，這裡只是不拿它來判斷；兩個人各按一次也只有一筆） |
| 4 | 配音沒勾、不是「跳過」，或影片是 Short（觀念解說以外的漫劇勾不了配音，也就沒有跳過的配音可以再做） | 409 `video_dub_retry_not_skipped`「只有跳過的配音可以再做一次」 |
| 5 | 跳過的原因是「這是影片原本旁白的語言」 | 409 `video_dub_retry_narration` |
| 6 | 工作檔已經清掉（`auto.json` 有 `tidied_at`，或跳過原因以「工作檔已在 」開頭） | 409 `video_dub_retry_tidied`，訊息帶清掉的日期 |
| 7 | 網站上最新的上架確認（`publish` 審核）帶不了語言批次：被退回或被取代、根本沒有，或還在等而且之前沒有任何一張核准過、影片也還沒上 YouTube | 409 `video_dub_retry_publish_pending` |
| 8 | 影片不在工人的工作區，或工人那邊已放棄 | 409 `video_dub_retry_worker_absent` |
| 9 | 影片卡住 | 409 `video_dub_retry_video_blocked`（先按「重試這支影片」） |
| 10 | 工人被 `STOP` 檔停住 | 409 `video_dub_retry_worker_stopped` |
| 11 | 自動產線（`enabled`）關著 | 409 `video_automation_disabled` |
| 12 | 網站沒有 Gemini 金鑰 | 503 `video_speech_not_configured` |
| 13 | 有月額度，但讀不到本月用量 | 503 `video_speech_meter_unavailable`（寧可不收，跟用量表壞掉時不放行同一個方向） |
| 14 | 有月額度，本月已用加這一條的估計超過額度 | 429 `video_speech_budget_exhausted`，訊息帶額度、剩餘與估計字數 |

第 5 到 10 項是同一個判斷（`dub_retry.blocker`），頁面在按之前就看得到：`ProjectOut.dub_retry_blocked[語言]` 給代碼（`narration`、`tidied`、`publish_pending`、`not_adopted`、`blocked`、`stopped`），那一格顯示原因、不顯示按鈕。清掉工作檔的影片因此在三個地方得到同一個答案：那一格說明為什麼不能、端點回 409、漏進來的要求工人照樣拒絕而且不送批次。第 7 項擋的是做了也送不出去的情形：`review-push` 只把語言批次綁在網站上最新、而且是核准或等待中的上架確認上；最新那一張被退回或根本沒有（站主手動貼網址的影片可以沒有）時，付了錢的音軌進不了語言包。

第 14 項的估計：這個語言最新一批（等站主或已核准）的字幕檔 `captions_<語言>` 裡，去掉空行、序號行與時間行之後的字數；讀不到檔案就用 10,000。跟 `video_speech_gemini_monthly_character_limit` 與本月 Gemini 語音用量比；額度是 0 表示不設限，跳過第 13、14 項。這是讀一次、不是保留額度：`dub` 開工前自己再查一次，每一個合成請求再各自保留。按下去之後才超過額度時，工人那邊是「延後」，不是卡住也不是放棄（`AUTOMATION.md` §語言）。

寫入：`dub_retries[語言]` 換成新的一筆，`updated_at` 與 `last_synced_at` 一起往前（工人的清單是照 `last_synced_at` 取最新 200 支），audit `video_dub_retry_requested`（`request_id`、`replaced_reason`、估計字數、當時的用量與額度、前一筆要求的 `id` 與讀出來的狀態）。

**誰結束一筆要求。** 每一種結局只有一個寫入的地方：

- 工人的回報（`PUT /api/v1/video/reviews/{slug}` 的 `dub_retries`：`{"ja": {"id", "status": "taken"}}` 或 `{"id", "status": "refused", "reason"}`）只帶「接手」與「拒絕」。`taken` 只對 `id` 相同、還沒過期的 `requested` 有效（audit `video_dub_retry_taken`）；`refused` 結束 `requested` 或 `taken`（audit `video_dub_retry_finished`，`via: "report"`）；已經結束的不會再被改。看不懂的內容直接忽略，不回 422。回應是整支影片，工人從同一個回應讀到自己這一句有沒有被採用。
- 語言批次（`POST …/reviews`，gate `languages`）結束 `made` 與 `skipped`，跟批次存進去是同一筆交易（audit `via: "batch"`）。批次和舊的一模一樣、網站沒有新增審核時也照樣結束。批次說這條配音 `ready`，但網站回的是一筆被退回或被取代的舊審核（位元組完全一樣，所以沒有新的卡片）：`taken` 的要求以 `refused` 結束，原因是固定的一句「重做出來的音軌和先前那一批語言審核一模一樣…」，不會說成 `made`。

**取消勾選。** 儲存語言選擇時把配音取消：還在等的要求（`requested`，過期的也算）跟著刪掉，audit `video_locales_set` 多記 `dub_retries_withdrawn`；已經 `taken` 的留著但藏起來、暫停，勾回去就接著做。這只是程式實際的行為，不是撤回的方法，頁面上也沒有任何一句這樣建議：影片上架之後語言選擇一變，已核准的那一批就對不上選擇，YouTube 同步會拒絕這支影片（「語言選擇已變更」），直到配音勾回去。等著的要求不用管它，滿 24 小時自己取消，沒有花錢。

**那一格顯示什麼。** 都接在配音那一格原本的狀態下面，從重新讀到的影片資料算出來，沒有本機狀態：

| 情況 | 顯示 |
| --- | --- |
| 跳過，沒有要求或上一筆已結束，沒被擋 | 跳過（原因）、上一筆的結局（有的話）、「再做一次」與費用說明（只有 `content.manage` 看得到按鈕） |
| 跳過，被擋（`dub_retry_blocked`） | 跳過（原因）與為什麼現在不能做，沒有按鈕 |
| 按了但被端點拒絕 | 紅字「沒有送出：」加端點的句子，按鈕還在 |
| `requested` | 已要求、等工人下一輪、還沒開始；超過 30 分鐘改說工人可能正忙或沒在跑，滿 24 小時會自動取消、不花錢 |
| `expired` | 24 小時內沒有工人接手，已自動取消；按鈕回來 |
| `taken` | 尚未完成，下面一行「工人已接手再做一次（…）」說這條正在重做，再一行是原本跳過的原因；超過 2 小時改說原因看影片上方的等待或卡住說明 |
| `made` | 已完成，並請站主到下面的語言審核卡下載這一條、上傳後按卡片的按鈕；卡片會把其他語言的音軌再列一次：面板上寫「你說已上傳」的不用重傳，其餘的還沒確認過（要求是在上一張語言審核卡還等著的時候按的，新批次取代了它），要和這一條一起上傳 |
| `made`，但那張卡被退回，而且還有一批已核准的語言審核寫著這條配音跳過 | 又是先前跳過的原因，加一句：那一批被退回了，再做一次會沿用同樣的錄音，翻譯或規則沒變就還是同一條、也不會有新卡片 |
| `made`，但那張卡被退回，而且之前沒有還算數的語言審核（要求是在上一張語言審核卡還等著的時候按的，新批次把它取代了） | 尚未完成（這支影片每個語言的每一格都是，因為沒有算數的批次），加一句：那一批被退回了、之前也沒有還算數的語言審核，這一格暫時不能再要求；翻譯或規則沒變之前工人送出的還是被退回的那一批，不會有新卡片。沒有按鈕，端點這時回 409 `video_dub_retry_not_skipped`。被退回的最新一批語言審核怎麼收拾，不在這個功能的範圍 |
| `skipped`（又做不出來） | 跳過（這一次的原因）；下面有等站主的語言審核卡時，另外說明那張卡沒有這個語言的新音軌、但要按它的按鈕網站才會再把語言送到 YouTube |
| `refused` | 那一次要求沒有做出新的音軌，加原因；按鈕回來（除非被擋） |

按鈕按下去先跳確認框，寫明會花什麼、做得出來與做不出來各會看到什麼。

**七天的期限，照實際的規則。** 影片上架滿 7 天（`VIDEO_TIDY_DAYS`）之後，工作檔只在還有東西需要它們時留著：等站主決定的審核、製作中的部件，或一筆還開著的再做一次要求。所以站主一按下語言審核卡的按鈕，下一輪清理就可能把成片、旁白與配音的錄音清掉，之後這支影片的配音不能再做。還想再做的其他語言，要在按卡片的按鈕之前先要求；費用說明與 `made` 的那一句都這樣寫。

**沒做的。** 清掉工作檔之後補做配音、撤回按鈕、把跳過放回去、只重列已確認音軌的批次自動核准、換掉 YouTube 上已有的字幕（再做一次會照新配音重切這個語言的字幕，但網站不會替換已經在 YouTube 上的那一份）。

## 上架流程：一張卡、五個狀態

| 狀態 | 條件 | 站主看到 |
| --- | --- | --- |
| 等你決定語言 | 成片核准，`locales_decided_at` 是 `null` | 語言面板與「只出繁體中文」；影片在「需要你」 |
| 語言製作中 | 已決定，還有勾了的部件不是 ready／skipped／uploaded | 每格的狀態；影片在「進行中」 |
| 可以上架 | 上傳包核准（檢查含選了的語言），每個勾了的部件都 ready／skipped／uploaded | 上傳包下載、貼網址、上架時間、配音的 Studio 步驟；影片在「可以上架」 |
| 已排定 | 有 `youtube_video_id` 與 `youtube_publish_at`，T8 已送出 | 送出結果（哪些語系的 `localizations`、字幕、縮圖成功） |
| 已上架 | 過了 `publish_at` | 語言面板仍可多勾；配音的卡片照舊 |

`readyToUpload(project)` 從「上傳包核准且沒有影片 id」改成再加「語言已決定且都做好」。伺服器算，`ProjectSummary` 帶 `ready_to_upload`，頁面不再自己推。

**站主什麼時候能上傳 mp4**：成片核准之後隨時可以在 Studio 上傳成私人、貼網址、選時間，不用等語言。T8 把 `publishAt` 送出去的條件才是「語言都做好」：語言還在做時卡片寫「排程會在語言做好後送出」，做好的那一輪工人回報、伺服器送出。這樣「決定後再發布」成立，站主的上傳也不用等。上架後再勾的語言，T8 只補新的 `localizations` 與字幕（先 `captions.list` 看已經有哪些）；配音照舊手動。

## 工人

成片核准且 `locales_decided_at` 不是 `null` 時，對每個勾了的語言（一輪做一個語言，跟現在的翻譯一樣）：

1. `i18n-sheet --slug <slug> --locale <l> --parts metadata,captions`（只出勾了的部件；勾配音時 `max_chars` 照 `DUBS.md`）→ 翻譯模型 → 字幕審稿模型 → `i18n-merge`。
2. 勾配音：`dub --locale <l>` → 塞不下的句子交翻譯模型縮短（最多 2 輪）→ `check-audio --locale <l>` → Jev 標記 → `dub --redo`（最多 2 輪）→ 仍不行寫 `dubs/<l>/skipped.json`，不擋。這個檔留著的期間工人不會再碰這個語言的配音；站主從面板要求再做一次、網站確認工人接手之後，工人才清掉它重做（上面「跳過的配音再做一次」）。
3. 全部語言做完：`captions`（只寫 zh-TW 與勾了 CC 的語系；有配音的跟配音時間軸）→ `package`（`upload/` 只放 zh-TW 與勾了的：`description.<l>.txt`、`captions/<l>.srt`、`dubs/<l>.m4a`；`metadata.json` 的 `locales` 照決定）→ `review-push --gate languages`。
4. `qa` 的 `captions` 與 `metadata` 項、`package` 的 `captions` 與 `descriptions` 項都改成「zh-TW 加勾了的」；跳過的算過、列成警告。

旁白不是 zh-TW 的影片（`narration_locale`，例如 `en`）：面板不會列 zh-TW，但 `captions`、`package`、`qa` 永遠要它（`alwaysLocales`），所以語言一決定，工人先把 zh-TW 的標題說明與 CC 翻一次（不配音），再做勾了的；什麼都沒勾時只把 `captions` 與 `package` 重寫一次，不送語言批次。成片審核卡也永遠帶旁白語言與 zh-TW 的標題說明。

沒勾語言、或按了「只出繁體中文」的影片：`captions` 只寫 zh-TW，`package` 只有 zh-TW，跟現在比少了三個語系的檔案，其餘一個位元組都不變。`caption_locales` 不再驅動任何工作。

之後多勾的：工人看到 `locales` 裡有 ready／skipped 都沒有的部件就再做一批，送新的 `languages` 審核。新批次只取代（superseded）還在等站主的舊批次；已核准的舊批次照舊是核准的，檔案也留著。每一批都把勾了的語言全部重列一次，站主確認過、檔案沒變的音軌在面板上仍然是「你說已上傳」（上面「站主確認過的音軌不會變回已完成」）。

## 成本

- 翻譯：每個語言一次翻譯加一次審稿呼叫（現在三語都做，之後只做勾的，只會少不會多）。
- 配音：`DUBS.md` §成本（一條 10 分鐘約 US$0.135；三條約 US$0.41；月額度要先調高）。
- 再做一次：最多一整條音軌的合成，加上逐句聽寫與 Jev 的檢查；錄音還在快取裡的句子不重新合成（`DUBS.md` §再做一次）。端點在收下要求之前先比本月的語音額度。
- YouTube 配額：T8 一支約 2,100 單位，語系少配額也少（`captions.insert` 一個語系 400）。

## 與其他票的關係

- `2026-09-26-video-dubs-worker`（未認領）：改寫成這裡的工人票（配音是三個部件之一，同一條流程），id 不變。
- `2026-09-24-video-youtube-sync`（T8）：`localizations` 與字幕只送勾了的語系；`publishAt` 等 `ready_to_upload`；上架後再勾的語系走同一支程式補送。
- `2026-09-26-video-dubs-setting`（已完成）：`DubLanguages` 與 `PUT …/dubs` 被語言面板取代；`DubsBody` 併進 `languages` 卡片。
- [`DUBS.md`](DUBS.md)：配音怎麼做（時間軸、縮短、Studio 步驟、限制）仍以它為準；「每支影片的選擇」一節由這份接手。
- [`README.md`](README.md) 的「字幕」「配音音軌」兩列與 skill 的 `publish.md`、`automated.md` 第 9、13 步照這份改（票 `video-languages-skill-docs`）。

## 票

| 票 | 內容 | scope | 依賴 |
| --- | --- | --- | --- |
| `video-languages-api` | `locales`、`locales_decided_at`、遷移（含 `dub_locales` 搬家）、`PUT …/languages`、gate `languages`、`languages` 與 `ready_to_upload` 的計算、`ProjectSummary` | `apps/api/app/models.py`、遷移、`apps/api/app/video_reviews`、測試 | — |
| `video-languages-web` | 語言面板（三部件、預設、只出繁中）、`languages` 卡片、上架卡的五個狀態、拿掉 `DubLanguages`／`DubsBody` | `admin-video-reviews.tsx`、`admin-video-review-card.tsx`、測試、`admin.json` | api |
| `video-dubs-worker`（改寫） | 工人只做勾了的部件：`i18n-sheet --parts`、翻譯、配音、`captions`、`package`、`review-push --gate languages`、`qa` 與上傳包檢查縮到選了的語系、測試 | `tools/video/automation`、`tools/video/i18n`、`tools/video/core/stages.mjs`、`tools/video/qa`、`tools/video/package`、`tools/video/review`、`docs/videos/AUTOMATION.md`、翻譯提示 | api |
| `video-youtube-sync`（T8，改寫） | 只送勾了的語系；`publishAt` 等語言做好；上架後補送新語系 | 不變 | web |
| `video-languages-skill-docs` | `publish.md`、`automated.md`、`drama.md`、`README.md` 的字幕與配音列、`DUBS.md` 指到這份 | `.agents/skills/youtube-video/references`、`docs/videos/README.md`、`docs/videos/DUBS.md` | dubs-worker |

順序：api → web 與 dubs-worker 平行 → T8 → skill-docs。api 落地後第二批三支（成片已核准、`locales_decided_at` 為 `null`）會出現在「需要你」等語言決定，這是預期的。

## 歷史

- 2026-10-09：站主把 zh-CN 從影片的語言拿掉（「預計四語就好」）：一支影片是 zh-TW 旁白，可加 en、ja、ko 三種語言的標題說明、CC 與配音。已經在 YouTube 上掛了 zh-CN 標題或字幕的影片照舊留著，站只會加、不會刪。網站本身仍是五個語系（文章、介面、`apps/api/app/i18n.py`），影片的語言表不再跟它（`tools/video/core/schema.mjs` 的 `LOCALES`）。
