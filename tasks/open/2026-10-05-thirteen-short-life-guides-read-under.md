---
id: 2026-10-05-thirteen-short-life-guides-read-under
title: Thirteen short life guides read under the 1,500-character floor in zh-TW, zh-CN and ko
status: open
priority: P3
area: docs
owner:
claimed_at:
created_at: 2026-10-05T06:52:42Z
completed_at:
branch:
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

- [ ] 每一篇要嘛五語都補到 1,500 字以上（補讀者用得到的操作段落，不是填字數、不是連結清單），要嘛在本票 Notes 寫明為什麼保留短篇。
- [ ] `pack_cli lint --kind life` 對這 13 個 slug 不再有低於下限的 `text_length` 警告，或 Notes 逐篇交代保留的理由。
- [ ] 改過的內容包在合併後由協調者經站主同意重新匯入（`guides-import --slug ... --dry-run`，再 `--publish`）。

## Steps

- [ ] 逐篇讀 zh-TW 原文，判斷缺哪一段讀者真的會用到的內容（走 skill `content-pipeline`，五語一起改，en 不要超過 6,000）。
- [ ] 新增的產品功能、數字都要有當天打開的官方來源並更新 `checked_on`；沒有新事實就只重開既有來源確認仍成立。
- [ ] 跑下方的 lint、`intake_check.py --from-content`、`docs/news-2026-batch-4/translation_checks.py`、`tests/test_guides_content_pack.py`。

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

## Review round (independent, 2026-10-06) — #1332

The round-1 report follows verbatim, with its headings moved down two levels so they sit under this section.

### verify-1: PR #1332 (claude/short-life-b), six short life guides get their operational sections

Checked on 2026-10-06 by an independent round-1 fact-checker (I did not write this PR). Read-only: nothing was edited, committed or posted.
Diff: `git diff origin/main...origin/claude/short-life-b`, one commit (8ed1a018), six packs, five locales each (zh-TW, en, ja, ko, zh-CN).
Fetch method: `curl -sSL -A 'Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)'`, about 1.2 s between requests. HTML comments were stripped before reading. No personal data was sent in any header, query or form. Every official page was also fetched in the zh-Hant/zh-tw, ja, ko and zh-Hans/zh-cn versions, so each locale's UI names were checked against that locale's own help page.

#### Sources fetched (all HTTP 200)
| Source | URL(s) | Status |
|---|---|---|
| Google Docs: @ menu | support.google.com/docs/answer/11276813?hl=en / zh-Hant / ja / ko / zh-Hans | 200 ×5 |
| Google Drive: scan (Android) | support.google.com/drive/answer/3145835?co=GENIE.Platform%3DAndroid&hl=en / zh-Hant / ja / ko / zh-Hans | 200 ×5 |
| Google Drive: scan (iOS tab, for cross-check) | …3145835?co=GENIE.Platform%3DiOS&hl=en | 200 |
| Google Calendar: share | support.google.com/calendar/answer/37082?hl=en / zh-Hant / ja / ko / zh-Hans | 200 ×5 |
| Apple: Set up a Focus | support.apple.com/{en-sg,zh-tw,ja-jp,ko-kr,zh-cn}/guide/iphone/iphd6288a67f/ios | 200 ×5 |
| Apple: Merge duplicates | support.apple.com/{en-by,zh-tw,ja-jp,ko-kr,zh-cn}/guide/iphone/iph1978d9c23/ios | 200 ×5 |
| Apple: Delete or hide photos (new source) | support.apple.com/{en-by,zh-tw,ja-jp,ko-kr,zh-cn}/guide/iphone/iphb4defbde9/ios | 200 ×5 |
| Cornell LSC page | lsc.cornell.edu/how-to-study/taking-notes/cornell-note-taking-system/ | 200 |
| Cornell LSC PDF (new source) | lsc.cornell.edu/wp-content/uploads/2016/10/Cornell-NoteTaking-System.pdf | 200, application/pdf, text read with pdftotext |

#### Claim table
| # | Slug | Claim (zh-TW, then locale parity) | Source | Verdict |
|---|---|---|---|---|
| 1 | meeting-notes | @ menu can insert dropdowns | Docs @ menu | CONFIRMED |
| 2 | meeting-notes | @ menu can insert checklists | Docs @ menu | CONFIRMED |
| 3 | meeting-notes | Custom building blocks cannot be shared | Docs @ menu | CONFIRMED |
| 4 | meeting-notes | Only the creator can reuse one | Docs @ menu | CONFIRMED |
| 5 | meeting-notes | Others copy the template to make their own | Docs @ menu | CONFIRMED |
| 6 | meeting-notes | checked_on 2026-10-06 (page reachable) | Docs @ menu | CONFIRMED |
| 7 | meeting-notes | Situation table, 4 rows, the same in all 5 locales | internal | CONFIRMED |
| 8 | meeting-notes | "postponed twice in a row" the same in all locales | internal | CONFIRMED |
| 9 | meeting-notes | Status labels (待確認/待辦 · to confirm/action item · 確認待ち/対応事項 · 확인 필요/할 일 · 待确认/待办) match the article's existing table | internal | CONFIRMED |
| 10 | notification | Settings app > Focus > choose a Focus | Focus | CONFIRMED |
| 11 | notification | People = whose notifications are allowed | Focus | CONFIRMED |
| 12 | notification | Apps = which apps are allowed | Focus | CONFIRMED |
| 13 | notification | Options = show silenced notifications on the Lock Screen | Focus | CONFIRMED |
| 14 | notification | Add Schedule = time, location, or while using an app | Focus | CONFIRMED |
| 15 | notification | Add Filter = which mail account or calendar to use | Focus | CONFIRMED |
| 16 | notification | Custom Focus with your own name | Focus | CONFIRMED |
| 17 | notification | Share Across Devices = same settings on Apple devices signed in to the same Apple Account | Focus | CONFIRMED |
| 18 | notification | Focus filters are not synced | Focus | CONFIRMED |
| 19 | notification | Share Focus Status = people who message you see notifications are silenced | Focus | CONFIRMED |
| 20 | notification | Change it per person on their contact card | Focus | CONFIRMED |
| 21 | notification | zh-TW labels 「設定」「專注模式」「聯絡人」App「選項」「加入排程」「加入過濾條件」「在所有裝置上共享」「分享專注模式狀態」 | Focus zh-tw | CONFIRMED |
| 22 | notification | ja labels 集中モード/連絡先/アプリ/オプション/スケジュールを追加/フィルタを追加/デバイス間で共有/集中モード状況を共有 | Focus ja-jp | CONFIRMED |
| 23 | notification | ko labels 사람/앱/옵션/시간 지정 추가/필터 추가/모든 기기에서 공유/집중 모드 상태 공유/사용자 설정 집중 모드 | Focus ko-kr | CONFIRMED |
| 24 | notification | zh-CN labels 联系人/选项/添加定时/添加过滤条件/在设备之间共享/共享专注模式状态 | Focus zh-cn | CONFIRMED |
| 25 | notification | Situation table, 4 rows × 4 columns, the same in all locales | internal | CONFIRMED |
| 26 | notification | 本文→這裡 (zh-TW) and 本文→这里 (zh-CN): zh-TW now has 這篇 ×1 and 本文 ×0 | reader-first | CONFIRMED |
| 27 | scanning | Done, then type a file name or pick a suggested title | Drive Android | CONFIRMED |
| 28 | scanning | Choose .pdf or .jpg | Drive Android | CONFIRMED |
| 29 | scanning | Location (optional) picks the folder | Drive Android | CONFIRMED |
| 30 | scanning | Then Save | Drive Android | CONFIRMED |
| 31 | scanning | Crop & Rotate | Drive Android | CONFIRMED |
| 32 | scanning | Filter = colour or grayscale | Drive Android | CONFIRMED |
| 33 | scanning | Clean = stains, fingers | Drive Android | CONFIRMED |
| 34 | scanning | "Drive scan" widget; choose the save folder when setting it up | Drive Android | CONFIRMED |
| 35 | scanning | Add / Retake / Delete | Drive Android | CONFIRMED |
| 36 | scanning | Switch between Manual and Auto capture | Drive Android | CONFIRMED |
| 37 | scanning | PDFs are searchable | Drive Android | CONFIRMED |
| 38 | scanning | "On iPhone … the buttons have different names, but you can check the same three things" | Drive iOS help | **WRONG**: Drive for iPhone uses the same names, and its help lists no .pdf/.jpg choice (see errors) |
| 39 | scanning | zh-TW labels 完成/位置/儲存/裁剪及旋轉/篩選器/清理/雲端硬碟掃描/新增/重拍/刪除 | Drive zh-Hant | CONFIRMED |
| 40 | scanning | ja labels ［完了］［場所］［保存］切り抜きと回転/フィルタ/汚れ除去/［ドライブのスキャン］/追加/再撮影/削除/手動撮影 | Drive ja | CONFIRMED |
| 41 | scanning | ko labels 완료/위치/저장/자르기 및 회전/필터/지우기/드라이브 스캔/추가/다시 촬영/삭제/수동 캡처 | Drive ko | CONFIRMED |
| 42 | scanning | zh-CN labels 完成/位置/保存/剪裁和旋转/滤镜/清理/云端硬盘扫描/添加/重拍/删除/手动拍摄 | Drive zh-Hans | CONFIRMED |
| 43 | scanning | Table and example file name the same in all locales | internal | CONFIRMED |
| 44 | photos | Deleted items stay in Recently Deleted for 30 days | Delete/hide | CONFIRMED |
| 45 | photos | Then permanently removed from iPhone, iCloud and other devices on the same Apple Account | Delete/hide | CONFIRMED |
| 46 | photos | Can be recovered during those 30 days | Delete/hide | CONFIRMED |
| 47 | photos | With iCloud Photos on, delete or hide applies on all devices | Delete/hide | CONFIRMED |
| 48 | photos | Collections > Utilities > Duplicates > Merge | Merge | CONFIRMED |
| 49 | photos | Hide via the photo's options (More > Hide); it moves to the Hidden collection | Delete/hide | CONFIRMED |
| 50 | photos | Select, then delete; items go to Recently Deleted | Delete/hide | CONFIRMED |
| 51 | photos | Recover in Recently Deleted | Delete/hide | CONFIRMED |
| 52 | photos | Recently Deleted and Hidden are locked by default; unlock with Face ID, Touch ID or passcode | Delete/hide | CONFIRMED |
| 53 | photos | Hidden is not a backup ("can't view them anywhere else") | Delete/hide | CONFIRMED (fair reading of the source) |
| 54 | photos | zh-TW labels 選集>更多項目>重複項目/合併/最近刪除/已隱藏/隱藏/選取/復原/iCloud 照片 | zh-tw pages | CONFIRMED |
| 55 | photos | ja labels コレクション>ユーティリティ>重複項目/結合/最近削除した項目/非表示/選択/復旧 | ja-jp pages | CONFIRMED |
| 56 | photos | ko labels 모음>기타>중복된 항목/병합/최근 삭제된 항목/가려진 항목/가리기/선택/복구/암호 | ko-kr pages | CONFIRMED |
| 57 | photos | zh-CN labels 精选集>更多项目>重复项目/最近删除/已隐藏/选择/恢复/面容 ID/触控 ID | zh-cn pages | CONFIRMED |
| 58 | photos | New source iphb4defbde9 (titles in each locale, en-by URL) | Delete/hide | CONFIRMED |
| 59 | reading-notes | Designed for lectures; record during class | Cornell PDF | CONFIRMED |
| 60 | reading-notes | Write questions as soon after class as possible | Cornell PDF | CONFIRMED |
| 61 | reading-notes | Cover the notes, look at the questions, answer aloud in your own words | Cornell PDF | CONFIRMED |
| 62 | reading-notes | Reflect: how to apply it, how it fits what you already know | Cornell PDF | CONFIRMED |
| 63 | reading-notes | Summary space at the bottom of each page | Cornell PDF | CONFIRMED |
| 64 | reading-notes | At least ten minutes every week reviewing previous notes | Cornell PDF | CONFIRMED |
| 65 | reading-notes | New PDF source is reachable and is a PDF | Cornell PDF | CONFIRMED |
| 66 | reading-notes | Existing LSC page source, checked_on bumped | LSC page | CONFIRMED (200) |
| 67 | reading-notes | 10 minutes and the step order the same in all locales | internal | CONFIRMED |
| 68 | reading-notes | 本文→下面 (zh-TW): 這篇 ×1, 本文 ×0 | reader-first | CONFIRMED |
| 69 | calendar | A different permission per person | Calendar | CONFIRMED |
| 70 | calendar | "Make changes and manage sharing" | Calendar | CONFIRMED |
| 71 | calendar | "Make changes and see event details" | Calendar | CONFIRMED |
| 72 | calendar | "See event details" | Calendar | CONFIRMED |
| 73 | calendar | "See only free/busy (hide details)" | Calendar | CONFIRMED |
| 74 | calendar | Manage sharing lets that person share the calendar with others | Calendar | CONFIRMED |
| 75 | calendar | Recipient gets an email and must click its link to add the calendar | Calendar | CONFIRMED |
| 76 | calendar | Troubleshooting: check the address, spam/trash, search for your email, remove and re-add | Calendar | CONFIRMED |
| 77 | calendar | Remove people under "Shared with" | Calendar | CONFIRMED |
| 78 | calendar | zh-TW labels 進行變更並管理共用設定/變更活動及查看活動詳細資料/查看活動詳細資料/只能看見是否有空（隱藏詳細資訊）/共用對象 | Calendar zh-Hant | CONFIRMED |
| 79 | calendar | ja labels 予定の変更および共有の管理/予定の詳細を変更、表示可能/予定の詳細の表示/予定の表示（時間枠のみ、詳細は非表示）/［共有する相手］ | Calendar ja | CONFIRMED |
| 80 | calendar | ko labels 변경 및 공유 관리/변경 후 일정 세부정보 확인/한가함/바쁨 정보만 보기(세부정보는 숨김)/공유 대상 | Calendar ko | CONFIRMED; row 3 「일정 세부정보 보기」 differs from the help's 「진행 중 이벤트 확인하기」 (see unverifiable) |
| 81 | calendar | zh-CN labels 进行更改和管理共享设置/做出更改并查看活动详情/查看活动详情/只能看到有空/忙碌信息（隐藏详细信息）/共享对象/“垃圾邮件”“已删除邮件” | Calendar zh-Hans | CONFIRMED |
| 82 | calendar | Role table, 4 rows, the same in all locales | internal | CONFIRMED |

#### Summary
- **Claims checked:** 82
- **Confirmed:** 81
- **Wrong:** 1 (#38, the same sentence in all five locales of phone-document-scanning-workflow)
- **Not found:** 0
- **Fact changes needed:** 1. Rule 7 calls for a second round only after more than three fact changes, so a second round is not required on these grounds.
- **Style findings (optional):** 3, all in meeting-notes-action-template.
  - The feature name for "building blocks" does not match the official locale help in three locales:
    - ko 맞춤 구성 요소 → 맞춤 템플릿
    - zh-CN 构建块 → 智能模块
    - zh-TW 建構區塊/核取清單 → 構成元素/檢查清單
  - The new paragraph only continues the wording the older paragraph already used. If the fixer changes it, both paragraphs need the change.
- **Per-locale review:** All five locales say the same thing as zh-TW in every new section: numbers (30 days, ten minutes, twice, seven days, 2026-10), names, table rows and order. The UI labels in each locale match that locale's own Apple or Google help page. Japanese uses 「復旧」 as the button and 「復元」 as the action heading, which matches Apple's ja page. The translations read naturally, and I found no mistranslations.
- **Internal consistency:**
  - The new sections do not contradict the existing intros, tables, descriptions or summaries.
  - The diagrams are unchanged and carry no numbers that the new text affects.
  - The status labels in meeting-notes match the article's earlier table.
- **Reader-first:**
  - zh-TW now has at most one 本文/這篇 per article (photo-declutter: 本文 ×1; the other five: 這篇 ×1).
  - No verification narration or attribution clutter in the new paragraphs. Source attributions sit in captions ("按鈕名稱依…說明"), which is acceptable.
- **Self-checks:** Not run (no venv in the clone, and the task is read-only). CI's results stand in for them.

#### Things suspected but not changed
- **Calendar, ko row 3:** The Korean help's label for "See event details" is 「진행 중 이벤트 확인하기」, which reads as a mistranslation. The article's 「일정 세부정보 보기」 is the sensible rendering, but the caption claims the names follow the help. Option: soften the ko caption, or leave it as is.
- **Photo-declutter, pre-existing paragraph (not in this diff):** It says a missing duplicates category does not prove there are no duplicates. Apple's merge page says the Duplicates collection does not appear when the system finds none. These are compatible (the article means visually similar shots), so no action.

### Applied (2026-10-06, on claude/short-life-b)

All four corrections were applied after their sources were re-read with the editorial UA (`curl -sSL`, comments stripped, HTTP 200 each).
- `phone-document-scanning-workflow`, the last paragraph of the save-name-format-location section, all five locales: the Drive scan help for iPhone & iPad (`3145835?co=GENIE.Platform%3DiOS`, read in en, zh-Hant, ja, ko and zh-Hans) uses the same button names as Android and goes Done → file name → optional Location → Save, with no .pdf/.jpg step and no widget section. The sentence now says other apps may name the buttons differently but still let you check the file name and location before saving, and that Drive for iPhone keeps the same names while its help has no .pdf/.jpg step. The rest of the paragraph is unchanged. The iOS page was added to `sources` in each locale (checked_on 2026-10-06).
- `meeting-notes-action-template` ko, both paragraphs: 구성 요소 → 템플릿, 맞춤 구성 요소는 → 맞춤 템플릿은. The ko help uses 템플릿 throughout, including the menu path 삽입 > 템플릿 (`answer/15740443`) and 맞춤 템플릿 (`answer/13584759`).
- `meeting-notes-action-template` zh-CN, both paragraphs: 构建块 → 智能模块, 自定义构建块 → 自定义智能模块, as on the cited @ menu page. The zh-Hans help is not consistent with itself: the insert page (`answer/15740443`) gives the menu as 插入 > 组成要素, and the smart-chips page says 构建基块. 构建块 appears on none of them.
- `meeting-notes-action-template` zh-TW, both paragraphs: 建構區塊 → 構成元素, 自訂的建構區塊 → 自訂構成元素, 核取清單 → 檢查清單. The zh-Hant help uses 構成元素 for the menu (插入 > 構成元素) and 檢查清單 on the @ menu page.
- Not changed: the two items under "Things suspected but not changed". Second round: not required (one fact change, repeated in five locales).
- Checks: `pack_cli lint --kind life` on the six PR slugs gives 0 errors (only the existing `no_summary` warnings). `intake_check.py --from-content` adds no new FAIL against origin/main; the only FAIL left is "first block is not summary", which this ticket leaves out. `translation_checks.py` gives 0 hits.
