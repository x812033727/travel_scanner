# 影片產線：每支影片的語言與上架（設計）

2026-09-27 起草。前提是 [`DESIGN.md`](DESIGN.md) 的四語 CC、[`DUBS.md`](DUBS.md) 的配音音軌（怎麼塞回時間軸、Studio 怎麼上傳）、[`HANDS-OFF.md`](HANDS-OFF.md) 的「可以上架」與 YouTube API 兩步，以及票 `2026-09-24-video-youtube-sync`（T8）。這份寫：一支影片的「語言」是什麼、站主在哪裡選、工人怎麼只做選了的、上架怎麼等語言做好。教學與漫劇都適用；漫劇的配音是第二期。票的 id 是 `2026-09-27-video-languages-*`，加上改寫的 `2026-09-26-video-dubs-worker` 與 T8。

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

依賴：配音要先有 CC 的翻譯；勾了配音會自動連 CC 一起做（面板上會勾起來且不能取消）。標題與說明可以單獨勾。漫劇的配音是第二期（多角色要重新混音，`DUBS.md` §已知限制），面板上灰掉。2026-10-01 起新漫劇對白全為可開關 CC，正片不燒字幕；這次十部先完成 zh-TW，再製作 ja／ko／en 配音與各自 CC，[製作規格](series-plans/production-20261001/profile.json) 的多角色多語狀態仍為待實作。

### 資料模型

| 在哪裡 | 內容 |
| --- | --- |
| `video_projects.locales` | JSON，`{"en": {"metadata": true, "captions": true, "dub": false}, "ja": {…}}`，只列有勾的語言；預設 `{}` |
| `video_projects.locales_decided_at` | 站主第一次儲存語言面板的時間（含「只出繁體中文」）；`null` 就是還沒決定 |
| `video_projects.dub_locales` | 不再讀寫；遷移把它搬進 `locales`（三個部件都 true），欄位留著不刪（同 `subscription_max_usage_percent` 的做法） |
| 遷移 | 已在 YouTube 上的、或 `dub_locales` 非空的影片，`locales_decided_at` 設成遷移時間；其餘留 `null`，站主要決定一次 |
| `PUT /admin/videos/{slug}/languages` | `{"locales": {…}}`；只收 en、ja、ko；勾 dub 就強制 captions；漫劇拒收 dub；寫 `locales_decided_at`（第一次）與 audit `video_locales_set`；已放棄的影片拒絕。取代 `PUT …/dubs` |
| `ProjectSummary`／`ProjectOut` | 帶 `locales`、`locales_decided_at`、`languages`（每個語言每個部件 `ready`｜`working`｜`skipped: <原因>`｜`uploaded`，伺服器從最新的 `languages` 審核算出）；工人從既有的影片清單就看得到 |
| 審核 gate `languages` | 取代 `dubs`（`Gate` 留著 `dubs` 讓舊列讀得出來，CHECK 加 `languages`）。payload `{ locales: { en: { metadata: "ready", captions: "ready", dub: "ready" }, ja: { …, dub: "skipped", reason } } }`，檔案：說明欄 `.txt`、字幕 `.srt`、音軌（role `dub_<locale>`，m4a、mp3 或 wav，照配音做出來的格式），加上當下的 `metadata.json`（role `metadata`）與綁定核准來源的語言清單（role `languages_manifest`，雜湊就是審核的 content hash；YouTube 同步只收有這兩份的批次，見 [`APPROVED-LANGUAGE-PACKAGE.md`](APPROVED-LANGUAGE-PACKAGE.md)）。**沒有配音的批次伺服器直接核准**（沒有站主要做的事）；有配音的等站主在 Studio 上傳後按「已上傳」 |
| 設定分頁 | `caption_locales` 與 `drama_caption_locales`（[`DRAMA-FLOW.md`](DRAMA-FLOW.md)）改成「語言面板預先勾選」：只影響面板打開時勾了什麼，不會自己做任何語言 |

### 後台：語言面板

在影片頁「進度」下面、審核卡片上面，取代 `DubLanguages`，成片核准後才出現（之前顯示一行「成片核准後可以選語言」）：

| 語言 | 標題與說明 | CC | 配音 |
| --- | --- | --- | --- |
| 英文 | ☐ | ☐ | ☐ |
| 日文 | ☐ | ☐ | ☐ |
| 韓文 | ☐ | ☐ | ☐ |

三顆鈕：「照預設勾選」（設定分頁的預先勾選）、「只出繁體中文」（存空的 `locales`，寫 `locales_decided_at`）、「儲存」。每一格旁邊顯示狀態：製作中、已完成、跳過（原因）、已上傳（配音）。上架後面板還在，多勾就再做一批；取消勾選只對還沒送上 YouTube 的部件有效，已經送上去的要站主自己在 Studio 刪，面板會這樣寫。

`languages` 的審核卡片列每個語言三個部件的狀態、下載連結（說明欄、字幕、音軌）、Studio「語言」頁的步驟（`DUBS.md` §站主要做的事）；有配音時一顆「我已經在 Studio 傳好這些配音」結案；卡片先寫明網站沒辦法替站主上傳音軌（YouTube 沒有這個 API），這顆鈕只記下站主說傳好了，面板那格顯示「你說已上傳」。

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
2. 勾配音：`dub --locale <l>` → 塞不下的句子交翻譯模型縮短（最多 2 輪）→ `check-audio --locale <l>` → Jev 標記 → `dub --redo`（最多 2 輪）→ 仍不行寫 `dubs/<l>/skipped.json`，不擋。
3. 全部語言做完：`captions`（只寫 zh-TW 與勾了 CC 的語系；有配音的跟配音時間軸）→ `package`（`upload/` 只放 zh-TW 與勾了的：`description.<l>.txt`、`captions/<l>.srt`、`dubs/<l>.m4a`；`metadata.json` 的 `locales` 照決定）→ `review-push --gate languages`。
4. `qa` 的 `captions` 與 `metadata` 項、`package` 的 `captions` 與 `descriptions` 項都改成「zh-TW 加勾了的」；跳過的算過、列成警告。

旁白不是 zh-TW 的影片（`narration_locale`，例如 `en`）：面板不會列 zh-TW，但 `captions`、`package`、`qa` 永遠要它（`alwaysLocales`），所以語言一決定，工人先把 zh-TW 的標題說明與 CC 翻一次（不配音），再做勾了的；什麼都沒勾時只把 `captions` 與 `package` 重寫一次，不送語言批次。成片審核卡也永遠帶旁白語言與 zh-TW 的標題說明。

沒勾語言、或按了「只出繁體中文」的影片：`captions` 只寫 zh-TW，`package` 只有 zh-TW，跟現在比少了三個語系的檔案，其餘一個位元組都不變。`caption_locales` 不再驅動任何工作。

之後多勾的：工人看到 `locales` 裡有 ready／skipped 都沒有的部件就再做一批，送新的 `languages` 審核（舊的 superseded）。

## 成本

- 翻譯：每個語言一次翻譯加一次審稿呼叫（現在三語都做，之後只做勾的，只會少不會多）。
- 配音：`DUBS.md` §成本（一條 10 分鐘約 US$0.135；三條約 US$0.41；月額度要先調高）。
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
