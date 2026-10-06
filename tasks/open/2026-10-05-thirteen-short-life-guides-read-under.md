---
id: 2026-10-05-thirteen-short-life-guides-read-under
title: Thirteen short life guides read under the 1,500-character floor in zh-TW, zh-CN and ko
status: in-progress
priority: P3
area: docs
owner: claude-opus-5-5-short-life-a
claimed_at: 2026-10-06T01:15:09Z
created_at: 2026-10-05T06:52:42Z
completed_at:
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

## Review round (independent, 2026-10-06) — #1331

The round-1 report follows verbatim, with its headings moved down two levels so they sit under this section.

### verify-1: PR #1331 (claude/short-life-a), seven short life guides, new sections

Checked 2026-10-06 by an independent round-1 fact-checker (read-only). Every fetch used `curl -sSL` with UA `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`, with HTML comments stripped and the HTTP status checked. No personal data was sent.

Diff read: `git diff origin/main...origin/claude/short-life-a`, 7 packs × 5 locales plus the task file. I extracted every block that is new or changed against main, per slug and locale, and read all of them in en, ja, ko and zh-CN against zh-TW.

#### Sources fetched (all HTTP 200 with real body unless noted)
| Source | URL (final) | Locales also read |
|---|---|---|
| MS File History | support.microsoft.com/en-au/windows/experience/backup-recovery/backup-and-restore-with-file-history (301 from the pack URL) | zh-tw, zh-cn, ja-jp, ko-kr |
| MS Backup/Restore/Recovery | support.microsoft.com/en-us/windows/experience/backup-recovery/backup-restore-and-recovery-in-windows (301 from the pack URL) | none |
| Chrome bookmarks | support.google.com/chrome/answer/188842?hl=en-UM | zh-Hant, zh-Hans, ja, ko |
| USB-IF | www.usb.org/cable_connector | none |
| OneDrive for Android scan | support.microsoft.com/en-us/onedrive/scan-a-whiteboard-document-business-card-or-photo-in-onedrive-for-android | zh-tw, zh-cn, ja-jp, ko-kr |
| Gmail organize & archive | support.google.com/mail/answer/9259770?hl=en | zh-Hant, zh-Hans, ja, ko |
| Google Drive organize | support.google.com/drive/answer/2375091?co=GENIE.Platform%3DDesktop&hl=en | zh-Hant, zh-Hans, ja, ko |
| iFixit scoring | www.ifixit.com/News/75533/how-ifixit-scores-repairability | none |
| OneDrive marketing page | www.microsoft.com/en-us/microsoft-365/onedrive/document-scanning | **200 bot-block shell, so not a source** (unchanged claim; checked_on correctly left at 2026-09-14) |

#### Claims (58 checked)
##### backup-and-restore-home-files (blocks 11–15)
1. File History automatically backs up Documents/Pictures/Videos/Desktop plus all libraries: CONFIRMED ("automatically backs up essential folders like Documents, Pictures, Videos, and Desktop"; "automatically backs up all your libraries").
2. Folders elsewhere must be added to a library: CONFIRMED.
3. "In File History, right-click the folder → Restore previous versions": **CHANGE NEEDED (all 5 locales).** The source does this step in File Explorer: "Open File Explorer and navigate to the folder… Right-click on the folder name, and then select Restore previous versions." File History only opens later, for the preview (Open → Open in File History).
4. Deleted today → choose yesterday's folder version: CONFIRMED.
5. Preview before restoring: CONFIRMED (expand Open → Open in File History).
6. Expand Restore → Restore to… another location: CONFIRMED.
7. A plain restore replaces the current version and can't be undone: CONFIRMED.
8. The recovery drive does not include personal files: CONFIRMED ("The Recovery Drive doesn't include your personal files").
9. Restore points and the recovery drive handle system state: CONFIRMED.
10. UI names: zh-TW 檔案歷程記錄/媒體櫃/還原先前版本/還原到; zh-CN 文件历史记录/库/还原以前的版本/还原到; ja ファイル履歴/ライブラリ/以前のバージョンの復元; ko 파일 히스토리 (MS ko page title)/라이브러리/이전 버전 복원: CONFIRMED.
- Sources: both pack URLs return 301. pitfalls.md wants the final URL; this predates the PR but the PR re-dated checked_on (style).

##### browser-bookmark-project-folders (blocks 11–15)
11. More > Bookmarks and lists > Show all bookmarks opens the side panel: CONFIRMED.
12. Organize icon → Sort by last opened: CONFIRMED (zh-Hant 「整理」/按「上次開啟時間」排序; zh-Hans 整理/按上次打开时间排序; ja 管理アイコン/最後に開いた日付で並べ替え; ko 구성/최근 연 날짜순으로 정렬).
13. A deleted bookmark can't be recovered: CONFIRMED in all 5 languages.
14. @bookmarks + Tab or Space, then keywords, searches bookmarks only: CONFIRMED.
15. Bookmarks and lists / Show all bookmarks localized labels: CONFIRMED (書籤和清單/顯示所有書籤; 书签和清单/显示所有书签; ブックマークとリスト/すべてのブックマークを表示; 북마크 및 목록/모든 북마크 표시).
16–17. Multi-device and shared-profile advice: editorial, no factual claim (OUT OF SCOPE).

##### desk-cable-charging-organization (blocks 3 wording, 8–12)
18. Certified USB-C to USB-C cables must carry a 60W or 240W power logo: CONFIRMED.
19. All except High-Speed USB (USB 2.0) cables must show the data rate: CONFIRMED.
20. Example 20Gbps/60W combined logo: CONFIRMED ("Combined Performance and Power 20Gbps/60W logo").
21. A certified cable with a power logo only is USB 2.0 class: CONFIRMED (follows from rule 19; USB 2.0 cables "required to have the power icon", speed logo optional).
22. A cable with one non-USB end or fixed to a device is outside certification: CONFIRMED ("Captive cables are not eligible… one USB connector and is either permanently attached or has a non-USB connector").
23. A certified cable doesn't raise a device's capability: CONFIRMED ("nor does it augment the capabilities of those products").
24. Block 3 change 本文→這裡 (zh-TW, zh-CN): wording only.
- Numbers 60/240/20 match across all 5 locales.

##### digital-receipt-archive (blocks 8–12, 15 wording)
25. OneDrive Android: choose Document mode: CONFIRMED (zh-tw [文件], zh-cn 文档, ja ドキュメント, ko 문서).
26. Enter a file name before saving: CONFIRMED ("tap Done, enter a file name, then tap Save").
27. Saved as PDF automatically: CONFIRMED.
28. Multi-page scan combines into one PDF, max 10 pages: CONFIRMED (all 4 localized pages say 10).
29. Receipt categories, weekly sorting, shared intake folder: editorial (OUT OF SCOPE).
30. en block 11 "Date_Item_Seller" vs en block 6 "Date_Product_Seller": **CONSISTENCY ERROR (en only).** The other four locales are identical in both places.
31. Callout 這套做法 (from 本文): wording only.
- Source 1 (marketing page) is unreadable to bots, so it is unverifiable. The PR correctly left its checked_on and its sentence alone.

##### email-triage-three-actions (blocks 3 wording, 11–15)
32. Archived mail is still in All Mail: CONFIRMED.
33. An archived message returns to the inbox when someone replies: CONFIRMED ("If someone replies to a message you archive, it returns to your inbox").
34. Trash auto-deletes after 30 days: CONFIRMED.
35. Mute: later replies skip the inbox and go to the archive: CONFIRMED.
36. is:muted finds muted threads: CONFIRMED.
37. Snooze: CONFIRMED.
38. Localized labels: zh-TW 封存/所有郵件/略過/延後/垃圾桶; zh-CN 归档/所有邮件/忽略/延后/已删除邮件; ja アーカイブ/すべてのメール/ミュート/スヌーズ/ゴミ箱; ko 보관처리/전체보관함/알림 끄기/다시 알림/휴지통: CONFIRMED.
39. The state names To do/Waiting/Archive in the new table match the existing table in every locale: CONFIRMED.

##### file-naming-system-for-home (blocks 3 changed, 11–15)
40. Block 3: "重新命名" removed. The Drive page has no rename step (naming-convention advice only): CONFIRMED, so the change is justified.
41. List view + sort by name surfaces similar-named duplicates: CONFIRMED.
42. Search bar to find suspected duplicates: CONFIRMED.
43. Deleting a shortcut doesn't delete the original: CONFIRMED.
44. Without move permission, a shortcut is created in the destination: CONFIRMED.
45. Custom folder colours apply only to your own view of Drive: CONFIRMED (zh-Hant 「只會套用到自己的雲端硬碟檢視畫面」).
46. Restore from trash: CONFIRMED.
47. Folder descriptions exist: CONFIRMED ("Add or edit descriptions").
48. Status examples 待確認→定稿 match the existing table (草稿、待確認、定稿): CONFIRMED.
49. Localized UI names (清單檢視/列表视图/リスト表示/목록 보기; 捷徑/快捷方式/ショートカット/바로가기): CONFIRMED.
- en block 14 "Anyone else with a view leaves a comment" is ambiguous ("view access"); zh-TW means "has an opinion" (translation).

##### gadget-purchase-needs-checklist (blocks 11–15)
50. Service manual 10%: CONFIRMED.
51. Replacement parts 10%: CONFIRMED.
52. Design for repair 80%: CONFIRMED.
53. Manual and parts are checkable on the OEM support site; registration or paywall disqualifies: CONFIRMED ("It can't be hidden away, require registration to access, or be locked behind a paywall").
54. 3–6 months after launch before parts are available: CONFIRMED ("not uncommon for 3-6 months to elapse").
55. Some genuine parts need OEM calibration or pairing software: CONFIRMED.
56. Studies cited by iFixit: repair over about 1/3 of the new price → many won't fix: CONFIRMED ("Studies show that if the cost of repair exceeds about a third of the price of a new product, many people won't bother fixing it").
57. Identifying marks and the settings screen: CONFIRMED.
58. Software-update length as a concern: CONFIRMED (iFixit notes it is not yet scored; the article only lists it as a check, which is fine).
- Ratios across locales: zh 一成/八成/三到六個月/三分之一, en 10 percent/80 percent/three to six months/a third, ja 1割/8割/3〜6か月/3分の1, ko 10%/80%/3~6개월/3분의 1. All match.

#### Per-locale review (en/ja/ko/zh-CN vs zh-TW, new sections)
- Numbers, dates and names match zh-TW in every locale (I diffed the numbers mechanically and then compared meaning by hand).
- Each locale keeps the register of its existing article (ko email uses -다 like the rest of that pack; the other ko packs use -요/-ㅂ니다).
- Issues: en receipt filename pattern inconsistency; en file-naming "with a view" ambiguity. ja backup block 14 doesn't name the [復元先] label but describes the action correctly (OK). ko desk-cable 「문제가 있다는 뜻은 아닙니다」 is slightly stronger than 不一定代表, but acceptable.

#### Reader-first
- 本文/這篇: exactly 1 in every zh-TW and zh-CN pack after the PR. The new sections contain no verification narration, and foreign terms are glossed on first use (檔案歷程記錄（File History）).

#### Suspected, not flagged as errors
- browser-bookmark zh-TW 「使用者資料」 and zh-CN 「用户配置」 for a Chrome profile repeat the wording of the existing block 3. Chrome's help pages say 設定檔 (zh-Hant) and 个人资料 (zh-Hans). The new block is consistent with the article, but the term is not Chrome's official one.
- desk-cable block 3 (existing) says USB-IF marks power and data speed 「分開標示」, while the new block 9 cites the combined 20Gbps/60W logo. These don't contradict each other (they are separate attributes shown on one combined logo), but a reader could notice.

#### Outcome
- 58 claims checked: 54 confirmed or out of scope, 1 fact change needed (the File History right-click step, in all 5 locales), 1 en consistency fix, 1 en translation fix, 1 source-URL style fix (301 redirects).
- 1 source unverifiable (OneDrive marketing page bot-block); unchanged content depends on it.
- Second round: the fact change is one claim repeated in five locales, so on the "more than three FACT changes" rule a second round is optional. The coordinator decides.

### Applied (2026-10-06, on claude/short-life-a)

All eight corrections were applied after their sources were re-read with the editorial UA (`curl -sSL`, comments stripped). The Microsoft File History page returned 200 in en-au, zh-tw, zh-cn, ja-jp and ko-kr, and every one starts the restore in File Explorer. Both old pack URLs return 301 to the final URLs.
- `backup-and-restore-home-files` block 14, all five locales: the right-click now happens in File Explorer (檔案總管／File Explorer／エクスプローラー／파일 탐색기／文件资源管理器). The rest of the paragraph is unchanged.
- `backup-and-restore-home-files` sources[0] and sources[1], all five locales: the post-redirect URLs. checked_on stays 2026-10-06.
- `digital-receipt-archive` en block 11: “Date_Product_Seller”, which matches block 6.
- `file-naming-system-for-home` en block 14: “Anyone else who has an opinion leaves a comment”.
- The two items under “suspected” were not changed. Second round: the coordinator decides, as the report says.

The round-2 report follows verbatim, with its headings moved down two levels so they sit under this section.

### verify-2: PR #1331 (claude/short-life-a), seven short life guides, new sections

An independent round-2 fact-checker ran this check on 2026-10-06, read-only. Branch head: `0e8c6a84e5045f1df866a698befd7203fe4c096f` (fetched again before checking). Every fetch used `curl -sSL` with UA `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`, at least 1.2 s apart per host. HTML comments were stripped before reading and the HTTP status was checked each time. No personal data was sent in any UA, header, query or form.

Scope: `git diff origin/main...origin/claude/short-life-a` covers 7 packs × 5 locales plus the task file. For each slug and locale I took every block that is new or changed against the merge-base and compared it with the head. Changes outside the new sections are limited to these:
- desk-cable zh-TW/zh-CN block 3, email-triage zh-TW/zh-CN block 3 and digital-receipt zh-TW/zh-CN callout: 本文/這篇文章 → 這裡/這套做法.
- file-naming block 3 in all locales: 「重新命名」 → 「命名」.
- `checked_on` re-dated to 2026-10-06.
- backup source URLs replaced.

Title, description and hero are unchanged in every locale.

#### Outcome

**No errors found.** All 8 round-1 corrections are applied correctly in every locale they cover and introduced nothing new. Every other new-section claim I checked (more than the required random third; in practice all of them) is CONFIRMED against the cited help page, in English and in the localized help page for ja, ko, zh-CN and zh-TW. The per-locale review of en/ja/ko/zh-CN against zh-TW found no mistranslation or meaning drift. Second round required: no further round (zero fact changes in this round).

#### Sources fetched
| Source | Final URL | Status | Locales also read |
|---|---|---|---|
| MS File History | support.microsoft.com/en-au/windows/experience/backup-recovery/backup-and-restore-with-file-history | 200 | zh-tw, ja-jp, ko-kr, zh-cn (all 200) |
| MS Backup/Restore/Recovery | support.microsoft.com/en-us/windows/experience/backup-recovery/backup-restore-and-recovery-in-windows | 200 | none |
| Old pack URL 1 (`/en-US/Windows/Experience/...`) | 301 to the URL above | 301 | none |
| Old pack URL 2 (`/en-au/windows/backup-and-restore-with-file-history-7bf065bf-...`) | 301 to the File History URL above | 301 | none |
| Chrome bookmarks | support.google.com/chrome/answer/188842?hl=en-UM | 200 | zh-Hant, ja, ko, zh-Hans (all 200) |
| USB-IF | www.usb.org/cable_connector | 200 | none |
| OneDrive for Android scan | support.microsoft.com/en-us/onedrive/scan-a-whiteboard-document-business-card-or-photo-in-onedrive-for-android | 200 | zh-tw, ja-jp, ko-kr, zh-cn (all 200) |
| Gmail organize & archive | support.google.com/mail/answer/9259770?hl=en | 200 | ko, ja, zh-Hans, zh-Hant (all 200) |
| Google Drive organize | support.google.com/drive/answer/2375091?co=GENIE.Platform%3DDesktop&hl=en | 200 | none |
| iFixit scoring | www.ifixit.com/News/75533/how-ifixit-scores-repairability | 200 | none |
| OneDrive marketing page | www.microsoft.com/en-us/microsoft-365/onedrive/document-scanning | 200, but a bot-block shell, so not a source | unchanged claim, `checked_on` stays 2026-09-14 (UNVERIFIABLE) |

#### A. Round-1 corrections, checked again at 0e8c6a84
| # | Correction | Verdict | Evidence |
|---|---|---|---|
| R1 | backup zh-TW block 14 → 「打開檔案總管，找到檔案原本所在的資料夾，按右鍵選「還原先前版本」」 | CONFIRMED | MS zh-tw: 「打開檔案總管，然後導航到原本包含該檔案或資料夾的資料夾。右鍵點擊資料夾名稱，然後選擇 還原先前版本」 |
| R2 | backup en block 14 → "Open File Explorer, go to the folder where the file used to be, right-click it and select Restore previous versions" | CONFIRMED | MS en-au: "Open File Explorer and navigate to the folder that used to contain the file or folder. Right-click on the folder name, and then select Restore previous versions." |
| R3 | backup ja block 14 → 「エクスプローラーで、…右クリックして［以前のバージョンの復元］」 | CONFIRMED | MS ja-jp: 「エクスプローラーを開き、…フォルダーに移動します。フォルダー名を右クリックし、[以前のバージョンの 復元] を選択します」 |
| R4 | backup ko block 14 → 「파일 탐색기에서 … 마우스 오른쪽 단추로 클릭하고 ‘이전 버전 복원’」 | CONFIRMED | MS ko-kr: 「파일 탐색기 열고 … 폴더 이름을 마우스 오른쪽 단추로 클릭한 다음 이전 버전 복원을 선택합니다」 |
| R5 | backup zh-CN block 14 → 「打开文件资源管理器，…右键单击并选择“还原以前的版本”」 | CONFIRMED | MS zh-cn: 「打开文件资源管理器并导航到用于包含文件或文件夹的文件夹。右键单击文件夹名称，然后选择“还原以前的版本”」 |
| R6 | backup sources[0]/[1] in all 5 locales → post-redirect URLs | CONFIRMED | Both old URLs return 301 to exactly the new URLs, and both new URLs return 200 with the real article. No old URL is left anywhere in the pack (grep count 0). |
| R7 | digital-receipt en block 11 "Date_Item_Seller" → "Date_Product_Seller" | CONFIRMED | Matches en block 6 table row 1. Pattern counts across the pack: Date_Product_Seller ×2, 日期_商品_店家 ×4 (zh-TW + zh-CN), 日付_商品_購入店 ×2, 날짜_상품_판매처 ×2. |
| R8 | file-naming en block 14 "Anyone else with a view" → "Anyone else who has an opinion" | CONFIRMED | Matches zh-TW 「其他人有意見就留言」, ja 「意見があれば」, ko 「의견이 있으면」 and zh-CN 「有意见就留言」. |

A grep of the head packs finds no leftover pre-fix wording: no "In File History", 「在檔案歷程記錄裡」, 「ファイル履歴では」, 「파일 히스토리에서는」, 「在文件历史记录中」, "Date_Item_Seller" or "with a view". Each fix sentence is otherwise unchanged, so the rest of block 14 (yesterday's version, preview, Restore to…, the irreversible-replace warning, recovery drive) still holds; see B3–B8.

#### B. Other changed claims (all new-section claims checked; all CONFIRMED)
##### backup-and-restore-home-files (blocks 11–15)
1. File History automatically backs up Documents, Pictures, Videos and Desktop plus libraries. Source: "automatically backs up all your libraries"; "automatically backs up essential folders like Documents, Pictures, Videos, and Desktop".
2. Folders elsewhere must be added to a library. Source: "add them to an existing library or create a new library"; "Include in library".
3. Deleted today → choose yesterday's folder version. Confirmed in all 5 MS locales.
4. Preview before restoring. Source: expand Open → Open in File History.
5. Expand Restore → Restore to… another location.
6. A plain restore replaces the current version and cannot be undone (Warning box, all locales).
7. The recovery drive does not include personal files. Source: "The Recovery Drive doesn't include your personal files".
8. Restore points and the recovery drive handle system state (System Protection / System Restore / Recovery Drive sections).
9. Table row 3: backups go to an external drive or network location.
10. UI names. zh-TW 檔案歷程記錄 matches the MS zh-tw page title 「使用 [檔案歷程記錄] 備份與還原」. ko 파일 히스토리 matches the MS ko-kr title 「파일 히스토리를 사용하여 백업 및 복원」. ja ファイル履歴, zh-CN 文件历史记录, 还原以前的版本 and 还原到 also match.

##### browser-bookmark-project-folders (blocks 11–15)
11. More > Bookmarks and lists > Show all bookmarks opens the side panel.
12. Organize icon → Sort by last opened. Localized labels match the help pages: zh-Hant 「整理」/按「上次開啟時間」排序; zh-Hans 整理/按上次打开时间排序; ja 管理アイコン/最後に開いた日付で並べ替え; ko 구성/최근 연 날짜순으로 정렬. 書籤和清單/顯示所有書籤, 书签和清单/显示所有书签, ブックマークとリスト/すべてのブックマークを表示 and 북마크 및 목록/모든 북마크 표시 also match.
13. A deleted bookmark cannot be recovered: "After you delete a bookmark, you can't get it back"; zh-Hant 「刪除書籤後就無法還原」; zh-Hans 「书签一经删除，便无法恢复」.
14. @bookmarks, then Tab or Space, then keywords.
15. Same Google Account on all devices: "When you sign in to Chrome with your Google Account, you can use bookmarks … on all your devices".

##### desk-cable-charging-organization (blocks 8–12)
16. Certified USB-C to USB-C cables must carry a 60W or 240W power logo.
17. Every cable except High-Speed USB (USB 2.0) must also show its data rate.
18. Example: the Combined Performance and Power 20Gbps/60W logo.
19. A certified cable with a power logo only is USB 2.0 class. This follows from 17: USB 2.0 cables are "required to have the power icon", and the speed logo is optional for them.
20. One non-USB end or a fixed cable puts it outside certification. Source: "Captive cables are not eligible … one USB connector and is either permanently attached or has a non-USB connector".
21. A certified cable does not raise a device's capability. Source: "nor does it augment the capabilities of those products".

##### digital-receipt-archive (blocks 8–12, 15)
22. Choose Document mode when scanning. Localized names match: 文件 / ドキュメント / 문서 / 文档.
23. Done → enter a file name → Save (en; ko 「완료를 탭하고 파일 이름을 입력한 다음 저장」).
24. Files are saved as PDF automatically (all 5 locales).
25. Multi-page scanning holds at most 10 pages. Source: "The maximum number of pages/images that can be multi-page scanned is 10" (also confirmed in zh-tw, ja-jp, ko-kr and zh-cn).
26. Callout change 本文 → 這套做法 is wording only.

##### email-triage-three-actions (blocks 11–15)
27. Archived mail stays in All Mail. Localized: 所有郵件 / 所有邮件 / すべてのメール / 전체보관함.
28. Muted conversations: replies skip the inbox and go to the archive. Localized: 略過 / 忽略 / ミュート / 알림 끄기 (ko step: 「더보기 알림 끄기」).
29. "If someone replies to a message you archive, it returns to your inbox" (en, ja, ko).
30. Trash is deleted automatically after 30 days. zh-Hans uses 已删除邮件, which matches the zh-CN text.
31. Snooze. Localized: 延後 / 延后 / スヌーズ / 다시 알림.
32. is:muted finds muted threads.
33. "Search by sender, select all, archive": the page describes multi-select. No numeric claim.

##### file-naming-system-for-home (blocks 3 and 11–15)
34. List view plus sort by name puts similar names together. Source: "Sort files by name and ensure you're in the list view".
35. The search bar can find suspected duplicates.
36. "If you delete a shortcut, the original file is not deleted."
37. Without move permission, "A shortcut is created in the destination folder instead."
38. Folder colors: "it only applies to your version of Drive".
39. Items can be restored from the trash.
40. Block 3 「重新命名」 → 「命名」 (en "name them clearly"): consistent with the page, which now gives naming-convention advice, not rename steps.
41. Folder and file descriptions exist ("Add or edit descriptions").

##### gadget-purchase-needs-checklist (blocks 11–15)
42. Service manual 10%, replacement parts 10%, design 80%.
43. Manual and parts can be checked on the OEM support site, or through a third party the support site links to.
44. A manual behind registration or a paywall earns no credit (table row 1).
45. "it's not uncommon for 3-6 months to elapse after a device first goes on sale before replacement parts … become available".
46. Parts pairing: genuine parts that need calibration or pairing software.
47. "Studies show that if the cost of repair exceeds about a third of the price of a new product, many people won't bother fixing it." The article attributes this to studies cited by iFixit.
48. Model identifier: iFixit raises missing identifying marks and the settings menu.
49. Software updates: iFixit raises this as a concern. The article does not claim it is scored (see notes).

#### C. Per-locale review (en/ja/ko/zh-CN against zh-TW, new sections of all 7 slugs)
I read every new heading, paragraph, table and caption. No meaning drift and no number mismatch. UI names follow each language's official help page (B10, B12, B22, B27–B31). The ko speech level matches each article's base text: email-triage stays in 해라체, the others in 합니다체.

#### D. Reader-first
In zh-TW and zh-CN, 本文 appears 0 times and 這篇/这篇 at most once per pack. The PR's 本文 → 這裡 replacements bring every pack under the limit. The new sections contain no verification narration.

#### E. Suspected but not changed (no error)
- gadget table rows 「軟體與安全更新」 and 「送修方式」 are not part of iFixit's current scorecard: software updates are "not yet integrated into our scorecard". Block 12 only says to add these rows when comparing candidates and does not claim they are scored, so this is not a factual error.
- desk-cable ja and ko block 12 render 「一直沒用到」 as "never used once" (一度も使わなかった / 한 번도 쓰지 않은). The nuance is negligible.
- backup en block 14 says "choose Restore to a different location", while the MS label is "Restore to…". zh-TW has the same structure (「還原到」另一個位置), so this is not an error.

#### F. Not done
- I did not run the mechanical self-checks (ingest dry-run, intake_check): there is no venv in the detached main clone, and this round is read-only. All 7 packs load as valid JSON.
- The OneDrive marketing page is unverifiable (bot-block shell). The PR did not change the claim it backs.
