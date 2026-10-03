---
id: 2026-09-22-publish-reviewed-five-language-sapporo-itinerary
title: Prepare reviewed five-language Sapporo itinerary PR
status: done
priority: P1
area: docs
owner: codex-p1-audit
claimed_at: 2026-09-29T02:10:53Z
created_at: 2026-09-22T01:55:46Z
completed_at: 2026-09-29T02:11:03Z
branch: codex/p1-task-audit
depends_on: []
scope:
  - apps/api/app/guides/content/sapporo-3-day-itinerary.json
  - apps/web/public/guides/sapporo-3-day-itinerary
---

# Prepare reviewed five-language Sapporo itinerary PR

## Why

The public Sapporo three-day guide only has a zh-TW document. The reviewed candidate adds full en, ja, ko, and zh-CN documents plus text-bearing route diagrams, and corrects the zh-TW source's premature promise of specific 2027 Tsudome attractions. The existing article slug, photos, credits, source URLs, and visibility remain unchanged. This task prepares a reviewable PR only; production source revision and locale publication require later approval and live version checks.

## Definition of done

- [x] Narrow draft PR #645 contains only this guide pack, four localized SVGs, and this task record; the reviewed Windows source bytes match the independent full editorial receipt.
- [x] An independent exact committed-LF byte/render review and all required CI pass before marking PR ready. The PR description distinguishes repository content from live publication.

## Steps

- [x] Start from freshly fetched main `d52af4d95a40f5e353c567d366ee1b2b69dc5696` and claim the two-path scope.
- [x] Verify the independent receipt and copy only the reviewed Sapporo pack and four SVGs byte for byte.
- [x] Run scoped lint/tests, task check, and review diff.
- [x] Open draft PR #645 and mark task `review`.
- [x] Verify final-head CI and independent LF artifact review before marking PR ready.

## How to verify

Run `python -m app.guides.pack_cli lint --slug sapporo-3-day-itinerary` from `apps/api`, the focused guide content/link tests, `npm run check:tasks`, `git diff --check`, and GitHub CI. Compare pack and all four SVG file SHA-256 values to `<home>\.codex\article-localization-release\batch012-selection\sapporo-final-full-review\receipt.json`. Verify the only normalized zh-TW source delta from the published v4 snapshot is `/blocks/22/text` and the new four locales have 30 blocks and 13 sources each.

## Notes

- Independent full review receipt SHA-256 `58de5ef025f5696d28bfd4bfe3f529e78f79221ecb9046f84d563b74d47de5d1` has disposition PASS for exact pack SHA-256 `050d862073cf13a3c8b3523bdd759a5da24e975136bd0e0c549e99b07d3491e1`. The four reviewed SVG hashes are recorded in the receipt.
- Independent source-only approval receipt SHA-256 `dbfc14b23d5d0768ada22757cc6663a66472d11b902eda28a84889515c6c665e` approves the one-pointer Tsudome correction. The previously published zh-TW normalized document is `9e332a1838281c3c50bc32fdf5d6ad81674ae163b47764355bdfc9843168b2a3` at article v2, locale/published v4. The reviewed local zh-TW candidate is `2777a791e06871e0fe191c46fe7ceb5620c223c4e31ef4dbf96ed491c34c5806`; a production write must recheck version/hash and create a guarded revision.
- The Sapporo-only clean worktree was created from current main after PR #635 merged. Otaru is excluded because its separate candidate still has review blockers.
- Verified the final full-review receipt file hash and exact candidate pack, all five normalized GuideDocument hashes, and four SVG hashes. The only normalized zh-TW delta from main/published v4 is `/blocks/22/text`.
- Scoped pack lint exited 0. It reports inherited `no_summary` warnings and the full English body over the howto length guideline, with no errors. Focused guide content/link tests: 12 passed, 5 skipped. `npm run check:tasks` passed (668 files).
- Draft PR: https://github.com/x812033727/travel_scanner/pull/645. Git's LF normalization changed file-byte hashes but not text: each committed pack/SVG blob equals the independently reviewed Windows file after CRLF-to-LF conversion only. `git diff HEAD^ --check` warns about trailing spaces on blank lines in the four exact reviewed SVGs. Do not alter their bytes solely to silence that warning until an independent committed-blob review decides the disposition.


## 2026-09-29 標記完成（由站主授權，非原持有者）

站主要求逐張核對原 64 張 P1 並處理已無剩餘工作的票，並明確確認本次 30 張封存、2 張刪除。本次只結案，不重做已合併實作。
原持有者：codex-batch012-draft；原分支：codex/article-localization-batch012-sapporo-pr。

- PR #645 merged 2026-09-22.
- External sapporo-whitespace-committed-review/receipt.json PASS_exact_whitespace_only_PR_patch_and_identical_visuals binds final commit 1954d1bb2708b0c2ef5bc27aa19be83c01eb0c0c.
- sapporo-release-fixed/journal-production.json sha256 e5c352e7da839531bbf7771a4e5a472df109898d8f77467c78ddf7e4f0553865: five draft/five publish done, pending=null; public QA results also retained.

上述後續證據補足舊清單仍未勾選的項目，已同步勾選。歷史限制保留供追溯；這是既有完成紀錄的核對，不宣稱本日重新部署、重新發布或重新跑過歷史測試。



`--force` 僅用於本次授權的任務結案記帳，未修改或接管原分支實作；已核對 main 與開啟 PR，完成判定依上列證據。Windows 的 tasks done 搬移曾留下 open 副本，本次用 Git 原子搬移保留完整任務紀錄。
