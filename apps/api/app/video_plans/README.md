# Admin long-form planning catalog

`GET /api/v1/admin/video-plans` requires `content.read` and reads the immutable
`data/catalog.json` inside the API image. The video admin opens it through
`/zh-TW/admin/videos?tab=plans`. Viewing cannot create projects, requests, episodes,
jobs, approvals, schedules or publication records. Source stages describe authored
text and must not be treated as live database or media-production states.

Regenerate from the repository root after an authorized source-plan revision:

```sh
node tools/video/long-form/admin-catalog.mjs build
node tools/video/long-form/admin-catalog.mjs check
node --test tools/video/long-form/admin-catalog.test.mjs
```

The generator validates all source bytes, record hashes, source packages, effective
duration inputs and revised chapter budgets before writing. CI checks exact byte
reproduction; commit the generator and its generated bundle together. This bundle
currently contains 100 first-season outlines, 92 adopted second-season outlines,
100 third-season candidates, 100 brand-story plans and 81 AI-term records. The
covered AI-agent record remains a reference, not a new production request.

Deployment packages these plans through the existing API Dockerfile `COPY . .`;
neither a database migration nor an import/apply command is needed for visibility.
Missing or invalid data returns `503 video_plans_unavailable`, without a partial
catalog or a stale fallback. The API does not read host worker directories.

Search (`q`, up to 200 characters) matches titles, IDs and video slugs. `catalog`
and `stage` accept the schema's explicit values; pagination uses `page` (starting
at 1) and `page_size` (default 25, maximum 100). Counts describe the full catalog;
`total` describes the filtered result. Production targets are 600 seconds, or 780
seconds for brand stories. Both narrated content and finished-video acceptance
require at least 480 seconds, with intros/outros excluded from narrated content.
Historical source documents retain their original duration wording.
