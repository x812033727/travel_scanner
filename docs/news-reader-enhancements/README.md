# News that answers a reader's question

This change connects the news layout preview to better drafting, deeper evidence,
useful follow-on reading, real subscriptions and measurable editorial outcomes.
It is prepared code and reviewed content; it has not been deployed or published.

| Improvement | Reviewable result | What runs automatically after deployment |
| --- | --- | --- |
| Select substantive news | Writer/editor instructions identify an audience, answer a concrete question and preserve regional, account and price limits. Unsupported promotional stories use the existing eligibility gate. | Existing news jobs use the revised instructions. No extra paid scoring stage was added. |
| Show real experiments | [Lazy-loading field test](lazy-loading-lab/article.md), structured draft, original fixtures and evidence: 18 Edge runs, two viewport sizes. | The reproducible local runner is available; new experiments are not invented or silently scheduled. |
| Help readers do something next | Clearer related-reading descriptions, canonical topic links, a worked practical tutorial and three separately reviewed news rewrites in PR #2063. | Existing curated/topic-related article selection is reused. A recommendation is not falsely labelled as a tested tutorial. |
| Follow a subject | Five-language Atom feeds for the three news topics, subscription links, copyable URLs and discovery metadata. | A reader's feed app checks for new published entries. No account or email subscription is created. A topic is not claimed to be a verified event timeline. |
| Find information needing review | [Published-news source review](freshness.md), filterable and paginated in the admin news page. | With news automation enabled, bounded daily source checks record advisory outcomes. No model call, rewrite or republication is triggered. |
| Measure continuation | [First-party reading measurements](reading-and-measurement.md) and an independent admin analytics section. | When first-party analytics is enabled and privacy signals permit it, actual related/topic-link clicks are recorded. |

## Deeper official documentation

Enabled first-party evidence sources can explicitly opt into a maximum of two linked
documents on the exact same host, using their existing `config_json`, for example:

```json
{"supplemental_paths": ["/docs", "/help"]}
```

Use only path prefixes actually checked for that source. The default is off.
No URL is invented; only original article links are considered, with no second hop.
The existing SSRF-safe fetcher, robots rules, byte/request limits and hashes still
apply. Cross-host redirects and unreadable shells are rejected. Same-site documents
remain one publisher for the independent-evidence gate. This work does not change
any production source configuration.

## Publication and measurement boundaries

The 90-day source-review window only includes articles created by the news pipeline,
including manually approved ones; it does not imply that all historical/imported
content has been rechecked. Source text remaining unchanged is not a guarantee that
an offer or product is still valid.

Continuation figures count clicks. They are not search impressions, click-through
rates, completed reads or income. Search Console/advertising revenue were not
connected or inferred. No existing third-party consent is expanded.

The field-test sample is a reviewed Traditional Chinese preview, not an imported
content pack. It preserves the actual test conditions and avoids converting image
counts into speed or bandwidth claims. Production import/publication and translations
would be separate work. Original source-page HTML is retained locally for review,
not copied into this repository.
