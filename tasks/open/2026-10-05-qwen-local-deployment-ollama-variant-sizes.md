---
id: 2026-10-05-qwen-local-deployment-ollama-variant-sizes
title: qwen-local-deployment does not explain Ollama's new size ranges, and its qwen3.6 sizes predate them
status: open
priority: P3
area: docs
owner:
claimed_at:
created_at: 2026-10-05T06:45:40Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/guides/content/qwen-local-deployment.json
  - apps/web/public/guides/qwen-local-deployment/diagram-1.svg
---

# qwen-local-deployment does not explain Ollama's new size ranges, and its qwen3.6 sizes predate them

## Why

Ollama re-published the default Qwen tags with two builds each. On 2026-10-05 the tag page
https://ollama.com/library/qwen3.5:9b lists "Details: mlx, llamacpp", and the tags pages now
show a size range for a default tag instead of one number (qwen3.5 updated about 2026-10-04,
qwen3.6 "4 days ago", that is about 2026-10-01). The pack `qwen-local-deployment` (zh-TW, sources
read 2026-09-14) was written when each tag had one size:

- qwen3.5: fixed in `2026-10-03-qwen-local-deployment-names-qwen3-5` (branch
  `claude/ai-article-rechecks`). That ticket had to date the qwen3.5 tags page 2026-10-05, so it
  copied the page's ranges into the bullet (0.8b 1.2 到 1.3GB, 2b 2.7 到 3.1GB, 4b 3.3 到 4.0GB,
  9b 6.6 到 7.6GB, 27b 17 到 20GB, 35b 22GB, 122b 81GB) and into the four qwen3.5 rows of the
  comparison table near the end (its caption now says the qwen3.5 sizes were re-checked on
  2026 年 10 月 5 日), without saying why there is a range.
- qwen3.6: the bullet still says "27b 是 18GB、35b 是 23GB" and the comparison table's
  qwen3.6:27b row says 18GB; the tags page shows 27b 18GB - 19GB and 35b 23GB - 24GB (latest
  still points at 35b; the 27b-coding tags are still there).
- The flow diagram `apps/web/public/guides/qwen-local-deployment/diagram-1.svg` prints
  "qwen3.5:9b 是 6.6GB", and the pack's image `description` repeats it; the page now shows
  6.6GB - 7.6GB for that tag.
- qwen3.8 (27b 18GB) and qwen3.8-flash-next (q4_K_M 120GB, q8_0 189GB) still match on 2026-10-05,
  but their tags pages also list mlx and nvfp4 variants (`27b-mlx`, `125b-mlx`, `*-nvfp4`).

A reader who pulls a default tag on a Mac and elsewhere may download different files, and the
paragraph after the list says the file size is the download amount and the memory floor.

## Definition of done

- [ ] The size bullets, the comparison table's rows and caption, and the diagram's size label
      (SVG text and the image `description`) match the tags pages on the day they are re-read,
      and their sources' `checked_on` is that day.
- [ ] One plain sentence tells the reader why a default tag now shows a size range (which build
      Ollama pulls), sourced from an Ollama page that says so; if no page says so, the text says
      only what the page shows.
- [ ] `pack_cli lint --kind life --slug qwen-local-deployment` stays at 0 errors (the pack is at
      the 20-source cap: replace rather than add).

## Steps

- [ ] Re-read the four tags pages and one default tag page per family with the editorial
      User-Agent; find an Ollama doc or blog page that explains the mlx and llamacpp builds.
- [ ] Rewrite the qwen3.6 bullet and the table's qwen3.6:27b row, and add the explanation; check
      the "檔案大小是要下載的量" paragraph, the table caption and the intro sentence that dates the
      numbers.
- [ ] Redraw the diagram's "qwen3.5:9b 是 6.6GB" label from the page (or drop the number) and
      update the image `description` to match.
- [ ] Check the sibling `deepseek-local-with-ollama` the same way and file a ticket if it drifted.
- [ ] After the merge, re-import the slug on the host with `guides-import --slug` (owner consent).

## How to verify

```bash
curl -sL -A "Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)" https://ollama.com/library/qwen3.6/tags \
  | sed 's/<[^>]*>/\n/g' | grep -E 'GB( - [0-9.]+GB)? •' | head
cd apps/api && PYTHONUTF8=1 uv run python -m app.guides.pack_cli lint --kind life --slug qwen-local-deployment
```

## Notes

- Found by claude-opus-5-5-ai-article-rechecks on 2026-10-05 while closing
  `2026-10-03-qwen-local-deployment-names-qwen3-5`. That ticket was told to leave other sentences
  alone, so it changed only what cites the qwen3.5 tags page it had to re-date: the qwen3.5
  bullet, and (after review of PR #1255) the table's qwen3.5 rows, its caption and the intro
  sentence that dated every number to 2026 年 9 月 14 日. The diagram is outside its scope.
- The pack already lists 20 sources, the schema maximum; `docs.ollama.com/cloud` (which says
  cloud models use names such as `gemma4:cloud` and run in Ollama's cloud) could not be added
  there for the same reason.
