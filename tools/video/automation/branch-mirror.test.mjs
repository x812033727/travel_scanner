// The branch mirror (branch-mirror.mjs) against a real local bare repository with transfer/*
// branches, and a fake rclone that syncs between real folders (rclone is not on every machine that
// runs these tests): what lands in Drive, when nothing is done, where replaced and deleted files go,
// and that a failed check is never recorded as mirrored.
import assert from "node:assert/strict";
import { execFileSync } from "node:child_process";
import { createHash, randomBytes } from "node:crypto";
import { cpSync, existsSync, mkdirSync, mkdtempSync, readdirSync, readFileSync, renameSync, rmSync, writeFileSync } from "node:fs";
import os from "node:os";
import path from "node:path";
import test from "node:test";

import { backupAfterRound, branchMirrorAfterBackup } from "./cli.mjs";
import { branchFolder, branchMirrorRound, gitAccess, MIRROR_DIR, parseHeads, prefixesFrom, readMirrorState, rejoinParts } from "./branch-mirror.mjs";

const NOW = new Date("2026-11-08T09:00:00Z");
const later = (minutes) => new Date(NOW.getTime() + minutes * 60_000);
const OLD = "_舊版";

const git = (cwd, ...args) => execFileSync("git", args, { cwd, encoding: "utf8", env: { ...process.env, GIT_CONFIG_GLOBAL: "/dev/null", GIT_CONFIG_NOSYSTEM: "1", GIT_AUTHOR_NAME: "t", GIT_AUTHOR_EMAIL: "t@example.com", GIT_COMMITTER_NAME: "t", GIT_COMMITTER_EMAIL: "t@example.com" } }).trim();

function put(dir, name, content = name) {
  const file = path.join(dir, ...name.split("/"));
  mkdirSync(path.dirname(file), { recursive: true });
  writeFileSync(file, content);
}

const listing = (dir, prefix = "") => (existsSync(dir) ? readdirSync(dir, { withFileTypes: true }).flatMap((entry) => (entry.isDirectory() ? listing(path.join(dir, entry.name), `${prefix}${entry.name}/`) : [`${prefix}${entry.name}`])).sort() : []);

/** A sandbox: a bare origin, a clone to commit from, the worker's work base, a Drive folder. */
function sandbox() {
  const box = mkdtempSync(path.join(os.tmpdir(), "branch-mirror-test-"));
  const origin = path.join(box, "origin.git");
  const clone = path.join(box, "clone");
  const work = path.join(box, "work");
  const drive = path.join(box, "drive");
  for (const dir of [clone, work, drive]) mkdirSync(dir, { recursive: true });
  git(box, "init", "--bare", "--quiet", origin);
  git(clone, "init", "--quiet");
  git(clone, "checkout", "--quiet", "-b", "main");
  put(clone, "README.md", "main");
  git(clone, "add", "-A");
  git(clone, "commit", "--quiet", "-m", "main");
  git(clone, "push", "--quiet", origin, "main");
  const conf = path.join(box, "rclone.conf");
  writeFileSync(conf, "[videobackup]\ntype = alias\n");
  return { box, origin, clone, work, drive, conf };
}

/** A commit on `branch` holding exactly `files` ({ path: content }), pushed to the origin. */
function pushBranch(box, branch, files) {
  const { clone, origin } = box;
  const exists = git(clone, "branch", "--list", branch);
  git(clone, "checkout", "--quiet", ...(exists ? [branch] : ["--orphan", branch]));
  git(clone, "rm", "-r", "--quiet", "--cached", "--ignore-unmatch", ".");
  for (const entry of readdirSync(clone)) if (entry !== ".git") rmSync(path.join(clone, entry), { recursive: true, force: true });
  for (const [name, content] of Object.entries(files)) put(clone, name, content);
  git(clone, "add", "-A");
  git(clone, "commit", "--quiet", "--allow-empty", "-m", `${branch} backup`);
  git(clone, "push", "--quiet", "--force", origin, `${branch}:refs/heads/${branch}`);
  return git(clone, "rev-parse", "HEAD");
}

/** `content` cut into `count` parts named like bk-episode.sh's: X.part00, X.part01… */
function parts(name, content, count = 3) {
  const size = Math.ceil(content.length / count);
  return Object.fromEntries(Array.from({ length: count }, (_, index) => [`${name}.part${String(index).padStart(2, "0")}`, content.subarray(index * size, (index + 1) * size)]));
}

/** rclone over real folders: "videobackup:" is `drive`. sync moves replaced and extra files to --backup-dir. */
function fakeRclone(drive, { fail = {}, corrupt = false } = {}) {
  const calls = [];
  const local = (where) => (where.startsWith("videobackup:") ? path.join(drive, ...where.slice("videobackup:".length).split("/").filter(Boolean)) : where);
  const outside = (relative) => !relative.startsWith(`${OLD}/`);
  const same = (a, b) => readFileSync(a).equals(readFileSync(b));
  const run = async (args) => {
    calls.push(args);
    const [command, source, target] = args;
    if (fail[command]) return { code: 1, stdout: "", stderr: `ERROR : ${fail[command]}\nNOTICE: 1 differences found` };
    if (command === "sync") {
      assert.ok(args.includes("--backup-dir"), "a sync always moves what it replaces aside");
      assert.ok(args.includes(`/${OLD}/**`), "and never touches the old versions");
      const into = local(target);
      const backupDir = local(args[args.indexOf("--backup-dir") + 1]);
      const aside = (relative) => {
        mkdirSync(path.dirname(path.join(backupDir, relative)), { recursive: true });
        renameSync(path.join(into, relative), path.join(backupDir, relative));
      };
      const wanted = new Set(listing(source));
      for (const relative of listing(into).filter(outside)) if (!wanted.has(relative)) aside(relative);
      for (const relative of wanted) {
        const there = path.join(into, relative);
        if (existsSync(there) && same(there, path.join(source, relative))) continue;
        if (existsSync(there)) aside(relative);
        mkdirSync(path.dirname(there), { recursive: true });
        cpSync(path.join(source, relative), there);
        if (corrupt) writeFileSync(there, "garbled");
      }
      return { code: 0, stdout: "", stderr: "" };
    }
    if (command === "check") {
      const into = local(target);
      const mine = listing(source);
      const theirs = listing(into).filter(outside);
      const bad = [...new Set([...mine, ...theirs])].filter((relative) => !mine.includes(relative) || !theirs.includes(relative) || !same(path.join(source, relative), path.join(into, relative)));
      return bad.length ? { code: 1, stdout: "", stderr: `ERROR : ${bad[0]}: sizes differ\nNOTICE: ${bad.length} differences found` } : { code: 0, stdout: "", stderr: "" };
    }
    return { code: 2, stdout: "", stderr: `unknown command ${command}` };
  };
  return { run, calls, commands: () => calls.map(([command]) => command) };
}

/** A git runner that records each call and runs the real git. */
function recordingGit() {
  const calls = [];
  const run = (args, options) => {
    calls.push(args);
    try {
      const stdout = execFileSync("git", args, { cwd: options.cwd, env: options.env, encoding: "utf8", stdio: ["ignore", "pipe", "pipe"] });
      return Promise.resolve({ code: 0, stdout, stderr: "" });
    } catch (error) {
      return Promise.resolve({ code: error.status ?? 1, stdout: String(error.stdout ?? ""), stderr: String(error.stderr ?? error.message) });
    }
  };
  return { run, calls, fetches: () => calls.filter((args) => args.includes("fetch")).length };
}

const site = (prefix = "") => ({ config: async () => ({ enabled: true, remote_prefix: prefix }) });

function ctxFor(box, { now = NOW, env = {} } = {}) {
  return {
    env: {
      VIDEO_WORKDIR: box.work, VIDEO_BACKUP_RCLONE_CONFIG: box.conf, VIDEO_BACKUP_LOCK_PATH: "AI/備份", TMPDIR: box.box,
      VIDEO_BRANCH_MIRROR: "on", VIDEO_BRANCH_MIRROR_REPO: `file://${box.origin}`,
      VIDEO_BRANCH_MIRROR_PER_ROUND: "5", VIDEO_BRANCH_MIRROR_MIN_FREE_GB: "0", PATH: process.env.PATH,
      ...env,
    },
    now: () => now,
    root: path.join(box.box, "repo"),
  };
}

const sha256 = (buffer) => createHash("sha256").update(buffer).digest("hex");
const ZT = "drama/zhong-tian-qu-qi/_分支/zt-live-e001";
const TN = "drama/tai-nainai/_分支/tn-e001";

test("names: the series folder from the branch's code, other prefixes under _其他, odd names refused", () => {
  assert.equal(branchFolder("transfer/zt-live-e001"), ZT);
  assert.equal(branchFolder("transfer/zt-shared"), "drama/zhong-tian-qu-qi/_分支/zt-shared");
  assert.equal(branchFolder("transfer/tn-e001"), TN);
  assert.equal(branchFolder("transfer/xb-e001"), "drama/_其他/_分支/xb-e001");
  assert.equal(branchFolder("transfer/zt/nested"), null, "a branch name with a sub-path is not a folder");
  assert.equal(branchFolder("transfer/../x"), null);
  assert.deepEqual(prefixesFrom({}), ["transfer/zt-", "transfer/tn-"]);
  assert.deepEqual(prefixesFrom({ VIDEO_BRANCH_MIRROR_PREFIXES: "transfer/zt-live-, transfer/tn-" }), ["transfer/zt-live-", "transfer/tn-"]);
  const sha = "a".repeat(40);
  assert.deepEqual(parseHeads(`${sha}\trefs/heads/transfer/zt-live-e001\n${sha}\trefs/heads/main\n${sha}\trefs/heads/transfer/tn-e001\n`, ["transfer/zt-", "transfer/tn-"]).map(({ branch }) => branch), ["transfer/tn-e001", "transfer/zt-live-e001"]);
});

test("access: anonymous over HTTPS by default (the repository is public); a token is a fallback and never goes on a command line", () => {
  const box = sandbox();
  const anonymous = gitAccess({});
  assert.equal(anonymous.url, "https://github.com/x812033727/travel_scanner.git");
  assert.equal(anonymous.how, "anonymous");
  assert.equal(anonymous.env.GIT_CONFIG_COUNT, undefined);
  assert.equal(anonymous.env.GIT_TERMINAL_PROMPT, "0");
  const token = gitAccess({ VIDEO_BRANCH_MIRROR_TOKEN: "s3cret" });
  assert.equal(token.url, "https://github.com/x812033727/travel_scanner.git");
  assert.match(token.env.GIT_CONFIG_VALUE_0, /^Authorization: Basic /);
  put(box.box, "token", "fromfile\n");
  assert.equal(gitAccess({ VIDEO_BRANCH_MIRROR_TOKEN_FILE: path.join(box.box, "token") }).how, "token");
  assert.match(gitAccess({ VIDEO_BRANCH_MIRROR_TOKEN_FILE: path.join(box.box, "missing") }).problem, /cannot be read/);
});

test("off: unless VIDEO_BRANCH_MIRROR is on (the production compose file sets it), nothing runs and nothing is printed", async () => {
  const box = sandbox();
  pushBranch(box, "transfer/zt-live-e001", { "a.txt": "a" });
  const rclone = fakeRclone(box.drive);
  const gitCalls = recordingGit();
  const off = await branchMirrorRound(ctxFor(box, { env: { VIDEO_BRANCH_MIRROR: "" } }), { client: site(), rclone: rclone.run, git: gitCalls.run });
  assert.deepEqual(off.lines, []);
  assert.equal(gitCalls.calls.length + rclone.calls.length, 0);
  const out = [];
  await branchMirrorAfterBackup({ ...ctxFor(box, { env: { VIDEO_BRANCH_MIRROR: "off" } }), stdout: { write: (line) => out.push(line) }, branchMirrorRclone: rclone.run });
  assert.deepEqual(out, []);
  const backupOff = await branchMirrorRound(ctxFor(box), { client: { config: async () => ({ enabled: false, remote_prefix: null }) }, rclone: rclone.run, git: gitCalls.run });
  assert.match(backupOff.lines.join("\n"), /backup is off/);
  assert.equal(gitCalls.calls.length, 0);
});

test("a branch lands in drama/<series>/_分支/<branch>/ with its parts joined back, checked, and recorded", async () => {
  const box = sandbox();
  const final = randomBytes(300_000);
  const draft = randomBytes(120_000);
  const zt = pushBranch(box, "transfer/zt-live-e001", {
    "README-backup.md": "說明",
    "zhong-tian-qu-qi-e901-dh/audio/zq901a01.wav": "wav",
    "_scratchpad/notes.md": "筆記",
    ...parts("zhong-tian-qu-qi-import/zhong-tian-qu-qi-e001/final.mp4", final, 3),
  });
  const tn = pushBranch(box, "transfer/tn-e001", {
    "tai-nainai-import/tai-nainai-e001/meta.json": "{}",
    ...parts("tai-nainai-e001/cut/e001.mp4", draft, 2),
    "tai-nainai-e001/cut/e001.mp4.SPLIT": `sha256 ${sha256(draft)}  e001.mp4\nparts 2\n`,
  });
  pushBranch(box, "transfer/other-thing", { "x.txt": "not mirrored" });
  const rclone = fakeRclone(box.drive);
  const { lines, mirrored } = await branchMirrorRound(ctxFor(box), { client: site(), rclone: rclone.run });

  assert.deepEqual(mirrored.map(({ branch }) => branch).sort(), ["transfer/tn-e001", "transfer/zt-live-e001"]);
  assert.deepEqual(listing(path.join(box.drive, ...ZT.split("/"))), ["README-backup.md", "_scratchpad/notes.md", "zhong-tian-qu-qi-e901-dh/audio/zq901a01.wav", "zhong-tian-qu-qi-import/zhong-tian-qu-qi-e001/final.mp4"]);
  assert.ok(readFileSync(path.join(box.drive, ...ZT.split("/"), "zhong-tian-qu-qi-import/zhong-tian-qu-qi-e001/final.mp4")).equals(final), "joined in order");
  assert.deepEqual(listing(path.join(box.drive, ...TN.split("/"))), ["tai-nainai-e001/cut/e001.mp4", "tai-nainai-e001/cut/e001.mp4.SPLIT", "tai-nainai-import/tai-nainai-e001/meta.json"]);
  assert.ok(readFileSync(path.join(box.drive, ...TN.split("/"), "tai-nainai-e001/cut/e001.mp4")).equals(draft));
  assert.ok(!existsSync(path.join(box.drive, "drama", "_其他")), "a branch outside the prefixes is left alone");
  assert.deepEqual(rclone.commands(), ["sync", "check", "sync", "check"]);

  const state = readMirrorState(box.work);
  assert.equal(state.branches["transfer/zt-live-e001"].commit, zt);
  assert.equal(state.branches["transfer/tn-e001"].commit, tn);
  assert.equal(state.branches["transfer/zt-live-e001"].check, "ok");
  assert.deepEqual(state.branches["transfer/zt-live-e001"].joined, ["zhong-tian-qu-qi-import/zhong-tian-qu-qi-e001/final.mp4"]);
  assert.equal(state.branches["transfer/zt-live-e001"].files, 4);
  assert.match(lines.join("\n"), /transfer\/zt-live-e001 [0-9a-f]{12} → drama\/zhong-tian-qu-qi\/_分支\/zt-live-e001: 4 files, .*1 joined from parts, rclone check 0 differences/);
  assert.deepEqual(listing(path.join(box.work, MIRROR_DIR)), ["branch-mirror.json"], "the staging folder and the throwaway repository are gone");
});

test("the site's backup folder is the root: a remote_prefix is kept in front", async () => {
  const box = sandbox();
  pushBranch(box, "transfer/zt-shared", { "sfx/rain.wav": "rain" });
  const rclone = fakeRclone(box.drive);
  await branchMirrorRound(ctxFor(box), { client: site("備份子資料夾"), rclone: rclone.run });
  assert.deepEqual(listing(path.join(box.drive, "備份子資料夾", "drama", "zhong-tian-qu-qi", "_分支", "zt-shared")), ["sfx/rain.wav"]);
});

test("an unchanged commit is no work: no fetch, no copy", async () => {
  const box = sandbox();
  pushBranch(box, "transfer/zt-live-e001", { "a.txt": "a" });
  await branchMirrorRound(ctxFor(box), { client: site(), rclone: fakeRclone(box.drive).run });
  const rclone = fakeRclone(box.drive);
  const gitCalls = recordingGit();
  const again = await branchMirrorRound(ctxFor(box, { now: later(5) }), { client: site(), rclone: rclone.run, git: gitCalls.run });
  assert.deepEqual(again.mirrored, []);
  assert.equal(gitCalls.fetches(), 0);
  assert.deepEqual(gitCalls.calls.map(([command]) => command), ["ls-remote"]);
  assert.equal(rclone.calls.length, 0);
  assert.deepEqual(again.lines, []);
});

test("a new commit: the changed file is replaced and the deleted one leaves, both kept under _舊版/<time>/", async () => {
  const box = sandbox();
  pushBranch(box, "transfer/zt-live-e001", { "keep.txt": "same", "picks.json": "v1", "old-draft.mp4": "draft" });
  await branchMirrorRound(ctxFor(box), { client: site(), rclone: fakeRclone(box.drive).run });
  const second = pushBranch(box, "transfer/zt-live-e001", { "keep.txt": "same", "picks.json": "v2", "new.txt": "new" });
  const { mirrored } = await branchMirrorRound(ctxFor(box, { now: later(60) }), { client: site(), rclone: fakeRclone(box.drive).run });
  assert.deepEqual(mirrored, [{ branch: "transfer/zt-live-e001", commit: second }]);
  const folder = path.join(box.drive, ...ZT.split("/"));
  assert.deepEqual(listing(folder), [`${OLD}/20261108T100000Z/old-draft.mp4`, `${OLD}/20261108T100000Z/picks.json`, "keep.txt", "new.txt", "picks.json"]);
  assert.equal(readFileSync(path.join(folder, "picks.json"), "utf8"), "v2");
  assert.equal(readFileSync(path.join(folder, OLD, "20261108T100000Z", "picks.json"), "utf8"), "v1");
  assert.equal(readMirrorState(box.work).branches["transfer/zt-live-e001"].commit, second);
});

test("a check with differences is not recorded as mirrored, and the next round tries again", async () => {
  const box = sandbox();
  const commit = pushBranch(box, "transfer/tn-e002", { "a.txt": "a" });
  const bad = await branchMirrorRound(ctxFor(box), { client: site(), rclone: fakeRclone(box.drive, { corrupt: true }).run });
  assert.deepEqual(bad.mirrored, []);
  let record = readMirrorState(box.work).branches["transfer/tn-e002"];
  assert.equal(record.commit, undefined, "never recorded as mirrored");
  assert.equal(record.check, "differences");
  assert.equal(record.failures, 1);
  assert.match(record.error, /^rclone check: NOTICE: 1 differences found/);
  assert.match(bad.lines.join("\n"), /not mirrored \(rclone check/);

  const failedSync = await branchMirrorRound(ctxFor(box, { now: later(5) }), { client: site(), rclone: fakeRclone(box.drive, { fail: { sync: "quota" } }).run });
  assert.deepEqual(failedSync.mirrored, []);
  assert.equal(readMirrorState(box.work).branches["transfer/tn-e002"].failures, 2);

  const good = await branchMirrorRound(ctxFor(box, { now: later(10) }), { client: site(), rclone: fakeRclone(box.drive).run });
  assert.deepEqual(good.mirrored, [{ branch: "transfer/tn-e002", commit }]);
  record = readMirrorState(box.work).branches["transfer/tn-e002"];
  assert.equal(record.check, "ok");
  assert.equal(record.failures, 0);
});

test("a .SPLIT note that does not match the joined file stops the branch before anything is copied", async () => {
  const box = sandbox();
  const data = randomBytes(50_000);
  pushBranch(box, "transfer/tn-e003", { ...parts("cut/e003.mp4", data, 2), "cut/e003.mp4.SPLIT": `sha256 ${"0".repeat(64)}\n` });
  const rclone = fakeRclone(box.drive);
  const { mirrored, lines } = await branchMirrorRound(ctxFor(box), { client: site(), rclone: rclone.run });
  assert.deepEqual(mirrored, []);
  assert.equal(rclone.calls.length, 0);
  assert.match(lines.join("\n"), /cut\/e003\.mp4: joined parts hash [0-9a-f]{64}, its \.SPLIT note says 0{64}/);
  assert.equal(readMirrorState(box.work).branches["transfer/tn-e003"].commit, undefined);
});

test("rejoin: a gap in the parts is refused; a file kept beside its parts stays as the branch has it", async () => {
  const box = sandbox();
  const stage = path.join(box.box, "stage");
  put(stage, "a.mp4.part00", "1");
  put(stage, "a.mp4.part02", "3");
  assert.match((await rejoinParts(stage)).problem, /a\.mp4: its parts do not run from part00 without a gap/);
  const other = path.join(box.box, "stage2");
  put(other, "b.mp4", "whole");
  put(other, "b.mp4.part00", "wh");
  put(other, "b.mp4.part01", "ole");
  put(other, "c/d.bin.part00", "cd");
  put(other, "c/d.bin.part01", "ef");
  const result = await rejoinParts(other);
  assert.equal(result.problem, null);
  assert.deepEqual(result.kept, ["b.mp4"]);
  assert.deepEqual(result.joined, ["c/d.bin"]);
  assert.deepEqual(listing(other), ["b.mp4", "b.mp4.part00", "b.mp4.part01", "c/d.bin"]);
  assert.equal(readFileSync(path.join(other, "c", "d.bin"), "utf8"), "cdef");
});

test("a round is capped: one branch by default, the rest wait; a full disk waits too", async () => {
  const box = sandbox();
  pushBranch(box, "transfer/zt-live-e001", { "a.txt": "a" });
  pushBranch(box, "transfer/zt-live-e002", { "b.txt": "b" });
  const env = { VIDEO_BRANCH_MIRROR_PER_ROUND: "" };
  const full = await branchMirrorRound({ ...ctxFor(box, { env: { ...env, VIDEO_BRANCH_MIRROR_MIN_FREE_GB: "" } }), branchMirrorFree: () => 1024 ** 3 }, { client: site(), rclone: fakeRclone(box.drive).run });
  assert.deepEqual(full.mirrored, []);
  assert.match(full.lines.join("\n"), /waiting: 1\.0 GB free on the work disk/);
  const first = await branchMirrorRound(ctxFor(box, { env }), { client: site(), rclone: fakeRclone(box.drive).run });
  assert.equal(first.mirrored.length, 1);
  assert.match(first.lines.join("\n"), /1 more branch wait/);
  const second = await branchMirrorRound(ctxFor(box, { env, now: later(5) }), { client: site(), rclone: fakeRclone(box.drive).run });
  assert.equal(second.mirrored.length, 1);
  assert.notEqual(second.mirrored[0].branch, first.mirrored[0].branch);
});

test("cli: the worker prints the mirror's lines after the backup when it is on", async () => {
  const box = sandbox();
  pushBranch(box, "transfer/zt-shared", { "music/theme.mp3": "mp3" });
  const out = [];
  await branchMirrorAfterBackup({ ...ctxFor(box), stdout: { write: (line) => out.push(line) }, backupClient: site(), branchMirrorRclone: fakeRclone(box.drive).run });
  assert.match(out.join(""), /^branch mirror: transfer\/zt-shared [0-9a-f]{12} → drama\/zhong-tian-qu-qi\/_分支\/zt-shared/);
});

test("cli: after the backup the mirror runs, except on the error path (mirror: false), which ends in an owner-policy exit", async () => {
  const box = sandbox();
  pushBranch(box, "transfer/tn-shared", { "sfx/door.wav": "door" });
  const backupSite = { ...site(), config: async () => ({ enabled: true, path: "AI/備份", lock_path: "AI/備份", remote_prefix: "", videos: [] }), lock: async () => ({}), answer: async () => ({}) };
  const run = async (options) => {
    const out = [];
    await backupAfterRound({ ...ctxFor(box), stdout: { write: (line) => out.push(line) }, backupClient: backupSite, backupRclone: fakeRclone(box.drive).run, branchMirrorRclone: fakeRclone(box.drive).run }, options);
    return out.join("");
  };
  assert.doesNotMatch(await run({ mirror: false }), /branch mirror/);
  assert.match(await run(), /branch mirror: transfer\/tn-shared [0-9a-f]{12} → drama\/tai-nainai\/_分支\/tn-shared/);
});
