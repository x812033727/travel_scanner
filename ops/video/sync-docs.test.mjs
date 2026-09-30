import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { chmod, link, lstat, mkdir, mkdtemp, readFile, readdir, readlink, rm, symlink, writeFile } from "node:fs/promises";
import { createServer } from "node:net";
import { tmpdir } from "node:os";
import path from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

import { syncDocs } from "./sync-docs.mjs";

const cli = fileURLToPath(new URL("./sync-docs.mjs", import.meta.url));

async function fixture(t) {
  const root = await mkdtemp(path.join(tmpdir(), "video-docs-"));
  const seed = path.join(root, "seed");
  const target = path.join(root, "volume");
  await mkdir(seed);
  t.after(() => rm(root, { recursive: true, force: true }));
  return { root, seed, target };
}

async function put(root, relative, contents) {
  const destination = path.join(root, relative);
  await mkdir(path.dirname(destination), { recursive: true });
  await writeFile(destination, contents);
}

// Include empty directories and links so abandoned staging entries cannot hide in a snapshot.
async function tree(root) {
  const entries = {};
  for (const name of (await readdir(root)).sort()) {
    const entry = path.join(root, name);
    const stat = await lstat(entry);
    entries[name] = stat.isSymbolicLink() ? { link: await readlink(entry) }
      : stat.isDirectory() ? await tree(entry) : (await readFile(entry)).toString("hex");
  }
  return entries;
}

async function makeLink(t, destination, linkPath, type) {
  try {
    await symlink(destination, linkPath, type);
    return true;
  } catch (error) {
    if (process.platform === "win32" && ["EPERM", "EACCES", "ENOTSUP"].includes(error.code)) {
      t.skip("Windows account cannot create symlinks; Linux smoke runs these cases");
      return false;
    }
    throw error;
  }
}

test("a fresh volume receives root files, lexicon and complete nested video folders", async (t) => {
  const { seed, target } = await fixture(t);
  await put(seed, "README.md", "Current instructions\n");
  await put(seed, "lexicon.json", '{"terms": ["Mokaair"]}\n');
  await put(seed, ".metadata", "hidden root file");
  await put(seed, "pilot/nested/script.json", '{"title":"試播"}\n');
  await put(seed, "pilot/nested/audio.bin", Buffer.from([0, 255, 1, 128]));
  await mkdir(path.join(seed, "pilot", "empty"));
  await syncDocs(seed, target);
  assert.deepEqual(await tree(target), await tree(seed));
  const first = await tree(target);
  await syncDocs(seed, target);
  assert.deepEqual(await tree(target), first, "startup repeats without artifacts or changes");
});

test("a newer image refreshes root docs while worker lexicon, drafts and extra files survive", async (t) => {
  const { seed, target } = await fixture(t);
  await put(seed, "README.md", "image one");
  await put(seed, "lexicon.json", '{"image":1}');
  await put(seed, "pilot/script.json", "image script");
  await syncDocs(seed, target);
  const lexicon = Buffer.from(' { "worker": ["自訂詞"] }\r\n', "utf8");
  await put(target, "lexicon.json", lexicon);
  await put(target, "pilot/script.json", "worker revised script");
  await put(target, "pilot/private/take.wav", Buffer.from([1, 2, 3, 0]));
  await put(target, "worker-only/notes.md", "draft not in the image");
  await put(target, "local-state.json", "worker state");
  await put(target, "retired.md", "keep files removed from newer images");
  const pilot = await tree(path.join(target, "pilot"));
  await put(seed, "README.md", "image two");
  await put(seed, "AUTOMATION.md", "new instructions");
  await put(seed, "lexicon.json", '{"image":2}');
  await put(seed, "pilot/script.json", "new image must not replace a draft");
  await put(seed, "pilot/new-image-file.txt", "must not enter an existing directory");
  await put(seed, "new-series/nested/episode.json", "new image folder");
  await syncDocs(seed, target);
  assert.equal(await readFile(path.join(target, "README.md"), "utf8"), "image two");
  assert.equal(await readFile(path.join(target, "AUTOMATION.md"), "utf8"), "new instructions");
  assert.deepEqual(await readFile(path.join(target, "lexicon.json")), lexicon);
  assert.deepEqual(await tree(path.join(target, "pilot")), pilot);
  assert.equal(await readFile(path.join(target, "worker-only/notes.md"), "utf8"), "draft not in the image");
  assert.equal(await readFile(path.join(target, "local-state.json"), "utf8"), "worker state");
  assert.equal(await readFile(path.join(target, "retired.md"), "utf8"), "keep files removed from newer images");
  assert.deepEqual(await tree(path.join(target, "new-series")), await tree(path.join(seed, "new-series")));
  const updated = await tree(target);
  await syncDocs(seed, target);
  assert.deepEqual(await tree(target), updated);
});

test("root file refresh replaces the file instead of rewriting its existing inode", async (t) => {
  const { root, seed, target } = await fixture(t);
  await put(seed, "README.md", "old complete instructions");
  await syncDocs(seed, target);
  const witness = path.join(root, "old-open-file");
  await link(path.join(target, "README.md"), witness);
  await put(seed, "README.md", "new complete instructions".repeat(1000));
  await syncDocs(seed, target);
  assert.equal(await readFile(witness, "utf8"), "old complete instructions");
  assert.deepEqual(await tree(target), await tree(seed), "no staging files remain");
});

test("missing or non-directory seeds and overlapping paths refuse without consuming worker data", async (t) => {
  const { root, seed, target } = await fixture(t);
  await put(seed, "README.md", "seed");
  await put(target, "draft.txt", "worker");
  const before = await tree(root);
  const fileSeed = path.join(seed, "README.md");
  for (const [from, to] of [
    [path.join(root, "missing"), target], [fileSeed, target], [seed, seed],
    [seed, path.join(seed, "nested-volume")], [seed, root],
  ]) {
    await assert.rejects(async () => syncDocs(from, to));
    assert.deepEqual(await tree(root), before);
  }
});

test("destination type conflicts fail without replacing worker files or directories", async (t) => {
  for (const conflict of ["target-file", "root-file", "video-directory", "lexicon"]) {
    const { seed, target } = await fixture(t);
    if (conflict === "target-file") {
      await put(seed, "README.md", "seed");
      await writeFile(target, "worker");
    } else if (conflict === "root-file" || conflict === "lexicon") {
      const name = conflict === "lexicon" ? "lexicon.json" : "README.md";
      await put(seed, name, "seed");
      await put(target, `${name}/draft.txt`, "worker");
    } else {
      await put(seed, "pilot/script.json", "seed");
      await put(target, "pilot", "worker");
    }
    const before = conflict === "target-file" ? await readFile(target) : await tree(target);
    await assert.rejects(async () => syncDocs(seed, target), conflict);
    const after = conflict === "target-file" ? await readFile(target) : await tree(target);
    assert.deepEqual(after, before);
  }
});

test("seed symlinks are refused at the root and in files or newly seeded folders", async (t) => {
  for (const location of ["root", "file", "nested"]) {
    const { root, seed, target } = await fixture(t);
    const outside = path.join(root, "outside");
    await put(outside, "private.txt", "must not be copied");
    await put(target, "pilot/draft.txt", "worker");
    let source = seed;
    if (location === "root") {
      source = path.join(root, "linked-seed");
      if (!await makeLink(t, seed, source, "dir")) return;
    } else {
      const relative = location === "file" ? "private.txt" : "new-pilot/private.txt";
      await mkdir(path.dirname(path.join(seed, relative)), { recursive: true });
      if (!await makeLink(t, path.join(outside, "private.txt"), path.join(seed, relative), "file")) return;
    }
    const before = await tree(target);
    await assert.rejects(async () => syncDocs(source, target), location);
    assert.deepEqual(await tree(target), before);
  }
});

test("destination symlinks cannot redirect root docs, lexicon or directory writes", async (t) => {
  for (const location of ["root", "README.md", "lexicon.json", "pilot"]) {
    const { root, seed, target } = await fixture(t);
    const outside = path.join(root, "outside");
    await put(outside, "sentinel.txt", "keep outside unchanged");
    if (location === "root") {
      await put(seed, "sentinel.txt", "overwrite attempt");
      if (!await makeLink(t, outside, target, "dir")) return;
    } else {
      await mkdir(target);
      if (location === "pilot") {
        await put(seed, "pilot/sentinel.txt", "overwrite attempt");
        if (!await makeLink(t, outside, path.join(target, location), "dir")) return;
      } else {
        await put(seed, location, "overwrite attempt");
        if (!await makeLink(t, path.join(outside, "sentinel.txt"), path.join(target, location), "file")) return;
      }
    }
    const before = await tree(outside);
    await assert.rejects(async () => syncDocs(seed, target), location);
    assert.deepEqual(await tree(outside), before);
  }
});

test("non-file seed entries are rejected", { skip: process.platform === "win32" }, async (t) => {
  const { seed, target } = await fixture(t);
  const server = createServer();
  await new Promise((resolve, reject) => {
    server.once("error", reject);
    server.listen(path.join(seed, "socket"), resolve);
  });
  try {
    await assert.rejects(async () => syncDocs(seed, target));
  } finally {
    await new Promise((resolve, reject) => server.close((error) => error ? reject(error) : resolve()));
  }
});

test("a failed directory copy leaves no partial folder or staging entries", {
  skip: process.platform === "win32" || process.getuid?.() === 0,
}, async (t) => {
  const { seed, target } = await fixture(t);
  await put(seed, "new-draft/nested/readable.txt", "seed");
  await put(seed, "new-draft/nested/blocked.txt", "unreadable seed");
  await put(target, "worker.txt", "untouched");
  const blocked = path.join(seed, "new-draft/nested/blocked.txt");
  await chmod(blocked, 0);
  try {
    const before = await tree(target);
    await assert.rejects(async () => syncDocs(seed, target));
    assert.deepEqual(await tree(target), before);
  } finally {
    await chmod(blocked, 0o600);
  }
});

test("worker entries appearing during staging keep ownership and incompatible types refuse", async (t) => {
  // Patch only a child process: no shared fs binding or timing race can affect other tests.
  const injectDuringCopy = `
    import fs from "node:fs";
    import path from "node:path";
    import { syncBuiltinESMExports } from "node:module";
    import { pathToFileURL } from "node:url";
    const [helper, seed, target, kind] = process.argv.slice(1);
    process.argv[1] = path.join(path.dirname(helper), "injected-copy-test.mjs");
    const copy = fs.copyFileSync;
    let injected = false;
    fs.copyFileSync = (...args) => {
      const result = copy(...args);
      if (!injected) {
        injected = true;
        if (kind === "lexicon") {
          fs.writeFileSync(path.join(target, "lexicon.json"), "worker terms");
        } else if (kind === "directory") {
          fs.mkdirSync(path.join(target, "new-pilot"));
          fs.writeFileSync(path.join(target, "new-pilot", "worker.txt"), "worker draft");
        } else {
          fs.writeFileSync(path.join(target, "new-pilot"), "worker file");
        }
      }
      return result;
    };
    syncBuiltinESMExports();
    const { syncDocs } = await import(pathToFileURL(helper).href);
    try {
      await syncDocs(seed, target);
      console.log(JSON.stringify({ injected, succeeded: true }));
    } catch (error) {
      console.log(JSON.stringify({ injected, succeeded: false, message: error.message }));
    }
  `;
  for (const kind of ["lexicon", "directory", "file"]) {
    const { seed, target } = await fixture(t);
    await put(seed, kind === "lexicon" ? "lexicon.json" : "new-pilot/image.txt", "seed");
    const child = spawnSync(process.execPath, [
      "--input-type=module", "-e", injectDuringCopy, cli, seed, target, kind,
    ], { encoding: "utf8" });
    assert.ifError(child.error);
    assert.equal(child.status, 0, child.stderr);
    const outcome = JSON.parse(child.stdout);
    assert.equal(outcome.injected, true);
    assert.equal(outcome.succeeded, kind !== "file", child.stdout);
    if (kind === "lexicon") {
      assert.deepEqual(await tree(target), { "lexicon.json": Buffer.from("worker terms").toString("hex") });
    } else if (kind === "directory") {
      assert.deepEqual(await tree(target), { "new-pilot": { "worker.txt": Buffer.from("worker draft").toString("hex") } });
    } else {
      assert.deepEqual(await tree(target), { "new-pilot": Buffer.from("worker file").toString("hex") });
    }
  }
});

test("the startup CLI syncs explicit paths and exits nonzero when the seed is missing", async (t) => {
  const { root, seed, target } = await fixture(t);
  await put(seed, "README.md", "current image");
  const ok = spawnSync(process.execPath, [cli, seed, target], { encoding: "utf8" });
  assert.ifError(ok.error);
  assert.equal(ok.status, 0, ok.stderr);
  assert.deepEqual(await tree(target), await tree(seed));
  const before = await tree(target);
  const failed = spawnSync(process.execPath, [cli, path.join(root, "missing"), target], { encoding: "utf8" });
  assert.ifError(failed.error);
  assert.notEqual(failed.status, 0);
  assert.ok(failed.stderr.trim(), "startup failure includes a diagnostic");
  assert.deepEqual(await tree(target), before);
});
