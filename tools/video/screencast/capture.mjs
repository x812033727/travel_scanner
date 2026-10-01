// Take, or reuse, the stills of every screencast scene in a video.
//
// Stills live in <VIDEO_WORKDIR>/<slug>/screencast/<key>/, keyed by the steps (steps.mjs
// captureKey), with a manifest that records each still's hash, the cursor target and the masks.
// A rerun with the same steps reuses them without opening a browser, so a re-render draws the same
// pixels even when the live page has changed since; changing a step, or passing `recapture`,
// takes that scene's page again.
import { createHash } from "node:crypto";
import { existsSync, mkdirSync, writeFileSync } from "node:fs";
import path from "node:path";

import { atomicWrite, readJson } from "../core/paths.mjs";
import { openScreencastBrowser } from "./browser.mjs";
import { runSteps } from "./runner.mjs";
import { captureCount, captureKey, isScreencast, RUNNER_VERSION, SCALE, VIEWPORT } from "./steps.mjs";

export const SCREENCAST_DIR = "screencast";
export const captureDir = (key) => `${SCREENCAST_DIR}/${key}`;
export const captureFile = (key, index) => `${captureDir(key)}/${String(index + 1).padStart(2, "0")}.png`;
export const manifestFile = (key) => `${captureDir(key)}/manifest.json`;

const sha256 = (buffer) => createHash("sha256").update(buffer).digest("hex");

/** A cached manifest that still matches its steps and whose stills are all on disk, or null. */
export function cachedManifest(workdir, scene, { profile = false } = {}) {
  const key = captureKey(scene.data, { profile });
  const manifest = readJson(path.join(workdir, manifestFile(key)), null);
  if (!manifest || manifest.key !== key || manifest.captures?.length !== captureCount(scene.data)) return null;
  return manifest.captures.every((capture) => existsSync(path.join(workdir, capture.file))) ? manifest : null;
}

/**
 * Make sure every screencast scene of `doc` has its stills. Returns { manifests: { sceneId:
 * manifest }, captured: [sceneId], reused: [sceneId] }. `open` opens the browser (injectable for
 * tests); it is called only when some scene has to be taken. Throws the runner's StepError or the
 * browser's BrowserMissing.
 */
export async function ensureCaptures(doc, workdir, { channel, profile, recapture = false, open = openScreencastBrowser, now = () => new Date(), log = () => {} } = {}) {
  const manifests = {};
  const captured = [];
  const reused = [];
  const todo = [];
  for (const scene of doc.scenes.filter(isScreencast)) {
    const known = recapture ? null : cachedManifest(workdir, scene, { profile: Boolean(profile) });
    if (known) {
      manifests[scene.id] = known;
      reused.push(scene.id);
    } else {
      todo.push(scene);
    }
  }
  if (!todo.length) return { manifests, captured, reused };
  const browser = await open({ channel, profile });
  try {
    for (const scene of todo) {
      const key = captureKey(scene.data, { profile: Boolean(profile) });
      log(`capturing ${scene.id} (${captureCount(scene.data)} stills, key ${key})\n`);
      const driver = await browser.newDriver();
      const { captures } = await runSteps(scene.data, driver);
      mkdirSync(path.join(workdir, captureDir(key)), { recursive: true });
      const manifest = {
        key,
        runner: RUNNER_VERSION,
        viewport: VIEWPORT,
        scale: SCALE,
        profile: Boolean(profile),
        captured_at: now().toISOString(),
        captures: captures.map((capture, index) => {
          const file = captureFile(key, index);
          writeFileSync(path.join(workdir, file), capture.png);
          return { file, sha256: sha256(capture.png), url: capture.url, target: capture.target, press: capture.press, zoom: capture.zoom, masks: capture.masks };
        }),
      };
      atomicWrite(path.join(workdir, manifestFile(key)), `${JSON.stringify(manifest, null, 2)}\n`);
      manifests[scene.id] = manifest;
      captured.push(scene.id);
    }
  } finally {
    await browser.close();
  }
  return { manifests, captured, reused };
}
