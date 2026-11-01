---
id: 2026-10-09-dub-skipped-because-jev-still-hears
title: Dub skipped because Jev still hears lines wrong is the top skip reason
status: in-progress
priority: P1
area: tools
owner: claude-opus-5.5
claimed_at: 2026-11-01T04:05:16Z
created_at: 2026-10-09T14:49:20Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/tts/check.mjs
  - tools/video/tts/check.test.mjs
  - tools/video/tts/client.mjs
  - tools/video/tts/speech-journal.mjs
  - tools/video/tts/check-journal.test.mjs
  - apps/api/app/video_speech/checking.py
  - apps/api/app/video_speech/schemas.py
  - apps/api/app/video_speech/admin_api.py
  - apps/api/tests/test_video_speech_check.py
  - docs/videos/DUBS.md
---

# Dub skipped because Jev still hears lines wrong is the top skip reason

## Why

The owner ticks English, Japanese and Korean dubs on every video, and on 2026-10-09 the
latest `languages` batch of each of the forty videos on production showed, per locale:

| locale | dub ready | dub skipped |
| --- | --- | --- |
| en | 10 | 14 |
| ja | 5 | 19 |
| ko | 6 | 16 |

Of the 49 skips, 31 carry the reason `Jev still hears lines wrong after 2 retakes and N
rewording rounds` (en 9, ja 12, ko 10): `gpt-6-sol-luna-where-to-use` and
`openai-cursor-wind-down-nov-12` lost all three locales to it, `sec-ai-trading-bot-whatsapp-scam`,
`mcdonalds-ai-pricing-engine-who-said-what` and `cloudflare-workers-per-worker-permissions-ai-agent`
two each. The worker gives up after `MAX_DUB_RETAKE_ROUNDS` retakes and
`MAX_DUB_REWORD_ROUNDS` rewordings (`flow.mjs`, the `Jev still hears lines wrong` branch)
and leaves `review/check-flags.<locale>.json` behind for a hand-run `dub --redo`, which
nobody runs. A dub that reaches the owner is the exception, not the rule.

DUBS.md §聲音會唸錯的地方 already records that most of Gemini's flags on its own are it
"correcting" version numbers and brands it does not know, and that `check-audio
--second-opinion` (local Whisper) clears those. Whether the production worker runs with a
second opinion, and what the 31 flags actually are, has not been measured.

## Definition of done

- [ ] The flags behind at least ten of the 31 skips are classified (real misreading,
      transcriber "correction" of a name or number, number or unit read wrong per
      DUBS.md's list) and the counts are in the Notes.
- [ ] The dominant class has a fix in the pipeline, not a hand-run instruction: a second
      opinion on by default on the host if it is off, dictionary entries fed back from the
      flags, or a bounded extra round, whichever the measurement supports.
- [ ] The skip rate on the next ten videos' first `languages` batch is reported against
      this baseline (31 of 49 skips, 20 of 70 ticked dubs ready).

## Steps

- [ ] On the host, read `review/check-flags.<locale>.json` under
      `/var/lib/mokaair/video-work/<slug>/` for the five videos above and classify each flag.
- [ ] Check whether `VIDEO_SECOND_OPINION` (or the `--second-opinion` argument) is set for
      the production video worker; if not, cost it and propose turning it on.
- [ ] Pick the fix from the measurement; add the regression to `automation.test.mjs`.
- [ ] Record the before/after counts here and in DUBS.md.

## How to verify

`npm run test:tools`; then one video through the automated route on the host with all
three dubs ticked, and its `languages` card showing dubs ready rather than skipped.

## Notes

- 2026-10-09 (claude-fable-5.1): the production worker had no second opinion at all. The
  video-worker container has no `VIDEO_SECOND_OPINION` in its environment and no
  `faster_whisper` module (`docker compose exec video-worker python3 -c "import faster_whisper"`
  → ModuleNotFoundError), so every Jev doubt counted as a misheard line. DUBS.md's rule
  ("two transcribers must hear the same error") was documented but never deployed.
- The flags themselves (`review/check-flags.<locale>.json`, read for the five videos above
  on the docker volume `travel_scanner_video_work`): 2–7 lines per locale, Jev scores mostly
  0.03–0.17, i.e. near the threshold. A mix: some are the transcriber's own slips
  (ja「測るのは野菜と財布の紐の硬さです」, ko「남은 뇌물은…」, ko「Mokaair 기사가 다시 정리했어?」),
  some read like the line as written (en「The second number is four. Four access rules decide
  how far it can go.」). Exactly the split a second transcriber settles.
- Fix taken (branch `claude/dub-skip-rate`): `ops/video/Dockerfile` installs faster-whisper
  1.2.1 in `/opt/whisper` (smoke target checks it); `docker-compose.prod.yml` sets
  `VIDEO_SECOND_OPINION`, `WHISPER_MODEL=medium`, `HF_HOME` on the video_home volume. The
  model (about 1.5 GB) downloads on first use, so the first check after the deploy is slower
  and needs egress to huggingface.co from the worker; the default time limit (10 min plus 2
  a clip) covers it. Dictionary feedback and extra rounds were not added: measure the skip
  rate with the second opinion first.
- Baseline to compare against after the deploy: 31 of 49 skips, 20 of 70 ticked dubs ready.
- Sibling tickets from the same count: `2026-10-09-dub-skipped-because-lines-do-not`
  (14 skips, windows that do not fit at 1.15x) and `2026-10-09-dub-given-up-as-the-retake`
  (4 skips, a retake that overran its window).
- The ready tracks were never uploaded either; see
  `2026-10-09-languages-card-says-the-site-cannot`.
- 2026-10-10: merged as #1416 and live. Checked in the video-worker container:
  `VIDEO_SECOND_OPINION` set, `WHISPER_MODEL=medium`, faster-whisper 1.2.1 imports, `HF_HOME`
  on the volume is writable and huggingface.co answers 200. The model has not been fetched
  yet: the first dub check after this downloads about 1.5 GB. Still open for the measurement:
  compare the next ten videos' first languages batch with the baseline above.

## Evidence 2026-11-01 (daily-ai-20261029, second opinion is set on the host)

Three of four skipped locales were flagged on a faithful or near-faithful reading:
- es utxn (Jev 0.22): script "editar PDF", voice said "editar PDFs" (plural only).
- pt mby2 (Jev 0.16): script "US$ 250 mil", voice said "250 mil dólares" — the correct way to read the symbol.
- pt 9ept (Jev 0.16): "ninguém diz" read "ninguém disse" (tense), plus ":" → "." pause.
- ko bgnr (Jev 0.06) is a real loss: "Claude Enterprise 4개도 같습니다" read "Claude Enterprise도 마찬가지입니다" — the
  translated line itself is unnatural Korean, so the voice smoothed it and dropped the number; rewording did not fix it.
Classes to add: currency-symbol verbalisation counts as a match; a plural/tense-only diff is a warning, not a skip.

## Measurement and fix (2026-11-01, claude-opus-5.5)

Baseline: the latest languages batch of every video, 2026-09-29..10-31: 23 dubs given up for
"Jev still hears", 119 flagged lines (5 more locales had no flags file left). Classified by hand:
~55 transcriber homophones the voice did not make, ~45 faithful-but-not-verbatim readings
(articles, colloquial forms, US$ → dólares, EE. UU. → Estados Unidos, plural), ~12 real
misreadings (625→620, B4 dropped, 4개 dropped, 2026→2024, Opus 5→Opus, Gemini 4→for).

Second opinion: of the 119, only the 4 from daily-ai-20261029 had one. The 10-19..10-24 story
videos (18 dubs) wrote hints files but got no transcript: PyAV 19 broke the script until #1862
(10-26). check-audio printed "the flags below stand" and the worker spent retakes and rewordings
and gave the dub up. Fix: a doubted line no second transcriber has heard ends check-audio with
exit 4 when the transcriber fails (worker defers), tests in check.test.mjs.

Jev: dubs were judged word for word like the narration. Fix: `track: "dub"` on speech/judge,
DUB_JUDGE_INSTRUCTIONS / DUB_JUDGE_CRITERIA in checking.py (meaning-preserving forms pass; a
number, date, unit, name, product or content word lost or changed does not). Re-asked Jev the 119
lines with the dub criteria on the host (8 calls, counted against the daily budget): 42 now pass,
all of the faithful-reading class; every real misreading above still fails (0.03-0.23).

- [x] Flags of more than ten skips classified (above).
- [x] Second opinion checked on the host: set, and it works now; its failures no longer count as misreadings.
- [x] Fix for both dominant classes, with tests (check.test.mjs, check-journal.test.mjs, test_video_speech_check.py).
- [ ] Skip rate on the next ten videos' first languages batch against 23 skips / 119 flags above.

