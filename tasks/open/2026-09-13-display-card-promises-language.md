---
id: 2026-09-13-display-card-promises-language
title: 外觀與語言卡片其實沒有語言選項
status: open
priority: P3
area: web
owner:
claimed_at:
created_at: 2026-09-13T12:22:39Z
completed_at:
branch:
depends_on: []
scope:
  - apps/web/components/community/home.tsx
  - apps/web/lib/frontend-navigation.ts
---

# 外觀與語言卡片其實沒有語言選項

## Why

`MyDirectory`（/my 與 /account 兩頁共用）最上面那張卡的標題，五個語系都寫成
「外觀與語言」（en: Display & language，ja: 表示と言語…），但卡片裡只有文字大小、
外觀主題與全站配色三項，沒有任何語言選擇。語言只出現在頁首的
`LanguageSwitcher`，以及 /account 另外一個「語言」區塊裡。

所以在 /my 讀到這張卡的人，會照著標題在卡片裡找語言，找不到；把它移到頁面最上面
（2026-09-13，PR 待開）之後更明顯，因為它現在是進入頁面第一眼看到的東西。

## Definition of done

- [ ] 卡片的標題與內容一致：不是把語言選擇放進卡片，就是把標題改成只講外觀。

## Steps

- [ ] 決定哪一邊改。放 `LanguageSwitcher` 進卡片會讓 /account 出現兩個語言選擇
      （卡片一個、下面的「語言」區塊一個），要一併處理。
- [ ] 若改標題，`frontendCopy` 的 `display` 在 en／zh-TW／zh-CN／ja／ko 五個語系
      都要改，`npm run check:i18n` 不涵蓋 `frontend-navigation.ts`，得自己看過。

## How to verify

`npm run test:web`，再開 /my 與 /account 兩頁確認標題與卡片內容相符、
/account 不會出現兩個語言選擇。

## Notes

- 卡片本身的順序已在 2026-09-13 移到 `MyDirectory` 第一個位置，
  `discovery-navigation.test.tsx` 有一條順序斷言守著，改動時不要把它推回下面。
