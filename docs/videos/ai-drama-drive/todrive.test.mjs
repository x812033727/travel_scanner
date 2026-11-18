// todrive.sh run for real against a fake rclone that treats every path as a local folder, the way
// a mounted Drive folder is used (docs/videos/AI-DRAMA-DRIVE.md §清單與不重複).
import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { createHash } from "node:crypto";
import { chmodSync, existsSync, mkdirSync, mkdtempSync, readdirSync, readFileSync, rmSync, symlinkSync, writeFileSync } from "node:fs";
import os from "node:os";
import path from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

import { excludedReason } from "./todrive-plan.mjs";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const SCRIPT = path.join(HERE, "todrive.sh");

// A small rclone: copy (--files-from, --backup-dir, --links), check (--one-way, --files-from),
// copyto, and lsjson -R --hash --files-only with --exclude "/<dir>/**". Every call is logged.
const FAKE = String.raw`#!/usr/bin/env node
const fs = require("node:fs"); const path = require("node:path"); const crypto = require("node:crypto");
const args = process.argv.slice(2);
fs.appendFileSync(process.env.FAKE_RCLONE_LOG, JSON.stringify(args) + "\n");
const opt = (name) => { const i = args.indexOf(name); return i < 0 ? null : args[i + 1]; };
const positional = []; for (let i = 1; i < args.length; i++) { if (args[i].startsWith("--")) { if (!["--links", "--checksum", "--one-way", "--files-only", "--hash", "-R"].includes(args[i])) i++; } else if (args[i] !== "-R") positional.push(args[i]); }
const md5 = (file) => crypto.createHash("md5").update(fs.readFileSync(file)).digest("hex");
const walk = (root, base = root) => fs.existsSync(root) ? fs.readdirSync(root, { withFileTypes: true }).flatMap((e) => { const full = path.join(root, e.name); return e.isDirectory() ? walk(full, base) : [path.relative(base, full).split(path.sep).join("/")]; }) : [];
const listed = (file) => file ? fs.readFileSync(file, "utf8").split("\n").filter(Boolean) : null;
const sourceOf = (src, name) => { if (name.endsWith(".rclonelink")) { const link = path.join(src, name.slice(0, -11)); try { return { link: fs.readlinkSync(link) }; } catch {} } return { file: path.join(src, name) }; };
const content = (src, name) => { const s = sourceOf(src, name); return s.link !== undefined ? Buffer.from(s.link) : fs.existsSync(s.file) ? fs.readFileSync(s.file) : null; };
const cmd = args[0];
if (process.env.FAKE_RCLONE_FAIL === cmd) { console.error("ERROR : " + cmd + " failed"); process.exit(1); }
if (cmd === "copyto") { const [from, to] = positional; if (!fs.existsSync(from)) { console.error("ERROR : not found"); process.exit(3); } fs.mkdirSync(path.dirname(to), { recursive: true }); fs.copyFileSync(from, to); process.exit(0); }
if (cmd === "lsjson") { const [dir] = positional; if (!fs.existsSync(dir)) process.exit(3); const skip = []; args.forEach((a, i) => { if (a === "--exclude") skip.push(args[i + 1].replace(/^\//, "").replace(/\/\*\*$/, "")); }); const out = walk(dir).filter((p) => !skip.some((s) => p === s || p.startsWith(s + "/"))).map((p) => ({ Path: p, Name: path.basename(p), Size: fs.statSync(path.join(dir, p)).size, IsDir: false, Hashes: { md5: md5(path.join(dir, p)) } })); console.log(JSON.stringify(out)); process.exit(0); }
if (cmd === "copy") { const [src, dest] = positional; const backup = opt("--backup-dir"); for (const name of listed(opt("--files-from"))) { const data = content(src, name); const into = path.join(dest, name); if (fs.existsSync(into) && !fs.readFileSync(into).equals(data)) { fs.mkdirSync(path.dirname(path.join(backup, name)), { recursive: true }); fs.copyFileSync(into, path.join(backup, name)); } fs.mkdirSync(path.dirname(into), { recursive: true }); fs.writeFileSync(into, data); } process.exit(0); }
if (cmd === "check") { const [src, dest] = positional; let bad = 0; for (const name of listed(opt("--files-from"))) { const data = content(src, name); const there = path.join(dest, name); if (!fs.existsSync(there) || !data || !fs.readFileSync(there).equals(data)) { bad++; console.error("ERROR : " + name + ": file not in " + dest); } } console.error("NOTICE: " + bad + " differences found"); process.exit(bad ? 1 : 0); }
console.error("unknown command " + cmd); process.exit(2);
`;

const sha = (data) => createHash("sha256").update(data).digest("hex");

function sandbox() {
  const box = mkdtempSync(path.join(os.tmpdir(), "todrive-"));
  const bin = path.join(box, "bin");
  mkdirSync(bin);
  writeFileSync(path.join(bin, "rclone"), FAKE);
  chmodSync(path.join(bin, "rclone"), 0o755);
  const log = path.join(box, "rclone.log");
  writeFileSync(log, "");
  const episode = path.join(box, "drive", "AI劇", "奇聞檔案局", "H-歷史懸案", "H01");
  const src = path.join(box, "work", "curio-h01");
  const put = (root, name, data) => { mkdirSync(path.dirname(path.join(root, name)), { recursive: true }); writeFileSync(path.join(root, name), data); };
  const run = (args, env = {}) => spawnSync("bash", [SCRIPT, ...args], { encoding: "utf8", env: { ...process.env, PATH: `${bin}:${process.env.PATH}`, FAKE_RCLONE_LOG: log, ...env } });
  const calls = () => readFileSync(log, "utf8").split("\n").filter(Boolean).map((line) => JSON.parse(line));
  return { box, episode, src, put, run, calls, dest: path.join(episode, "製作檔", "curio-h01") };
}

/** The host worker's copy of an episode: its files and the backup.json it writes last. */
function workerCopy(s, files) {
  for (const [name, data] of Object.entries(files)) s.put(s.episode, name, data);
  s.put(s.episode, "backup.json", JSON.stringify({ slug: "curio-h01", files: Object.entries(files).map(([name, data]) => ({ path: name, size: Buffer.byteLength(data), sha256: sha(data) })) }));
}

const latest = (dest) => JSON.parse(readFileSync(path.join(dest, "_todrive", "latest.json"), "utf8"));
const fates = (manifest) => Object.fromEntries(manifest.files.map((file) => [file.path, file.fate]));

test("the exclusions are the documented ones only", () => {
  assert.match(excludedReason("node_modules/x/index.js"), /node_modules/);
  assert.match(excludedReason("tools/.venv/bin/python"), /\.venv/);
  assert.match(excludedReason(".env"), /secret/);
  assert.match(excludedReason("cfg/.env.local"), /secret/);
  assert.match(excludedReason("rclone.conf"), /secret/);
  assert.match(excludedReason("keys/service.pem"), /secret/);
  assert.match(excludedReason("credentials-gcp.json"), /secret/);
  assert.match(excludedReason("_舊版/20261101/a.txt"), /old versions/);
  for (const kept of ["review/zh-TW.wav", "build/video.mp4", "segments/s1.mp4", "notes.env.md", "envelope.json", "credential-notes.md", ".gitignore", "keyframes/k.png"]) {
    assert.equal(excludedReason(kept), null, kept);
  }
});

test("a file the worker already holds with the same bytes is listed, not uploaded; the rest goes, and the manifest lands after the check", () => {
  const s = sandbox();
  workerCopy(s, { "final.mp4": "the cut", "clips/s01.mp4": "clip one", "recordings/l01.wav": "line" });
  s.put(s.src, "upload/final.mp4", "the cut");
  s.put(s.src, "clips/s01.mp4", "clip one, re-graded");
  s.put(s.src, "recordings/l01.wav", "line");
  s.put(s.src, "review/zh-TW.wav", "a gigabyte of takes");
  s.put(s.src, "node_modules/pkg/index.js", "module");
  s.put(s.src, ".env", "TOKEN=secret");
  symlinkSync("upload/final.mp4", path.join(s.src, "current.mp4"));
  const result = s.run([s.src, s.dest]);
  assert.equal(result.status, 0, result.stderr);
  assert.match(result.stdout, /todrive: 7 files, 0 differences/);
  assert.match(result.stdout, /todrive: 3 uploaded, 2 already in the host backup, 2 excluded/);
  for (const name of ["clips/s01.mp4", "review/zh-TW.wav", "current.mp4.rclonelink"]) assert.ok(existsSync(path.join(s.dest, name)), name);
  for (const name of ["upload/final.mp4", "recordings/l01.wav", "node_modules/pkg/index.js", ".env"]) assert.ok(!existsSync(path.join(s.dest, name)), name);
  const manifest = latest(s.dest);
  assert.deepEqual(fates(manifest), {
    ".env": "excluded", "clips/s01.mp4": "upload", "current.mp4": "upload", "node_modules/pkg/index.js": "excluded",
    "recordings/l01.wav": "worker", "review/zh-TW.wav": "upload", "upload/final.mp4": "worker",
  });
  const cut = manifest.files.find((file) => file.path === "upload/final.mp4");
  assert.equal(cut.worker_path, "final.mp4");
  assert.equal(cut.sha256, sha("the cut"));
  assert.equal(manifest.files.find((file) => file.path === "current.mp4").link, "upload/final.mp4");
  assert.match(manifest.files.find((file) => file.path === ".env").reason, /secret/);
  assert.ok(manifest.worker_backup?.sha256);
  const [stamp] = readdirOf(path.join(s.dest, "_todrive")).filter((name) => name !== "latest.json");
  const sums = readFileSync(path.join(s.dest, "_todrive", stamp, "SHA256SUMS"), "utf8");
  assert.equal(sums, `${sha("clip one, re-graded")}  clips/s01.mp4\n${sha("a gigabyte of takes")}  review/zh-TW.wav\n`);
  // The order: copy, check, then the records.
  const order = s.calls().map(([command]) => command);
  assert.deepEqual(order.slice(order.indexOf("copy")), ["copy", "check", "copyto", "copyto", "copyto"]);
  assert.ok(!s.calls().some(([command]) => ["sync", "delete", "deletefile", "purge", "move"].includes(command)), "never deletes in Drive");
});

test("with no worker backup.json every file is uploaded, and a worker file that changed is uploaded too", () => {
  const s = sandbox();
  s.put(s.src, "upload/final.mp4", "the cut");
  s.put(s.src, "notes.md", "notes");
  const first = s.run([s.src, s.dest]);
  assert.equal(first.status, 0, first.stderr);
  assert.match(first.stdout, /2 uploaded, 0 already in the host backup, 0 excluded/);
  assert.match(latest(s.dest).note, /no host backup\.json/);

  // backup.json names the cut, but the folder holds other bytes under that name: not trusted.
  const t = sandbox();
  workerCopy(t, { "final.mp4": "the cut" });
  writeFileSync(path.join(t.episode, "final.mp4"), "something else");
  t.put(t.src, "final.mp4", "the cut");
  const second = t.run([t.src, t.dest]);
  assert.equal(second.status, 0, second.stderr);
  assert.match(second.stdout, /1 uploaded, 0 already in the host backup/);

  // A shared folder has no episode backup: everything goes.
  const u = sandbox();
  u.put(u.src, "track.wav", "music");
  const shared = path.join(u.box, "drive", "AI劇", "_共用素材", "music", "flow");
  const third = u.run([u.src, shared]);
  assert.equal(third.status, 0, third.stderr);
  assert.ok(existsSync(path.join(shared, "track.wav")));
  assert.ok(!u.calls().some(([command, from]) => command === "copyto" && String(from).endsWith("backup.json")), "no episode to read");
});

test("--check copies nothing and fails when an upload is missing or the worker copy changed", () => {
  const s = sandbox();
  workerCopy(s, { "final.mp4": "the cut" });
  s.put(s.src, "final.mp4", "the cut");
  s.put(s.src, "notes.md", "notes");
  assert.equal(s.run([s.src, s.dest]).status, 0);
  const calm = s.run(["--check", s.src, s.dest]);
  assert.equal(calm.status, 0, calm.stderr);
  assert.match(calm.stdout, /2 files, 0 differences/);

  rmSync(path.join(s.dest, "notes.md"));
  const missing = s.run(["--check", s.src, s.dest]);
  assert.equal(missing.status, 1);
  assert.match(missing.stdout, /1 differences/);
  writeFileSync(path.join(s.dest, "notes.md"), "notes");

  writeFileSync(path.join(s.episode, "final.mp4"), "a different cut");
  const changed = s.run(["--check", s.src, s.dest]);
  assert.equal(changed.status, 1, "the worker's copy no longer holds those bytes, and DEST never had them");
  assert.match(changed.stdout, /2 uploaded, 0 already in the host backup/);
  assert.match(changed.stdout, /1 differences/);
  const copies = s.calls().filter(([command]) => command === "copy").length;
  assert.equal(copies, 1, "--check never copies");
});

test("a failed check writes no manifest, and DEST outside AI劇/ is refused", () => {
  const s = sandbox();
  s.put(s.src, "a.txt", "a");
  const failed = s.run([s.src, s.dest], { FAKE_RCLONE_FAIL: "check" });
  assert.equal(failed.status, 1);
  assert.ok(!existsSync(path.join(s.dest, "_todrive")), "no manifest for an unchecked copy");
  const outside = s.run([s.src, path.join(s.box, "drive", "elsewhere")]);
  assert.equal(outside.status, 2);
  assert.match(outside.stderr, /must be under AI劇/);
  const climbing = s.run([s.src, path.join(s.box, "drive", "AI劇", "..", "x")]);
  assert.equal(climbing.status, 2);
});

function readdirOf(dir) {
  return existsSync(dir) ? readdirSync(dir).sort() : [];
}
