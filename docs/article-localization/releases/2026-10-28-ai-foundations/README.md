# Twelve AI foundation life articles — 2026-10-28

Status: released and accepted. Forty-eight reviewed English, Japanese, Korean
and Simplified Chinese translations are public. The twelve complete Traditional
Chinese source rows and all 36 original asset files remain unchanged. This release
does not complete the wider travel-information and life localization backlog.

The owner explicitly chose to repair the security audit first, then back up,
deploy and publish this cohort. Security PR [#1887](https://github.com/x812033727/travel_scanner/pull/1887)
was merged after all 22 exact-head checks and an enforcing dependency audit passed.
Its API tests matched the preceding main revision: 8327 passed, 25 skipped. The
merged-main enforcing audit also passed. Installed production package versions
were checked after deployment; issue #1646 was then closed.

Content PR [#1911](https://github.com/x812033727/travel_scanner/pull/1911) is included
in deployed revision `911443f2d0fb102dbe501d265849746af185a787`. There were no migrations, application-code,
Compose or Dockerfile changes in the approved range.

| Gate | Actual result |
| --- | --- |
| Full database backup | 566,709,335 bytes; pg_dump exit 0; actual isolated pg_restore exit 0 |
| New-image rehearsal | 48 drafts, 48 publications, 0 hubs; exactly 96 new revisions and 96 audits |
| Isolated preservation and replay | Protected rows and all 167 table rowsets unchanged after replay |
| Deployment | Native exit 0; health 3/3; all 11 API-image services and actual dependency versions verified |
| Publication | 48 public v2 translations; 60 total five-language documents; source12 full rows unchanged |
| Production replay | Four phases exited 0; selected documents, versions and authorized history unchanged |
| Public acceptance | 60 exact documents, 144 translated assets and 24 displayed original images; complete API/XML sitemap chains |
| Browser and independent review | 120 original desktop/mobile screenshots viewed by three independent reviewers |
| Link acceptance | All 140 new unpublished-reference findings retain authored plain text without a clickable link |
| Final host verification | Own hold cleared after acceptance; unchanged verifier: 11 PASS, 0 FAIL |

Backup SHA-256: `73986f5b6671a71b73b160fdf912826db89a3c0bf5351bbd1b1510557e8e09c3`.
Native manifest: `c7a96098b4e8483937394e666144194d950f1b94e634d49b2d5f6fa5d13c6de0`.
Publication completed: 2026-10-28T12:32:13.580443+00:00.
Final acceptance completed: 2026-10-28T13:16:29.116263+00:00.

The main acceptance collection made 461 actual HTTP
requests, all returning 200. Optional
requests cancelled before fetching are recorded separately, not counted as HTTP
successes. The browser closed and all route tasks drained before evidence sealing.
Machine checks and independent visual review have separate receipts. Visual
review covers rendering, readable glyphs, images, clipping and desktop/mobile
layout; it is not a fresh word-for-word translation audit. Per-image limitations
are preserved in the private reviews and summarized in evidence.json.

The original strict 1300 ms request-spacing check failed: one of 460 measured
intervals was 1299 ms. The other 459 met the configured minimum and no requests
overlapped. The original failure and timestamps are preserved. Independent
review and an explicit operational decision admit only this exact hash-bound
capture's one-millisecond deviation; a new offline assembler reruns every other
guard unchanged. `strict_configured_minimum_met` remains false in the mechanical,
aggregate, final QA and this release evidence. Strict 1.3-second pacing is not
claimed. Future deadline and settled-layout guidance is tracked separately.

One original Simplified Chinese inference desktop screenshot retained the header's
loading placeholder. A separate settled-header capture, independently viewed by
reviewer C, confirms the complete navigation; its 19 actual requests all returned
200. The first supplemental attempt also had 19 HTTP 200 responses, then stopped
on an ambiguous local selector; that failure is preserved. The English SFT desktop
capture ends before the final copyright strip, which is visible in its mobile
capture. Original captures are unchanged, and neither unseen pixels nor interactive
horizontal scrolling are claimed as reviewed.

The native `report_progress.py` accounting also exited 0 with no evidence errors:
all seven stages, from translation through browser verification, completed 48/48.
It binds the original baseline, reviewed jobs, bundle, actual production journal
and a separate reviewed browser-evidence wrapper. This is historical evidence
accounting, not another live database query. The twelve unchanged source locales
required no translation work; their public acceptance is recorded separately.
The detailed QA retains the timing deviation, which the native summary does not
have a field to express. Original baseline, bundle, journal and captures remain
unchanged.

The native link rebuild and five-language comparison retained existing global
findings. There were no unexpected new findings. References to untranslated
same-language articles were verified against authored ArticleInline text, saved
API link resolution and captured DOM; this does not claim the site's entire link
backlog is resolved.

The complete captured public sitemap independently enumerated the remaining
scope after publication: travel information has 12 incomplete articles / 48
missing locale versions, and life has 654 incomplete articles / 2616 missing
locale versions. Total: 2664. This is a publication-aware public enumeration,
excluding hidden, expired and draft-only entries; it is not an atomic database
census. The saved page hashes and observation times bind this count, rather than
subtracting this release from an old inventory.

| Article | zh-TW | en | ja | ko | zh-CN |
| --- | --- | --- | --- | --- | --- |
| `ai-term-artificial-intelligence` | [v10](https://mokaair.com/zh-TW/life/ai-term-artificial-intelligence) | [v2](https://mokaair.com/en/life/ai-term-artificial-intelligence) | [v2](https://mokaair.com/ja/life/ai-term-artificial-intelligence) | [v2](https://mokaair.com/ko/life/ai-term-artificial-intelligence) | [v2](https://mokaair.com/zh-CN/life/ai-term-artificial-intelligence) |
| `ai-term-machine-learning` | [v8](https://mokaair.com/zh-TW/life/ai-term-machine-learning) | [v2](https://mokaair.com/en/life/ai-term-machine-learning) | [v2](https://mokaair.com/ja/life/ai-term-machine-learning) | [v2](https://mokaair.com/ko/life/ai-term-machine-learning) | [v2](https://mokaair.com/zh-CN/life/ai-term-machine-learning) |
| `ai-term-deep-learning` | [v8](https://mokaair.com/zh-TW/life/ai-term-deep-learning) | [v2](https://mokaair.com/en/life/ai-term-deep-learning) | [v2](https://mokaair.com/ja/life/ai-term-deep-learning) | [v2](https://mokaair.com/ko/life/ai-term-deep-learning) | [v2](https://mokaair.com/zh-CN/life/ai-term-deep-learning) |
| `ai-term-neural-network` | [v2](https://mokaair.com/zh-TW/life/ai-term-neural-network) | [v2](https://mokaair.com/en/life/ai-term-neural-network) | [v2](https://mokaair.com/ja/life/ai-term-neural-network) | [v2](https://mokaair.com/ko/life/ai-term-neural-network) | [v2](https://mokaair.com/zh-CN/life/ai-term-neural-network) |
| `ai-term-generative-ai` | [v10](https://mokaair.com/zh-TW/life/ai-term-generative-ai) | [v2](https://mokaair.com/en/life/ai-term-generative-ai) | [v2](https://mokaair.com/ja/life/ai-term-generative-ai) | [v2](https://mokaair.com/ko/life/ai-term-generative-ai) | [v2](https://mokaair.com/zh-CN/life/ai-term-generative-ai) |
| `ai-term-transformer` | [v10](https://mokaair.com/zh-TW/life/ai-term-transformer) | [v2](https://mokaair.com/en/life/ai-term-transformer) | [v2](https://mokaair.com/ja/life/ai-term-transformer) | [v2](https://mokaair.com/ko/life/ai-term-transformer) | [v2](https://mokaair.com/zh-CN/life/ai-term-transformer) |
| `ai-term-attention-mechanism` | [v2](https://mokaair.com/zh-TW/life/ai-term-attention-mechanism) | [v2](https://mokaair.com/en/life/ai-term-attention-mechanism) | [v2](https://mokaair.com/ja/life/ai-term-attention-mechanism) | [v2](https://mokaair.com/ko/life/ai-term-attention-mechanism) | [v2](https://mokaair.com/zh-CN/life/ai-term-attention-mechanism) |
| `ai-term-pretraining` | [v8](https://mokaair.com/zh-TW/life/ai-term-pretraining) | [v2](https://mokaair.com/en/life/ai-term-pretraining) | [v2](https://mokaair.com/ja/life/ai-term-pretraining) | [v2](https://mokaair.com/ko/life/ai-term-pretraining) | [v2](https://mokaair.com/zh-CN/life/ai-term-pretraining) |
| `ai-term-inference` | [v2](https://mokaair.com/zh-TW/life/ai-term-inference) | [v2](https://mokaair.com/en/life/ai-term-inference) | [v2](https://mokaair.com/ja/life/ai-term-inference) | [v2](https://mokaair.com/ko/life/ai-term-inference) | [v2](https://mokaair.com/zh-CN/life/ai-term-inference) |
| `ai-term-model-parameters` | [v10](https://mokaair.com/zh-TW/life/ai-term-model-parameters) | [v2](https://mokaair.com/en/life/ai-term-model-parameters) | [v2](https://mokaair.com/ja/life/ai-term-model-parameters) | [v2](https://mokaair.com/ko/life/ai-term-model-parameters) | [v2](https://mokaair.com/zh-CN/life/ai-term-model-parameters) |
| `ai-term-overfitting` | [v2](https://mokaair.com/zh-TW/life/ai-term-overfitting) | [v2](https://mokaair.com/en/life/ai-term-overfitting) | [v2](https://mokaair.com/ja/life/ai-term-overfitting) | [v2](https://mokaair.com/ko/life/ai-term-overfitting) | [v2](https://mokaair.com/zh-CN/life/ai-term-overfitting) |
| `ai-term-supervised-fine-tuning` | [v8](https://mokaair.com/zh-TW/life/ai-term-supervised-fine-tuning) | [v2](https://mokaair.com/en/life/ai-term-supervised-fine-tuning) | [v2](https://mokaair.com/ja/life/ai-term-supervised-fine-tuning) | [v2](https://mokaair.com/ko/life/ai-term-supervised-fine-tuning) | [v2](https://mokaair.com/zh-CN/life/ai-term-supervised-fine-tuning) |

Sanitized counts, public document versions and hashes, original screenshot hashes
and receipt hashes are in [evidence.json](evidence.json). Full private source
snapshots, journals, logs and screenshots remain outside Git. The full backup and
restored sandbox remain on the host. Only the release driver's own hold was cleared.
