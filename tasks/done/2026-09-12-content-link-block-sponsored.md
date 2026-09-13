---
id: 2026-09-12-content-link-block-sponsored
title: 文章內文 link 區塊缺 rel=sponsored 與追蹤參數過濾
status: done
priority: P3
area: web
owner: claude-opus-5
claimed_at: 2026-09-13T05:06:13Z
created_at: 2026-09-12T14:18:00Z
completed_at: 2026-09-13T09:37:18Z
branch: claude/claude-tutorial-affiliate-links-084ff0
depends_on: []
scope:
  - apps/api/app/site_pages/service.py
  - apps/api/app/i18n.py
  - apps/api/tests/test_site_pages.py
  - apps/web/components/content-blocks.tsx
  - apps/web/components/content-blocks.test.tsx
---

# 文章內文 link 區塊缺 rel=sponsored 與追蹤參數過濾

## Why

文章與法律頁共用的 `link` 內文區塊只擋 scheme（http／https／mailto）與控制字元
（`apps/api/app/site_pages/schemas.py` `LinkBlock.safe_link`、`apps/web/lib/content-blocks.ts`
`contentBlockLink`），對主機與查詢參數完全不管；渲染時只有 `rel="noopener noreferrer"`
（`apps/web/components/content-blocks.tsx`）。編輯把 Klook／Agoda 的追蹤網址貼進內文，會變成
一條未揭露、未追蹤（沒有 `affiliate_clicks`）、沒有 `sponsored`／`nofollow` 的分潤連結——
`docs/travel-services.md` 「Ordinary links … never show an affiliate disclosure by themselves」的反面。
生活分享專區上線後，編輯貼外站連結的機率會明顯提高。

## Definition of done

- [x] 帶已知分潤參數或短網址的連結存不進去，後台看得到清楚的錯誤訊息（`422 content_link_affiliate`，
      訊息指出是哪個參數或網域，並請編輯改用「合作夥伴連結」區塊）。文章的 `link`、資料來源、圖片出處，
      以及法律頁的 `link` 都擋。**擋在寫入路徑，不在 `LinkBlock` 模型**，原因見 Notes。
- [x] 外站連結的 `rel`：一般編輯連結維持 `noopener noreferrer`、不加 `nofollow`（見 Notes 的決定）；
      分潤連結改由 `partner_link` 區塊畫成 `rel="sponsored noopener"`，站內連結不受影響。
- [x] 後台預覽與公開頁走同一個渲染器；渲染器只把 `link` 區塊畫成連結，不認得的區塊不再掉進 link 分支。

## Steps

- [x] API：`app/site_pages/service.py` 的 `_write_revision` 呼叫 `_refuse_affiliate_links`，
      `app/i18n.py` 的 `_SITE_PAGE_ERRORS` 補五語；文章那一半在 `app/guides/admin_service.py` 的 `_validate_document`。
- [x] 測試：`tests/test_site_pages.py` 的 `test_a_tracked_link_cannot_be_saved_or_published`；
      文章的四條寫入路徑在 `tests/test_guide_partner_links.py`。
- [x] Web：`components/content-blocks.tsx` 只畫 `link` 區塊；`content-blocks.test.tsx` 加未知區塊不畫成連結。
- [x] 文件：`docs/travel-guides.md`（Storage、reader's side、Still open）與 `docs/affiliate-configuration.md` §8。

## How to verify

```bash
cd apps/api && uv run pytest tests/test_site_pages.py tests/test_guide_partner_links.py -q
cd apps/web && npx vitest run components/content-blocks
```

## Notes

- 這是規劃生活分享專區時的反駁代理找出的既有缺口，不是新功能造成的。
- 2026-09-13 與 `2026-09-13-content-partner-links-in-articles-non` 同一個 PR 做完（claude-opus-5）。
- **為什麼不放在 `LinkBlock`**：公開讀取（`guides/service.py`、`site_pages/service.py`）與後台明細每次都用模型重新驗證已存的版本。
  規則放進模型，日後清單每多一個參數，舊版本就可能變成 500，而且編輯連打開來修都不行。
  放在寫入路徑，舊草稿仍然讀得到，只是不能再發布，直到把連結換掉。
- **辨識規則**在 `app/affiliates/content_links.py` 的 `affiliate_marker`，分三層：
  - 任何網域都擋的分潤參數：`marker`、`trs`、`aff`、`aff_id`、`affiliate_id`、`sub_id`、`clickid`、`irclickid`、`cjevent`、`awc`…
  - 只在商家網域才擋的參數（旅遊品牌、合作夥伴、Amazon）：`aid`、`cid`、`sid`、`tag`、`allianceid`、`utm_source`。
    新聞網站的 `?aid=` 是文章編號。
  - 追蹤轉址與短網址網域：`tp.st`、`tp.media`、`awin1.com`、`bit.ly`、`reurl.cc`…
  `untracked_url` 的 13 個參數全部涵蓋，有測試逐一核對。
- **rel 的決定**（計畫核准時的預設，站主可改）：一般編輯連結不加 `nofollow`。分潤網址在存檔時就被擋，
  剩下的都是編輯引用，Google 不要求標註。要改就是 `content-blocks.tsx` 一行。
