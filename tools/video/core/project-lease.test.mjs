import assert from "node:assert/strict";
import { spawn } from "node:child_process";
import { existsSync, mkdtempSync, readdirSync, readFileSync, writeFileSync } from "node:fs";
import os from "node:os";
import path from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

import { acquireProjectLease, holdsProjectLease, LEASE_FILE, leaseHolder, PROJECT_LEASED, ProjectLeaseError, requireProjectLease } from "./project-lease.mjs";

const MODULE = fileURLToPath(new URL("./project-lease.mjs", import.meta.url));
const workdir = () => mkdtempSync(path.join(os.tmpdir(), "video-lease-"));
const leased = (error) => error instanceof ProjectLeaseError && error.code === PROJECT_LEASED;
const record = (dir) => JSON.parse(readFileSync(path.join(dir, LEASE_FILE), "utf8"));

/** Another process that takes the lease, says so, and then waits; `release` lets it go and exit. */
function holder(dir, { release = true } = {}) {
  const script = `
    import { acquireProjectLease } from ${JSON.stringify(MODULE)};
    const lease = acquireProjectLease(${JSON.stringify(dir)}, { owner: "manual recovery" });
    process.stdout.write("held\\n");
    process.stdin.on("data", () => { if (${release}) lease.release(); process.exit(0); });
  `;
  const child = spawn(process.execPath, ["--input-type=module", "-e", script], { stdio: ["pipe", "pipe", "inherit"] });
  const ready = new Promise((resolve, reject) => {
    child.stdout.on("data", (chunk) => String(chunk).includes("held") && resolve());
    child.on("exit", (code) => reject(new Error(`holder exited ${code} before holding`)));
  });
  const exited = new Promise((resolve) => child.on("exit", resolve));
  return { child, ready, exited };
}

test("a lease another live process holds refuses this one, keeps its bytes, and is free once that process lets go", async () => {
  const dir = workdir();
  const other = holder(dir);
  await other.ready;
  const before = readFileSync(path.join(dir, LEASE_FILE), "utf8");
  assert.throws(() => acquireProjectLease(dir, { owner: "auto" }), (error) => leased(error) && error.holder.pid === other.child.pid && /manual recovery/.test(error.message));
  assert.throws(() => requireProjectLease(dir, { owner: "keyframes" }), leased);
  assert.equal(readFileSync(path.join(dir, LEASE_FILE), "utf8"), before, "the holder's record is not touched");
  other.child.stdin.write("go\n");
  await other.exited;
  assert.equal(existsSync(path.join(dir, LEASE_FILE)), false, "the holder removed its own lease");
  const lease = acquireProjectLease(dir, { owner: "auto" });
  assert.equal(record(dir).pid, process.pid);
  lease.release();
  assert.equal(existsSync(path.join(dir, LEASE_FILE)), false);
});

test("a process that exits without releasing leaves no lease; one that was killed leaves it, and only a certainly dead holder is taken over", async () => {
  const exited = workdir();
  const clean = holder(exited, { release: false });
  await clean.ready;
  clean.child.stdin.write("go\n");
  await clean.exited;
  assert.equal(existsSync(path.join(exited, LEASE_FILE)), false, "the exit hook removed it");

  const killed = workdir();
  const crashed = holder(killed);
  await crashed.ready;
  const old = record(killed);
  crashed.child.kill("SIGKILL");
  await crashed.exited;
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
