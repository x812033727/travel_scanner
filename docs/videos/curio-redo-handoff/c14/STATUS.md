# 奇聞檔案局重做 14 支：交接狀態（2026-11-10）

To the next session: report in Traditional Chinese. The full rules are in `../RULES.md`, `../HANDOFF.md`, the owner's handover message (copied into `DECISIONS.md`'s last section), and the `curio-episode` skill.

Episodes: curio-s13/s14/s23/s24/s25/s26/s27/s28/s30/s31/s34/s38/s39/s40-v2.
Do not touch: W03, B02, B03 (another conversation) or B01, H24, S42, W01, W02, S10-v2.

## Working copy

- Run the tools from a checkout of **main**, not from this branch. The branch's tools are older and lint reports `unknown field "nobody"` on scenes 134–136.
- The last session used `git worktree add /home/user/wt-prod origin/main`. Copy into it:
  - `docs/videos/curio-*-v2/` (all 14)
  - `curio-redo-handoff/`
  - this branch's `lexicon.json` terms
- Move each episode's old `i18n/` folder aside (`old-i18n/<slug>/`). It was translated from the pre-redo script and is stale. Retranslate it at the language step.
- Work dirs live in `/root/mokaair-work/videos/<slug>`. Copy `characters/` from the Ada sheet into each one (W03 sheet E, fixed).
- Then run `approve outline` and `approve look` with the owner's fixed notes:
  - outline: "owner 2026-11-07: redo scripts already approved; outline gate recorded without per-video clicks"
  - look: "owner 2026-11-07: Ada sheet is fixed for the series (W03 sheet E); approve without per-video clicks"
- Music library: `/root/mokaair-work/videos/_music` (backup: the `transfer/curio-music-library` branch in `x812033727/mokaair-video-backup`). The container may be fresh, so pull it from there and verify sha256.
  - S13 uses `curio-bed-w02-5846379f.mp3`, sha256 `1e5ed2ec…5717`.
  - S14 uses `curio-bed-w01-5846379f.mp3`, sha256 `5cdf708c…6661`.

## Backup (PR #2059)

- Do not push `transfer/*` branches any more.
- Upload with `todrive.sh <workdir> "videobackup:AI劇/奇聞檔案局/<S13>/製作檔/<slug>"`. Shared files go to `AI劇/奇聞檔案局/_共用/製作檔/`.
- It must print `todrive: N files, 0 differences` before every review-push.
- Before deleting a local work dir, an independent agent runs `todrive.sh --check`.
- The owner added `RCLONE_CONFIG_VIDEOBACKUP_*` environment variables. They load only in a new session. First run `rclone lsd "videobackup:AI劇"` (install rclone with `apt-get install -y rclone`, not curl|bash). Never print the token.

## S13-v2

- Done:
  - Fact check: verify-2.md written by an independent agent. 5 lines changed, and sources added (kotobank 真田幸村, ja.wikipedia 真田信繁).
  - claims.md has a new 2026-11-10 table.
  - lint: 0/0 on main.
  - TTS, plus check-audio with 2 redo rounds and a Whisper medium second opinion (`WHISPER_MODEL=medium node tools/video/cli.mjs check-audio --slug curio-s13-v2 --second-opinion "python3 tools/video/tts/whisper_second_opinion.py"`).
- Lines the owner should listen to when the script+audio gate goes out (both transcribers got them wrong):
  - sv321, sv614: 左衛門佐 (衛 missing in both)
  - sv602, sv619, sv803: 幸村 (heard as 存)
  - sv516, sv521, sv522: 信仍 (heard as -en)
  - sv710: 那封 (heard as 逆風)
- Not done: keyframes. Only one episode draws at a time, and S14 went first.
- If the container is fresh, the work dir is gone. Redo approve outline/look, TTS and check-audio. The audio cache is lost too.

## S14-v2

- Done:
  - verify-2.md written by an independent agent. 6 lines fixed.
  - 6 lines reworded for dictation, without changing facts.
  - check-audio passed. mv317, mv321, mv505 and mv703 were released as proper-noun or homophone transcription errors (speaking rate 86–114%).
  - lint: 0/0 on main.
- Keyframes round 1 (`--takes 3`): about 134 of 140 scenes done when this session ended, US$3.30 spent. **These images exist only in the old container.** If the new session has a fresh container, redraw them (about US$3.5, within the US$15 budget).
- Zoom group A (an independent agent checked 49 judge-passed images in the first 60 scenes; details and suggested prompt fixes are in `zoom-s14-A.json`):
  - 34 ok.
  - 15 need fixing:
    - People drawn as people: gorin-brush, stele-iori, merchant-ask, merchant-old, toyota-names. Show them through objects instead.
    - Wrong era or culture: gorin-copies, stele-raise, stele-blade, stele-maybe, toyota-admit.
    - Wrong era, but take 1 is usable: stele-lightning. Use `stele-lightning-1.jpg` via import at the end.
    - Fake text: numata-book, merchant-again.
    - Ada off-model: numata-name, gorin-silent.
- Failed the judge, so they need the `--seed-offset 3` round: gorin-first, gorin-climb, gorin-young, gorin-remember, gorin-next, stele-nolate, stele-son, merchant-spring, merchant-young, merchant-kin, merchant-uneasy.
- Next steps:
  1. Apply the prompt fixes (positive wording).
  2. Run the seed-offset round.
  3. Zoom-check scenes 61–140 and all redraws with 3 independent agents (`zoom-brief-template.md`).
  4. Run `keyframes import --provider external --usd 0` last.
  5. Upload to Drive.
  6. Send the script+audio gate, then the storyboard gate.

## After that

- Continue S13/S14 through every gate: assemble/QA → final → eight languages → package → publish → languages → owner uploads → final Drive backup plus independent check → delete the work dir.
- Start the next episode only once the current one reaches the publish gate. At most two episodes in flight.
- Remaining 12, in order: s23, s24, s25, s26, s27, s28, s30, s31, s34, s38, s39, s40.

## Files here

- `DECISIONS.md`: the decision log.
- `run-kf.sh`: waits for other keyframe runs, retries on network errors.
- `rate.py`: chars/sec per line.
- `run-s14-tts.sh`, `s14-redo2.json`
- `todrive.sh`
- zoom brief and template
- `zoom-s14-split.json`, `zoom-s14-A.json`
