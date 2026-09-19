---
id: 2026-09-13-display-card-promises-language
title: 外觀與語言卡片其實沒有語言選項
status: review
priority: P3
area: web
owner: claude-fable-5-1
claimed_at: 2026-09-19T09:40:33Z
created_at: 2026-09-13T12:22:39Z
completed_at:
branch: claude/travel-scanner-pr-552-rpq36m
depends_on: []
scope:
  - apps/web/components/community/home.tsx
  - apps/web/lib/frontend-navigation.ts
  - apps/web/messages/en/community.json
  - apps/web/messages/ja/community.json
  - apps/web/messages/ko/community.json
  - apps/web/messages/zh-CN/community.json
  - apps/web/messages/zh-TW/community.json
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

- [x] 卡片的標題與內容一致：不是把語言選擇放進卡片，就是把標題改成只講外觀。

## Steps

- [x] 決定哪一邊改。放 `LanguageSwitcher` 進卡片會讓 /account 出現兩個語言選擇
      （卡片一個、下面的「語言」區塊一個），要一併處理。
- [x] 若改標題，`frontendCopy` 的 `display` 在 en／zh-TW／zh-CN／ja／ko 五個語系
      都要改，`npm run check:i18n` 不涵蓋 `frontend-navigation.ts`，得自己看過。

## How to verify

`npm run test:web`，再開 /my 與 /account 兩頁確認標題與卡片內容相符、
/account 不會出現兩個語言選擇。

## Notes

- 卡片本身的順序已在 2026-09-13 移到 `MyDirectory` 第一個位置，
  `discovery-navigation.test.tsx` 有一條順序斷言守著，改動時不要把它推回下面。

### 2026-09-19 done in repo (claude-fable-5-1)

- 選了改標題這一邊：卡片裡只有文字大小、外觀主題與全站配色，語言仍由頁首的
  `LanguageSwitcher` 與 /account 的「語言」區塊負責，所以 /account 不會多出第二個語言選擇。
- `apps/web/lib/frontend-navigation.ts` 的 `display` 五個語系改成只講外觀，用詞對齊卡片內
  三個控制項的標籤（`navigation.themeLabel`／`paletteLabel`／`textSizeLabel`）：
  en「Display settings」、zh-TW「外觀設定」、zh-CN「外观设置」、ja「表示設定」、ko「화면 설정」。
  key 名稱 `display` 不動：`home.tsx` 與 `discovery-navigation.test.tsx` 都靠它，那條順序
  斷言讀 `frontendCopy("zh-TW").display`，自動跟著新標題走，沒有碰它。
- 同一頁的登出提示 `community.signedOutBody`（五個語系的 `apps/web/messages/*/community.json`）
  原本寫「下面的外觀與語言設定不用登入就能改」：一樣許諾了語言，而且卡片 09-13 已移到提示
  上方，「下面」也錯了。改成「這一頁的外觀設定不用登入就能改」這種不指方向的說法，之後卡片
  再搬也不會又過期。這五個檔案原本不在 scope 內，改之前已先加進 scope；當時沒有任何
  in-progress／review 的票持有 `apps/web/messages` 底下的路徑。
- `home.tsx` 沒有需要改的地方（key 沒換，卡片內容不變）。
- 驗證：`npx vitest run components/discovery-navigation.test.tsx components/account-list-i18n.test.tsx
  components/frontend-plan-action.test.tsx "app/[locale]/page.seo.test.tsx" lib/frontend-flow.test.ts`
  36 passed；`npm run check:i18n`（5 locales × 25 namespaces）、`npm run lint:web`、
  `npm run typecheck:web` 皆通過。舊標題字串在 apps/web 的程式、訊息檔與 e2e spec 裡都已不存在。
  這個 session 沒有可開 /my 與 /account 的瀏覽器環境，「How to verify」的人工核對留給 PR review。
