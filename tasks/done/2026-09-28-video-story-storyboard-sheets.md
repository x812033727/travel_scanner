---
id: 2026-09-28-video-story-storyboard-sheets
title: 超過 47 鏡的分鏡送審改送聯絡表
status: done
priority: P1
area: tools
owner: claude-opus-5-5-video-story-review
claimed_at: 2026-09-28T05:41:03Z
created_at: 2026-09-28T03:31:11Z
completed_at: 2026-09-28T06:36:12Z
branch: claude/video-story-storyboard-sheets
depends_on:
  - 2026-09-28-video-story-design-docs
scope:
  - tools/video/review/sync.mjs
  - tools/video/review/sync.test.mjs
---

# 超過 47 鏡的分鏡送審改送聯絡表

## Why

一支品牌故事有 85–100 個鏡頭（`docs/videos/STORY.md`）。分鏡關卡送審時，`storyboardSubmission`（`tools/video/review/sync.mjs`）每個鏡頭上傳一個檔，而一筆審核最多 48 個檔（`apps/api/app/video_reviews/schemas.py` 的 `MAX_REVIEW_FILES`）。超過 47 鏡的影片永遠送不出分鏡，整支卡住。

## Definition of done

- [x] 鏡頭數在上限以內時，送審內容與現在完全相同。
- [x] 超過上限時，送審改成：分頁的聯絡表（每頁最多 24 格）加上所有標成待修（`needs_review`）的鏡頭；payload 仍列出每個鏡頭的 id、judge 分數與是否待修，審核卡看得到全貌。（審核卡看不到分頁，見 Notes「後台審核卡」。）
- [x] 95 鏡的測試案例送得出去，檔案數不超過 48。

## Steps

- [x] `sync.mjs`：依鏡頭數選擇送法；聯絡表分頁。（這裡讀 manifest 列的分頁；畫分頁是 `keyframes` 的事，見 Notes。）
- [x] 測試：47 鏡、48 鏡、95 鏡三個案例。（另有 95 鏡單張聯絡表、120 鏡 60 鏡待修、放得下的分頁、只寫檔名的分頁。）
- [x] 確認後台審核卡在缺少單鏡檔案時照常顯示（`apps/web/components/admin-video-review-card.tsx` 已容忍缺檔，這張票不改 web）。

## How to verify

```bash
node --test "tools/video/review/*.test.mjs"
npm run test:tools
```

`node --test tools/video/review`（目錄）在 Node 24 會把目錄當成模組載入，以 MODULE_NOT_FOUND 失敗，要寫成上面的 glob。

## Notes

- 聯絡表由 `keyframes` 階段產生（`drawContactSheet`）；分頁如果要改 `tools/video/media`，另開票，不要擴 scope。
- PR #870 也改了 `sync.mjs`（約 90 行），合併順序誰後誰 rebase。
- **送法**（`storyboardSubmission`）：關鍵影格數加聯絡表張數不超過 `MAX_REVIEW_FILES`（48，對應 `apps/api/app/video_reviews/schemas.py`）時照舊：每一鏡的關鍵影格（`shot_NN`，鏡頭順序），最後是聯絡表。超過時先送聯絡表，再依鏡頭順序送待修的鏡頭，送到 48 個為止；放不下的只留在 payload。改動前後的 `sync.mjs` 對同一個工作目錄送 4、20、46、47 鏡，POST 的內容逐位元組相同；48 鏡起走聯絡表（以前是 48 張關鍵影格、不附聯絡表）。
- **聯絡表從哪裡讀**（給 `keyframes` 分頁的那張票）：`keyframes/manifest.json` 有 `contact_sheets` 時讀它，每一項 `{ file, shots }`：`file` 相對於工作目錄，`shots` 是這一頁的鏡頭 id、依順序。只寫檔名字串也行，這時當作依序每頁 24 鏡（`SHEET_PAGE_SHOTS`），所以寫出 `shots` 比較可靠。沒有 `contact_sheets` 時用 `keyframes/contact-sheet.png` 一張；檔案不在的頁略過。只有一張時 role 是 `contact_sheet`，兩張以上是 `contact_sheet_01`、`contact_sheet_02`…（伺服器 `ReviewFile.role` 是 `^[a-z][A-Za-z0-9_-]{0,39}$`）。
- **payload 合約**（給 worker 與後台的票）：
  - 一律有 `shots: [{ id, chapter, prompt, seconds, file_role, needs_review, judge: { overall, problems } }]`（每個有關鍵影格的鏡頭，依順序；影格沒送上去的 `file_role` 是 `null`）、`judge: { overall: 最低分, problems: 待修鏡頭的問題 }`、`duplicates`。伺服器自動核准分鏡（`storyboard_check_passed`）只讀 `judge` 與 `shots`，行為不變。
  - 不是「每一鏡加最多一張聯絡表」時多兩個鍵：`sheets: [{ role, shots: [id, …] }]`（頁序，`role` 對應 `files`）與 `omitted`（影格沒送上去的鏡頭數）。放得下但有兩頁以上時也有，`omitted` 是 0。
  - 摘要：`分鏡 95 鏡（聯絡表 4 頁），judge 最低 5/10，3 鏡待修`；待修的也放不下時接 `，其中 17 鏡沒附單張圖`；超過上限卻沒有聯絡表時括號寫「沒有聯絡表」。
  - `content_sha256` 仍是 `keyframes/manifest.json` 的雜湊；payload 仍受伺服器 256 KiB（`MAX_PAYLOAD_BYTES`）限制，100 鏡、每鏡 1,000 字英文提示詞約 115 KB。
- **後台審核卡**（`admin-video-review-card.tsx` 的 `StoryboardBody`，只讀沒改）：不會壞。`file_role: null` 的鏡頭照樣列出、只是沒有圖（`fileFor(review, "")` 找不到檔），`sheets`、`omitted` 被忽略，摘要照常顯示；沒分頁的長分鏡那一張 `contact_sheet` 也照常顯示。**看不到的是分頁**：卡片只找 role 為 `contact_sheet` 的檔，`contact_sheet_01`… 不顯示，所以分頁送審時卡上沒有任何聯絡表，也看不出沒附圖的鏡頭在第幾頁。要補的是依 `payload.sheets` 逐頁顯示、沒附圖的鏡頭標出頁數（五語文字）；`video-story-admin` 的 scope 不含這個元件，要另開票或擴那張。
- 與 PR #870：它改 import、`REVIEW_GATES`、`STEP_LABELS`、`nextGate`、final 與 dubs、在 `downloadNote` 後加 `languagesSubmission`、`recordApproval`；這張票只動 `lookSubmissions` 之後到 `storyboardSubmission` 結尾，測試只動 import 那一行與舊分鏡測試之後，彼此不相鄰。#870 在 2026-09-28 06:38Z 合併進 main，這個分支併進已含 #870 的 #888 分支時沒有衝突；合併後分鏡測試重跑全過，4、20、46、47 鏡的送審內容也仍與 #870 版本逐位元組相同。
