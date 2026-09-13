---
id: 2026-09-13-adsense-slot-id-help
title: 文章頁 Google 廣告卡片的 slot ID 說明要擋住「填成客戶 ID」
status: done
priority: P2
area: web
owner: claude-opus-5
claimed_at: 2026-09-13T12:39:30Z
created_at: 2026-09-13T12:38:46Z
completed_at: 2026-09-13T12:52:43Z
branch: claude/unruffled-ptolemy-5bcb39
depends_on: []
scope:
  - apps/web/messages/*/admin.json
---

# 文章頁 Google 廣告卡片的 slot ID 說明要擋住「填成客戶 ID」

## Why

2026-09-13 站主在後台「文章頁 Google 廣告」卡片（provider `adsense`）的
`adsense_slot_id` 填了 `6710144873`。那是 AdSense「帳戶 → 帳戶資訊」頁上的**客戶 ID**，
不是廣告單元的 slot。兩者都是 10 位數字，所以格式檢查
（`apps/api/app/admin/service.py` 的 `re.fullmatch(r"[0-9]{10}", slot_id)`、
`apps/api/app/ads/service.py` 的 `SLOT_ID_PATTERN`）全部通過，卡片亮綠燈，
正式站文章頁輸出了 `<ins data-ad-slot="6710144873">`——一個不存在的版位。
已經手動改成真正的文中廣告單元 `5728135637`。

原本的說明只寫「in-article 廣告單元的 10 位數字」，沒說去哪裡找，也沒警告最容易拿錯的那個
10 位數字。

## Definition of done

- [x] 五語系 `admin.providerFields.adsense_slot_id.help` 都寫出值的來源
      （AdSense「廣告 → 按廣告單元」→ 文中廣告單元的 `data-ad-slot`，或清單上的 ID 欄），
      並明說不是「帳戶資訊」頁的客戶 ID。
- [x] 合法的 slot ID 仍然照常通過，驗證規則沒有變嚴。

## Steps

- [x] 改 zh-TW、zh-CN、en、ja、ko 五份 `admin.json` 的說明文字。
- [x] 評估 API 能不能直接擋掉「等於客戶 ID」的值（結論見 Notes：不能，沒做）。
- [x] `npm run lint:web && npm run check:i18n && npm run typecheck:web && npm run test:web`。

## How to verify

打開 `/admin/settings`，找到「文章頁 Google 廣告」卡片，「文中廣告單元 slot ID」欄位標籤下方的
灰色說明文字，五個語系都應該看到來源路徑與「不是客戶 ID」的警告。
`npm run check:i18n` 確認五語系的鍵一致；`npm run test:web` 全過（249 檔、2712 個測試）。

## Notes

- **API 端沒有乾淨的訊號可擋。** 客戶 ID 是 AdSense 帳戶自己的 10 位流水號，和
  `adsense_publisher_id`（`ca-pub-` 加 16 位）的數字沒有推導關係，本地無從比對；
  要知道真正的客戶 ID 或列出現有廣告單元只能呼叫 AdSense Management API，這張票明訂不加對
  Google 的網路呼叫。所以只改說明文字。
- 另外兩個想過但沒做的方向：把 `6710144873` 這個值寫死進黑名單（只擋得住這一個帳戶的這一次）、
  以及在卡片上顯示「slot 是否真的有廣告填充」（要走 AdSense 報表 API，同樣是網路呼叫）。
- en、ja、ko、zh-CN 的 AdSense 選單名稱（Ads → By ad unit、広告 → 広告ユニットごと、
  광고 → 광고 단위 기준、广告 → 按广告单元；帳戶資訊頁對應 Account information／アカウント情報／
  계정 정보／账号信息）是照 AdSense 各語系介面的慣用譯名寫的，沒有登入各語系後台逐一核對；
  如果站主用的介面語系字面不同，改說明文字即可。
