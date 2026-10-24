---
id: 2026-10-24-prepare-c14-camelbak-approved-canonical-video
title: Prepare C14 CamelBak approved canonical video project
status: done
priority: P1
area: docs
owner: codex-c14-canonical
claimed_at: 2026-10-24T07:47:39Z
created_at: 2026-10-24T07:47:29Z
completed_at: 2026-10-24T07:54:46Z
branch: codex/c14-camelbak-canonical-20261024
depends_on: []
scope:
  - docs/videos/story-everyday-camelbak-c14/build-canonical.mjs
  - docs/videos/story-everyday-camelbak-c14/video.json
  - docs/videos/story-everyday-camelbak-c14/series.json
  - docs/videos/story-everyday-camelbak-c14/brief.md
  - docs/videos/story-everyday-camelbak-c14/claims.md
  - docs/videos/story-everyday-camelbak-c14/verify-1.md
  - docs/videos/story-everyday-camelbak-c14/preflight.mjs
  - docs/videos/story-everyday-camelbak-c14/reviews/canonical-video-preflight-20261024.md
---

# Prepare C14 CamelBak approved canonical video project

## Why

C14 的 70 句繁中劇本與 70 鏡方向已有站主按四個來源雜湊核准，仍缺正式影片工具可讀的專案檔。未轉檔就無法做同一份稿件的非付費預檢；既有紙上「496.5 秒正文」也混入了片頭前的 40.3 秒冷開場。

## Definition of done

- [x] 四份核准原件保持原位且 SHA-256 不變；正式專案逐句、逐鏡對應 70／70，54 張概念插圖、16 張後製字卡。
- [x] 重跑產生器可核對生成檔完全相同；schema、lint、來源 ID 和分鏡預檢有收據。
- [x] 收據明列片頭後正文紙估 456.2 秒、小於 480 秒，實際 TTS、付款與預算路由均 HOLD；沒有媒體生成或匯入。

## Steps

- [x] 綁定站主核准 SHA，逐行轉換 script 與 visual JSON，產生正式專案、系列、主張與既有來源判定對接。
- [x] 執行非付費預檢、必要工具檢查與獨立只讀覆核；寫入精確收據並結案任務。

## How to verify

- `node docs/videos/story-everyday-camelbak-c14/build-canonical.mjs --check`
- `node docs/videos/story-everyday-camelbak-c14/preflight.mjs`
- `node tools/video/cli.mjs lint --slug story-everyday-camelbak-c14`
- `npm run check:tasks`; `git diff --check`

## Notes

- 站主核准收據：`docs/videos/story-everyday-camelbak-c14/reviews/owner-script-approval.md`。舊稿頁首的「待覆核」文字早於該收據，不能為改狀態而動原件。
- `production-quote.md` 是未核准提案。C14 沒有可歸因且已讀回的單集帳本、舊費用與供應商正式帳戶實價，因此第一筆付費請求仍不可送。
- 獨立非作者轉檔核查 PASS：70／70 文字與視覺一致、54／16、9 項實際引用來源，`preflight` 0 lint errors／9 warnings；18 個 `say` 僅為待試聽候選。收據見 `reviews/canonical-video-preflight-20261024.md`。
- `npm run test:docs-videos` 已啟動；本票不把尚未回傳的廣域測試宣稱 PASS。69 項聚焦 schema／lint／facts 測試已通過。
