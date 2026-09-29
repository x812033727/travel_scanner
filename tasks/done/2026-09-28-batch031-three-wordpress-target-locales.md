---
id: 2026-09-28-batch031-three-wordpress-target-locales
title: Batch031 three WordPress target language drafts
status: done
priority: P1
area: docs
owner: codex-p1-audit
claimed_at: 2026-09-29T02:12:12Z
created_at: 2026-09-28T01:09:10Z
completed_at: 2026-09-29T02:12:17Z
branch: codex/p1-task-audit
depends_on: []
scope:
  - apps/api/app/guides/content/wordpress-member-registration.json
  - apps/api/app/guides/content/wordpress-security-basics.json
  - apps/api/app/guides/content/wordpress-social-login.json
  - apps/web/public/guides/wordpress-member-registration
  - apps/web/public/guides/wordpress-security-basics
  - apps/web/public/guides/wordpress-social-login
  - docs/article-localization/batch031-content-draft-evidence.md
  - tasks/open/2026-09-28-batch031-three-wordpress-target-locales.md
---

# Batch031 three WordPress target language drafts

## Why

These three public WordPress guides have a published zh-TW source, but their
en, ja, ko, and zh-CN documents and localized diagram/cover assets remain in
separate Batch031 Pair A/B commits. Integrate their reviewed content into a
draft code PR while preserving the existing zh-TW source and public state.

## Definition of done

- [x] Each of the three packs contains the existing zh-TW document unchanged
      plus four complete target-language documents.
- [x] Exactly 36 localized assets are added; original assets remain unchanged.
- [x] A draft PR records exact source and asset hashes, checks, and publication
      gates. No deployment, database import, or publication occurs.

## Steps

- [x] Claim the narrow three-pack and three-asset-directory scope.
- [x] Bring in Pair A/B content without cherry-picking their unrelated task files.
- [x] Recheck the 12 target documents and 36 assets against Pair commits and
      inspect native-size visual renders.
- [x] Run pack lint, focused API checks, task checks, and exact diff review.
- [x] Open draft PR #879 and keep the source-publication gate explicit.

## How to verify

Run `uv run python -m app.guides.pack_cli lint --kind life --slug` for each
article in `apps/api`, focused guide tests, `npm run check:tasks`, and
`git diff --check`. Compare the four target-locale JSON documents and twelve
localized asset hashes per article to Pair A/B commit blobs.

## Notes

Pair A commit `b885927df5ee0bc6a13b1a1e93b9457eaa3dba3f` supplies
`wordpress-member-registration` and `wordpress-security-basics`; Pair B
commit `e8fa87d9abb0969a5c9861e5b0b551757cd47ba6` supplies
`wordpress-social-login`. `wordpress-user-roles` is excluded because the
active #875 source-correction task owns that pack until its source revision is
published and its task is released/done. This code PR must not imply any
target locale is live.

The three packs and 36 assets match Pair Git blobs exactly. Pack lint found
zero errors; 78 focused API tests passed with seven skips. All 24 SVGs parsed,
all 12 JPGs decoded at 1600×900, and twelve four-locale contact sheets were
visually checked. See `docs/article-localization/batch031-content-draft-evidence.md`
for the complete document and asset hashes. Rebased on merged #875 at
`4b6c5cd99fa9eab3b658d5b6cf639cb001f8fc3e`; repeated source, target,
asset, task, and diff checks against that exact base.


## 2026-09-29 標記完成（由站主授權，非原持有者）

站主要求逐張核對原 64 張 P1 並處理已無剩餘工作的票，並明確確認本次 30 張封存、2 張刪除。本次只結案，不重做已合併實作。
原持有者：codex-batch031-content-draft；原分支：codex/batch031-content-draft。

- PR #879 merged 2026-09-28; main three packs have five locales; scoped evidence docs/article-localization/batch031-content-draft-evidence.md exists.
- Task explicitly covers 12 reviewed target documents +36 assets in draft PR; deployment/import/publication are excluded.

上述後續證據補足舊清單仍未勾選的項目，已同步勾選。歷史限制保留供追溯；這是既有完成紀錄的核對，不宣稱本日重新部署、重新發布或重新跑過歷史測試。

Do not call these live based on this closure; later release remains separate.

`--force` 僅用於本次授權的任務結案記帳，未修改或接管原分支實作；已核對 main 與開啟 PR，完成判定依上列證據。Windows 的 tasks done 搬移曾留下 open 副本，本次用 Git 原子搬移保留完整任務紀錄。
