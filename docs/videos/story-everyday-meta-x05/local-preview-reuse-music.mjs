// Import a previous track from this owner's media work base for a LOCAL CONCEPT only.
// The result stays under review/local-preview/; official music/manifest.json is untouched.
import { copyFileSync, existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { parseArgs } from "node:util";

import { sha256File } from "../../../tools/video/core/approvals.mjs";
import { mixHash, resolveMusic } from "../../../tools/video/core/drama.mjs";
import { isInside, resolveWorkBase, resolveWorkdir, ROOT } from "../../../tools/video/core/paths.mjs";
import { loadProject } from "../../../tools/video/core/state.mjs";

const SLUG = "story-everyday-meta-x05";
const CONCEPT_MANIFEST = "review/local-preview/reused-music.json";
const slugPattern = /^story-everyday-[a-z0-9-]+$/;
const readJson = (file) => JSON.parse(readFileSync(file, "utf8"));

export async function prepareConceptMusic({ workBase, sourceSlug, dryRun = false }) {
  if (!slugPattern.test(sourceSlug) || sourceSlug === SLUG) throw new Error("source slug must be a different story-everyday video");
  const { doc } = loadProject({ slug: SLUG, root: ROOT });
  const workdir = resolveWorkdir({ flag: workBase, slug: SLUG, root: ROOT });
  const sourceDir = path.join(workBase, sourceSlug);
  const sourceManifestFile = path.join(sourceDir, "music/manifest.json");
  const sourceManifest = readJson(sourceManifestFile);
  const music = resolveMusic(doc);
  if (sourceManifest.source !== "generated" || sourceManifest.model?.provider !== "gemini" || sourceManifest.model?.model !== "lyria-3.5"
    || sourceManifest.prompt !== music?.prompt || !sourceManifest.file || !sourceManifest.sha256) {
    throw new Error("source track is not a matching locally generated Lyria bed");
  }
  const sourceFile = path.resolve(sourceDir, sourceManifest.file);
  if (!isInside(sourceFile, sourceDir) || !existsSync(sourceFile)) throw new Error("source track file is missing or outside its workdir");
  const sourceSha = await sha256File(sourceFile);
  if (sourceSha !== sourceManifest.sha256) throw new Error("source track SHA differs from its generation manifest");
  const sourceLedger = readJson(path.join(sourceDir, "media/ledger.json"));
  const booked = sourceLedger.entries?.find((entry) => entry.stage === "music" && entry.kind === "music"
    && entry.status === "ready" && entry.key === sourceManifest.key && entry.provider === "gemini" && entry.model === "lyria-3.5");
  if (!booked) throw new Error("source track has no matching completed music ledger entry");

  const file = `review/local-preview/reused-${sourceSlug}.mp3`;
  const target = path.join(workdir, file);
  const manifest = {
    mix_hash: mixHash(doc), source: "local-concept-reuse", file, sha256: sourceSha,
    seconds: sourceManifest.seconds, prompt: music.prompt,
    reused_from: {
      source: "generated", slug: sourceSlug, file: sourceManifest.file, sha256: sourceSha,
      original_manifest_sha256: await sha256File(sourceManifestFile), generated_at: sourceManifest.generated_at,
      model: sourceManifest.model, original_cost_usd: booked.cost_usd, original_job_id: booked.job_id,
      scope: "local-concept-only; no new music quota or charge",
    },
  };
  if (!dryRun) {
    mkdirSync(path.dirname(target), { recursive: true });
    if (existsSync(target) && await sha256File(target) !== sourceSha) throw new Error("existing concept track has different bytes");
    if (!existsSync(target)) copyFileSync(sourceFile, target);
    writeFileSync(path.join(workdir, CONCEPT_MANIFEST), `${JSON.stringify(manifest, null, 2)}\n`);
  }
  return { manifest, concept_manifest: CONCEPT_MANIFEST, dry_run: dryRun };
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  try {
    const { values } = parseArgs({ args: process.argv.slice(2), options: {
      workdir: { type: "string" }, "source-slug": { type: "string" }, "dry-run": { type: "boolean" },
    }, strict: true });
    if (!values.workdir || !values["source-slug"]) throw new Error("usage: local-preview-reuse-music.mjs --workdir <work base> --source-slug <slug> [--dry-run]");
    const workBase = resolveWorkBase({ flag: values.workdir, root: ROOT });
    const result = await prepareConceptMusic({ workBase, sourceSlug: values["source-slug"], dryRun: values["dry-run"] });
    process.stdout.write(`${result.dry_run ? "would prepare" : "prepared"} local concept music from ${result.manifest.reused_from.slug}, SHA ${result.manifest.sha256}; ${result.concept_manifest}\n`);
  } catch (error) { process.stderr.write(`${error.message}\n`); process.exitCode = 1; }
}
