---
id: 2026-09-06-planning-flow-remaining-increments
title: 剩下的規劃流程增量：營業時間感知、匯入、匯出、分享
status: done
priority: P2
area: meta
owner: claude-fable-5-1
claimed_at: 2026-09-06T02:23:46Z
created_at: 2026-09-06T00:55:50Z
completed_at: 2026-09-06T02:28:31Z
branch: claude/board-warmup
depends_on: []
scope:
  - docs/planning-flow-spec.md
---

# 剩下的規劃流程增量：營業時間感知、匯入、匯出、分享

## Why

`docs/planning-flow-spec.md` 是對照競品去趣 chicTrip 做的完整規劃流程設計，
§6 把它拆成 14 個可獨立出貨的增量。目前只做完前四個：

| 增量 | 狀態 |
|---|---|
| 真 AI 行程解析器（取代假 AI） | 已上線 PR #146 |
| `PATCH /trips/{id}` 行程中繼資料 | 已上線 PR #155 |
| 鎖定 + preserved-set | 早已存在，不需要做 |
| 意圖列 | 已合併 PR #168，但帶著 blocker（見其他任務） |

這張任務只是把**剩下的十個增量**留在板上，讓它們不會因為對話結束而消失。
每個真的要動工時應該各自開一張帶明確 scope 的任務，這張只負責指路。

## Definition of done

- [x] 剩下的增量各自有了自己的任務，或被明確決定不做。
- [x] 這張任務關掉。

## Steps

按規格 §6 的順序，投報率由高到低：

- [x] **營業時間感知排程**（M）→ `2026-09-06-opening-hours-aware-scheduling`（P2）。第一個真正的超越點：去趣 8 篇評測都沒提到營業時間，
      damei17 顯示的是一律預設 1 小時。而 `HotspotPlaceProfile.opening_hours_json` **已經存在**、
      `normalize_draft` 也已經在把每個開始時間重寫到時段網格上，只差把前者餵進 `_safe_slots`。
      「我們不會讓你星期一跑去一間沒開的美術館」是可以截圖示範的差異。
- [x] **貼 Google Maps 連結加景點**（M，但七成已存在）→ `2026-09-06-paste-maps-links-ingest`（P2）。`restaurants/imports.py:101`
      的 `resolve_maps_input()` 已經會做短網址展開、15 個主機的白名單、Place ID 抽取，
      目前只在一個地方被呼叫。這是去趣最受好評的能力，而我們用一小部分成本就能對打。
- [x] **ICS 行事曆匯出**（S）→ `2026-09-06-ics-calendar-export`。純序列化，時間都已經算好了。
- [x] **列印版行程表**（M）→ `2026-09-06-printable-itinerary`。去趣的「旅遊小書」是 8/8 評測的情感高潮；
      規格選擇先做有用的一半。**這是規格作者信心最低的一項** —— 見規格 §7 Q3，
      評審 3 主張那正是去趣贏的地方。
- [x] **分享連結「存成我的行程」+ QR**（S 各一）→ `2026-09-06-share-fork-and-qr`。比多人共編便宜 20 倍，
      而且把分享流量轉成新帳號，共編做不到這件事。
- [x] **已存行程掛分潤選項**（S）→ `2026-09-06-trip-affiliate-options`。後端 `AffiliateClick.trip_id` 已支援，前端從沒傳過。
      去趣的商業層只做台灣，兩篇評測作者都抱怨要日韓 —— 我們的框架不綁地區。
- [x] **行程狀態標籤 + 封面圖**（S）→ `2026-09-06-trip-status-and-cover`。便宜的對等補齊。
- [x] **最佳化上限的 UX**（S）→ `2026-09-06-optimizer-limit-ux`。超過 12 個可移動景點時先提示，而不是直接 422。
- [x] **誠實路段守衛**（S）→ `2026-09-06-honest-leg-guard`。拒絕四捨五入成 0 分鐘的候選、拒絕漏掉 250m 以上步行段的轉乘方案。
      去趣的評測者 hansphoto 就抱怨過首爾出現 0 分鐘路段。
- [x] **PWA + share target**（L）/ **今日檢視** → `2026-09-06-pwa-share-target-today-view`。iOS 的 share sheet 是永久性的對等落差。

被外部條件卡住、不建議現在動的：

- **韓國轉乘**：需要 ODsay 或 Kakao Mobility 合約。`routing.py:2154` 的 `region == "KR"` 還擋著。
- **商家驗證積壓**：155 家全是 pending/inactive，`/foods` 在管理員逐一驗證前發佈不出任何一家。
  這是營運工作不是程式問題，但我們的內容優勢在它跑完之前是隱形的。
- **多人共編**：XL，要重寫 `owned_trip()` 和它 20 個呼叫端。規格建議先做「存成我的行程」再看需求。

## How to verify

讀 `docs/planning-flow-spec.md` §6，確認每一項都有對應的任務或已被明確放棄。

## Notes

**2026-09-06 結案。** 十個增量各自立了任務（前兩個 P2，其餘 P3），scope 都釘到明確路徑，
所以它們互相之間、以及與其他 open 任務之間，只要不同時被認領就不會互相擋。
被外部條件卡住的三項明確決定**現在不立案**：韓國轉乘等 ODsay／Kakao 合約；商家驗證積壓已由
`2026-09-06-merchant-coordinate-backlog` 追蹤（是營運工作）；多人共編等「存成我的行程」上線後看需求再說（規格 §5 的判斷）。
§7 的六個開放問題裡，Q1（精修定價）在 `2026-09-06-intent-trip-scope-free` 處理，Q4（匯入配額）寫進了貼連結那張的 Steps，
Q2／Q3／Q5／Q6 留在規格裡，各自的任務檔 Notes 有指回去。

規格本身是四個獨立設計提案經三位評審評分後合成的，
評審一致給「散文開場 + 意圖列」最高分（8/8/8）。§0 有六項對原始提案的事實更正，
§7 有六個需要產品判斷的開放問題（精修定價、33 個目的地之外怎麼辦、旅遊小書要不要做、
匯入配額、iOS 收集、版本衝突容忍度），每一個都寫了選項和當時的建議。

同一份規格的落差分析（去趣有什麼、我們有什麼、誰贏在哪）在對話中產出，
規格的 §2 和 §5 保留了結論。最重要的一句：**去趣沒有生成式的步驟** ——
8 篇評測有 7 篇完全沒提到 AI，使用者自己找完所有景點，App 只負責排序。
它的「智慧」是確定性的 TSP 重排加行車時間計算。
