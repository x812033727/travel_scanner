// The rest of the full backup tier, sent with the upload confirmation of a video made off the host.
//
// The owner, 2026-11-03: every video has one whole copy on the host before it goes up, wherever it
// was made (docs/videos/BACKUP.md). A cloud session's 奇聞檔案局 episode reaches the host only as
// reviews, and the upload package alone lacks most of the full tier: the keyframes, narration.wav,
// timeline.json, the clips and the line recordings. `review-push --gate publish` from a work
// directory the worker did not make (no auto.json) attaches them too, as roles the site counts
// apart from a review's 48 files (apps/api/app/video_reviews/clips.py); the host's worker fetches
// the approved package into video_work/<slug>/ and lays each file back where it came from
// (tools/video/automation/review-package.mjs placeOf). Nothing that reads a package for YouTube
// looks at these roles.
import { existsSync, readdirSync, statSync } from "node:fs";
import path from "node:path";

import { packRecordings } from "../import/recordings.mjs";

// The site's limits (clips.py): keep them in step.
export const MAX_KEYFRAME_FILES = 400;
export const MAX_CLIP_FILES = 120;
// A role is at most 40 characters (schemas.py ReviewFile): kf_ and up to 37 more.
const KEYFRAME_STEM = /^[A-Za-z0-9][A-Za-z0-9_-]{0,36}$/;
const CLIP_STEM = /^[A-Za-z0-9][A-Za-z0-9_-]{0,34}$/;
const IMAGE_TYPES = { ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg" };

const isFile = (file) => {
  try {
    return statSync(file).isFile();
  } catch {
    return false;
  }
};

/**
 * The full tier's files of `workdir` beyond its upload package: [{ file, role, content_type }], and
 * the problems that leave a file out (a name no role can carry, or more files than the site takes).
 * The line recordings are packed into `<workdir>/review/recordings/` as `import` packs them.
 */
export function fullTierFiles(workdir) {
  const files = [];
  const problems = [];
  const keyframes = path.join(workdir, "keyframes");
  if (existsSync(keyframes)) {
    const images = [];
    for (const name of readdirSync(keyframes).sort()) {
      const file = path.join(keyframes, name);
      if (!isFile(file)) continue;
      if (name === "manifest.json") {
        files.push({ file, role: "keyframes_manifest", content_type: "application/json" });
        continue;
      }
      const ext = path.extname(name).toLowerCase();
      if (!IMAGE_TYPES[ext]) continue;
      const stem = name.slice(0, -ext.length);
      if (!KEYFRAME_STEM.test(stem)) {
        problems.push(`keyframes/${name}: a keyframe's name is letters, digits, - or _ and at most 37 of them`);
        continue;
      }
      images.push({ file, role: `kf_${stem}`, content_type: IMAGE_TYPES[ext] });
    }
    if (images.length > MAX_KEYFRAME_FILES) problems.push(`keyframes/: ${images.length} images; the site takes ${MAX_KEYFRAME_FILES}, so the rest stay out`);
    files.push(...images.slice(0, MAX_KEYFRAME_FILES));
  }
  const clips = path.join(workdir, "clips");
  if (existsSync(clips)) {
    const found = [];
    for (const name of readdirSync(clips).sort()) {
      if (!name.toLowerCase().endsWith(".mp4") || !isFile(path.join(clips, name))) continue;
      const stem = name.slice(0, -4);
      if (!CLIP_STEM.test(stem)) {
        problems.push(`clips/${name}: a clip's name is letters, digits, - or _ and at most 35 of them`);
        continue;
      }
      found.push({ file: path.join(clips, name), role: `clip_${stem}`, content_type: "video/mp4" });
    }
    if (found.length > MAX_CLIP_FILES) problems.push(`clips/: ${found.length} clips; the site takes ${MAX_CLIP_FILES}, so the rest stay out`);
    files.push(...found.slice(0, MAX_CLIP_FILES));
  }
  const narration = path.join(workdir, "narration.wav");
  if (isFile(narration)) files.push({ file: narration, role: "full_narration", content_type: "audio/wav" });
  const timeline = path.join(workdir, "timeline.json");
  if (isFile(timeline)) files.push({ file: timeline, role: "full_timeline", content_type: "application/json" });
  const recordings = packRecordings(workdir, path.join(workdir, "review", "recordings"));
  problems.push(...recordings.problems.map((problem) => `line recordings: ${problem}`));
  files.push(...recordings.files);
  return { files, problems };
}
