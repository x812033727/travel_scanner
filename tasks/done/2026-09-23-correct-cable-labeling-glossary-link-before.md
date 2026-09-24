---
id: 2026-09-23-correct-cable-labeling-glossary-link-before
title: Correct cable labeling glossary link before localization
status: done
priority: P1
area: api
owner: codex-cable-source-correction
claimed_at: 2026-09-23T11:02:46Z
created_at: 2026-09-23T10:40:33Z
completed_at: 2026-09-24T05:23:52Z
branch: codex/fix-cable-label-glossary-link
depends_on: []
scope:
  - apps/api/app/guides/content/desk-cable-charging-organization.json
---

# Correct the unrelated Token link in the desk-cable source before batch021 translation

This open follow-up records a source-link defect discovered during batch021 inventory. The other two inventory candidates can proceed independently; this article needs a corrected, rechecked source baseline.

## Problem

The currently published zh-TW source has `/blocks/2/inlines/1` equal to `{"type":"article","text":"標記","kind":"life","slug":"ai-term-token"}`. Here「標記」means labeling a physical cable after tracing its endpoints. Linking that word to an AI Token article changes the intended meaning and should not be copied into four translations.

## Definition of done

- [x] Re-export the exact published article and all its locale rows before correction; compare the full current draft, published and latest models against the pinned source. Stop on a concurrent edit, visibility change or unexpected locale row.
- [x] Prefer the smallest correction: replace this one ArticleInline with the TextInline `{"type":"text","text":"標記"}`. Use another article target only if its relevance and actual publication are independently verified. Keep the visible word unchanged.
- [x] Preserve every other body field, title, image, credit, source URL, original `checked_on`, pack metadata and article state. Preserve the original snapshot/version evidence; never manually rewrite revision history or counters.
- [x] Independently compare the corrected normalized source with the original, allowing only the one inline type/target change. Validate the pack and confirm the import/link processing will not recreate the unrelated link.
- [ ] Complete the source-correction PR/publication sequence using the existing revision services and fresh concurrency checks; preserve every historical revision.
- [ ] Re-export after the corrected source is actually published, verify draft/published/latest equality and new real versions, and pin that full source as the baseline before translating this article. Keep the old v1/v6 evidence as history.

## Evidence and verification

Exact repository baseline: `ea893f4c9bdb0f17c153ae2ade526a3ce2a2f164`.

Read-only three-article snapshot: `batch021-candidate-inventory/live-source-full-20260923T103546Z.json`, SHA-256 `9794e7d03a9ba11ced25f245d54f1be0f4c5d43b5304f02cea976831303ac590`. At capture, the cable article was active and published, article v1, zh-TW draft/published/latest v6, and the full normalized model equaled the repository source. No other locale rows existed.

Source/conflict receipt: `batch021-candidate-inventory/live-approval-20260923T103546Z.json`, SHA-256 `997f0a925c39dde398504aff705c51f74be30e976332aa272d2d83e9279ad391`.

The separate household-inventory candidate is article v2 / zh-TW v6; do not generalize the cable article's v1 to the whole batch. No article source, host file or database row was changed during inventory. The follow-up was initially recorded as open and unclaimed; the execution notes below supersede that initial state.

## Execution notes — 2026-09-23

- Claimed in an isolated worktree as `codex-cable-source-correction`. This correction remains separate from batch020 publication and batch021's two other articles.
- Fresh read-only source at 11:03 UTC exactly matches the complete earlier row: article v1, zh-TW v6, no concurrent draft or other locales. Archive `cable-source-correction/live-source-before-20260923T110331Z.json`, SHA256 `a4d7fee8c422ed5a982dee66807acd218a6021a9db7122bdcfe9a0230ff65842`.
- The pack changes only `/blocks/2/inlines/1`; every other normalized pack field and both original image files are unchanged. Source model `37de00d77292389366109f1e076867964e38e588eb1a0eb4d493c3cc341a1297` becomes `b67d107a9413dbf52e5729d0c543cbb9698524feeb332f67c6df8b0de8e3619c`.
- Scoped pack lint passed with the existing `no_summary` and `text_length` advisories. Actual `ArticlePack`/`GuideDocument` validation and explicit inline-target extraction passed.
- Independent review: `cable-source-correction/independent-review-v1/receipt-pass.json`, SHA256 `1de9a3d614cc2621d4edf702c51bc6126d6f6511344a2fe5c8e25fafe89e466c`. The existing source-correction validator accepted the bound approval and rejected ten stale, extra-change or unpublished-edit variants. Actual inline materialization was checked with mocked database boundaries; it retains the relevant gadget article link and drops the removed Token relation.
- Compatible correction approval: `source-correction-approval.json`, SHA256 `599af8ad587bd6ca8dbc0f2529e9fe225eea2170443b992db51250bf8100e479`. The optional standalone `pack_cli autolink` command is not part of import/publication and must not be applied to this corrected pack.
- Pending: PR/CI, actual guarded publication through existing revision services, and fresh public source verification. Recheck the full live row immediately before any source write. Do not translate this article from the old baseline.

### 2026-09-24 標記完成（由站主授權，非原持有者）

站主在對話中指示由 Claude 結案這張票（原持有者 `codex-cable-source-correction`），並選擇「結案＋另開發布票」。

- repo 端已完成：PR #690 合併為 `b626f310`（2026-09-23 14:11 UTC）。它就是上面四個已勾項目的成果，只改了 `/blocks/2/inlines/1`。
- 正式站**尚未**修正：2026-09-24 05:00 UTC 查 `GET https://mokaair.com/api/travel/guides/life/desk-cable-charging-organization?locale=zh-TW`，`document.blocks[2].inlines[1]` 仍是 `{"type":"article","text":"標記","kind":"life","slug":"ai-term-token"}`，`article_links` 仍含 `ai-term-token`。
- 兩個沒勾的項目（透過既有 revision 服務發布、發布後重新匯出並釘成翻譯基準）原封不動移到 `2026-09-24-publish-cable-labeling-source-correction`。上面的證據、雜湊與「不要跑 `pack_cli autolink`」的警告，那張票都指回這裡。
- 結案的目的是解除這張票對 `apps/api/app/guides/content/desk-cable-charging-organization.json` 的 scope 鎖；新票沿用同一條 scope，所以同一時間仍只有一張票能改這個檔。
