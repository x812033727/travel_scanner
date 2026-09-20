---
id: 2026-09-20-chiang-rai-wat-phra-kaew-hours
title: chiang-rai-2-day-itinerary：清萊玉佛寺「沒有官方公告」已過時，觀光局寫 07:00 到 17:00、免費參拜
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
  - apps/api/app/guides/content/chiang-rai-2-day-itinerary.json
---

# chiang-rai-2-day-itinerary：清萊玉佛寺「沒有官方公告」已過時，觀光局寫 07:00 到 17:00、免費參拜

## Why

`chiang-rai-2-day-itinerary` `blocks[17]`（paragraph）最後一句寫
「順路可以加玉佛寺（Wat Phra Kaew）：15 世紀建的寺院，曼谷玉佛寺的翡翠佛曾供奉在這裡；**開放時間與門票沒有官方公告**。」
2026-09-20 打開泰國觀光局東京辦事處的清萊玉佛寺頁 https://www.thailandtravel.or.jp/wat-phra-kaew/ ，可見內容（確認不在 HTML 註解裡）寫著
営業時間「07:00～17:00」、料金「拝観自由」、アクセス「チェンライ市内中心部より車で約20分」——「沒有官方公告」已經過時，
讀者現在看不到本來查得到的開放時間與「免費參拜」。

**抓頁陷阱**：同一個網域的 `wat-phra-kaew` 是**清萊**那座；曼谷大皇宮園區的玉佛寺沒有獨立的 TAT 東京景點頁，不要把這一頁用到曼谷篇。

## Definition of done

- [ ] `blocks[17]` 末句改成「07:00 到 17:00、免費參拜」（可順便補「離市中心車程約 20 分」），不再寫「沒有官方公告」。
- [ ] 同一塊講鐘樓燈光秀的「場次時間沒有官方公告，以現場公告為準」**保留**（那一項確實沒有官方公告）。
- [ ] `sources` 補上 TAT 東京清萊玉佛寺頁（`checked_on` 填實際重讀日）；原本 `sources[0]` 的清萊地區頁不動。
- [ ] 全篇沒有其他地方說玉佛寺沒有公告；圖不用改（`apps/web/public/guides/chiang-rai-2-day-itinerary/diagram-1.svg` 2026-09-20 確認沒有提到玉佛寺）。
- [ ] lint 與內容包測試綠；部署後 `guides-import --slug chiang-rai-2-day-itinerary` 是 `update` 再 `--publish`。

## Steps

- [ ] 重開 https://www.thailandtravel.or.jp/wat-phra-kaew/ 確認三個欄位還在（頁面若改版，以當天讀到的為準）。
- [ ] 改 `blocks[17]` 末句、補 `sources`。
- [ ] lint、pytest、PR；部署後匯入。

## How to verify

```bash
cd apps/api
uv run python -m app.guides.pack_cli lint --kind howto
uv run pytest tests/test_guides_content_pack.py -q
```

部署後在主機上（站主同意後）：

```bash
uv run python -m app.cli guides-import --slug chiang-rai-2-day-itinerary --dry-run   # 計畫應該只有這幾篇的 zh-TW 是 update
uv run python -m app.cli guides-import --slug chiang-rai-2-day-itinerary --publish
uv run python -m app.cli guides-links-check --locale zh-TW
```

## Notes

- 來源：審查記錄 `plan8/review/review-thailand-a.md` C3 第 9 列與第八批第 14 篇規格「口徑衝突另記一筆」（彙整在 `docs/travel-guides-batch-8/FOLLOWUPS.md` 第 3 節）。
- 第八批第 14 篇 `thailand-temple-etiquette-dress-code` 會寫清萊玉佛寺這一組數字，兩篇要一致。
- 白廟（`watrongkhun.org` 現在被別家公司佔著、夾賭場連結）與藍廟的票價**不在**這張票；哪天那個網域恢復成寺方官網，是另一張條件票（FOLLOWUPS 第 1 節第 82 列）。
- scope 與「既有文章補連第八批」重疊：那張票要在 `blocks[31]`（list）與 `blocks[32]`（已是 rich_paragraph）之間**新增**一個 `rich_paragraph` 連第 14 篇。兩張票不能同時 claim；新增區塊會讓 `blocks[32]` 之後位移，所以兩張票都要以當下的檔案內容為準再數一次。
