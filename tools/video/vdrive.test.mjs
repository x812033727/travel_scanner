import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import test from "node:test";

import {
  createAdapter,
  detectBackend,
  normalizeSafeRelPath,
  pullRules,
  pushEpisode,
  pushRule,
  sha256File,
  shouldExcludeEpisodeRelPath,
} from "./vdrive.mjs";

function makeTempDrive() {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "vdrive-test-"));
  const driveRoot = path.join(root, "drive");
  const cacheDir = path.join(root, "cache");
  fs.mkdirSync(path.join(driveRoot, "_規則", "解說系列共用"), { recursive: true });
  fs.mkdirSync(path.join(driveRoot, "_規則", "奇聞檔案局"), { recursive: true });
  fs.mkdirSync(path.join(driveRoot, "_規則", "通用"), { recursive: true });
  fs.writeFileSync(path.join(driveRoot, "_START-HERE.md"), "# Start Here\n", "utf8");
  fs.writeFileSync(path.join(driveRoot, "_規則", "CHANGELOG.md"), "# Changelog\n", "utf8");
  fs.writeFileSync(
    path.join(driveRoot, "_規則", "解說系列共用", "FLOW-PRODUCTION-RULES.md"),
    "v1 shared rules\n",
    "utf8",
  );
  fs.writeFileSync(
    path.join(driveRoot, "_規則", "奇聞檔案局", "CURIO-FLOW-CHECKLIST.md"),
    "v1 curio checklist\n",
    "utf8",
  );
  fs.writeFileSync(path.join(driveRoot, "_規則", "通用", "lexicon.json"), "{}\n", "utf8");
  return { root, driveRoot, cacheDir };
}

test("detectBackend respects override, local mount, rclone, gdrive, and fails cleanly when none exist", () => {
  assert.deepEqual(
    detectBackend({ explicitRoot: "videobackup:AI劇", env: {}, probe: { existsSync: () => false, hasCommand: () => false } }),
    { type: "rclone", root: "videobackup:AI劇" },
  );
  assert.deepEqual(
    detectBackend({
      env: {},
      probe: {
        existsSync: (p) => p === "G:/我的雲端硬碟/AI/備份/AI劇",
        hasCommand: () => false,
      },
    }),
    { type: "local", root: "G:/我的雲端硬碟/AI/備份/AI劇" },
  );
  assert.deepEqual(
    detectBackend({
      env: { RCLONE_CONFIG_VIDEOBACKUP_TYPE: "drive" },
      probe: {
        existsSync: () => false,
        hasCommand: (cmd) => cmd === "rclone",
      },
    }),
    { type: "rclone", root: "videobackup:AI劇" },
  );
  assert.deepEqual(
    detectBackend({
      env: {},
      probe: {
        existsSync: () => false,
        hasCommand: (cmd) => cmd === "gdrive",
      },
    }),
    { type: "gdrive", root: "1EKqfreFk028Roxv1aF0k2R1Hh3DRJ7kG" },
  );
  assert.throws(
    () => detectBackend({ env: {}, probe: { existsSync: () => false, hasCommand: () => false } }),
    /No Google Drive backend found/,
  );
});

test("normalizeSafeRelPath rejects traversal and empty paths", () => {
  assert.equal(normalizeSafeRelPath("/a/b/c.md/"), "a/b/c.md");
  assert.equal(normalizeSafeRelPath("解說系列共用\\FLOW.md"), "解說系列共用/FLOW.md");
  assert.throws(() => normalizeSafeRelPath("../secret.md"));
  assert.throws(() => normalizeSafeRelPath("a/../b.md"));
  assert.throws(() => normalizeSafeRelPath(""));
});

test("shouldExcludeEpisodeRelPath blocks secrets and rebuildable caches", () => {
  assert.equal(shouldExcludeEpisodeRelPath(".env"), true);
  assert.equal(shouldExcludeEpisodeRelPath("nested/.env.local"), true);
  assert.equal(shouldExcludeEpisodeRelPath("keys/rclone.conf"), true);
  assert.equal(shouldExcludeEpisodeRelPath("auth/api_token.json"), true);
  assert.equal(shouldExcludeEpisodeRelPath("node_modules/pkg/index.js"), true);
  assert.equal(shouldExcludeEpisodeRelPath(".git/HEAD"), true);
  assert.equal(shouldExcludeEpisodeRelPath("腳本定稿/video.json"), false);
  assert.equal(shouldExcludeEpisodeRelPath("review/audience-review.md"), false);
});

test("pullRules pulls scoped rules and records SHA-256 pull manifest", () => {
  const { root, driveRoot, cacheDir } = makeTempDrive();
  try {
    const adapter = createAdapter({ type: "local", root: driveRoot });
    const result = pullRules({ adapter, scope: "curio", cacheDir });
    const rels = result.pulled.map((x) => x.remoteRel).sort();
    assert.deepEqual(rels, [
      "_START-HERE.md",
      "_規則/CHANGELOG.md",
      "_規則/奇聞檔案局/CURIO-FLOW-CHECKLIST.md",
      "_規則/解說系列共用/FLOW-PRODUCTION-RULES.md",
      "_規則/通用/lexicon.json",
    ]);
    assert.equal(
      fs.readFileSync(path.join(cacheDir, "rules", "_規則", "奇聞檔案局", "CURIO-FLOW-CHECKLIST.md"), "utf8"),
      "v1 curio checklist\n",
    );
    const manifest = JSON.parse(fs.readFileSync(path.join(cacheDir, ".pull-manifest.json"), "utf8"));
    assert.equal(manifest.scope, "curio");
    assert.ok(manifest.files["_規則/奇聞檔案局/CURIO-FLOW-CHECKLIST.md"].sha256);
  } finally {
    fs.rmSync(root, { recursive: true, force: true });
  }
});

test("pushRule enforces optimistic locking, archives old version to _history/, and appends CHANGELOG.md", () => {
  const { root, driveRoot, cacheDir } = makeTempDrive();
  try {
    const adapter = createAdapter({ type: "local", root: driveRoot });
    const draftPath = path.join(root, "draft.md");
    fs.writeFileSync(draftPath, "v2 curio checklist\n", "utf8");

    // 1. Refuses without prior pull or --expected-sha256
    assert.throws(
      () =>
        pushRule({
          adapter,
          localFile: draftPath,
          targetRel: "奇聞檔案局/CURIO-FLOW-CHECKLIST.md",
          note: "update checklist",
          cacheDir,
        }),
      /Optimistic lock required/,
    );

    // 2. Pull first, then simulate concurrent edit on Drive -> conflict error!
    pullRules({ adapter, scope: "curio", cacheDir });
    fs.writeFileSync(
      path.join(driveRoot, "_規則", "奇聞檔案局", "CURIO-FLOW-CHECKLIST.md"),
      "concurrent remote edit\n",
      "utf8",
    );
    assert.throws(
      () =>
        pushRule({
          adapter,
          localFile: draftPath,
          targetRel: "奇聞檔案局/CURIO-FLOW-CHECKLIST.md",
          note: "update checklist",
          cacheDir,
        }),
      /Optimistic lock conflict/,
    );

    // 3. Re-pull, then push succeeds, archives previous copy, and appends CHANGELOG
    pullRules({ adapter, scope: "curio", cacheDir });
    const res = pushRule({
      adapter,
      localFile: draftPath,
      targetRel: "奇聞檔案局/CURIO-FLOW-CHECKLIST.md",
      note: "tighten safety prompt rule",
      cacheDir,
      agent: "gemini",
      now: new Date("2026-11-25T02:00:00Z"),
    });
    assert.equal(res.remoteRel, "_規則/奇聞檔案局/CURIO-FLOW-CHECKLIST.md");
    assert.equal(res.archivedRel, "_規則/_history/20261125T020000Z-奇聞檔案局__CURIO-FLOW-CHECKLIST.md");
    assert.equal(
      fs.readFileSync(path.join(driveRoot, "_規則", "奇聞檔案局", "CURIO-FLOW-CHECKLIST.md"), "utf8"),
      "v2 curio checklist\n",
    );
    assert.equal(
      fs.readFileSync(path.join(driveRoot, ...res.archivedRel.split("/")), "utf8"),
      "concurrent remote edit\n",
    );
    const changelog = fs.readFileSync(path.join(driveRoot, "_規則", "CHANGELOG.md"), "utf8");
    assert.match(changelog, /2026-11-25 02:00Z \| `gemini` \| `奇聞檔案局\/CURIO-FLOW-CHECKLIST\.md`/);
    assert.match(changelog, /tighten safety prompt rule/);
  } finally {
    fs.rmSync(root, { recursive: true, force: true });
  }
});

test("pushEpisode excludes secrets/caches and writes verified SHA256SUMS", () => {
  const { root, driveRoot } = makeTempDrive();
  try {
    const adapter = createAdapter({ type: "local", root: driveRoot });
    const epDir = path.join(root, "ep-work");
    fs.mkdirSync(path.join(epDir, "腳本定稿"), { recursive: true });
    fs.mkdirSync(path.join(epDir, "node_modules", "foo"), { recursive: true });
    fs.writeFileSync(path.join(epDir, "腳本定稿", "video.json"), '{"slug":"curio-test"}\n', "utf8");
    fs.writeFileSync(path.join(epDir, ".env"), "SECRET=1\n", "utf8");
    fs.writeFileSync(path.join(epDir, "node_modules", "foo", "a.js"), "ignored\n", "utf8");

    const res = pushEpisode({
      adapter,
      series: "curio",
      destPath: "H-歷史懸案/H99/製作檔/curio-h99-test",
      fromDir: epDir,
    });
    assert.equal(res.fileCount, 1);
    assert.equal(res.remoteBase, "奇聞檔案局/H-歷史懸案/H99/製作檔/curio-h99-test");

    const destBase = path.join(driveRoot, ...res.remoteBase.split("/"));
    assert.equal(fs.existsSync(path.join(destBase, ".env")), false);
    assert.equal(fs.existsSync(path.join(destBase, "node_modules")), false);
    const uploadedJson = path.join(destBase, "腳本定稿", "video.json");
    assert.equal(fs.existsSync(uploadedJson), true);
    const sums = fs.readFileSync(path.join(destBase, "SHA256SUMS"), "utf8");
    assert.equal(sums.trim(), `${sha256File(uploadedJson)}  腳本定稿/video.json`);
  } finally {
    fs.rmSync(root, { recursive: true, force: true });
  }
});
