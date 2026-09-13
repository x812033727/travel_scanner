---
id: 2026-09-13-hide-guide-published-and-valid-until
title: 前台不再顯示情報攻略的發布日期與適用期限
status: review
priority: P2
area: web
owner: claude-opus-5
claimed_at: 2026-09-13T09:20:08Z
created_at: 2026-09-13T09:19:15Z
completed_at:
branch: claude/charming-hopper-m0vhru
depends_on: []
scope:
  - apps/web/components/guides
  - apps/web/app/[locale]/guides
  - apps/web/app/[locale]/life
  - apps/web/messages/en/common.json
  - apps/web/messages/en/metadata.json
  - apps/web/messages/ja/common.json
  - apps/web/messages/ja/metadata.json
  - apps/web/messages/ko/common.json
  - apps/web/messages/ko/metadata.json
  - apps/web/messages/zh-TW/common.json
  - apps/web/messages/zh-TW/metadata.json
  - apps/web/messages/zh-CN/common.json
  - apps/web/messages/zh-CN/metadata.json
  - docs/travel-guides.md
---

# 前台不再顯示情報攻略的發布日期與適用期限

## Why

情報攻略的卡片與文章頁都把日期擺在讀者面前：卡片印「發布日期」與「適用至」，文章頁的
頁首印「發布日期」，過期的情報還會多一條「這則情報已經過了適用期限，內容可能不再正確」
的橫幅。擁有者的決定是這些都不給讀者看——一篇還正確的攻略不該被發布日期看成舊文，而
過期的情報本來就已經離開列表與 sitemap，不必再在頁面上自我否定。

`published_at` 與 `valid_until` 仍然是編輯與營運欄位：它們決定什麼東西上列表、sitemap
帶什麼、`Article` JSON-LD 報什麼，也決定過期的情報不掛合作按鈕。這張票只動前台看得到的
部分，後台編輯器、結構化資料與 sitemap 都不變。

## Definition of done

- [x] 列表卡片（/guides、/guides/[kind]、/life、延伸閱讀）不顯示發布日期、適用至與
      「已過期」標籤。
- [x] 文章頁不顯示發布日期，也不顯示過期橫幅；更新日期與閱讀時間照舊。
- [x] 五個語系的 `common.json` 不再留下這四個用不到的字串，後台複寫面板也就看不到它們。
- [x] 承諾「標明適用期限」的行銷文案跟著改，頁面沒有做的事不要寫在 meta description 裡。
- [x] `docs/travel-guides.md` 說明現在的規則，下一個人不會把橫幅加回去。

## Steps

- [x] `components/guides/card.tsx`：拿掉日期列與過期標籤，`GuideCardLabels` 縮成每個專區
      一個名字。
- [x] `components/guides/article.tsx`：頁首只留更新日期與閱讀時間（兩者都沒有就整列不畫），
      刪掉 `role="status"` 的過期橫幅；`state.expired` 仍然用來擋合作按鈕。
- [x] `components/guides/article-page.tsx` 與三個列表頁不再把這些 label 傳下去。
- [x] 五個語系刪掉 `guides.published`、`guides.validUntil`、`guides.expired`、
      `guides.expiredNotice`，並改寫 `guides.intelLead` 與 `metadata.guidesDescription`。
- [x] 測試改成守住「看不到」：文章頁沒有任何 `<time>`、過期情報沒有 `role="status"`
      也看不到 `valid_until`。

## How to verify

```bash
npm run lint:web && npm run check:i18n && npm run typecheck:web && npm run test:web
npm run check:tasks && npm run test:tools
```

畫面上：`/zh-TW/guides` 的卡片只剩專區、城市、標題、描述與主題；一篇已過期的情報
（`valid_until` 已過）打開後仍然是正常文章，沒有橫幅、沒有日期，也沒有合作按鈕。

## Notes

- 移除語言檔的鍵是安全的：`applyUiTextOverrides` 對沒有預設值的覆寫回報
  `missing_default` 並略過，所以資料庫裡若留著舊的後台複寫，只會被忽略。
- 文章頁仍算出 `published`，但只拿來跟 `modified_at` 比大小——沒有改版的文章
  `modified_at` 等於發布時間，直接畫出來會變成假的「更新日期」。
- `apps/web/app/[locale]/guides/[kind]/[slug]/page.test.tsx` 原本有一條
  「keeps its page and says what date it applied until」，已改成守住相反的行為。
- `lib/guides.ts` 的 `isExpired` 現在只剩自己的測試在用（卡片本來是唯一的使用者）。沒有
  刪，因為它不在這張票的 scope，而且 API 已經直接給 `expired`，要不要留是下一個動
  `lib/guides.ts` 的人可以順手決定的事。
- 沒有動 JSON-LD 的 `datePublished`／`dateModified`、sitemap 的 `lastmod` 與後台編輯器的
  「適用至」欄位；這是擁有者確認過的範圍（前台文章頁＋列表卡片）。
