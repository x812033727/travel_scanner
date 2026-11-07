You are applying an owner-approved change order to an AI live-action drama, 《恁祖媽今年18》, in the repo at /home/user/travel_scanner: **every episode must have at least four shots starting in its first 10 seconds** (lint warning `craft hook.opening`). Episode 1 is already done — study it first: `docs/videos/tai-nainai-e001/script.md` (rows c01, c01b and the section `### 2026-11-06 開場四鏡（站主變更單…）`) and its `shots-en.json` (c01 has `action_seconds: 1`, c01b is new).

Only edit, for your episodes: `docs/videos/tai-nainai-e0NN/script.md`, `shots-en.json`, and the compiled `video.json` / `brief.md`. Do not commit or push; spend no cloud/GPU credits. Keep scratch files in your own subfolder of /tmp/claude-0/-home-user-travel-scanner/d7c8ad43-e108-54da-93b6-f9db4da0f46a/scratchpad/ (shared with other agents — never write at its top level).

## Rules (all must hold)
1. **Dialogue text never changes** — not one character. You may move a line to a new shot (as e001 moved Lin Meifeng's off-screen laugh line from c01 to c01b), but the speaker, the words and their order in the episode stay the same.
2. **No new plot, no new character, no new information.** The added shot is a new angle on what is already in the scene: an insert of a prop or hands already named in the rows, a reaction of someone already present, an establishing view of the same room, or a split of a long first shot into two framings. Prefer short silent inserts.
3. **Continuity**: the episode's first shot continues the previous episode's last shot (bible 〈接點表〉 in `docs/videos/series-plans/top40-2025-2026/2025-01-tai-nainai/production/s1-bible-e001-e060.md`). Keep c01's content as the junction; add after it, or shorten it, never replace it.
4. **New shot ids**: insert `cNNb` right after the shot it follows (e.g. `c01b`, `c02b`); if that id exists, use the next letter. Never renumber existing shots.
5. **Row format**: exactly six columns like the other rows (鏡 | 景別、運鏡 | 畫面裡有誰 | 動作 | 台詞 | 秒數), written in the same Chinese style and detail as the surrounding rows (who is where, costume/look, props, mouths: 「畫面上沒有嘴」 or 「嘴閉著」, lamp level in the ancestral hall, nothing written in frame). Silent shot: 台詞 `—`. Seconds `約 N 秒` (a quick beat may be 1.5–2 秒).
6. Update the scene header's 約 N 秒, the episode total line (秒、鏡數) if the file has one, and add a section at the end of the revision notes, before `## 配音`:
   `### 2026-11-06 開場四鏡（站主變更單，票 \`2026-11-06-tai-nainai-change-ageing-opening\`）` with one bullet per change (what was added/split and why) and the new totals.
7. `shots-en.json`: update `zh_sha256` of every row you changed (from `parse_script.py --json`), add the new shot with full English fields in the same style as the file (camera, prompt ≤950 chars with no Chinese, characters/ref_characters/looks/set/lamp as the scene needs, `motion` for silent shots, `action_seconds` integer for a silent beat under 2 s). Keep the shot order of the script.

## Verify for each episode
```bash
T=docs/videos/series-plans/top40-2025-2026/2025-01-tai-nainai/production/tools
python3 -I docs/videos/series-plans/zhong-tian-qu-qi/production/colab/runs/_scripts/storyboard-check.py docs/videos/tai-nainai-e0NN/script.md   # 0 ERROR
python3 -I $T/compile.py N --check && python3 -I $T/compile.py N
node tools/video/cli.mjs lint --slug tai-nainai-e0NN    # 0 errors, and NO `craft hook.opening:` line (hook.opening30 may stay)
```
The lint timing is an estimate from lines and `action_seconds`; it must show ≥4 shots starting before 10 s. If a shot starts at 10.0x s, shave it with a 1-second beat as e001 did.

Reply when done with, per episode: what you added (shot id + one line), new shot count and seconds, lint errors/warnings, and confirm hook.opening is gone. Keep it short.
