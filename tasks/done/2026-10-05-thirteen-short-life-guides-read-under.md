---
id: 2026-10-05-thirteen-short-life-guides-read-under
title: Thirteen short life guides read under the 1,500-character floor in zh-TW, zh-CN and ko
status: done
priority: P3
area: docs
owner: claude-opus-5-5-short-life-a
claimed_at: 2026-10-06T01:15:09Z
created_at: 2026-10-05T06:52:42Z
completed_at: 2026-10-06T13:35:41Z
branch: claude/short-life-a
depends_on: []
scope:
  - apps/api/app/guides/content/backup-and-restore-home-files.json
  - apps/api/app/guides/content/browser-bookmark-project-folders.json
  - apps/api/app/guides/content/desk-cable-charging-organization.json
  - apps/api/app/guides/content/digital-receipt-archive.json
  - apps/api/app/guides/content/email-triage-three-actions.json
  - apps/api/app/guides/content/file-naming-system-for-home.json
  - apps/api/app/guides/content/gadget-purchase-needs-checklist.json
  - apps/api/app/guides/content/meeting-notes-action-template.json
  - apps/api/app/guides/content/notification-focus-boundaries.json
  - apps/api/app/guides/content/phone-document-scanning-workflow.json
  - apps/api/app/guides/content/phone-photo-declutter-workflow.json
  - apps/api/app/guides/content/reading-notes-that-you-reuse.json
  - apps/api/app/guides/content/shared-household-calendar.json
---

# Thirteen short life guides read under the 1,500-character floor in zh-TW, zh-CN and ko

## Why

`2026-10-04-two-ja-life-articles-read-under` 把 `household-inventory-spreadsheet` 與 `weekly-review-reset-routine`
五語都補過 1,500 字之後，`pack_cli lint --kind life` 仍有 17 個 pack 有低於下限的 `text_length` 警告。其中四個是索引／目錄頁
（`claude-code-templates-cheatsheet`、`claude-code-tutorials`、`codex-learning-hub`、`gemini-guide`），短是設計，不在本票。
其餘 13 篇和那兩篇同一批（#468 的生活分享原創文）：zh-TW 原文約 950–1,010 字，zh-CN 跟著短，ko 多半在 1,400 上下，
少數連 ja 也低於下限。讀者拿到的是一篇偏短、缺一兩個實際操作段落的文章；這是警告不是錯誤，不擋 ingest 或 CI。

2026-10-05 在 `claude/ja-life-length` 上量的 `_body_length`（只列低於 1,500 的語言）：

| pack | 低於下限的語言 |
| --- | --- |
| `backup-and-restore-home-files` | zh-TW 1,004、ko 1,433、zh-CN 1,050 |
| `browser-bookmark-project-folders` | zh-TW 997、ko 1,455、zh-CN 1,070 |
| `desk-cable-charging-organization` | zh-TW 953、ko 1,427、zh-CN 997 |
| `digital-receipt-archive` | zh-TW 1,001、ko 1,436、zh-CN 1,075 |
| `email-triage-three-actions` | zh-TW 955、ja 1,442、ko 1,224、zh-CN 995 |
| `file-naming-system-for-home` | zh-TW 1,011、ko 1,415、zh-CN 1,018 |
| `gadget-purchase-needs-checklist` | zh-TW 974、ko 1,407、zh-CN 992 |
| `meeting-notes-action-template` | zh-TW 951、ja 1,405、ko 1,293、zh-CN 990 |
| `notification-focus-boundaries` | zh-TW 956、ja 1,445、ko 1,271、zh-CN 991 |
| `phone-document-scanning-workflow` | zh-TW 986、ko 1,412、zh-CN 1,020 |
| `phone-photo-declutter-workflow` | zh-TW 1,001、ko 1,445、zh-CN 1,011 |
| `reading-notes-that-you-reuse` | zh-TW 970、ko 1,379、zh-CN 982 |
| `shared-household-calendar` | zh-TW 966、ko 1,369、zh-CN 990 |

## Definition of done

- [x] 每一篇要嘛五語都補到 1,500 字以上（補讀者用得到的操作段落，不是填字數、不是連結清單），要嘛在本票 Notes 寫明為什麼保留短篇。
- [x] `pack_cli lint --kind life` 對這 13 個 slug 不再有低於下限的 `text_length` 警告，或 Notes 逐篇交代保留的理由。
- [ ] 改過的內容包在合併後由協調者經站主同意重新匯入（`guides-import --slug ... --dry-run`，再 `--publish`）。

## Steps

- [x] 逐篇讀 zh-TW 原文，判斷缺哪一段讀者真的會用到的內容（走 skill `content-pipeline`，五語一起改，en 不要超過 6,000）。
- [x] 新增的產品功能、數字都要有當天打開的官方來源並更新 `checked_on`；沒有新事實就只重開既有來源確認仍成立。
- [x] 跑下方的 lint、`intake_check.py --from-content`、`docs/news-2026-batch-4/translation_checks.py`、`tests/test_guides_content_pack.py`。

## How to verify

```bash
cd apps/api
PYTHONUTF8=1 uv run python -m app.guides.pack_cli lint --kind life \
  --slug backup-and-restore-home-files --slug browser-bookmark-project-folders \
  --slug desk-cable-charging-organization --slug digital-receipt-archive \
  --slug email-triage-three-actions --slug file-naming-system-for-home \
  --slug gadget-purchase-needs-checklist --slug meeting-notes-action-template \
  --slug notification-focus-boundaries --slug phone-document-scanning-workflow \
  --slug phone-photo-declutter-workflow --slug reading-notes-that-you-reuse \
  --slug shared-household-calendar
```

## Notes

- 從 `2026-10-04-two-ja-life-articles-read-under` 發現（不是拆票）。那張票的做法可以照抄：每篇加一個 H2（約 450–600 個 zh-TW 字，
  段落加一張小表或清單），內容是原文沒講到的操作規則，例如「誰在什麼時候更新」「中斷後怎麼接回來」；四語由同一份 zh-TW 對譯。
- `no_summary` 與 `intake_check.py` 的「first block is not summary」不在本票：摘要走 `2026-09-15-content-summary-howto-and-life`，
  那張票要站主逐批審 diff。
- 只補正文，不改標題：其他文章的 article inline 把這些標題存成自己的 `text`，改標題會牽動別的內容包。
- 2026-10-06 分工：本票分兩條線並行。`claude/short-life-a`（claude-opus-5-5-short-life-a，持有認領）只做前七篇：
  `backup-and-restore-home-files`、`browser-bookmark-project-folders`、`desk-cable-charging-organization`、`digital-receipt-archive`、
  `email-triage-three-actions`、`file-naming-system-for-home`、`gadget-purchase-needs-checklist`；另外六篇由 short-life-b 的 PR 做。
  DoD 與 Steps 每一項都涵蓋 13 篇，所以 short-life-a 一項都不勾；兩個 PR 都合併後由協調者勾選並 `done`。scope 沒有縮小。
- 2026-10-06 short-life-a 的七篇（每篇加一個 H2：一段說明＋一張三欄表＋兩段操作規則，五語由同一份 zh-TW 對譯，標題與 summary 都沒動）：
  - `backup-and-restore-home-files`：「抽查找不到檔案時，先查這幾個地方」，放在「把檢查排成可維持的習慣」之前。四種失敗狀況各查什麼；
    檔案歷程記錄只備份媒體櫃與文件／圖片／影片／桌面，其他資料夾要先加入媒體櫃；「還原先前版本」挑刪除前一天的資料夾版本、
    先預覽、用「還原到」避免取代（取代無法復原）；復原磁碟機不含個人檔案；多臺裝置由誰抽查、失敗時記原因與下次日期。
  - `browser-bookmark-project-folders`：「舊收藏有幾百個時，先排出處理順序」，放在「書籤之外的重要資訊」之前。側邊面板按
    「上次開啟時間」排序先處理沉睡的一批；認不出用途的先移進「待刪」資料夾（刪除後無法還原），緩衝期滿再刪；`@bookmarks` + Tab
    只搜書籤；同帳號多裝置在電腦上整理、共用電腦只整理自己的使用者資料。
  - `desk-cable-charging-organization`：「看懂 USB-C 線上的標誌，再決定放哪一區」，放在「讓走線配合每天的動作」之前。USB-IF 認證的
    C 對 C 線必須標 60W 或 240W，USB 2.0 以外還要標資料速度（例：20Gbps／60W）；四種標示各放哪一區；一端非 USB 接頭或固定在裝置上的
    線不在認證範圍；認證線不會提高裝置本身的能力；待確認區定期清。
  - `digital-receipt-archive`：「先決定哪些收據要存，再固定整理的時間」，放在「掃描後檢查可讀性與完整性」之前。依用途（不是金額）
    分四類決定存不存、何時整理；Android 版 OneDrive 選「文件」模式、存檔前就輸入「日期_商品_店家」、自動存 PDF、多頁掃描一次最多 10 頁；
    「待整理」資料夾每週清空、多人購物送同一個收件資料夾、確認檔案能開再刪相簿裡的重複照片。
  - `email-triage-three-actions`：「休假幾天回來，先接回承諾，再處理數量」，放在「整理舊信與處理新信分開」之前。先照等待清單搜回覆；
    四類信件的成批處理（封存、略過）；封存的信有人回覆會回到收件匣、垃圾桶 30 天後自動刪除、`is:muted` 找回略過的討論串、「延後」；
    出發前更新等待清單並告知急事聯絡人、回來第一天只處理承諾與急事。
  - `file-naming-system-for-home`：「已經混在一起的版本，先收斂成一份原稿」，放在「整理完成的標準，是找得到正確檔案」之前。清單檢視
    依名稱排序找相近檔名；原稿＋捷徑（刪捷徑不刪原檔）；沒有搬移權限只會建立捷徑；資料夾顏色只套用在自己的畫面；共用資料夾由建立者
    或負責人改狀態；誤刪可從垃圾桶還原但不能當作不確認的理由。
  - `gadget-purchase-needs-checklist`：「下單前，替候選產品查一次「壞了怎麼辦」」，放在「到貨後先驗證關鍵用途」之前。iFixit 評分的
    手冊 10%、零件 10%、設計 80%；五項買前可查的維修資訊；新品零件常要 3–6 個月才買得到；零件配對需要製造商軟體；iFixit 引用的研究：
    維修費超過新品約三分之一時多數人不修，自訂「修或換」界線。
- 2026-10-06 來源（編輯 UA `curl -sSL`，都看 HTTP 狀態與內文）：Microsoft 備份／還原總覽、File History、Chrome 書籤、USB-IF
  `cable_connector`、Android 版 OneDrive 掃描、Gmail 整理與封存、Google Drive 整理、iFixit 評分方法八頁都是 200，內文支持原有句子與新段落，
  五語 `checked_on` 改成 2026-10-06。UI 名稱另外對過同一批說明頁的 zh-TW／zh-CN／ja／ko 版（File History、Chrome、Gmail、Drive、
  OneDrive 各四語，全部 200）。`www.microsoft.com/en-us/microsoft-365/onedrive/document-scanning` 三次逾時（60–90 秒、0 bytes，
  同站首頁 200），沒有讀到，所以 `digital-receipt-archive` 的這個來源 `checked_on` 留在 2026-09-14，引用它的舊句子也沒改；新段落只用
  Android 說明頁的事實。
- 2026-10-06 順手改的既有句子（同檔、只改正文）：
  - `file-naming-system-for-home`：Drive 說明頁現在寫的是建立資料夾、移動、捷徑與命名建議，沒有「重新命名」的步驟，所以五語把
    「建立、移動、重新命名與捷徑」改成「建立、移動、命名與捷徑」（en／ja／ko／zh-CN 同義），`checked_on` 才能誠實改日期。
  - `desk-cable-charging-organization`、`digital-receipt-archive`、`email-triage-three-actions` 的 zh-TW 原本各有兩次「本文／這篇」，
    `intake_check.py` 判 FAIL（讀者優先上限 1 次）。第二次改成「這裡」或「這套做法」，zh-CN 同步；意思不變。
- 2026-10-06 `_body_length` 前 → 後（zh-TW / en / ja / ko / zh-CN），全部落在 1,500–6,000：
  - backup：1,004 / 3,178 / 1,667 / 1,433 / 1,050 → 1,663 / 5,099 / 2,705 / 2,257 / 1,717
  - bookmark：997 / 3,323 / 1,704 / 1,455 / 1,070 → 1,528 / 4,905 / 2,569 / 2,159 / 1,603
  - desk-cable：953 / 3,284 / 1,687 / 1,427 / 997 → 1,545 / 5,051 / 2,582 / 2,223 / 1,589
  - receipt：1,001 / 3,416 / 1,699 / 1,436 / 1,075 → 1,563 / 5,096 / 2,601 / 2,178 / 1,651
  - email：955 / 2,945 / 1,442 / 1,224 / 995 → 1,534 / 4,647 / 2,345 / 1,961 / 1,586
  - file-naming：1,011 / 3,056 / 1,583 / 1,415 / 1,018 → 1,594 / 4,859 / 2,473 / 2,198 / 1,618
  - gadget：974 / 3,424 / 1,604 / 1,407 / 992 → 1,523 / 5,312 / 2,494 / 2,150 / 1,548
- 2026-10-06 short-life-a 的檢查（`apps/api`，`PYTHONUTF8=1`）：七個 slug 的 `pack_cli lint --kind life` 0 error、沒有 `text_length`，
  只剩原本的 `no_summary` ×35；`intake_check.py --from-content` 七篇都 `body_length ok`，唯一 FAIL 是改動前就有的「first block is not summary」；
  `docs/news-2026-batch-4/translation_checks.py "" <七個 slug>` 0 hit；`pytest tests/test_guides_content_pack.py tests/test_guides_content_links.py`
  12 passed、5 skipped；全站 `pack_cli lint --kind life`（1,004 篇）0 error，低於下限的 pack 從 17 降到 10（四個索引頁＋ short-life-b 的六篇）。
- 發布（合併並部署之後，協調者取得站主同意才做；publish after merge (coordinator, owner consent)）：兩個 PR 都合併後，
  `guides-import --slug <13 個 slug> --locale zh-TW --locale en --locale ja --locale ko --locale zh-CN --dry-run` 應為 65 個 `update`
  （只有 short-life-a 合併時是前七篇的 35 個），再換成 `--publish --actor-email <ACTOR_EMAIL>`，之後 `guides-links-rebuild`。
- 2026-10-06 claude-opus-5-5-train-a：#1331（short-life-a，七篇）與 #1332（short-life-b，六篇）一起併入 train 分支 `claude/train-a-18-green`。
  併完後上方 How to verify 的 13 個 slug `pack_cli lint --kind life` 沒有任何 `text_length` 警告（只剩本票範圍外的 `no_summary`），
  前兩項 DoD 與 Steps 都勾選。第三項（合併並部署後經站主同意的 `guides-import` dry-run 65 個 update → `--publish` → `guides-links-rebuild`）
  是合併後的發布動作，不是程式工作，留給協調者照上一條 Notes 做；本票以 done 結案。
