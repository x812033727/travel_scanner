---
id: 2026-09-22-localize-llms-txt-evaluation-draft-only
title: Draft llms.txt evaluation localization without publication
status: review
priority: P2
area: docs
owner: codex-batch016-en-zhcn
claimed_at: 2026-09-22T05:35:42Z
created_at: 2026-09-22T05:35:38Z
completed_at:
branch: codex/article-localization-batch016-llms
depends_on: []
scope:
  - apps/api/app/guides/content/llms-txt-evaluation.json
  - apps/web/public/guides/llms-txt-evaluation
  - tasks/open/2026-09-22-localize-llms-txt-evaluation-draft-only.md
  - tasks/open/2026-09-22-correct-llms-txt-evaluation-token-link.md
---

# Draft llms.txt evaluation localization without publication

## Why

The original 626-article localization scope includes `llms-txt-evaluation`, but the
article has no production database row and was deliberately excluded from
publication because it overlaps the published `ai-search-llms-txt` topic. Prepare
complete translation drafts and localized-artwork inputs without weakening that
publication exclusion or treating repository presence as public state.

## Definition of done

- [x] English and zh-CN drafts preserve all 33 blocks, 7 sources, 5
      `ArticleInline` nodes, URLs, checked dates, literal paths and technical terms.
- [x] Japanese and Korean remain owned by the coordinating parent; this task does
      not duplicate those drafts.
- [x] Draft documents validate as `GuideDocument` values and have raw and
      normalized hashes recorded outside the repository for independent review.
- [x] The source pack and three source assets remain byte-for-byte unchanged.
- [x] Four localized hero SVG/JPG pairs and four localized diagram SVGs pass
      independent text, desktop and actual-mobile visual review.
- [x] The repository change remains a draft PR and the canonical wrapper remains
      offline; no database write, import or publication is performed.

## Steps

- [x] Pin the repository source and assets and confirm the production row is absent.
- [x] Claim the exact pack and asset paths before drafting.
- [x] Draft and validate English and zh-CN outside the repository.
- [x] Hand exact hashes and the source-link observation to independent review.
- [x] Bind final localized assets and image-path-only document changes to an
      independent review receipt.
- [x] Integrate all four reviewed drafts and localized assets into the repository
      pack, then pass scoped pack lint and task validation.
- [x] Record the source-link issue as a dependency-gated follow-up without
      changing the frozen zh-TW source.

## How to verify

Use the isolated Python 3.13 API runtime to parse all five documents as an
`ArticlePack`, compare the four target locales with the independently reviewed
documents, and compare zh-TW plus pack metadata with the original repository
pack. Run scoped pack lint, `npm run check:tasks`, and `git diff --check`; inspect
the exact pack, twelve localized assets and two task records before commit.

## Notes

- Candidate receipt:
  `C:/Users/x8120/.codex/article-localization-release/batch016-candidate-readonly.json`
  (SHA-256 `9b4a4665e983b968bc49b05577207f001ccf79602882d5daf6c3546e9fa197f0`).
- Exact source document:
  `C:/Users/x8120/.codex/article-localization-release/batch016-llms/source-document.json`
  (raw SHA-256 `7cec7418109436a1af699a5cae7080a00e12d0c0218863dec71e9f86dc6aaaed`,
  normalized SHA-256 `fbf7c5867be88cd1b7058024b7ec79e807b206d749a1876da4cd543f392391a4`).
- Repository pack Git blob `9f935d820f6e02d08c0272a2fed2ab86e19b8e07`, raw SHA-256
  `35860cdb23f40fefef6825ab68c4a8309da24cc362e395b622cd7b6d417373c6`.
- The candidate receipt was created at `dc6d67229af4c2148fc94023ec6bb61f36f51882`.
  Before this worktree was created, `origin/main` advanced to
  `c47429e98cb6a9b472733502aa0e033889924dde` through unrelated PR #644. The
  source pack, diagram SVG, hero SVG, hero JPG and publication-exclusion task
  blobs were unchanged at that base. Immediately before commit, this branch was
  fast-forwarded to `3ac56b9a1b437a395a2ab8ba9b0c7bf3eb809b16`; that additional main commit
  only added a separate batch010 hold task, and all reviewed batch016 hashes
  remained unchanged.
- `tasks/done/2026-09-15-publish-held-ai-coding-content.md:107` records the
  duplicate-topic exclusion. Preserve it: this article remains draft-only.
- `/blocks/21/inlines/1` links visible text `標記` to `ai-term-token`. Preserve
  the source slug and link identity in translations and record the semantic
  mismatch for later source editorial review rather than silently changing it.
- All four prose drafts passed independent review. EN receipt SHA-256
  `aff60a23262475a9fa49be08436d0521aa16c0f475b517ba2585e15866399995`;
  zh-CN `d751a37f97ce7b5447e2ad0a0f35d6406ad3b9d995e3fe86a16007394580ad3e`;
  JA `f527642ca9f1a1132fde5fff9b49030fa1f17ffd288581a6087c6dabad6ae6eb`;
  KO `ece7a32aeee3555c92bb87e5e2284b7fdf72205da391b0bd1a73b70b1b421a39`.
- Localized asset and image-path author freeze:
  `C:/Users/x8120/.codex/article-localization-release/batch016-llms/asset-freeze-and-image-path-supplement.json`
  (SHA-256 `17b2a26f5493f3ebbb08ff623177a68cb00743ec8a98b2273eec9dcd7de77645`).
  It binds 24 reviewed renders.
- The exact `/hero/src`-only document supplement passed independent review at
  `C:/Users/x8120/.codex/article-localization-release/batch016-llms/independent-review/image-path-supplement-pass.json`
  (SHA-256 `fceb5d3e7394533aed112a5be35816410258f813fc01c37493a15d2bfcd96489`).
  Visible-label and visual review passed independently at
  `C:/Users/x8120/.codex/article-localization-release/batch016-llms/independent-review/asset-visual-receipt-pass.json`
  (SHA-256 `42944726891231cf34fddc8381be67527570ee84860b9e6bffb21775bf4d0488`).
- The integrated five-locale pack has SHA-256
  `c58130d91dad79d1aa8659208d33a12805bb53ece98d5b5d9959010c51fc8ebd`;
  its normalized `ArticlePack` SHA-256 is
  `29ae9d18a0737f24bc4499132bfc22799f116b5fb462ed4ccfb2d65b8c5450a4`.
  Integration audit:
  `C:/Users/x8120/.codex/article-localization-release/batch016-llms/pack-integration-audit.json`
  (SHA-256 `93c9f94bf4fba45725ef734a1557a5b9b701acf5fcdf0b74d019c08b91939892`).
- Scoped `guides-pack lint` passed with no errors and rendered all five diagrams
  plus the source hero. It retained source-shape warnings for missing summary
  blocks in all locales and the full English translation exceeding the preferred
  life-article length; neither warning changes or truncates the reviewed source.
  Receipt:
  `C:/Users/x8120/.codex/article-localization-release/batch016-llms/pack-lint.json`
  (SHA-256 `ea6062c88e03ecf8cec1ed949e13e198f317de76ba12534ecde99fe8b6de8cba`).
- Final pre-commit model and byte verification passed at
  `C:/Users/x8120/.codex/article-localization-release/batch016-llms/precommit-verification.json`
  (SHA-256 `9126b3ead50789a6b5c6cf11080db0dc7d3ade01f62d620191c12153471460c7`).
- The semantic link issue now also has an unclaimed, dependency-gated follow-up:
  `2026-09-22-correct-llms-txt-evaluation-token-link`, whose scope is only its
  own task record until a future editor claims a separate source-correction scope.
