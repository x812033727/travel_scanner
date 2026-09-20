---
id: 2026-09-20-chiang-mai-3-day-unsourced-claims
title: chiang-mai-3-day-itinerary：blocks[2] 兩句沒有官方來源、blocks[9]「門口租沙龍」要照觀光局改寫
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-09-20T03:12:47Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/guides/content/chiang-mai-3-day-itinerary.json
---

# chiang-mai-3-day-itinerary：blocks[2] 兩句沒有官方來源、blocks[9]「門口租沙龍」要照觀光局改寫

## Why

`chiang-mai-3-day-itinerary` 有三句話沒有官方依據，或已經有更好的官方數字可寫（2026-09-20 打開 zh-TW 內容包逐句確認，全篇 30 個區塊）。

1. `blocks[2]`：「用 Grab 就照 app 指示走到指定上車點，**價格與櫃台計程車差不多**，深夜與雨天加價」——後半段沒有任何官方來源。
   Grab 官網 https://www.grab.com/th/en/transport/ 只寫「Upfront pricing…before you book」（上車前就看到價格），沒有和機場計程車比較過。
2. `blocks[2]`：「清邁國際機場（CNX）就在古城西南邊，離塔佩門**只有幾公里**，不塞車十來分鐘就到」——現在查得到官方數字：
   泰國觀光局東京辦事處塔佩門頁 https://www.thailandtravel.or.jp/tha-phae-gate/ アクセス「チェンマイ国際空港から車で約15分。」
3. `blocks[9]`：「進寺要遮肩過膝、脫鞋進殿，短褲短裙的人**可以在門口租沙龍圍上**」——無官方依據的肯定句，而且和第八批第 14 篇
   `thailand-temple-etiquette-dress-code` 的 warning callout 互相矛盾。泰國觀光局 https://www.thailandtravel.or.jp/visiting-temples/ 寫的是
   「場所によっては腰巻などを有料で借りられる場合もありますが、不適切な服装では入場を断られることもございます。」

## Definition of done

- [ ] `blocks[2]` 的 Grab 那半句拿掉或改寫成官網說法（上車前就看到價格），不留「和櫃台計程車差不多」。
- [ ] `blocks[2]` 的「離塔佩門只有幾公里，不塞車十來分鐘就到」改成有出處的「機場到塔佩門車程約 15 分（泰國觀光局）」。
- [ ] `blocks[9]` 的「短褲短裙的人可以在門口租沙龍圍上」改成「有些寺廟可以付費租腰布，不是每一座都有」。
- [ ] `blocks[2]` 的 40／60 泰銖、12 號門、06:00 到 23:30，以及 `blocks[9]` 第二段的市集時段與「從古城搭雙條車約 10 分鐘」**一個字都沒動**（那幾組是第八批第 10、11 篇要一字不差的共用事實）。
- [ ] `sources` 補 Grab 官網、TAT 塔佩門頁與 TAT 參拜寺廟頁。
- [ ] lint 與內容包測試綠；部署後 `guides-import --slug chiang-mai-3-day-itinerary` 是 `update` 再 `--publish`。

## Steps

- [ ] `blocks[2]`：兩句一次改完（Grab 與「幾公里」），其餘數字不動。
- [ ] `blocks[9]`：第一段結尾那句改寫；第二段（三個市集）原文一字不改。
- [ ] 確認 `blocks[7]`（image）的 `alt`／`description` 與 `apps/web/public/guides/chiang-mai-3-day-itinerary/diagram-1.svg` 沒有這三句話（2026-09-20 兩處都確認過沒有），所以圖與圖說不用改。
- [ ] lint、pytest、PR；部署後匯入。

## How to verify

```bash
cd apps/api
uv run python -m app.guides.pack_cli lint --kind howto
uv run pytest tests/test_guides_content_pack.py -q
```

部署後在主機上（站主同意後）：

```bash
uv run python -m app.cli guides-import --slug chiang-mai-3-day-itinerary --dry-run   # 計畫應該只有這幾篇的 zh-TW 是 update
uv run python -m app.cli guides-import --slug chiang-mai-3-day-itinerary --publish
uv run python -m app.cli guides-links-check --locale zh-TW
```

## Notes

- 來源：審查記錄 `plan8/review/review-thailand-a.md` C3 第 4–6 列（彙整在 `docs/travel-guides-batch-8/FOLLOWUPS.md` 第 3 節），由第八批第 10、11、14 篇的規格審查帶出。
- ⚠️ `blocks[9]` 那一句的改寫**也寫在「既有文章補連第八批」票的合併編輯裡**：規格 #11 與 #14 要求把 `blocks[9]` 整塊改成 `rich_paragraph`、插兩個 inline，並在同一次把這句改掉。**哪一張票先做就在那張做完**，另一張把該項打勾並註明；兩張票 scope 重疊、不能同時 claim。
- `blocks[26]`（只含 `thailand-entry-2026-tdac` inline 的 rich_paragraph，2027-01-01 整塊刪）與 `blocks[29]` 的 `foods?city=chiang-mai`（不是錯）都**不在**這張票。
- 「柴迪隆寺」那個譯名問題在另一篇（`chiang-mai-old-city-slow-day`），票 `2026-09-20-chiang-mai-old-city-chedi-luang`；本篇正文與 `blocks[7]` 已經寫「契迪龍寺」，不用改。
