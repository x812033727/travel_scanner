/** Validate and release only the reviewed Gemini catalogue through guides-import. */
import { spawnSync } from "node:child_process";
import { appendFileSync, existsSync, readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
import { contract, draftCatalogue, expectedCatalogue, freezeRelease, releaseWrites, stable, verifyFrozenRelease } from "../docs/gemini-series/advanced/platform/release-contract.mjs";
export { draftCatalogue, freezeRelease, verifyFrozenRelease };

export const root = fileURLToPath(new URL("../", import.meta.url));
export const catalogue = JSON.parse(readFileSync(path.join(root, "apps/web/lib/guide-series.json"), "utf8"));
const origin = "https://mokaair.com";
const json = (filename) => JSON.parse(readFileSync(filename, "utf8"));
export const seriesSlugs = (series) => [...series.articles.map((entry) => entry.slug), series.hubSlug];

export function validateCatalogue(series, phase = "base") {
  const errors = [];
  const expected = expectedCatalogue(phase);
  const numbers = series.articles.map((entry) => entry.number);
  const slugs = seriesSlugs(series);
  if (stable(series.articles.map(({ number, slug }) => ({ number, slug }))) !== stable(expected.articles.map(({ number, slug }) => ({ number, slug })))) errors.push("Lessons must match the frozen identities and order exactly.");
  if (series.locale !== expected.locale || series.hubSlug !== expected.hubSlug || new Set(slugs).size !== expected.articles.length + 1) errors.push("Unexpected locale, hub or duplicate slugs.");
  if (stable(series.groups.map((entry) => entry.id)) !== stable(expected.groups)) errors.push("Expected the eight original groups.");
  if (stable(series.paths.map((entry) => entry.id)) !== stable(expected.paths.map((entry) => entry.id))) errors.push("Learning paths must match the frozen contract.");
  for (const entry of series.articles) {
    if (!series.groups.some((group) => group.id === entry.group)) errors.push(`${entry.slug}: unknown group`);
    if (!entry.title || !entry.purpose || !entry.level || !entry.platforms.length || !entry.keywords.length || entry.minutes < 1) errors.push(`${entry.slug}: incomplete discovery metadata`);
    if (entry.related.length < 2 || entry.related.length > 4) errors.push(`${entry.slug}: expected 2–4 related lessons`);
    if (new Set(entry.related).size !== entry.related.length || new Set(entry.prerequisites).size !== entry.prerequisites.length) errors.push(`${entry.slug}: duplicate references`);
    const identity = expected.articles.find((item) => item.number === entry.number);
    if ((entry.stage ?? 1) !== identity?.stage || (identity?.stage === 2 && (entry.track !== identity.track || !Number.isInteger(entry.labMinutes) || entry.labMinutes < 1))) errors.push(`${entry.slug}: invalid stage, track or lab time`);
    for (const number of [...entry.prerequisites, ...entry.related]) {
      if (!numbers.includes(number) || number === entry.number) errors.push(`${entry.slug}: invalid reference ${number}`);
    }
  }
  for (const route of series.paths) {
    if (!route.articles.length || new Set(route.articles).size !== route.articles.length || route.articles.some((number) => !numbers.includes(number))) errors.push(`${route.id}: invalid learning path`);
  }
  for (const command of series.commands) {
    if (!numbers.includes(command.article) || !["提示詞", "CLI 指令", "終端機命令"].includes(command.kind)) errors.push(`${command.command}: invalid command destination or type`);
  }
  const visiting = new Set();
  const visited = new Set();
  function visit(number) {
    if (visiting.has(number)) { errors.push(`Prerequisite cycle at ${number}`); return; }
    if (visited.has(number)) return;
    visiting.add(number);
    const entry = series.articles.find((item) => item.number === number);
    entry?.prerequisites.forEach(visit);
    visiting.delete(number);
    visited.add(number);
  }
  numbers.forEach(visit);
  return errors;
}

export function bodyLength(blocks) {
  return blocks.flatMap((block) => {
    if (block.type === "rich_paragraph") return block.inlines.map((child) => child.text);
    if (block.type === "paragraph") return [block.text];
    if (block.type === "list") return block.items;
    if (block.type === "table") return [...block.header, ...block.rows.flat()];
    if (block.type === "callout") return [block.title, block.text];
    return [];
  }).reduce((total, text) => total + [...text.replace(/\s+/gu, "")].length, 0);
}

export function checkPacks(series = catalogue, workspace = root, { phase = "base", slugs = seriesSlugs(series) } = {}) {
  const errors = validateCatalogue(series, phase);
  const known = new Set(seriesSlugs(series));
  const selected = new Set(slugs);
  if (!slugs.length || selected.size !== slugs.length || slugs.some((slug) => !known.has(slug))) {
    errors.push("Selected packs must be a nonempty, unique subset of the catalogue.");
    return { errors, packs: new Map(), slugs };
  }
  const packs = new Map();
  function readPack(slug) {
    if (packs.has(slug)) return packs.get(slug);
    if (!known.has(slug)) { errors.push(slug + ": unknown linked lesson"); return undefined; }
    let filename = path.join(workspace, "apps/api/app/guides/content", slug + ".json");
    // An isolated draft build may reference unchanged first-phase packs in the checkout.
    if (!existsSync(filename) && !selected.has(slug) && (slug === series.hubSlug || contract.articles.some((entry) => entry.stage === 1 && entry.slug === slug))) {
      filename = path.join(root, "apps/api/app/guides/content", slug + ".json");
    }
    if (!existsSync(filename)) { errors.push(slug + ": missing content pack"); return undefined; }
    let pack;
    try { pack = json(filename); } catch { errors.push(slug + ": invalid JSON"); return undefined; }
    if (pack.slug !== slug || pack.kind !== "life" || !Array.isArray(pack.locales?.[series.locale]?.blocks)) {
      errors.push(slug + ": wrong identity, locale or blocks"); return undefined;
    }
    packs.set(slug, pack);
    return pack;
  }
  for (const slug of slugs) {
    const pack = readPack(slug);
    if (!pack) continue;
    const document = pack.locales[series.locale];
    const blocks = document.blocks;
    if (slug !== series.hubSlug) {
      const length = bodyLength(blocks);
      if (slug !== "gemini-cli-command-reference" && (length < 1800 || length > 3000)) errors.push(slug + ": " + length + " body characters; expected 1800–3000");
      if (!blocks.some((block) => block.type === "code")) errors.push(slug + ": missing copyable example");
      if (!blocks.some((block) => block.type === "rich_paragraph")) errors.push(slug + ": missing inline links");
      if (!blocks.some((block) => block.type === "heading" && /常見問題/.test(block.text))) errors.push(slug + ": missing FAQ section");
    }
    if (!document.sources?.length || document.sources.some((source) => !/^\d{4}-\d{2}-\d{2}$/.test(source.checked_on))) errors.push(slug + ": missing source verification dates");
    if (!document.hero || !blocks.some((block) => block.type === "image")) errors.push(slug + ": missing cover or diagram");
    for (const asset of [document.hero, ...blocks.filter((block) => block.type === "image")].filter(Boolean)) {
      const disk = path.resolve(workspace, "apps/web/public", "." + asset.src);
      const publicRoot = path.resolve(workspace, "apps/web/public") + path.sep;
      if (!disk.startsWith(publicRoot) || !existsSync(disk)) errors.push(slug + ": missing or invalid asset " + asset.src);
    }
    const member = series.articles.find((entry) => entry.slug === slug);
    for (const number of [...(member?.prerequisites || []), ...(member?.related || [])]) {
      const target = series.articles.find((entry) => entry.number === number);
      if (target) readPack(target.slug);
    }
    for (const block of blocks) {
      const links = block.type === "rich_paragraph" ? block.inlines.filter((child) => ["link", "article"].includes(child.type)) : block.type === "link" ? [block] : [];
      for (const link of links) {
        let url;
        try { url = new URL(link.type === "article" ? "/" + series.locale + "/" + (link.kind === "life" ? "life" : "guides/" + link.kind) + "/" + link.slug : link.url, origin); }
        catch { errors.push(slug + ": invalid link URL"); continue; }
        if (url.origin === origin && url.pathname.startsWith("/guides/")) {
          let decoded;
          try { decoded = decodeURIComponent(url.pathname); } catch { errors.push(slug + ": invalid download URL"); continue; }
          const disk = path.resolve(workspace, "apps/web/public", "." + decoded);
          const publicRoot = path.resolve(workspace, "apps/web/public") + path.sep;
          if (!disk.startsWith(publicRoot) || !existsSync(disk)) errors.push(slug + ": missing or invalid download " + url.pathname);
          continue;
        }
        if (url.origin !== origin || !url.pathname.startsWith("/" + series.locale + "/life/")) continue;
        const target = url.pathname.split("/").at(-1);
        if (!known.has(target)) {
          // Since the glossary term links and the relink of raw site URLs (docs/travel-guides.md,
          // "Links") a lesson may link any shipped article, not only a sibling; it has to exist.
          const shipped = [workspace, root].some((base) => existsSync(path.join(base, "apps/api/app/guides/content", target + ".json")));
          if (!shipped) errors.push(slug + ": missing linked article " + target);
          continue;
        }
        const linked = readPack(target);
        if (linked && url.hash && !hasAnchor(linked, url.hash.slice(1), series.locale)) errors.push(slug + ": missing anchor " + target + url.hash);
      }
    }
  }
  for (const command of series.commands) {
    const lesson = series.articles.find((entry) => entry.number === command.article);
    if (!lesson || !selected.has(lesson.slug)) continue;
    const pack = packs.get(lesson.slug);
    if (pack && command.anchor && !hasAnchor(pack, command.anchor, series.locale)) errors.push(command.command + ": missing section " + command.anchor);
  }
  return { errors, packs, slugs };
}
function hasAnchor(pack, anchor, locale) {
  const count = pack.locales[locale].blocks.filter((block) => block.type === "heading" && block.level === 2).length;
  return /^section-\d+$/.test(anchor) && Number(anchor.slice(8)) >= 1 && Number(anchor.slice(8)) <= count;
}

export function importArguments(slugs, { dryRun = false, actorEmail } = {}) {
  if (!slugs.length || new Set(slugs).size !== slugs.length || slugs.some((slug) => !/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(slug))) throw new Error("An explicit, unique slug whitelist is required.");
  const args = ["-m", "app.cli", "guides-import", "--locale", "zh-TW", ...slugs.flatMap((slug) => ["--slug", slug])];
  if (dryRun) args.push("--dry-run");
  else {
    if (!actorEmail) throw new Error("An administrator actor email is required.");
    args.push("--publish", "--actor-email", actorEmail);
  }
  return args;
}

/** Injectable functions keep the ordering and partial-commit behavior independently testable. */
export async function releaseSeries(series, { importPack, verifyPublic, journal, beforeWrite = async () => undefined }, writes = seriesSlugs(series)) {
  if (writes.at(-1) !== series.hubSlug || writes.length !== new Set(writes).size || writes.some((slug) => !seriesSlugs(series).includes(slug))) throw new Error("Invalid release whitelist; hub must be last.");
  const preflight = await importPack(writes, true);
  if (preflight.failed) throw new Error(`dry-run stopped: ${preflight.failed}`);
  for (const slug of writes.slice(0, -1)) {
    await beforeWrite(slug);
    await journal({ slug, state: "starting" });
    const result = await importPack([slug], false);
    if (result.failed) throw new Error(`${slug}: import stopped: ${result.failed}`);
    await verifyPublic(slug);
    await journal({ slug, state: "verified" });
  }
  // Re-read every child immediately before exposing the directory.
  for (const entry of series.articles) await verifyPublic(entry.slug);
  await beforeWrite(series.hubSlug);
  await journal({ slug: series.hubSlug, state: "starting" });
  const result = await importPack([series.hubSlug], false);
  if (result.failed) throw new Error(`${series.hubSlug}: import stopped: ${result.failed}`);
  await verifyPublic(series.hubSlug);
  await journal({ slug: series.hubSlug, state: "verified" });
}

export function parseOptions(args) {
  const booleans = new Set(["draft"]);
  const values = new Set(["phase", "track", "workspace", "manifest", "updates", "python", "actor-email", "api-origin", "journal"]);
  const options = {};
  for (let index = 0; index < args.length; index++) {
    const name = args[index].startsWith("--") ? args[index].slice(2) : "";
    if (!booleans.has(name) && !values.has(name)) throw new Error("Unknown option: " + args[index]);
    if (Object.hasOwn(options, name)) throw new Error("Duplicate option: --" + name);
    if (booleans.has(name)) options[name] = true;
    else {
      const value = args[++index];
      if (!value || value.startsWith("--")) throw new Error("Missing value for --" + name);
      options[name] = value;
    }
  }
  return options;
}

async function main() {
  const [command = "check", ...args] = process.argv.slice(2);
  if (!["check", "freeze", "dry-run", "publish"].includes(command)) throw new Error("Use check|freeze|dry-run|publish. Authoring: check --draft --track md [--workspace dir]. Release: freeze --phase advanced --manifest file; dry-run|publish --phase advanced --manifest file.");
  const options = parseOptions(args);
  const allowed = {
    check: ["phase", "draft", "track", "workspace"],
    freeze: ["phase", "manifest", "updates"],
    "dry-run": ["phase", "manifest", "python"],
    publish: ["phase", "manifest", "python", "actor-email", "api-origin", "journal"],
  };
  for (const name of Object.keys(options)) if (!allowed[command].includes(name)) throw new Error("--" + name + " is not valid for " + command);
  const phase = options.phase || (options.draft ? "advanced" : "base");
  expectedCatalogue(phase);
  if ((options.draft || options.track || options.workspace) && command !== "check") throw new Error("Draft, track and workspace options are check-only; publication uses the installed catalogue.");
  if (options.draft && phase !== "advanced") throw new Error("Draft checks require the advanced phase.");
  if (options.updates && command !== "freeze") throw new Error("--updates is only allowed when freezing a release.");
  const series = options.draft ? draftCatalogue(root) : catalogue;
  let slugs = seriesSlugs(series);
  if (options.track) {
    slugs = series.articles.filter((entry) => entry.stage === 2 && entry.track === options.track).map((entry) => entry.slug);
    if (!slugs.length) throw new Error("Unknown or unavailable track: " + options.track);
  }
  const workspace = options.workspace ? path.resolve(options.workspace) : root;
  const { errors, packs } = checkPacks(series, workspace, { phase, slugs });
  if (errors.length) throw new Error(errors.join("\n"));
  if (command === "check") {
    console.log(slugs.length + " selected Gemini pages: catalogue, length, assets and internal links passed." + (options.draft ? " Draft check only; no publication." : ""));
    return;
  }
  if (command === "freeze") {
    if (!options.manifest) throw new Error("freeze requires a new --manifest path.");
    const manifest = freezeRelease(series, root, { phase, updates: options.updates ? options.updates.split(",") : [] });
    writeFileSync(path.resolve(options.manifest), JSON.stringify(manifest, null, 2) + "\n", { flag: "wx" });
    console.log(JSON.stringify({ releaseId: manifest.releaseId, writes: manifest.writes, reviewedFiles: manifest.files.length }, null, 2));
    return;
  }
  if (phase === "advanced" && !options.manifest) throw new Error("Advanced dry-run and publish require a frozen --manifest.");
  const manifest = options.manifest ? verifyFrozenRelease(json(path.resolve(options.manifest)), series, root) : undefined;
  if (manifest && manifest.phase !== phase) throw new Error("Manifest phase does not match --phase.");
  const writes = manifest?.writes || releaseWrites(series, phase);
  const python = options.python || path.join(root, "apps/api/.venv", process.platform === "win32" ? "Scripts/python.exe" : "bin/python");
  const beforeWrite = async () => { if (manifest) verifyFrozenRelease(manifest, series, root); };
  const importPack = async (selectedSlugs, dryRun) => {
    if (selectedSlugs.some((slug) => !writes.includes(slug))) throw new Error("Import escaped the reviewed whitelist.");
    const run = spawnSync(python, importArguments(selectedSlugs, { dryRun, actorEmail: options["actor-email"] }), { cwd: path.join(root, "apps/api"), encoding: "utf8", windowsHide: true, maxBuffer: 10 * 1024 * 1024 });
    if (run.status !== 0) throw new Error("guides-import failed (" + run.status + "); inspect stderr in the deployment environment before resuming.");
    let report;
    try { report = JSON.parse(run.stdout); } catch { throw new Error("guides-import did not return a JSON report; stop and inspect before resuming."); }
    if (report.failed) throw new Error("guides-import reported partial failure: " + report.failed);
    return report;
  };
  if (command === "dry-run") { console.log(JSON.stringify(await importPack(writes, true), null, 2)); return; }
  if (!options["actor-email"] || !options["api-origin"] || !options.journal) throw new Error("publish requires --actor-email, --api-origin and --journal. Use the approved deployment environment.");
  if (manifest && existsSync(path.resolve(options.journal))) {
    const records = readFileSync(path.resolve(options.journal), "utf8").split(/\r?\n/).filter(Boolean).map((line) => JSON.parse(line));
    if (records.some((record) => record.releaseId !== manifest.releaseId)) throw new Error("Journal belongs to a different release; use a new journal.");
  }
  const api = new URL(options["api-origin"]);
  if (api.protocol !== "https:" && !(api.protocol === "http:" && ["127.0.0.1", "localhost"].includes(api.hostname))) throw new Error("Public verification requires HTTPS or local HTTP.");
  const verifyPublic = async (slug) => {
    const response = await fetch(new URL("/api/v1/guides/life/" + slug + "?locale=" + series.locale + "&verify=" + Date.now(), api), { cache: "no-store", signal: AbortSignal.timeout(20000) });
    if (!response.ok) throw new Error(slug + ": public API returned " + response.status);
    const state = await response.json();
    if (state.status !== "published" || !state.document) throw new Error(slug + ": not publicly readable");
    const expected = packs.get(slug).locales[series.locale];
    for (const key of ["title", "description", "hero", "blocks", "sources"]) {
      if (stable(state.document[key]) !== stable(expected[key])) throw new Error(slug + ": public " + key + " differs from the reviewed pack");
    }
  };
  await releaseSeries(series, {
    importPack, verifyPublic, beforeWrite,
    journal: async (event) => appendFileSync(path.resolve(options.journal), JSON.stringify({ ...event, phase, releaseId: manifest?.releaseId ?? null, at: new Date().toISOString() }) + "\n"),
  }, writes);
  console.log(writes.length + " selected pages published; all " + series.articles.length + " children verified. Visibility activation, browser and sitemap verification remain required.");
}
if (process.argv[1] && pathToFileURL(path.resolve(process.argv[1])).href === import.meta.url) {
  main().catch((error) => { console.error(error.message); process.exitCode = 1; });
}
