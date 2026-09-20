---
id: 2026-09-19-plan-articles-batch-8
title: 規劃第八批旅遊文章：補薄的城市（胡志明市、廣島、金澤、名古屋、沖繩、濟州、清邁、普吉、峴港）與大叻
status: in-progress
priority: P2
area: docs
owner: claude-fable-5-1
claimed_at: 2026-09-19T23:52:05Z
created_at: 2026-09-19T23:52:03Z
completed_at:
branch: claude/travel-guide-info-0c934d
depends_on: []
scope:
  - docs/travel-guides-batch-8
---

# 規劃第八批旅遊文章：補薄的城市（胡志明市、廣島、金澤、名古屋、沖繩、濟州、清邁、普吉、峴港）與大叻

## Why

站主 2026-09-20 要求再補一批旅遊情報與攻略（只做 zh-TW）。第七批（PR #543）上線後，zh-TW 的 howto＋intel 共 125 篇，
分布很不平均：東京 11、首爾 10、大阪京都 9，但廣島、金澤、胡志明市、清萊各只有 1 篇，清邁、峴港、大邱、濟州、喀比、名古屋、沖繩、普吉各 2 篇，
目的地目錄裡的大叻仍是 0 篇（第七批因官方數字讀不到一半而淘汰）。薄的城市只有一篇行程文，讀者落地之後的交通、住哪、一日遊都沒有站內文章可接，
城市頁與行程文也沒有可以互連的對象。

## Definition of done

- [ ] 照第七批的流程（`docs/travel-guides-batch-7/README.md` 開頭）在 `docs/travel-guides-batch-8/` 產出 README 與每篇規格：
      各區研究代理提候選 → 逐一在官方頁核對核心數字（curl 與 WebFetch 各試一次，讀到的數字逐字記檔，核心數字一半以上讀不到就淘汰）→ 選 20 篇 → 一篇一個規格代理 → 三輪一致性審查。
- [ ] 優先補 1–2 篇的城市；大叻重查一次，仍讀不到就再延後並寫明原因。
- [ ] display_order 接 1210 起；README 清單的 slug、kind、destination_id、topics、display_order、valid_until 與各規格一致。
- [ ] 撰稿與上線另開票（`launch-articles-batch-8`），並把規格裡有日期的後續項目列出來。

## Steps

- [x] 五個區域研究代理（opus）：日本西部與中部、韓國、泰國、越南、港星馬與跨區（2026-09-20 00:26Z 全部回來，無一被額度切斷）
- [x] 協調者選 20 篇、定 display_order 與互連（1210–1400，清單見下方「交接」）
- [ ] 規格代理（opus，一次 ≤7 個）
- [ ] 三輪一致性審查（連結與時效、區塊規則、事實與口徑）
- [ ] README、check:tasks、PR

## How to verify

`npm run check:tasks` 通過；README 表格與各規格的欄位一致；每個規格的「官方來源」一節都有規劃當天讀到的數字與網址。

## Notes

- 研究檔與抓下來的原始頁留在規劃工作區（session scratchpad `plan8/`），不進 repo（同第七批）。
- 對外請求的 User-Agent 一律 `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`，不得帶任何人的 email 或個人資料。

## 交接（2026-09-20）

這張票由 session「Google 索引未建立問題」（worktree `exciting-wozniak-51d668`，分支 `claude/travel-guides-batch-8-plan`）開出並認領，
做完研究、選題，派了規格 #1–#9。站主同一時間另開 session「旅遊攻略與情報」下了同一個指令；兩邊撞題後，站主用 AskUserQuestion
決定由後者（本分支 `claude/travel-guide-info-0c934d`，脈絡較小、協調較省 Fable 額度）接手整批 20 篇。切點：

- 原 session：不再派代理；在途的規格 #3–#9 跑完後連同 #1、#2 交過來（寫在它的 worktree，未 commit）；不從它的分支開 PR。
- 本 session：規格 #10–#20、三輪一致性審查、README、launch 票、PR，以及之後的撰稿與上線。
- 研究檔、原始頁與原 session 的狀態檔留在它的 scratchpad `plan8/`（只讀）；本 session 的狀態檔在自己的 scratchpad `plan8/STATE-here.md`。

選定的 20 篇（display_order）：okinawa-lodging-tax-2027（intel，1210）、japan-public-holidays-2027（intel，1220）、
ghibli-park-tickets-and-access（1230）、kanazawa-shirakawago-day-trip（1240）、onomichi-shimanami-kaido-cycling（1250）、
kerama-islands-ferry-from-naha（1260）、okinawa-without-a-car（1270）、hallasan-hiking-reservation-guide（1280）、
marado-gapado-ferry-day-trip（1290）、chiang-mai-airport-transport-where-to-stay（1300）、
chiang-mai-night-markets-walking-streets（1310）、phuket-old-town-big-buddha-viewpoints（1320）、
pattaya-koh-larn-day-trip-from-bangkok（1330）、thailand-temple-etiquette-dress-code（1340）、da-lat-3-day-itinerary（1350）、
ninh-binh-day-trip-from-hanoi（1360）、my-son-sanctuary-day-trip-from-da-nang（1370）、vung-tau-day-trip-from-ho-chi-minh（1380）、
ngong-ping-360-lantau-day（1390）、kuala-lumpur-3-day-itinerary（1400）。
