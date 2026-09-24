// What to draw: every slide state of every scene as HTML, with a content key for the frame cache.
//
// The states come from the same timeline code the audio uses (tools/video/core/timeline.mjs), so
// the assemble stage can pair each state here with its start and end frame by position. The key
// hashes the HTML and the stylesheet, so a frame is redrawn exactly when what it shows changes.
import { createHash } from "node:crypto";
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";

import { estimateTimeline } from "../core/timeline.mjs";
import { sceneProblems, slideHtml, thumbnailHtml, thumbnailProblems, visibleText } from "../templates/templates.mjs";

export const THEME_FILE = fileURLToPath(new URL("../templates/theme.css", import.meta.url));
// Chapter cards and the title card say where they are themselves; a label on top would repeat it.
const NO_CHAPTER_LABEL = new Set(["title", "chapter"]);

const hash = (...parts) => {
  const digest = createHash("sha256");
  for (const part of parts) digest.update(part);
  return digest.digest("hex").slice(0, 16);
};

export function themeHash(css = readFileSync(THEME_FILE, "utf8")) {
  return hash(css);
}

/** Template data problems for the whole video, labelled like lint's. */
export function renderProblems(doc) {
  const problems = [];
  doc.scenes.forEach((scene, index) => {
    for (const message of sceneProblems(scene)) problems.push({ path: `scenes[${index}] (${scene.id}).data`, message });
  });
  for (const message of thumbnailProblems(doc.thumbnail)) problems.push({ path: "thumbnail", message });
  return problems;
}

/**
 * Every state to draw. Returns { scenes: [{ id, states: [{ reveal, first, html, key, text }] }], thumbnail }.
 * `theme` is the stylesheet's hash, part of every key.
 */
export function renderPlan(doc, theme = themeHash()) {
  const timeline = estimateTimeline(doc);
  let chapter = null;
  let chapterNumber = 0;
  const scenes = doc.scenes.map((scene, index) => {
    if (scene.chapter) {
      chapter = scene.chapter;
      chapterNumber += 1;
    }
    const totalReveals = scene.lines.reduce((sum, line) => sum + (line.reveal ?? 0), 0);
    const states = timeline.scenes[index].states.map((state, stateIndex, all) => {
      const html = slideHtml(scene, {
        reveal: state.reveal,
        previousReveal: stateIndex ? all[stateIndex - 1].reveal : 0,
        first: stateIndex === 0,
        totalReveals,
        chapter: NO_CHAPTER_LABEL.has(scene.template) ? null : chapter,
        chapterNumber,
      });
      return { reveal: state.reveal, first: stateIndex === 0, html, key: hash(theme, html), text: visibleText(html) };
    });
    return { id: scene.id, template: scene.template, states };
  });
  let thumbnail = null;
  if (doc.thumbnail) {
    const html = thumbnailHtml(doc.thumbnail);
    thumbnail = { html, key: hash(theme, html), text: visibleText(html) };
  }
  return { scenes, thumbnail };
}

// Relative to the work directory, with forward slashes so the manifest reads the same everywhere.
export const stillFile = (key) => `frames/${key}.png`;
export const transitionFile = (key, index) => `frames/${key}-t${String(index).padStart(2, "0")}.png`;
