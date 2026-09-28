// `push`: a finished Short goes to the site (docs/videos/SHORTS.md §工具端).
//
// It reports the video (format "shorts", its content line, series and source), uploads the files
// in parts, and submits the final review with the quality check's report and what making the
// Short used. When the site approves the cut, on arrival or by the owner's hand, the same command
// submits the upload package. Each review is bound to the hash of the file it is about: the cut
// for the final review, metadata.json for the publish review. Sending the same cut again is
// safe: the site answers with the review it has.
import { closeSync, existsSync, openSync, readFileSync, readSync, statSync } from 'node:fs';
import path from 'node:path';

import { readJson } from '../core/paths.mjs';
import { CHECK_FILE } from './check.mjs';
import { SCRIPT_FILE, USAGE_FILE, lineOf, sha256 } from './core.mjs';
import { DESCRIPTION_FILE, METADATA_FILE, PACKAGE_FILE, captionLocales } from './package.mjs';
import { QA_FILE, VERIFY_FILE, scriptShape } from './qa.mjs';

// Mirrors PART_BYTES in apps/api/app/video_reviews/storage.py: under nginx's 6 MB request cap.
export const PART_BYTES = 4 * 1024 * 1024;
// What the review store takes (apps/api/app/video_reviews/schemas.py ContentType); an evidence
// file of another kind goes up as plain text, which is what it is to a reader.
const TYPES = { '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.json': 'application/json', '.srt': 'application/x-subrip', '.mp4': 'video/mp4' };
const typeOf = (file) => TYPES[path.extname(file).toLowerCase()] ?? 'text/plain';
const STEPS = [
  ['built', '成片合成'],
  ['audio', '旁白檢查'],
  ['qa', '自動品管'],
  ['package', '上傳包'],
];

/** The role an evidence file is attached under: evidence_ and what is left of its path. */
export function evidenceRole(relative) {
  const name = relative.replace(/\.[A-Za-z0-9]+$/, '').replace(/[^A-Za-z0-9_-]+/g, '_').replace(/^_+|_+$/g, '');
  return `evidence_${name}`.slice(0, 40);
}

/**
 * What the site is told about the video: where it is and what has been done. It is at its
 * final cut until that is approved, whatever is ready behind it.
 */
export function projectBody({ doc, qa, check, report, stage = 'final' }) {
  const done = { built: true, audio: check?.ok === true, qa: qa?.ok === true, package: report?.ok === true };
  const line = lineOf(doc);
  return {
    title: doc.titles[0],
    stage,
    checklist: STEPS.map(([key, label]) => ({ key, label, done: done[key] })),
    // A vertical drama short keeps the drama format; what makes it a Short is its line.
    format: line === 'drama' ? 'drama' : 'shorts',
    shorts_line: line,
    shorts_series: doc.series,
    ...(doc.source?.slug ? { source_slug: doc.source.slug } : {}),
  };
}

export function qaSummary(qa) {
  if (!qa) return 'Shorts 自動品管沒有結果';
  const failed = qa.items.filter((each) => !each.ok).map((each) => each.id);
  return failed.length ? `Shorts 自動品管 ${failed.length} 項沒過：${failed.join('、')}` : `Shorts 自動品管 ${qa.items.length} 項全過`;
}

export function packageSummary(report) {
  const failed = report.items.filter((each) => !each.ok).map((each) => each.id);
  return failed.length ? `Shorts 上傳包 ${failed.length} 項沒過：${failed.join('、')}` : `Shorts 上傳包 ${report.items.length} 項齊全`;
}

/** The final review, without its files: bound to the cut, carrying the report and the usage. */
export function finalReview({ doc, qa, usage, timeline, finalSha256 }) {
  const { checked_at: _at, script: _script, ...report } = qa ?? {};
  const current = qa?.final_sha256 === finalSha256 ? report : null;
  return {
    gate: 'final',
    content_sha256: finalSha256,
    summary: `Shorts ${timeline.seconds.toFixed(1)} 秒，${qaSummary(current)}`,
    payload: {
      duration_seconds: timeline.seconds,
      line: lineOf(doc),
      series: doc.series,
      titles: doc.titles,
      script: { series: doc.series, ...scriptShape(doc) },
      ...(current ? { qa: current } : {}),
      ...(usage ? { usage } : {}),
    },
  };
}

/** The publish review, without its files: bound to metadata.json, carrying the package check. */
export function publishReview({ metadata, report, metadataSha256 }) {
  const { checked_at: _at, ...check } = report;
  return {
    gate: 'publish',
    content_sha256: metadataSha256,
    summary: check.ok ? `${packageSummary(check)}：照月曆上架` : packageSummary(check),
    payload: {
      package: check,
      locales: captionLocales(metadata),
      zh: { title: metadata.title, titles: metadata.titles, description: metadata.description, tags: metadata.tags },
      disclosure: { synthetic: metadata.contains_synthetic_media, reason: metadata.disclosure_reason },
      category_id: metadata.category_id,
      made_for_kids: metadata.made_for_kids,
      source: metadata.source,
    },
  };
}

/** Upload one file in parts unless the site has it already; returns its review file entry. */
export async function upload(client, slug, file, role) {
  const size = statSync(file).size;
  const digest = sha256(readFileSync(file));
  const parts = Math.max(1, Math.ceil(size / PART_BYTES));
  const handle = openSync(file, 'r');
  try {
    for (let part = 0; part < parts; part++) {
      const length = Math.min(PART_BYTES, size - part * PART_BYTES);
      const bytes = Buffer.alloc(length);
      readSync(handle, bytes, 0, length, part * PART_BYTES);
      const result = await client.part(slug, digest, bytes, { part: String(part), parts: String(parts), size: String(size) });
      if (result.complete) break;
    }
  } finally {
    closeSync(handle);
  }
  return { role, sha256: digest, size, content_type: typeOf(file) };
}

/**
 * Send a build directory. Returns { slug, final, publish }: each the site's review, or null when
 * it was not sent; `waits` says what the Short waits for when the package did not go.
 */
export async function push({ directory, client, log = () => {} }) {
  const doc = readJson(path.join(directory, SCRIPT_FILE), null);
  const timeline = readJson(path.join(directory, 'timeline.json'), null);
  const final = path.join(directory, 'upload', 'final.mp4');
  if (!doc || !timeline || !existsSync(final)) throw new Error(`${directory} is not a finished build`);
  const qa = readJson(path.join(directory, QA_FILE), null);
  const report = readJson(path.join(directory, PACKAGE_FILE), null);
  const slug = doc.slug;
  const metadataFile = path.join(directory, 'upload', METADATA_FILE);
  const metadata = readJson(metadataFile, null);
  const metadataSha256 = metadata ? sha256(readFileSync(metadataFile)) : null;
  if (metadata && report) {
    if (report.final_sha256 !== metadataSha256) return { slug, final: null, publish: null, waits: 'the upload package changed: run package again' };
    for (const locale of captionLocales(metadata)) {
      const file = path.join(directory, 'upload', `${locale}.srt`);
      if (!existsSync(file) || metadata.captions_sha256?.[locale] !== sha256(readFileSync(file))) {
        return { slug, final: null, publish: null, waits: 'the captions changed or have no package binding: run package again' };
      }
    }
  }
  await client.report(slug, projectBody({ doc, qa, check: readJson(path.join(directory, CHECK_FILE), null), report }));

  const files = [await upload(client, slug, final, 'preview'), await upload(client, slug, path.join(directory, 'upload', 'cover.png'), 'thumbnail')];
  const sheet = path.join(directory, 'contact-sheet.png');
  if (existsSync(sheet)) files.push(await upload(client, slug, sheet, 'contact_sheet'));
  const roles = new Set(files.map((file) => file.role));
  for (const evidence of doc.evidence ?? []) {
    const file = path.join(directory, 'evidence', evidence.path);
    let role = evidenceRole(evidence.path);
    // Two paths that shorten to the same role are told apart by the start of their hash.
    if (roles.has(role)) role = `${role.slice(0, 31)}_${evidence.sha256.slice(0, 8)}`;
    roles.add(role);
    if (existsSync(file)) files.push(await upload(client, slug, file, role));
  }
  const verify = path.join(directory, VERIFY_FILE);
  if (existsSync(verify)) files.push(await upload(client, slug, verify, 'evidence_verify'));
  const finalSha256 = files[0].sha256;
  const sent = await client.submit(slug, { ...finalReview({ doc, qa, usage: readJson(path.join(directory, USAGE_FILE), null), timeline, finalSha256 }), files });
  log(`${slug}: final review ${sent.status}${sent.note ? ` (${sent.note})` : ''}`);
  if (sent.status !== 'approved') {
    return { slug, final: sent, publish: null, waits: sent.status === 'rejected' ? `the owner sent the cut back: ${sent.note ?? ''}`.trim() : 'the final cut waits for the owner on /admin/videos' };
  }

  if (!metadata || !report) return { slug, final: sent, publish: null, waits: 'the upload package is not made yet: run package, then push again' };
  if (metadata.final_sha256 !== finalSha256) return { slug, final: sent, publish: null, waits: 'the upload package is of another cut: run package, then push again' };
  // No thumbnail goes with the package: the site sets on YouTube what the package holds, and
  // a Short's cover is its first frame. The cover the tab shows is the final review's.
  const packaged = [
    await upload(client, slug, metadataFile, 'metadata'),
    await upload(client, slug, final, 'final'),
  ];
  if (packaged[0].sha256 !== metadataSha256) return { slug, final: sent, publish: null, waits: 'the upload package changed during push: run package again' };
  for (const locale of captionLocales(metadata)) {
    const caption = await upload(client, slug, path.join(directory, 'upload', `${locale}.srt`), `captions_${locale}`);
    if (caption.sha256 !== metadata.captions_sha256[locale]) return { slug, final: sent, publish: null, waits: 'the captions changed during push: run package again' };
    packaged.push(caption);
  }
  packaged.push(await upload(client, slug, path.join(directory, 'upload', DESCRIPTION_FILE), 'description_zh-TW'));
  await client.report(slug, projectBody({ doc, qa, check: readJson(path.join(directory, CHECK_FILE), null), report, stage: 'publish' }));
  const confirmed = await client.submit(slug, { ...publishReview({ metadata, report, metadataSha256: packaged[0].sha256 }), files: packaged });
  log(`${slug}: publish review ${confirmed.status}${confirmed.note ? ` (${confirmed.note})` : ''}`);
  return { slug, final: sent, publish: confirmed, waits: confirmed.status === 'approved' ? null : 'the upload package waits for the owner on /admin/videos' };
}
