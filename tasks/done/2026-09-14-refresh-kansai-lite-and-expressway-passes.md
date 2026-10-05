---
id: 2026-09-14-refresh-kansai-lite-and-expressway-passes
title: 十月起 KANSAI RAILWAY PASS LITE 與 TEP、KEP 高速周遊券的新版本要回填三篇文章
status: done
priority: P2
area: docs
owner: claude-opus-5-5-kansai-passes
claimed_at: 2026-10-05T06:37:30Z
created_at: 2026-09-14T00:49:22Z
completed_at: 2026-10-05T07:15:08Z
branch: claude/kansai-passes
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

- [x] 三篇文章寫的是「修改當天」官網上的版本：票價、發售與使用期間、範圍，`sources` 的 `checked_on` 更新；
      沒有續辦的就明寫停止，不要留舊價。
- [x] 兩張 SVG 圖解的底註跟正文一致，圖上每個數字仍出現在正文。
- [ ] 正式站跑過 `guides-import --dry-run` 與 `--publish`，三篇的更新日期是新的。
      （publish after merge (coordinator, owner consent)）

## Steps

- [x] 十月第一週查官網：`https://www.surutto.com/kansai_rwpl/en/krp.html`、
      `https://www.driveplaza.com/etc/drawari/tohoku_expass/`、`https://global.w-nexco.co.jp/en/kep/`、
      NEXCO 東日本 HEP 頁。
- [x] 改內容包 JSON 與圖解；跑 `cd apps/api && uv run pytest tests/test_guides_content_pack.py -q`。
- [ ] 合併、部署後在正式站匯入。（publish after merge (coordinator, owner consent)）

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

### 2026-10-05 查證與改寫（claude-opus-5-5-kansai-passes，分支 claude/kansai-passes）

全部用 `curl -sSL` 與編輯 UA 抓，先剝 `<!-- -->` 再讀，HTTP 都是 200。

- **LITE 已續辦**（surutto.com krp.html）：2026 年 10 月版 2 日 5,200、3 日 6,500 日圓（同價），發售 2026-10-01 到
  2027-03-31，購買日起 3 個月有效、最晚 2027-03-31 啟用，2 日券用到 2027-04-01、3 日券 2027-04-02，天數連續。
  販售平台多了 Trip.com（Klook、KKday、WAUG、Trip.com 四家）；除外範圍不變。兩篇與 `kansai-rail-passes-guide`
  的圖解（`<desc>`、賣點行、底註）都改了，`checked_on` 換成 2026-10-05。中文版 `kansai_rwpl/tc/krp.html` 是 404，只有英文頁。
- **TEP 沒有續辦公告**：ドラぷら日文頁仍寫「2026年9月30日ご利用開始分まで受付中」，英文、繁中頁同（Last-Modified
  2026-10-02）；`/cms/news/etc.xml` 沒有 TEP 的新聞；利用約款第 6 條說期限在官網公告。照 DoD「不要留舊價」，文章拿掉
  TEP 票價，改寫「受理只到 2026 年 9 月 30 日開始使用的行程，之後的版本與票價都還沒公布」，H3 改成「目前都申請不到」，
  圖解底註同。周遊範圍（東北六縣、不含新潟）用官網的 `img_map_jp.gif` 對過。
- **KEP 照常販售，但規約沒換新**：global 站英文、繁中頁價格不變（2 天 6,200 到 10 天 23,800），掛的仍是
  `UserAgreement2410e.pdf`（2025-03-23 修訂，第 6 條有效期間到 2026-09-30）。兩個官方說法並存，文章保留價格並加一句
  「10 月以後的行程預約時先向租車公司確認能不能套用」。受理名單變了：Nippon 也標「Currently not accepted」
  （Toyota、Budget、ORIX、Nippon 不受理；Times、Nissan 與 NICONICO、SKY、SUZUKI 等九家受理），文章原本叫讀者訂 Nippon，已改。
- **HEP 不變**：普通車 4 天 7,700 到 8 天 15,400、輕自動車 6,200 到 12,300；頁面沒寫受理期限；取扱店舗名單仍有 Toyota、
  ORIX、Nippon、Nissan、Budget、Times。**CEP** 仍是「We have closed our new bookings」。
- 圖解用 `pack_ingest.render_svg`（Edge）轉 PNG 看過，沒有超框或壓線。
- 留下的事拆成兩張票：`2026-10-05-tep-kep-renewal-recheck`（TEP 續辦或 KEP 換規約時回填）、
  `2026-10-05-itinerary-usj-september-hours`（四天行程的環球影城營業時間與票價寫死 9 月，不在本票範圍）。
- 正式站匯入（DoD 第三項、Steps 第三項）沒做：publish after merge (coordinator, owner consent)。三篇只有 zh-TW，
  repo 裡沒有其他語系；正式站若有 article-localization 的譯本，要另外重譯。
