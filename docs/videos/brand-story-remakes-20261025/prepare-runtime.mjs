// Prepare a genuinely new, isolated project using the ordinary immutable dictionary lifecycle.
// No provider, backend, approval, or paid operation is called.
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { createHash } from "node:crypto";
import { initializeStoryLexicon } from "../../../tools/video/core/lexicon-store.mjs";
import { writeScreenplay } from "../../../tools/video/core/screenplay.mjs";

const batch = path.dirname(fileURLToPath(import.meta.url));
const repository = path.resolve(batch, "../../..");
const [runtimeArgument, mediaArgument, ...requestedProjects] = process.argv.slice(2);
// Free source initialization only; these identities do not authorize any production spend.
const nonCRemakes = {
  seiko: "story-adapt-seiko-quartz-astron-remake-20261025",
  garmin: "story-garmin-smartphone-pivot-worker-2026-remake-20261025",
  dyson: "story-dyson-japan-first-20261021-remake-20261025",
  doraemon: "story-adapt-doraemon-after-fujiko-remake-20261025",
  "rolling-suitcase": "story-rolling-suitcase-v2-remake-20261025",
};
const allowedProjects = new Set(["c03", "c04", "c05", "c06", "c07", "c08", "c09", "c10", "c11", "c14", "c15", "c19", "c20", ...Object.keys(nonCRemakes)]);
const projectIds = requestedProjects.length ? requestedProjects : ["c04", "c05", "c09"];
if (!runtimeArgument || !mediaArgument || !path.isAbsolute(runtimeArgument) || !path.isAbsolute(mediaArgument)) {
  throw new Error("Usage: node prepare-runtime.mjs <absolute isolated runtime root> <absolute media base> [c03|c04|c05|c06|c07|c08|c09|c10|c11|c14|c15|c19|c20|seiko|garmin|dyson|doraemon|rolling-suitcase ...]");
}
if (new Set(projectIds).size !== projectIds.length || projectIds.some(id => !allowedProjects.has(id))) {
  throw new Error("Choose each supported project at most once; preparing C03 must not overwrite an approved earlier runtime.");
}
const runtime = path.resolve(runtimeArgument);
const media = path.resolve(mediaArgument);
const inside = (parent, child) => child === parent || child.startsWith(parent + path.sep);
if (inside(repository, media) || inside(runtime, media) || inside(repository, runtime)) {
  throw new Error("Runtime and generated media must stay outside the source checkout, and media outside runtime.");
}
const shelf = path.join(runtime, "docs/videos");
fs.mkdirSync(shelf, { recursive: true });
const shared = fs.readFileSync(path.join(repository, "docs/videos/lexicon.json"));
const sharedFile = path.join(shelf, "lexicon.json");
if (fs.existsSync(sharedFile) && !fs.readFileSync(sharedFile).equals(shared)) {
  throw new Error("Existing runtime shared dictionary differs; inspect it instead of replacing it.");
}
if (!fs.existsSync(sharedFile)) fs.writeFileSync(sharedFile, shared);
const hash = file => createHash("sha256").update(fs.readFileSync(file)).digest("hex");
const projects = [];
for (const id of projectIds) {
  const source = path.join(batch, id);
  const doc = JSON.parse(fs.readFileSync(path.join(source, "video.json")));
  const context = JSON.parse(fs.readFileSync(path.join(source, "series.json")));
  const correctIdentity = nonCRemakes[id] ? doc.slug === nonCRemakes[id] : doc.slug.startsWith("story-everyday-") && doc.slug.endsWith("-remake-20261025");
  if (doc.series || !correctIdentity) {
    throw new Error(`${id}: preserve the expected new remake identity and original family; no rebinding or budget-prefix changes`);
  }
  const target = path.join(shelf, doc.slug);
  const workdir = path.join(media, doc.slug);
  for (const file of ["auto.json", "approvals.json", "timeline.json", "narration.wav", "final.mp4"]) {
    if (fs.existsSync(path.join(workdir, file))) throw new Error(`${id}: existing production artifact ${file}; stop and reconcile`);
  }
  fs.mkdirSync(target, { recursive: true });
  const dictionary = initializeStoryLexicon({ root: runtime, slug: doc.slug, workdir, names: context.names ?? [] });
  const files = {};
  const sourceFiles = ["video.json", "brief.md", "series.json", "claims.md"];
  const verification = path.join(source, "verify-1.md");
  if (fs.existsSync(verification)) {
    if (!fs.readFileSync(verification, "utf8").includes(hash(path.join(source, "video.json")))) {
      throw new Error(`${id}: independent verification does not name this exact video; stop and review the changed source`);
    }
    sourceFiles.push("verify-1.md");
  }
  for (const file of sourceFiles) {
    fs.copyFileSync(path.join(source, file), path.join(target, file));
    files[file] = hash(path.join(target, file));
  }
  // Carry the native, source-bound text translations; keep review history outside the runtime.
  for (const locale of ["en", "ja", "ko", "es", "pt", "id", "vi", "th"]) {
    const file = path.join("i18n", `${locale}.json`);
    if (!fs.existsSync(path.join(source, file))) continue;
    JSON.parse(fs.readFileSync(path.join(source, file), "utf8"));
    fs.mkdirSync(path.join(target, "i18n"), { recursive: true });
    fs.copyFileSync(path.join(source, file), path.join(target, file));
    files[file] = hash(path.join(target, file));
  }
  const screenplay = writeScreenplay(target, doc);
  projects.push({ id, slug: doc.slug, source_files_sha256: files, author_script_sha256: hash(path.join(source, "script.md")), runtime_script_sha256: hash(screenplay), lexicon_sha256: dictionary.lexicon_sha256 });
}
fs.writeFileSync(path.join(runtime, "runtime-manifest.json"), JSON.stringify({ schema_version: 1, source_base_commit: "2b20c30d359fe5d93a4ea66f013a52fa20a35c05", projects, paid_calls: 0, backend_writes: 0, approvals_created: 0 }, null, 2) + "\n");
console.log(`Prepared ${projects.length} isolated projects; no media, backend writes, or approvals created.`);
