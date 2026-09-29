# Batch042 SEO source-link correction

This change starts from `origin/main` commit `0d30e604c52f5e8abb55c4fc567e8699573010a8`. Five rich-text links in four zh-TW source packs pointed ordinary SEO prose at unrelated AI glossary articles. Each linked inline is now plain text with the same visible wording. No other JSON fields, prose, metadata, sources, or image references changed.

| Source pack | Original SHA-256 | Corrected SHA-256 | Link removed |
| --- | --- | --- | --- |
| `seo-search-intent` | `74c8faac11795fb2929f3f1f5aeb49835a1b3994b4c7601a317829b86c21acca` | `420e80f7c483ac21c1d3a5c9803e8daee846dd5e60c687e48354bb23d695f0ab` | Marking ads separately (`標記`) → AI token |
| `seo-content-quality` | `467e75f4c264884fc294527c885c9f8e814ee9090eb8d29c44d1184c04bc7f51` | `aa8e6b95b373ec4f2fab13e9a99798173532541c760407cf07daf259b229880f` | Using comparison tools (`工具使用`) → AI tool calling |
| `technical-seo-checklist` | `59b68038f68cc40ad8af1ee1738db6861b55c5d3b359fe3de22ee4ad73c5414c` | `a5f692c99703c5b15e683fd4543d7438c6179d46042f8336f8abaee6cdcc5e08` | Robots meta tag (`標記`) → AI token |
| `seo-learning-roadmap` | `38f0e8fc1f8a17d1a2b1783a553f1c71e6d6c94ef3a9cce7173e91979ac602e1` | `5d4d982e675e03e7cf3b9840e5ce26488bf7dbc8f54a40f75c7113fdd7635dd5` | Adjusting a description (`微調`) → AI fine-tuning; international-site markup (`標記`) → AI token |

Checks: a structural comparison against the original commit accepted exactly these five inline conversions and confirmed rendered zh-TW text is unchanged. `pack_cli lint` checked the four packs with no errors; each retains its existing `no_summary` advisory. `tests/test_guides_content_links.py` passed (3 tests), `npm run check:tasks` passed, and `git diff --check` passed.

This repository correction does not change the live article revision. Before importing translated locales, the release operator must read the current production status, revision and content hash for each source article, reconcile any intervening editorial changes, and apply the source correction only through the guarded release procedure. No production write or publication was performed here.
