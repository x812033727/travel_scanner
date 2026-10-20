# Pinning a reviewed manual story draft before media production

The worker pins a story's pronunciation dictionary before it writes the first chapter. A locally composed `video.json` already exists, so `initializeStoryLexicon` correctly refuses it with `STORY_LEXICON_MIGRATION_REQUIRED`. The old-chapter migration requires a genuine worker `auto.json` and chapter files; a manual draft must not invent either. This separate command pins the same genesis bytes only after the manual script, series plan and independent reviews are bound by hash and the media work directory is empty.

## Review receipt

Save a structured receipt under `docs/videos/<slug>/reviews/lexicon-bootstrap.json`. The three evidence files must also be under that `reviews/` directory, must each mention the current `video.json` SHA-256, and must match the SHA-256 values in the receipt. A reviewer should check the source review and two independent narrative readings before signing this decision; the `reviewer` field records attribution, not user authentication.

```json
{
  "schema_version": 1,
  "kind": "manual_story_lexicon_bootstrap_review",
  "slug": "story-everyday-netflix-x03",
  "video_json_sha256": "<64 lowercase hex characters>",
  "series_json_sha256": "<64 lowercase hex characters>",
  "decision": "pin_unspoken_manual_draft",
  "reviewer": "<independent reviewer identifier>",
  "evidence": [
    { "role": "source", "file": "reviews/source-review.md", "sha256": "<64 lowercase hex characters>" },
    { "role": "narrative_a", "file": "reviews/blind-a.md", "sha256": "<64 lowercase hex characters>" },
    { "role": "narrative_b", "file": "reviews/blind-b.md", "sha256": "<64 lowercase hex characters>" }
  ]
}
```

The command checks that `series.json` is a story, that `video.json` has the same slug, series and episode, and that the script, plan, receipt and three evidence files are regular files inside the project with matching hashes. It rejects media paths inside the repository, including paths whose ancestors are symlinks, before creating a lease. It refuses any existing work state, including `auto.json`, chapters, audio, timeline, approvals, media ledger, pending lexicon transaction or STOP. It never copies an existing pronunciation snapshot or changes `docs/videos/lexicon.json`.

## Command

The `--workdir` value is the **media base** outside this repository; the command appends the slug. The standalone CLI has no dependency on the worker's main `cli.mjs`.

```bash
node tools/video/lexicon-manual-bootstrap.mjs \
  --slug story-everyday-netflix-x03 \
  --workdir /workspace/.brand-video-workdir \
  --review docs/videos/story-everyday-netflix-x03/reviews/lexicon-bootstrap.json \
  --json

# Only after the read-only report says allowed and its hashes match the intended sources:
node tools/video/lexicon-manual-bootstrap.mjs \
  --slug story-everyday-netflix-x03 \
  --workdir /workspace/.brand-video-workdir \
  --review docs/videos/story-everyday-netflix-x03/reviews/lexicon-bootstrap.json \
  --apply
```

Without `--apply`, the command writes nothing, including no lease or work directory. `--apply` repeats admission under the project lease and the common lexicon-writer lease, then writes intents on both volumes, immutable genesis version/event and a provenance sidecar, selects `current.json`, reads the complete strict chain back, commits a work-volume receipt and only then clears the intents. It re-reads the script, series, receipt and three evidence files immediately before the first intent and again before the committed receipt; a changed byte aborts, leaving an in-progress transaction held if publication has begun. The sidecar records the current shared dictionary hash, seeded name tokens, script and series hashes, review receipt hash and its three evidence hashes. The genesis event remains byte-identical to an ordinary new story; the strict reader accepts no alternative genesis format.

After a crash **before** the committed receipt, the transaction stays held for operator review. A crash **after** the receipt can be recovered using its UUID, provided the sidecar, receipt, current pointer and immutable chain still match:

```bash
node tools/video/lexicon-manual-bootstrap.mjs \
  --slug story-everyday-netflix-x03 \
  --workdir /workspace/.brand-video-workdir \
  --recover <transaction-id>
```

The receipt is under `<media-base>/<slug>/story/lexicon-transactions/`. Recovery does not erase a partial transaction or approve script, audio, storyboard, final cut or publishing. Once pinned, the normal strict story reader and speech hash use the selected lexicon. A later script edit requires renewed story/source review and regenerated audio as usual; it does not silently repin this immutable genesis.
