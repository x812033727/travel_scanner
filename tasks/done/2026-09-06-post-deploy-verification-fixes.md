---
id: 2026-09-06-post-deploy-verification-fixes
title: 上線後查核抓到的六個問題（大字閃爍、焦點掉回 body、標點與複數）
status: done
priority: P1
area: web
owner: claude-opus-5
claimed_at: 2026-09-07T01:20:00Z
created_at: 2026-09-07T01:20:00Z
completed_at: 2026-09-06T17:56:37Z
branch: claude/ux-simplify-public-2
depends_on: []
scope:
  - apps/web/app/[locale]/layout.tsx
  - apps/web/components/mobile-nav.tsx
  - apps/web/components/text-size-switcher.tsx
  - apps/web/components/account-panel.tsx
  - apps/web/components/account-panel.test.tsx
  - apps/web/lib/api.ts
  - apps/web/messages/en/foods.json
---

# 上線後查核抓到的六個問題（大字閃爍、焦點掉回 body、標點與複數）

## Why

PR #229 部署到 mokaair.com 之後，用 39 個獨立代理把線上站再走一次（公開頁 ×
桌機／手機、五個語系、深淺主題、首屏時間、兩個崩潰情境），每一條發現都由另一個
代理重跑一次試著推翻它。19 條成立，其中六條小到可以直接修：

1. **大字模式在第一次繪製之後才套用。** bootstrap 用 `next/script`
   的 `beforeInteractive`，實際被排進 `self.__next_s`，位置在 `</head>` 之後。量到
   的結果：localStorage 設 largest、4× CPU 節流，首頁 H1 先以 30px（root 16px）畫出來，
   再跳成 37.5px（root 20px），標題往下移 30px。改成 `<head>` 裡一支普通的 inline
   `<script>`（會擋 parser，本來就該這樣）。
2. **手機選單關掉後焦點掉回 `<body>`。** 開啟時焦點正確落在關閉鈕、9 次 Tab 都留在
   對話框裡，但 Escape 或按關閉之後 `document.activeElement` 是 BODY，鍵盤與螢幕
   閱讀器使用者被丟回文件開頭，要按三次 Tab 才回得到剛才那顆按鈕（WCAG 2.4.3）。
3. **英文 320px、特大字時「Standard」超出自己的按鈕框 9px。** 三顆固定 `grid-cols-3`
   在 81px 裡放不下 20px 的 Standard；zh-TW／ja／ko 都沒事，只有英文。
4. **`/account` 未登入時把 API 的句子和自己的句子黏在一起**：
   「請先登入後再繼續，請先登入。」改成跟 `/trips`、`/alerts` 一樣的單一入口。
5. **`/search` 把三則供應商訊息用 `。；` 串起來**（每則本來就有句號）。
   `lib/api.ts` 串接前先去掉句尾句號。
6. **`/en/foods` 出現六次「1 merchants」。** `cityCount` 改成 ICU plural。

## Definition of done

- [x] 大字模式沒有任何一格畫面是用錯的字級畫出來的（量測：before 2 格、after 0 格）。
- [x] 手機選單關閉後焦點回到開啟它的按鈕。
- [x] en 320px 特大字時三顆按鈕都在自己的框內。
- [x] `/account` 未登入只出現一句話與一顆按鈕。
- [x] 串接起來的錯誤訊息不再出現「。；」。
- [x] 英文的店家數量單複數正確。

## How to verify

```bash
cd apps/web && npx vitest run components/mobile-nav components/text-size-switcher components/account-panel lib/api.test.ts
node scratchpad/flash_check.mjs   # painted-at-the-wrong-size frames: production 2, this build 0
```

## Notes

- 查核用的 workflow 腳本與完整結果留在
  `.claude/projects/…/workflows/scripts/verify-mokaair-ux-deploy-*.js` 與
  `tasks/wzkat2vyz.output`（19 confirmed / 11 refuted）。剩下 13 條比較大的另外開任務。
- `next/script` 的 `beforeInteractive` 在 App Router 裡不等於「在 head 裡同步執行」。
  任何要在第一次繪製前決定外觀的東西（主題、字級）都要自己寫 `<script>` 進 `<head>`，
  並帶上 proxy 給的 nonce。
