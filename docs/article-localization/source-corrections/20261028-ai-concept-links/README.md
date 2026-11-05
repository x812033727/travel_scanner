# Four AI concept source corrections

The Traditional Chinese articles used ordinary words as links to different AI
concepts: sequence/example/provenance labeling linked to Token, and reviewing a
household appliance linked to AI Evals. This patch preserves those words as plain
text. It also expands OCR to 光學字元辨識（OCR） at its first use in the multimodal
article and corrects the zero-shot hero description to match the existing drawing.

| Article | Exact document change | Observed source / published version |
| --- | --- | --- |
| `ai-term-fine-tuning` | `/blocks/5/inlines/1`: 標記 becomes plain text | 8 / 8 |
| `ai-term-few-shot-prompting` | `/blocks/10/inlines/1`: 標記 becomes plain text | 10 / 10 |
| `ai-term-multimodal-ai` | `/blocks/19/inlines/1`: 標記 becomes plain text; `/blocks/0/items/2`: first OCR expansion | 10 / 10 |
| `ai-term-zero-shot-prompting` | `/blocks/10/inlines/1`: 評測 becomes plain text; `/hero/alt`: describe the open manual, three gray lines, orange circle and blue right-pointing arrow | 10 / 10 |

Zero-shot's `hero.svg` receives the same description in its `desc` element. All
visible SVG geometry, the original JPEG, the other eleven source assets, source
citations and their `checked_on: 2026-09-14` values remain unchanged. There are no
target-language documents or assets in this change.

## Evidence and review boundary

[evidence.json](evidence.json) records complete old/new canonical document hashes,
candidate file hashes, native review hashes, exact pointer changes and all twelve
before/after asset hashes. The four candidate authors and their independent
reviewers are identified separately. Raw snapshots and native receipts contain
database bindings and remain in the retained external evidence collection; the
JSON here is a public summary, not a publication receipt.
Candidate file hashes bind the retained original bytes; `repository_pack_sha256`
binds the staged Git blob after the repository's LF normalization. Both forms
produce the same approved canonical document hashes.

A new read-only production snapshot at `2026-10-29T00:56:21.795830+00:00` confirmed
the four published `zh-TW` rows, matching draft and published versions/hashes, no
dirty source row and no other locale rows. All four original source documents and
the twelve deployed checkout assets matched the retained review bindings. Native
`source_correction.verify_review` passed for each complete final candidate using
these freshly revalidated bindings. Historical incomplete reviews and original
translation attempts remain preserved; their earlier results are not relabeled
as current approval.

The eight declared primary URLs and six supplemental URLs were reopened on
2026-10-29 and the passages relevant to the unchanged claims were checked. No new
blocking finding was found. This was a targeted refresh, not a new exhaustive
review of every reference cited by those sources. The original source dates were
not advanced. Zero-shot's original JPEG and retained candidate render were also
viewed again during installation; the description matches both. Its SVG change
is exactly the old description replaced by the new description, with all other
bytes preserved.

Validation passed for the four selected packs with `pack_cli lint`, all four
native reviews against the final staged blobs and all twelve source assets. The
existing `test_the_packaged_content_validates_and_its_images_exist` and
`test_the_packaged_life_content_passes_lint` checks passed (2 tests). Task validation
passed; unrelated existing stale-claim/scope-overlap warnings remain. No production
request was made by the installation or validation scripts.

## Publication remains a separate operation

This source-only draft does not authorize merging, deployment, source publication
or translation. Before a later source correction release, obtain the scoped
authorization and a fresh snapshot, verify the deployed content and all source
version/hash bindings again, then use the guarded publication workflow with its
native receipts. Publish and verify these source corrections before building a
new localization baseline or authoring translations. A changed source, asset,
visibility or locale state requires revalidation rather than reuse of this
snapshot as action-time evidence.

The shared task remains open for that separate release and fresh-baseline work:
`2026-10-28-correct-misleading-ai-concept-source-links`.
