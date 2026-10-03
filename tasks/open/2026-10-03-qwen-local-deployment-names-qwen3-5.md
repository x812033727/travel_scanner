---
id: 2026-10-03-qwen-local-deployment-names-qwen3-5
title: qwen-local-deployment names qwen3.5:cloud as a cloud tag but the qwen3.5 tags page lists no cloud tag
status: open
priority: P3
area: docs
owner:
claimed_at:
created_at: 2026-10-03T17:55:52Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/guides/content/qwen-local-deployment.json
---

# qwen-local-deployment names qwen3.5:cloud as a cloud tag but the qwen3.5 tags page lists no cloud tag

## Why

`qwen-local-deployment` (zh-TW, sources read on 2026-09-14) uses `qwen3.5:cloud` once as its
example of an Ollama cloud tag. While fact-checking `ai-workflow-agent-glm-qwen-deepseek` on
2026-10-03, the checker read https://ollama.com/library/qwen3.5/tags and found no tag with
`cloud` in it among the 65 listed; the copy of that page the coordinator fetched the same day
agrees. The new article links to this one as its second closing link, so a reader who follows
the link meets a tag the library page no longer shows. Either the tag was withdrawn after
2026-09-14 or it never was on that page.

## Definition of done

- [ ] The sentence names a cloud tag that the cited Ollama page shows on the day it is re-read,
      or no tag at all, and its source's `checked_on` is that day.
- [ ] `pack_cli lint --kind life --slug qwen-local-deployment` stays at 0 errors.

## Steps

- [ ] Re-read the qwen3.5 tags page and the Qwen families' library pages with the editorial
      User-Agent; record which of them, if any, has a cloud tag today.
- [ ] Rewrite the sentence from what the page shows (the series' rule for telling local from
      cloud is in `docs/ai-workflow-series/agent-local/README.md`: a local address and a tag
      without `cloud`, with a file size on the tag page).
- [ ] After the merge, re-import the one slug on the host with `guides-import --slug`.

## How to verify

```bash
curl -sL -A "Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)" \
  https://ollama.com/library/qwen3.5/tags | grep -o -i 'qwen3[.]5:[a-z0-9._-]*cloud[a-z0-9._-]*' | sort -u
# empty on 2026-10-03
grep -o 'qwen3[.]5:cloud' apps/api/app/guides/content/qwen-local-deployment.json   # one hit today
cd apps/api && uv run python -m app.guides.pack_cli lint --kind life --slug qwen-local-deployment
```

## Notes

- Found by the first-round fact-checker of `ai-workflow-agent-glm-qwen-deepseek`
  (`docs/ai-workflow-series/factcheck/ai-workflow-agent-glm-qwen-deepseek.md`, "留給站主").
  Not fixed there: the file is outside that ticket's scope.
