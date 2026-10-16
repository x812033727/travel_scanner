import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";
import sharp from "sharp";

import { openRenderer } from "../../../../../tools/video/render/browser.mjs";
import { sceneProblems, slideHtml } from "../../../../../tools/video/templates/templates.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, "../../../../..");
const source = path.resolve(here, "../B18-authored-chapters-candidate");
const ideaPath = path.join(source, "chapters/idea.json");
const videoPath = path.join(source, "synthetic/docroot/docs/videos/story-conveyor-belt-sushi-v2/video.json");
const themePath = path.join(root, "tools/video/templates/theme.css");
const variant = JSON.parse(readFileSync(path.join(here, "variant.json"), "utf8"));
const sha = (value) => createHash("sha256").update(value).digest("hex");
const ideaBytes = readFileSync(ideaPath);
const videoBytes = readFileSync(videoPath);
assert.equal(sha(ideaBytes), variant.source_idea_sha256, "source idea changed");
assert.equal(sha(videoBytes), variant.source_video_sha256, "source video changed");
assert.equal(sha(readFileSync(themePath)), "ae26b5b6c920b2d2cfffa45bdc0c181a996c7cd3689cc9769d6186875df360c5", "slide theme changed");

const idea = JSON.parse(ideaBytes);
const video = JSON.parse(videoBytes);
for (const doc of [idea, video]) {
  const scene = doc.scenes.find(({ id }) => id === variant.scene_id);
  assert.ok(scene, "scene missing");
  assert.equal(scene.template, "title");
  assert.equal(scene.data.title, variant.title);
  assert.equal(scene.data.tag, variant.tag);
  assert.equal(scene.data.subtitle, variant.before_subtitle);
  scene.data.subtitle = variant.after_subtitle;
}
const ideaOut = Buffer.from(`${JSON.stringify(idea, null, 2)}\n`);
const videoOut = Buffer.from(`${JSON.stringify(video, null, 2)}\n`);
const outputDir = path.join(os.tmpdir(), "brand-b18-mobile-card-revision-20261016");
mkdirSync(outputDir, { recursive: true });
writeFileSync(path.join(outputDir, "idea.json"), ideaOut);
writeFileSync(path.join(outputDir, "video.json"), videoOut);

const scene = video.scenes.find(({ id }) => id === variant.scene_id);
assert.deepEqual(sceneProblems(scene), [], "revised card schema");
const state = { reveal: 0, previousReveal: 0, first: true, totalReveals: 0, chapter: null, chapterNumber: 0, chapterCount: 0 };
const renderer = await openRenderer({ root, channel: process.env.VIDEO_BROWSER_CHANNEL || "msedge" });
try {
  const frame = await renderer.capture("b18a027", slideHtml(scene, state));
  assert.deepEqual(frame.problems, [], "revised card renderer");
  const mobile = await sharp(frame.still).resize(320, 180).png().toBuffer();
  writeFileSync(path.join(outputDir, "idea-s027-1920x1080.png"), frame.still);
  writeFileSync(path.join(outputDir, "idea-s027-320x180.png"), mobile);
  const report = {
    source_idea_sha256: sha(ideaBytes), source_video_sha256: sha(videoBytes),
    revised_idea_sha256: sha(ideaOut), revised_video_sha256: sha(videoOut),
    mobile_png_sha256: sha(mobile), full_png_sha256: sha(frame.still),
    renderer_problems: frame.problems, change: { scene_id: variant.scene_id, field: "data.subtitle", before: variant.before_subtitle, after: variant.after_subtitle },
  };
  writeFileSync(path.join(outputDir, "report.json"), `${JSON.stringify(report, null, 2)}\n`);
  process.stdout.write(`${JSON.stringify(report, null, 2)}\n`);
} finally {
  await renderer.close();
}
