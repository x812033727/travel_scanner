---
id: 2026-10-05-write-the-visit-jeju-hidden-payload
title: Write the Visit Jeju hidden-payload and 더보기 rules into the content pitfalls
status: done
priority: P3
area: docs
owner: claude-opus-5-5-content-pitfalls-visitjeju
claimed_at: 2026-10-05T13:23:38Z
created_at: 2026-10-05T07:41:59Z
completed_at: 2026-10-05T13:36:22Z
branch: claude/content-pitfalls-visitjeju
depends_on: []
scope:
  - .agents/skills/content-pipeline/references/pitfalls.md
---

# Write the Visit Jeju hidden-payload and 더보기 rules into the content pitfalls

## Why

`visitjeju.net` 改版後每一頁都有 `<div style="display:none" id="__SEARCH_DATA__">`，裡面是舊版長介紹（`sbstseo`）、地址與營業時間。2026-09-20 韓國美食特輯的查核者發現這件事，寫進批次工作區的 `prompts/SOURCE-TIPS.md`，但那個工作區（`mokaair-work/korea-food-specials`）已經不在了，repo 裡的 `.agents/skills/content-pipeline/references/pitfalls.md` 一個字都沒寫。下一批引 Visit Jeju 的撰稿或查核代理會再踩一次。

2026-10-05 重驗兩篇舊文（票 `2026-09-20-visitjeju-hidden-payload-recheck`）時又多學到一件反方向的事：店家與景點頁的 `이용안내` 區塊在 curl 抓到的 HTML 裡是**空的** `<ul>`，按下「더보기 +」（英文版「View more +」）才由前端畫出 `이용 시간`、`상세 정보`（就是 `usedescinfo` 的分季時間與休息日）、`요금 정보`。也就是說營業時間**讀者按一下就看得到**，不是只在隱藏區塊；只用 HTMLParser 判斷會誤刪。特輯的 `jeju-heukdwaeji-food-guide` 查核兩輪都寫「Visit Jeju 可見이용안내為空」，那是沒執行 JS 的結果。

## Definition of done

- [x] `pitfalls.md`「抓取與來源」有一條 Visit Jeju 的規則：`#__SEARCH_DATA__` 永遠不是來源；`이용안내` 的「더보기 +」內容要用真的瀏覽器點開再判斷，點得出來的算可見
- [x] 同一條寫明正文區「펼치기 +」只是把同一段文字展開，不會顯示隱藏區塊

## Steps

- [x] 在 `pitfalls.md`「抓取與來源」加一條祈使句，後面寫為什麼（參考下方 Notes 的實測）
- [x] 確認 `.claude/skills/content-pipeline/` 底下沒有 pitfalls.md 的複本要同步（#1222 之後只有 SKILL.md 鏡像）
- [x] `node --test tools/skills.test.mjs`

## How to verify

```bash
node --test tools/skills.test.mjs
grep -n "visitjeju" .agents/skills/content-pipeline/references/pitfalls.md
```

## Notes

- 在票 `2026-09-20-visitjeju-hidden-payload-recheck` 重驗時發現；那張票只管兩篇文章的內容，不改 skill，所以另開這張。
- 2026-10-05 實測（內建瀏覽器，`성산일출봉` 韓文與英文頁 `CONT_000000000500349`）：點「더보기 +」之前 `section.detail_information` 的 `<ul>` 只有 Vue 的註解佔位；點之後出現 11 列，包含「(동절기) 11월~익년 2월 06:00~18:00 (매표 06:00~17:00) / … / 매달 첫 번째 월요일 정기 휴무(공휴일인 경우 다음 날 휴무) / 음식물 반입 금지」與票價。正文的「펼치기 +」點開前後文字長度一樣（1345→1344），只是解除高度裁切。
- 主題頁（`/themtour/view`）的 `sbstseo` 是空的，隱藏區塊只有標題與 tag，可見正文就是全文。
- 同一天掃過 VISITKOREA、Visit Seoul、Visit Busan 各一頁：`display:none` 且超過 200 字的只有 cookie 提示，沒有 SEO 隱藏正文。
- 掃描與切分腳本（stdlib `html.parser`）只放在該次 session 的 scratchpad，沒有進 repo；要的話照上面的規則重寫，二十幾行。

### 2026-10-05 寫進 skill（claude-opus-5-5-content-pitfalls-visitjeju）

- `pitfalls.md`「抓取與來源」最後加了一條，一句祈使句後接原因，兩個完成條件都寫在同一條裡。`.claude/skills/content-pipeline/` 底下只有 `SKILL.md`，沒有東西要同步。
- 寫之前重驗一次（UA `Mokaair-editorial/1.0`，curl 兩頁加一個主題頁，再用內建瀏覽器開韓文頁，請求之間有間隔）：
  - curl：韓文與英文 성산일출봉 頁都是 200、沒有轉址；`#__SEARCH_DATA__` 是 `display:none;`，欄位是 `<pre data-key="…">`（`sbstseo`、`usedescinfo`、`roadaddress` 等）；`section.detail_information` 的 `<ul>` 只有 Vue 註解。英文頁的標題是 `Tip`、按鈕是 `View more +`，正文按鈕是 `Expand +`。主題頁 `CNTS_200000000010918` 的 `sbstseo` 是空的 `<pre>`。
  - 內建瀏覽器：**不按也會**在頁面載入完成後把 11 列放進 DOM，只是容器 `.container` 高度 0、`overflow:hidden`、`visibility:hidden`，整個 section 的 `innerText` 只有 5 個字元。按「더보기 +」後容器變可見、高 680 px、按鈕變「닫기-」、`innerText` 610 字。所以原本 Notes 寫的「點之前只有註解佔位」是載入完成前讀到的狀態；結論不變（讀者要按一下才看得到），但用 Playwright 讀 `textContent` 的檢查器在按之前就會讀到這 11 列，用 `innerText` 的則讀不到。規則因此寫「用真的瀏覽器按開再判斷」，並點名 HTMLParser 與 `innerText` 兩種誤判。
  - `이용 시간` 那一列今天寫「평일 : 05:00 ~ 19:00 , 주말 : 05:00 ~ 19:00」，只有一組時間；分季時間與休息日在 `상세 정보` 那列。這條順手寫進規則，避免查核者拿 `이용 시간` 當全年時間。
  - 正文「펼치기 +」：`section.detail_contents` 的 `innerText` 1345→1344、高度 1081→11919 px，按鈕變「접기 -」，裡面沒有 `#__SEARCH_DATA__`。與原本 Notes 相同。
- 內建瀏覽器的窗格在背景，`computer` 的點擊因為頁面沒有繪製而失敗；改用 `javascript_tool` 呼叫按鈕自己的 `click()` 量測。英文頁在內建瀏覽器裡卡住沒載完，英文版只用 curl 看了標籤與空 `<ul>`。
- 檢查：`node --test tools/skills.test.mjs` 7 pass、0 fail；`grep -n "visitjeju" .agents/skills/content-pipeline/references/pitfalls.md` 命中第 17 行。這個 worktree 的 `package-lock.json` 跟 brief 指定的 junction 來源不同（差在 next、rolldown 等 35 個套件），所以沒有建 junction；`skills.test.mjs` 只用 `js-yaml`，從上層 checkout 解析到的是 4.3.2，跟這份 lock 相同。
