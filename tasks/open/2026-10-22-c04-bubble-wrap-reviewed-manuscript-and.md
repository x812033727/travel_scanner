---
id: 2026-10-22-c04-bubble-wrap-reviewed-manuscript-and
title: C04 Bubble Wrap reviewed manuscript and full-film quote
status: review
priority: P2
area: docs
owner: codex-gpt6-c04-script
claimed_at: 2026-10-22T02:28:22Z
created_at: 2026-10-22T02:28:18Z
completed_at:
branch: codex/brand-story-bubble-wrap-c04-reviewed-script
depends_on: []
scope:
  - docs/videos/story-everyday-bubble-wrap-c04
---

# C04 Bubble Wrap reviewed manuscript and full-film quote

## Why

站主已選「採用 C04 企劃方向」，但這只採用 Bubble Wrap 的 Treatment，不等於逐字稿、分鏡、成本或付費核准。下一階段要把六章因果主線落成可查核的約十分鐘逐句稿與本機漫劇格式分鏡，遵守「日用品的意外轉身」沿用奇聞檔案局的畫面、配樂和鉤子規則。提交整支張數與總額之前，不呼叫 TTS、圖片或配樂。

## Definition of done

- [x] 留下綁定 Treatment SHA-256 的站主企劃決定收據，清楚排除逐字稿、費用及上傳核准。
- [x] 六章逐句稿與約十分鐘 `video.json` 連成一條故事，具可回收的 30–45 秒實質鉤子、濃縮片頭，並標出 5 秒片頭動畫、21 秒片尾動畫與可點連結的後製位置。
- [x] 全部年份、發明人、專利用途與 IBM／溫室等公司回顧均可逐句追至一手來源；另一代理留獨立事實查核收據，兩位讀者各自盲評敘事。
- [x] Curio 可愛插圖占比至少七成、連續卡最多三張、卡片單焦點；本機 lint、純旁白時長估算、整支圖片張數與費用上限可供站主審閱。
- [x] 本輪沒有付費媒體、TTS、上傳或發布，也沒有借用 C03 的 US$25 授權。

## Steps

- [x] 寫企劃決定收據、讀現行規則與 C01／C02 格式，在新分支凍結來源界線。
- [x] 寫六章旁白和逐鏡 `video.json`／`series.json`，核對鉤子、畫面比例與片頭片尾。
- [x] 請獨立代理逐句核源、兩位讀者盲評，修正後重新檢查雜湊。
- [x] 跑本機 lint 與成本 dry-run，留下完整報價和驗證結果；提交疊在 C04 Treatment PR 的草稿 PR。

## How to verify

以 `node tools/video/cli.mjs lint --slug story-everyday-bubble-wrap-c04`、`npm run test:docs-videos` 的相關檢查、`npm run check:tasks` 及 `git diff --check` 驗證；另用程式統計場景／卡片／插圖／連續卡與旁白字數、估算旁白時長。成本只跑 `--dry-run`，沒有 paid POST。逐句來源表及盲評收據需綁定最後一版內容 SHA-256。

## Notes

2026-10-22 在隔離 `codex/brand-story-bubble-wrap-c04-script` 草稿分支先認領，基底為 C04 Treatment commit `4fcf282b8`、草稿 PR #1668。為按正式時序在第一份 `video.json` 前建立故事專屬字典，將最終工作轉入同基底、同票的隔離分支 `codex/brand-story-bubble-wrap-c04-reviewed-script`；轉移和雜湊比對記於 `docs/videos/story-everyday-bubble-wrap-c04/reviews/transfer-and-lexicon.md`。其 Treatment 已有獨立來源覆核；這一份事實核准不能延伸到新稿。系列 `story-` slug 的 Curio 視覺自動 lint 仍依賴另一張 guard PR #1667，提交前須另行統計確認，不以 story lint 綠燈代表畫面比例通過。

最終稿 `draft-lines.tsv` SHA-256 `39198B822F0F32F2162884DE6ED1030B4BCA0FF380BD09E0525893CB92915DB0`、`video.json` SHA-256 `1BB9FD7355E6BFA5FCFA8D9A4BCFB0F89F2A5F01451131BDC3754B12243B330B`。獨立來源查核 94／94 PASS、兩位新雜湊盲讀 PASS、視覺逐鏡預檢 PASS；IBM 包材關聯仍只按 Sealed Air 後來的回顧講，核發文本未冒稱原始申請稿或當年量產。`lint` 0 errors／0 warnings，手算 84 張插圖＋10 張單焦點卡、最長連卡 1；`npm run test:docs-videos` 在 bundled Node v24.19.0 為 236／236 PASS，`npm run check:tasks` PASS。第 02–06 章 2,558 漢字／300 字每分鐘僅估 8:32；實測 TTS 若少於 480 秒須先停線，不能買圖。全片可見圖像最多三次加一首配樂估 US$3.48，另有語音／音訊等未拆帳；擬請 C04 整支 US$25 停線上限尚未獲站主核准。本輪全程零付費媒體、零上傳。

腳本草稿 PR [#1670](https://github.com/x812033727/travel_scanner/pull/1670) 疊在 Treatment PR #1668，標記 `no-auto-merge`，本票保持 `review` 等站主審稿及費用決定。`check:tasks` 的前述 PASS 是執行 `tasks done` 前；該指令寫下未追蹤的 `tasks/done/` 副本後未能移走 `tasks/open/` 原件，自動政策又拒絕一次精確路徑刪除。副本**沒有**納入 PR，故本機目前的 `check:tasks` 會因重複 ID 失敗；不要把此環境殘留誤當成已結案，亦不可用其他刪除手法繞過政策。
