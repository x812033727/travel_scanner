// The owner's approvals, each bound to the exact file approved.
//
// Three gates need the site owner: the outline (brief.md), the narration (timeline.json, which
// changes whenever any line is re-synthesized) and the finished video (final.mp4). Recording the
// SHA-256 of what was approved means an edit after the approval silently voids it, and the
// stages after the gate refuse to run instead of shipping something nobody looked at.
import { createHash } from "node:crypto";
import { createReadStream, existsSync, readFileSync } from "node:fs";
import path from "node:path";

import { atomicWrite } from "./paths.mjs";

export const GATES = {
  outline: ({ docDir }) => path.join(docDir, "brief.md"),
  audio: ({ workdir }) => path.join(workdir, "timeline.json"),
  final: ({ workdir }) => path.join(workdir, "final.mp4"),
  // The owner's "this may be uploaded", given on /admin/videos to the package `package` wrote.
  publish: ({ workdir }) => path.join(workdir, "upload", "metadata.json"),
};

export const approvalsFile = (workdir) => path.join(workdir, "approvals.json");

export function sha256File(file) {
  return new Promise((resolve, reject) => {
    const hash = createHash("sha256");
    createReadStream(file)
      .on("error", reject)
      .on("data", (chunk) => hash.update(chunk))
      .on("end", () => resolve(hash.digest("hex")));
  });
}

export function readApprovals(workdir) {
  const file = approvalsFile(workdir);
  if (!existsSync(file)) return { approvals: [] };
  return JSON.parse(readFileSync(file, "utf8"));
}

function target(gate, places) {
  const locate = GATES[gate];
  if (!locate) throw new Error(`unknown gate "${gate}"; one of ${Object.keys(GATES).join(", ")}`);
  return locate(places);
}

/** Record that the owner approved the gate's file as it is now. */
export async function approve({ gate, docDir, workdir, now = new Date(), note = "" }) {
  const file = target(gate, { docDir, workdir });
  if (!existsSync(file)) throw new Error(`nothing to approve: ${file} does not exist yet`);
  const entry = { gate, file: path.basename(file), sha256: await sha256File(file), approved_at: now.toISOString(), note };
  const record = readApprovals(workdir);
  record.approvals.push(entry);
  atomicWrite(approvalsFile(workdir), `${JSON.stringify(record, null, 2)}\n`);
  return entry;
}

/** approved, stale (the file changed since), missing (never approved) or absent (no file yet). */
export async function approvalState({ gate, docDir, workdir }) {
  const file = target(gate, { docDir, workdir });
  if (!existsSync(file)) return { status: "absent", entry: null };
  const entry = readApprovals(workdir).approvals.filter((each) => each.gate === gate).at(-1) ?? null;
  if (!entry) return { status: "missing", entry: null };
  const sha256 = await sha256File(file);
  return { status: entry.sha256 === sha256 ? "approved" : "stale", entry, sha256 };
}
