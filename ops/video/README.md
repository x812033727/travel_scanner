# Video worker document initialization

The image keeps its repository snapshot at `/opt/mokaair/docs-seed/videos`.
The `video_docs` volume mounts at `/opt/mokaair/docs/videos`, which is writable
by `pwuser`. The seed remains outside that mount and is owned by root.

On every worker startup, `sync-docs.mjs` initializes or refreshes the volume
before pairing, the Shorts tick, or `auto`. A failed sync stops startup with a
nonzero exit code. Recreating a container with a newer image therefore refreshes
the existing volume using the same rules as the first start:

- Top-level files other than `lexicon.json` belong to the repository and are
  refreshed from the image. This includes the channel's `README.md`, which the
  planner reads at runtime.
- Existing top-level directories belong to the worker. They are preserved in
  full, including video drafts and edits. A directory from the image is copied
  only when that name is absent from the volume; existing directories are not
  filled in or updated.
- `lexicon.json` belongs to the worker after its first seed. If it is absent,
  the image supplies it. An existing dictionary is preserved, including terms
  the worker has added. Later repository dictionary changes are not merged
  automatically.
- Nothing is removed from the volume when it disappears from the image.

The helper uses the paths above by default. Tests and local checks can supply
separate source and destination directories:

```sh
node ops/video/sync-docs.mjs /tmp/video-docs-seed /tmp/video-docs-volume
node --test ops/video/sync-docs.test.mjs
```

The Dockerfile's `smoke` target runs the sync tests and initializes the actual
image paths as `pwuser` before the existing document and media checks. The
`Video worker image` CI workflow builds that target:

```sh
docker build -f ops/video/Dockerfile --target smoke --progress plain .
```

These checks exercise image startup behavior. Updating a running production
worker still requires the normal deployment procedure.
