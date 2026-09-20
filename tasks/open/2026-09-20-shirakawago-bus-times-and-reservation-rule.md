---
id: 2026-09-20-shirakawago-bus-times-and-reservation-rule
title: 白川鄉巴士三個錯：金澤發是座席指定制不是預約優先、所要時間 1 小時 15 分、展望台接駁上行末班 15:40
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-09-20T03:12:40Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/guides/content/takayama-shirakawago-day-trip.json
  - apps/web/public/guides/takayama-shirakawago-day-trip
  - apps/api/app/guides/content/kanazawa-2-day-itinerary.json
---

# 白川鄉巴士三個錯：金澤發是座席指定制不是預約優先、所要時間 1 小時 15 分、展望台接駁上行末班 15:40

## Why

第八批第 4 篇 `kanazawa-shirakawago-day-trip` 的審查（2026-09-20）在既有兩篇裡查到三個讀者看得到的錯，出處都是營運者官網。

**1. `takayama-shirakawago-day-trip` `blocks[23]`（paragraph）的展望台接駁巴士**，現在寫
「接駁巴士乘車處離白川鄉巴士總站約 200 公尺，單程 300 日圓、車上付現金，**9:00 到 16:10** 約每 20 分鐘一班，積雪或視線不良會停駛；走上去單程約 **15 分鐘**」。
官方時刻表是**上行 9:00 到 15:40、下行 9:10 到 16:10，12 點到 13 點之間沒有上行班次**——現文把下行末班當成整條線的末班，
上行末班差了 30 分鐘，讀者會以為 16:00 還上得去展望台。乘車處官方寫「和田家旁」（「約 200 公尺」出自 shirakawa-going.jp，不是官方），步行官方寫「15〜20 分」。
出處（2026-09-20）：白川村役場 https://www.vill.shirakawa.lg.jp/1952.htm （時刻表，12 時與 16 時都只有下行）、
https://www.vill.shirakawa.lg.jp/2696.htm （官方繁體中文版：「乘坐和田家旁的接駁巴士（最後發車時間15:40）」）、
白川鄉觀光協會 https://shirakawa-go.gr.jp/events/441/ （curl 200：「展望台シャトルバスは、通常営業（上り9：00～15：40、下り9：10～16：10）となります。」
「徒歩の場合、見学施設の和田家の裏の遊歩道から15～20分ほどで展望台へ行けます。」）。

**2. `kanazawa-2-day-itinerary` `blocks[55]`（paragraph）整句是**
「白川鄉：從金澤站出發的巴士約 1 小時 20 分，要先預約（**部分直通班次為預約優先**）。」
金澤發的每一班都是座席指定制、**必須**預約，沒有「預約優先」——那是岐阜巴士名古屋白川郷線的規則
（同站 `takayama-shirakawago-day-trip` `blocks[8]` 寫對了），被搬錯地方。
出處：北陸鐵道 https://www.hokutetsu.co.jp/highway-bus/takayama/ 與 https://www.hokutetsu.co.jp/highway-bus/shirakawa/
（2026-09-20 都 curl 200、HTML 註解 0 條有字）：「本路線は座席指定制です。必ずご予約の上、ご乗車ください。」

**3. 所要時間沒有標出處。** 營運者寫 1 小時 15 分（高山線頁「所要時間（見込み）：60分（金沢ー五箇山）、1時間15分（金沢ー白川郷）、2時間15分（金沢ー高山）」），
站上寫的都是觀光協會的「約 1 小時 20 分」（https://shirakawa-go.gr.jp/access/ 「金沢駅所要時間 約1時間30分／高速バス 約1時間20分」），
其中 `takayama-shirakawago-day-trip` `blocks[4]` 表格那一格**完全沒有標出處**，`apps/web/public/guides/takayama-shirakawago-day-trip/diagram-1.svg` 上也有 2 處。
兩篇是同一個事實，要同一個 PR 改，否則會一邊 1 小時 15 分、一邊 1 小時 20 分。

## Definition of done

- [ ] `takayama-shirakawago-day-trip` `blocks[23]` 三處一次改完：乘車處寫「和田家旁」（拿掉沒有官方出處的「約 200 公尺」）、班表寫「上行 9:00 到 15:40、下行 9:10 到 16:10，12 點到 13 點之間沒有上行班次」、步行寫「15 到 20 分」。同一塊的 300 日圓、和田家與民家園的票價時間一個都沒動。
- [ ] `takayama-shirakawago-day-trip` `blocks[4]`（table 末列「巴士 白川鄉–金澤」）的「約 1 小時 20 分」改成「約 1 小時 15 分（觀光協會寫約 1 小時 20 分）」；`blocks[7]` 補一句營運者的 1 小時 15 分（原句「白川鄉觀光協會標示約 1 小時 20 分」有標出處、不刪）。
- [ ] `apps/web/public/guides/takayama-shirakawago-day-trip/diagram-1.svg` 上的「白川郷到金沢約 1 小時 20 分」（2 處）與正文一致。
- [ ] `kanazawa-2-day-itinerary` `blocks[55]` 改成座席指定制、必須預約，且所要時間改成「約 1 小時 15 分（觀光協會寫約 1 小時 20 分）」。
- [ ] 兩篇的 `sources` 補上或更新北陸鐵道兩個路線頁、白川村役場兩頁與觀光協會 access／events 頁，`checked_on` 只更新實際重讀的那幾條。
- [ ] lint 與內容包測試綠；部署後兩個 slug 的 `guides-import` 都是 `update` 再 `--publish`。

## Steps

- [ ] `takayama-shirakawago-day-trip` `blocks[23]`：(a) 和田家旁、(b) 上下行兩組時刻與中午無上行、(c) 15 到 20 分，**一次改完**。
- [ ] `takayama-shirakawago-day-trip` `blocks[4]` 表格末列與 `blocks[7]` 的所要時間。
- [ ] `diagram-1.svg` 的兩處「1 小時 20 分」（改完 lint 會檢查圖上的數字有沒有出現在正文）。
- [ ] `kanazawa-2-day-itinerary` `blocks[55]`（全文就是那一句）。
- [ ] **不要動**：`takayama-shirakawago-day-trip` `blocks[25]` 的「每車 6,000 到 10,000 日圓」（第 1 回 6,000／9,000、第 2 回 7,000／10,000，合起來正確）、`blocks[7]` 的「白川鄉回高山末班 17:30（18:35 到）」（與官方時刻表相符）、兩篇結尾的 `foods?city=`。

## How to verify

```bash
cd apps/api
uv run python -m app.guides.pack_cli lint --kind howto
uv run pytest tests/test_guides_content_pack.py -q
```

部署後在主機上（站主同意後）：

```bash
uv run python -m app.cli guides-import --slug takayama-shirakawago-day-trip --slug kanazawa-2-day-itinerary --dry-run   # 計畫應該只有這幾篇的 zh-TW 是 update
uv run python -m app.cli guides-import --slug takayama-shirakawago-day-trip --slug kanazawa-2-day-itinerary --publish
uv run python -m app.cli guides-links-check --locale zh-TW
```


改完 `grep -c "預約優先" apps/api/app/guides/content/kanazawa-2-day-itinerary.json` 是 0，
`grep -c "9:00 到 16:10" apps/api/app/guides/content/takayama-shirakawago-day-trip.json` 是 0。

## Notes

- 來源：`docs/travel-guides-batch-8/kanazawa-shirakawago-day-trip.md` 的「上線後與交叉檢查」與審查記錄 `plan8/review/review-japan.md` C3 第 1–3 條，彙整在 `docs/travel-guides-batch-8/FOLLOWUPS.md` 第 3 節。
- 三件事併成一張票的理由：所要時間是**同一個事實出現在兩篇**，同一個 PR 才不會互相矛盾；接駁巴士那一塊又在同一個檔案裡。
- scope 與「既有文章補連第八批」重疊：那張票要把 `kanazawa-2-day-itinerary` `blocks[55]` 與 `takayama-shirakawago-day-trip` `blocks[7]` 改成 `rich_paragraph` 加 inline 連第八批第 4 篇。**哪一張票先做就在那張一起做完**，另一張把該項打勾並註明；兩張票不能同時 claim。
- 撰稿當天還要再開一次白川村役場 `/2866.htm`（展望台步道封閉公告，內文是圖片、沒有文字層）：步道若封閉，`blocks[23]` 的步行時間要再處理一次。
- `kanazawa-2-day-itinerary` 另有「宿泊稅」用詞那張票（`2026-09-20-lodging-tax-wording-site-wide`）也在同一個檔上，兩張票同樣不能同時 claim。
