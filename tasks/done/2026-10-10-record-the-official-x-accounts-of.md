---
id: 2026-10-10-record-the-official-x-accounts-of
title: Record the official X accounts of AI companies and the first-party page the scanner reads for each
status: done
priority: P2
area: docs
owner: claude-opus-5-5-official-accounts
claimed_at: 2026-10-10T07:34:23Z
created_at: 2026-10-10T07:34:16Z
completed_at: 2026-10-10T07:42:14Z
branch: claude/official-accounts-list-f2d973
depends_on: []
scope:
  - docs/official-ai-accounts.md
  - tasks/open/2026-09-30-evaluate-social-accounts-with-public-rss.md
---

# Record the official X accounts of AI companies and the first-party page the scanner reads for each

## Why

The owner asked on 2026-10-10 for the official X accounts of AI companies (the way
`@AnthropicAI`, `@claudeai` and `@ClaudeDevs` are Claude's), so the latest news, updates
and tutorials can be followed at the source and turned into news and tutorial videos.
Nothing in the repository listed them, and nothing recorded which first-party page the
news scanner reads for each company, or why it cannot read one.

Impersonation is common on X, and several handles a person would guess are wrong or
renamed (`@xai` is now `@SpaceXAI`, Microsoft links `@MSFTCopilot` and not `@Copilot`,
MiniMax is `@MiniMax_AI` with one underscore). A checked list saves the next session
the same research and keeps an unverified handle off an article or a video card.

## Definition of done

- [x] `docs/official-ai-accounts.md` lists each account with what it posts, the
      first-party page that links to it (or "third-party only", "unverified",
      "conflicting"), the company's own update page, and whether the scanner reads it.
- [x] The page states that nothing reads x.com, and the two rules for using a row.
- [x] The 2026-10-10 answer to the X question (the paid API's price, and the owner's
      "no") is on the ticket that holds the 2026-09-30 decision.
- [x] The two pieces of work this list leads to are filed as their own tasks.

## Steps

- [x] Verify each handle against a first-party page (web research, 2026-10-10).
- [x] Write the document, grouped by company.
- [x] Note the price and the decision on
      `2026-09-30-evaluate-social-accounts-with-public-rss`.
- [x] File `2026-10-10-add-official-changelog-and-developer-update` and
      `2026-10-10-official-pages-the-news-writer-declined`.

## How to verify

```bash
npm run check:tasks
node --test tools/repo-hygiene.test.mjs
```

Open `docs/official-ai-accounts.md` and follow three "verified by" links at random: each
page should carry a link to the handle on its row.

## Notes

- "Verified" means a first-party page links to the handle. x.com itself could not be
  loaded during the research, so no row was checked against the live profile.
- Third-party only: `@ClaudeDevs`, `@Gemini_Notebook`, `@Hailuo_AI`. No first-party page
  links to `@GoogleAIStudio`, `@MetaAI` or `@GitHubCopilot`. ElevenLabs' own pages disagree
  (`@elevenlabs` on its GitHub organisation, `@elevenlabsio` on Hugging Face).
- Found while checking the owner's question about the Claude release-notes page:
  `claude.com/blog` now redirects to `claude.com/resources/articles`, and the "Claude blog"
  row in `sources.json` still filters on `/blog/`, so by its own config it reads nothing.
  Developer posts moved to `claude.dev`, which has an RSS feed. Both are in the next task.
- The owner decided on 2026-10-10 not to use the X API after seeing the price.
