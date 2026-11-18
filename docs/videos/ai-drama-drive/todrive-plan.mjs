#!/usr/bin/env node
// todrive-plan.mjs SRC_DIR OUT_DIR [--worker backup.json] [--listing listing.json] [--source NAME]
//
// The plan todrive.sh uploads by (docs/videos/AI-DRAMA-DRIVE.md §清單與不重複). The owner's rule
// is still "everything" (2026-11-10). On 2026-11-18 the owner added: a file the host worker has
// already put in the episode's folder, with exactly the same content, is not uploaded a second
// time. It is recorded in the manifest with where the worker's copy is.
//
// Every file under SRC_DIR gets one line in the manifest, with its size, sha256, md5 and fate:
//   upload   copied into DEST (it is in upload.txt and SHA256SUMS)
//   worker   the same bytes are already in the episode folder: the worker's backup.json names a
//            file of that sha256 and size, and the folder listing (rclone lsjson --hash) shows
//            that path with the same size and md5. Both have to agree; either one alone is not
//            enough, because backup.json may be older than the folder.
//   excluded the only things the rule leaves out: secrets and packages that are reinstalled
//            (node_modules, .venv). They stay in the manifest with the reason, so every file is
//            on some list (docs/videos/lessons/shared.md §十三).
// A symlink is never followed and is always uploaded as a link.
//
// Writes OUT_DIR/upload.txt (for rclone --files-from), OUT_DIR/manifest.json and OUT_DIR/SHA256SUMS,
// and prints one JSON line with the counts.
import { createHash } from "node:crypto";
import { createReadStream, lstatSync, mkdirSync, readdirSync, readFileSync, readlinkSync, writeFileSync } from "node:fs";
import path from "node:path";

export const OLD = "_舊版";
export const RECORDS = "_todrive";

/** Why a path is left out, or null when it goes. Paths are relative, with "/". */
export function excludedReason(relative) {
  const parts = relative.split("/");
  const name = parts.at(-1);
  if (parts[0] === OLD) return "old versions folder (todrive.sh files replaced copies there itself)";
  if (parts[0] === RECORDS) return "todrive's own records";
  if (parts.includes("node_modules")) return "reinstallable package (node_modules)";
  if (parts.includes(".venv")) return "reinstallable package (.venv)";
  if (name === ".env" || name.startsWith(".env.")) return "secret (.env)";
  if (name === "rclone.conf") return "secret (rclone.conf)";
  if (/\.(pem|key)$/i.test(name)) return "secret (key file)";
  if (/^credentials.*\.json$/i.test(name)) return "secret (credentials)";
  return null;
}

function hashes(file) {
  return new Promise((resolve, reject) => {
    const sha256 = createHash("sha256");
    const md5 = createHash("md5");
    createReadStream(file)
      .on("data", (chunk) => { sha256.update(chunk); md5.update(chunk); })
      .on("error", reject)
      .on("end", () => resolve({ sha256: sha256.digest("hex"), md5: md5.digest("hex") }));
  });
}

/** Every file and link under root, relative, sorted; directories are walked, links are not. */
export function walk(root) {
  const found = [];
  const visit = (dir) => {
    for (const entry of readdirSync(dir, { withFileTypes: true }).sort((a, b) => (a.name < b.name ? -1 : a.name > b.name ? 1 : 0))) {
      const full = path.join(dir, entry.name);
      const relative = path.relative(root, full).split(path.sep).join("/");
      if (entry.isSymbolicLink()) found.push({ relative, link: true });
      else if (entry.isDirectory()) visit(full);
      else if (entry.isFile()) found.push({ relative, link: false });
    }
  };
  visit(root);
  return found;
}

/** The worker's files by "sha256 size", from its backup.json; empty when there is none. */
export function workerIndex(backup) {
  const byContent = new Map();
  for (const entry of Array.isArray(backup?.files) ? backup.files : []) {
    if (typeof entry?.path === "string" && typeof entry.sha256 === "string" && Number.isInteger(entry.size)) {
      const key = `${entry.sha256} ${entry.size}`;
      if (!byContent.has(key)) byContent.set(key, entry.path);
    }
  }
  return byContent;
}

/** The episode folder as rclone lsjson -R --hash lists it: path -> { size, md5 }. */
export function listingIndex(listing) {
  const byPath = new Map();
  for (const item of Array.isArray(listing) ? listing : []) {
    if (item?.IsDir || typeof item?.Path !== "string") continue;
    const md5 = item.Hashes?.md5 ?? item.Hashes?.MD5;
    byPath.set(item.Path, { size: item.Size, md5: typeof md5 === "string" ? md5.toLowerCase() : null });
  }
  return byPath;
}

export async function plan(src, { backup = null, listing = null, source = path.basename(src), now = new Date() } = {}) {
  const worker = workerIndex(backup);
  const there = listingIndex(listing);
  const files = [];
  for (const { relative, link } of walk(src)) {
    const full = path.join(src, relative);
    const reason = excludedReason(relative);
    if (reason) {
      files.push({ path: relative, fate: "excluded", reason });
      continue;
    }
    if (link) {
      const target = readlinkSync(full);
      files.push({ path: relative, fate: "upload", link: target, sha256: createHash("sha256").update(target).digest("hex") });
      continue;
    }
    const size = lstatSync(full).size;
    const { sha256, md5 } = await hashes(full);
    const held = worker.get(`${sha256} ${size}`);
    const listed = held ? there.get(held) : null;
    if (held && listed && listed.size === size && listed.md5 === md5) files.push({ path: relative, size, sha256, md5, fate: "worker", worker_path: held });
    else files.push({ path: relative, size, sha256, md5, fate: "upload" });
  }
  const counts = { files: files.length, upload: 0, worker: 0, excluded: 0 };
  for (const file of files) counts[file.fate] += 1;
  return {
    schema_version: 1,
    made_at: now.toISOString(),
    source,
    worker_backup: backup ? { sha256: createHash("sha256").update(JSON.stringify(backup)).digest("hex"), files: worker.size } : null,
    note: backup ? null : "no host backup.json to compare with: every file is uploaded",
    counts,
    files,
  };
}

export function write(manifest, out) {
  mkdirSync(out, { recursive: true });
  const uploads = manifest.files.filter((file) => file.fate === "upload");
  // With --links rclone names a local symlink <name>.rclonelink, and --files-from matches that name.
  writeFileSync(path.join(out, "upload.txt"), uploads.map((file) => `${file.link ? `${file.path}.rclonelink` : file.path}\n`).join(""));
  writeFileSync(path.join(out, "SHA256SUMS"), uploads.filter((file) => !file.link).map((file) => `${file.sha256}  ${file.path}\n`).join(""));
  writeFileSync(path.join(out, "manifest.json"), `${JSON.stringify(manifest, null, 2)}\n`);
}

function readJson(file) {
  if (!file) return null;
  try {
    return JSON.parse(readFileSync(file, "utf8"));
  } catch {
    return null;
  }
}

async function main(argv) {
  const positional = [];
  const options = {};
  for (let i = 0; i < argv.length; i += 1) {
    if (argv[i].startsWith("--")) options[argv[i].slice(2)] = argv[++i];
    else positional.push(argv[i]);
  }
  if (positional.length !== 2) {
    console.error("usage: todrive-plan.mjs SRC_DIR OUT_DIR [--worker backup.json] [--listing listing.json] [--source NAME]");
    process.exit(2);
  }
  const [src, out] = positional;
  const manifest = await plan(src, { backup: readJson(options.worker), listing: readJson(options.listing), source: options.source || path.basename(src) });
  write(manifest, out);
  console.log(JSON.stringify(manifest.counts));
}

if (process.argv[1] && path.resolve(process.argv[1]) === path.resolve(new URL(import.meta.url).pathname)) {
  await main(process.argv.slice(2));
}
