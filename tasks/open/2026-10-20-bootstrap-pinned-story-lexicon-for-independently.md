---
id: 2026-10-20-bootstrap-pinned-story-lexicon-for-independently
title: Bootstrap pinned story lexicon for independently reviewed manual drafts
status: open
priority: P2
area: tools
owner:
claimed_at:
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
