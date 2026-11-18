---
id: 2026-11-18-illustrated-ai-and-technology-news-channels
title: Illustrated AI and technology news channels
status: done
priority: P2
area: web
owner: codex-news-discovery
claimed_at: 2026-11-18T07:57:37Z
created_at: 2026-11-18T07:55:57Z
completed_at: 2026-11-18T08:18:03Z
branch: codex/news-discovery-seo-20261118
depends_on: []
scope:
  - apps/web/components/guides/article-page.tsx
  - apps/web/components/guides/article-page.test.tsx
  - apps/web/components/guides/news-list.tsx
  - apps/web/components/guides/news-list.test.tsx
  - apps/web/components/guides/topic-hub-page.tsx
  - apps/web/components/guides/topic-hub-page.test.tsx
  - docs/content/news-image-playbook.md
  - apps/web/public/guides/tech-news-github-microsoft-mdash-open-source-fixes-20261117/mdash-pilot-zh-tw.png
  - apps/web/public/guides/ai-news-sagemaker-hyperpod-nvidia-dynamo-20261117/dynamo-inference-zh-tw.png
  - apps/web/components/guides/channel-guide.tsx
  - apps/web/messages/zh-TW/common.json
  - apps/web/messages/zh-CN/common.json
  - apps/web/messages/en/common.json
  - apps/web/messages/ja/common.json
  - apps/web/messages/ko/common.json
---

# Illustrated AI and technology news channels

## Why

Both news channels present the current reports with equal weight. Recent automatic stories lack representative pictures, and readers have little indication of the illustrated guides available alongside the news.

## Definition of done

- [x] Readers can scan the lead and supporting reports and open a published illustrated guide in their language.
- [x] Article previews use a suitable visible editorial picture and report their assigned news section.

## Steps

- [x] Check image use on the comparison site and the current Mokaair channels.
- [x] Preserve chronological order, pagination and compact archive views.
- [x] Verify real localized content on desktop and phones.

## How to verify

Run the news list, channel and article tests, the web checks and a production build. In a browser open a channel, follow its headline and illustrated guide, switch channels and check a paged view.

## Notes

The task shares the existing news discovery draft. The two video-worker tasks claim the messages directory for admin copy. This task only changes the public guides label in the five common catalogues.

November 18 public API replay covered 24 headlines per channel in all five languages. Chrome covered both desks at 1440, 390 and 320 pixels with JavaScript disabled, the RSS feed, pagination and actual headline and guide destinations. The local production build, focused web tests, lint, type check and translation checks passed. The first build surfaced two existing npm advisories affecting the locked Next.js 16.4.2. A subsequent normal build completed.

The [editor's image guide](../../docs/content/news-image-playbook.md) includes original 1600 × 900 Traditional Chinese figures for MDASH and Dynamo, case-specific captions and direct sources. These assets can be inserted into the corresponding published reports through the CMS after deployment.
