---
id: 2026-10-05-qwen-local-deployment-ollama-variant-sizes
title: qwen-local-deployment does not explain Ollama's new size ranges, and its qwen3.6 sizes predate them
status: done
priority: P3
area: docs
owner: claude-opus-5-5-small-content-fixes
claimed_at: 2026-10-05T13:38:31Z
created_at: 2026-10-05T06:45:40Z
completed_at: 2026-10-05T14:19:16Z
branch: claude/small-content-fixes
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

- [x] The size bullets, the comparison table's rows and caption, and the diagram's size label
      (SVG text and the image `description`) match the tags pages on the day they are re-read,
      and their sources' `checked_on` is that day.
- [x] One plain sentence tells the reader why a default tag now shows a size range (which build
      Ollama pulls), sourced from an Ollama page that says so; if no page says so, the text says
      only what the page shows.
- [x] `pack_cli lint --kind life --slug qwen-local-deployment` stays at 0 errors (the pack is at
      the 20-source cap: replace rather than add).

## Steps

- [x] Re-read the four tags pages and one default tag page per family with the editorial
      User-Agent; find an Ollama doc or blog page that explains the mlx and llamacpp builds.
- [x] Rewrite the qwen3.6 bullet and the table's qwen3.6:27b row, and add the explanation; check
      the "檔案大小是要下載的量" paragraph, the table caption and the intro sentence that dates the
      numbers.
- [x] Redraw the diagram's "qwen3.5:9b 是 6.6GB" label from the page (or drop the number) and
      update the image `description` to match.
- [x] Check the sibling `deepseek-local-with-ollama` the same way and file a ticket if it drifted.
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
- 2026-10-05, claude-opus-5-5-small-content-fixes (branch `claude/small-content-fixes`). Pages read
  that day with the editorial User-Agent, all HTTP 200: the qwen3.5, qwen3.6, qwen3.8 and
  qwen3.8-flash-next tags pages; the default tag pages qwen3.5:9b, qwen3.6:27b, qwen3.6:35b and
  qwen3.8:27b; the qwen3.8 and qwen3.8-flash-next library pages; the Ollama blog index and its MLX
  (2026-03-30, 06-11) and GGUF (06-05) posts; docs.ollama.com `llms.txt`, macos, windows, gpu, faq,
  cli, import, api/pull, api/tags; the GitHub releases API and the v0.40.0-rc3 release page.
- What the pages show: each default tag page has a "Details" box with two tabs, `mlx` and
  `llamacpp`, each with its own blob and size: qwen3.5:9b 7.6GB / 6.6GB, qwen3.6:27b 19GB / 18GB,
  qwen3.6:35b 24GB / 23GB, qwen3.8:27b 18GB / 18GB. The tags page prints the two as a range, and a
  single number when they are equal (qwen3.8). qwen3.6 on 2026-10-05: latest and 35b share the ID
  8a43277aac50 (23GB - 24GB), 27b is 18GB - 19GB, and there are coding tags for 35b as well as
  27b (`35b-coding`, `35b-a3b-coding`, both 23GB - 24GB). qwen3.5's ranges (#1255) still match;
  qwen3.8 27b 18GB and qwen3.8-flash-next q4_K_M 120GB / q8_0 189GB still match, as do their
  library-page claims (vision, tools, thinking; "experimental preview of the architecture that will
  underpin Qwen4").
- Which build gets pulled: no docs.ollama.com page or blog post says. The only Ollama page that does
  is the GitHub release note of v0.40.0-rc3, a pre-release on 2026-10-05: "on Apple Silicon
  devices, model architectures supported by the MLX runtime will automatically run on MLX", naming
  qwen3.8, qwen3.6 and qwen3.5. The new text says exactly that, calls it the 0.40.0 預覽版, and keeps
  the consequence to 「可能不同」. The docs also show an MLX (CUDA) package for Windows, so the text
  does not claim that only Macs get the mlx build. When 0.40.0 ships, re-check that sentence.
- Sources (still 20): the GitHub QwenLM/Qwen3.8 README, which no sentence cited on its own, became
  the v0.40.0-rc3 release page. The Ollama qwen3.8 library page became the qwen3.5:9b tag page
  (the two builds and their sizes). Its two claims stay sourced: the vision/tools/thinking labels
  are on the qwen3.8 tags page header (title updated to say so), and the thinking default and
  reasoning_effort sentence already cites the Hugging Face Qwen3.8-27B model card. The four tags
  pages and the two new sources have `checked_on` 2026-10-05.
- Text changes: the intro (block 1) now dates the Ollama tag-page sizes to 2026-10-05; the qwen3.6
  bullet; two sentences that explain the range open the "檔案大小是要下載的量" paragraph (block 6);
  the table's qwen3.6:27b row (18 到 19GB) and caption; the image `description`, and the SVG's
  label and `<desc>`, now 「qwen3.5:9b 是 6.6 到 7.6GB」. The label fits its box (rendered to PNG
  with `render_svg` and looked at). The search-page facts (block 4) were not re-read and keep their
  2026-09-14 date. The pack `description` first kept dating every source to 2026 年 9 月 14 日;
  after review of PR #1290 it says, as block 1 does, that the Ollama tag-page file sizes were
  re-checked on 10 月 5 日 (the parenthetical follows `ai-video-tools-compared`'s description).
- Checks: `pack_cli lint --kind life --slug qwen-local-deployment` 0 errors, 1 warning
  (`no_summary`, as on main); `intake_check.py --slug qwen-local-deployment --from-content`: the
  diagram-number check passes. Its two FAILs (first block is not a summary; 本文/這篇 three times)
  were already there on main, and this change adds no self-reference.
- Sibling `deepseek-local-with-ollama`: the deepseek-r1 tags page on 2026-10-05 still shows 1.5b
  1.1GB, 7b 4.7GB, 8b 5.2GB (= latest), 14b 9.0GB, 32b 20GB, 70b 43GB, 671b 404GB, and 7b q8_0
  8.1GB / fp16 15GB. There are no ranges and no mlx builds (deepseek-r1 is not in the 0.40.0-rc3
  MLX list), so it has not drifted and no ticket was filed.
- Left: re-import the slug on the host after the merge (publish after merge, coordinator, owner
  consent).
