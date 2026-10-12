---
id: 2026-10-12-preserve-balanced-parentheses-when-extracting-video
title: Preserve balanced parentheses when extracting video description URLs
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-12T03:36:59Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/qa/links.mjs
  - tools/video/qa/links.test.mjs
---

# Preserve balanced parentheses when extracting video description URLs

## Why

The video QA URL extractor ends every URL at the first ASCII closing parenthesis.
A valid Commons filename such as `File:A_Cosmic_Explosion_Over_Siberia_(154488_-_russia_tunguskablast_oli_20240706_lrg).jpg`
therefore loses `).jpg`, and QA requests a different URL that returns a false 404.
H03 works around this in its asset-credit metadata with `%28`/`%29`; the shared parser remains affected.

## Definition of done

- [ ] Preserve valid balanced parentheses in paths, query strings and fragments, including nested pairs.
- [ ] Exclude outer prose/Markdown delimiters and trailing punctuation; preserve deduplication and ordering.
- [ ] Keep existing percent encoding unchanged and send the complete URL to the injected link checker.
- [ ] Genuine remote failures such as HTTP 403 remain failures, with separate source-readability evidence.

## Steps

- [ ] Add offline cases for the Commons filename, nested pairs, wrappers and percent-encoded URLs.
- [ ] Repair extraction and verify existing callers without changing provider-access behavior.

## How to verify

Run `node --test tools/video/qa/links.test.mjs tools/video/shorts/cut.test.mjs`, then applicable `test:tools` checks.
Use injected fetch responses; regression tests must not depend on live networking.

## Notes

H03's complete encoded URL returned 200 under the native checker. Its JPL source still returned 403;
that result was retained even though independent web access read the official article.
The failing field is `video.assets[1].url`, composed into the description's credit list.
Current tests cover external full-width parentheses and punctuation but omit balanced parentheses inside URLs.
