---
id: 2026-09-06-admin-session-settings
title: 後台的登入時效設定要能真的生效
status: in-progress
priority: P3
area: api
owner: claude-fable-5-1
claimed_at: 2026-09-06T07:55:01Z
created_at: 2026-09-06T00:54:26Z
completed_at:
branch: claude/p3-polish
depends_on: []
scope:
  - apps/api/app/auth/service.py
  - apps/api/app/admin/service.py
---

# 後台的登入時效設定要能真的生效

## Why

使用者要求「登入時效可以在後台調」。我做過一版 UI，欄位存得進資料庫，但**完全沒有
作用** —— 因為認證路徑讀的是 `get_settings()`，那是 `@lru_cache` 的純環境變數版本；
資料庫的覆寫要透過 `load_runtime_settings(session)` 才會生效，而 auth 沒有用它。

當時的處理是**整個撤掉那版 UI**，理由是「不留看得到卻沒作用的設定」。所以現在的狀態
是：時效只能改 `.env` 然後重新部署（目前正式機 `ACCESS_TOKEN_EXPIRE_MINUTES=1440`，
絕對上限 `session_absolute_max_days=30`）。

## Definition of done

- [ ] 管理員在後台改登入時效，**不重新部署**就會影響新發的 token。
- [ ] 或者：明確決定這個設定不進後台，並把理由寫在文件裡，讓下一個人不用重新發現一次。

## Steps

- [ ] 先確認要不要做。`.env` + 重新部署其實可以接受，只是慢；把設定搬進後台的代價是
      要在每次認證都碰資料庫，或者做一層有 TTL 的快取。
- [ ] 若要做：讓 `create_access_token` / `should_renew_session` / `session_past_absolute_cap`
      能拿到執行期設定。注意這三個函式目前是同步的、沒有 session，改動面不小。
- [ ] 加測試證明「後台改了值 → 新 token 的 exp 跟著變」，這正是上一版缺的東西。

## How to verify

改完之後在容器裡：後台改成 X 分鐘 → 重新登入 → 解 token 看 `exp - iat` 是不是 X。
不要只驗證欄位存進資料庫，那是上次犯的錯。

## Notes

**不要動 `should_renew_session` 讀設定的方式**。它現在刻意用 token 自己的壽命
（`claims.expires_at - claims.issued_at`）而不是當下的設定值。原因：如果讀當下設定，
把壽命從 60 分鐘調長到 480 分鐘的那一刻，所有既有 token 的續期點會被推到它們自己的
過期時間之後 —— 一個「讓大家登入更久」的改動會把所有人踢出去。這個坑我踩過並在
PR #145 修掉，請保留那個註解。

相關脈絡：`jti` 現在代表「整次登入」而不是「其中一個 token」，續期時會把原本的 jti
帶過去，這樣登出才能終止整條續期鏈（同樣是 #145）。改認證路徑時不要破壞這個性質。
