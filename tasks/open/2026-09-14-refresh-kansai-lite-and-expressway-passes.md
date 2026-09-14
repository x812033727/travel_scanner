---
id: 2026-09-14-refresh-kansai-lite-and-expressway-passes
title: 十月起 KANSAI RAILWAY PASS LITE 與 TEP、KEP 高速周遊券的新版本要回填三篇文章
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-09-14T00:49:22Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/guides/content/kansai-rail-passes-guide.json
  - apps/api/app/guides/content/osaka-kyoto-nara-4-day-itinerary.json
  - apps/api/app/guides/content/japan-car-rental-expressway-guide.json
  - apps/web/public/guides/kansai-rail-passes-guide/diagram-1.svg
  - apps/web/public/guides/japan-car-rental-expressway-guide/diagram-1.svg
---

# 十月起 KANSAI RAILWAY PASS LITE 與 TEP、KEP 高速周遊券的新版本要回填三篇文章

## Why

三篇文章寫進了 2026-09-30 就到期的票券版本，十月一到內容就會變成過期資訊：

- `kansai-rail-passes-guide`（正文、表格與圖解底註）與 `osaka-kyoto-nara-4-day-itinerary`：KANSAI RAILWAY
  PASS LITE 目前的版本要在 2026-09-30 前啟用，官網還沒公布下一版的票價與期間。
- `japan-car-rental-expressway-guide`（正文與圖解底註）：東北 TEP 受理到 2026-09-30 開始使用的申請、
  九州 KEP 使用規約的有效期間到 2026-09-30，中部 CEP 已停止新預約；HEP 官網沒寫受理期限。

## Definition of done

- [ ] 三篇文章寫的是「修改當天」官網上的版本：票價、發售與使用期間、範圍，`sources` 的 `checked_on` 更新；
      沒有續辦的就明寫停止，不要留舊價。
- [ ] 兩張 SVG 圖解的底註跟正文一致，圖上每個數字仍出現在正文。
- [ ] 正式站跑過 `guides-import --dry-run` 與 `--publish`，三篇的更新日期是新的。

## Steps

- [ ] 十月第一週查官網：`https://www.surutto.com/kansai_rwpl/en/krp.html`、
      `https://www.driveplaza.com/etc/drawari/tohoku_expass/`、`https://global.w-nexco.co.jp/en/kep/`、
      NEXCO 東日本 HEP 頁。
- [ ] 改內容包 JSON 與圖解；跑 `cd apps/api && uv run pytest tests/test_guides_content_pack.py -q`。
- [ ] 合併、部署後在正式站匯入。

## How to verify

```bash
cd apps/api && uv run pytest tests/test_guides_content_pack.py -q
uv run python -m app.cli guides-import --actor-email <admin> --dry-run
```

dry-run 應該只列出這三篇為 updated。

## Notes

- 查到時的數字（2026-09-13）：LITE 2 日 5,200、3 日 6,500 日圓；TEP 普通車 4 天 8,500 到 8 天 17,000；
  KEP 2 天 6,200 到 10 天 23,800；HEP 普通車 4 天 7,700 到 8 天 15,400 日圓。
- KEP 官網當時標示 Toyota、Budget、ORIX 不受理，續辦時一併確認。
