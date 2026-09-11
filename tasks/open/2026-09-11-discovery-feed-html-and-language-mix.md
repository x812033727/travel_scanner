---
id: 2026-09-11-discovery-feed-html-and-language-mix
title: 推薦流印出原始 HTML 標籤且語言混雜未去重
status: open
priority: P1
area: web
owner:
claimed_at:
created_at: 2026-09-11T13:05:05Z
completed_at:
branch:
depends_on: []
scope:
  - apps/web/components/discovery/card.tsx
  - apps/api/app/discovery
---

# 推薦流印出原始 HTML 標籤且語言混雜未去重

## Why

用登入的 session 抓 production 的 `GET /discovery/feed?limit=6`，並在真實瀏覽器看渲染結果，三個問題同時出現在首頁第一畫面：

**一、原始 HTML 標籤被當文字印出。** 6 筆裡有 2 筆的 `summary` 含 HTML，前端直接渲染成字面：

```
There's <strong>shopping, dining, souvenir shopping</strong> – you name it, you can do it.
From <strong>delicious ramen to unique souvenirs</strong>, Tokyo Station Ichibangai has so…
```

使用者看到的就是上面那個樣子，含角括號。

**二、繁中首頁沒有一筆中文內容。** API 回應裡每筆都有 `language` 欄位，實測值是：

```
[ja] 東京駅一番街特集 | GOOD LUCK TRIP
[en] The Complete Guide to Tokyo Station: The Best Places…
[ja] 東京駅一番街 クチコミ・アクセス・周辺情報｜丸の内…
[ko] 블라인드 | 블라블라: 도쿄 여행 지역별로 알려줄게
[en] Visit Tokyo Station Ichibangai in Tokyo | Live the World
[ja] 東京駅一番街（とうきょうえきいちばんがい）の見どころ…
```

一個看繁中介面的使用者，首頁「為你推薦」全是看不懂的日文、英文、韓文。**欄位就在回應裡，前端既沒用它排序、也沒用它標示。**

**三、6 筆全是同一個地點。** 全部關於「東京駅一番街」，卡片的分類標籤也完全一樣（東京・攻略・購物・伴手禮・動漫周邊）。推薦流沒有依主題去重。

## Definition of done

- [ ] 卡片內文不再出現原始 HTML 標籤。
- [ ] 使用者語系的內容優先，或至少在卡片上標示內容語言。
- [ ] 同一畫面不會出現多筆同一地點的重複推薦。

## Steps

- [ ] **HTML**：決定在哪一層處理。後端在 ingest 時把 `summary` 轉純文字最乾淨（一次修好，所有用戶端受惠）；若要保留 HTML 供未來渲染，前端就得安全地 strip。不要在前端用 `dangerouslySetInnerHTML`。
- [ ] **語言**：用回應裡既有的 `language` 欄位。最小可行做法是排序時把符合使用者語系的往前排；退一步至少在卡片加上語言標示，讓人知道點進去會看到什麼語言。
- [ ] **去重**：依地點／主題做 dedupe，同一個 POI 在一頁最多出現一次。
- [ ] 三件事可以分開上線，HTML 那項最急也最小。

## How to verify

```bash
cd apps/api && uv run pytest tests -k discovery -q
cd apps/web && npm run test:web -- discovery
```

手動：開 `/zh-TW`，第一畫面的卡片內文不應出現 `<strong>`，且不應 6 筆都是同一個地點。

## Notes

- 這是 production 的真實資料，不是測試資料——用一般會員帳號登入 production 取得。
- 與 `2026-09-09-discovery-card-details`（codex 持有中，review 狀態）主題相近但不同：那張講卡片的密度與來源連結，這張講內容本身的清洗與選取。動工前確認 scope 不衝突。
