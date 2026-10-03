---
id: 2026-09-22-publish-reviewed-five-language-otaru-day
title: Publish reviewed five-language Otaru day trip
status: done
priority: P1
area: docs
owner: codex-p1-audit
claimed_at: 2026-09-29T02:10:50Z
created_at: 2026-09-22T02:13:11Z
completed_at: 2026-09-29T02:10:53Z
branch: codex/p1-task-audit
depends_on: []
scope:
  - apps/api/app/guides/content/otaru-day-trip-from-sapporo.json
  - apps/web/public/guides/otaru-day-trip-from-sapporo
---

# Publish reviewed five-language Otaru day trip

## Why

The published Otaru day-trip guide has only zh-TW. Add complete en, ja, ko and zh-CN
GuideDocuments and language-specific route diagrams. The reviewed candidate also
corrects the zh-TW Nikka Yoichi eligibility paragraph and Tenguyama New Year
ropeway last-car times; those source revisions must be guarded against the live v6.

## Definition of done

- [x] A narrow, independently reviewed five-language candidate and five SVG route
  diagrams are committed in a draft PR without changing publication state.
- [x] Independent exact committed LF blob and render review approves the PR bytes.
- [x] Release owner separately verifies current live version/hash, CI, import dry run,
  guarded source revision, publication, and browser/device checks.

## Steps

- [x] Verify current main zh-TW GuideDocument against pinned live v6 SHA-256.
- [x] Copy only the receipt-bound Otaru pack and five SVGs from the isolated draft.
- [x] Verify the zh-TW delta is limited to three reviewed content pointers.
- [x] Run scoped lint, guide content/link tests, and task check.
- [x] Open draft PR; independent committed LF blob/render review remains pending.

## How to verify

From `apps/api`, run `python -m app.guides.pack_cli lint --slug
otaru-day-trip-from-sapporo` and `pytest tests/test_guides_content_pack.py
tests/test_guides_content_links.py -q`. At the repository root, run
`npm run check:tasks`. Compare pack and all five SVG SHA-256 values to the
independent re-review receipt before staging, then inspect committed LF blobs
and render them separately.

## Notes

- Independent full PASS receipt:
  `<home>/.codex/article-localization-release/batch012-selection/otaru-revision/independent-review/receipt.json`,
  SHA-256 `3d8b81cbee97d0435a7bb6462524ab2d7fb689b35848629274be928978d4ff98`.
  It binds pack SHA-256 `1901b14cd4453697592ac91348983d941182f81971174185e11c415d3812618e`
  and freeze SHA-256 `00228db75c13873e55a366de796f4d24592a1f970f63700b2be42a1de888b892`.
- Current main `d52af4d95a40f5e353c567d366ee1b2b69dc5696` has only zh-TW,
  normalized SHA-256 `24dd0796020e4621ca14cb4aa766c92786721ed9d89c63bc1dd725c508913f46`,
  matching the previously observed published v6. Comparing normalized source
  documents, this candidate changes only `/blocks/18/text` (Tenguyama winter
  exceptions), `/blocks/21/text` (Nikka age/driving/pregnancy eligibility),
  and `/blocks/25/items/3` (winter checklist). No other source field differs.
- The source SVG changes only its bus-label baseline y=392 to y=410. The four
  language SVGs are new; all five exact working-file hashes match the receipt.
- This draft PR must remain held until an independent review binds and renders
  the exact LF-normalized Git blobs. Editorial approval of the Windows candidate
  does not establish committed-blob identity. No automatic merge, deployment,
  import or publication.
- Draft PR: `https://github.com/x812033727/travel_scanner/pull/646`;
  initial content commit `90ceb6fccf34dce0478e2187cdcb300e6791cae8` from
  main `d52af4d95a40f5e353c567d366ee1b2b69dc5696`. Keep the PR draft and
  do not enable auto-merge pending exact committed LF blob/render review.
- Scoped lint exited 0 (inherited no-summary and English length warnings);
  content/link tests: 12 passed, 5 skipped; `check:tasks` exited 0 with
  unrelated pre-existing stale-claim warnings. Git staging transformed only
  CRLF to LF in the pack and four new SVGs; the source SVG was byte-identical.
  Staged LF SHA-256: pack `e4a1c8888a64cf9a452709117800cede33b502e4f89b23daaa559144f342fe1a`;
  en `593789554ed2ffa0fca4462dd2793bb56bbbd1b856f9ca2f2c72f2fa8eaed290`;
  ja `fad27f78c7041782c017b75bdd9848e8b988af1042245ce8bff636e5d2745f8f`;
  ko `3b21eb0c4af2d77e4a29b11b68db440405ca7e3f4ccda418d3e2cab11405ce7f`;
  zh-CN `c998038e999483f5e28b0f0c885d590c35b1ac4d2d208a2ac27bd3e370d08ac3`.
  `git diff --cached --check` flags two trailing-space blank lines in each
  of the four reviewed localized SVGs; do not rewrite reviewed bytes solely
  to silence this warning before independent committed-blob review.


## 2026-09-29 標記完成（由站主授權，非原持有者）

站主要求逐張核對原 64 張 P1 並處理已無剩餘工作的票，並明確確認本次 30 張封存、2 張刪除。本次只結案，不重做已合併實作。
原持有者：codex-batch012-draft；原分支：codex/article-localization-batch012-otaru-pr。

- PR #646 merged 2026-09-22; exact committed review receipt says PASS_exact_committed_LF_blobs_and_visuals.
- External otaru-release/new-head/journal-production.json sha256 6e954b7f692cd977c48988b7e104d2b9bf41d3d2f71645fdd07d989b8e73def4 has five drafts/five published done and pending=null.
- public-qa-66fb5c57/visual-and-related-links.json status PASS sha256 7808fc9e95db5cc83ffc32f5ab0af6e84d3da48af0b12c27d06e1d617a09e089.

上述後續證據補足舊清單仍未勾選的項目，已同步勾選。歷史限制保留供追溯；這是既有完成紀錄的核對，不宣稱本日重新部署、重新發布或重新跑過歷史測試。



`--force` 僅用於本次授權的任務結案記帳，未修改或接管原分支實作；已核對 main 與開啟 PR，完成判定依上列證據。Windows 的 tasks done 搬移曾留下 open 副本，本次用 Git 原子搬移保留完整任務紀錄。
