# Japan entry source correction before four-language authoring

The published `japan-entry-2026-visit-japan-web` source had independently verified
customs wording and an unrelated Machine Learning link inside the unit `760 ml`.
The final v4 correction covers ten exact document pointers, two visible SVG text
slots and the paired SVG/image description. It preserves the existing repository
answer-first description, original root metadata, photographs, credits and other
locale documents.

The distinct source reviewer is `localization_task_inventory`. Its genuine
schema-v1 source-correction review SHA-256 is
`9ec315b0adeb31ea3d2f9ecd1ae236960cdfe54d4144b2f18d011421faa6f4e4`;
the independently read source/artwork evidence SHA-256 is
`b440a4f3f33dee75641354f8ea2918f90c97aa4f3b57e64b1dac2a131012b906`.
The source admission executor did not issue a new editorial approval.

The unchanged official `source_correction.verify_review` accepted the exact v4
source against the post-publication baseline captured on 2026-10-07. The baseline
SHA-256 is
`19c0ff10e958055d59d71ac4fb2b8ef9291d77dbbc2d3917bb491661829b3eae`.
Its original article/locale identity and version guards, published/draft source
hashes and four missing target languages remain unchanged. No target database row
or pending source edit was present in that captured baseline.

| Hash domain | SHA-256 |
| --- | --- |
| Original published source, normalized GuideDocument | `b61bf8edee8f8ab40529399de2f6ef2c3f2419eeb69fb6958955c6c07793743e` |
| Original repository source, normalized GuideDocument | `ad50c99886ca30c358ae664509a9efc41c798540ba1c0b4e9e3334b55051927e` |
| Reviewed corrected source, normalized GuideDocument | `4709f8e36b080bc76a1703704db2744b28409fcc31289eebf5c3105c7ca3f3c5` |
| Original raw repository pack | `ff77ccb926b9a218d2587ade952840e31e96bb439cc1d67a1ddfc0d135a75ab9` |
| Exact reviewed raw v4 pack admitted locally | `9d3010d037bc477408bb738133c52a440c5011129cca9c64474c6b6d5d9c4679` |
| Original source diagram SVG | `5fa315f00462003a37a8ac093e6c2c5954ec91ac860f88fe86c182446be2a065` |
| Exact reviewed v4 source diagram SVG | `104a70f6b7dc06e41f6717c134f0d5d885c8c0e02119a7fa06b0bc76b9cb5afc` |

Both the candidate document and the source inside its pack normalize to the same
reviewed GuideDocument hash. A raw null description field and an omitted field
are treated according to the existing schema; raw file hashes are recorded
separately. The original source cutoff remains 2026-09-13. Only the independently
reviewed replacement official citation at source index 8 has the new actual
`checked_on` date 2026-10-07; other citation dates remain unchanged.

Original pack and all three source assets were backed up before the exact local
copy. The two photographs retain SHA-256
`395176a8c5fc850176787d296467442ee717ab6fccd723369876ed40ccbc56d0`
and `79636ac2970e2a7aa86b189e3f7fdd8c1e10b70bc7344c3e916e222cdb74ea48`.

The explicit derived admission baseline changes only this article's desired
source document/hash, locale document, pack hash and source diagram asset hash.
All unselected baseline rows and original database guards are preserved. Its
SHA-256 is
`b743c32e7ef650f43b3688f53bb1ac8d07bea7e005470131a6985307b1477d03`.
The actual admission/four-job preparation receipt SHA-256 is
`63914054fb223a6c889e2fdc0002ba42926cedef2f948b38e15f956585408839`.

At source admission, official `pipeline.py prepare` exited 0 and produced four fresh `prepared` jobs
for en, ja, ko and zh-CN, with no previous attempts, copied reviews or provider
requests. Target translation, independent full-language/image review, bundle
installation, merge, deployment and publication remain later stages. This local
source admission does not change the production source or the completed first32
release evidence.

## Actual four-language review and local installation

All four CLI translations now have distinct full-document, native-diagram,
glyph, caption, photograph and link reviews. The original single attempts and
their translator identities remain preserved; no provider retry was made.
Root applied only proposed protected-token, description and compact diagram-label
repairs, then materialized and rendered the affected jobs again. Final reviewers
were independent of the corresponding translator and proposed wording. Earlier
render and review failures remain retained as evidence.

The final reviewers read the seventeen paired body blocks, fourteen citations,
six-row table, callout, offer, fifty visible diagram labels plus title/description,
and both original photographs. The native diagrams retain at least 15px text and
their original geometry. Native visual review caught English card/arrow padding
collisions that the automatic layout check missed; the final artifact was separately
reviewed after compact labels were applied. A narrow tools follow-up records that
limitation. No clipping, missing glyph or unresolved finding remained in these final
reviews. Cached source HTTP limitations and checked locale/related routes are retained
in the external evidence; they do not establish global related-language coverage.

| Locale | Normalized document SHA-256 | Final artifact-manifest SHA-256 | Authentic final review SHA-256 |
| --- | --- | --- | --- |
| en | `7f9a33164fb1604389cbbc22f58367ae7f1516a73625594a880d719925646296` | `aa03a56d54e390ae4bece33c0ff92fe8c024597b86a3faa8d52ccccb078ea5f7` | `b4ad149021ae1b0d07b86cf19e7e472fe598afe4dd1f14b1712029c170535b03` |
| ja | `08bd4a72e8863f09f4a94121ea2469578a48639122bfe56ee845eca3bb4e7481` | `036240d15ac03ec9c2b024dca1cce1486001b6546d9080fb3fc009ca12a2e3f9` | `d21a2ee9970bf3633d4cfe25256c9c9f4597e98d6201c1addba3c1d11873c2f1` |
| ko | `50450eef58a25a0854b7f87e52650118305e914c26402ac8ec0a0923e2a3bece` | `94d3d62c22698aeded55ee0cedb798eab0672285fa5d3db0609180506d66c1c6` | `28f5783962bda3a4607cfe9fa6cc6e2e4255572ae7f9bcac5e796b699e703e9b` |
| zh-CN | `a520083b89694a276f3399958c5de3ae77ca354965c56565076ebc8c58bfcd41` | `01ecf33bb86eb554a4c41a2ad116504a35090aa28b33612e3d4889464afb174e` | `42b4188975eccb36d73a446275b7c5d73cdadf8c5d3d8114f0fe7f8ba0209f59` |

English final review was performed by `japan_en_release_final_review`, Japanese
by `news_gate_review`, and Korean/Simplified Chinese by `localization_existing_work`.
The unchanged official `reviewed_document` accepted each actual admitted job.

Unchanged official assembly completed with one article, seven assets and the
approved source-correction review. Manifest SHA-256:
`fc048145476869d1e7ec5fffba794908d0b58065fcb84b04477a3ea046791a3c`.
The installed raw pack SHA-256 is
`bbfc97ceb2747ae3ab8a96ee280b413cf3f3dc70d2c9b5831b87079b907ced02`.
The original photographs are shared by all languages; each new diagram is an SVG.
PNG previews are review artifacts and no raster diagram replacements were added.

Official local installation and the identical replay both exited 0. All eight
journal operations and every captured pack/asset/journal/receipt byte agree before
and after replay. Original photograph bytes, metadata and external job/review/attempt
bytes remain preserved. Installation completion receipt SHA-256:
`c83c899a2606f17aed486197dd7bc77d5a6d0d1b6d8001ce0bd6eeafcd97ca2a`;
journal SHA-256:
`cfaebf083f42d057abd94300ead001c43d94362fe9ec77be7025d213cdf1bd9b`.

Scoped pack lint passed for this single intel entry and translation checks reported
zero hits. The English body retains its existing text-length warning; no reviewed
text was truncated. Actual checks receipt SHA-256:
`94c2da0c0d4cd6de97cec4fc32e08725b856bfc35a783c806d25598d1d567756`.
The unchanged content-pack and localization-tool suites were already run for the
same content-only worktree: 9 passed / 5 skipped and 68 passed respectively.
Integration skips do not establish production release safety; the exact content
PR still requires CI, including the release-safety job, before merge.

The separate open release task selects four new locales and the approved zh-TW
source correction. Its future acceptance cohort is five public pages and ten
desktop/mobile views. This local authoring result establishes no merge, deployment,
database publication or public acceptance and does not expand the earlier 32-article
owner approval.

An additional independent technical peer audit completed 144 checks with zero
technical findings. It verified the one installed pack, seven assets, eight journal
operations, fourteen captured replay files, all four current review/evidence bindings,
the exact approved source and both photographs. Evidence SHA-256:
`8cb14d413c38f24751fcfc2fc0b2d641ab0d43916ad3505e60ca6f6fe7112945`.
The peer compared normalized schema values and explicitly bounded default-field
materialization; it issued no replacement editorial review. Its replay conclusion
is limited to matching journal identity, outputs and files; the individual operation
receipts do not independently record process argv. Root's executed wrapper supplied
the same command object to both official invocations.
