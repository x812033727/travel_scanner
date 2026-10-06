// `check-audio`: does every phrase say what the script says? (docs/videos/SHORTS.md §自動品管)
//
// Each phrase's clip goes to the site's transcriber. A transcript that says the phrase already
// (word for word, apart from filler words, or in characters that sound the same) passes without
// a judgement; the rest go to Jev, which answers how likely each transcript says its phrase.
// What Jev doubts is flagged, and `build --redo` synthesizes those phrases again.
//
// The same two endpoints and the same rules as the long videos' check (tools/video/tts/check.mjs),
// over a Short's phrases instead of a script's lines. A service that does not answer fails the
// check: nothing passes because it could not be judged.
//
// Both calls are paid and go through a speech journal in the build directory
// (tts/speech-journal.mjs): one whose answer was lost is not sent again by the next check of that
// build until a person clears its hold, and one that came back before the check was saved is taken
// from the journal instead of being bought again.
import { existsSync, readFileSync } from 'node:fs';
import path from 'node:path';

import { readJson } from '../core/paths.mjs';
import { DEFAULT_THRESHOLD, MAX_HEARD_CHARACTERS, MAX_INTENDED_CHARACTERS, MAX_JUDGE_LINES, hintTerms, matchKind, spokenForm } from '../tts/check.mjs';
import { judgeLines, transcribeClip } from '../tts/client.mjs';
import { JOURNAL_DIR, openSpeechJournal } from '../tts/speech-journal.mjs';
import { downsample, encodeWav, parseWav, requireNarrationFormat } from '../tts/wav.mjs';
import { SCRIPT_FILE, phrasesOf, saveJson, sha256 } from './core.mjs';

export const CHECK_FILE = 'check.json';
// What the transcriber takes; a build's clips are 48 kHz.
const TRANSCRIBE_RATE = 16_000;
const NO_TERMS = { terms: {} };
const number = (i) => String(i).padStart(3, '0');
const lineId = (index) => `p${number(index)}`;
const fit = (text, max) => [...String(text)].slice(0, max).join('');

/** The hash a check is bound to: the clips in order, so a check of other audio never counts. */
export const audioHash = (clips) => sha256(clips.map((clip) => sha256(clip)).join(''));

/** The exact intended words in order; JSON preserves the boundary between phrases. */
export const phrasesHash = (phrases) => sha256(JSON.stringify(phrases));

/** A build's clip as the transcriber takes it. */
export function transcribable(clip) {
  const samples = requireNarrationFormat(parseWav(clip));
  return encodeWav(downsample(samples, Math.round(48_000 / TRANSCRIBE_RATE)), TRANSCRIBE_RATE);
}

/**
 * The check of a build's clips: { ok, audio_sha256, phrases_sha256, lines, checked, flagged, threshold,
 * transcribe_calls, judge_calls, results, flagged_lines }. `transcribe` and `judge` are the
 * site's two calls; tests hand in their own. `prepare` turns a clip into what is sent.
 */
export async function checkPhrases({ phrases, clips, lexicon = null, threshold = DEFAULT_THRESHOLD, transcribe, judge, prepare = transcribable }) {
  if (clips.length !== phrases.length) throw new Error(`${phrases.length} phrases but ${clips.length} clips`);
  const dictionary = lexicon ?? NO_TERMS;
  const results = [];
  const doubtful = [];
  for (const [index, phrase] of phrases.entries()) {
    const line = { id: lineId(index), text: phrase };
    const heard = await transcribe({ wav: prepare(clips[index]), terms: hintTerms(line, { lexicon: dictionary }) });
    const kind = matchKind(heard, line, dictionary);
    const result = { index, text: phrase, heard, verdict: kind ?? 'judge', ok: kind !== null };
    results.push(result);
    if (kind === null) doubtful.push(result);
  }
  for (let start = 0; start < doubtful.length; start += MAX_JUDGE_LINES) {
    const batch = doubtful.slice(start, start + MAX_JUDGE_LINES);
    const nouls = await judge({
      lines: batch.map((result) => ({
        id: lineId(result.index),
        intended: fit(result.text, MAX_INTENDED_CHARACTERS),
        spoken_form: fit(spokenForm({ text: result.text }, dictionary), MAX_INTENDED_CHARACTERS),
        heard: fit(result.heard, MAX_HEARD_CHARACTERS),
      })),
    });
    for (const result of batch) {
      const noul = nouls.get(lineId(result.index));
      result.noul = Number.isFinite(noul) ? noul : null;
      // No answer for a phrase is a doubt, never a pass.
      result.ok = result.noul !== null && result.noul >= threshold;
    }
  }
  const flagged = results.filter((result) => !result.ok);
  return {
    ok: flagged.length === 0,
    audio_sha256: audioHash(clips),
    phrases_sha256: phrasesHash(phrases),
    lines: phrases.length,
    checked: results.length,
    flagged: flagged.length,
    threshold,
    transcribe_calls: results.length,
    judge_calls: Math.ceil(doubtful.length / MAX_JUDGE_LINES),
    results,
    flagged_lines: flagged.map(({ index, text, heard, noul }) => ({ index, text, heard, noul: noul ?? null })),
  };
}

/** The clips of a build directory, in phrase order. */
export function buildClips(directory, count) {
  return Array.from({ length: count }, (_unused, index) => {
    const file = path.join(directory, 'audio', `${number(index)}.wav`);
    if (!existsSync(file)) throw new Error(`no clip for phrase ${index}: build the Short first`);
    return readFileSync(file);
  });
}

/**
 * Check a build directory and write its check.json; returns the check. Its call counts are this
 * run's: an answer the journal kept from an earlier check of the build is not counted again.
 */
export async function checkAudio({ directory, client, lexicon = null, threshold, transcribeImpl = transcribeClip, judgeImpl = judgeLines }) {
  const doc = readJson(path.join(directory, SCRIPT_FILE), null);
  if (!doc) throw new Error(`${directory} holds no ${SCRIPT_FILE}: it is not a build of this tool`);
  const phrases = phrasesOf(doc);
  const calls = { site: client.site, token: client.token, fetchImpl: client.fetch, sleep: client.sleep };
  // Released once check.json is written: until then a restart takes what was bought from here.
  const journal = openSpeechJournal(path.join(directory, JOURNAL_DIR));
  const paid = { transcribe: 0, judge: 0 };
  const counted = (what, send) => async (options) => {
    const reused = journal.reused;
    const answer = await send({ ...calls, ...options });
    if (journal.reused === reused) paid[what] += 1;
    return answer;
  };
  const check = await checkPhrases({
    phrases,
    clips: buildClips(directory, phrases.length),
    lexicon,
    threshold,
    transcribe: counted('transcribe', journal.wrapTranscribe(transcribeImpl)),
    judge: counted('judge', journal.wrapJudge(judgeImpl)),
  });
  const result = { ...check, transcribe_calls: paid.transcribe, judge_calls: paid.judge };
  saveJson(path.join(directory, CHECK_FILE), { ...result, checked_at: new Date().toISOString() });
  journal.release();
  return result;
}
