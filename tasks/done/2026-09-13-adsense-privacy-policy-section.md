---
id: 2026-09-13-adsense-privacy-policy-section
title: 隱私權政策加上 AdSense 廣告揭露（五語系）
status: done
priority: P3
area: docs
owner: claude-opus-5
claimed_at: 2026-09-13T08:06:17Z
created_at: 2026-09-13T05:16:04Z
completed_at: 2026-09-13T08:08:41Z
branch: claude/google-adsense-integration-plan-650u03
depends_on:
  - 2026-09-06-legal-content-from-owner
scope:
  - apps/api/app/site_pages/drafts
  - apps/api/tests/test_site_pages_drafts.py
  - docs/privacy-data-map.md
---

# 隱私權政策加上 AdSense 廣告揭露（五語系）

## Why

評估全文在 `docs/adsense-feasibility.md`。AdSense 的計畫政策要求隱私權政策揭露兩件事：
「Google 等第三方供應商使用 cookie，依使用者先前造訪投放廣告」，以及退出管道（Google 廣告設定或
aboutads.info）。現在五語系的 `privacy` 草稿**一句都沒提廣告**（`docs/privacy-data-map.md:291-293`）。
即使只放非個人化廣告，Google 仍會用 cookie 做頻率上限與彙總報表，所以一定要揭露。

**先別動手**：這張票等兩件事。

1. 站主決定評估文件第六節的 D1（非個人化廣告＋DNT／GPC 不載入，還是個人化廣告＋CMP）。
   兩種寫法不同，也不能描述一個不存在的同意橫幅（`privacy-data-map.md:117-120`）。
2. `2026-09-06-legal-content-from-owner` 完成，也就是四個法律頁先照已核准的文字上線。
   不要為了廣告拖住法律頁。

## Definition of done

- [x] 五語系 `privacy` 各多一個同結構的區塊（heading＋paragraph，或 heading＋list），內容：
      第三方（含 Google）用 cookie 投放與衡量廣告；本站採用的是 D1 的哪一種；
      DNT／GPC 時不載入廣告；退出連結 `https://adssettings.google.com` 與 `https://www.aboutads.info`；
      若 D1 選個人化，還要說明同意訊息只對 EEA／英國／瑞士顯示。
- [x] ~~廣告還沒上線前，不要在正式站發布這段文字。~~ 改成條件句後不再需要卡發布時機，見 Notes。
- [x] （站主手動）正式站（`site_pages` 已初始化之後，改 `drafts/*.json` 不會生效，見 `privacy-data-map.md:311-314`）：
      在後台「網站資訊」逐語系貼上、改生效日期、發布；五個語系都要做。
      → 2026-09-13 五語系都已補上並發布，生效日 `2026-09-13`，做法與核對方式見
      `tasks/done/2026-09-06-legal-content-from-owner.md` 的「正式站發布結果」。
- [x] `docs/privacy-data-map.md` 第八節刪掉「全文沒有任何一句提到廣告」這個缺口，第三節補上廣告腳本的載入條件。

## Steps

- [x] 等 D1 的答案，寫進本檔 Notes。
- [x] 改 `apps/api/app/site_pages/drafts/{zh-TW,zh-CN,en,ja,ko}.json`，新區塊放在「Service providers and usage analytics」那段之後。
- [x] `uv run pytest tests/test_site_pages_drafts.py` 通過（`:43-49` 要求五語系結構相同，`:93-100` 的英文字句不能被改掉）。
- [x] （站主）核准文字，再到後台逐語系發布。→ 站主 2026-09-13 核准照草稿發布。

## How to verify

```bash
cd apps/api && uv run pytest tests/test_site_pages_drafts.py -q
```

發布後：`curl -s https://mokaair.com/zh-TW/privacy | grep -c aboutads` 大於 0，其他四個語系也各查一次。

## Notes

- D1 的答案：**只投非個人化廣告，不裝 CMP**；DNT／GPC 時完全不載入廣告。文字照這個寫。
- **解掉了對 `2026-09-06-legal-content-from-owner` 的時序依賴**（`--force` 認領的理由）。
  原本的規定是「廣告上線那天才發布這段文字」，但正式站 `site_pages` 還是空的，站主一旦從草稿
  初始化四個法律頁，這段文字就會跟著上線，描述一件還沒發生的事。
  改法是把措辭寫成條件句——「**當本站在……文章頁顯示 Google 廣告時**，Google 等第三方供應商
  會使用 Cookie……」——這樣在廣告開啟前後都成立，時序衝突消失，法律頁那張 P1 也不會被廣告拖住。
- 區塊用 heading＋paragraph＋list。**不能用 `link` 區塊**：`components/content-blocks.tsx:74-122`
  只渲染 heading／paragraph／list／image／table／callout，`link` 會整個不見。
  退出管道的網址因此是清單裡的純文字，跟頁面上 `support@mokaair.com` 的呈現方式一致。
- 新增 `test_privacy_discloses_advertising_cookies_and_an_opt_out`，五語系都斷言
  兩個退出網址與 DNT／GPC 的說法還在，翻譯漏掉會紅。
- 順手核對 `docs/privacy-data-map.md:72-73`「GA4 啟用時 Google 會設自己的 `_ga*`」那句：
  **這次沒有查證**（要在真的開著 GA4 的環境用瀏覽器看 cookie），所以原文沒有動。
  這件事仍然懸著，跟廣告無關。

- 順手核對一句可能不準的描述：`docs/privacy-data-map.md:72-73` 說「GA4 啟用時 Google 會設自己的 `_ga*`」，
  但 `analytics-provider.tsx:59` 把 `analytics_storage` 設成 denied，照 Consent Mode 的設計，這個狀態下 gtag 不寫 `_ga*`。
  先在開著 GA4 的環境用瀏覽器看一次 cookie，確認了再改文件。
- 法律頁的營運者、所在地、聯絡方式等欄位已由站主定案（`tasks/done/2026-09-12-site-page-requirements.md`），不要重寫。
