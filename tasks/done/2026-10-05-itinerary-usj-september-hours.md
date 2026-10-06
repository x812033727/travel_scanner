---
id: 2026-10-05-itinerary-usj-september-hours
title: 大阪京都奈良四天行程的環球影城營業時間與票價寫死 2026 年 9 月
status: done
priority: P3
area: docs
owner: claude-opus-5-5-usj-hours
claimed_at: 2026-10-06T01:44:35Z
created_at: 2026-10-05T07:05:00Z
completed_at: 2026-10-06T02:00:40Z
branch: claude/usj-hours
depends_on: []
scope:
  - apps/api/app/guides/content/osaka-kyoto-nara-4-day-itinerary.json
---

# 大阪京都奈良四天行程的環球影城營業時間與票價寫死 2026 年 9 月

## Why

`osaka-kyoto-nara-4-day-itinerary` 的 Day 4 段落寫的是「2026 年 9 月的營業時間依日期在 8:00 到 9:00 開園、21:00 到
22:00 閉園」，票價也標成「官方指定售票網站 2026 年 9 月價格」（1 日券 8,400 日圓起、1.5 日券 13,600 起、2 日券 16,000 起）。
十月起這段讀起來就是上個月的資料；環球影城的營業時間每天不同、票價是浮動的，寫死月份的寫法每個月都會過期。
2026-10-05 處理 KANSAI RAILWAY PASS LITE 時（票 `2026-09-14-refresh-kansai-lite-and-expressway-passes`）看到，不在那張票的範圍，沒有動。

## Definition of done

- [x] Day 4 的營業時間不再綁某一個月份：寫成讀者能自己查的形式（例如開園、閉園時間的大致範圍加「出發前一週看官網時間表」），
      或換成查證當月的數字並寫明月份。
- [x] 票價是改寫當天在官方或官方指定售票網站看到的起價，`sources` 的 `checked_on` 是那天。
- [ ] 合併後由協調者在站主同意下跑 `guides-import --slug osaka-kyoto-nara-4-day-itinerary`（dry-run 再 publish）。
      publish after merge (coordinator, owner consent)

## Steps

- [x] 用編輯 UA 讀 `https://www.usj.co.jp/web/zh/tw/park-guide/schedule/park-hour2`、`https://www.usj.co.jp/web/zh/tw/tickets`、
      `https://www.usjticketing.com/`。
- [x] 改 Day 4 段落；`cd apps/api && PYTHONUTF8=1 uv run python -m app.guides.pack_cli lint --slug osaka-kyoto-nara-4-day-itinerary`、
      `PYTHONUTF8=1 uv run pytest tests/test_guides_content_pack.py -q`。

## How to verify

```bash
cd apps/api
grep -n "9 月" app/guides/content/osaka-kyoto-nara-4-day-itinerary.json   # 不再有綁九月的營業時間
PYTHONUTF8=1 uv run python -m app.guides.pack_cli lint --slug osaka-kyoto-nara-4-day-itinerary   # 0 errors
```

## Notes

- 同一篇的 description 與開頭段落也寫「2026 年 9 月查證」；全篇重查時一起換，只改 USJ 段就不必動。
- 這篇沒有 summary 區塊，`pack_cli lint` 一直有 `no_summary` 警告；要補的話照 `docs/travel-guides-batch-7/README.md` §`pack.json`。
- 2026-10-06（claude-opus-5-5-usj-hours）：三頁用 curl 只拿到 app shell（`usj.co.jp` 是 Angular 殼加 Akamai 腳本，
  `usjticketing.com` 是 Vue 殼），沒有任何數字。改用 Playwright（`playwright-core` 1.63）啟動
  `ms-playwright/chromium_headless_shell-1243` 的 headless shell、編輯 UA 渲染，三頁都讀得到：
  - 營業時間日曆（要點月份標題右邊的箭頭換月，日曆文字在 `innerText` 抓不到，截圖或走訪 DOM 才看得到）：
    10/6–10/31 每天 08:00–22:00，只有 10/25 是 08:30–21:30；11 月 08:00–09:00 開園、19:00–22:00 閉園；
    12 月 08:00–09:00 開園、19:00–21:30 閉園，12/31 是 09:00–17:00。日曆只排到 2026 年 12 月。頁首另寫「當天可能會較園區開園時間提早開放入場」。
  - `usjticketing.com`（JTRWeb LTD.，USJ 授權售票）：1 Day Studio Pass 成人 ¥8,400〜、1.5 Day ¥13,600〜、2 Day ¥16,000〜（含稅），
    「Prices vary depending on the date of admission」；跟 9 月的起價一樣。
  - `usj.co.jp/web/zh/tw/tickets`：價格依日期不同、4 至 11 歲兒童票、購買需指定來園日期（購買後可辦改期）、嚴禁轉售、轉賣票的 QR Code 無效，
    段落裡原本這幾句都對得上，沒改。
- 段落改成「營業時間每天不一樣，大致在 8:00 到 9:00 開園、19:00 到 22:00 閉園，少數日子更早閉園」加看官網日曆；範圍取自
  9 月（舊文）到 12 月的日曆，不寫月份。票價改註「官方指定售票網站 2026 年 10 月 6 日的起價」。三筆 USJ 來源的 `checked_on` 改 2026-10-06，
  其他 17 筆沒重開、沒動。
- description、開頭段落與兩張表 caption 的「2026 年 9 月查證」、缺 summary、「這篇／本文」兩次，照上面的 Notes 沒動，開成
  `2026-10-06-itinerary-osaka-kyoto-nara-full-recheck`。
- 檢查：`pack_cli lint --slug osaka-kyoto-nara-4-day-itinerary` 0 errors（`no_summary` 警告是舊的）；`pack_cli lint --kind howto`
  152 篇 0 errors；`pytest tests/test_guides_content_pack.py -q` 9 passed、5 skipped；`intake_check.py --from-content` 的三個 FAIL
  （沒有 summary、`?city=` 連結、自稱兩次）都是 main 上原本就有的。
- DoD 第三項沒做：publish after merge (coordinator, owner consent)。

## Review round (independent, 2026-10-06)

- **Applied 2026-10-06** (claude-opus-5-5, apply pass; I wrote neither the PR nor the report
  below). The report's one finding (row 23) was applied with its second option, 「9 至 10 月」, in
  both places the finding names, so the description and the intro agree with each other:
  - `description`: 「…環球影城的門票與開放時間（2026 年 9 至 10 月查證），…」
  - `blocks[1]`: 「…門票、開放時間、車程都在 2026 年 9 至 10 月從官網查證過。…」 Leaving the intro at
    「9 月」 would have made it disagree with the new description. 「9 至 10 月」 is true for every
    reader-visible date in the pack: 清水寺, 東大寺, 大阪城 and the transport times are 2026-09-13,
    KANSAI RAILWAY PASS LITE is 2026-10-05 (#1258), and USJ is 2026-10-06.
  - The two table captions (`blocks[22]`, `blocks[24]`) are not touched: they cover only the
    transport tables, as the report says. No other text, number or source changed.
  - This supersedes the Notes line above that says the description and intro were left at 「2026 年 9 月查證」.
    The follow-up `2026-10-06-itinerary-osaka-kyoto-nara-full-recheck` still applies: it replaces
    「9 至 10 月」 with the recheck's own month, plus the captions, the summary and the self-references.
  - The report's headings are nested two levels down so they sit under this section; its text is
    otherwise unchanged.
- **Source re-opened for this pass** (Playwright from `/opt/node-tools` with
  `/opt/pw-browsers/chromium-1194/chrome-linux/chrome`, editorial UA, `networkidle` plus 7 s):
  `https://www.usjticketing.com/` HTTP 200, 「1 Day Studio Pass … Adult from ¥8,400〜 (incl. tax)」,
  1.5 Day ¥13,600〜, 2 Day ¥16,000〜, 「*Prices vary depending on the date of admission.」;
  `https://www.usj.co.jp/web/zh/tw/park-guide/schedule/park-hour2` HTTP 200, calendar renders
  2026-10 to 2026-12 (October 08:00〜22:00, one day 08:30〜21:30). So the USJ figures are October
  reads and 「9 至 10 月」 is accurate for the description's list.

### verify-1: PR #1330 `claude/usj-hours`, osaka-kyoto-nara-4-day-itinerary (zh-TW only)

Checker: independent round-1 verifier (did not write the change). Date: 2026-10-06. Mode: read-only.

#### Scope of the change
- `apps/api/app/guides/content/osaka-kyoto-nara-4-day-itinerary.json`: one paragraph rewritten (zh-TW `blocks[17]`, Day 4 USJ), plus `checked_on` 2026-09-13 → 2026-10-06 on the three USJ sources (`sources[8..10]`).
- The pack has only one locale (`zh-TW`), so there is no cross-locale comparison to make.
- Task files: `tasks/done/2026-10-05-itinerary-usj-september-hours.md` (closed), `tasks/open/2026-10-06-itinerary-osaka-kyoto-nara-full-recheck.md` (new follow-up).

#### Fetch method
- Every request used UA `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`, with no personal data in any header, query or form.
- `curl -sSL` on all three USJ sources: HTTP 200, but each is an app shell (usj.co.jp ~9 KB Angular shell, usjticketing.com 2.2 KB Vue shell) with no prices or hours. Not usable as a source.
- Rendered instead with Playwright 1.56.1 (`/opt/node-tools`) and `/opt/pw-browsers/chromium-1194/chrome-linux/chrome`, same UA, `networkidle` + 6-8 s wait.
  - Dumped `innerText` and the full DOM text.
  - Walked the hours calendar by clicking `[data-aui="nextMonth"]` until it disappeared (after 2026-12).
- Route images on the train-access page were downloaded with curl (200) and read visually.

#### Claim table (blocks[17] and the changed metadata)
| # | Claim | URL | HTTP | Verdict | Evidence |
|---|---|---|---|---|---|
| 1 | USJ is at 環球城站 on the JR 夢咲線 | https://www.usj.co.jp/web/zh/tw/access/train (+ image usj-gds-graphic-access-time-osaka-umeda-to-universal-city-tw-gallery-b.jpg) | 200 / 200 | CONFIRMED | Diagram: 西九條 → 「JR夢咲線」約5分鐘 → 環球城 |
| 2 | From 大阪站, take the 大阪環狀線 and change at 西九条 | same | 200 | CONFIRMED | 梅田／大阪 → JR大阪環狀線 約6分鐘 → 西九條. Note: the diagram also shows direct trains (「直達／經由西九條站 約11分鐘」); the article's wording is still correct. Unchanged sentence. |
| 3 | Hours differ by date | https://www.usj.co.jp/web/zh/tw/park-guide/schedule/park-hour2 | 200 (rendered) | CONFIRMED | Calendar lists per-day hours; page says 「營業時間可能不經預告逕自更改」 |
| 4 | Opening roughly 8:00-9:00 | same | 200 | CONFIRMED (to 2026-12-31) | Oct: 08:00 every day except 10/25 08:30. Nov: 08:00 / 08:30 / 09:00. Dec: 08:00 / 08:30 / 09:00. |
| 5 | Closing roughly 19:00-22:00 | same | 200 | CONFIRMED (to 2026-12-31) | Oct: 22:00 except 10/25 21:30. Nov: 19:00-22:00 (11/20, 11/27 at 19:00). Dec: 19:00-21:30. |
| 6 | 「少數日子更早閉園」 | same | 200 | CONFIRMED | 12/31 09:00〜17:00 |
| 7 | The official 「營業時間、時間表」 page has a calendar with each day's hours | same | 200 | CONFIRMED | Page heading 「營業時間、時間表」; calendar runs through 2026-12 only |
| 8 | Floating price, varies by admission date | https://www.usjticketing.com/ ; https://www.usj.co.jp/web/zh/tw/tickets | 200 / 200 | CONFIRMED | 「*Prices vary depending on the date of admission.」; 「* 價格依日期而有所不同。」 |
| 9 | 1 日影城入場券 adult 8,400 日圓起 | usjticketing.com | 200 | CONFIRMED | 「1 Day Studio Pass … Adult from ¥8,400〜 (incl. tax)」 |
| 10 | Adult means 12 and over | usj.co.jp/web/zh/tw/tickets | 200 | CONFIRMED | 「12歲以上者請購買成人票」 |
| 11 | 1.5 日券 13,600 日圓起 | usjticketing.com | 200 | CONFIRMED | 「1.5 Day Studio Pass (Visit Date 9/1~) … Adult from ¥13,600〜」; entry from 3:00 PM on day 1 (the article doesn't mention this, which is fine) |
| 12 | 2 日券 16,000 日圓起 | usjticketing.com | 200 | CONFIRMED | 「2 Day Studio Pass (Visit Date 9/1~) … Adult from ¥16,000〜」 |
| 13 | Prices include tax | usjticketing.com | 200 | CONFIRMED | 「(incl. tax)」 |
| 14 | usjticketing.com is the 「官方指定售票網站」 | https://www.usj.co.jp/web/en/us/tickets ; usjticketing.com | 200 / 200 | CONFIRMED | USJ's EN site links `https://www.usjticketing.com/` as 「Official Web Ticket Store」; the store says 「operated by JTRWeb LTD. - an authorised ticket reseller of Universal Studios Japan」 |
| 15 | 「2026 年 10 月 6 日的起價」 | usjticketing.com | 200 | CONFIRMED | Read today (2026-10-06); same three starting prices |
| 16 | Separate child ticket for ages 4-11 | usj.co.jp/web/zh/tw/tickets | 200 | CONFIRMED | 「若入場當日遊客年齡為4至11歲，請購買兒童票」 |
| 17 | The visit date is set at purchase | same | 200 | CONFIRMED | 「※購買影城入場券需要指定來園日期。請於購買時選擇您的來園日期。」 (date changes are possible afterwards; the article doesn't contradict this) |
| 18 | SNW: get an entry ticket in the official app, or buy a ticket with guaranteed entry in advance | https://www.usj.co.jp/web/zh/tw/enjoy/numbered-ticket ; usjticketing.com | 200 / 200 | CONFIRMED (unchanged sentence) | 「區域入場號碼券」 in the official app, switching to 「區域入場抽籤券」 when issued out; 「區域入場保證券」 obtainable in advance. Nuance: the requirement applies 「依照當天的現場狀況」, and the store says entry may sometimes be possible without one. Pre-existing wording, not touched by this PR. |
| 19 | The official site bans resale; tickets bought on auction sites are voided | usj.co.jp/web/zh/tw/tickets | 200 | CONFIRMED | 「警告：票券嚴禁轉售。」「在門票販售網站或拍賣網站上向轉賣者購買的門票，其QR Code將會無效且無法使用。」 |
| 20 | `checked_on` 2026-10-06 on the three USJ sources | the three URLs above | 200 | CONFIRMED | All three render today with the facts used. Titles match the pages. |

#### Task-file claims
| # | Claim | Verdict | Evidence |
|---|---|---|---|
| 21 | Calendar notes in the done task (10/6-10/31 08:00-22:00 except 10/25 08:30-21:30; Nov 08:00-09:00 open / 19:00-22:00 close; Dec 08:00-09:00 open / 19:00-21:30 close, 12/31 09:00-17:00; calendar ends at 2026-12) | CONFIRMED | Calendar walk, identical |
| 22 | Follow-up task: 16 of 20 sources still `checked_on` 2026-09-13; KANSAI LITE changed in #1258 on 2026-10-05; 「這篇／本文」 appears twice | CONFIRMED | Branch sources: 16 × 2026-09-13, 3 × 2026-10-06, 1 × 2026-10-05. `88459c4e … (#1258)`. blocks[1] 「這篇給一份」 and blocks[22] 「照本文行程不需要」 |

#### Internal and cross-pack consistency
| # | Check | Verdict |
|---|---|---|
| 23 | description and intro vs the Day 4 paragraph | INCONSISTENT (minor, non-blocking): see below |
| 24 | Shared numbers with `usj-guide.json` (zh-TW) | CONSISTENT: same 8,400 / 13,600 / 16,000 日圓起 |

Other internal checks: the Day 4 row of the overview table (「開園前 30 分鐘到」), the list in blocks[18] and the tip callout in blocks[26] do not conflict with the new paragraph.

##### The September wording (asked to decide)
- **description:** 「…環球影城的門票與開放時間（2026 年 9 月查證）」 names USJ explicitly with a September check date. The body now says the prices are 「2026 年 10 月 6 日的起價」, and the hours are no longer September figures.
- **intro (blocks[1]):** 「門票、開放時間、車程都在 2026 年 9 月從官網查證過」 is the same drift, in a softer form.
- **captions (blocks[22], blocks[24]):** both cover only the transport tables, not USJ, so they are not inconsistent with this change. blocks[22] already carries a mixed date (KANSAI LITE 2026-10-05) from #1258.

**Decision:** a real but low-impact inconsistency for readers.
- A reader sees two check dates for the same USJ facts.
- No number is misleading: the prices are the same on both dates, and the hours are now a range with a pointer to the calendar.
- The stale date understates freshness rather than overstating it.
- The PR defers it on purpose to `2026-10-06-itinerary-osaka-kyoto-nara-full-recheck`.

**Recommendation:** not a merge blocker. An optional one-phrase fix inside this PR's scope: remove 環球影城 from the description's 「（2026 年 9 月查證）」 list, or change that to 「2026 年 9 至 10 月查證」.

#### Summary
- Claims checked: 24. Confirmed: 22, plus 1 consistent shared-number check. Changed needed: 0 facts. Not found: 0. Consistency issues: 1 (minor, non-blocking).
- Time-sensitive state today:
  - Official calendar published through 2026-12-31 only. Today 08:00-22:00.
  - Store starting prices ¥8,400 / ¥13,600 / ¥16,000 incl. tax.
  - The store shows a maintenance notice: no purchases 10/13 22:00 to 10/14 06:00 JST. Not relevant to the article.
- Shared numbers: `usj-guide` matches on prices.
- Reader-first (changed paragraph only): no new 「本文／這篇」; one parenthetical attribution, the same pattern as before; no verification narration.
- Optional style note: 「營業時間每天不一樣」 could be read as literally different every day, whereas October is almost uniform. 「依日期不同」 would be more exact. Not a fact error.
- Self-checks: not re-run, because this check is read-only. The writer reports `pack_cli lint --slug` 0 errors and pytest 9 passed / 5 skipped. The `intake_check` FAILs it reports (no summary, `?city=`, two self-references) already exist on main.
- Suspected but outside this PR:
  1. `usj-guide.json` (five locales) still ties its hours to September 2026: 「2026 年 9 月閉園時間是 21:00 到 22:00」, 「9 月開園 8:00 到 9:00」, also in its diagram description. This is the same staleness this PR fixed in the itinerary. No open task covers it; worth filing.
  2. The SNW sentence in blocks[17] states the entry requirement flatly. Officially it applies depending on the day's conditions. The sentence predates this PR.
- Second round required: no (0 fact changes in this round).
