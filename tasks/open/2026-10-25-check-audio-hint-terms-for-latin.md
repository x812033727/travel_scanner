---
id: 2026-10-25-check-audio-hint-terms-for-latin
title: check-audio: hint terms for Latin-script dubs are word fragments
status: in-progress
priority: P2
area: tools
owner: claude-opus-5-5
claimed_at: 2026-10-25T23:03:52Z
created_at: 2026-10-25T23:03:35Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/tts/check.mjs
  - tools/video/tts/check.test.mjs
  - .agents/skills/youtube-video/references/automated.md
---

# check-audio: hint terms for Latin-script dubs are word fragments

## Why

A dub's audio check sends the transcriber the English words a line says, so it spells product names as the script does. For dubs written in Latin letters with accents (vi, es, pt, id) the list was the whole sentence cut into fragments, so the real names fell off the 20-word cap and the transcriber "corrected" them (GPT-5.6 Sol heard as GPT-3.5, Soho). Together with a hand run that had no second transcriber, seven of eight PHP2Shell dubs were flagged for noise the voice did not make.

## Definition of done

- [x] A vi, es, pt or id line hints only the dictionary's terms it says, whole ("GPT-5.6", "Sol"), never fragments of accented words.
- [x] ja, ko, th and zh-TW hints are unchanged.
- [x] A check that flags lines without a second transcriber says so.

## Steps

- [x] Fix `hintTerms` and test it on real lines.
- [x] Re-check the PHP2Shell dubs with the fix and Whisper (see the PHP2Shell ticket).
- [x] Document the hand-run second transcriber in the youtube-video skill.

## How to verify

The exact commands or clicks that prove it works.

## Notes

Findings, decisions and dead ends, so the next agent does not repeat them.

## Notes (2026-10-25, claude-opus-5-5)

- `hintTerms` matched `[A-Za-z0-9]…` in every dub, so in vi, es, pt and id each accented word broke into fragments ("Dùng" → "D", "ng") and the whole sentence went to the transcriber as "English words"; the 20-word cap filled up before the product names, and Gemini then wrote GPT-5.6 Sol as GPT-3.5 or Soho.
- Fix: `LATIN_SCRIPT_LOCALES` (en, es, pt, id, vi) take whole Unicode words, keep only ASCII ones and only the dictionary's terms, as English already did. ja, ko, th and zh-TW are unchanged.
- `check-audio` also prints a line when lines are flagged and no second transcriber was asked.
- Tests in `tools/video/tts/check.test.mjs`.
- The second transcriber cleared a line only when its transcript matched the script or Jev passed it, though DUBS.md says a line is wrong only when both transcribers hear the same place wrong. With Whisper running, PHP2Shell's ja `pmmz` stayed flagged although Gemini missed one particle and Whisper two other words. `missedInDifferentPlaces` now lines each transcript up with the script (words in Latin-script languages, characters elsewhere, as written, as spoken and in dictionary form) and clears the line when no unit is missed by both; a unit both miss (id "sudah" said as "udah", es "post" heard as "juez" and "PUSTA") keeps it flagged. Tests use those real transcripts.
- Outside Mandarin a transcript now also passes without Jev when it differs only where it spells a loanword in Latin letters that the script writes in its own letters (Thai ล็อกอิน / "login", Japanese パッチ / "Patch"); match kind "spelling". Not in the languages written in Latin letters, where another Latin word is another word, and not for numbers in general: "3" against a number word could be another number.
- Thai number words up to 99, Thai digits and the abbreviation mark ฯ are read by value (`thaiNumbers`), so "ตี 3" lines up with ตีสาม and a wrong number still differs.
- Re-check of the PHP2Shell dubs with all of this (cached transcripts, Whisper medium): en 0, ko 0, ja 0, th 0 flagged (31 Thai lines now match without Jev); what is left both transcribers hear the same way, so it is in the recording: es 1 ("post" slurred), id 3 ("sudah" read as "udah"), vi 1 (closing particle), pt 4 ("patch" read as "pet", "Na sua" run together, the PM's name).
