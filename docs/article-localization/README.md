# Article localization bundle tools

`assemble_bundle.py` combines independently reviewed jobs with a pinned production
baseline. `install_bundle.py` installs the exact manifest into repository content
and image paths with a resumable journal. Neither tool publishes production data.
Use the [shared localization skill](../../.agents/skills/article-localization/SKILL.md)
for source audits, independent text/image review and the guarded release workflow.

The assembler preserves root metadata from the hash-verified source pack,
including article aliases, ordered related-article picks and `news_date`, when
an older baseline omits those fields. Values explicitly pinned in baseline
metadata retain precedence. Locale documents still come only from the baseline
and the exact independently reviewed jobs or source-correction receipts.

An installation check must compare all original root fields, source documents,
image bytes and credits with the candidate, as well as verifying new locales.
A successful installer exit or replay alone does not establish preservation.
If a candidate loses data, preserve its manifest/journal and restore the exact
pinned source before compiling a corrected manifest; never edit an installed
pack under an existing reviewed manifest.

Focused validation:

```bash
PYTHONPATH=apps/api python -m pytest docs/article-localization/test_assemble_bundle.py docs/article-localization/test_install_bundle.py
```

Raw database snapshots and job/release state contain private identities and belong
in the persistent private working area. Commit sanitized counts and hashes only.
