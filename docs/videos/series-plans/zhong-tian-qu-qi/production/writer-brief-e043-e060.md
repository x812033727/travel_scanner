You are writing episodes of the AI drama 種田娶妻打天下 (slug zhong-tian-qu-qi), script and storyboard only — NO generation (no Colab, no Gemini TTS, no paid calls). Repo /home/user/travel_scanner, branch claude/intelligent-gates-9n92xm. Do NOT commit, push, or switch branches; the main session commits. Other writers are writing other episodes at the same time.

Owner's request (2026-10-31): write season 1 through to its end (e060), in the same format as e033–e042, leaving season-2 foreshadowing; the owner reviews before any clip is made.

READ FIRST
- docs/videos/series-plans/zhong-tian-qu-qi/season-01.json — your episodes' entries are the spec (hook, mid_hook, conflict, turn, satisfaction, cliffhanger, spectacle, glamour_shot, setups/payoffs/reveals, general_payoffs, characters, locations, state, duration_s). Also the episode before your first one and after your last one, for continuity. season-01.json `threads`, setting.json `mysteries` (only reveal what the outline says to reveal in your episode; never reveal a later-season mystery).
- docs/videos/series-plans/zhong-tian-qu-qi/authoring.md, production/storyboard-rules.md, production/README.md.
- docs/videos/series-plans/zhong-tian-qu-qi/production/s01-e043-e060-registry.md — the cast ids, set ids, which English phrase picks each set in gen-dh.mjs (first match from the top wins), and which pictures exist.
- Exemplars: docs/videos/zhong-tian-qu-qi-e040, e041, e042 (brief.md, script.md, storyboard.md, video.json, overlays.json) and tasks/open/2026-10-31-zhong-tian-e041-e042-brief-script.md (verification commands, notes on what was learned). Match their length per second, line density, shot count per minute, prompt style and file structure exactly. git log -p on e041/e042 shows how they were built.
- Skills: .agents/skills/youtube-video/references/drama-craft.md, .agents/skills/animation-camera/SKILL.md, .agents/skills/minimax-h3-colab/references/motion-quality.md and lessons.md (e.g. lessons on scene-picture contamination, close-ups, inserts that open on the plate — write prompts that avoid known failures).

FOR EACH EPISODE (in order)
1. docs/videos/zhong-tian-qu-qi-e0NN/: brief.md, script.md, storyboard.md, video.json, overlays.json, in the e041/e042 format, Traditional Chinese dialogue, Taiwanese Mandarin phrasing. No dub.*.json (those come after the cut).
2. Generate production/hailuo/ff-dh-e0NN.json and clips-dh-e0NN.json with gen-dh.mjs exactly the way e041/e042 were (find the lock file and argument order from git history / production/hailuo/README.md).
3. Pass: node tools/video/cli.mjs lint --slug zhong-tian-qu-qi-e0NN (0 errors); node .agents/skills/youtube-video/scripts/drama_craft_check.mjs docs/videos/zhong-tian-qu-qi-e0NN/video.json (all pass); node .agents/skills/animation-camera/scripts/shot_reading.mjs docs/videos/zhong-tian-qu-qi-e0NN/video.json (0 traps). Then node docs/videos/series-plans/zhong-tian-qu-qi/production/colab/ref2manifest.mjs for the episode in a scratch output dir if that is how e041 was checked, to confirm every shot resolves its pictures (missing pictures that the registry marks 🎨 are expected; list them).
4. Continuity: your first episode picks up the previous episode's cliffhanger question in its first 10 seconds (per README rules). If the previous episode's files exist when you start, read them; otherwise use season-01.json state.

RULES
- Edit ONLY files of your own episodes: docs/videos/zhong-tian-qu-qi-e0NN/* and production/hailuo/ff-dh-e0NN.json, clips-dh-e0NN.json. Do NOT edit cast.json, gen-dh.mjs, ref2manifest.mjs, dub-glossary.json, the registry, or any other shared file — if you need a character/set/glossary term that is missing, work around it if possible and list it in your report.
- Series rules: 不黃標 (no sexual content, no banned title words), 顏值 rules, Tang Xiaotang's high closed collar, no text drawn in pictures, minors safe. Every male line must have a registered speaker id with a voice.
- YouTube title per season-01 youtube_title (check banned words).

REPORT: per episode — shot count, seconds, line count, check results, pictures still missing, anything you needed but could not register, choices you made where the outline was ambiguous, and every file you wrote.
