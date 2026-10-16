# A01 + B18 exact-build diagnostic — HOLD (2026-10-17)

This isolated sandbox copied the active `build.mjs`, `series.json`, approved A01 row and review byte for byte. It copied the new B18 name-trim row and its first independent review byte for byte. The shim at `sandbox/tools/video/story-plans/plan.mjs` only re-exports the repository's actual validator; the compiler source is unchanged. `manifest.json` pins all inputs and receipts. No active `episodes/`, `reviews/`, or `stories.json` file was edited.

From the repository root:

```powershell
node docs/videos/brand-stories-pilot-v2-20261015/preproduction-20261016/B18-import-build-20261017/sandbox/docs/videos/brand-stories-pilot-v2-20261015/build.mjs --draft
node docs/videos/brand-stories-pilot-v2-20261015/preproduction-20261016/B18-import-build-20261017/sandbox/docs/videos/brand-stories-pilot-v2-20261015/build.mjs --write
$env:PYTHONPATH='apps/api'
& 'apps/api/.venv/Scripts/python.exe' docs/videos/brand-stories-pilot-v2-20261015/preproduction-20261016/B18-import-build-20261017/backend-check.py
```

`--draft` exits 0. The exact `--write` exits **1** with `B18: source and new reviewer caveats exceed 800 characters`, so this sandbox has **no compiled import file**. B18 source caveat length is 394, first review notes length is 425, and the compiler joins them with two newline characters: **821/800**. The Python diagnostic mirrors this in memory and `check_story_file` refuses B18 with `caveats must be text of at most 800 characters`. It is not a substitute for a successful exact build. A01's compiled row is deep-equal to active `stories.json`; the series is also deep-equal. The new B18 projection changes only `caveats`, `chapters`, `logline`, `must_verify`, `names`, `sources`, and `takeaway` compared with the active B18 projection.

The independent reviewer later made a **separate notes-only successor** at `../B18-review-short-20261017/`. Its B18 review changes only `notes`, retaining the same bound story SHA. Its isolated exact build produced `stories.json` SHA-256 `07a71fc18c3aa12d426dcc1c9ecd30e59c150079a1e83d868b7024c09670c999`. Read-only `check_story_file` on that successor returned A01/B18, `problems=[]`, `refused=[]`, `ignored=[]`, with B18 caveats **616/800**. Its compiler, series, A01 row/review, and B18 row match this sandbox byte for byte; only the reviewer-authored B18 review differs. Use that successor for further review. This original failed build remains an immutable explanation of why the first receipt cannot be imported.

No host access, import, worker, paid call, commit, or push occurred here. The successor's successful local checks do not approve formal scene review or authorize production import.
