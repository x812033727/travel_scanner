// `check-audio`: every narrated line back to text, and Jev's judgement where it differs.
//
// The site owner asked for Jev, not a person, to decide whether the narration says what the
// script says. Jev reads text only, so the server transcribes each line's clip (Gemini, the site's
// key) and this tool compares the transcript with the script itself. Lines that match once
// punctuation, spacing and case are ignored pass without Jev; the rest go to Jev in one call per
// scene, and every line Jev doubts lands in a flags file that `tts --redo` takes as it is.
// Transcripts are cached by the clip's hash, so a rerun after `tts --redo` only redoes those lines.
//
// Two differences never reach Jev. Jev documents no accuracy for Chinese, and on the pilot it
// doubted 它 heard as 他 and 級聯 heard as 吉蓮. So a transcript that reads the same, tones
// included, passes as "same sound". The owner kept the filler words the conversational voice adds
// (啊, 喔, 欸, 齁, a closing 耶 or 餒…) on 2026-09-25, so a transcript that differs only by those
// passes as "filler".
//
// The transcriber is told which English words each line says. Without that, the ChatGPT video's
// lone "Go" came back as 狗, 各, 購 or 夠 on 2026-09-25, and Jev flagged eleven lines for it.
import { createHash } from "node:crypto";
import { existsSync, readFileSync } from "node:fs";
import path from "node:path";
import { parseArgs } from "node:util";

import { pinyin } from "pinyin-pro";

import { emptyLexicon } from "../core/lexicon.mjs";
import { atomicWrite, lexiconFile, readJson, resolveWorkdir, stopRequested, UsageError } from "../core/paths.mjs";
import { eachLine, spokenText } from "../core/schema.mjs";
import { ARTIFACTS, lintProject, loadProject, recordStage } from "../core/state.mjs";
import { judgeLines, SpeechError, transcribeClip } from "./client.mjs";
import { spokenParts } from "./requests.mjs";
import { downsample, encodeWav, parseWav, requireNarrationFormat } from "./wav.mjs";

// Mirrors JudgeIn's max_length in apps/api/app/video_speech/schemas.py.
export const MAX_JUDGE_LINES = 40;
export const DEFAULT_THRESHOLD = 0.5;
// A line Gemini will not transcribe even after the client's retries is skipped, not fatal: the
// first pilot run stopped at line 40 of 157 on one such line. This many in a row means Gemini
// itself is down, and the run stops instead of spending minutes of retries on every line left.
export const GIVE_UP_AFTER = 3;
const TRANSCRIBE_RATE = 16_000;
const CHECK_FILE = path.join("review", "check.json");
const FLAGS_FILE = path.join("review", "check-flags.json");

/** The text with only its words left: NFKC, lower case, no punctuation, symbols or spaces. */
export function comparable(text) {
  return String(text).normalize("NFKC").toLowerCase().replace(/[\p{P}\p{S}\p{Z}\s]/gu, "");
}

/** How a line was meant to sound: the dictionary's spoken forms in place of its terms. */
export function spokenForm(line, lexicon) {
  return spokenParts(spokenText(line), lexicon)
    .map((part) => part.alias || part.text)
    .join("");
}

// Interjections the voice adds on its own. 耶 and 餒 count only when added at the end of a line
// (好耶, 氣餒 are words); 吧 is left out, since the script uses it as a particle too.
const FILLERS = /[啊喔哦欸誒嗯呃齁]/gu;
const CLOSING_PARTICLES = /[耶餒]+$/u;
// Latin-script words, as the transcriber's hint list takes them: one word each.
const LATIN_WORD = /[A-Za-z0-9][A-Za-z0-9.+#'_-]*/g;
// Mirrors TranscribeIn.terms' max_length in apps/api/app/video_speech/schemas.py.
export const MAX_HINT_TERMS = 20;

/** The English words a line says, spelled as the script spells them, for the transcriber. */
export function hintTerms(line) {
  const words = (spokenText(line).match(LATIN_WORD) ?? [])
    .map((word) => word.replace(/[.'_-]+$/, ""))
    .filter((word) => /[A-Za-z]/.test(word) && word.length <= 40);
  return [...new Set(words)].slice(0, MAX_HINT_TERMS);
}

/** How a text is read aloud, tone by tone: 它 and 他 read the same, 旗 and 期 do not. */
export function reading(text) {
  return pinyin(comparable(text), { toneType: "num", type: "array", nonZh: "consecutive", v: true }).join(" ");
}

/**
 * Whether a transcript already says the line, before any judgement is needed, and how:
 * "exact" word for word, "filler" apart from interjections, "sound" apart from characters that
 * read the same; null when only a judgement can tell.
 */
export function matchKind(heard, line, lexicon) {
  const forms = [line.text, spokenText(line), spokenForm(line, lexicon)];
  const said = comparable(heard);
  if (forms.some((form) => comparable(form) === said)) return "exact";
  const bare = (text) => comparable(text).replace(FILLERS, "");
  // A closing particle comes off what was heard only, so a script ending in 氣餒 still needs it.
  const saidBare = [bare(heard), bare(heard).replace(CLOSING_PARTICLES, "")];
  if (forms.some((form) => saidBare.includes(bare(form)))) return "filler";
  const saidReadings = saidBare.map(reading);
  if (forms.some((form) => saidReadings.includes(reading(bare(form))))) return "sound";
  return null;
}

export function matches(heard, line, lexicon) {
  return matchKind(heard, line, lexicon) !== null;
}

const clipHash = (bytes) => createHash("sha256").update(bytes).digest("hex").slice(0, 16);

export async function checkAudio(args, ctx, options) {
  const { EXIT } = ctx;
  const values = parseArgs({
    args,
    options: { slug: { type: "string" }, file: { type: "string" }, workdir: { type: "string" }, threshold: { type: "string" }, force: { type: "boolean" } },
    strict: true,
  }).values;
  if (!values.slug && !values.file) throw new UsageError("check-audio needs --slug (or --file for an example outside docs/videos)");
  const threshold = values.threshold === undefined ? DEFAULT_THRESHOLD : Number(values.threshold);
  if (!(threshold > 0 && threshold < 1)) throw new UsageError("--threshold must be between 0 and 1");
  const project = loadProject({ slug: values.slug, file: values.file, root: ctx.root });
  if (lintProject(project).errors.length) {
    ctx.stdout.write(`${project.doc.slug} has lint errors; run lint first\n`);
    return EXIT.lint;
  }
  const { doc } = project;
  const lexicon = project.lexicon ?? readJson(lexiconFile(ctx.root), emptyLexicon());
  const workdir = resolveWorkdir({ flag: values.workdir, env: ctx.env, slug: doc.slug, root: ctx.root, home: ctx.home });
  const timeline = readJson(path.join(workdir, ARTIFACTS.timeline), null);
  if (!timeline) throw new UsageError(`no narration yet: run tts --slug ${doc.slug} first`);
  const audioDir = path.join(workdir, ARTIFACTS.audio);
  const cacheFile = path.join(workdir, CHECK_FILE);
  const cache = readJson(cacheFile, { lines: {} });
  const results = {};

  let transcribed = 0;
  let failedInARow = 0;
  let gaveUp = false;
  const unchecked = new Map();
  for (const { scene, line } of eachLine(doc)) {
    if (stopRequested(workdir)) {
      ctx.stdout.write("STOP found; transcripts so far are saved\n");
      return EXIT.ok;
    }
    const file = path.join(audioDir, `${line.id}.wav`);
    if (!existsSync(file)) throw new UsageError(`no clip for line ${line.id}: run tts --slug ${doc.slug}`);
    const bytes = readFileSync(file);
    const clip = clipHash(bytes);
    const cached = cache.lines[line.id];
    const terms = hintTerms(line);
    // A transcript made with other hints (or none, before hints existed) is made again.
    const sameHints = (cached?.terms ?? []).join(" ") === terms.join(" ");
    let entry = !values.force && cached?.clip === clip && sameHints && typeof cached.heard === "string" ? cached : null;
    if (!entry) {
      const samples = requireNarrationFormat(parseWav(bytes));
      const wav = encodeWav(downsample(samples, Math.round(48_000 / TRANSCRIBE_RATE)), TRANSCRIBE_RATE);
      let heard;
      try {
        heard = await transcribeClip({ ...options, wav, terms });
      } catch (error) {
        // The owner's problems (token, key) stop the run; so does anything that is not the service.
        if (!(error instanceof SpeechError) || error.who !== "service") throw error;
        unchecked.set(line.id, error.message);
        failedInARow += 1;
        if (failedInARow >= GIVE_UP_AFTER) {
          gaveUp = true;
          break;
        }
        continue;
      }
      failedInARow = 0;
      transcribed += 1;
      entry = { scene: scene.id, clip, terms, heard, noul: null };
    }
    entry.intended = spokenText(line);
    entry.spoken_form = spokenForm(line, lexicon);
    entry.match_kind = matchKind(entry.heard, line, lexicon);
    entry.match = entry.match_kind !== null;
    results[line.id] = entry;
    cache.lines[line.id] = entry;
    atomicWrite(cacheFile, `${JSON.stringify(cache, null, 2)}\n`);
  }

  // Jev looks only at lines whose transcript differs and has not been judged for this clip.
  const toJudge = Object.entries(results).filter(([, entry]) => !entry.match && typeof entry.noul !== "number");
  const byScene = new Map();
  for (const [id, entry] of toJudge) {
    if (!byScene.has(entry.scene)) byScene.set(entry.scene, []);
    byScene.get(entry.scene).push({ id, intended: entry.intended, spoken_form: entry.spoken_form, heard: entry.heard });
  }
  let jevCalls = 0;
  for (const lines of byScene.values()) {
    for (let start = 0; start < lines.length; start += MAX_JUDGE_LINES) {
      const batch = lines.slice(start, start + MAX_JUDGE_LINES);
      const verdicts = await judgeLines({ ...options, lines: batch });
      jevCalls += 1;
      for (const { id } of batch) results[id].noul = verdicts.get(id) ?? 0;
      atomicWrite(cacheFile, `${JSON.stringify(cache, null, 2)}\n`);
    }
  }

  const entries = Object.entries(results);
  const exact = entries.filter(([, entry]) => entry.match_kind === "exact").length;
  const alike = entries.filter(([, entry]) => entry.match && entry.match_kind !== "exact").length;
  const flagged = entries.filter(([, entry]) => !entry.match && entry.noul < threshold);
  const judgedFine = entries.length - exact - alike - flagged.length;
  const flagsFile = path.join(workdir, FLAGS_FILE);
  const notes = Object.fromEntries(flagged.map(([id, entry]) => [id, `Jev ${entry.noul.toFixed(2)}: heard 「${entry.heard}」`]));
  atomicWrite(flagsFile, `${JSON.stringify({ slug: doc.slug, speech_hash: timeline.speech_hash, flags: flagged.map(([id]) => id), notes }, null, 2)}\n`);
  const total = [...eachLine(doc)].length;
  const missing = total - entries.length;
  recordStage(
    workdir,
    "check-audio",
    { lines: total, exact, alike, judged: judgedFine + flagged.length, flagged: flagged.length, unchecked: missing, transcribed, jev_calls: jevCalls },
    ctx.now(),
  );

  ctx.stdout.write(
    `${entries.length} of ${total} lines checked: ${exact} match the script word for word, ${alike} differ only by same-sound characters or filler words, ${judgedFine} judged fine by Jev, ${flagged.length} flagged (below ${threshold})\n`,
  );
  ctx.stdout.write(`${transcribed} clips transcribed now, ${jevCalls} Jev calls; details in ${cacheFile}\n`);
  for (const [id, entry] of flagged) {
    ctx.stdout.write(`  ${id}  Jev ${entry.noul.toFixed(2)}\n    script: ${entry.intended}\n    heard:  ${entry.heard}\n`);
  }
  if (flagged.length) {
    ctx.stdout.write(`next: fix the dictionary or the line, then node tools/video/cli.mjs tts --slug ${doc.slug} --redo ${flagsFile}\n`);
  }
  if (missing) {
    const why = gaveUp ? `Gemini failed ${GIVE_UP_AFTER} lines in a row, so the run stopped` : "Gemini would not transcribe them";
    ctx.stdout.write(`${missing} lines not checked yet (${why}); run check-audio again later, finished lines are kept\n`);
    for (const [id, message] of unchecked) ctx.stdout.write(`  ${id}  ${message}\n`);
    return EXIT.external;
  }
  return flagged.length ? EXIT.lint : EXIT.ok;
}
