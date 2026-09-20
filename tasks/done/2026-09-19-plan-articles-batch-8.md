---
id: 2026-09-19-plan-articles-batch-8
title: 規劃第八批旅遊文章：補薄的城市（胡志明市、廣島、金澤、名古屋、沖繩、濟州、清邁、普吉、峴港）與大叻
status: done
priority: P2
area: docs
owner: claude-fable-5-1
claimed_at: 2026-09-19T23:52:05Z
created_at: 2026-09-19T23:52:03Z
completed_at: 2026-09-20T03:27:37Z
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

- [x] 照第七批的流程（`docs/travel-guides-batch-7/README.md` 開頭）在 `docs/travel-guides-batch-8/` 產出 README 與每篇規格：
      各區研究代理提候選 → 逐一在官方頁核對核心數字（curl 與 WebFetch 各試一次，讀到的數字逐字記檔，核心數字一半以上讀不到就淘汰）→ 選 20 篇 → 一篇一個規格代理 → 三輪一致性審查。
- [x] 優先補 1–2 篇的城市；大叻重查一次，仍讀不到就再延後並寫明原因。（大叻 12 個核心數字全讀到，收進本批。）
- [x] display_order 接 1210 起；README 清單的 slug、kind、destination_id、topics、display_order、valid_until 與各規格一致。
- [x] 撰稿與上線另開票（`2026-09-20-launch-articles-batch-8`），並把規格裡有日期的後續項目列出來（`docs/travel-guides-batch-8/FOLLOWUPS.md`）。

## Steps

- [x] 五個區域研究代理（opus）：日本西部與中部、韓國、泰國、越南、港星馬與跨區（2026-09-20 00:26Z 全部回來，無一被額度切斷）
- [x] 協調者選 20 篇、定 display_order 與互連（1210–1400，清單見下方「交接」）
- [x] 規格代理（opus，一次 ≤7 個）
- [x] 一致性審查（改成按地區分六組，每組同時看事實與口徑、區塊規則、連結與時效）
- [x] README、check:tasks、PR

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

## 規劃紀錄（2026-09-20）

**研究。** 五個區域各一位 opus 研究代理，60 個候選逐一在官方頁核對核心數字，keep 39、drop 21（日本 11／1、韓國 6／6、
泰國 8／4、越南 6／6、港星馬與跨區 8／4）。研究檔與 741 個原始頁留在規劃工作區，不進 repo。

**選 20 篇**（清單見 `docs/travel-guides-batch-8/README.md`）：沖繩 3（含住宿稅情報）、日本本島 4（含 2027 國定假日情報）、濟州 2、
清邁 2、普吉 1、芭達雅 1、泰國寺廟禮儀 1、越南 4、昂坪 1、吉隆坡 1。display_order 1210 到 1400。大叻是目的地目錄裡最後一個
0 篇的城市，第七批淘汰它的理由（官方數字讀不到一半）這次不成立，12 個核心數字全讀到。

**規格。** 一篇一位 opus 規格代理，把研究讀到的每個數字再開官方頁確認一次。三個研究階段的前提被推翻：金澤→白川鄉去回各
11 班（不是一天兩班）、吉卜力公園 2026 年 7 月起七種券（不是四種）、廣島機場→尾道 60 分且這一期 6＋5 班。

**審查。** 20 份規格共 1.17 MB，單一代理讀不完，所以從第七批的「三個鏡頭各一位」改成按地區分六組、每組同時看三個鏡頭，
先跑一支機械檢查列出每份規格引用的站內文章、會過期的情報文與同批互連對稱性。六份審查記錄合計改了 155 處、
約 30 條交協調者裁決。抓到的典型問題：

- 住宿稅篇寫「不要寫成慶良間兩村都收」，被慶良間篇推翻——渡嘉敷「環境協力税」、座間味「美ら島税」各 100 日圓，稅名不同。
- 日本四份規格的字數全部會超標（漏算 summary、表格每一格、callout 與連結句），補了逐段上限。
- 寧平篇的火車表欄名把北上半張表標錯；大叻篇原本要去改季節篇一句其實有官方出處的話，已撤回。
- 多份規格各自要改同一篇既有文章的同一個區塊（清邁三天篇 blocks[9]、沖繩四天篇、季節篇），已合併成一次編輯。
- article inline 被指定放進放不了的區塊（list 的 item、callout、paragraph），全部補上型別改法。
- 四次差點採用 HTML 註解裡的死內容（漢拏山「每日 3,000 人」等），寫進 README 的通用防錯。

**全批通則**（都在 README）：兩個官方來源打架時數字擇一、另一邊一句話揭露、開放時間取較窄的時段；null 文章的 offer 與結尾
link 規則；`foods?city=` 自 2026-09-19 起不是錯、不要順手改；譯名裁決（格蘭島、契迪龍寺、漢拏山、會安古城、沖繩「住宿稅」、
のぞみ「全席指定席」）。

**後續。** `FOLLOWUPS.md` 彙整了 106 列有日期或條件的複查（建議 37 張票，上線 PR 才開）、31 篇既有文章的反向連結、
以及審查時發現的既有文章錯誤——後者已開成 10 張票，另有四件事併進 `2026-09-20-jeju-itinerary-gwaneumsa-reopens-0924`。
延後的兩篇時效情報各有一張票：`2026-09-20-korea-autumn-leaves-2026-intel`、`2026-09-20-loy-krathong-yi-peng-2026-intel`。
