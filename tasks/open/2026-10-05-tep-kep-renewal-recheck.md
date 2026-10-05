---
id: 2026-10-05-tep-kep-renewal-recheck
title: 東北 TEP 續辦或九州 KEP 換新使用規約時，回填日本自駕文章
status: open
priority: P3
area: docs
owner:
claimed_at:
created_at: 2026-10-05T07:03:47Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/guides/content/japan-car-rental-expressway-guide.json
  - apps/web/public/guides/japan-car-rental-expressway-guide/diagram-1.svg
---

# 東北 TEP 續辦或九州 KEP 換新使用規約時，回填日本自駕文章

## Why

`japan-car-rental-expressway-guide` 在 2026-10-05 依官網改寫了三張高速公路周遊券（票 `2026-09-14-refresh-kansai-lite-and-expressway-passes`）。
那天兩張券的官方狀態還沒定下來，文章只能照實寫「未公布」：

- 東北 TEP（NEXCO 東日本 ドラぷら，日文、英文、繁中三頁）仍寫「2026年9月30日ご利用開始分まで受付中」，頁面 Last-Modified
  是 2026-10-02，`/cms/news/etc.xml` 也沒有續辦公告。利用約款第 6 條說期限「当社ホームページにてお知らせします」。
  文章因此拿掉 TEP 的票價，改寫「受理只到 2026 年 9 月 30 日開始使用的行程，之後的版本與票價都還沒公布」，圖解底註同。
- 九州 KEP（NEXCO 西日本 global 站）照常列價格與受理的租車公司，但掛出的使用規約 `UserAgreement2410e.pdf`
  （2025 年 3 月 23 日修訂，Last-Modified 2025-03-07）第 6 條有效期間只到 2026-09-30，沒有新版。文章保留價格，
  加一句「10 月以後的行程預約時先向租車公司確認能不能套用」。

NEXCO 一公布 TEP 的續辦（或正式停辦）、或 KEP 換上新版規約，這兩句就會變成過期資訊。

## Definition of done

- [ ] 文章的 TEP 段落寫的是當天官網的狀態：續辦就寫回受理期間與普通車、輕自動車票價；正式停辦就寫停辦。
- [ ] KEP 段落的規約有效期間跟官網當天掛的規約一致，不再要讀者自己去問。
- [ ] 圖解底註與 `<desc>`（＝ `image.description`）跟正文一致，圖上每個數字都在正文；`sources` 的 `checked_on` 是查的那天。
- [ ] 合併後由協調者在站主同意下跑 `guides-import --slug japan-car-rental-expressway-guide`（dry-run 再 publish）。

## Steps

- [ ] 用編輯 UA `curl -sSL` 讀 `https://www.driveplaza.com/etc/drawari/tohoku_expass/`（看「受付中」那行與料金表）、
      `https://www.driveplaza.com/cms/news/etc.xml`、`https://global.w-nexco.co.jp/en/kep/`（規約 PDF 的連結檔名）與新規約第 6 條。
- [ ] 改內容包與圖解；`cd apps/api && PYTHONUTF8=1 uv run python -m app.guides.pack_cli lint --slug japan-car-rental-expressway-guide`、
      `PYTHONUTF8=1 uv run pytest tests/test_guides_content_pack.py -q`。
- [ ] 圖解用 `pack_ingest.render_svg` 轉 PNG 看過。

## How to verify

```bash
cd apps/api
PYTHONUTF8=1 uv run python -m app.guides.pack_cli lint --slug japan-car-rental-expressway-guide   # 0 errors
PYTHONUTF8=1 uv run pytest tests/test_guides_content_pack.py -q
grep -n "TEP\|KEP" app/guides/content/japan-car-rental-expressway-guide.json   # 期間與官網一致
```

## Notes

- 拆自 `2026-09-14-refresh-kansai-lite-and-expressway-passes`（2026-10-05 結案）。
- 最後一次看到的 TEP 價格（官網 2026-10-05 仍列）：普通車 4 天 8,500、5 天 10,600、6 天 12,800、7 天 14,900、8 天 17,000 日圓；
  輕自動車 4 天 6,800、5 天 8,500、6 天 10,200、7 天 11,900、8 天 13,600 日圓。續辦時以當天官網為準，不要直接抄這裡。
- KEP 2026-10-05 的受理名單：Toyota、Budget、ORIX、Nippon 標「Currently not accepted」；Times、Nissan 與 NICONICO、SKY、SUZUKI 等九家受理。
- 前一年的模式（2025 年）沒查到：要是 NEXCO 每年十月才補公告，這張票可以等到 11 月再看。
