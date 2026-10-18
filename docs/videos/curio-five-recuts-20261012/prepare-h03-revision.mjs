// One authorized pronunciation revision: exactly H03 JA intro03 + intro05.
// No speech/network. Preserve every prior intro file, keep the visible script,
// copy unchanged raw takes/check caches, and expose exactly two pending requests.
import { createHash } from "node:crypto";
import { existsSync, lstatSync, mkdirSync, readdirSync, readFileSync, unlinkSync } from "node:fs";
import path from "node:path";
import { pathToFileURL } from "node:url";
import { parseArgs } from "node:util";
import { atomicWrite, isInside } from "../../../tools/video/core/paths.mjs";
import { acquireProjectLease } from "../../../tools/video/core/project-lease.mjs";
import { describePlan, loadEpisode, LOCALES } from "./speech.mjs";

export const SAY_REPAIRS = Object.freeze({
  intro03: "十九年後、地質学者くりくがようやく現地へ。倒木をたどって隕石を探しました。",
  intro05: "倒れた木は、はっせんまんぼん。その数字はどこから来たのでしょう。",
});
const hash = (bytes) => createHash("sha256").update(bytes).digest("hex");
const json = (value) => `${JSON.stringify(value, null, 2)}\n`;
const read = (file) => JSON.parse(readFileSync(file, "utf8").replace(/^\uFEFF/, ""));
const need = (value, message) => { if (!value) throw new Error(message); };
const same = (a, b) => JSON.stringify(a) === JSON.stringify(b);
const fileHash = (file) => hash(readFileSync(file));

export function validateRevision(oldSpec, newSpec) {
  const approved = structuredClone(oldSpec);
  const episode = approved.episodes?.find((entry) => entry.slug === "curio-h03");
  need(episode?.locales?.ja?.lines, "H03 Japanese source is missing");
  for (const [id, say] of Object.entries(SAY_REPAIRS)) {
    const line = episode.locales.ja.lines.find((entry) => entry.id === id);
    need(line && line.say === undefined, "the starting script is not revision one");
    line.say = say;
  }
  need(same(approved, newSpec), "only the two approved H03 JA say fields may change");
}

function inventory(root, { skipLeases = false } = {}) {
  const files = {};
  function walk(directory) {
    for (const entry of readdirSync(directory, { withFileTypes: true }).sort((a, b) => a.name.localeCompare(b.name))) {
      const file = path.join(directory, entry.name);
      need(isInside(path.resolve(file), path.resolve(root)), "inventory escaped its exact root");
      const stat = lstatSync(file);
      need(!stat.isSymbolicLink(), "revision source contains a link/junction; inspect before copying");
      if (stat.isDirectory()) walk(file);
      else {
        need(stat.isFile(), "revision source contains a non-file entry");
        const relative = path.relative(root, file).replaceAll("\\", "/");
        if (skipLeases && entry.name === "LEASE") continue;
        files[relative] = fileHash(file);
      }
    }
  }
  walk(root);
  return files;
}

function copyInventory(from, to, files) {
  mkdirSync(to, { recursive: true });
  for (const [relative, sha] of Object.entries(files)) {
    const bytes = readFileSync(path.join(from, relative));
    need(hash(bytes) === sha, `source changed while preserving ${relative}`);
    const target = path.join(to, relative);
    if (existsSync(target)) need(fileHash(target) === sha, `existing preserved file differs: ${relative}`);
    else atomicWrite(target, bytes);
    need(fileHash(target) === sha, `copy verification failed: ${relative}`);
  }
}

/** Archive/copy/install under continuous common+all-locale leases. No API calls. */
export function prepareH03Revision({ oldSpecFile, newSpecFile, sources, out }) {
  const oldSpec = read(oldSpecFile), newSpec = read(newSpecFile);
  validateRevision(oldSpec, newSpec);
  const oldEpisode = oldSpec.episodes.find((entry) => entry.slug === "curio-h03");
  const newEpisode = newSpec.episodes.find((entry) => entry.slug === "curio-h03");
  const oldItems = LOCALES.map((locale) => loadEpisode({ episode: oldEpisode, sources, out, locale }));
  const newItems = LOCALES.map((locale) => loadEpisode({ episode: newEpisode, sources, out, locale }));
  const intro = path.dirname(oldItems[0].directory), slugDir = path.dirname(intro);
  const history = path.join(slugDir, "intro-revisions", "revision-1");
  const staged = path.join(slugDir, "intro-revisions", "revision-2-prepared");
  const operationFile = path.join(slugDir, "intro-revisions", "prepare-revision-2.json");
  const leases = [];
  const verify = () => {
    for (const lease of leases) lease.verify();
    for (const item of oldItems) {
      need(fileHash(item.sourceFile) === item.identity.source_sha256 && fileHash(item.lexiconFile) === item.identity.lexicon_sha256, "source files changed during revision");
      if (item.voiceFile) need(fileHash(item.voiceFile) === item.identity.voice_source_sha256, "original dub voice changed during revision");
    }
    for (const dir of [path.resolve(out), slugDir, intro, ...oldItems.map((item) => item.directory)]) need(!existsSync(path.join(dir, "STOP")), `STOP found at ${dir}`);
    need(fileHash(oldSpecFile) === binding.old_spec_sha256 && fileHash(newSpecFile) === binding.new_spec_sha256, "specification changed during revision");
  };
  const binding = { old_spec_sha256: fileHash(oldSpecFile), new_spec_sha256: fileHash(newSpecFile), old_identities: oldItems.map((item) => item.identity), new_identities: newItems.map((item) => item.identity) };
  try {
    for (const dir of [intro, ...oldItems.map((item) => item.directory)]) leases.push(acquireProjectLease(dir, { owner: "curio-h03-pronunciation-revision" }));
    verify();
    let operation = existsSync(operationFile) ? read(operationFile) : null;
    if (operation) {
      need(same(operation.binding, binding), "revision operation belongs to different scripts/sources");
      need(["preserved", "staged", "installing", "installed"].includes(operation.state), "invalid revision operation state");
      if (operation.state === "installed") return { ...operation, plans: newItems.map(describePlan) };
    } else {
      for (const item of oldItems) need(describePlan(item).pending_lines === 0, "revision one contains unfinished takes");
      const ja = oldItems.find((item) => item.locale === "ja"), check = read(path.join(ja.directory, "check.json"));
      const receipt = read(path.join(ja.directory, "receipt.json"));
      need(same(check.identity, ja.identity), "old check identity changed");
      for (const id of Object.keys(SAY_REPAIRS)) {
        need(check.flags.includes(id) && check.lines[id]?.sha256 === receipt.lines[id]?.sha256, `first retake does not have a current failed check: ${id}`);
        const retakeRoot = path.join(intro, "retakes", `ja-${id}`);
        const first = read(path.join(retakeRoot, "attempt-1", "operation.json"));
        need(!existsSync(path.join(retakeRoot, "attempt-2")), "second extra take already exists; no revision purchase is allowed");
        need(first.state === "committed" && first.attempt === 1 && first.candidate_sha256 === receipt.lines[id].sha256 && same(first.identity, ja.identity), `first retake lineage mismatch: ${id}`);
      }
      const before = inventory(intro);
      copyInventory(intro, history, before);
      need(same(inventory(intro), before), "intro changed while making the complete revision-one snapshot");
      operation = { schema_version: 1, kind: "curio-h03-pronunciation-revision", slug: "curio-h03", state: "preserved", binding, history, staged, before, created_at: new Date().toISOString(), repairs: SAY_REPAIRS, additional_takes: { intro03: { same_text: 1, pronunciation_revision: 1, maximum: 2 }, intro05: { same_text: 1, pronunciation_revision: 1, maximum: 2 } }, owner_listened: false, full_video_approved: false };
      atomicWrite(operationFile, json(operation));
    }
    for (const [relative, sha] of Object.entries(operation.before)) need(fileHash(path.join(history, relative)) === sha, "preserved revision-one history changed");
    if (operation.state === "preserved") {
      const media = Object.fromEntries(Object.entries(operation.before).filter(([relative]) => path.basename(relative) !== "LEASE"));
      // Copy from the immutable history, not a potentially interrupted installation.
      // A prepared directory is created once; later resumes use its saved manifest.
      need(!existsSync(staged), "incomplete staged revision exists; inspect it before resuming");
      copyInventory(history, staged, media);
      const lineage = { revision: 2, reason: "two independently reviewed pronunciation-only say repairs", old_spec_sha256: binding.old_spec_sha256, new_spec_sha256: binding.new_spec_sha256, history, repairs: SAY_REPAIRS, maximum_additional_takes_per_repaired_line: 2, further_retakes_disabled: true, owner_listened: false, full_video_approved: false };
      for (const item of newItems) {
        const dir = path.join(staged, item.locale);
        const receipt = read(path.join(dir, "receipt.json")), check = read(path.join(dir, "check.json"));
        receipt.identity = item.identity;
        Object.assign(receipt, { aligned: false, status: "pronunciation-revision-awaiting-shared-alignment", revision_lineage: lineage });
        check.identity = item.identity;
        Object.assign(check, { ok: false, revision_lineage: lineage, owner_listened: false, full_video_approved: false });
        if (item.locale === "ja") for (const id of Object.keys(SAY_REPAIRS)) {
          delete receipt.lines[id];
          delete check.lines[id];
          const target = path.resolve(dir, "audio", `${id}.wav`);
          need(isInside(target, path.resolve(staged)), "selected removal escaped prepared revision");
          unlinkSync(target);
        }
        atomicWrite(path.join(dir, "receipt.json"), json(receipt));
        atomicWrite(path.join(dir, "check.json"), json(check));
        atomicWrite(path.join(dir, "video.json"), json(item.doc));
      }
      const shared = read(path.join(staged, "shared-timeline.json"));
      Object.assign(shared, { duration_ok: false, padding_ok: false, status: "pronunciation-revision-awaiting-shared-alignment", revision_lineage: lineage });
      atomicWrite(path.join(staged, "shared-timeline.json"), json(shared));
      atomicWrite(path.join(staged, "REVISION.json"), json(lineage));
      atomicWrite(path.join(staged, "RETAKES_DISABLED"), "The two H03 JA repair lines have reached the maximum of two additional takes. No further paid retakes.\n");
      operation.after = inventory(staged);
      operation.removed = ["ja/audio/intro03.wav", "ja/audio/intro05.wav"];
      operation.state = "staged";
      atomicWrite(operationFile, json(operation));
    }
    // Fail closed on any competing write; a partial install can contain only its
    // recorded original or revised bytes. The exact two removals are recoverable.
    const currentFiles = inventory(intro, { skipLeases: true });
    for (const [relative, sha] of Object.entries(currentFiles)) need(sha === operation.before[relative] || sha === operation.after[relative], `concurrent revision conflict: ${relative}`);
    for (const relative of Object.keys(operation.before).filter((name) => path.basename(name) !== "LEASE" && !operation.removed.includes(name))) need(currentFiles[relative], `current intro file disappeared: ${relative}`);
    verify();
    operation.state = "installing";
    atomicWrite(operationFile, json(operation));
    for (const [relative, sha] of Object.entries(operation.after)) {
      verify();
      const bytes = readFileSync(path.join(staged, relative));
      need(hash(bytes) === sha, "prepared revision changed");
      const target = path.join(intro, relative);
      if (!existsSync(target) || fileHash(target) !== sha) atomicWrite(target, bytes);
    }
    for (const relative of operation.removed) {
      verify();
      const target = path.resolve(intro, relative);
      need(isInside(target, path.resolve(intro)) && [path.resolve(intro, "ja/audio/intro03.wav"), path.resolve(intro, "ja/audio/intro05.wav")].includes(target), "removal is outside the exact authorized two files");
      if (existsSync(target)) { need(fileHash(target) === operation.before[relative], "repair clip changed before removal"); unlinkSync(target); }
    }
    need(same(inventory(intro, { skipLeases: true }), operation.after), "installed revision differs from prepared bytes");
    const plans = newItems.map(describePlan);
    need(plans.reduce((sum, plan) => sum + plan.pending_lines, 0) === 2 && plans.find((plan) => plan.locale === "ja").pending_lines === 2, "revision must expose exactly two Japanese pending requests");
    operation.state = "installed";
    operation.installed_at = new Date().toISOString();
    operation.pending_lines = ["ja/intro03", "ja/intro05"];
    operation.pending_billable_characters = plans.reduce((sum, plan) => sum + plan.pending_billable_characters, 0);
    atomicWrite(operationFile, json(operation));
    return { ...operation, plans };
  } finally { for (const lease of leases.reverse()) lease.release(); }
}

export function main(args = process.argv.slice(2)) {
  const { values } = parseArgs({ args, options: Object.fromEntries(["old-spec", "new-spec", "sources", "out"].map((key) => [key, { type: "string" }])) });
  for (const name of ["old-spec", "new-spec", "sources", "out"]) need(values[name], `--${name} is required`);
  const result = prepareH03Revision({ oldSpecFile: values["old-spec"], newSpecFile: values["new-spec"], sources: values.sources, out: values.out });
  console.log(json({ state: result.state, history: result.history, pending_lines: result.pending_lines, pending_billable_characters: result.pending_billable_characters, plans: result.plans.map(({ locale, pending_lines, pending_billable_characters }) => ({ locale, pending_lines, pending_billable_characters })), owner_listened: false }));
}
if (process.argv[1] && import.meta.url === pathToFileURL(path.resolve(process.argv[1])).href) { try { main(); } catch (error) { console.error(error.message); process.exitCode = 1; } }
