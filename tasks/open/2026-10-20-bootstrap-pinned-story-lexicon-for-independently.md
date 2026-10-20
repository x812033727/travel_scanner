---
id: 2026-10-20-bootstrap-pinned-story-lexicon-for-independently
title: Bootstrap pinned story lexicon for independently reviewed manual drafts
status: review
priority: P2
area: tools
owner: codex-gpt6-netflix-bootstrap
claimed_at: 2026-10-20T14:16:49Z
created_at: 2026-10-20T13:57:02Z
completed_at:
branch: codex/brand-story-netflix-x03
depends_on: []
scope:
  - tools/video/core/lexicon-manual-bootstrap.mjs
  - tools/video/core/lexicon-manual-bootstrap.test.mjs
  - tools/video/lexicon-manual-bootstrap.mjs
  - docs/videos/story-lexicon-manual-bootstrap.md
  - tasks/open/2026-10-20-bootstrap-pinned-story-lexicon-for-independently.md
---

# Bootstrap pinned story lexicon for independently reviewed manual drafts

## Why

X03 Netflix 是獨立審過的本機手稿，已有 `video.json`，但沒有工人的 `auto.json`／章稿和任何媒體。一般故事 genesis 正確拒絕既有 `video.json`；舊故事 migration 又要求真正的工人章稿，不能拿它或偽造工作狀態繞過防護。要在有來源與盲讀收據的前提下，將這種尚未開口的手稿安全綁定 immutable 發音詞庫。

## Definition of done

- [x] 有獨立唯讀預檢及明確 `--apply` CLI；稿、系列、三份審查證據 SHA 必須一致，既有媒體或交易一律拒絕。
- [x] 套用時雙租約、兩邊 intent、immutable genesis／provenance sidecar、嚴格讀回與 committed receipt；重跑不再改寫。
- [x] 交易開始前、committed receipt 前重新比對六份輸入 SHA，並拒絕指回儲存庫的媒體路徑及其 symlink 祖先。
- [x] 交易中斷前後可分辨：未 committed 保持 HOLD；已 committed 且 sidecar 相符者可用交易 UUID 恢復。
- [x] 集中測試與相關工具檢查完成；本案交回 X03 製作票後才由協調者決定何時建立實際審查收據並套用。

## Steps

- [x] 避開舊 migration 和主影片 CLI 的既有任務 scope，在新模組與獨立 CLI 實作。
- [x] 測試乾跑無寫入、憑證漂移、既有媒體、symlink、中斷及恢復。
- [x] 跑完整相關檢查、檢視 diff 並把分支交協調者。

## How to verify

`node --test tools/video/core/lexicon-manual-bootstrap.test.mjs`；`npm run test:tools`；`npm run check:tasks`；`git diff --check`。CLI 用法與收據格式在 `docs/videos/story-lexicon-manual-bootstrap.md`。

## Notes

2026-10-20：現有舊故事遷移的唯讀檢查對 X03 回 `STORY_LEXICON_MIGRATION_WORKDIR_UNPROVEN`，因 X03 根本沒有工人工作目錄；其 `video.json` SHA `b65241c55c35f6692cac89e3af4e5aa651b6664025c33890e497846346e722a4` 已被來源審查與兩份盲讀收據引用。一般 `initializeStoryLexicon` 因既有 `video.json` 回 `STORY_LEXICON_MIGRATION_REQUIRED`。新工具仍需 X03 獨立 reviewer 的結構化 bootstrap 收據才准 `--apply`，所以目前只用合成測試驗證，真實 X03 未寫入詞庫、未付費生成。

同日驗證：新增集中測試 9/9 通過；`npm run test:tools` 2,586 通過、0 失敗、5 既定跳過；`npm run test:docs-videos` 236/236 通過；`npm run check:tasks` 通過（僅既有過期／重疊任務警告）；`git diff --check` 通過。其他代理既有 scope 覆蓋 `tools/video/cli.mjs`、`lexicon-store.mjs` 和舊 migration，故本票刻意使用獨立 CLI 及新模組。協調者接手時建立 `reviews/lexicon-bootstrap.json`（格式見設計文件）並先乾跑；`--apply` 只在仍無 X03 媒體的情況下執行。

二次審查發現兩個競態邊界：`now()` callback 可在來源讀取後改稿，舊版仍可能寫出 `bootstrapped:true`；symlink 媒體 base 可讓字面上的儲存庫外路徑實際指進儲存庫。已補提交前兩次來源 SHA 比對與媒體路徑祖先/realpath 檢查；focused 回歸涵蓋六份檔案在這兩個提交時點各自漂移，以及 symlink 指向 repo 的 `--apply`/`--recover` 拒絕。真實 X03 仍未套用。

修補後再驗：focused 12/12；`npm run test:docs-videos` 246/246；`npm run test:tools` 2,590 通過、0 失敗、5 既定跳過；`npm run check:tasks` 與 `git diff --check` 通過。實際 X03 CLI 僅做唯讀乾跑，安全路徑與空工作區檢查通過，因最終結構化審查收據尚未存在而如預期拒絕套用；未產生 X03 LEASE 或媒體。

交接後實際驗證：X03 定稿 `video.json` SHA-256 `647b73fdb22a2452ad2817ca5554689db5801af0e97996913e7e73c1694b2fb9` 已取得一份來源與兩份獨立敘事 PASS 收據；獨立審查者建立 `reviews/lexicon-bootstrap.json`，唯讀檢查 7/7 通過，正式 `--apply` 回 `bootstrapped:true`。提交交易 `640c455f-0c37-42b5-89d9-ea897fe6e3a5` 的工作區 receipt 與儲存庫 genesis/current/sidecar 均存在，後續真實 X03 `lint` 為 0 錯誤／0 警告、`tts --dry-run` 顯示 78 次合成請求與足夠額度。付費語音與成片驗收歸 X03 製作票處理。
