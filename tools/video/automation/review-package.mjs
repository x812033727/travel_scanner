// An off-host video's upload package, fetched from the site's review store into video_work so the
// Drive backup (backup.mjs, docs/videos/BACKUP.md) can copy it.
//
// Since 2026-11-03 also a video sent by hand with `review-push` (payload `hand_pushed`: a cloud
// session's 奇聞檔案局 episodes) and the newest approved language batch of either kind
// (`review-push --gate languages`: dub tracks, captions, descriptions and per-language thumbnails
// approved after the upload confirmation). The owner wants a whole copy of every video on the host
// before it goes up; the site names both reviews in `review_package` (apps/api/app/video_backup).
// Such a package also carries the rest of the full tier (tools/video/review/full-tier.mjs): each
// keyframe (`kf_<name>`), keyframes/manifest.json, narration.wav and timeline.json, placed back
// where they came from.
//
// `import --publish` (tools/video/import/import.mjs) runs where the video was made, a cloud
// session's Colab drama for one, and sends the package to the review store: metadata.json, the
// 1080p cut, the thumbnail, the captions and dub tracks, and since 2026-10-31 the episode's
// per-shot clips (`clip_<shot>`). None of it reaches this host's video_work/<slug>/, and the
// backup copies only what that folder holds, so an imported video was never backed up. The site
// now names, for each imported video it lists for the backup, its approved package
// (`review_package`: review id and metadata.json's SHA-256; apps/api/app/video_backup). Before the
// backup looks at the video, this fetches that package with the video tool token (the route
// `review-files` uses), checks every file's SHA-256 and size against the review, and lays it out
// as `package` would: upload/final.mp4, upload/metadata.json, upload/thumbnail.<ext>,
// upload/captions/<l>.srt, upload/dubs/<l>.<ext>, upload/description.<l>.txt (written from
// metadata.json) and clips/<shot>.mp4. The full tier then copies clips/ with the rest.
//
// Written to touch as little as it can: never a folder the worker made (auto.json) or one made by
// hand (it exists without this file's record), only the files a package it fetched placed, and a
// renewed package replaces only those. A file the store no longer holds (its mp4s go a week after
// YouTube) is recorded as gone and the backup copies the rest; the site then lists what is missing.
import { createHash } from "node:crypto";
import { createReadStream, existsSync, mkdirSync, readFileSync, renameSync, rmSync, statSync, writeFileSync } from "node:fs";
import path from "node:path";

import { atomicWrite, readJson } from "../core/paths.mjs";

export const PACKAGE_RECORD = "review-package.json";
const PARTIAL_DIR = "review-package.partial";
// The site lets a video tool token read 600 files an hour (apps/api/app/video_reviews/admin_api.py
// DOWNLOADS_PER_HOUR); twelve rounds an hour of at most this many stay under it.
export const DOWNLOADS_PER_ROUND = 40;
const SHA256 = /^[0-9a-f]{64}$/;
const LOCALE = /^[A-Za-z]{2,3}(?:-[A-Za-z0-9]{2,8})?$/;
const NAME = /^[A-Za-z0-9][A-Za-z0-9_-]{0,34}$/;
// A keyframe's name as review-push sends it (tools/video/review/full-tier.mjs): kf_ and up to 37 more.
const KEYFRAME = /^[A-Za-z0-9][A-Za-z0-9_-]{0,36}$/;
const IMAGE = { "image/png": "png", "image/jpeg": "jpg" };
const AUDIO = { "audio/mp4": "m4a", "audio/mpeg": "mp3", "audio/wav": "wav" };
const CAPTION = { "application/x-subrip": "srt", "text/vtt": "vtt" };
// `review-push` sends captions as text/plain (tools/video/package/check.mjs packageFiles): SubRip.
const PLAIN_CAPTION = "text/plain";
// A dub role as tools/video/core/stages.mjs dubRole writes it: the locale lowercased with `_` for
// `-` (dub_pt, dub_pt_br). Read back as the locale package names files by (pt, pt-BR).
const ROLE_LOCALE = /^([a-z]{2,3})(?:_([a-z0-9]{2,8}))?$/;
function localeOfRole(rest) {
  if (LOCALE.test(rest)) return rest;
  const match = ROLE_LOCALE.exec(rest);
  if (!match) return null;
  return match[2] ? `${match[1]}-${match[2].length === 2 ? match[2].toUpperCase() : match[2]}` : match[1];
}

/**
 * Where a package file goes in the work directory, relative to it, as `package` lays it out; null
 * for a role this does not place (a file the backup would not count, or a name it cannot trust).
 */
export function placeOf(role, contentType) {
  const r = String(role);
  if (r === "metadata") return contentType === "application/json" ? "upload/metadata.json" : null;
  if (r === "final") return contentType === "video/mp4" ? "upload/final.mp4" : null;
  if (r === "thumbnail" && IMAGE[contentType]) return `upload/thumbnail.${IMAGE[contentType]}`;
  const variant = /^thumbnail-([a-z])$/.exec(r);
  if (variant && IMAGE[contentType]) return `upload/thumbnail-${variant[1]}.${IMAGE[contentType]}`;
  const [prefix, rest] = [r.slice(0, r.indexOf("_") + 1), r.slice(r.indexOf("_") + 1)];
  if (prefix === "clip_") return NAME.test(rest) && contentType === "video/mp4" ? `clips/${rest}.mp4` : null;
  // The rest of the full tier a package made off the host carries (review-push, full-tier.mjs):
  // each back where it came from in the work directory.
  if (r.startsWith("kf_")) {
    const name = r.slice(3);
    return KEYFRAME.test(name) && IMAGE[contentType] ? `keyframes/${name}.${IMAGE[contentType]}` : null;
  }
  if (r === "keyframes_manifest") return contentType === "application/json" ? "keyframes/manifest.json" : null;
  if (r === "full_narration") return contentType === "audio/wav" ? "narration.wav" : null;
  if (r === "full_timeline") return contentType === "application/json" ? "timeline.json" : null;
  // The line recordings (tools/video/import/recordings.mjs): one wav a locale and the manifest that
  // cuts them back into the original line files (`node tools/video/import/recordings.mjs unpack`).
  if (r === "recordings_manifest") return contentType === "application/json" ? "recordings/manifest.json" : null;
  if (prefix === "recording_") return LOCALE.test(rest) && contentType === "audio/wav" ? `recordings/${rest}.wav` : null;
  // A language batch's dub track the check gave up on (uncheckedDubRole): the owner may still
  // upload it by hand, so it goes where the worker keeps its own tracks, outside the package; the
  // full tier backs it up under dubs/未進上傳包/ (backup.mjs planFiles).
  if (r.startsWith("dub_unchecked_")) {
    const locale = localeOfRole(r.slice("dub_unchecked_".length));
    return locale && AUDIO[contentType] ? `dubs/${locale}.${AUDIO[contentType]}` : null;
  }
  if (prefix === "dub_") {
    const locale = localeOfRole(rest);
    return locale && AUDIO[contentType] ? `upload/dubs/${locale}.${AUDIO[contentType]}` : null;
  }
  if (!LOCALE.test(rest)) return null;
  if (prefix === "captions_" && contentType === PLAIN_CAPTION) return `upload/captions/${rest}.srt`;
  if (prefix === "captions_" && CAPTION[contentType]) return `upload/captions/${rest}.${CAPTION[contentType]}`;
  if (prefix === "description_" && contentType === "text/plain") return `upload/description.${rest}.txt`;
  if (prefix === "thumbnail_" && contentType === "image/jpeg") return `upload/thumbnails/${rest}.jpg`;
  return null;
}

/** The package's description files from metadata.json: zh-TW's title and description, and each localization's. */
export function descriptionsOf(metadata) {
  const out = {};
  const write = (locale, entry) => {
    if (LOCALE.test(locale) && typeof entry?.title === "string" && typeof entry?.description === "string") {
      out[`upload/description.${locale}.txt`] = `${entry.title}\n\n${entry.description}\n`;
    }
  };
  write(typeof metadata?.default_language === "string" ? metadata.default_language : "zh-TW", metadata);
  const localizations = metadata?.localizations;
  if (localizations && typeof localizations === "object" && !Array.isArray(localizations)) {
    for (const [locale, entry] of Object.entries(localizations)) write(locale, entry);
  }
  return out;
}

function sha256File(file) {
  return new Promise((resolve, reject) => {
    const hash = createHash("sha256");
    createReadStream(file).on("error", reject).on("data", (chunk) => hash.update(chunk)).on("end", () => resolve(hash.digest("hex")));
  });
}

async function holds(file, entry) {
  try {
    return statSync(file).size === entry.size && (await sha256File(file)) === entry.sha256;
  } catch {
    return false;
  }
}

/** Remove a file this module placed, never through `..` or outside the work directory. */
function removePlaced(workdir, relative) {
  const file = path.resolve(workdir, relative);
  if (!file.startsWith(path.resolve(workdir) + path.sep)) return;
  rmSync(file, { force: true });
}

/**
 * Fetch `video.review_package` into the video's work directory, or say why not. Returns null when
 * there is nothing to do, else { line, downloads, complete }. `budget` is how many files this
 * round may still download. Throws only what the caller logs: a site that cannot be reached.
 */
export async function fetchReviewPackage({ base, video, client, budget = DOWNLOADS_PER_ROUND, now = new Date() }) {
  const wanted = video?.review_package;
  if (!wanted || typeof wanted.review_id !== "string" || !SHA256.test(String(wanted.content_sha256))) return null;
  // The newest approved language batch, when the site names one.
  const batch = typeof wanted.languages_review_id === "string" && SHA256.test(String(wanted.languages_sha256)) ? { review_id: wanted.languages_review_id, content_sha256: wanted.languages_sha256 } : null;
  const workdir = path.join(base, video.slug);
  if (existsSync(path.join(workdir, "auto.json"))) return null;
  const record = readJson(path.join(workdir, PACKAGE_RECORD), null);
  if (existsSync(workdir) && !record) return null; // made here by hand: never written over
  if (record?.complete && record.review_id === wanted.review_id && (record.languages_review_id ?? null) === (batch?.review_id ?? null)) return null;
  if (budget <= 0) return { line: `backup: ${video.slug}: its upload package waits for the next round`, downloads: 0, complete: false };

  const project = await client.project(video.slug);
  const reviews = project?.reviews ?? [];
  const named = (wantedReview, gate) => {
    const review = reviews.find((each) => String(each.id) === wantedReview.review_id);
    return review && review.gate === gate && review.status === "approved" && review.content_sha256 === wantedReview.content_sha256 ? review : null;
  };
  const review = named(wanted, "publish");
  if (!review) {
    return { line: `backup: ${video.slug}: the site no longer has the approved upload package it named; the next round asks again`, downloads: 0, complete: false };
  }
  const languages = batch ? named(batch, "languages") : null;
  if (batch && !languages) {
    return { line: `backup: ${video.slug}: the site no longer has the approved language batch it named; the next round asks again`, downloads: 0, complete: false };
  }
  // The package's files, then the language batch's: approved after it, the batch's dub track,
  // captions and descriptions take the place of the package's own for the same language.
  const byPlace = new Map();
  for (const item of [...(review.files ?? []), ...(languages?.files ?? [])]) {
    const where = placeOf(item?.role, item?.content_type);
    if (!where || !SHA256.test(String(item.sha256)) || !(Number(item.size) > 0)) continue;
    byPlace.set(where, { role: item.role, path: where, sha256: item.sha256, size: Number(item.size) });
  }
  const files = [...byPlace.values()];
  const places = new Set(byPlace.keys());
  const batchIds = batch ? { languages_review_id: batch.review_id, languages_sha256: batch.content_sha256 } : {};
  // A record before the first file: the folder is this module's from now on, and the backup waits.
  mkdirSync(workdir, { recursive: true });
  const started = { schema_version: 1, review_id: wanted.review_id, content_sha256: wanted.content_sha256, ...batchIds, complete: false, started_at: now.toISOString(), files: record?.files ?? [], written: record?.written ?? [] };
  atomicWrite(path.join(workdir, PACKAGE_RECORD), `${JSON.stringify(started, null, 2)}\n`);

  const partial = path.join(workdir, PARTIAL_DIR);
  mkdirSync(partial, { recursive: true });
  let downloads = 0;
  const gone = [];
  for (const entry of files) {
    const target = path.join(workdir, entry.path);
    if (await holds(target, entry)) continue;
    if (downloads >= budget) {
      return { line: `backup: ${video.slug}: fetched ${downloads} file(s) of its upload package; the rest next round`, downloads, complete: false };
    }
    const part = path.join(partial, entry.sha256);
    downloads += 1;
    try {
      await client.download(video.slug, entry.sha256, part);
    } catch (error) {
      rmSync(part, { force: true });
      if (error?.status === 404) {
        gone.push(entry.path);
        continue;
      }
      return { line: `backup: ${video.slug}: ${entry.path} could not be fetched (${error.message}); the next round goes on`, downloads, complete: false };
    }
    if (!(await holds(part, entry))) {
      rmSync(part, { force: true });
      return { line: `backup: ${video.slug}: ${entry.path} did not match the review's SHA-256 and size; the next round fetches it again`, downloads, complete: false };
    }
    mkdirSync(path.dirname(target), { recursive: true });
    renameSync(part, target);
  }
  rmSync(partial, { recursive: true, force: true });

  // The description files package writes, from the approved metadata.json, unless the package has its own.
  let written = [];
  const metadataFile = path.join(workdir, "upload", "metadata.json");
  if (!gone.includes("upload/metadata.json") && existsSync(metadataFile)) {
    let metadata = null;
    try {
      metadata = JSON.parse(readFileSync(metadataFile, "utf8"));
    } catch {
      metadata = null;
    }
    for (const [where, text] of Object.entries(descriptionsOf(metadata))) {
      if (places.has(where)) continue;
      mkdirSync(path.dirname(path.join(workdir, where)), { recursive: true });
      writeFileSync(path.join(workdir, where), text);
      written.push(where);
    }
  }
  // A renewed package: what the earlier one placed and this one does not name goes from here
  // (Drive keeps it; the backup never deletes there).
  const kept = new Set([...files.map((entry) => entry.path), ...written]);
  for (const old of [...(record?.files ?? []).map((entry) => entry.path), ...(record?.written ?? [])]) {
    if (typeof old === "string" && !kept.has(old)) removePlaced(workdir, old);
  }
  written = written.sort();
  const done = { schema_version: 1, review_id: wanted.review_id, content_sha256: wanted.content_sha256, ...batchIds, complete: true, fetched_at: now.toISOString(), files: files.filter((entry) => !gone.includes(entry.path)), written, gone };
  atomicWrite(path.join(workdir, PACKAGE_RECORD), `${JSON.stringify(done, null, 2)}\n`);
  const clips = done.files.filter((entry) => entry.path.startsWith("clips/")).length;
  return {
    line: `backup: ${video.slug}: fetched its upload package${batch ? " and language batch" : ""} from the site (${done.files.length} file(s), ${clips} clip(s))${gone.length ? `; no longer in the review store: ${gone.slice(0, 3).join(", ")}${gone.length > 3 ? ", …" : ""}` : ""}`,
    downloads,
    complete: true,
  };
}

/** Whether a work directory holds a package this module is still fetching: the backup waits for it. */
export function packageIncomplete(workdir) {
  const record = readJson(path.join(workdir, PACKAGE_RECORD), null);
  return Boolean(record) && record.complete !== true;
}

/** Whether a work directory holds a package this module fetched. */
export function packageFetched(workdir) {
  return readJson(path.join(workdir, PACKAGE_RECORD), null)?.complete === true;
}
