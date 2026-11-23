# Admin AI drama scripts

`GET /api/v1/admin/video-dramas` lists the AI dramas (恁祖媽今年18, 種田娶妻打天下, 歐德江湖,
零根妖族, 修仙獎勵) with each episode's available texts and the series documents;
`/{series}/episodes/{slug}` returns an episode's `brief`, `script`, `storyboard` and `review`
Markdown, and `/{series}/documents/{id}` one series document (the top-level
Markdown of the series planning folder: outline, seasons, setting, README; rules and lessons
change often and are left out). All require `content.read` and read only the immutable files
in `data/` inside the API image: `index.json` plus one content file per series, whose sha256
the index pins. The video admin shows them at `/zh-TW/admin/videos?tab=scripts`.

This is authored text, not production state: the production reviews of the same episodes
live in the database and are shown on the Dramas tab.

Regenerate after changing any AI drama brief, script, storyboard, review or series planning
Markdown:

```sh
node tools/video/drama-admin/bundle.mjs build
node tools/video/drama-admin/bundle.mjs check
```

`npm run test:tools` fails while the committed files differ from `docs/videos`. Deployment
ships them through the API Dockerfile `COPY . .`. Missing, oversized or mismatched files
return `503 video_dramas_unavailable`; an unknown episode or document returns 404.
