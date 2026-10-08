import assert from "node:assert/strict";
import { spawn } from "node:child_process";
import { existsSync, mkdtempSync, readdirSync, readFileSync, renameSync, writeFileSync } from "node:fs";
import os from "node:os";
import path from "node:path";
import test from "node:test";

import { acquireProjectLease, holdsProjectLease, LEASE_FILE, leaseHolder, PROJECT_LEASED, ProjectLeaseError, requireProjectLease } from "./project-lease.mjs";

const MODULE = new URL("./project-lease.mjs", import.meta.url).href;
const workdir = () => mkdtempSync(path.join(os.tmpdir(), "video-lease-"));
const leased = (error) => error instanceof ProjectLeaseError && error.code === PROJECT_LEASED;
const record = (dir) => JSON.parse(readFileSync(path.join(dir, LEASE_FILE), "utf8"));

/** Another process that takes the lease, says so, and then waits; `release` lets it go and exit. */
function holder(t, dir, { release = true } = {}) {
  const script = `
    import { acquireProjectLease } from ${JSON.stringify(MODULE)};
    const lease = acquireProjectLease(${JSON.stringify(dir)}, { owner: "manual recovery" });
    process.stdout.write("held\\n");
    process.stdin.on("data", () => { if (${release}) lease.release(); process.exit(0); });
  `;
  const child = spawn(process.execPath, ["--input-type=module", "-e", script], { stdio: ["pipe", "pipe", "pipe"], windowsHide: true });
  let stdout = "";
  let stderr = "";
  let failure;
  let finished = false;
  child.on("error", (error) => { failure = error; });
  child.stdin.on("error", (error) => { failure = error; });
  child.stderr.on("data", (chunk) => { stderr += chunk; });
  const marked = new Promise((resolve) => {
    child.stdout.on("data", (chunk) => {
      stdout += chunk;
      if (stdout.split(/\r?\n/).includes("held")) resolve();
    });
  });
  const closed = new Promise((resolve) => child.on("close", (code, signal) => {
    finished = true;
    resolve({ code, signal });
  }));
  const problem = (message) => new Error(`${message}${failure ? `: ${failure.message}` : ""}${stderr ? `\n${stderr}` : ""}`);
  const bounded = async (promise, ms, message) => {
    let timer;
    try {
      return await Promise.race([promise, new Promise((_, reject) => {
        timer = setTimeout(() => reject(problem(message)), ms);
      })]);
    } finally {
      clearTimeout(timer);
    }
  };
  // Register cleanup before any readiness or test assertion can fail.
  t.after(async () => {
    try {
      if (!finished) {
        child.kill("SIGKILL");
        await bounded(closed, 5_000, "holder did not close during cleanup");
      }
    } finally {
      child.stdin.destroy();
      child.stdout.destroy();
      child.stderr.destroy();
      if (!finished) child.unref();
    }
  });
  return {
    child,
    ready: () => bounded(Promise.race([marked, closed.then(({ code, signal }) => {
      throw problem(`holder closed before holding (code=${code}, signal=${signal})`);
    })]), 10_000, "holder did not become ready"),
    exited: () => bounded(closed, 5_000, "holder did not exit"),
    release: async () => {
      if (finished) throw problem("holder closed before release");
      child.stdin.end("go\n");
      const result = await bounded(closed, 5_000, "holder did not exit after release");
      assert.deepEqual(result, { code: 0, signal: null }, problem("holder failed after release").message);
      if (failure) throw problem("holder failed after release");
    },
  };
}

test("a lease another live process holds refuses this one, keeps its bytes, and is free once that process lets go", async (t) => {
  const dir = workdir();
  const other = holder(t, dir);
  await other.ready();
  const before = readFileSync(path.join(dir, LEASE_FILE), "utf8");
  assert.throws(() => acquireProjectLease(dir, { owner: "auto" }), (error) => leased(error) && error.holder.pid === other.child.pid && /manual recovery/.test(error.message));
  assert.throws(() => requireProjectLease(dir, { owner: "keyframes" }), leased);
  assert.equal(readFileSync(path.join(dir, LEASE_FILE), "utf8"), before, "the holder's record is not touched");
  await other.release();
  assert.equal(existsSync(path.join(dir, LEASE_FILE)), false, "the holder removed its own lease");
  const lease = acquireProjectLease(dir, { owner: "auto" });
  assert.equal(record(dir).pid, process.pid);
  lease.release();
  assert.equal(existsSync(path.join(dir, LEASE_FILE)), false);
});

test("a process that exits without releasing leaves no lease; one that was killed leaves it, and only a certainly dead holder is taken over", async (t) => {
  const exited = workdir();
  const clean = holder(t, exited, { release: false });
  await clean.ready();
  await clean.release();
  assert.equal(existsSync(path.join(exited, LEASE_FILE)), false, "the exit hook removed it");

  const killed = workdir();
  const crashed = holder(t, killed);
  await crashed.ready();
  const old = record(killed);
  crashed.child.kill("SIGKILL");
  await crashed.exited();
  assert.equal(record(killed).token, old.token, "a killed holder's lease stays");
  const lease = acquireProjectLease(killed, { owner: "auto" });
  assert.notEqual(record(killed).token, old.token);
  const kept = JSON.parse(readFileSync(path.join(killed, `${LEASE_FILE}.${old.token}.dead.json`), "utf8"));
  assert.deepEqual(kept, old, "the dead holder's record is kept beside the new lease");
  lease.release();
});

test("ownership that is only probably over counts as held: another host, a live pid without proof, unreadable bytes", () => {
  const base = { schema_version: 1, token: "11111111-2222-3333-4444-555555555555", owner: "auto", pid: 4242, boot_id: null, start_ticks: null, acquired_at: "2026-10-07T00:00:00.000Z" };
  const elsewhere = workdir();
  writeFileSync(path.join(elsewhere, LEASE_FILE), JSON.stringify({ ...base, host: "another-container" }));
  assert.throws(() => acquireProjectLease(elsewhere, { owner: "auto", io: { kill: () => assert.fail("another host's pid means nothing here") } }), leased);

  const alive = workdir();
  writeFileSync(path.join(alive, LEASE_FILE), JSON.stringify({ ...base, host: os.hostname() }));
  assert.throws(() => acquireProjectLease(alive, { owner: "auto", io: { kill: () => true, readFile: () => { throw new Error("no /proc"); } } }), leased, "a live pid with no start time to compare may be the holder");

  const garbled = workdir();
  writeFileSync(path.join(garbled, LEASE_FILE), "{ not json");
  assert.throws(() => acquireProjectLease(garbled, { owner: "auto" }), leased);
  assert.equal(readFileSync(path.join(garbled, LEASE_FILE), "utf8"), "{ not json", "unreadable bytes are left for a person");
  for (const dir of [elsewhere, alive, garbled]) assert.deepEqual(readdirSync(dir), [LEASE_FILE]);
});

test("a pid now running another process, or this process's own pid from an earlier start, is a dead holder", () => {
  const base = { schema_version: 1, token: "11111111-2222-3333-4444-555555555555", owner: "auto", host: os.hostname(), boot_id: null, acquired_at: "2026-10-07T00:00:00.000Z" };
  const stat = (ticks) => `4242 (node worker) S ${"0 ".repeat(18)}${ticks} 0`;
  const reused = workdir();
  writeFileSync(path.join(reused, LEASE_FILE), JSON.stringify({ ...base, pid: 4242, start_ticks: "100" }));
  const io = { kill: () => true, readFile: (file) => (file.endsWith("/stat") ? stat("200") : assert.fail(file)) };
  acquireProjectLease(reused, { owner: "auto", io }).release();
  // A container restarted: the worker has the same pid as the one that held the lease before.
  const restarted = workdir();
  writeFileSync(path.join(restarted, LEASE_FILE), JSON.stringify({ ...base, pid: process.pid, start_ticks: "100" }));
  acquireProjectLease(restarted, { owner: "auto", io: { readFile: (file) => (file.endsWith("/stat") ? stat("200") : assert.fail(file)) } }).release();
  // Another boot of the same host: whatever held it then is gone.
  const rebooted = workdir();
  writeFileSync(path.join(rebooted, LEASE_FILE), JSON.stringify({ ...base, pid: 4242, start_ticks: "200", boot_id: "old-boot" }));
  acquireProjectLease(rebooted, { owner: "auto", io: { kill: () => true, readFile: (file) => (file.endsWith("boot_id") ? "new-boot\n" : stat("200")) } }).release();
  for (const dir of [reused, restarted, rebooted]) assert.equal(existsSync(path.join(dir, LEASE_FILE)), false);
});

test("holders inside one process share the lease, which goes with the last of them; a replaced lease is no longer this process's", () => {
  const dir = workdir();
  const unit = acquireProjectLease(dir, { owner: "auto" });
  assert.equal(holdsProjectLease(dir), true);
  const nested = acquireProjectLease(dir, { owner: "keyframes" });
  requireProjectLease(dir, { owner: "keyframes" });
  assert.equal(nested.token, unit.token);
  nested.release();
  nested.release();
  assert.ok(existsSync(path.join(dir, LEASE_FILE)), "the unit still holds it");
  unit.verify();
  unit.release();
  assert.equal(existsSync(path.join(dir, LEASE_FILE)), false);
  assert.throws(() => unit.verify(), leased);

  const replaced = workdir();
  const mine = acquireProjectLease(replaced, { owner: "auto" });
  writeFileSync(path.join(replaced, LEASE_FILE), JSON.stringify({ ...record(replaced), token: "99999999-2222-3333-4444-555555555555", owner: "someone by hand" }));
  assert.throws(() => mine.verify(), (error) => leased(error) && /someone by hand/.test(error.message));
  assert.throws(() => requireProjectLease(replaced, { owner: "keyframes" }), leased);
  mine.release();
  assert.equal(leaseHolder(replaced).owner, "someone by hand", "release never removes another producer's file");
});

test("two producers that read the same dead lease: the second puts the first one's new lease back instead of taking it", () => {
  const dir = workdir();
  const dead = { schema_version: 1, token: "11111111-2222-3333-4444-555555555555", owner: "auto", pid: 4242, host: os.hostname(), boot_id: null, start_ticks: null, acquired_at: "2026-10-07T00:00:00.000Z" };
  const live = { ...dead, token: "22222222-2222-3333-4444-555555555555", owner: "the first taker", pid: 4343, host: "another-container" };
  writeFileSync(path.join(dir, LEASE_FILE), JSON.stringify(dead));
  // Between this producer's read of the dead record and its move, the first taker moved it and made its own lease.
  const io = {
    kill: () => { throw Object.assign(new Error("no such process"), { code: "ESRCH" }); },
    rename: (from, to) => {
      if (from.endsWith(LEASE_FILE)) writeFileSync(from, JSON.stringify(live));
      return renameSync(from, to);
    },
  };
  assert.throws(() => acquireProjectLease(dir, { owner: "auto", io }), (error) => leased(error) && /the first taker/.test(error.message));
  assert.equal(record(dir).token, live.token, "the first taker's lease is back in place");
  assert.deepEqual(readdirSync(dir), [LEASE_FILE], "nothing of it is left aside, and the dead record is not overwritten");
});
