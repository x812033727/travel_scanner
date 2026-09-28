# Batch042 Pair A: search intent and content quality

This branch adds 24 localized assets for `seo-search-intent` and `seo-content-quality`: 16 hero/diagram SVGs and eight 1600×900 JPEG covers. Eight complete zh-CN, English, Japanese and Korean documents are independently reviewed outside the repository. Article JSON is unchanged while source correction #942 remains unmerged. Original zh-TW, root metadata and original artwork are preserved.

## Source and candidate versions

The read-only inventory receipt SHA-256 is `167d0a345864d1a3ca2117b585e8aaee91e5ef7dcd099954efd65f28e783f29f`; repository inventory SHA-256 is `2df6cd72344c96025188ab1407459a669d37d1c20d300a77897c4ec288fadfd5`. These historical records are not a current release preflight. #942 removes two false AI-glossary links from these source documents without changing visible wording. Translation follows that corrected repository version; live reconciliation remains a separate release requirement.

| Article | Corrected source pack SHA-256 | Reviewed final LF candidate pack SHA-256 |
| --- | --- | --- |
| `seo-search-intent` | `420e80f7c483ac21c1d3a5c9803e8daee846dd5e60c687e48354bb23d695f0ab` | `daba67de0fa4e32348e7d38c179b289218bcec2cc27ac23be29636de6a02fa78` |
| `seo-content-quality` | `aa8e6b95b373ec4f2fab13e9a99798173532541c760407cf07daf259b229880f` | `6f0e03a0d56bac60dc68929ffc00d5f63237c80c84b439e7f3e912fe67a845cc` |

Original candidate bytes are pinned as `3d6434666aacc17ab268834c6ef0857136e76e3061844d4e0b430ab45cc71389` and `dc142ce9a935638e1c3e2480c72bedd8cba477f8bcaae1aeb42242649379573e`. Final LF candidates preserve the exact JSON values. Installation refuses a different main source or intervening working-copy edits. The current dry run refuses main because the source correction has not merged; it wrote nothing.

## Independent content and artwork review

Independent peer QA compared all eight full target documents with the corrected source, including title, description, all 32 blocks, tables, lists, callouts, image descriptions and source titles. Exact original source URLs, checked dates, root metadata, image credits and shapes were preserved. The final report records corrections to zh-CN table wording, the Korean Taipei Main Station name, Japanese/Korean query-to-page diagram labels and the English description length without loss of meaning. Those corrected frozen candidates are unchanged.

New-locale related-reading and glossary labels remain plain translated text until their corresponding language routes are verified public. This repository guard does not assert the live publication status. Search intent remains a hypothesis to validate against reader tasks and query data; content-quality examples do not claim firsthand product testing or ranking guarantees.

The peer reviewer inspected all 16 localized SVGs and eight covers, including complete diagrams, mobile tables and endings. Browser text bounds found no canvas/card overflow. The coordinator additionally inspected the final four five-language desktop/mobile heading/cover sheets and rechecked all 24 assets against the frozen historical hashes. Only proven CRLF/LF equivalence is accepted for SVGs.

The final standalone local previews cover both articles in all five languages at 1365×900 and 375×812: **20/20 passed**, with 32 blocks, expected source counts, both 1600×900 images loaded, no browser errors and no page-level horizontal overflow. The first concurrent screenshot attempt failed inside browser capture; sequential recapture completed all cases. This is local HTML layout evidence, not the Next.js renderer or production acceptance.

## Evidence and checks

Raw candidate files, receipts and screenshots remain outside the repository.

| Evidence | SHA-256 |
| --- | --- |
| Structural/asset audit | `fdd1b1691c52cb4e3d485c61a43b18ab7b4c7c96e8cd955af77784ca9eac4931` |
| SVG browser text bounds | `46e246f1f069201f9c4e53d2893204aac1818680fe53daa0febd57ee81289004` |
| Independent full-text/image peer review | `2a859bac89181a8b2aa0fe60d923a30f8f07d689f952ab16d8224e99aad3f12d` |
| Final candidate/asset bindings | `4e995615ee2b13d7ef2fb0ce80e16b60f651e12d264eef3836641871177677de` |
| Final review and visual checks | `b765132a7188557a2466df9e39e6facc3aebe61cd167ffd3b66631c8192c106f` |
| Final 20-case article preview | `c4b61591023ebaa43394a029666e9746cea467617288f5d34b32b30181e268ca` |

Candidate pack lint has zero errors; English lengths of 7,134/6,972 characters are advisory, and complete paragraphs were retained. Strict source intake is **not fully passed**: both originals start with a paragraph rather than summary, and content quality has two source self-references (limit one). Internal article targets and SVG numeric checks pass. Installation must rerun scoped lint, focused API tests, task checks and current-head CI.

## Remaining stages

`2026-09-28-batch042-pair-a-install-reviewed-locales` tracks safe installation after #942 merges, source task scopes release and main source hashes match. PR #946 currently reviews art/evidence only. No database draft import, deployment, publication or live browser acceptance occurred. Same-image nonproduction rehearsal remains unavailable; later release requires that rehearsal, live-source reconciliation, backup/write-control checks, explicit slug/locale dry run and real-route verification.
