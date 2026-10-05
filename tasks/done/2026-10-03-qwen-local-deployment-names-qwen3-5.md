---
id: 2026-10-03-qwen-local-deployment-names-qwen3-5
title: qwen-local-deployment names qwen3.5:cloud as a cloud tag but the qwen3.5 tags page lists no cloud tag
status: done
priority: P3
area: docs
owner: claude-opus-5-5-ai-article-rechecks
claimed_at: 2026-10-05T06:14:45Z
created_at: 2026-10-03T17:55:52Z
completed_at: 2026-10-05T06:48:55Z
branch: claude/ai-article-rechecks
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

- [x] The sentence names a cloud tag that the cited Ollama page shows on the day it is re-read,
      or no tag at all, and its source's `checked_on` is that day.
- [x] `pack_cli lint --kind life --slug qwen-local-deployment` stays at 0 errors.

## Steps

- [x] Re-read the qwen3.5 tags page and the Qwen families' library pages with the editorial
      User-Agent; record which of them, if any, has a cloud tag today.
- [x] Rewrite the sentence from what the page shows (the series' rule for telling local from
      cloud is in `docs/ai-workflow-series/agent-local/README.md`: a local address and a tag
      without `cloud`, with a file size on the tag page).
- [ ] After the merge, re-import the one slug on the host with `guides-import --slug`.
      Publish after merge (coordinator, owner consent).

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

### Re-read on 2026-10-05 (claude-opus-5-5-ai-article-rechecks)

Fetched with `curl -sSL` and the editorial User-Agent, all HTTP 200, HTML comments stripped:

- https://ollama.com/library/qwen3.5/tags, qwen3.6/tags, qwen3.8/tags, qwen3.8-flash-next/tags and
  the qwen3.5, qwen3.6 and qwen3.8 library pages: no tag containing `cloud` on any of them
  (`grep -i cloud` finds nothing in the stripped text).
- https://ollama.com/search?q=qwen: the only "cloud" strings are the Cloud capability filter and
  a Qwen 1.5 description ("Alibaba Cloud"); no Qwen family carries a cloud badge.
- https://ollama.com/search?c=cloud and https://ollama.com/api/tags (the cloud model list): no
  Qwen model among the 16 libraries and 17 names listed.
- https://docs.ollama.com/cloud: cloud models run in Ollama's cloud and "do not need to be
  downloaded"; in the app or CLI their names carry `cloud` (its example is `gemma4:cloud`).

So the sentence now names no tag: "標籤名稱帶 cloud 的跑在 Ollama 的雲端，不是你的電腦，別誤以為選了就是離線可用。"
`grep -c 'qwen3[.]5:cloud'` on the pack is 0.

Two things the plan did not expect:

- The pack already has 20 sources, the schema maximum (`pack_cli lint` fails with "List should
  have at most 20 items" when a 21st is added), so `docs.ollama.com/cloud` could not be added as
  the sentence's source. The sentence stays with the qwen3.5 tags page, as before, and that page's
  `checked_on` is now 2026-10-05.
- Ollama re-published the qwen3.5 tags about 2026-10-04 with an mlx and a llamacpp build per
  default tag, and the tags page now shows size ranges. Dating that page 2026-10-05 with the old
  sizes would have certified numbers the page no longer shows, so the qwen3.5 bullet was changed
  to the page's values (0.8b 1.2 到 1.3GB, 2b 2.7 到 3.1GB, 4b 3.3 到 4.0GB, 9b 6.6 到 7.6GB,
  27b 17 到 20GB, 35b 22GB, 122b 81GB; 256K context, text and image input, latest is 9b: unchanged).
  Explaining the ranges and the qwen3.6 drift (now 18 to 19GB and 23 to 24GB) is left to
  `2026-10-05-qwen-local-deployment-ollama-variant-sizes`; the qwen3.6, qwen3.8 and
  flash-next sources keep 2026-09-14.

Review of PR #1255 found that the comparison table near the end still gave the September sizes
for the same tags (qwen3.5:4b 3.4GB, 35b 24GB) under the caption 查證於 2026 年 9 月, so the article
showed two sizes for one tag. The tags page re-read on 2026-10-05 (HTTP 200) shows 4b 3.3GB - 4.0GB,
9b 6.6GB - 7.6GB, 27b 17GB - 20GB and 35b 22GB, so the four qwen3.5 rows now carry those values,
the caption says the qwen3.5 sizes were re-checked on 2026 年 10 月 5 日, and the intro sentence
that dated every number to 2026 年 9 月 14 日 now names the same exception. The table's qwen3.6:27b
row (18GB) and the diagram's "qwen3.5:9b 是 6.6GB" (in `diagram-1.svg`, outside this scope) were
added to `2026-10-05-qwen-local-deployment-ollama-variant-sizes`.

Checks: `PYTHONUTF8=1 uv run python -m app.guides.pack_cli lint --kind life --slug qwen-local-deployment`
reports 0 errors; with `--warnings` only the existing `no_summary` warning.

Left: the host re-import. Publish after merge (coordinator, owner consent).
