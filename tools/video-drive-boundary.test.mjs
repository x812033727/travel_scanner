/**
 * Route B anti-leak boundary guard (2026-11-25).
 *
 * Owner decision: all new video rules, lessons, topic pools, finalized episode scripts
 * (`video.json`, `script.md`, `i18n/*.json`), and media assets live on Google Drive
 * (`AI/備份/AI劇/_START-HERE.md` and `AI/備份/AI劇/_規則/`) as the single source of truth —
 * zero new per-episode commits or binary assets in GitHub.
 *
 * Legacy directories/files already in `docs/videos/` are frozen below and may only shrink
 * as Stage 3 moves them to Google Drive (`tasks/open/2026-11-25-slim-docs-videos-pools-and-plans.md`).
 */

import assert from "node:assert/strict";
import { execFileSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

const ROOT = fileURLToPath(new URL("../", import.meta.url));
const MEDIA_BINARY = /\.(png|jpe?g|gif|webp|avif|mp3|mp4|m4a|wav|webm|mov|zip|gz|tgz|pdf)$/i;

// Frozen legacy episode directories under docs/videos/. Shrink-only: never add new entries.
const LEGACY_EPISODE_DIRS = new Set([
  "curio-five-recuts-20261012",
  "curio-h01",
  "curio-h01-v2",
  "curio-h01-v3",
  "curio-h02-v2",
  "curio-h03-v2",
  "curio-h04-v2",
  "curio-h04-v3",
  "curio-h05-v2",
  "curio-h05-v3",
  "curio-h06-v2",
  "curio-h07",
  "curio-h07-v2",
  "curio-h09-v2",
  "curio-h10",
  "curio-h11",
  "curio-h12",
  "curio-h24",
  "curio-l08",
  "curio-l08-v2",
  "curio-m09",
  "curio-next-five-20261016",
  "curio-s01",
  "curio-s02",
  "curio-s03",
  "curio-s06",
  "curio-s07",
  "curio-s09",
  "curio-s10",
  "curio-s10-v2",
  "curio-s11",
  "curio-s12",
  "curio-s13",
  "curio-s13-v2",
  "curio-s14",
  "curio-s15",
  "curio-s16",
  "curio-s17",
  "curio-s18",
  "curio-s19",
  "curio-s20",
  "curio-s21",
  "curio-s23-v2",
  "curio-s24",
  "curio-s24-v2",
  "curio-s25",
  "curio-s25-v2",
  "curio-s26",
  "curio-s26-v2",
  "curio-s27",
  "curio-s28",
  "curio-s29",
  "curio-s30",
  "curio-s30-v2",
  "curio-s31",
  "curio-s34",
  "curio-s37",
  "curio-s42",
  "curio-s43",
  "curio-s44",
  "curio-s45",
  "curio-s48",
  "curio-u02",
  "curio-u02-v2",
  "curio-u02-v3",
  "curio-u09",
  "curio-w01-dolby-licensing",
  "curio-w02-michelin-guide-stars",
  "curio-w03-garmin-smartphone-pivot",
  "sothatswhy-b26",
  "sothatswhy-p02-cloud-rain",
  "sothatswhy-p05-down-jacket",
  "sothatswhy-p07-fridge-door",
  "sothatswhy-p08-popcorn-pressure",
  "sothatswhy-p14-sky-colors",
  "sothatswhy-p25-train-tunnel",
  "sothatswhy-t26",
  "sothatswhy-t27",
  "story-everyday-bialetti-c16",
  "story-everyday-bubble-wrap-c04",
  "story-everyday-bubble-wrap-c04-pilot",
  "story-everyday-camelbak-c14",
  "story-everyday-crocs-c01",
  "story-everyday-dr-martens-c07",
  "story-everyday-fiskars-c18",
  "story-everyday-frixion-c15",
  "story-everyday-kikkoman-c08",
  "story-everyday-kikkoman-c08-short-v8",
  "story-everyday-kincho-c05",
  "story-everyday-moleskine-c03",
  "story-everyday-nalgene-c17",
  "story-everyday-oxo-c10",
  "story-everyday-patagonia-c09",
  "story-everyday-patagonia-c09-review",
  "story-everyday-patagonia-c09-revised-script-review",
  "story-everyday-patagonia-c09-script-review",
  "story-everyday-play-doh-c06",
  "story-everyday-pyrex-c12",
  "story-everyday-pyrex-c12-review",
  "story-everyday-pyrex-c12-script",
  "story-everyday-seven-bank-c19",
  "story-everyday-tupperware-c02",
  "story-everyday-ucc-c11",
  "story-everyday-victorinox-c13",
  "story-everyday-zippo-c20",
  "story-everyday-zippo-c20-short-v8",
  "story-plans",
]);

// Shrink-only ceiling for tracked binary media files under docs/videos/.
const MAX_LEGACY_BINARY_FILES = 349;

function trackedDocsVideos() {
  const raw = execFileSync("git", ["ls-files", "-z", "--", "docs/videos"], {
    cwd: ROOT,
    encoding: "utf8",
    maxBuffer: 64 * 1024 * 1024,
  });
  return raw.split("\0").filter(Boolean);
}

test("no new episode script directories are committed under docs/videos/ (Route B: Drive SSOT)", () => {
  const added = new Set();
  for (const file of trackedDocsVideos()) {
    const match = /^docs\/videos\/((?:curio|sothatswhy|story)-[^/]+)\//.exec(file);
    if (match && !LEGACY_EPISODE_DIRS.has(match[1])) {
      added.add(match[1]);
    }
  }
  assert.deepEqual(
    [...added].sort(),
    [],
    "New episode scripts must live on Google Drive (`npm run vdrive -- push-episode`), not in GitHub docs/videos/.",
  );
});

test("tracked binary media files under docs/videos/ never increase", () => {
  const binaries = trackedDocsVideos().filter((f) => MEDIA_BINARY.test(f));
  assert.ok(
    binaries.length <= MAX_LEGACY_BINARY_FILES,
    `docs/videos/ has ${binaries.length} tracked binary files (limit ${MAX_LEGACY_BINARY_FILES}); store new media on Google Drive instead.`,
  );
});

test("gitignore blocks local Drive rule cache and episode draft workdirs", () => {
  const gitignore = fs.readFileSync(path.join(ROOT, ".gitignore"), "utf8");
  assert.match(gitignore, /^\.cache\/video-drive\/$/m);
  assert.match(gitignore, /^work\/video-episodes\/$/m);
});

test("agent entrypoints and curio-episode skill point to Google Drive SSOT (_START-HERE.md & vdrive)", () => {
  for (const rel of ["AGENTS.md", "CLAUDE.md", "GEMINI.md", ".agents/skills/curio-episode/SKILL.md"]) {
    const text = fs.readFileSync(path.join(ROOT, rel), "utf8");
    assert.match(text, /_START-HERE\.md/, `${rel} must point to Google Drive _START-HERE.md`);
    assert.match(text, /npm run vdrive -- pull-rules/, `${rel} must document npm run vdrive -- pull-rules`);
  }
});
