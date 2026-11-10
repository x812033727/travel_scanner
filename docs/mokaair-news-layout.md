# Mokaair news and article layout

## Reader experience

The news desk on `/life` and the AI, technology and crypto news topic hubs now opens with its first chronological story. A larger headline and cover introduce it, followed by image-and-text rows with event dates and short descriptions. The topic sidebar links to the existing hubs. Continuation pages use ordinary rows and retain their existing cursor URLs.

Covers retain their full 16:9 composition so diagram labels and image credits are not cropped. On phones, the lead headline precedes the picture. Keyboard focus remains visible around the whole lead link.

The life hub uses a compact title/search masthead to bring news closer to the top. Existing topic browsing, curated articles, search and pagination remain available. The API's `news_date` still determines chronology; bulk import timestamps never substitute for it. Stories shared by several topics remain deduplicated on the life hub.

Lifestyle articles outside series use stronger title/deck typography and readable content width. Articles with three or more sections have a desktop contents rail and a folded mobile contents list. The desktop rail is bounded by the viewport and scrolls when long. Travel guides, course navigation, publication gating, canonical URLs and hreflang remain unchanged.

## Content and revenue boundaries

The layout uses actual published titles, descriptions, images and topic labels. Missing covers render as text-only stories. Existing authored summary blocks are preserved; there are no generated key points, made-up authors or popularity rankings. All interface labels reuse the five-language catalogs.

Existing in-article advertising and contextual affiliate integrations retain their placement and disclosure rules. The mockup's illustrative ad boxes and bookmark control were not introduced as inactive product controls. No new tracking, advertisement provider or backend dependency is added.

## Verification

- Component coverage: event dates, chronology, cross-topic deduplication, one lead, missing covers, topic URLs, cursor continuation, article headings and existing travel/series behavior.
- Browser coverage extends `guides-adsense.spec.ts`, already included in CI: news-to-article navigation, category/cursor/back navigation, desktop/mobile contents, deliberate scrolling, anchor hit testing and narrow-width enlarged text.
- Local visual captures use an isolated API with existing content packs; they do not read or write production data.

The initial visual review caught cropped diagram edges and a clipped keyboard focus outline. Both were corrected and covered by browser assertions. The original captures remain separate from the final evidence.

Validation results and the final commit are recorded in the associated task and pull request. Merge and deployment require the owner's separate approval.
