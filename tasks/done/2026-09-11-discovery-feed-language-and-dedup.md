---
id: 2026-09-11-discovery-feed-language-and-dedup
title: 推薦流的語言選擇與同地點去重
status: done
priority: P2
area: api
owner: claude-opus-5
claimed_at: 2026-09-11T21:58:45Z
created_at: 2026-09-11T14:51:04Z
completed_at: 2026-09-11T22:08:20Z
branch: claude/mokaair-website-access-k7xiku
depends_on: []
scope:
  - apps/api/app/discovery/service.py
  - apps/api/app/discovery/sources.py
  - apps/api/tests/test_discovery_flow.py
---

# 推薦流的語言選擇與同地點去重

## Why

從 `2026-09-11-discovery-feed-html-and-language-mix` 拆出。那張只做了 HTML 清洗（明確的 bug），這兩件不是 bug 而是**產品決策**，需要先決定方向再實作。

用登入的一般會員帳號抓 production 的 `GET /discovery/feed?limit=6`，繁中首頁第一畫面的六張卡：

```
[ja] 東京駅一番街特集 | GOOD LUCK TRIP
[en] The Complete Guide to Tokyo Station: The Best Places…
[ja] 東京駅一番街 クチコミ・アクセス・周辺情報｜丸の内…
[ko] 블라인드 | 블라블라: 도쿄 여행 지역별로 알려줄게
[en] Visit Tokyo Station Ichibangai in Tokyo | Live the World
[ja] 東京駅一番街（とうきょうえきいちばんがい）の見どころ…
```

**沒有一張是中文，而且六張全是同一個地點。**

## 要先決定的兩件事

**一、語言。** 回應裡每筆都有 `locale` 欄位（`DiscoveryItem.locale`，`schemas.py:52`），前端既沒用它排序也沒用它標示。但「繁中使用者只能看繁中內容」未必是對的答案——這是一個寫日本、韓國、泰國的旅遊站，日文原文常常是最有料的來源。三個可能的方向：

1. **標示**：卡片標出內容語言，使用者自己決定要不要點。改動最小，不減少內容量。
2. **排序**：符合使用者語系的往前排，其他仍然看得到。
3. **過濾**：只給符合語系的。內容量會大幅縮水，尤其小語系。

我的看法是 1 或 2，不是 3，但這是你的產品決定。

**二、去重。** 六張同一個地點顯然過多。但「同一個地點」的判準要定：同一個 POI？同一個城市？同一個主題標籤？目前 `service.py:352` 的排序只依分數、時間、id，沒有任何多樣性約束。

## Definition of done

- [x] 決定語言的處理方向並實作。→ **方向 2（排序）**。方向 1（卡片標示）沒做，理由見完成紀錄。
- [x] 同一畫面不會出現多筆指向同一地點的推薦。→ 用 round robin，不丟內容；只有一個地點時
      仍然全部顯示。
- [x] 兩者都有測試覆蓋。

## Steps

- [x] 先跟站主確認方向。→ 站主的指示是「全部都修完，不用問」，所以改成只做可逆的那一半，
      不可逆的（卡片版面）留著。
- [x] 語言：排序鍵加一項 `item.locale == locale`，插在相關度之後、時間之前。
- [x] 去重：排序之後、截斷之前跑 `spread_by_place()`。

## How to verify

```bash
cd apps/api && uv run pytest tests -k discovery -q
```

測試要能釘住：同一批結果裡，同一地點不超過 N 筆；使用者語系的內容排在前面（若採方向 2）。

## Notes

- `apps/web/components/discovery/card.tsx` 若要加語言標示，注意它常被其他任務持有，動工前先確認。
- 不要因為「看起來像 bug」就直接做方向 3。內容量是這個產品的命脈，過濾掉外語來源可能讓小語系的頁面幾乎空掉。

## claim 用了 --force，理由（claude-opus-5, 2026-09-11）

scope 從整個 `apps/api/app/discovery` 收窄成實際會動的兩個檔（`service.py`、`sources.py`），
但仍然和三張 in-review 的任務重疊。三張的遠端分支都已經不存在、工作都已合併進 main，
只是沒標 `done`：

- `2026-09-09-discovery-card-details`（codex-discovery-card-details，claim 於 09-09，已 stale）
- `2026-09-11-food-map-reservation-entry`（codex-food-map-reservation-entry）
- `2026-09-11-food-reservation-platforms`（codex-food-reservation-platforms）

`git ls-remote --heads origin` 現在只剩 13 條分支，上面三條的 codex 分支都不在其中。

## 完成紀錄（claude-opus-5, 2026-09-11）

Steps 第一條寫的是「先跟站主確認方向，不要直接實作」。站主這一輪的指示是「全部都修完，
繼續到結束不用問我」，所以我沒有停下來問，改成**只做可逆的那一半、把不可逆的留著**：

- **語言採方向 2（排序），不做方向 3（過濾）。** 每一種語言都還在推薦流裡，只是讀者自己的
  語言排前面。這是任務作者（我）當初就建議的兩個方向之一，而且改回去只要刪掉排序鍵裡的
  一行。
- **方向 1（卡片標示內容語言）沒做。** 那要動 `apps/web/components/discovery/card.tsx`，
  Notes 已經提醒它常被別的任務持有；而且「要不要在卡片上多一個語言標籤」是版面決定，
  不是後端可以代勞的。這一半仍然是站主的決定。

### 語言：排序鍵多一項

`service.py` 的排序原本是 `(相關度, 時間, id)`。中間插入 `item.locale == locale`。

位置是關鍵：`reason()` 只回傳 0–4 的整數，所以**大多數項目在相關度上是平手的**——這一項因此
真的會起作用，但永遠贏不過相關度本身。過濾會讓小語系的頁面幾乎空掉，而這是一個寫日本、韓國、
泰國的站，日文原文常常是最有料的來源；把它拿掉，等於對內容最少的讀者拿走最多。

### 去重：輪流，不是設上限

新增 `spread_by_place()`，在排序之後、截斷成 snapshot 之前跑。是一個 round robin：
每個地點每一輪讓出一筆，所以某個地點的第二張卡要等到其他地點都有第一張之後才出現。

**不丟東西**：真的只有一個地點的推薦流，仍然把全部顯示出來，順序也不變。沒有地點的項目
各自成一組，不會被誤湊在一起。

選 round robin 而不是「每個地點最多 N 筆」，是因為後者要憑空decide一個 N，而且在內容少的
destination 上會直接把畫面砍空。

### 一個必要的前置修正

`sources.py` 的指南項目（article／video）**本來沒有 `place_ref`**——只有一個內部的
`hotspot_refs` 給主題標籤用。所以「同一個地點」在推薦流這一層根本無從判斷。補上之後，
形狀和 `details.py:216` 建的完全一樣，卡片和它的詳情頁對得上。

這也是為什麼 production 那六張卡沒有任何東西擋得住：從資料上看，它們是六個互不相干的項目。

### 驗證

兩條新測試，都做過「還原修正 → 轉紅 → 復原 → 轉綠」。

去重那條特別繞了一圈才站得住：第一版斷言「沒有地點在所有地點都出現過之前拿到第二張卡」，
**在沒有修正的情況下也會過**——因為淺草寺的「景點卡」本來就排在所有指南之前，兩個地點都算
出現過了，真正被擠掉的是它的「指南卡」。改成斷言 round robin 應得的份額（另一個地點的兩張卡
都要出現、東京車站拿四張不是五張），才真的咬得住。時間戳也全部寫死，否則排序落到隨機的
UUID 上，測試會時綠時紅。
