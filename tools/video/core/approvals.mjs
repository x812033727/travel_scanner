// The owner's approvals, each bound to the exact file approved.
//
// The gates need the site owner: the outline (brief.md), the narration (timeline.json, which
// changes whenever any line is re-synthesized) and the finished video (final.mp4); a drama adds
// the look (characters/manifest.json, the character sheets the owner picks from) and the
// storyboard (keyframes/manifest.json). Recording the SHA-256 of what was approved means an edit
// after the approval silently voids it, and the stages after the gate refuse to run instead of
// shipping something nobody looked at.
import { createHash } from "node:crypto";
import { createReadStream, existsSync, readFileSync } from "node:fs";
import path from "node:path";

import { atomicWrite } from "./paths.mjs";
import { hasAnimePolicy, runtimePolicyHash } from "./anime-policy.mjs";

export const ANIME_APPROVAL_GATES = new Set(["script", "audio", "final", "publish"]);

/** Unmarked historical videos keep their byte-bound approvals; marked episode context is explicit. */
export function approvalRuntimePolicyHash(gate, docDir) {
  if (!ANIME_APPROVAL_GATES.has(gate)) return null;
  const file = path.join(docDir, "video.json");
  if (!existsSync(file)) return null;
  const doc = JSON.parse(readFileSync(file, "utf8"));
  return hasAnimePolicy(doc) ? runtimePolicyHash(doc) : null;
}

export const GATES = {
  outline: ({ docDir }) => path.join(docDir, "brief.md"),
  // A series episode's screenplay (docs/videos/SERIES.md): the narrative only, so a prompt fix
  // by the media stages does not unsettle an approval the owner gave.
  script: ({ docDir }) => path.join(docDir, "script.md"),
  // Drama only (docs/videos/DRAMA.md): the character sheets, then the keyframes before any clip is paid for.
  look: ({ workdir }) => path.join(workdir, "characters", "manifest.json"),
  storyboard: ({ workdir }) => path.join(workdir, "keyframes", "manifest.json"),
  audio: ({ workdir }) => path.join(workdir, "timeline.json"),
  final: ({ workdir }) => path.join(workdir, "final.mp4"),
  // The owner's "this may be uploaded", given on /admin/videos to the package `package` wrote.
  publish: ({ workdir }) => path.join(workdir, "upload", "metadata.json"),
  // The owner's "I uploaded these dub tracks in Studio" (docs/videos/DUBS.md), bound to the
  // manifest `review-push --gate dubs` writes of the tracks it sent.
  dubs: ({ workdir }) => path.join(workdir, "dubs", "manifest.json"),
  // A batch of the languages the owner chose (docs/videos/LANGUAGES.md), bound to the manifest
  // `review-push --gate languages` writes of the parts and files it sent; approved on the site
  // by the owner once the dub tracks are up in Studio, or by the site itself when there is none.
  languages: ({ workdir }) => path.join(workdir, "review", "languages.json"),
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
export async function approve({ gate, docDir, workdir, now = new Date(), note = "", expected_runtime_policy_hash = undefined }) {
  const file = target(gate, { docDir, workdir });
  if (!existsSync(file)) throw new Error(`nothing to approve: ${file} does not exist yet`);
  const hash = approvalRuntimePolicyHash(gate, docDir);
  if (expected_runtime_policy_hash !== undefined && expected_runtime_policy_hash !== hash) throw new Error("the approved runtime policy or episode context has changed; submit the current version for review again");
  const entry = { gate, file: path.basename(file), sha256: await sha256File(file), approved_at: now.toISOString(), note, ...(hash ? { runtime_policy_hash: hash } : {}) };
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
  let hash;
  try { hash = approvalRuntimePolicyHash(gate, docDir); }
  catch { return { status: "stale", entry, sha256 }; }
  const current = !ANIME_APPROVAL_GATES.has(gate) || (entry.runtime_policy_hash ?? null) === hash;
  return { status: entry.sha256 === sha256 && current ? "approved" : "stale", entry, sha256 };
}
