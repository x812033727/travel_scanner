// `qa`: the twelve checks a Short's final cut passes before the site approves it without the
// owner (docs/videos/SHORTS.md §自動品管). The report is what `push` sends with the final review:
// { ok, final_sha256, kind: "shorts", line, items }, the items in ITEM_IDS order, which is the
// order of SHORTS_QA_ITEMS in apps/api/app/video_automation/judge.py.
//
// Every item is a pure function over what was read or measured; `runQa` does the reading, the
// measuring and the calls. The cut is measured again here with ffprobe and ffmpeg: the build's
// own receipt is not taken for the answer. A call that fails (Jev, a link, the site) fails its
// item; nothing passes because it could not be checked.
import { existsSync, readFileSync } from 'node:fs';
import path from 'node:path';

import { locateFfmpeg } from '../assemble/ffmpeg.mjs';
import { readJson } from '../core/paths.mjs';
import { checkLinks, descriptionUrls, linkChecker, linksDetail } from '../qa/links.mjs';
import { policyVerdict } from '../qa/policy.mjs';
import { comparable } from '../tts/check.mjs';
import { loudnessProblems, measureFinal, profileProblems } from './build.mjs';
import { audioHash, buildClips, CHECK_FILE } from './check.mjs';
import { PROFILE, SCRIPT_FILE, lineOf, phrasesOf, saveJson, sha256, verifyEvidence } from './core.mjs';
import { CAPTIONS_FILE, captionProblems, composeMetadata, disclosureOf, metadataProblems, sourceUrlOf } from './package.mjs';

export const ITEM_IDS = Object.freeze(['profile', 'loudness', 'layout', 'narration', 'evidence', 'facts', 'policy', 'metadata', 'captions', 'links', 'variety', 'disclosure']);
export const QA_FILE = 'qa.json';
export const VERIFY_FILE = 'verify.json';
// How many of the latest Shorts an opening is compared with.
export const VARIETY_WINDOW = 30;
const OFFLINE = 'not checked: the quality check ran without the site';

export const item = (id, ok, detail) => ({ id, ok: Boolean(ok), detail: String(detail) });
const verdict = (id, problems, fine) => item(id, !problems.length, problems.length ? problems.join('; ') : fine);

/** The report the site reads; throws when the items are not exactly the twelve, in order. */
export function qaReport(items, finalSha256, line) {
  const ids = items.map((each) => each.id);
  if (ids.length !== ITEM_IDS.length || ids.some((id, index) => id !== ITEM_IDS[index])) throw new Error(`qa items must be exactly ${ITEM_IDS.join(', ')}; got ${ids.join(', ')}`);
  return { ok: items.every((each) => each.ok), final_sha256: finalSha256 ?? null, kind: 'shorts', line, items };
}

export function profileItem({ measured, frames, range = PROFILE }) {
  const problems = profileProblems(measured, frames);
  const seconds = frames / PROFILE.fps;
  if (seconds < range.minSeconds || seconds > range.maxSeconds) problems.push(`${seconds.toFixed(2)}s is outside ${range.minSeconds}–${range.maxSeconds}s`);
  return verdict('profile', problems, `${PROFILE.width}×${PROFILE.height}, ${PROFILE.fps} fps, ${seconds.toFixed(2)}s, ${frames} frames, h264 and aac at 48 kHz`);
}

export function loudnessItem({ loudness }) {
  return verdict('loudness', loudnessProblems(loudness), `${loudness.input_i} LUFS, true peak ${loudness.input_tp} dBTP`);
}

/** layout: every cue was measured inside the safe area when the cards were rendered. */
export function layoutItem({ checks, cues }) {
  if (!checks) return item('layout', false, 'checks.json is missing; build the Short first');
  if (checks.imported) return item('layout', false, 'a cut made elsewhere has no layout measurement: look at it once with the safe-area overlay on the site');
  const measured = Array.isArray(checks.layout) ? checks.layout : [];
  const problems = measured.flatMap((entry) => (entry.problems ?? []).map((problem) => `cue ${entry.cue}: ${problem}`));
  if (measured.length !== cues) problems.push(`${measured.length} cues measured of ${cues}`);
  return verdict('layout', problems, `${cues} cards inside the safe area, captions above the interface`);
}

/** narration: the listener's check passed, for these very clips, over every phrase. */
export function narrationItem({ check, audioSha256, phrases }) {
  if (!check) return item('narration', false, 'check.json is missing; run check-audio');
  const problems = [];
  if (check.audio_sha256 !== audioSha256) problems.push('the check is of other audio; run check-audio again');
  if (check.lines !== phrases || check.checked !== phrases) problems.push(`${check.checked} of ${phrases} phrases checked`);
  if (check.flagged) problems.push(`${check.flagged} phrases flagged: ${(check.flagged_lines ?? []).map((line) => `#${line.index} heard 「${line.heard}」`).join(', ')}`);
  if (check.ok !== true && !problems.length) problems.push('the check did not pass');
  return verdict('narration', problems, `${phrases} phrases say what the script says`);
}

/**
 * evidence: an experiment's evidence files are the ones the script names, byte for byte; a
 * highlight's or a vertical short's source is a video the site knows that is public, or whose
 * final cut is approved. `source` is the site's record, null when it has none.
 */
export function evidenceItem({ doc, evidenceError = null, source = null, now = new Date() }) {
  if (lineOf(doc) === 'lab') {
    if (evidenceError) return item('evidence', false, evidenceError);
    return item('evidence', true, `${doc.evidence.length} evidence files match the script's hashes`);
  }
  if (!doc.source?.slug) return item('evidence', true, 'a short of its own, cut from no video');
  if (!source) return item('evidence', false, `the site has no video ${doc.source.slug}, or did not answer`);
  if (source.dropped_at) return item('evidence', false, `${doc.source.slug} was dropped`);
  const publishAt = source.youtube_publish_at ? new Date(source.youtube_publish_at) : null;
  const isPublic = Boolean(source.youtube_video_id) && publishAt !== null && publishAt <= now;
  const approved = (source.reviews ?? []).some((review) => review.gate === 'final' && review.status === 'approved');
  if (isPublic) return item('evidence', true, `cut from ${doc.source.slug}, public since ${publishAt.toISOString()}`);
  if (approved) return item('evidence', true, `cut from ${doc.source.slug}, whose final cut is approved`);
  return item('evidence', false, `${doc.source.slug} is neither public nor approved yet`);
}

/**
 * facts: a checker in a conversation of its own compared every number and conclusion on the
 * cards and in the narration with the evidence, for this very script, and found nothing.
 * verify.json: { ok, document_sha256, checked_by, claims: [{ text, ok }], problems: [] }.
 */
export function factsItem({ verify, documentSha256 }) {
  if (!verify) return item('facts', false, 'verify.json is missing: the script has not been checked against its evidence');
  const problems = [];
  if (verify.document_sha256 !== documentSha256) problems.push('the check is of another version of the script');
  const open = [...(Array.isArray(verify.problems) ? verify.problems : []), ...(Array.isArray(verify.claims) ? verify.claims.filter((claim) => claim?.ok !== true).map((claim) => claim?.text ?? 'a claim') : [])];
  if (open.length) problems.push(`not backed by the evidence: ${open.map(String).join('; ')}`);
  if (!Array.isArray(verify.claims) || !verify.claims.length) problems.push('the check lists no claim');
  if (verify.ok !== true && !problems.length) problems.push('the check did not pass');
  return verdict('facts', problems, `${verify.claims?.length ?? 0} claims backed by the evidence${verify.checked_by ? `, checked by ${verify.checked_by}` : ''}`);
}

export function policyItem(answer) {
  const { ok, detail } = policyVerdict(answer);
  return item('policy', ok, detail);
}

export function metadataItem({ metadata }) {
  return verdict('metadata', metadataProblems(metadata), `title ${[...metadata.title].length} characters, description ${Buffer.byteLength(metadata.description, 'utf8')} bytes, ${metadata.tags.length} tags, ${metadata.hashtags.length} hashtags`);
}

/** captions: zh-TW is there and on the timeline; so is every language the settings add. */
export function captionsItem({ captions, timeline, locales = [] }) {
  const problems = captions.has('zh-TW') ? captionProblems(captions.get('zh-TW'), timeline) : [`${CAPTIONS_FILE} is missing`];
  for (const locale of locales) {
    if (!captions.has(locale)) problems.push(`${locale}.srt is missing`);
    else {
      // A translation says other words on the same clock.
      const translated = captionProblems(captions.get(locale), timeline, { checkText: false });
      problems.push(...translated.map((problem) => `${locale}: ${problem}`));
    }
  }
  return verdict('captions', problems, `${['zh-TW', ...locales].join(', ')}: ${timeline.cues.length} captions on the timeline`);
}

export function linksItem({ results, metadata }) {
  const broken = results.filter((result) => !result.ok);
  if (metadata.source && !metadata.source.url) return item('links', false, 'the description does not lead back to the full video yet');
  return item('links', !broken.length, linksDetail(results));
}

/** What two Shorts are compared on: how the first phrase reads, and how the cards are built. */
export function scriptShape(doc) {
  return {
    opening: comparable(phrasesOf(doc)[0] ?? ''),
    structure: doc.scenes.map((scene) => `${scene.narration.length}${scene.big ? 'b' : ''}${scene.asset ? 'a' : ''}${scene.body?.length ?? 0}${scene.note ? 'n' : ''}`).join('-'),
  };
}

/**
 * variety: the opening is not one of the latest Shorts', and the cards are not built exactly
 * like the series' previous Short. `history` is the latest Shorts, newest first, each
 * { slug, series, opening, structure }; null when the site did not answer.
 */
export function varietyItem({ doc, history }) {
  if (!Array.isArray(history)) return item('variety', false, 'the latest Shorts could not be read from the site');
  const mine = scriptShape(doc);
  const others = history.filter((entry) => entry.slug !== doc.slug).slice(0, VARIETY_WINDOW);
  const problems = [];
  const same = others.find((entry) => entry.opening && comparable(entry.opening) === mine.opening);
  if (same) problems.push(`${same.slug} opens with the same words`);
  const previous = others.find((entry) => entry.series === doc.series);
  if (previous?.structure && previous.structure === mine.structure) problems.push(`the cards are built exactly like ${previous.slug}, the series' previous Short`);
  return verdict('variety', problems, `the opening differs from the latest ${others.length} Shorts${previous ? `, the cards from ${previous.slug}` : ''}`);
}

/** disclosure: records the answer; it never fails the check. */
export function disclosureItem({ doc }) {
  const { synthetic, reason } = disclosureOf(doc);
  return item('disclosure', true, `${synthetic ? 'disclosed as altered or synthetic content' : 'not disclosed'}: ${reason}`);
}

/** The latest Shorts as the site has them: what each final review carried in payload.script. */
export async function siteHistory(client, limit = VARIETY_WINDOW) {
  const listed = await client.videos({ shorts: 'only', limit: String(limit * 2) });
  const history = [];
  for (const video of listed) {
    if (history.length >= limit + 1) break;
    const project = await client.project(video.slug);
    const final = (project?.reviews ?? []).find((review) => review.gate === 'final' && review.status !== 'superseded' && review.payload?.script);
    if (final) history.push({ slug: video.slug, series: video.shorts_series ?? final.payload.script.series ?? null, opening: final.payload.script.opening ?? '', structure: final.payload.script.structure ?? '' });
  }
  return history;
}

const failing = async (call) => {
  try {
    return { value: await call() };
  } catch (error) {
    return { error: error?.message ?? String(error) };
  }
};

/**
 * Check a build directory and write its qa.json. `client` is the site (null with `offline`, when
 * the items that need it fail saying so); `tools`, `linkCheck` and `history` are for tests.
 */
export async function runQa({ directory, client = null, offline = false, settings = null, tools = null, linkCheck = null, history = undefined, now = () => new Date() }) {
  const scriptFile = path.join(directory, SCRIPT_FILE);
  if (!existsSync(scriptFile)) throw new Error(`${directory} holds no ${SCRIPT_FILE}: it is not a build of this tool`);
  const scriptBytes = readFileSync(scriptFile);
  const doc = JSON.parse(scriptBytes);
  const timeline = readJson(path.join(directory, 'timeline.json'), null);
  const final = path.join(directory, 'upload', 'final.mp4');
  if (!timeline || !existsSync(final)) throw new Error(`${directory} is not a finished build`);
  const online = !offline && client !== null;
  const finalSha = sha256(readFileSync(final));
  const phrases = phrasesOf(doc);
  const used = settings ?? (online ? (await failing(() => client.settings())).value : null) ?? {};
  const range = { minSeconds: used.seconds_min ?? PROFILE.minSeconds, maxSeconds: used.seconds_max ?? PROFILE.maxSeconds };
  const measured = await measureFinal(final, tools ?? (await locateFfmpeg()));

  const line = lineOf(doc);
  let evidenceError = null;
  if (line === 'lab') {
    try {
      verifyEvidence(doc, path.join(directory, 'evidence'));
    } catch (error) {
      evidenceError = error.message;
    }
  }
  const source = line !== 'lab' && doc.source?.slug && online ? (await failing(() => client.project(doc.source.slug))).value ?? null : null;
  const metadata = composeMetadata({ doc, finalSha256: finalSha, seconds: timeline.seconds, settings: used, sourceUrl: sourceUrlOf(doc, source) });

  let policy = item('policy', false, OFFLINE);
  if (online) {
    const asked = await failing(() => client.judgePolicy({ slug: doc.slug, script: phrases.join('\n'), viewpoint: '' }));
    policy = asked.error ? item('policy', false, asked.error) : policyItem(asked.value);
  }
  let links = item('links', false, OFFLINE);
  if (!offline) {
    const urls = descriptionUrls([metadata.description]);
    links = linksItem({ results: await checkLinks(urls, linkCheck ?? linkChecker()), metadata });
  }
  const past = history !== undefined ? history : online ? (await failing(() => siteHistory(client))).value ?? null : null;
  const captions = new Map();
  for (const locale of ['zh-TW', ...(used.locales ?? [])]) {
    const file = path.join(directory, 'upload', `${locale}.srt`);
    if (existsSync(file)) captions.set(locale, readFileSync(file, 'utf8'));
  }
  const clips = (() => {
    try {
      return buildClips(directory, phrases.length);
    } catch {
      return null;
    }
  })();

  const items = [
    profileItem({ measured, frames: timeline.frames, range }),
    loudnessItem({ loudness: measured.loudness }),
    layoutItem({ checks: readJson(path.join(directory, 'checks.json'), null), cues: timeline.cues.length }),
    clips ? narrationItem({ check: readJson(path.join(directory, CHECK_FILE), null), audioSha256: audioHash(clips), phrases: phrases.length }) : item('narration', false, 'the clips of the phrases are missing'),
    line !== 'lab' && doc.source?.slug && !online ? item('evidence', false, OFFLINE) : evidenceItem({ doc, evidenceError, source, now: now() }),
    factsItem({ verify: readJson(path.join(directory, VERIFY_FILE), null), documentSha256: sha256(scriptBytes) }),
    policy,
    metadataItem({ metadata }),
    captionsItem({ captions, timeline, locales: used.locales ?? [] }),
    links,
    past === null && offline ? item('variety', false, OFFLINE) : varietyItem({ doc, history: past }),
    disclosureItem({ doc }),
  ];
  const report = qaReport(items, finalSha, line);
  saveJson(path.join(directory, QA_FILE), { ...report, script: { series: doc.series, ...scriptShape(doc) }, checked_at: now().toISOString() });
  return report;
}
