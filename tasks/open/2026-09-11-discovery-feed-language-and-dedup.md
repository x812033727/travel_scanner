---
id: 2026-09-11-discovery-feed-language-and-dedup
title: 推薦流的語言選擇與同地點去重
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-09-11T14:51:04Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/discovery
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

- [ ] 決定語言的處理方向（標示／排序／過濾）並實作。
- [ ] 同一畫面不會出現多筆指向同一地點的推薦。
- [ ] 兩者都有測試覆蓋。

## Steps

- [ ] **先跟站主確認方向**，不要直接實作。
- [ ] 語言：`content_locale` 目前只用在社群貼文那一支（`service.py:210`），其他來源沒吃到。若採方向 2，排序鍵加一個「語系相符」的權重即可。
- [ ] 去重：在 `service.py:352` 的排序之後、截斷之前，依選定的判準做多樣性約束。

## How to verify

```bash
cd apps/api && uv run pytest tests -k discovery -q
```

測試要能釘住：同一批結果裡，同一地點不超過 N 筆；使用者語系的內容排在前面（若採方向 2）。

## Notes

- `apps/web/components/discovery/card.tsx` 若要加語言標示，注意它常被其他任務持有，動工前先確認。
- 不要因為「看起來像 bug」就直接做方向 3。內容量是這個產品的命脈，過濾掉外語來源可能讓小語系的頁面幾乎空掉。
