---
id: 2026-10-07-enable-verified-hong-kong-localization-routes
title: Enable verified Hong Kong localization routes
status: done
priority: P1
area: tools
owner: codex-article-localization-4e16
claimed_at: 2026-10-07T07:34:34Z
created_at: 2026-10-07T07:34:28Z
completed_at: 2026-10-07T08:40:04Z
branch: codex/article-locales-wave3-20261007
depends_on: []
scope:
  - tools/article-localization/pipeline.py
  - tools/article-localization/test_pipeline.py
  - tools/article-localization/README.md
  - docs/article-localization/route-verification-hong-kong-20261007.json
  - .agents/skills/article-localization/SKILL.md
  - .claude/skills/article-localization/SKILL.md
  - .agents/skills/article-localization/references/pipeline.md
---

# Enable verified Hong Kong localization routes

## Why

The localization pipeline correctly refuses unverified site links, including
Hong Kong's destination and city-filtered food catalogue. Both routes now have
genuine five-language public content proofs. Permit those exact URLs without
allowing arbitrary food filters, aliases, fragments or other query variants.

## Definition of done

- [x] Hong Kong destination and only literal foods?city=hong-kong preserve the
      city selection while switching to each verified target language.
- [x] All other queries/duplicates/fragments/aliases and unverified destinations
      still refuse materialization before writing artifacts.
- [x] Public-safe proof preserves actual HTTP/content/lang/canonical/filter hashes.
- [x] Meaningful pipeline regression tests and applicable tooling checks pass.
- [x] Shared skill descriptions and their byte-identical twin match final behavior.

## Steps

- [x] Verify10 actual public routes, including selected Hong Kong filters and real merchant data.
- [x] Add the narrowly verified destination and exact query allowlist with meaningful refusals.
- [x] Test full materialization, external/source preservation and query/alias edge cases.
- [x] Independently review the change, validate skills/tooling and record precise evidence.

## How to verify

Run tools/article-localization/test_pipeline.py with the real API Python environment,
Ruff and the applicable artifact/skill tests with the bundled Node runtime.
Positive tests cover all five target languages and full materialization; negative
tests prove no output artifacts for rejected query/fragment/path variants.

## Notes

- Original actual route proof SHA:
  `2213722c89e182d41a83f87603b96d184e174e15f67d395c70b7497ee3934c1f`.
- The food catalogue deliberately has a base canonical without the query. Its
  server-rendered selected destination and all20 displayed records prove the
  literal Hong Kong filter; this is not a successful empty/error shell.
- The separate hash-bound Hong Kong source review has now passed; it grants no target, tool, deployment or publication approval.
- No arbitrary query parsing, fallback locale or publication guard is weakened.

Continuation evidence: the current pipeline SHA is
`4e0243362ec79dce4c2ea5dcb8683088992ba8d4764f718ae649568eed4d4ad1`.
All 35 Python pipeline tests and Ruff pass. Seventeen applicable artifact/layout
tests and seven shared-skill tests pass. Empty fragment and bare query markers
are refused along with extra/duplicate/encoded city filters. The independent
code review remains pending, so this task is not done yet. No full Windows tools
suite result is claimed; unrelated known Windows failures have existing tickets.

Final independent code peer review PASS SHA:
`7d0c4b872ae976e241cee48239d6b5178306acf8d71ca9c7286be08de239084f`.
The first4e024... code review found real urlsplit normalization of LF, TAB and
leading space; its failure/probe evidence remains preserved. Root now inspects
the raw same-site string forASCII controls and surrounding whitespace before
route admission. Five full-materialization refusal variants were added. Current
pipeline SHA `4864de9e1e238dc678bcf9fbb2bd6f5b2bf7f8b8b40634c59a2f2aa8d9ab2a91`;
test SHA `0dc961c3a1a4fe74a0a86c974baf0dbbf59124b8ff3692e2ec080028a90de052`.
Root and independent reviewer actually reran all35 pipeline tests successfully;
Ruff and all24 applicable artifact/layout/shared-skill tests pass. The reviewer
also checked both approved routes in all five locales, seven raw-boundary
variants and unchanged external/source URLs. Only code approval is credited.
Taiwan/HK target image reviews remain separate and unfinished.
