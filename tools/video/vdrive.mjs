#!/usr/bin/env node
/**
 * Cross-environment Google Drive Single-Source-of-Truth (SSOT) CLI (`npm run vdrive`).
 *
 * Implements Route B (2026-11-25): all video rules, lessons, canon sheets, topic pools,
 * and finalized episode scripts live on Google Drive (`AI/備份/AI劇/_START-HERE.md` and
 * `AI/備份/AI劇/_規則/`), never committed to GitHub.
 *
 * Auto-detects the available Drive backend across environments:
 *   1. `VDRIVE_ROOT` override (local directory or `rclone` remote)
 *   2. Local Google Drive mount (`G:/我的雲端硬碟/AI/備份/AI劇`, `G:/My Drive/...`, Colab)
 *   3. `rclone` remote (`videobackup:AI劇`) on VPS / cloud sessions
 *   4. `gdrive` CLI plugin (Antigravity cloud VM)
 *
 * Commands:
 *   npm run vdrive -- status
 *   npm run vdrive -- pull-rules [all|explainer|sothatswhy|curio|shorts|common] [--out <dir>]
 *   npm run vdrive -- push-rule <localFile> --target <relUnderRules> --note "<reason>" [--expected-sha256 <hex>] [--force]
 *   npm run vdrive -- push-episode --series <sothatswhy|curio|...> --path <relDest> --from <localDir> [--dry-run]
 */

import { createHash } from "node:crypto";
import { execFileSync, spawnSync } from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = fileURLToPath(new URL("../../", import.meta.url));
export const DEFAULT_CACHE_DIR = path.join(ROOT, ".cache", "video-drive");
export const DEFAULT_GDRIVE_AI_DRAMA_ROOT_ID = "1EKqfreFk028Roxv1aF0k2R1Hh3DRJ7kG";

export const SERIES_DIRS = {
  sothatswhy: "原來如此事務所",
  curio: "奇聞檔案局",
  shorts: "Shorts",
  "zhong-tian-qu-qi": "種田娶妻打天下",
  "zhong-tian-qu-qi-r2": "種田娶妻打天下（真人版）",
  "tai-nainai": "恁祖媽今年18",
};

export const RULE_SCOPES = {
  all: ["解說系列共用", "原來如此事務所", "奇聞檔案局", "通用", "短劇與漫劇"],
  explainer: ["解說系列共用", "原來如此事務所", "奇聞檔案局", "通用"],
  sothatswhy: ["解說系列共用", "原來如此事務所", "通用"],
  curio: ["解說系列共用", "奇聞檔案局", "通用"],
  shorts: ["短劇與漫劇", "通用"],
  common: ["通用"],
};

const EXCLUDED_DIR_NAMES = new Set([
  ".git",
  "node_modules",
  ".venv",
  "venv",
  "__pycache__",
  ".pytest_cache",
  ".mypy_cache",
  ".ruff_cache",
  ".next",
]);

const SECRET_FILE_PATTERNS = [
  /^\.env(?:\.|$)/i,
  /^rclone\.conf$/i,
  /(?:secret|token|credential|password|passwd).*\.(?:json|txt|env|ya?ml|toml|conf|ini)$/i,
  /\.(?:pem|key|ppk|p12|pfx|agekey)$/i,
  /^id_(?:rsa|ed25519|ecdsa)$/i,
];

export function sha256Buffer(buf) {
  return createHash("sha256").update(buf).digest("hex");
}

export function md5Buffer(buf) {
  return createHash("md5").update(buf).digest("hex");
}

export function sha256File(filePath) {
  return sha256Buffer(fs.readFileSync(filePath));
}

export function toPosix(p) {
  return p.split(path.sep).join("/");
}

export function isRcloneRemote(value) {
  if (!value || typeof value !== "string") return false;
  if (/^[A-Za-z]:[\\/]/.test(value)) return false;
  return /^[A-Za-z0-9_.-]+:/.test(value);
}

export function hasCommand(cmd) {
  const res = spawnSync(cmd, ["--version"], { stdio: "ignore" });
  return !res.error;
}

export function detectAgent(env = process.env) {
  if (env.VDRIVE_AGENT) return env.VDRIVE_AGENT;
  if (env.CLAUDE_CODE || env.CLAUDE_CONFIG_DIR || env.ANTHROPIC_MODEL) return "claude";
  if (env.CODEX_HOME || env.CODEX_SANDBOX_TYPE || env.CODEX_CI) return "codex";
  if (env.ANTIGRAVITY_AGENT || env.USER === "antigravity" || (env.HOME && env.HOME.includes("antigravity"))) {
    return "gemini";
  }
  return "agent";
}

export function detectBackend({ explicitRoot, env = process.env, probe = {} } = {}) {
  const exists = probe.existsSync ?? fs.existsSync;
  const cmdAvailable = probe.hasCommand ?? hasCommand;

  const override = explicitRoot || env.VDRIVE_ROOT;
  if (override) {
    if (isRcloneRemote(override)) {
      return { type: "rclone", root: override.replace(/\/+$/, "") };
    }
    return { type: "local", root: path.resolve(override) };
  }

  const localCandidates = [
    "G:/我的雲端硬碟/AI/備份/AI劇",
    "G:/My Drive/AI/備份/AI劇",
    "/content/drive/MyDrive/AI/備份/AI劇",
  ];
  for (const candidate of localCandidates) {
    if (exists(candidate)) {
      return { type: "local", root: candidate };
    }
  }

  if (
    cmdAvailable("rclone") &&
    (env.RCLONE_CONFIG_VIDEOBACKUP_TYPE ||
      exists("/etc/travel-scanner/rclone-videos/rclone.conf") ||
      env.RCLONE_CONFIG)
  ) {
    return { type: "rclone", root: "videobackup:AI劇" };
  }

  if (cmdAvailable("gdrive")) {
    return {
      type: "gdrive",
      root: env.VDRIVE_GDRIVE_ROOT_ID || DEFAULT_GDRIVE_AI_DRAMA_ROOT_ID,
    };
  }

  throw new Error(
    "No Google Drive backend found. Mount Google Drive (G:/我的雲端硬碟/AI/備份/AI劇), " +
      "configure rclone (videobackup:), enable the gdrive CLI plugin, or set VDRIVE_ROOT.",
  );
}

export function normalizeSafeRelPath(rel) {
  const cleaned = String(rel ?? "")
    .replace(/\\/g, "/")
    .replace(/^\/+|\/+$/g, "");
  if (!cleaned || cleaned.split("/").some((part) => !part || part === "." || part === "..")) {
    throw new Error(`Invalid relative Drive path: ${rel}`);
  }
  return cleaned;
}

export function shouldExcludeEpisodeRelPath(relPosix) {
  const parts = relPosix.split("/");
  for (const part of parts.slice(0, -1)) {
    if (EXCLUDED_DIR_NAMES.has(part)) return true;
  }
  const base = parts[parts.length - 1];
  if (EXCLUDED_DIR_NAMES.has(base)) return true;
  return SECRET_FILE_PATTERNS.some((re) => re.test(base));
}

function walkLocalFiles(baseDir, currentDir = baseDir, out = []) {
  for (const entry of fs.readdirSync(currentDir, { withFileTypes: true }).sort((a, b) => a.name.localeCompare(b.name))) {
    const full = path.join(currentDir, entry.name);
    const rel = toPosix(path.relative(baseDir, full));
    if (shouldExcludeEpisodeRelPath(rel)) continue;
    if (entry.isDirectory()) {
      walkLocalFiles(baseDir, full, out);
    } else if (entry.isFile()) {
      out.push({ rel, full });
    }
  }
  return out;
}

// ---------------------------------------------------------------------------
// Backend adapters: uniform { readFile, listFiles, writeFile } over relPath
// ---------------------------------------------------------------------------

function createLocalAdapter(rootDir) {
  return {
    type: "local",
    root: rootDir,
    readFile(relPath) {
      const full = path.join(rootDir, ...relPath.split("/"));
      if (!fs.existsSync(full) || !fs.statSync(full).isFile()) return null;
      return fs.readFileSync(full);
    },
    listFiles(relDir) {
      const target = relDir ? path.join(rootDir, ...relDir.split("/")) : rootDir;
      if (!fs.existsSync(target) || !fs.statSync(target).isDirectory()) return [];
      const results = [];
      function walk(dir) {
        for (const entry of fs.readdirSync(dir, { withFileTypes: true }).sort((a, b) => a.name.localeCompare(b.name))) {
          const full = path.join(dir, entry.name);
          const rel = toPosix(path.relative(rootDir, full));
          if (entry.isDirectory()) {
            walk(full);
          } else if (entry.isFile()) {
            results.push({ rel, size: fs.statSync(full).size });
          }
        }
      }
      walk(target);
      return results;
    },
    writeFile(relPath, localSourcePath) {
      const dest = path.join(rootDir, ...relPath.split("/"));
      fs.mkdirSync(path.dirname(dest), { recursive: true });
      fs.copyFileSync(localSourcePath, dest);
      const srcSha = sha256File(localSourcePath);
      const dstSha = sha256File(dest);
      if (srcSha !== dstSha) {
        throw new Error(`Checksum mismatch after local write: ${relPath}`);
      }
      return { sha256: dstSha };
    },
  };
}

function createRcloneAdapter(remoteRoot) {
  function runRclone(args) {
    const env = { ...process.env };
    if (!env.RCLONE_CONFIG && fs.existsSync("/etc/travel-scanner/rclone-videos/rclone.conf")) {
      env.RCLONE_CONFIG = "/etc/travel-scanner/rclone-videos/rclone.conf";
    }
    return execFileSync("rclone", args, { encoding: "utf8", env });
  }
  function remotePath(relPath) {
    return relPath ? `${remoteRoot}/${relPath}` : remoteRoot;
  }
  return {
    type: "rclone",
    root: remoteRoot,
    readFile(relPath) {
      const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), "vdrive-rc-get-"));
      try {
        const dest = path.join(tmpDir, path.basename(relPath));
        const res = spawnSync("rclone", ["copyto", remotePath(relPath), dest], { stdio: "pipe" });
        if (res.status !== 0 || !fs.existsSync(dest)) return null;
        return fs.readFileSync(dest);
      } finally {
        fs.rmSync(tmpDir, { recursive: true, force: true });
      }
    },
    listFiles(relDir) {
      try {
        const out = runRclone(["lsjson", "-R", "--files-only", remotePath(relDir)]);
        const items = JSON.parse(out || "[]");
        return items.map((item) => ({
          rel: relDir ? `${relDir}/${item.Path}` : item.Path,
          size: item.Size ?? 0,
        }));
      } catch {
        return [];
      }
    },
    writeFile(relPath, localSourcePath) {
      runRclone(["copyto", "--checksum", localSourcePath, remotePath(relPath)]);
      const check = spawnSync("rclone", ["check", "--one-way", localSourcePath, path.posix.dirname(remotePath(relPath))], {
        stdio: "pipe",
      });
      // `rclone check` works on directories; fallback to reading back if filename differs
      if (check.status !== 0) {
        const readBack = this.readFile(relPath);
        const srcSha = sha256File(localSourcePath);
        if (!readBack || sha256Buffer(readBack) !== srcSha) {
          throw new Error(`Checksum mismatch after rclone upload: ${relPath}`);
        }
        return { sha256: srcSha };
      }
      return { sha256: sha256File(localSourcePath) };
    },
  };
}

function createGdriveAdapter(rootFolderId) {
  const lsCache = new Map();

  function runGdrive(args) {
    return execFileSync("gdrive", args, { encoding: "utf8", maxBuffer: 64 * 1024 * 1024 }).trim();
  }

  function lsFolder(folderId, { refresh = false } = {}) {
    if (!refresh && lsCache.has(folderId)) return lsCache.get(folderId);
    const out = runGdrive(["readonly", "ls", folderId, "--json"]);
    const items = out ? JSON.parse(out) : [];
    lsCache.set(folderId, items);
    return items;
  }

  function parseCreatedId(out, parentId, name) {
    try {
      const parsed = JSON.parse(out);
      if (parsed?.id) return parsed.id;
    } catch {
      // gdrive mutate may return human-readable text with "(ID: ...)"
    }
    const match = /\(ID:\s*([A-Za-z0-9_-]+)\)/.exec(out) || /\bID:\s*([A-Za-z0-9_-]+)/.exec(out);
    if (match) return match[1];
    lsCache.delete(parentId);
    const found = lsFolder(parentId, { refresh: true }).find((x) => x.name === name);
    if (found?.id) return found.id;
    throw new Error(`Could not resolve Drive ID for ${name}: ${out}`);
  }

  function resolveFolder(relDir, { create = false } = {}) {
    if (!relDir) return rootFolderId;
    let current = rootFolderId;
    for (const part of relDir.split("/")) {
      const items = lsFolder(current);
      const found = items.find(
        (x) => x.name === part && x.mimeType === "application/vnd.google-apps.folder",
      );
      if (found) {
        current = found.id;
      } else if (create) {
        const out = runGdrive(["mutate", "mkdir", part, "--parent", current]);
        const createdId = parseCreatedId(out, current, part);
        lsCache.delete(current);
        current = createdId;
      } else {
        return null;
      }
    }
    return current;
  }

  function resolveFileEntry(relPath) {
    const parts = relPath.split("/");
    const fileName = parts.pop();
    const dirId = resolveFolder(parts.join("/"), { create: false });
    if (!dirId) return null;
    const item = lsFolder(dirId).find(
      (x) => x.name === fileName && x.mimeType !== "application/vnd.google-apps.folder",
    );
    return item ? { ...item, parentId: dirId } : null;
  }

  return {
    type: "gdrive",
    root: rootFolderId,
    readFile(relPath) {
      const entry = resolveFileEntry(relPath);
      if (!entry) return null;
      const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), "vdrive-gd-get-"));
      try {
        const outPath = path.join(tmpDir, entry.name);
        runGdrive(["readonly", "download", entry.id, "--out", outPath]);
        return fs.readFileSync(outPath);
      } finally {
        fs.rmSync(tmpDir, { recursive: true, force: true });
      }
    },
    listFiles(relDir) {
      const dirId = resolveFolder(relDir, { create: false });
      if (!dirId) return [];
      const results = [];
      function walk(folderId, prefix) {
        for (const item of lsFolder(folderId)) {
          const nextRel = prefix ? `${prefix}/${item.name}` : item.name;
          if (item.mimeType === "application/vnd.google-apps.folder") {
            walk(item.id, nextRel);
          } else {
            results.push({ rel: nextRel, id: item.id, size: Number(item.size || 0) });
          }
        }
      }
      walk(dirId, relDir);
      return results;
    },
    writeFile(relPath, localSourcePath) {
      const parts = relPath.split("/");
      const fileName = parts.pop();
      const parentId = resolveFolder(parts.join("/"), { create: true });
      const existing = lsFolder(parentId, { refresh: true }).find(
        (x) => x.name === fileName && x.mimeType !== "application/vnd.google-apps.folder",
      );

      const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), "vdrive-gd-put-"));
      const staged = path.join(tmpDir, fileName);
      fs.copyFileSync(localSourcePath, staged);
      try {
        let fileId;
        if (existing) {
          runGdrive(["mutate", "update", existing.id, staged]);
          fileId = existing.id;
        } else {
          const out = runGdrive(["mutate", "upload", staged, "--parent", parentId]);
          fileId = parseCreatedId(out, parentId, fileName);
        }
        lsCache.delete(parentId);
        const info = JSON.parse(runGdrive(["readonly", "info", fileId, "--json"]));
        const localBuf = fs.readFileSync(localSourcePath);
        const localMd5 = md5Buffer(localBuf);
        if (info.md5Checksum && info.md5Checksum !== localMd5) {
          throw new Error(`MD5 mismatch after gdrive upload (${relPath}): local=${localMd5} remote=${info.md5Checksum}`);
        }
        return { id: fileId, sha256: sha256Buffer(localBuf), md5: info.md5Checksum || localMd5 };
      } finally {
        fs.rmSync(tmpDir, { recursive: true, force: true });
      }
    },
  };
}

export function createAdapter(backend) {
  if (backend.type === "local") return createLocalAdapter(backend.root);
  if (backend.type === "rclone") return createRcloneAdapter(backend.root);
  if (backend.type === "gdrive") return createGdriveAdapter(backend.root);
  throw new Error(`Unsupported backend: ${backend.type}`);
}

// ---------------------------------------------------------------------------
// Core operations (exported for unit tests + CLI)
// ---------------------------------------------------------------------------

export function pullRules({ adapter, scope = "explainer", cacheDir = DEFAULT_CACHE_DIR } = {}) {
  const dirs = RULE_SCOPES[scope];
  if (!dirs) {
    throw new Error(`Unknown scope "${scope}". Expected one of: ${Object.keys(RULE_SCOPES).join(", ")}`);
  }

  const outRoot = path.join(cacheDir, "rules");
  fs.mkdirSync(outRoot, { recursive: true });

  const manifestFiles = {};
  const pulled = [];

  function fetchOne(remoteRel) {
    const buf = adapter.readFile(remoteRel);
    if (!buf) return false;
    const localDest = path.join(outRoot, ...remoteRel.split("/"));
    fs.mkdirSync(path.dirname(localDest), { recursive: true });
    fs.writeFileSync(localDest, buf);
    const sha256 = sha256Buffer(buf);
    manifestFiles[remoteRel] = { sha256, bytes: buf.length };
    pulled.push({ remoteRel, localDest, sha256, bytes: buf.length });
    return true;
  }

  fetchOne("_START-HERE.md");
  fetchOne("_規則/CHANGELOG.md");
  if (scope === "all") fetchOne("_規則/SHA256SUMS");

  for (const dir of dirs) {
    const entries = adapter.listFiles(`_規則/${dir}`);
    for (const entry of entries) {
      if (entry.rel.includes("/_history/")) continue;
      fetchOne(entry.rel);
    }
  }

  if (pulled.length === 0) {
    throw new Error(
      `No rule files found on Google Drive under _START-HERE.md or _規則/ (backend=${adapter.type}, root=${adapter.root}).`,
    );
  }

  const manifest = {
    pulledAt: new Date().toISOString(),
    backend: adapter.type,
    root: adapter.root,
    scope,
    files: manifestFiles,
  };
  fs.writeFileSync(path.join(cacheDir, ".pull-manifest.json"), JSON.stringify(manifest, null, 2) + "\n", "utf8");

  return { outRoot, pulled, manifest };
}

export function pushRule({
  adapter,
  localFile,
  targetRel,
  note,
  expectedSha256,
  force = false,
  cacheDir = DEFAULT_CACHE_DIR,
  agent = detectAgent(),
  now = new Date(),
} = {}) {
  if (!localFile || !fs.existsSync(localFile)) {
    throw new Error(`Local rule file not found: ${localFile}`);
  }
  if (!note || !note.trim()) {
    throw new Error("push-rule requires --note \"<reason for rule change>\".");
  }
  const cleanRel = normalizeSafeRelPath(targetRel);
  if (cleanRel.startsWith("_history/") || cleanRel === "_history" || cleanRel === "CHANGELOG.md" || cleanRel === "SHA256SUMS") {
    throw new Error(`Refusing to push directly to reserved metadata path: ${cleanRel}`);
  }

  const remoteRel = `_規則/${cleanRel}`;
  const currentRemote = adapter.readFile(remoteRel);
  let archivedRel = null;

  if (currentRemote) {
    const remoteSha = sha256Buffer(currentRemote);
    if (!force) {
      let baseSha = expectedSha256;
      if (!baseSha) {
        const manifestPath = path.join(cacheDir, ".pull-manifest.json");
        if (fs.existsSync(manifestPath)) {
          const manifest = JSON.parse(fs.readFileSync(manifestPath, "utf8"));
          baseSha = manifest.files?.[remoteRel]?.sha256;
        }
      }
      if (!baseSha) {
        throw new Error(
          `Optimistic lock required: ${remoteRel} already exists on Drive (sha256=${remoteSha.slice(0, 12)}). ` +
            "Run `npm run vdrive -- pull-rules` first or pass `--expected-sha256 <hex>`.",
        );
      }
      if (baseSha !== remoteSha) {
        throw new Error(
          `Optimistic lock conflict on ${remoteRel}: expected=${baseSha.slice(0, 12)} remote=${remoteSha.slice(0, 12)}. ` +
            "Pull the latest rule from Drive and merge before pushing.",
        );
      }
    }

    // Archive previous version before overwriting
    const stamp = now.toISOString().replace(/[-:]/g, "").replace(/\.\d+Z$/, "Z");
    const flatName = cleanRel.replace(/\//g, "__");
    archivedRel = `_規則/_history/${stamp}-${flatName}`;
    const tmpArchive = fs.mkdtempSync(path.join(os.tmpdir(), "vdrive-arch-"));
    try {
      const archLocal = path.join(tmpArchive, path.basename(archivedRel));
      fs.writeFileSync(archLocal, currentRemote);
      adapter.writeFile(archivedRel, archLocal);
    } finally {
      fs.rmSync(tmpArchive, { recursive: true, force: true });
    }
  }

  const uploaded = adapter.writeFile(remoteRel, localFile);

  // Update CHANGELOG.md
  const existingLogBuf = adapter.readFile("_規則/CHANGELOG.md");
  const existingLog = existingLogBuf
    ? existingLogBuf.toString("utf8").trimEnd()
    : "# 雲端規則正本異動紀錄（CHANGELOG）";
  const dateLine = now.toISOString().slice(0, 16).replace("T", " ") + "Z";
  const entry = `- ${dateLine} | \`${agent}\` | \`${cleanRel}\` | sha256:\`${uploaded.sha256.slice(0, 12)}\` | ${note.trim()}`;
  const updatedLog = `${existingLog}\n${entry}\n`;
  const tmpLog = fs.mkdtempSync(path.join(os.tmpdir(), "vdrive-log-"));
  try {
    const logPath = path.join(tmpLog, "CHANGELOG.md");
    fs.writeFileSync(logPath, updatedLog, "utf8");
    adapter.writeFile("_規則/CHANGELOG.md", logPath);
  } finally {
    fs.rmSync(tmpLog, { recursive: true, force: true });
  }

  // Update local pull manifest if present so subsequent pushes know the new SHA
  const manifestPath = path.join(cacheDir, ".pull-manifest.json");
  if (fs.existsSync(manifestPath)) {
    const manifest = JSON.parse(fs.readFileSync(manifestPath, "utf8"));
    manifest.files = manifest.files || {};
    manifest.files[remoteRel] = { sha256: uploaded.sha256, bytes: fs.statSync(localFile).size };
    fs.writeFileSync(manifestPath, JSON.stringify(manifest, null, 2) + "\n", "utf8");
  }

  return { remoteRel, sha256: uploaded.sha256, archivedRel };
}

export function pushEpisode({ adapter, series, destPath, fromDir, dryRun = false } = {}) {
  if (!fromDir || !fs.existsSync(fromDir) || !fs.statSync(fromDir).isDirectory()) {
    throw new Error(`Episode source directory not found: ${fromDir}`);
  }
  const seriesDir = SERIES_DIRS[series] || series;
  if (!seriesDir) {
    throw new Error("push-episode requires --series <sothatswhy|curio|shorts|series-folder>");
  }
  const cleanDest = normalizeSafeRelPath(destPath);
  const remoteBase = `${seriesDir}/${cleanDest}`;
  const files = walkLocalFiles(fromDir);
  if (files.length === 0) {
    throw new Error(`No uploadable files found in ${fromDir}`);
  }

  const sums = [];
  for (const file of files) {
    if (file.rel === "SHA256SUMS") continue;
    const sha = sha256File(file.full);
    sums.push(`${sha}  ${file.rel}`);
    if (!dryRun) {
      adapter.writeFile(`${remoteBase}/${file.rel}`, file.full);
    }
  }

  const sumsContent = sums.sort().join("\n") + "\n";
  if (!dryRun) {
    const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), "vdrive-ep-"));
    try {
      const sumsPath = path.join(tmpDir, "SHA256SUMS");
      fs.writeFileSync(sumsPath, sumsContent, "utf8");
      adapter.writeFile(`${remoteBase}/SHA256SUMS`, sumsPath);
    } finally {
      fs.rmSync(tmpDir, { recursive: true, force: true });
    }
  }

  return { remoteBase, fileCount: sums.length, dryRun };
}

// ---------------------------------------------------------------------------
// CLI entry
// ---------------------------------------------------------------------------

function parseFlags(args) {
  const positional = [];
  const flags = {};
  for (let i = 0; i < args.length; i += 1) {
    const arg = args[i];
    if (arg.startsWith("--")) {
      const key = arg.slice(2);
      const next = args[i + 1];
      if (!next || next.startsWith("--")) {
        flags[key] = true;
      } else {
        flags[key] = next;
        i += 1;
      }
    } else {
      positional.push(arg);
    }
  }
  return { positional, flags };
}

function usage() {
  console.log(`Usage: npm run vdrive -- <command> [options]

Commands:
  status
      Show detected Google Drive backend, root, and local cache status.

  pull-rules [all|explainer|sothatswhy|curio|shorts|common] [--out <dir>]
      Pull authoritative rules, lessons, lexicon, and canon sheets from Drive
      into gitignored .cache/video-drive/rules/ (default scope: explainer).

  push-rule <localFile> --target <relUnderRules> --note "<reason>" [--expected-sha256 <hex>] [--force]
      Optimistic-lock update to AI/備份/AI劇/_規則/<relUnderRules>.
      Refuses if remote changed since pull; archives previous copy to _history/
      and appends an entry to CHANGELOG.md.

  push-episode --series <sothatswhy|curio|shorts> --path <relDest> --from <localDir> [--dry-run]
      Upload finalized script (腳本定稿/) and episode production files to Drive
      with SHA256SUMS verification (0 GitHub commits).
`);
}

function main() {
  const { positional, flags } = parseFlags(process.argv.slice(2));
  const cmd = positional[0];
  if (!cmd || cmd === "help" || flags.help) {
    usage();
    return;
  }

  const cacheDir = flags.out ? path.resolve(flags.out) : DEFAULT_CACHE_DIR;
  const backend = detectBackend({ explicitRoot: flags.root });
  const adapter = createAdapter(backend);

  if (cmd === "status") {
    const manifestPath = path.join(cacheDir, ".pull-manifest.json");
    const manifest = fs.existsSync(manifestPath) ? JSON.parse(fs.readFileSync(manifestPath, "utf8")) : null;
    console.log(
      JSON.stringify(
        {
          backend: backend.type,
          root: backend.root,
          cacheDir,
          lastPull: manifest
            ? { pulledAt: manifest.pulledAt, scope: manifest.scope, fileCount: Object.keys(manifest.files || {}).length }
            : null,
        },
        null,
        2,
      ),
    );
    return;
  }

  if (cmd === "pull-rules") {
    const scope = positional[1] || "explainer";
    const result = pullRules({ adapter, scope, cacheDir });
    console.log(`vdrive: pulled ${result.pulled.length} file(s) [scope=${scope}, backend=${adapter.type}] -> ${result.outRoot}`);
    for (const item of result.pulled) {
      console.log(`  ${item.remoteRel}  (${item.bytes} B, sha256:${item.sha256.slice(0, 12)})`);
    }
    return;
  }

  if (cmd === "push-rule") {
    const localFile = positional[1];
    const result = pushRule({
      adapter,
      localFile,
      targetRel: flags.target,
      note: flags.note,
      expectedSha256: flags["expected-sha256"],
      force: Boolean(flags.force),
      cacheDir,
    });
    console.log(
      `vdrive: updated ${result.remoteRel} (sha256:${result.sha256.slice(0, 12)})` +
        (result.archivedRel ? ` [archived previous -> ${result.archivedRel}]` : " [new file]"),
    );
    return;
  }

  if (cmd === "push-episode") {
    const result = pushEpisode({
      adapter,
      series: flags.series,
      destPath: flags.path,
      fromDir: flags.from,
      dryRun: Boolean(flags["dry-run"]),
    });
    console.log(
      `vdrive: ${result.dryRun ? "dry-run " : ""}pushed ${result.fileCount} file(s) + SHA256SUMS -> ${result.remoteBase} (0 differences)`,
    );
    return;
  }

  throw new Error(`Unknown command: ${cmd}`);
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  try {
    main();
  } catch (error) {
    console.error(`vdrive error: ${error.message}`);
    process.exitCode = 1;
  }
}
