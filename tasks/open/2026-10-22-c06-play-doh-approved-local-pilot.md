---
id: 2026-10-22-c06-play-doh-approved-local-pilot
title: C06 Play-Doh approved local pilot and lexicon genesis
status: blocked
priority: P2
area: docs
owner: codex-gpt6-c06-pilot
claimed_at: 2026-10-22T05:28:11Z
created_at: 2026-10-22T05:28:05Z
completed_at:
branch: codex/brand-story-play-doh-c06-pilot
depends_on: []
scope:
  - docs/videos/story-everyday-play-doh-c06/reviews/owner-script-production-approval.md
  - docs/videos/story-everyday-play-doh-c06/story-lexicon
  - docs/videos/story-everyday-play-doh-c06/production-pilot.md
---

# C06 Play-Doh approved local pilot and lexicon genesis

## Why

站主於 2026-10-22 分別核准 C06 Play-Doh 的 PR #1676 劇本與分鏡，以及本機試片最多 80 張插圖、每張最多三次、94 句旁白與一首配樂、整支 US$25 停線。C06 原劇本工作樹已有 `video.json`，正常新故事發音字典初始化因此拒絕；必須從尚未有該檔的企劃提交建立可讀回的專屬字典，再執行付費前檢查。

## Definition of done

- [x] 稿件與成本核准綁定確切檔案雜湊，範圍限本機試片，沒有上傳或發布。
- [x] C06 專屬發音字典以新故事 genesis 建立且嚴格讀回，沒有偽造舊工作狀態。
- [ ] 先合成並檢查正文配音；正文純語音至少 480 秒才允許圖片、配樂與組片，所有實際花費與暫停原因留收據。

## Steps

- [x] 核對既有工作樹、PR、稿件雜湊、C06 工作資料夾不存在與全域 STOP 不存在，認領獨立製作票。
- [x] 自 C06 Treatment 精確提交 `3e49a964aa61f20fcf12743140984588a6a1c488` 建立工作樹，於 `video.json` 不存在時初始化字典並嚴格讀回 sequence 1。
- [x] 接入 PR #1676 精確稿件，寫入兩項站主核准收據及整支停線，執行 `tts --dry-run`。
- [ ] 按配音、時長、音訊查核、插圖、配樂、組片順序推進；每階段檢查可核算成本與品質，留下持續或停線紀錄。

## How to verify

`videoLexicon({root,slug,workdir,requireSnapshot:true})` 嚴格讀回；`Get-FileHash` 比對稿件與逐鏡；`node tools/video/cli.mjs lint --slug story-everyday-play-doh-c06`、`tts --dry-run`、實際音檔與 timeline 秒數讀回、ledger 及產物 QA；`npm run check:tasks`、針對性影片文件檢查。

## Notes

- 2026-10-22 05:28 UTC：新故事 genesis 成功，sequence 1、lexicon SHA256 `7dfd45e09466d424522c405627249ae59c42716572c7246979507bfff09c2477`、head event SHA256 `42b422ea8a45c866fb5fabd0a29e18ae74a15412a39dde1802a721dd13f8caa7`；原 C06 工作資料夾在初始化前不存在。
- 2026-10-22 05:32 UTC：核准稿件／逐鏡三檔的 SHA-256 全與 PR #1676 相同；`lint` 0／0、`tts --dry-run` 94 個請求、約 2,716 計費字元，伺服器本月額度足夠。script gate 已寫入本機 `approvals.json` 並讀回 SHA。
- 2026-10-22 05:33 UTC：正式 TTS 在供應商 HTTP 429 停下；無任何 WAV、timeline、narration，工作租約已釋放，本集媒體帳本 US$0.00。依製作順序停止，正文 480 秒未通過，沒有買圖。下一次先核對額度與工作日誌，再續配音。
- 本機驗證：C06 `lint` 0 errors／0 warnings，`lexicon-store.test.mjs` 10／10 PASS，`check:tasks` PASS。`test:docs-videos` 235／236 通過；唯一失敗在無關的 `imported-long-languages/runner.test.mjs:679`，Windows 子程序 exit `3221226505` 且 stdout/stderr 皆空，C06 原劇本分支先前亦重現。沒有為這項既有環境失敗擴改工具或影片稿件。
