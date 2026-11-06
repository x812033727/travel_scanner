// An imported drama episode's build data: what a later re-cut needs besides the clips and the line
// recordings (tasks/open/2026-11-04-zhong-tian-an-imported-drama-episode.md).
//
// The workdir that made an episode (zhong-tian-qu-qi-eNNN-dh/) keeps them next to clips/ and audio/,
// and they go with the cloud container unless the upload package carries them (owner, 2026-11-05:
// "以後備份也要一起備份"):
//
//   cut/*.log           final.log (which take each shot used, where it starts, how long, any hold)
//                       and dub-<locale>.log (each dubbed line's length and tempo)
//   music/*.mp3|wav     the music cues the cut used; a regenerated cue is a different piece
//   first-frames/*      the paid first frames a clip was made from (sNN-tK.png)
//   edit*.json          the edit table the cut was made with (or `--edit FILE`)
//
// Roles: build_log-<name> (text/plain), build_music-<name> (audio/mpeg or audio/wav) and
// build_edit-<name> (application/json), placed by the host's worker under recut/ in the episode's
// work directory (tools/video/automation/review-package.mjs placeOf), so the full-tier backup keeps
// recut/cut/, recut/music/ and recut/<edit>.json; the first frames go as kf_<name> keyframes, which
// the site already takes, into keyframes/. All are backup-tier roles (apps/api/app/video_reviews/
// clips.py): nothing that uploads or shows a package reads them.
import { createHash } from "node:crypto";
import { existsSync, readdirSync, readFileSync, statSync } from "node:fs";
import path from "node:path";

// The site's limits (apps/api/app/video_reviews/clips.py MAX_BUILD_FILES, MAX_KEYFRAME_FILES).
export const MAX_BUILD_FILES = 40;
export const MAX_FIRST_FRAMES = 400;
// A build role's name: build_<kind>- and 1–28 more (the site keeps a role to 40 characters, schemas.py
// ReviewFile); no dots or slashes, so it cannot climb out of recut/.
export const BUILD_NAME = /^[A-Za-z0-9][A-Za-z0-9_-]{0,27}$/;
// A keyframe's name as the site keeps it (review-package.mjs KEYFRAME).
const KEYFRAME_NAME = /^[A-Za-z0-9][A-Za-z0-9_-]{0,36}$/;
const MUSIC = { ".mp3": "audio/mpeg", ".wav": "audio/wav" };
const IMAGE = { ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg" };
// A log or an edit table bigger than this is not one (a final.log is a few kB).
const MAX_TEXT_BYTES = 2 * 1024 * 1024;

const filesIn = (dir) => (existsSync(dir) && statSync(dir).isDirectory() ? readdirSync(dir).sort().filter((name) => statSync(path.join(dir, name)).isFile()) : []);

/**
 * The build data in an episode's workdir, as the files an upload package carries:
 * { files: [{ file, role, content_type }], firstFrames: [...same], problems, counts }.
 * `edit` names the edit table when it is not an edit*.json in the workdir itself; given and missing is a mistake.
 */
export function buildFiles(episodeDir, { edit = null } = {}) {
  const problems = [];
  const files = [];
  const firstFrames = [];
  if (!episodeDir || !existsSync(episodeDir)) return { files, firstFrames, problems, counts: { logs: 0, music: 0, edit: 0, firstFrames: 0 } };
  const named = (kind, stem, file, contentType, where) => {
    if (!BUILD_NAME.test(stem)) problems.push(`${where}: a name is 1–28 letters, digits, - or _`);
    else files.push({ file, role: `build_${kind}-${stem}`, content_type: contentType });
  };
  const text = (file, where) => {
    if (statSync(file).size > MAX_TEXT_BYTES) {
      problems.push(`${where} is ${statSync(file).size} bytes; a build file is at most ${MAX_TEXT_BYTES}`);
      return false;
    }
    return true;
  };

  for (const name of filesIn(path.join(episodeDir, "cut"))) {
    if (!name.endsWith(".log")) continue;
    const file = path.join(episodeDir, "cut", name);
    if (text(file, `cut/${name}`)) named("log", name.slice(0, -4), file, "text/plain", `cut/${name}`);
  }
  for (const name of filesIn(path.join(episodeDir, "music"))) {
    const ext = path.extname(name).toLowerCase();
    if (MUSIC[ext]) named("music", name.slice(0, -ext.length), path.join(episodeDir, "music", name), MUSIC[ext], `music/${name}`);
  }
  const editFiles = edit !== null ? [edit] : filesIn(episodeDir).filter((name) => /^edit[A-Za-z0-9_-]*\.json$/.test(name)).map((name) => path.join(episodeDir, name));
  if (edit !== null && !existsSync(edit)) problems.push(`--edit ${edit} does not exist`);
  else {
    for (const file of editFiles) {
      const name = path.basename(file);
      if (!name.toLowerCase().endsWith(".json")) { problems.push(`${name}: an edit table is a .json file`); continue; }
      if (!text(file, name)) continue;
      try {
        JSON.parse(readFileSync(file, "utf8"));
      } catch {
        problems.push(`${name}: not JSON`);
        continue;
      }
      named("edit", name.slice(0, -5), file, "application/json", name);
    }
  }
  for (const name of filesIn(path.join(episodeDir, "first-frames"))) {
    const ext = path.extname(name).toLowerCase();
    if (!IMAGE[ext]) continue;
    const stem = name.slice(0, -ext.length);
    if (!KEYFRAME_NAME.test(stem)) problems.push(`first-frames/${name}: a name is 1–37 letters, digits, - or _`);
    else firstFrames.push({ file: path.join(episodeDir, "first-frames", name), role: `kf_${stem}`, content_type: IMAGE[ext] });
  }
  const roles = new Set();
  for (const item of [...files, ...firstFrames]) {
    if (roles.has(item.role)) problems.push(`two files would both be ${item.role} (${path.basename(item.file)})`);
    roles.add(item.role);
  }
  if (files.length > MAX_BUILD_FILES) problems.push(`${files.length} build files; the site takes ${MAX_BUILD_FILES}`);
  if (firstFrames.length > MAX_FIRST_FRAMES) problems.push(`${firstFrames.length} first frames; the site takes ${MAX_FIRST_FRAMES}`);
  const count = (kind) => files.filter((item) => item.role.startsWith(`build_${kind}-`)).length;
  return { files, firstFrames, problems, counts: { logs: count("log"), music: count("music"), edit: count("edit"), firstFrames: firstFrames.length } };
}

/** One sha256 over every build file's name and bytes, so a package sent again with other build data is a new review. */
export function buildDigest(items) {
  const hash = createHash("sha256");
  for (const item of [...items].sort((a, b) => a.role.localeCompare(b.role))) {
    hash.update(`${item.role}\n`);
    hash.update(createHash("sha256").update(readFileSync(item.file)).digest("hex"));
    hash.update("\n");
  }
  return hash.digest("hex");
}

/** What the import says it left out: the build data a drama episode should have and this one lacks. */
export function missingBuild(counts) {
  const missing = [];
  if (!counts.logs) missing.push("cut/final.log");
  if (!counts.music) missing.push("music/");
  if (!counts.edit) missing.push("the edit table (edit*.json or --edit FILE)");
  return missing;
}
