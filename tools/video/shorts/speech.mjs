// Where a Short's narration comes from, phrase by phrase (docs/videos/SHORTS.md §工具端).
//
//   server   the site synthesizes it in the channel's voice (POST /api/video/speech); what the
//            host worker uses, and any computer with a video tool token
//   windows  the installed Windows voice, as the three pilots were made; costs nothing
//   files    WAVs someone supplies, one per phrase: 000.wav, 001.wav, ...
//
// Every source ends as one 48 kHz mono WAV per phrase. A server phrase is cached under the voice
// and its own words, so editing one phrase, or sending back the ones the listener flagged,
// synthesizes those alone. Each server request goes through the speech journal beside that
// cache (tts/speech-journal.mjs): a phrase whose answer was lost is not sent again by the next
// build or lab round until a person clears its hold, and one that came back but was not cached
// yet is taken from the journal instead of being bought again. When the server can say when each
// character is spoken (POST /video/speech/align: an Azure voice's word boundaries come with the
// one synthesis call, any other clip is timed afterwards by the server's aligner when it has
// one), that timing is cached beside the WAV and the karaoke captions follow it (karaoke.mjs);
// otherwise they are estimated.
import { execFile } from 'node:child_process';
import { existsSync, mkdirSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { promisify } from 'node:util';

import { atomicWrite, readJson } from '../core/paths.mjs';
import { alignClip, synthesize, synthesizeAligned } from '../tts/client.mjs';
import { spokenParts, voiceFields } from '../tts/requests.mjs';
import { JOURNAL_DIR, openSpeechJournal } from '../tts/speech-journal.mjs';
import { phrasesOf, sha256 } from './core.mjs';

const exec = promisify(execFile);
const HERE = path.dirname(fileURLToPath(import.meta.url));
export const SOURCES = Object.freeze(['server', 'windows', 'files']);
export const WINDOWS_VOICE = 'Microsoft Hanhan Desktop';
const number = (i) => String(i).padStart(3, '0');

/** The source a build uses when none is named: the machine's own voice only on Windows. */
export const defaultSource = (platform = process.platform) => (platform === 'win32' ? 'windows' : 'server');

/** The request the narration server takes for one phrase in one voice. */
export function phraseBody(voice, phrase, lexicon = null) {
  return { ...voiceFields(voice), segments: [{ parts: spokenParts(phrase, lexicon ?? { terms: {} }), break_after_ms: 0 }] };
}

/** What a server phrase is cached under: the voice as sent and the words as spoken. */
export const phraseKey = (voice, phrase, lexicon = null) => sha256(JSON.stringify(phraseBody(voice, phrase, lexicon))).slice(0, 24);

/** Where a server phrase's measured timing is cached: beside its WAV, under the same key. */
export const timingFileOf = (cacheDir, voice, phrase, lexicon = null) => path.join(cacheDir, `${phraseKey(voice, phrase, lexicon)}.timing.json`);

/**
 * The phrases from the narration server, each with its measured timing when the server gave one
 * (`timings`, null where it could not). `redo` lists the phrase numbers to synthesize again
 * whatever the cache holds; the usage counts only what this call was charged for, so an answer
 * an earlier build paid for and the journal kept is not counted again. An Azure voice gets its
 * timing in the one synthesis call; with `align`, any other clip, a clip synthesized before the
 * route existed, and an answer the journal kept from an earlier run, is sent for alignment
 * afterwards, which costs nothing and is asked again next build until the server can answer it.
 * A build that draws no karaoke passes `align: false` and takes only the timing the cache
 * already holds.
 */
export async function serverNarration({ phrases, voice, cacheDir, client, lexicon = null, redo = [], align = true, synthesizeImpl = synthesize, synthesizeAlignedImpl = synthesizeAligned, alignImpl = alignClip }) {
  mkdirSync(cacheDir, { recursive: true });
  const options = { site: client.site, token: client.token, fetchImpl: client.fetch, sleep: client.sleep };
  const journal = openSpeechJournal(path.join(cacheDir, JOURNAL_DIR));
  // One journal entry per phrase body, whichever route it goes out on: an Azure voice asks
  // speech/align first (the WAV and its timing in the one paid call); a site that cannot time it
  // answers null without charging, and the phrase goes to speech as before. A lost answer on
  // either route holds the phrase.
  const send = journal.wrap(async (body) => {
    const aligned = voice.provider === 'gemini' ? null : await synthesizeAlignedImpl({ body, ...options });
    return aligned ?? synthesizeImpl({ body, ...options });
  });
  const again = new Set(redo);
  const clips = [];
  const timings = [];
  let calls = 0;
  let characters = 0;
  for (const [index, phrase] of phrases.entries()) {
    const file = path.join(cacheDir, `${phraseKey(voice, phrase, lexicon)}.wav`);
    const timingFile = timingFileOf(cacheDir, voice, phrase, lexicon);
    if (again.has(index) || !existsSync(file)) {
      const { wav, billable, reused, timing } = await send(phraseBody(voice, phrase, lexicon));
      // Whole or not at all: a cached phrase is never asked for again. The take's timing goes
      // with it: an older take's is dropped, and an answer the journal kept comes without one.
      atomicWrite(file, wav);
      rmSync(timingFile, { force: true });
      if (timing) atomicWrite(timingFile, `${JSON.stringify(timing)}\n`);
      journal.release();
      if (!reused) {
        calls += 1;
        characters += billable || [...phrase].length;
      }
    }
    const wav = readFileSync(file);
    let timing = readJson(timingFile, null);
    if (!timing && align) {
      timing = await alignImpl({ wav, text: phrase, ...options });
      if (timing) atomicWrite(timingFile, `${JSON.stringify(timing)}\n`);
    }
    clips.push(wav);
    timings.push(timing);
  }
  return { clips, timings, provider: voice.provider, model: voice.model ?? null, voice: voice.name, calls, characters };
}

async function windowsNarration({ phrases, voice, cacheRoot }) {
  if (process.platform !== 'win32') throw new Error('the Windows narrator runs on Windows only: use --speech server, or --speech files with --audio-dir');
  const script = readFileSync(path.join(HERE, 'speech.ps1'), 'utf8');
  const cache = path.join(cacheRoot, sha256(JSON.stringify({ phrases, voice, rate: 1, speechScript: script })).slice(0, 16));
  mkdirSync(cache, { recursive: true });
  if (!existsSync(path.join(cache, 'complete.json'))) {
    writeFileSync(path.join(cache, 'phrases.json'), JSON.stringify(phrases));
    await exec('powershell.exe', ['-NoProfile', '-NonInteractive', '-ExecutionPolicy', 'Bypass', '-File', path.join(HERE, 'speech.ps1'), '-InputJson', path.join(cache, 'phrases.json'), '-OutputDirectory', cache, '-Voice', voice], { windowsHide: true, maxBuffer: 1024 * 1024 });
    writeFileSync(path.join(cache, 'complete.json'), `${JSON.stringify({ voice, rate: 1, phrases: phrases.length, provider: 'Windows installed speech', incremental_api_cost_ntd: 0 }, null, 2)}\n`);
  }
  return { clips: phrases.map((_phrase, index) => readFileSync(path.join(cache, `${number(index)}.wav`))), provider: 'windows', model: null, voice, calls: 0, characters: 0 };
}

function filesNarration({ phrases, audioDir }) {
  if (!audioDir) throw new Error('--speech files needs --audio-dir with one WAV per phrase: 000.wav, 001.wav, ...');
  return { clips: phrases.map((_phrase, index) => readFileSync(path.join(audioDir, `${number(index)}.wav`))), provider: 'files', model: null, voice: 'external', calls: 0, characters: 0 };
}

/**
 * The narration of a script from one source: { clips, provider, model, voice, calls, characters },
 * and from the server also `timings` (karaoke.mjs; `align` asks the server to time the clips it
 * has not timed yet). `workBase` is where the caches live, beside the builds and outside the
 * repository.
 */
export async function narrate({ doc, source, workBase, voice, client = null, audioDir = null, windowsVoice = WINDOWS_VOICE, lexicon = null, redo = [], align = true, synthesizeImpl, synthesizeAlignedImpl, alignImpl }) {
  const phrases = phrasesOf(doc);
  if (source === 'files') return filesNarration({ phrases, audioDir });
  if (source === 'windows') return windowsNarration({ phrases, voice: windowsVoice, cacheRoot: path.join(workBase, doc.slug, '.speech') });
  if (source !== 'server') throw new Error(`--speech must be one of ${SOURCES.join(', ')}`);
  if (!client) throw new Error('--speech server needs the site: run `node tools/video/cli.mjs login` first');
  return serverNarration({ phrases, voice, cacheDir: path.join(workBase, '.speech-server'), client, lexicon, redo, align, synthesizeImpl, synthesizeAlignedImpl, alignImpl });
}

/** The phrase numbers a finished check flagged, from its check.json; none when there is no file. */
export function flaggedPhrases(checkFile) {
  const check = readJson(checkFile, null);
  return Array.isArray(check?.flagged_lines) ? check.flagged_lines.map((line) => Number(line.index)).filter(Number.isInteger) : [];
}
