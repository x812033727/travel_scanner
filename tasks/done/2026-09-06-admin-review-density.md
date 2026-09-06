---
id: 2026-09-06-admin-review-density
title: 後台審核頁在看到第一筆待審之前先給 30 個控制項
status: done
priority: P2
area: web
owner: claude-opus-5
claimed_at: 2026-09-06T18:39:46Z
created_at: 2026-09-06T15:00:00Z
completed_at: 2026-09-06T18:51:14Z
branch: claude/admin-density
depends_on: []
scope:
  - apps/web/components/admin-hotspots-panel.tsx
  - apps/web/components/admin-hotspots-workspace.tsx
  - apps/web/components/admin-filter-pills.tsx
  - apps/web/components/admin-hotspots-panel.test.tsx
  - apps/web/messages/en/admin.json
  - apps/web/messages/ja/admin.json
  - apps/web/messages/ko/admin.json
  - apps/web/messages/zh-CN/admin.json
  - apps/web/messages/zh-TW/admin.json
---

# 後台審核頁在看到第一筆待審之前先給 30 個控制項

## Why

2026-09-06 用登入的瀏覽器看線上的 `/zh-TW/admin/hotspots`（當時有 196 筆待審、
全站待審工作 403 筆）。1528×784 的第一屏由上到下是：

1. 五個分頁（景點候選／Google 地點資料／多語景點介紹／附近餐廳掃描／餐廳來源）
2. 國家膠囊八顆
3. 類型膠囊八顆
4. 六個下拉／輸入（狀態、城市代碼、目的地 ID、層級、母目的地 ID、來源）
5. 「核准／拒絕／停用」三顆批次按鈕
6. 「移動至目的地 ID」＋「移動目的地」
7. 才輪到第一筆候選，而那一筆本身又是一組下拉＋三個數字欄位＋四個評分欄位

也就是說要按到第一個決定之前，畫面上已經有三十個左右的控制項。這是每天都要清
幾百筆的人在用的頁面，篩選條件多半不會每次都換。

## Definition of done

- [x] 第一屏就看得到第一筆待審與它的核准／拒絕。
- [x] 篩選（膠囊與六個欄位）預設收合成一行摘要（例如「待審 · 全部國家 · 全部類型」），
      點開才展開，展開狀態記在 URL 或 localStorage。
- [x] 批次操作在沒有勾選任何一筆時不佔第一屏。

## How to verify

1440×900 開 `/zh-TW/admin/hotspots`，不捲動就能看到第一筆候選的名稱與核准鈕；
390px 下同樣的順序。

## Notes


- 不要把篩選拿掉，只是預設收起來：`admin-filter-pills.tsx` 已經是共用元件，收合
  的行為做在那裡，美食目錄那頁可以跟著用。
- 這是 2026-09-06 全站 UI/UX 健檢的一部分；同一輪還發現後台載入失敗會整頁換成
  英文錯誤頁（已修）與側邊欄目前頁籤看不見（已修）。

### 做完之後（2026-09-07，claude-opus-5）

兩件事，加起來把第一屏的控制項從大約三十個降到三個（一行摘要、一行統計、第一筆的核取方塊）：

1. **篩選收合。** `admin-filter-pills.tsx` 多一個 `FilterDisclosure`（照任務指定的位置，
   美食那頁可以直接拿去用）。收合時只有一行：`待審 · 全部國家 · 所有類型`。
   狀態記在 `localStorage`（`mokaair-admin-hotspot-filters`），預設收合。
2. **批次操作在沒有勾選時整組不顯示**：核准／拒絕／停用、移動目的地、深度旅遊那一整塊
   （四個評分欄位、兩個按鈕）本來就 `disabled={!selected.size}`，也就是說沒有選取時
   它們純粹在佔位置。統計那一行留著，因為它隨時都有意義。

實作上唯一麻煩的是讀 `localStorage`：`useEffect` 裡同步 `setState` 會被 lint 的
cascading-render 規則擋下來，改用 `useSyncExternalStore`——伺服器端回 false（收合），
瀏覽器 hydrate 時才校正，這也是 React 對這種瀏覽器狀態的建議寫法。

scope 多了五個 `admin.json`（三個新字串：篩選條件／展開／收合）與該面板的測試檔。
測試改成先點「展開篩選條件」再查膠囊，並新增一條釘住「第一筆候選在畫面上時，
核准與深度按鈕都還不存在；勾選之後才出現」。

1440×900 的實測留到部署後（後台需要登入）。


## 正式站量測（2026-09-07，部署 1eb573f 之後）

`https://mokaair.com/zh-TW/admin/hotspots`，1464×807，已登入：

| | 之前 | 現在 |
| --- | --- | --- |
| 看到表格之前的互動控制項 | 30 | **6** |
| 表格頂端的 y | ——| 424（在第一屏裡） |

那 6 個是五個工作區分頁加一個收合起來的「篩選條件」按鈕，`aria-expanded="false"`，
摘要行寫著「待審 · 全部國家 · 所有類型」——先說現在在看什麼，要改再展開。
