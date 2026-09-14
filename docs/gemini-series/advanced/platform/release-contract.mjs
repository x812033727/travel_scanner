/** Frozen editorial identities and reviewed release files; never imported by the website. */
import { createHash } from "node:crypto";
import { existsSync, readFileSync, readdirSync, realpathSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

export const repositoryRoot = fileURLToPath(new URL("../../../../", import.meta.url));
export const contract = JSON.parse(readFileSync(new URL("./catalogue-contract.json", import.meta.url), "utf8"));
const readJson = (file) => JSON.parse(readFileSync(file, "utf8"));
export const stable = (value) => JSON.stringify(value, (_, item) => item && typeof item === "object" && !Array.isArray(item)
  ? Object.fromEntries(Object.keys(item).sort().map((key) => [key, item[key]])) : item);
const hash = (value) => createHash("sha256").update(value).digest("hex");

export function expectedCatalogue(phase = "base") {
  if (!["base", "advanced"].includes(phase)) throw new Error("Unknown Gemini phase: " + phase);
  const stage = phase === "advanced" ? 2 : 1;
  const articles = contract.articles.filter((entry) => entry.stage <= stage);
  const paths = contract.paths.filter((entry) => entry.stage <= stage);
  if (articles.length !== contract.counts[phase].articles || paths.length !== contract.counts[phase].paths) {
    throw new Error("Frozen catalogue contract is incomplete.");
  }
  return { ...contract, articles, paths };
}

/** An editor-only projection. Runtime catalogue is never overwritten by draft operations. */
export function draftCatalogue(workspace = repositoryRoot) {
  const base = readJson(path.join(workspace, "apps/web/lib/guide-series.json"));
  const plan = readJson(path.join(workspace, "docs/gemini-series/advanced/curriculum.json"));
  return {
    ...base,
    articles: [...base.articles.filter((entry) => entry.number <= 50), ...plan.articles.map((entry) => ({
      number: entry.number, slug: entry.slug, title: entry.title, purpose: entry.purpose,
      group: entry.group, level: entry.level, platforms: entry.platforms, keywords: entry.keywords,
      prerequisites: entry.prerequisites, related: entry.related,
      minutes: entry.estimatedReadingMinutes, labMinutes: entry.estimatedLabMinutes,
      stage: 2, track: entry.track,
    }))],
    paths: [...base.paths.filter((entry) => contract.paths.some((p) => p.stage === 1 && p.id === entry.id)),
      ...plan.routes.map((entry) => ({ ...entry, stage: 2, description: entry.title }))],
  };
}

export function releaseWrites(series, phase = "base", updates = []) {
  const expected = expectedCatalogue(phase);
  if (stable(series.articles.map(({ number, slug }) => ({ number, slug })))
    !== stable(expected.articles.map(({ number, slug }) => ({ number, slug })))) {
    throw new Error("Release catalogue does not match the frozen identities.");
  }
  if (updates.length !== new Set(updates).size || updates.some((slug) => !contract.allowedUpdates.includes(slug))
    || (phase === "base" && updates.length)) throw new Error("Only the two declared plan/cost updates may be added.");
  const children = expected.articles.filter((entry) => phase === "base" || entry.stage === 2).map((entry) => entry.slug);
  const orderedUpdates = contract.allowedUpdates.filter((slug) => updates.includes(slug));
  return [...children, ...orderedUpdates, series.hubSlug];
}

function inside(parent, candidate) {
  const relative = path.relative(realpathSync(parent), realpathSync(candidate));
  return relative !== ".." && !relative.startsWith(".." + path.sep) && !path.isAbsolute(relative);
}

function assetFiles(directory) {
  return readdirSync(directory, { withFileTypes: true }).flatMap((entry) => {
    const file = path.join(directory, entry.name);
    if (entry.isSymbolicLink()) throw new Error("Release assets must not be symlinks: " + file);
    return entry.isDirectory() ? assetFiles(file) : [file];
  });
}

function reviewedFiles(series, workspace) {
  const files = [];
  const workspaceRoot = realpathSync(workspace);
  for (const slug of [...series.articles.map((entry) => entry.slug), series.hubSlug]) {
    if (!/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(slug)) throw new Error("Invalid release slug.");
    const pack = path.join(workspace, "apps/api/app/guides/content", slug + ".json");
    const assets = path.join(workspace, "apps/web/public/guides", slug);
    if (!existsSync(pack) || !existsSync(assets)) throw new Error(slug + ": missing release files");
    for (const file of [pack, ...assetFiles(assets)]) {
      if (!inside(workspaceRoot, file)) throw new Error("Release file escapes the workspace.");
      const relative = path.relative(workspaceRoot, realpathSync(file)).split(path.sep).join("/");
      const text = /\.(json|svg|md|txt|py|mjs|js|toml|html|css|csv|jsonl|ps1|sh|yml|yaml)$/.test(file);
      files.push({ path: relative, slug, encoding: text ? "utf8-lf" : "binary",
        sha256: hash(text ? readFileSync(file, "utf8").replace(/\r\n/g, "\n") : readFileSync(file)) });
    }
  }
  return files.sort((a, b) => a.path.localeCompare(b.path, "en"));
}

export function freezeRelease(series, workspace, { phase = "base", updates = [] } = {}) {
  const payload = {
    schemaVersion: 1, phase, locale: series.locale, hubSlug: series.hubSlug,
    reviewedAt: new Date().toISOString(), catalogueSha256: hash(stable(series)),
    writes: releaseWrites(series, phase, updates),
    verifySlugs: series.articles.map((entry) => entry.slug),
    files: reviewedFiles(series, workspace),
  };
  return { ...payload, releaseId: hash(stable(payload)) };
}

/** Verify file hashes again immediately before writes; this is a receipt, not a signature. */
export function verifyFrozenRelease(manifest, series, workspace) {
  const { releaseId, ...payload } = manifest;
  if (manifest.schemaVersion !== 1 || !/^[a-f0-9]{64}$/.test(releaseId || "") || hash(stable(payload)) !== releaseId) {
    throw new Error("Release manifest is invalid or has been edited.");
  }
  if (manifest.locale !== series.locale || manifest.hubSlug !== series.hubSlug
    || manifest.catalogueSha256 !== hash(stable(series))) throw new Error("Catalogue changed after freeze.");
  const updates = manifest.writes.filter((slug) => contract.allowedUpdates.includes(slug));
  const writes = releaseWrites(series, manifest.phase, manifest.phase === "base" ? [] : updates);
  if (stable(writes) !== stable(manifest.writes)
    || stable(series.articles.map((entry) => entry.slug)) !== stable(manifest.verifySlugs)) {
    throw new Error("Release whitelist or verification targets changed.");
  }
  if (stable(reviewedFiles(series, workspace)) !== stable(manifest.files)) {
    throw new Error("Reviewed content or assets changed after freeze.");
  }
  return manifest;
}

