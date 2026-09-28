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
//
// A dubbed track (docs/videos/DUBS.md) takes the same check with `--locale`: its clips and
// timeline come from dubs/<locale>/, its script is the translation the dub reads, the server
// transcribes in that language, and its transcript cache and flags file are its own, so
// `dub --redo` takes the flags as they are. The same-sound and filler rules are Mandarin's and
// apply to zh-TW and zh-CN only; in English, Japanese and Korean, whatever differs beyond case,
// width, spacing and punctuation goes to Jev.
import { createHash } from "node:crypto";
import { existsSync, readFileSync } from "node:fs";
import path from "node:path";
import { parseArgs } from "node:util";

import { pinyin } from "pinyin-pro";

import { emptyLexicon, isKnownTerm } from "../core/lexicon.mjs";
import { atomicWrite, lexiconFile, readJson, resolveWorkdir, stopRequested, UsageError } from "../core/paths.mjs";
import { eachLine, LOCALES, NARRATION_LOCALE, narrationLocale, spokenText } from "../core/schema.mjs";
import { ARTIFACTS, lintProject, loadProject, recordStage } from "../core/state.mjs";
import { judgeLines, SpeechError, transcribeClip } from "./client.mjs";
import { spokenParts } from "./requests.mjs";
import { downsample, encodeWav, parseWav, requireNarrationFormat } from "./wav.mjs";

// Mirrors JudgeIn's max_length in apps/api/app/video_speech/schemas.py.
export const MAX_JUDGE_LINES = 40;
// Mirrors JudgeLineIn's max_length for intended and spoken_form, and for heard, in the same file.
// A longer line is cut to fit and noted, rather than failing its whole batch on a 422.
export const MAX_INTENDED_CHARACTERS = 400;
export const MAX_HEARD_CHARACTERS = 800;
export const DEFAULT_THRESHOLD = 0.5;
// A line Gemini will not transcribe even after the client's retries is skipped, not fatal: the
// first pilot run stopped at line 40 of 157 on one such line. This many in a row means Gemini
// itself is down, and the run stops instead of spending minutes of retries on every line left.
export const GIVE_UP_AFTER = 3;
const TRANSCRIBE_RATE = 16_000;
// The languages a dub can be in: every caption locale but the narration's (docs/videos/DUBS.md).
export const DUB_LOCALES = LOCALES.filter((locale) => locale !== NARRATION_LOCALE);
const CHINESE = new Set([NARRATION_LOCALE, "zh-CN"]);

/** A `--locale` value: a caption locale other than the narration's, or a usage error naming them. */
export function parseDubLocale(value, narration = NARRATION_LOCALE) {
  const dubs = LOCALES.filter((locale) => locale !== narration);
  if (!dubs.includes(value)) {
    throw new UsageError(`--locale must be one of ${dubs.join(", ")}: a dubbed track; the narration is checked without --locale`);
  }
  return value;
}

/**
 * Where a track's clips and timeline are, relative to the work directory: the narration's
 * artifacts, or the dubs/<locale>/ layout that `dub` writes (docs/videos/DUBS.md).
 */
export function trackFiles(locale = NARRATION_LOCALE, narration = NARRATION_LOCALE) {
  if (locale === narration) return { audio: ARTIFACTS.audio, timeline: ARTIFACTS.timeline };
  return { audio: path.join("dubs", locale, "audio"), timeline: path.join("dubs", locale, "timeline.json") };
}

/** A track's transcript cache and flags file, relative to the work directory: one pair per locale. */
export function checkFiles(locale = NARRATION_LOCALE, narration = NARRATION_LOCALE) {
  const suffix = locale === narration ? "" : `.${locale}`;
  return { cache: path.join("review", `check${suffix}.json`), flags: path.join("review", `check-flags${suffix}.json`) };
}

/**
 * The text with only its words left: NFKC, lower case, no punctuation, symbols or spaces. That
 * is what every locale's transcript is compared on: case and punctuation in English, full-width
 * forms and spacing in Japanese and Korean, punctuation in Chinese.
 */
export function comparable(text) {
  return String(text).normalize("NFKC").toLowerCase().replace(/[\p{P}\p{S}\p{Z}\s]/gu, "");
}

/** How a line was meant to sound: the dictionary's spoken forms in place of its terms. */
export function spokenForm(line, lexicon) {
  return spokenParts(spokenText(line), lexicon)
    .map((part) => part.alias || part.text)
    .join("");
}

// Han, kana and Hangul.
const CJK = /[぀-ヿ㐀-䶿一-鿿豈-﫿ｦ-ﾟ가-힯]/u;

/**
 * The dictionary as a dub reads it. Mirrors the rule in tools/video/dubs/: an alias applies only
 * when it has no CJK characters ("API" is "A P I" in English or Japanese too), and a term whose
 * alias is a Mandarin reading ("p95" as "P 九十五") is spoken as written instead.
 */
export function dubLexicon(lexicon) {
  const terms = {};
  for (const [term, say] of Object.entries(lexicon?.terms ?? {})) terms[term] = typeof say === "string" && CJK.test(say) ? null : say;
  return { ...(lexicon ?? emptyLexicon()), terms };
}

/** The dictionary a track's spoken forms come from: the narration's as it is, a dub's filtered. */
export function lexiconFor(lexicon, locale = NARRATION_LOCALE, narration = NARRATION_LOCALE) {
  return locale === narration ? lexicon : dubLexicon(lexicon);
}

// Interjections the voice adds on its own, in Traditional and Simplified characters. 耶 and 餒
// count only when added at the end of a line (好耶, 氣餒 are words); 吧 is left out, since the
// script uses it as a particle too.
const FILLERS = /[啊喔哦欸誒诶嗯呃齁]/gu;
const CLOSING_PARTICLES = /[耶餒馁]+$/u;
// Latin-script words, as the transcriber's hint list takes them: one word each.
const LATIN_WORD = /[A-Za-z0-9][A-Za-z0-9.+#'_-]*/g;
// Mirrors TranscribeIn.terms' max_length in apps/api/app/video_speech/schemas.py.
export const MAX_HINT_TERMS = 20;

// A word the dictionary lists, or a joined term ("GPT-5.5") built on one. A single letter, which
// the dictionary always accepts, is an ordinary English word here.
function dictionaryTerm(word, lexicon) {
  const terms = lexicon?.terms ?? {};
  if (Object.hasOwn(terms, word)) return true;
  return isKnownTerm(word, lexicon) && word.split(/[-.+#']+/).some((part) => Object.hasOwn(terms, part));
}

/**
 * The English words a line says, spelled as the script spells them, for the transcriber. In an
 * English dub every word is Latin, so only the dictionary's terms (the acronyms and product
 * names a transcriber spells its own way) are hinted there.
 */
export function hintTerms(line, { locale = NARRATION_LOCALE, lexicon } = {}) {
  const words = (spokenText(line).match(LATIN_WORD) ?? [])
    .map((word) => word.replace(/[.'_-]+$/, ""))
    .filter((word) => /[A-Za-z]/.test(word) && word.length <= 40)
    .filter((word) => locale !== "en" || dictionaryTerm(word, lexicon));
  return [...new Set(words)].slice(0, MAX_HINT_TERMS);
}

/** How a text is read aloud, tone by tone: 它 and 他 read the same, 旗 and 期 do not. */
export function reading(text) {
  return pinyin(comparable(text), { toneType: "num", type: "array", nonZh: "consecutive", v: true }).join(" ");
}

/**
 * Whether a transcript already says the line, before any judgement is needed, and how:
 * "exact" word for word, "filler" apart from interjections, "sound" apart from characters that
 * read the same; null when only a judgement can tell. Outside Chinese only "exact" is possible.
 */
export function matchKind(heard, line, lexicon, locale = NARRATION_LOCALE) {
  const forms = [line.text, spokenText(line), spokenForm(line, lexicon)];
  const said = comparable(heard);
  if (forms.some((form) => comparable(form) === said)) return "exact";
  // Same-sound characters and filler particles are Mandarin's; in another language, whatever
  // differs beyond spelling is Jev's to judge.
  if (!CHINESE.has(locale)) return null;
  const bare = (text) => comparable(text).replace(FILLERS, "");
  // A closing particle comes off what was heard only, so a script ending in 氣餒 still needs it.
  const saidBare = [bare(heard), bare(heard).replace(CLOSING_PARTICLES, "")];
  if (forms.some((form) => saidBare.includes(bare(form)))) return "filler";
  const saidReadings = saidBare.map(reading);
  if (forms.some((form) => saidReadings.includes(reading(bare(form))))) return "sound";
  return null;
}

export function matches(heard, line, lexicon, locale) {
  return matchKind(heard, line, lexicon, locale) !== null;
}

const clipHash = (bytes) => createHash("sha256").update(bytes).digest("hex").slice(0, 16);

/** The first `max` characters of a text, counted the way the server counts them (code points). */
function fit(text, max) {
  const characters = [...String(text)];
  return characters.length > max ? characters.slice(0, max).join("") : String(text);
}

/** The narration's lines in order, each with the scene it belongs to. */
function narrationLines(doc) {
  return [...eachLine(doc)].map(({ scene, line }) => ({ scene: scene.id, line }));
}

/**
 * A dub's lines in its timeline's order, each saying its translation. A line the translation no
 * longer has can be checked against nothing, so the dub is remade first.
 */
export function dubLines(timeline, translation, locale, slug) {
  return (timeline.lines ?? []).map((entry) => {
    const text = translation?.lines?.[entry.id]?.text;
    if (typeof text !== "string" || !text.trim()) {
      throw new UsageError(`line ${entry.id} has no ${locale} translation: run i18n-merge, then dub --slug ${slug} --locale ${locale} again`);
    }
    return { scene: entry.scene, line: { id: entry.id, text } };
  });
}

export async function checkAudio(args, ctx, options) {
  const { EXIT } = ctx;
  const values = parseArgs({
    args,
    options: {
      slug: { type: "string" },
      file: { type: "string" },
      workdir: { type: "string" },
      threshold: { type: "string" },
      force: { type: "boolean" },
      locale: { type: "string" },
    },
    strict: true,
  }).values;
  if (!values.slug && !values.file) throw new UsageError("check-audio needs --slug (or --file for an example outside docs/videos)");
  const threshold = values.threshold === undefined ? DEFAULT_THRESHOLD : Number(values.threshold);
  if (!(threshold > 0 && threshold < 1)) throw new UsageError("--threshold must be between 0 and 1");
  const project = loadProject({ slug: values.slug, file: values.file, root: ctx.root });
  const narration = narrationLocale(project.doc);
  const locale = values.locale === undefined ? narration : parseDubLocale(values.locale, narration);
  const dub = locale !== narration;
  if (lintProject(project).errors.length) {
    ctx.stdout.write(`${project.doc.slug} has lint errors; run lint first\n`);
    return EXIT.lint;
  }
  const { doc } = project;
  const lexicon = lexiconFor(project.lexicon ?? readJson(lexiconFile(ctx.root), emptyLexicon()), locale, narration);
  const workdir = resolveWorkdir({ flag: values.workdir, env: ctx.env, slug: doc.slug, root: ctx.root, home: ctx.home });
  const track = trackFiles(locale, narration);
  const timeline = readJson(path.join(workdir, track.timeline), null);
  if (!timeline) {
    throw new UsageError(dub ? `no ${locale} dub yet: run dub --slug ${doc.slug} --locale ${locale} first` : `no narration yet: run tts --slug ${doc.slug} first`);
  }
  const lines = dub ? dubLines(timeline, project.translations[locale], locale, doc.slug) : narrationLines(doc);
  // What makes the clips again: the flags file goes to it as `--redo`.
  const remake = dub ? `dub --slug ${doc.slug} --locale ${locale}` : `tts --slug ${doc.slug}`;
  const audioDir = path.join(workdir, track.audio);
  const files = checkFiles(locale, narration);
  const cacheFile = path.join(workdir, files.cache);
  const cache = readJson(cacheFile, { lines: {} });
  const results = {};

  let transcribed = 0;
  let failedInARow = 0;
  let gaveUp = false;
  const unchecked = new Map();
  for (const { scene, line } of lines) {
    if (stopRequested(workdir)) {
      ctx.stdout.write("STOP found; transcripts so far are saved\n");
      return EXIT.ok;
    }
    const file = path.join(audioDir, `${line.id}.wav`);
    if (!existsSync(file)) throw new UsageError(`no clip for line ${line.id}: run ${remake}`);
    const bytes = readFileSync(file);
    const clip = clipHash(bytes);
    const cached = cache.lines[line.id];
    const terms = hintTerms(line, { locale, lexicon });
    // A transcript made with other hints (or none, before hints existed) is made again.
    const sameHints = (cached?.terms ?? []).join(" ") === terms.join(" ");
    let entry = !values.force && cached?.clip === clip && sameHints && typeof cached.heard === "string" ? cached : null;
    if (!entry) {
      const samples = requireNarrationFormat(parseWav(bytes));
      const wav = encodeWav(downsample(samples, Math.round(48_000 / TRANSCRIBE_RATE)), TRANSCRIBE_RATE);
      let heard;
      try {
        heard = await transcribeClip({ ...options, wav, terms, language: locale });
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
      entry = { scene, clip, terms, heard, noul: null };
    }
    entry.intended = spokenText(line);
    entry.spoken_form = spokenForm(line, lexicon);
    entry.match_kind = matchKind(entry.heard, line, lexicon, locale);
    entry.match = entry.match_kind !== null;
    results[line.id] = entry;
    cache.lines[line.id] = entry;
    atomicWrite(cacheFile, `${JSON.stringify(cache, null, 2)}\n`);
  }

  // Jev looks only at lines whose transcript differs and has not been judged for this clip.
  const toJudge = Object.entries(results).filter(([, entry]) => !entry.match && typeof entry.noul !== "number");
  const byScene = new Map();
  const cut = [];
  for (const [id, entry] of toJudge) {
    if (!byScene.has(entry.scene)) byScene.set(entry.scene, []);
    const question = {
      id,
      intended: fit(entry.intended, MAX_INTENDED_CHARACTERS),
      spoken_form: fit(entry.spoken_form, MAX_INTENDED_CHARACTERS),
      heard: fit(entry.heard, MAX_HEARD_CHARACTERS),
    };
    if (question.intended !== entry.intended || question.spoken_form !== entry.spoken_form || question.heard !== entry.heard) cut.push(id);
    byScene.get(entry.scene).push(question);
  }
  let jevCalls = 0;
  for (const questions of byScene.values()) {
    for (let start = 0; start < questions.length; start += MAX_JUDGE_LINES) {
      const batch = questions.slice(start, start + MAX_JUDGE_LINES);
      const verdicts = await judgeLines({ ...options, lines: batch, language: locale });
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
  const flagsFile = path.join(workdir, files.flags);
  const notes = Object.fromEntries(flagged.map(([id, entry]) => [id, `Jev ${entry.noul.toFixed(2)}: heard 「${entry.heard}」`]));
  // A dub's flags name their track, and the translation the dub was read from.
  const provenance = dub ? { locale, translation_hash: timeline.translation_hash } : {};
  atomicWrite(flagsFile, `${JSON.stringify({ slug: doc.slug, ...provenance, speech_hash: timeline.speech_hash, flags: flagged.map(([id]) => id), notes }, null, 2)}\n`);
  const total = lines.length;
  const missing = total - entries.length;
  recordStage(
    workdir,
    "check-audio",
    { ...(dub ? { locale } : {}), lines: total, exact, alike, judged: judgedFine + flagged.length, flagged: flagged.length, unchecked: missing, transcribed, jev_calls: jevCalls },
    ctx.now(),
  );

  ctx.stdout.write(
    `${dub ? `${locale} dub: ` : ""}${entries.length} of ${total} lines checked: ${exact} match the script word for word, ${alike} differ only by same-sound characters or filler words, ${judgedFine} judged fine by Jev, ${flagged.length} flagged (below ${threshold})\n`,
  );
  ctx.stdout.write(`${transcribed} clips transcribed now, ${jevCalls} Jev calls; details in ${cacheFile}\n`);
  for (const id of cut) {
    ctx.stdout.write(`  ${id}  is longer than Jev takes: it judged the first ${MAX_INTENDED_CHARACTERS} characters of the script and ${MAX_HEARD_CHARACTERS} of the transcript\n`);
  }
  for (const [id, entry] of flagged) {
    ctx.stdout.write(`  ${id}  Jev ${entry.noul.toFixed(2)}\n    script: ${entry.intended}\n    heard:  ${entry.heard}\n`);
  }
  if (flagged.length) {
    ctx.stdout.write(`next: fix the dictionary or the ${dub ? "translation" : "line"}, then node tools/video/cli.mjs ${remake} --redo ${flagsFile}\n`);
  }
  if (missing) {
    const why = gaveUp ? `Gemini failed ${GIVE_UP_AFTER} lines in a row, so the run stopped` : "Gemini would not transcribe them";
    ctx.stdout.write(`${missing} lines not checked yet (${why}); run check-audio again later, finished lines are kept\n`);
    for (const [id, message] of unchecked) ctx.stdout.write(`  ${id}  ${message}\n`);
    return EXIT.external;
  }
  return flagged.length ? EXIT.lint : EXIT.ok;
}
