---
id: 2026-09-11-trip-editor-close-guard-order-dependence
title: trip-editor 的關閉守門測試會隨檔案順序變紅
status: open
priority: P1
area: web
owner:
claimed_at:
created_at: 2026-09-11T17:16:50Z
completed_at:
branch:
depends_on: []
scope:
  - apps/web/components/trip-editor.test.tsx
  - apps/web/components/trip-editor.tsx
---

# trip-editor 的關閉守門測試會隨檔案順序變紅

## Why

`components/trip-editor.test.tsx` 的 `disables arrange and adjustment navigation until itinerary generation finishes` 會隨著**測試檔案的數量與順序**而變紅——單獨跑一定過，整套跑有時不過。

實際觀察到的（同一台機器、同一個 commit 連跑兩次都紅）：

```
commit 17cd7b2（在 main 9548f3f 之上只有這一個 commit）
npm run test:web
  ❯ components/trip-editor.test.tsx (67 tests | 1 failed) 27690ms
  FAIL … > disables arrange and adjustment navigation until itinerary generation finishes
  components/trip-editor.test.tsx:292:19
  TestingLibraryElementError: Unable to find an accessible element with the role "dialog"
```

對照：

| 樹 | 結果 |
| --- | --- |
| `origin/main`（9548f3f） | 225 files / 2288 tests 全過 |
| `17cd7b2`（多了三個 i18n 測試檔） | trip-editor 那一條紅，連兩次 |
| 再往後（又多了 `lib/warnings.test.ts` 等） | 228 files / 2304 tests 全過 |

那個 commit 沒有動 `trip-editor.tsx`，也沒有動它用到的任何元件；動的是 catalog 與三個新測試檔。所以這不是行為壞掉，是**那條斷言對執行順序或時間敏感**。

失敗的那一行是 `:292`：

```ts
fireEvent.click(within(assistant).getByRole("button", { name: "關閉" }));
fireEvent.keyDown(document, { key: "Escape" });
expect(screen.getAllByRole("dialog")).toEqual([assistant]);   // ← 這裡彈層已經不在了
```

也就是說：預覽在途時「關閉」應該被守門擋掉，但在某些執行順序下它真的把彈層關掉了。這和 `2026-09-11-planner-overlay-close-guard-race`（關閉鈕在儲存在途時被靜默吞掉）講的是同一個守門，方向相反。

## Definition of done

- [ ] 找出為什麼這條斷言會隨順序改變結果。
- [ ] 要嘛把守門修成確定性的，要嘛把測試改成不依賴時序的寫法——但**不可以**只是放寬斷言把紅色藏起來。
- [ ] 連續跑三次整套 `npm run test:web` 都綠。

## Steps

- [ ] 重現：`git checkout 17cd7b2 && npm run test:web`。
- [ ] 用 `--reporter=verbose` 看 trip-editor 前一個執行的檔案是誰，確認是不是跨檔污染（`vitest.setup.tsx` 的 `translators` Map、`document.documentElement.lang`、未清掉的 timer 都是嫌疑）。
- [ ] 那個檔案跑了 27.7 秒 / 67 個案例，`testTimeout` 只有 5 秒；也要排除單純是機器負載造成的。

## How to verify

```bash
cd apps/web && npx vitest run components/trip-editor.test.tsx   # 單獨跑會過，要整套跑才重現
```

## Notes

- 目前 HEAD 整套是綠的，所以這不是擋著不能合併的問題；但它會在別人加測試檔時毫無預警地變紅，而且看起來像是那個人改壞的。
- 我沒有放寬那條斷言，也沒有把它 skip 掉——那會讓守門的行為失去保護。
