---
id: 2026-09-23-correct-five-unrelated-ai-glossary-links-before
title: Correct five unrelated AI glossary links before localization
status: done
priority: P2
area: api
owner: claude-opus-5-5
claimed_at: 2026-09-30T15:54:46Z
created_at: 2026-09-23T17:44:28Z
completed_at: 2026-09-30T15:56:50Z
branch: claude/glossary-links
depends_on: []
scope:
  - apps/api/app/guides/content/website-www-subdomains.json
  - apps/api/app/guides/content/website-404-recovery.json
---

# Correct five unrelated AI glossary links before localization

## Why

A read-only Batch026 candidate review found five structured article inlines in four existing Traditional Chinese articles. Two WordPress migration inlines are now split to `2026-09-27-correct-wordpress-migration-tag-links-batch030`, leaving the three website inlines in this task. They link ordinary website/search tags or URL parameters to AI token/model-parameter articles. The surrounding source sentences are correct; the linked glossary destinations change their meaning.

This task is separate from the existing cable-label correction and the three URL-parameter corrections for `https-certificate-setup`, `dns-records-troubleshooting` and `cloudways-ssl-setup`. No source correction, translation, import or publication has been performed for these five findings.

## Exact proposed changes

| Article | JSON pointer | Visible label | Current wrong destination | Replacement |
|---|---|---|---|---|
| website-www-subdomains | `/blocks/7/inlines/1` | 標記 | `ai-term-token` | `{"type":"text","text":"標記"}` |
| website-www-subdomains | `/blocks/21/inlines/1` | 參數 | `ai-term-model-parameters` | `{"type":"text","text":"參數"}` |
| website-404-recovery | `/blocks/12/inlines/1` | 參數 | `ai-term-model-parameters` | `{"type":"text","text":"參數"}` |

Each of the three remaining listed `ArticleInline` objects becomes a `TextInline` containing the identical visible word. Preserve every other field in the full source document, parent metadata, source URL/title/date, assets, credits, visibility and sorting. Do not rebuild links automatically in a way that recreates the wrong destinations.

## Definition of done

- [x] Claim the two-pack website scope after checking current tasks, worktrees and open PRs.
- [ ] Capture fresh read-only full production draft, published and latest revision rows; confirm current metadata, versions and exact repository source models. The cached evidence below is not permission to overwrite newer edits.
- [x] Change only the three remaining listed inline objects; require full normalized before/after equality after reversing those three changes.
- [x] Independently review the semantic correction and run scoped pack lint, task validation and diff checks.
- [x] Land a separate scoped PR with required CI.
- [ ] Complete separately authorized guarded source publication with fresh source/version comparison, verified backup and concurrency/state protection. Preserve any hidden, withdrawn or edited article state.
- [ ] Verify the public text is unchanged and the three remaining incorrect links are absent; record the resulting source versions before localization.

## Read-only source pins

Source cached `origin/main`: `85b76908543e1fb59256a2c8ec30e9c3e8196275`. These are actual Git bytes inspected offline; no fresh host reads or primary-source requests were made.

| Article | Original pack SHA256 | Git blob SHA1 |
|---|---|---|
| website-www-subdomains | `833cfb0a6f8ef604e2815a721cfb6cce8c2507192448cdc1a548ef35d9c95c87` | `d92f82a01d400d5b81a9e970e07b498039f61a19` |
| website-404-recovery | `7226237ab4f5a10b867c9fdc4a5fac99d09514714076577a9e4e4ade09c4beb5` | `63b3d13bff9a28fa74b1f37c3c7bf94577df20f6` |

Evidence: `C:/Users/x8120/.codex/article-localization-release/batch026-candidate-inventory-v1/deferred-source-link-findings.json`
SHA256: `2ba5d9c8f3f3eb6ae6a98e12b1bab9f3eb5604c276536944f17b941e4a1782b0`. It includes complete surrounding paragraphs, exact old/new inline objects and pointers.

The saved after-Batch023 metadata is historical evidence only. A fresh full live source comparison and primary-source review remain pending. Merge is not source publication; Batch026 does not fix or publish these articles.

On 2026-09-27, the two WordPress migration links were split into the narrow Batch030 task named above. This task retains the other three link corrections and no WordPress migration pack scope. The original five-finding evidence remains a historical record.

## Notes (2026-09-30, claude-opus-5-5)

- The three `ArticleInline` objects were exactly as listed (label, `kind: life`, slug) on
  current `origin/main`; each is now `{"type":"text","text":<same word>}`. A script put
  the three originals back into the edited pack and asserted equality with the original,
  and asserted the original file re-serialises byte-for-byte, so nothing else moved.
  Both packs are zh-TW only. `pack_cli lint`: 0 errors (the `no_summary` warning on
  website-www-subdomains was already there).
- Visible text is unchanged: "標記" and "參數" read the same, they just no longer link to
  the AI token / model-parameter glossary.
- Publication was not done here. It goes with the next `guides-import` batch, which the
  owner approves (dry run first; a newer live edit wins over this change).
