// What to draw: every slide state of every scene as HTML, with a content key for the frame cache.
//
// The states come from the same timeline code the audio uses (tools/video/core/timeline.mjs), so
// the assemble stage can pair each state here with its start and end frame by position. The key
// hashes the HTML and the stylesheet, so a frame is redrawn exactly when what it shows changes.
import { createHash } from "node:crypto";
import { existsSync, readFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

import { isExplainer, isShot } from "../core/drama.mjs";
import { LOCALES, narrationLocale } from "../core/schema.mjs";
import { localizedThumbnail, localizedThumbnailHash, thumbnailGap } from "../core/translations.mjs";

/** The series whose own thumbnail a video wears (templates.mjs THUMB_SERIES), or null. */
export const thumbnailSeries = (doc) => (isExplainer(doc) ? "sothatswhy" : null);
import { estimateTimeline } from "../core/timeline.mjs";
import { screencastHtml, screencastPlan } from "../screencast/scene.mjs";
import { isScreencast, screencastSceneProblems } from "../screencast/steps.mjs";
import { isStockPath, ORIGIN, sceneProblems, slideHtml, svgProblems, thumbnailHtml, thumbnailProblems, thumbnailVariants, visibleText } from "../templates/templates.mjs";

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

/**
 * The files a scene draws: its diagram or its screenshot, as a repository path or a stock photo's
 * work-directory path (stock/<sha256>.<ext>, templates.mjs isStockPath).
 */
export function sceneAssets(scene) {
  if (scene.template === "diagram" && typeof scene.data?.svg === "string") return [scene.data.svg];
  if (scene.template === "screenshot" && typeof scene.data?.image === "string") return [scene.data.image];
  return [];
}

/** Where an asset is read: a stock photo under the work directory (null without one), anything else under the repository. */
export function assetFile(asset, { root, workdir = null }) {
  if (isStockPath(asset)) return workdir ? path.join(workdir, asset) : null;
  return path.join(root, asset);
}

/**
 * Template data problems for the whole video, labelled like lint's. With `root`, also the asset
 * files: they must exist, and an SVG must not script or reach the network. A stock photo must be
 * listed in assets[] (that is where the description's credit comes from; `stock fetch` writes the
 * entry) and, with `workdir`, be fetched into it. A drama's shots are generated clips, not
 * slides: lint checks their prompts and the media stages draw them.
 */
export function renderProblems(doc, root = null, { workdir = null } = {}) {
  const problems = [];
  const listed = (asset) => (Array.isArray(doc.assets) ? doc.assets : []).some((entry) => entry?.path === asset);
  doc.scenes.forEach((scene, index) => {
    if (isShot(scene)) return;
    const where = `scenes[${index}] (${scene.id}).data`;
    const own = isScreencast(scene) ? screencastSceneProblems(scene) : sceneProblems(scene);
    for (const message of own) problems.push({ path: where, message });
    if (own.length) return;
    for (const asset of sceneAssets(scene)) {
      if (isStockPath(asset)) {
        if (!listed(asset)) problems.push({ path: where, message: `${asset} is not in assets[]: stock fetch writes the entry there, and without it the description carries no credit` });
        if (workdir && !existsSync(path.join(workdir, asset))) problems.push({ path: where, message: `${asset} is not in the work directory; fetch it with stock fetch (tools/video/media/cli.mjs)` });
        continue;
      }
      if (!root) continue;
      const file = path.join(root, asset);
      if (!existsSync(file)) problems.push({ path: where, message: `${asset} does not exist` });
      else if (asset.endsWith(".svg")) for (const message of svgProblems(readFileSync(file, "utf8"))) problems.push({ path: where, message: `${asset}: ${message}` });
    }
  });
  for (const message of thumbnailProblems(doc.thumbnail, { series: thumbnailSeries(doc) })) problems.push({ path: "thumbnail", message });
  // A variant's own background must be a shot too (A's is checked with the drama's shots).
  const shots = new Set(doc.scenes.filter(isShot).map((scene) => scene.id));
  for (const { id, thumbnail } of thumbnailVariants(doc.thumbnail)) {
    const shot = thumbnail.data.shot;
    if (shot !== undefined && shot !== doc.thumbnail.data?.shot && !shots.has(shot)) problems.push({ path: "thumbnail", message: `variant ${id}: data.shot "${shot}" is not a shot of this video` });
  }
  return problems;
}

/**
 * Every state to draw. Returns { scenes: [{ id, kind, states: [{ reveal, first, html, key, text }] }], thumbnail }.
 * `theme` is the stylesheet's hash, part of every key; with `root`, diagrams are inlined and each
 * asset's bytes are part of its scene's keys, so replacing an image redraws the slides that show it.
 * A stock photo's bytes are read from `workdir` (stock/<sha256>.<ext>), so a swapped photo
 * redraws its slide too; without `workdir` the photo is not read and not part of the key.
 * A drama's shots come back as `{ kind: "clip", states: [] }`: the clips stage supplies their
 * pictures. `keyframes` maps a shot id to its drawn keyframe `{ file, sha256 }` (the keyframes
 * manifest's `shots`); a thumbnail that names a shot uses that picture as its background, and the
 * picture's hash is part of the thumbnail's key. Without the keyframe, `thumbnail.keyframe` is
 * null and the caller says what to run first. `screencasts` maps a screencast scene's id to its
 * capture manifest (tools/video/screencast/capture.mjs); each state shows one capture, and the
 * captures' hashes are part of its key. With `translations` (locale to i18n file), every other
 * caption locale whose thumbnail words are current gets its own thumbnail in
 * `thumbnail.locales` ({ locale, file, hash, html, key, text }), the same picture and layout with
 * its words; `thumbnail.gaps` says why each other locale has none.
 */
export function renderPlan(doc, theme = themeHash(), root = null, { keyframes = {}, screencasts = {}, translations = null, workdir = null } = {}) {
  const timeline = estimateTimeline(doc);
  const chapterCount = doc.scenes.filter((scene) => scene.chapter).length;
  let chapter = null;
  let chapterNumber = 0;
  const scenes = doc.scenes.map((scene, index) => {
    if (scene.chapter) {
      chapter = scene.chapter;
      chapterNumber += 1;
    }
    if (isShot(scene)) return { id: scene.id, template: scene.template, kind: "clip", states: [] };
    if (isScreencast(scene)) {
      const states = screencastStates(scene, timeline.scenes[index].states, screencasts[scene.id], theme, { chapter, chapterNumber, chapterCount });
      return { id: scene.id, template: scene.template, kind: "stills", states };
    }
    const totalReveals = scene.lines.reduce((sum, line) => sum + (line.reveal ?? 0), 0);
    const assets = root ? sceneAssets(scene).map((asset) => assetFile(asset, { root, workdir })).filter(Boolean).map((file) => readFileSync(file)) : [];
    const assetHash = hash(...assets);
    const svg = scene.template === "diagram" && assets.length ? assets[0].toString("utf8") : undefined;
    const states = timeline.scenes[index].states.map((state, stateIndex, all) => {
      const html = slideHtml(scene, {
        svg,
        reveal: state.reveal,
        previousReveal: stateIndex ? all[stateIndex - 1].reveal : 0,
        first: stateIndex === 0,
        totalReveals,
        chapter: NO_CHAPTER_LABEL.has(scene.template) ? null : chapter,
        chapterNumber,
        chapterCount,
      });
      return { reveal: state.reveal, first: stateIndex === 0, html, key: hash(theme, html, assetHash), text: visibleText(html) };
    });
    return { id: scene.id, template: scene.template, kind: "stills", states };
  });
  // `locale` is a caption locale's own thumbnail, which may be set in its own font (fonts.mjs).
  const drawThumbnail = (own, locale = null) => {
    const shot = typeof own.data?.shot === "string" ? own.data.shot : null;
    const keyframe = shot && keyframes[shot]?.file ? { file: keyframes[shot].file, sha256: keyframes[shot].sha256 ?? "" } : null;
    // The work directory is served under /work/ by the renderer's fake origin.
    const background = keyframe ? `${ORIGIN}/work/${keyframe.file.split("/").map(encodeURIComponent).join("/")}` : null;
    const html = thumbnailHtml(own, { background, series: thumbnailSeries(doc), locale });
    return { html, key: hash(theme, html, keyframe?.sha256 ?? ""), text: visibleText(html), ...(shot ? { shot, keyframe } : {}) };
  };
  let thumbnail = null;
  if (doc.thumbnail) {
    thumbnail = drawThumbnail(doc.thumbnail);
    // B and C for YouTube's test (thumbnailVariants); only a thumbnail that has them carries the key.
    const variants = thumbnailVariants(doc.thumbnail).map(({ id, thumbnail: own }) => ({ id, file: thumbnailVariantFile(id), ...drawThumbnail(own) }));
    if (variants.length) thumbnail.variants = variants;
    if (translations) {
      const locales = [];
      const gaps = {};
      for (const locale of LOCALES.filter((each) => each !== narrationLocale(doc))) {
        const own = localizedThumbnail(doc, translations[locale]);
        if (own) locales.push({ locale, file: localeThumbnailFile(locale), hash: localizedThumbnailHash(doc, translations[locale]), ...drawThumbnail(own, locale) });
        else gaps[locale] = thumbnailGap(doc, translations[locale], locale);
      }
      thumbnail.locales = locales;
      thumbnail.gaps = gaps;
    }
  }
  return { scenes, thumbnail };
}

/** Where a caption locale's own thumbnail is written in the work directory (and in upload/). */
export const localeThumbnailFile = (locale) => `thumbnails/${locale}.jpg`;

/** A screencast scene's states: one capture each, with the cursor and highlight drawn over it. */
function screencastStates(scene, timelineStates, manifest, theme, chromeState) {
  if (!manifest) throw new Error(`screencast scene ${scene.id} has no captures yet; the render stage takes them first`);
  return screencastPlan(manifest, timelineStates).map((plan, stateIndex) => {
    const html = screencastHtml(scene, plan, { ...chromeState, first: stateIndex === 0 });
    return { reveal: timelineStates[stateIndex].reveal, first: stateIndex === 0, html, key: hash(theme, html, plan.sha256), text: visibleText(html) };
  });
}

/** Where variant B or C of the thumbnail is written, beside thumbnail.jpg (A). */
export const thumbnailVariantFile = (id) => `thumbnail-${id}.jpg`;

// Relative to the work directory, with forward slashes so the manifest reads the same everywhere.
export const stillFile = (key) => `frames/${key}.png`;
export const transitionFile = (key, index) => `frames/${key}-t${String(index).padStart(2, "0")}.png`;
