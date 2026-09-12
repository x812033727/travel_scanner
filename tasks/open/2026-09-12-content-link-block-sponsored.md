---
id: 2026-09-12-content-link-block-sponsored
title: 文章內文 link 區塊缺 rel=sponsored 與追蹤參數過濾
status: open
priority: P3
area: web
owner:
claimed_at:
created_at: 2026-09-12T14:18:00Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/site_pages/schemas.py
  - apps/api/tests/test_site_pages.py
  - apps/web/lib/content-blocks.ts
  - apps/web/lib/content-blocks.test.ts
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

- [ ] `LinkBlock` 拒絕帶已知分潤參數（`marker`、`trs`、`aid`、`cid`、`aff`、`affiliate_id`、`aff_id`；
      參考 `apps/api/app/travel_services/schemas.py` 的 `untracked_url`）的網址，並在後台給出清楚的錯誤訊息。
- [ ] 渲染的外站連結加 `rel="nofollow noopener noreferrer"`（或依站主決定 `sponsored`），站內連結不受影響。
- [ ] 後台預覽與公開頁走同一個渲染器，行為一致。

## Steps

- [ ] API 驗證＋測試（`tests/test_site_pages.py`、`tests/test_guides.py` 現有形狀）。
- [ ] web sanitizer 對齊＋渲染器 `rel`；`content-blocks.test.tsx`。
- [ ] `docs/affiliate-configuration.md` §9 更新。

## How to verify

```bash
cd apps/api && uv run pytest tests/test_site_pages.py tests/test_guides.py -q
cd apps/web && npx vitest run lib/content-blocks components/content-blocks
```

## Notes

- 這是規劃生活分享專區時的反駁代理找出的既有缺口，不是新功能造成的。
- `nofollow` 與 `sponsored` 的取捨要站主決定；Google 兩者都接受。
