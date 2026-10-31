#!/usr/bin/env node
// Read-only, fail-closed branding prerequisite for this batch. Never pins or renders a film.
import { createHash } from "node:crypto";
import { existsSync, lstatSync, readFileSync, readdirSync, realpathSync, statSync, writeFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
import { parseArgs } from "node:util";

const here = path.dirname(fileURLToPath(import.meta.url));
const json = (file) => JSON.parse(readFileSync(file, "utf8"));
const sha = (bytes) => createHash("sha256").update(bytes).digest("hex");
const same = (actual, expected, label) => { if (actual !== expected) throw new Error(`${label}: expected ${expected}, got ${actual}`); };
const report = { observed_at: new Date().toISOString(), passed: false, paid_requests: 0, story_media_generated: 0, pins_written: 0, rendered: false };
let receipt;
try {
  const { values } = parseArgs({ options: { "project-root": { type: "string" }, slug: { type: "string" }, receipt: { type: "string" }, "adopt-branding": { type: "boolean" } }, strict: true });
  const requestedReceipt = values.receipt && path.resolve(values.receipt);
  // A receipt is optional; writes stay in this batch's external evidence directory.
  if (requestedReceipt && !requestedReceipt.startsWith("/workspace/work/brand-story-20261025/branding-pr1860-evidence/")) throw new Error("receipt must be under this batch's external branding-pr1860-evidence directory");
  receipt = requestedReceipt;
  if (Boolean(values["project-root"]) !== Boolean(values.slug)) throw new Error("pass --project-root and --slug together, or neither for package-only verification");
  const required = json(path.join(here, "required-branding.json"));
  const provenance = json(path.join(here, "source-provenance.json"));
  same(sha(readFileSync(path.join(here, "media-qa.json"))), required.qa_receipt_sha256, "reference full-decode receipt SHA-256");
  const files = [];
  function walk(directory, prefix = "") {
    for (const name of readdirSync(directory).sort()) {
      if (name === "node_modules") continue;
      const file = path.join(directory, name), relative = path.posix.join(prefix, name), stat = lstatSync(file);
      if (stat.isDirectory()) walk(file, relative);
      else if (stat.isFile()) files.push({ path: relative, sha256: sha(readFileSync(file)), bytes: stat.size });
      else throw new Error(`unexpected archive entry ${relative}`);
    }
  }
  walk(provenance.tool_root);
  same(files.length, provenance.regular_files, "reviewed tool file count");
  same(sha(JSON.stringify(files)), provenance.archive_tree_sha256, "reviewed tool tree SHA-256");
  const load = (relative) => import(pathToFileURL(path.join(provenance.tool_root, relative)).href);
  const core = await load("tools/video/core/branding.mjs");
  const { explainerSeries } = await load("tools/video/core/drama.mjs");
  const { verifyBrandingAssets } = await load("tools/video/assemble/branding.mjs");
  const { brandingStatus } = await load("tools/video/media/client.mjs");
  const { readCredentials } = await load("tools/video/tts/credentials.mjs");
  const local = core.readCurrentBranding(required.media_base);
  if (!local) throw new Error("required channel branding is missing or disabled");
  same(local.id, required.id, "local package id");
  same(local.hash, required.package_hash, "local package hash");
  const brandingDirectory = realpathSync(path.join(required.media_base, "_branding"));
  for (const role of ["intro", "outro"]) {
    const file = realpathSync(local[role].file);
    if (!file.startsWith(`${brandingDirectory}${path.sep}`)) throw new Error(`${role} resolves outside this task's installed branding directory`);
    same(local[role].sha256, required[role].sha256, `${role} declared SHA-256`);
    same(local[role].frames, required[role].frames, `${role} declared frames`);
    same(statSync(file).size, required[role].size, `${role} bytes`);
  }
  // Official installer validation recomputes both file hashes and probes packets, size, fps and audio.
  await verifyBrandingAssets(local);
  const { site, token } = readCredentials();
  if (!token) throw new Error("video-tool credential is absent; current site package cannot be verified");
  const requests = [];
  report.requests = requests;
  const remote = await brandingStatus({ site, token, attempts: 1, sleep: async () => {}, fetchImpl: async (url, init) => {
    const response = await fetch(url, { ...init, signal: AbortSignal.timeout(10_000) });
    requests.push({ method: "GET", url: String(url), status: response.status });
    return response;
  } });
  same(remote.series, null, "site channel selector");
  same(remote.id, local.id, "site/local package id");
  same(remote.hash, local.hash, "site/local package hash");
  for (const role of ["intro", "outro"]) for (const field of ["sha256", "frames", "size"]) same(remote[role][field], required[role][field], `site ${role} ${field}`);
  report.package = { id: local.id, hash: local.hash, media_base: required.media_base, intro: remote.intro, outro: remote.outro };
  if (values.slug) {
    if (!/^story-[a-z0-9-]+-remake-20261025$/.test(values.slug)) throw new Error("slug is outside this brand-story remake batch");
    const root = realpathSync(values["project-root"]), directory = path.join(root, "docs", "videos", values.slug);
    const doc = json(path.join(directory, "video.json")), series = json(path.join(directory, "series.json"));
    same(doc.slug, values.slug, "project slug");
    same(series.kind, "story", "project series kind");
    if (series.compilation === true) throw new Error("a compilation episode suppresses bookends and cannot use this per-episode profile");
    if (doc.series != null) throw new Error("this batch must not be rebound to a drama series for branding");
    same(explainerSeries(doc), null, "native branding selector (sothatswhy is a different package)");
    const selected = await core.selectBrandingForBuild({ doc, series, workBase: required.media_base, workdir: path.join(required.media_base, values.slug), introAfterCondensation: true, adoptCurrent: Boolean(values["adopt-branding"]) });
    if (!selected) throw new Error("native assembly would select no branding");
    same(selected.id, required.id, "native selected id");
    same(selected.hash, required.placed_hash, "native selected placement hash");
    same(selected.intro_at, required.intro_at, "native intro placement");
    for (const role of ["intro", "outro"]) {
      same(selected[role].sha256, required[role].sha256, `native ${role} SHA-256`);
      same(selected[role].frames, required[role].frames, `native ${role} frames`);
    }
    await verifyBrandingAssets(selected);
    report.project = { root, slug: values.slug, selector: null, selected_hash: selected.hash, intro_at: selected.intro_at, adopt_current: Boolean(values["adopt-branding"]), existing_pin: existsSync(path.join(required.media_base, values.slug, "branding.json")), source_sha256: sha(readFileSync(path.join(directory, "video.json"))), series_sha256: sha(readFileSync(path.join(directory, "series.json"))), timeline_created: false };
  }
  report.passed = true;
} catch (error) {
  report.error = { message: error.message, ...(error.code ? { code: error.code } : {}), ...(error.status ? { status: error.status } : {}) };
  process.exitCode = 1;
}
report.finished_at = new Date().toISOString();
const bytes = `${JSON.stringify(report, null, 2)}\n`;
if (receipt) writeFileSync(receipt, bytes);
process.stdout.write(bytes);
