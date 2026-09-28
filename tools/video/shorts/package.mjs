// `package`: what goes to YouTube with a Short, and the check that it is all there
// (docs/videos/SHORTS.md §上架).
//
// upload/metadata.json holds every field the site sets on the video: the title and its spare,
// the description, tags, the category of the content line, whether it is made for kids, and the
// answer to "altered or synthetic content" with its reason. The package check has the four items
// the site requires on a publish review, in the shape of the quality check's report; its
// `final_sha256` is the hash of metadata.json, the file the publish review is bound to, as in
// tools/video/package/check.mjs.
import { existsSync, readFileSync, writeFileSync } from 'node:fs';
import path from 'node:path';

import { readJson } from '../core/paths.mjs';
import { MAX_HASHTAGS, SCRIPT_FILE, lineOf, parseSrt, saveJson, sha256 } from './core.mjs';

export const PACKAGE_ITEM_IDS = Object.freeze(['files', 'descriptions', 'captions', 'disclosure']);
export const METADATA_FILE = 'metadata.json';
export const PACKAGE_FILE = 'package.json';
export const DESCRIPTION_FILE = 'description.zh-TW.txt';
export const CAPTIONS_FILE = 'zh-TW.srt';
export const EXTRA_LOCALES = Object.freeze(['en', 'ja', 'ko', 'zh-CN']);
const selectedLocales = (settings) => EXTRA_LOCALES.filter((locale) => Array.isArray(settings?.locales) && settings.locales.includes(locale));
export const captionLocales = (metadata) => ['zh-TW', ...selectedLocales(metadata)];
// YouTube's categories: Science & Technology, and Entertainment for a drama.
export const CATEGORY = Object.freeze({ lab: '28', cut: '28', drama: '24' });
const DEFAULT_HASHTAGS = Object.freeze({ lab: ['#AI', '#實測'], cut: ['#AI'], drama: ['#AI漫劇'] });
export const TITLE_MAX = 100;
export const DESCRIPTION_MAX_BYTES = 5000;
export const TAGS_MAX = 500;

export const item = (id, ok, detail) => ({ id, ok: Boolean(ok), detail: String(detail) });
const bytesOf = (text) => Buffer.byteLength(text, 'utf8');

/**
 * Whether the video is disclosed as altered or synthetic content, and why. Cards with a
 * synthetic narrator are not what the question asks about; a realistic generated picture is, and
 * so is a drama, whose every frame is generated.
 */
export function disclosureOf(doc) {
  const line = lineOf(doc);
  if (line === 'drama') return { synthetic: true, reason: '畫面是 AI 生成的漫劇' };
  if (doc.synthetic_media === true) return { synthetic: true, reason: '畫面裡有擬真的生成圖' };
  return { synthetic: false, reason: line === 'cut' ? '重寫的字卡與合成旁白，沒有擬真的生成或變造內容' : '字卡、實測紀錄與合成旁白，沒有擬真的生成或變造內容' };
}

export function hashtagsOf(doc) {
  const tags = (doc.hashtags?.length ? doc.hashtags : DEFAULT_HASHTAGS[lineOf(doc)]).map((tag) => (tag.startsWith('#') ? tag : `#${tag}`));
  return [...new Set(tags)].slice(0, MAX_HASHTAGS);
}

export function tagsOf(doc) {
  const own = Array.isArray(doc.tags) ? doc.tags : [];
  return [...new Set([...own, ...hashtagsOf(doc).map((tag) => tag.slice(1))])];
}

/** The address of the full video a highlight or a vertical short leads back to, or null. */
export const sourceUrlOf = (doc, source = null) => doc.source?.url ?? (source?.youtube_video_id ? `https://youtu.be/${source.youtube_video_id}` : null);

/**
 * The description. A Short's "related video" can only be set in Studio, so the link back to the
 * full video is the first line; the test's scope and its limits follow for an experiment.
 */
export function composeDescription(doc, { sourceUrl = null } = {}) {
  const parts = [];
  if (sourceUrl) parts.push(`完整影片：${sourceUrl}`);
  parts.push(doc.description.trim());
  if (lineOf(doc) === 'lab') parts.push(`實測範圍：${doc.experiment_summary.trim()}\n限制：${doc.limitations.trim()}`);
  if (doc.links?.length) parts.push(doc.links.map((link) => `${link.label.trim()}：${link.url}`).join('\n'));
  parts.push(hashtagsOf(doc).join(' '));
  return `${parts.join('\n\n')}\n`;
}

export function composeMetadata({ doc, finalSha256, seconds, settings = {}, sourceUrl = null }) {
  const line = lineOf(doc);
  const disclosure = disclosureOf(doc);
  return {
    schema_version: 1,
    kind: 'shorts',
    slug: doc.slug,
    line,
    series: doc.series,
    source: doc.source ? { ...doc.source, ...(sourceUrl ? { url: sourceUrl } : {}) } : null,
    default_language: 'zh-TW',
    locales: selectedLocales(settings),
    title: doc.titles[0],
    titles: [...doc.titles],
    description: composeDescription(doc, { sourceUrl }),
    tags: tagsOf(doc),
    hashtags: hashtagsOf(doc),
    category_id: CATEGORY[line],
    made_for_kids: settings.made_for_kids === true,
    contains_synthetic_media: disclosure.synthetic,
    disclosure_reason: disclosure.reason,
    duration_seconds: seconds,
    final_sha256: finalSha256,
  };
}

/** What YouTube would refuse or cut in the metadata; empty when it fits. */
export function metadataProblems(metadata) {
  const problems = [];
  for (const title of metadata.titles ?? []) {
    if (![...title].length || [...title].length > TITLE_MAX) problems.push(`a title of ${[...title].length} characters (1 to ${TITLE_MAX})`);
    if (/[<>]/.test(title)) problems.push(`a title with an angle bracket: ${title}`);
  }
  if ((metadata.titles ?? []).length !== 2) problems.push('two titles are needed: the one in use and a spare');
  if (bytesOf(metadata.description ?? '') > DESCRIPTION_MAX_BYTES) problems.push(`the description is ${bytesOf(metadata.description)} bytes (at most ${DESCRIPTION_MAX_BYTES})`);
  if (/[<>]/.test(metadata.description ?? '')) problems.push('the description has an angle bracket');
  // YouTube counts a tag with a space as quoted, and the commas between tags.
  const tags = (metadata.tags ?? []).map((tag) => (/\s/.test(tag) ? `"${tag}"` : tag)).join(',');
  if (tags.length > TAGS_MAX) problems.push(`the tags are ${tags.length} characters together (at most ${TAGS_MAX})`);
  if ((metadata.hashtags ?? []).length > MAX_HASHTAGS) problems.push(`${metadata.hashtags.length} hashtags (at most ${MAX_HASHTAGS})`);
  if (metadata.source && !metadata.source.url) problems.push('the full video has no address yet, so the description cannot lead back to it');
  return problems;
}

/** Why a caption file does not match the timeline; empty when it does. */
export function captionProblems(source, timeline, { checkText = true } = {}) {
  let cues;
  try {
    cues = parseSrt(source);
  } catch (error) {
    return [error.message];
  }
  if (cues.length !== timeline.cues.length) return [`${cues.length} captions for ${timeline.cues.length} phrases`];
  const problems = [];
  for (const [index, cue] of cues.entries()) {
    const expected = timeline.cues[index];
    if (checkText && cue.text !== expected.text) problems.push(`caption ${index + 1} says another phrase`);
    if (Math.abs(cue.start - expected.startFrame / timeline.fps) > 0.002 || Math.abs(cue.end - expected.endFrame / timeline.fps) > 0.002) problems.push(`caption ${index + 1} is off the timeline`);
  }
  return problems;
}

/** The four items of the package check, from what upload/ holds. `files` maps a name to its bytes. */
export function packageItems({ files, metadata, timeline, qa }) {
  const names = ['final.mp4', CAPTIONS_FILE, 'cover.png', METADATA_FILE, ...selectedLocales(metadata).map((locale) => `${locale}.srt`)];
  const missing = names.filter((name) => !files.has(name));
  const finalSha = files.has('final.mp4') ? sha256(files.get('final.mp4')) : null;
  const fileProblems = missing.map((name) => `${name} is missing`);
  if (finalSha && metadata && metadata.final_sha256 !== finalSha) fileProblems.push('metadata.json records another final cut');
  if (finalSha && qa?.final_sha256 !== finalSha) fileProblems.push('the quality check is of another final cut, or has not run');
  for (const locale of captionLocales(metadata)) {
    const caption = files.get(`${locale}.srt`);
    if (caption && metadata?.captions_sha256?.[locale] !== sha256(caption)) fileProblems.push(`${locale}.srt differs from the metadata binding`);
  }
  const description = files.has(DESCRIPTION_FILE) ? files.get(DESCRIPTION_FILE).toString('utf8') : null;
  const descriptionProblems = [];
  if (description === null) descriptionProblems.push(`${DESCRIPTION_FILE} is missing`);
  else if (metadata && description !== metadata.description) descriptionProblems.push(`${DESCRIPTION_FILE} differs from metadata.json`);
  if (metadata) descriptionProblems.push(...metadataProblems(metadata));
  const captions = captionLocales(metadata).flatMap((locale) => {
    const name = `${locale}.srt`;
    if (!files.has(name)) return [`${name} is missing`];
    return captionProblems(files.get(name).toString('utf8'), timeline, { checkText: locale === 'zh-TW' }).map((problem) => `${locale}: ${problem}`);
  });
  const disclosed = typeof metadata?.contains_synthetic_media === 'boolean' && typeof metadata.disclosure_reason === 'string' && metadata.disclosure_reason.trim().length > 0;
  return [
    item('files', !fileProblems.length, fileProblems.length ? fileProblems.join('; ') : `${names.join(', ')}; final.mp4 is the checked cut (${finalSha.slice(0, 12)})`),
    item('descriptions', !descriptionProblems.length, descriptionProblems.length ? descriptionProblems.join('; ') : `zh-TW, ${bytesOf(description)} bytes`),
    item('captions', !captions.length, captions.length ? captions.join('; ') : `${captionLocales(metadata).join(", ")}: ${timeline.cues.length} captions on the timeline`),
    item('disclosure', disclosed, disclosed ? `${metadata.contains_synthetic_media ? 'disclosed as synthetic' : 'not synthetic'}: ${metadata.disclosure_reason}` : 'metadata.json does not answer the synthetic content question'),
  ];
}

/** The report the site reads: { ok, final_sha256, kind: "shorts", items }. */
export function packageReport(items, metadataSha256) {
  const ids = items.map((each) => each.id);
  if (ids.length !== PACKAGE_ITEM_IDS.length || ids.some((id, index) => id !== PACKAGE_ITEM_IDS[index])) throw new Error(`package items must be exactly ${PACKAGE_ITEM_IDS.join(', ')}; got ${ids.join(', ')}`);
  return { ok: items.every((each) => each.ok), final_sha256: metadataSha256 ?? null, kind: 'shorts', items };
}

/** The files of upload/ the package is made of, by name; a missing one is left out. */
export function uploadFiles(directory, metadata = {}) {
  const files = new Map();
  for (const name of ['final.mp4', CAPTIONS_FILE, 'cover.png', METADATA_FILE, DESCRIPTION_FILE, ...selectedLocales(metadata).map((locale) => `${locale}.srt`)]) {
    const file = path.join(directory, 'upload', name);
    if (existsSync(file)) files.set(name, readFileSync(file));
  }
  return files;
}

/**
 * Write a build's metadata.json and description, check the package, and let the manifest say how
 * the quality check went. `source` is the site's record of the video a highlight was cut from.
 */
export function packageBuild({ directory, settings = {}, source = null, now = () => new Date() }) {
  const doc = readJson(path.join(directory, SCRIPT_FILE), null);
  const timeline = readJson(path.join(directory, 'timeline.json'), null);
  if (!doc || !timeline) throw new Error(`${directory} is not a finished build: build the Short first`);
  const qa = readJson(path.join(directory, 'qa.json'), null);
  const finalBytes = readFileSync(path.join(directory, 'upload', 'final.mp4'));
  const metadata = composeMetadata({ doc, finalSha256: sha256(finalBytes), seconds: timeline.seconds, settings, sourceUrl: sourceUrlOf(doc, source) });
  // The server's approval identity is metadata.json's hash. Bind every selected track into it
  // so repackaging changed caption bytes cannot reuse an earlier approved review.
  const files = uploadFiles(directory, metadata);
  metadata.captions_sha256 = Object.fromEntries(captionLocales(metadata).flatMap((locale) => {
    const caption = files.get(`${locale}.srt`);
    return caption ? [[locale, sha256(caption)]] : [];
  }));
  const metadataText = `${JSON.stringify(metadata, null, 2)}\n`;
  writeFileSync(path.join(directory, 'upload', METADATA_FILE), metadataText);
  writeFileSync(path.join(directory, 'upload', DESCRIPTION_FILE), metadata.description);
  const report = packageReport(packageItems({ files: uploadFiles(directory, metadata), metadata, timeline, qa }), sha256(metadataText));
  saveJson(path.join(directory, PACKAGE_FILE), { ...report, checked_at: now().toISOString() });
  const manifestFile = path.join(directory, 'upload', 'manifest.json');
  const manifest = readJson(manifestFile, {});
  const names = [...uploadFiles(directory, metadata).keys()];
  saveJson(manifestFile, {
    ...manifest,
    // What the checks found, not a fixed word: the site decides from the reports, not from this.
    status: !qa || qa.final_sha256 !== metadata.final_sha256 ? 'unchecked' : qa.ok ? 'qa-passed' : 'qa-failed',
    packaged_at: now().toISOString(),
    files: names.map((name) => ({ name, sha256: sha256(readFileSync(path.join(directory, 'upload', name))) })),
  });
  return { metadata, report };
}
