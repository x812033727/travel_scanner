---
id: 2026-10-02-fare-lab-details-and-crawler-warnings
title: Fare lab comparison details and crawler warnings still reach readers as Chinese
status: done
priority: P3
area: api
owner: codex-fare-lab-ui-20261003
claimed_at: 2026-10-03T11:16:26Z
created_at: 2026-10-02T17:06:47Z
completed_at: 2026-10-03T11:33:03Z
branch: codex/unfinished-tickets-20261003
depends_on: []
scope:
  - apps/api/app/crawlers/airlines.py
  - apps/api/app/crawlers/back_to_back.py
  - apps/api/app/providers/live_back_to_back.py
  - apps/api/tests/test_airline_crawlers.py
  - apps/api/tests/test_back_to_back_fares.py
  - apps/api/tests/test_live_back_to_back.py
  - apps/web/components/airline-fare-lab.tsx
  - apps/web/components/back-to-back-fare-search.tsx
  - apps/web/components/live-back-to-back-search.tsx
  - apps/web/lib/fare-lab-copy.ts
  - apps/web/lib/fare-lab-copy.test.ts
  - apps/web/components/airline-fare-lab.test.tsx
  - apps/web/components/live-back-to-back-search.test.tsx
  - apps/web/lib/fare-lab-messages/en.json
  - apps/web/lib/fare-lab-messages/ja.json
  - apps/web/lib/fare-lab-messages/ko.json
  - apps/web/lib/fare-lab-messages/zh-CN.json
  - apps/web/lib/fare-lab-messages/zh-TW.json
---

# Fare lab comparison details and crawler warnings still reach readers as Chinese

## Why

`2026-09-11-fare-lab-warnings-and-copy` 把航班票價實驗室三個畫面改成五語系目錄
（`apps/web/lib/fare-lab-messages/`），倒買與即時倒買兩支 API 的 `warnings` 也都改成代碼。
但還有三種 API 寫好的繁中句子，原樣出現在每個語系的畫面上：

1. **比較卡的 `detail`**。`BackToBackFareService._comparison` 與 `search` 寫的
   「混搭航空公司的外站兩段票估算較省。」「…缺少第一趟一般票的公開快取票價，因此無法組成完整比較；
   這不是 0% 節省。」，以及 `LiveBackToBackService.search` 的「所有必要票價均來自同一次使用者主動即時比較。」。
   兩個元件都是 `<p>{comparison.detail}</p>`。
2. **一般來回分頁的警告**。`app/crawlers/airlines.py` 的 `AirlineFareCrawlerService` 寫
   `f"{adapter.name}：{detail}"`，`detail` 是 `CrawlerError.detail` 或 `disabled_reason`（繁中）。
   `test_warning_codes.py` 的 ratchet 抓不到它，因為漢字不在 append 那一行。
3. **來源卡的 `detail`**（`AirlineCrawlerSource.detail`）。目前畫面沒有顯示它，若之後要顯示，同樣要先改。

## Definition of done

- [x] 英文、日文、韓文讀者在三個分頁都看不到 API 寫的中文句子（比較說明與警告）。
- [x] `airlines.py` 的警告用 `app.warnings.warning_code`，airline 與失敗原因當參數；渲染端已經用
      `fareLabWarnings`，只要在 `lib/fare-lab-messages/*.json` 補 `warning.*` 鍵。
- [x] 比較說明改成代碼（例如沿用 warning 的 `code?name=value` 形狀放進 `detail`，或新增欄位），
      缺哪幾張票用 role 值列出，讓前端用 `ticketRole.*` 說出名稱。

## Steps

- [x] 先 grep 有沒有別的讀者讀 `detail`（2026-10-02 時只有倒買與即時倒買兩個元件顯示它；
      兩支 router 讀 `comparisons` 只為了決定扣不扣次，不看 `detail`）。
- [x] 決定 `detail` 的形狀，舊的冪等重播結果仍是中文句子，前端要讓非代碼字串原樣通過。
- [x] 補五語系文案與 `lib/fare-lab-copy.test.ts` 的案例。

## How to verify

```bash
cd apps/api && uv run pytest tests/test_back_to_back_fares.py tests/test_live_back_to_back.py tests/test_airline_crawlers.py tests/test_warning_codes.py -q
cd apps/web && npx vitest run lib/fare-lab-copy.test.ts components/airline-fare-lab.test.tsx components/live-back-to-back-search.test.tsx
```

## Notes

- 從 `2026-09-11-fare-lab-warnings-and-copy` 拆出來：那張票的範圍是畫面上寫死的中文與 ratchet 抓到的警告。
- `airline_fares` 是站主刻意關閉的功能之一，不急。

- 2026-10-03: Force-claimed only this fare ticket after the full 18-path gate: 2 open PRs, 34 remote heads, 430 local branch refs and 28 visible worktrees. PR #1172 API implementation is merged at b0a2645; its broad `apps/api/tests` review metadata now retains independent long-form/post-deploy acceptance only. Its task, owner and remaining gates are preserved. Local usage-settings changes match all five blobs in squash-merged PR #47. Two old OneDrive dirty files are AST-equivalent formatting residue of landed bases; those private bytes are preserved. Gate receipts: external `fare-collision-refresh-20261003/gate-verdict.json`, `collision-snapshot.json`, `remaining-ref-classification.json`, and `product-next-candidates-20261003/foods-maps-dirty-independent-classification.json`. No production access or feature enablement is authorized or performed.

- 2026-10-03 implementation: new public-fare warnings and `AirlineCrawlerSource.detail` use `warning_code` with airline and diagnostic reason codes; cached and live comparison details use code strings with mode, strategy and missing-role parameters. The five fare catalogs localize these values through the existing warning renderer. Old sentence-shaped cached/replayed Chinese text still passes through unchanged; unknown code-shaped text remains hidden. No price arithmetic, eligibility, usage charging, authentication, crawler policy, request timing, cache behavior or feature settings changed. The owner-disabled feature was not enabled.
- Regression proof: API `api-red-corrected.log` reports 16 assertion failures against original Chinese output (43 deselected); `api-final.log` reports 67 passed across `test_airline_crawlers.py`, `test_back_to_back_fares.py`, `test_live_back_to_back.py`, `test_warning_codes.py`. Public disabled/blocked/failed/empty/success, browser-capture empty, both comparison modes and verdicts, missing role order, and incompatible live fares are covered with offline fixtures. The initial draft RED included a misnamed private helper and is retained as non-authoritative; the corrected RED is the proof used here.
- Independent web tests by root: `fare-web-validation-20261003/red-final.log` has 26 new contract failures and 27 existing/legacy passes; after implementation all 53 cases across the three scoped web test files pass. Includes the same API-shaped values in all five locales, actual public/cached/live component rendering, old Chinese replay preservation and suppression of unknown codes. These are local component tests, not a deployed/browser/live-crawler acceptance claim.
- API Ruff and scoped mypy passed on all six changed API files. Only newly appended test blocks were formatted; unrelated historical formatting was preserved. Private validation directory: `C:/Users/x8120/.codex/tmp/fare-lab-i18n-20261003/`. Full web lint/typecheck/build and final PR checks are coordinated by root separately.
- During implementation main advanced to 4f8c381772a2e5cbfd66a80031dc07027874a7ef via PR #1174. Its full 13-file comparison has no Fare Lab path intersection; evidence `fare-collision-refresh-20261003/main-drift-1174.json`. No agent fetch, rebase, commit or push was performed.
