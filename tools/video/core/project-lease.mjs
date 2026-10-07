// One producer at a time per video project: the worker's unit, a media command run by hand, a
// manual recovery. Each one holds <workdir>/LEASE while it may dispatch a paid request or write the
// project's canonical files (video.json, keyframes/manifest.json), so a second producer meets the
// lease and does nothing, instead of racing the first one's paid answers and overwriting its
// files. A process-local busy set or an empty jobs table is only a snapshot; this file is created
// exclusively (O_EXCL), so two processes cannot both believe they hold it.
//
// The lease is not the owner's approval, and it does not replace the project's STOP file: a
// holder still checks STOP before each paid request and each write. Nothing here touches paid
// receipts, ledgers or pending job ids, so a crash keeps them for the next holder to reconcile.
//
// A lease whose holder certainly died (the same host and boot, and its process is gone or is now
// another process) is taken over, keeping the old record beside it. Anything less certain (another
// host or container, a process that may still run, unreadable bytes) counts as held: zero
// dispatches and zero writes until a person removes the file.
import { randomUUID } from "node:crypto";
import { closeSync, existsSync, fsyncSync, linkSync, mkdirSync, openSync, readFileSync, renameSync, unlinkSync, writeFileSync } from "node:fs";
import os from "node:os";
import path from "node:path";

export const LEASE_FILE = "LEASE";
export const PROJECT_LEASED = "video_project_leased";

export class ProjectLeaseError extends Error {
  constructor(message, { holder = null } = {}) {
    super(message);
    this.code = PROJECT_LEASED;
    this.holder = holder;
  }
}

/** Linux only: what identifies this boot, and a process's start time on it (clock ticks). */
function bootId(io) {
  try { return io.readFile("/proc/sys/kernel/random/boot_id", "utf8").trim() || null; }
  catch { return null; }
}
function startTicks(pid, io) {
  try {
    const stat = io.readFile(`/proc/${pid}/stat`, "utf8");
    // The command name (field 2) may hold spaces and parentheses; the fields after its last ")" start at field 3.
    return stat.slice(stat.lastIndexOf(")") + 2).split(" ")[19] ?? null;
  } catch {
    return null;
  }
}
function running(pid, io) {
  try { io.kill(pid, 0); return true; }
  catch (error) { return error?.code === "EPERM"; }
}

const IO = { readFile: readFileSync, rename: renameSync, kill: (pid, signal) => process.kill(pid, signal), hostname: () => os.hostname(), pid: process.pid };

// This process's leases, by file: the token it wrote and how many holders inside it share it
// (the worker's unit, then a media command it runs in the same process). Released at exit.
const held = new Map();
let exitHook = false;
function releaseAllAtExit() {
  for (const [file, lease] of held) {
    try { if (JSON.parse(readFileSync(file, "utf8")).token === lease.token) unlinkSync(file); }
    catch { /* nothing of ours is left to remove */ }
  }
  held.clear();
}

const leaseFile = (workdir) => path.join(workdir, LEASE_FILE);

/** The lease record in a work directory, or null when there is none; unreadable bytes throw. */
export function leaseHolder(workdir) {
  const file = leaseFile(workdir);
  if (!existsSync(file)) return null;
  let record;
  try { record = JSON.parse(readFileSync(file, "utf8")); }
  catch { throw new ProjectLeaseError(`${file} is unreadable; inspect it and remove it by hand once no producer runs`); }
  if (record?.schema_version !== 1 || typeof record.token !== "string" || !Number.isInteger(record.pid)) {
    throw new ProjectLeaseError(`${file} is not a lease this tool wrote; inspect it and remove it by hand once no producer runs`, { holder: record });
  }
  return record;
}

const describe = (holder) => `${holder.owner || "a producer"} (pid ${holder.pid} on ${holder.host}, since ${holder.acquired_at})`;

/** Whether a lease's holder is certainly gone: same host and boot, and its pid is free or reused. */
function certainlyDead(holder, io) {
  if (holder.host !== io.hostname()) return false;
  const boot = bootId(io);
  if (holder.boot_id && boot && holder.boot_id !== boot) return true;
  if (holder.pid === io.pid) return held.get(holder.file)?.token !== holder.token && holder.start_ticks !== null && startTicks(io.pid, io) !== holder.start_ticks;
  if (!running(holder.pid, io)) return true;
  // A live pid is the holder only if it started when the holder did; without /proc, it may be.
  const ticks = startTicks(holder.pid, io);
  return Boolean(holder.start_ticks && ticks && ticks !== holder.start_ticks);
}

/**
 * Hold the project's lease for `owner` (a short label such as "auto" or "keyframes"), or join
 * this process's own. Returns `{ token, release, verify }`; throws ProjectLeaseError when another
 * producer holds it, or may. `io` is for tests (readFile, kill, hostname, pid).
 */
export function acquireProjectLease(workdir, { owner, now = () => new Date(), io: overrides = {} } = {}) {
  const io = { ...IO, ...overrides };
  const file = leaseFile(workdir);
  const mine = held.get(file);
  if (mine) {
    const holder = leaseHolder(workdir);
    if (holder?.token !== mine.token) {
      held.delete(file);
      throw new ProjectLeaseError(`the project's lease was replaced while this process held it${holder ? `; it is now ${describe(holder)}` : ""}`, { holder });
    }
    mine.count++;
    return handle(file, mine);
  }
  mkdirSync(workdir, { recursive: true });
  const existing = leaseHolder(workdir);
  if (existing) {
    if (!certainlyDead({ ...existing, file }, io)) throw new ProjectLeaseError(`the project is held by ${describe(existing)}; nothing was sent or written`, { holder: existing });
    takeOver(workdir, file, existing, io);
  }
  const record = { schema_version: 1, token: randomUUID(), owner, pid: io.pid, host: io.hostname(), boot_id: bootId(io), start_ticks: startTicks(io.pid, io), acquired_at: now().toISOString() };
  let fd;
  try { fd = openSync(file, "wx", 0o600); }
  catch (error) {
    if (error.code !== "EEXIST") throw error;
    const holder = leaseHolder(workdir);
    throw new ProjectLeaseError(`the project was taken by ${holder ? describe(holder) : "another producer"} a moment ago; nothing was sent or written`, { holder });
  }
  try { writeFileSync(fd, `${JSON.stringify(record, null, 2)}\n`); fsyncSync(fd); }
  finally { closeSync(fd); }
  const lease = { token: record.token, count: 1 };
  held.set(file, lease);
  if (!exitHook) {
    process.on("exit", releaseAllAtExit);
    exitHook = true;
  }
  return handle(file, lease);
}

/**
 * Move a dead holder's lease aside, kept as the record of who held it and when. Two producers can
 * both read the same dead record: the first moves it and creates its own lease, so the second
 * must not move that one. Each moves the file to a name of its own and reads back what it moved;
 * another holder's live lease goes back (link fails if a third has made one since, and then the
 * moved one's holder fails its next verify, before it pays).
 */
function takeOver(workdir, file, dead, io) {
  const moving = path.join(workdir, `${LEASE_FILE}.${randomUUID()}.moving`);
  try { io.rename(file, moving); }
  catch (error) {
    if (error.code === "ENOENT") return; // gone already: the exclusive create below decides
    throw error;
  }
  let moved = null;
  try { moved = JSON.parse(readFileSync(moving, "utf8")); } catch { /* compared below as not the dead one */ }
  if (moved?.token === dead.token) {
    renameSync(moving, path.join(workdir, `${LEASE_FILE}.${dead.token}.dead.json`));
    return;
  }
  try { linkSync(moving, file); unlinkSync(moving); }
  catch { /* a third producer holds the project now; the moved lease is kept beside it */ }
  throw new ProjectLeaseError(`the project was taken by ${moved ? describe(moved) : "another producer"} a moment ago; nothing was sent or written`, { holder: moved });
}

function handle(file, lease) {
  let released = false;
  return {
    token: lease.token,
    /** Throw unless this process still holds the lease: call it before a paid request or a write. */
    verify() {
      const holder = leaseHolder(path.dirname(file));
      if (released || held.get(file) !== lease || holder?.token !== lease.token) {
        throw new ProjectLeaseError(`the project's lease is no longer this process's${holder ? `; it is ${describe(holder)}` : ""}; nothing was sent or written`, { holder });
      }
    },
    /** Give this holder's share back; the file goes once the last holder in the process lets go. */
    release() {
      if (released) return;
      released = true;
      if (held.get(file) !== lease || --lease.count > 0) return;
      held.delete(file);
      try { if (JSON.parse(readFileSync(file, "utf8")).token === lease.token) unlinkSync(file); }
      catch { /* another producer's file, or none: leave it */ }
    },
  };
}

/** Whether this process holds the project's lease right now (a nested holder may join it). */
export function holdsProjectLease(workdir) {
  return held.has(leaseFile(workdir));
}

/**
 * Before a paid request or a canonical write by a command: when this process holds the lease
 * (the worker's unit, which runs the command in its own process), check it is still ours; else
 * take it for the rest of the process (a command run by hand), released at exit. Throws
 * ProjectLeaseError when another producer holds it, or may.
 */
export function requireProjectLease(workdir, { owner, now, io, as = null } = {}) {
  try {
    const file = leaseFile(workdir);
    const mine = held.get(file);
    if (!mine) {
      acquireProjectLease(workdir, { owner, now, io });
      return;
    }
    const holder = leaseHolder(workdir);
    if (holder?.token !== mine.token) {
      held.delete(file);
      throw new ProjectLeaseError(`the project's lease is no longer this process's${holder ? `; it is ${describe(holder)}` : ""}; nothing was sent or written`, { holder });
    }
  } catch (error) {
    // `as` turns the refusal into the caller's own error (a SpeechError, a MediaError), whose
    // exit code its command already maps.
    if (as && error instanceof ProjectLeaseError) throw as(error);
    throw error;
  }
}
