/** Validate and release only the reviewed Gemini catalogue through guides-import. */
import { spawnSync } from "node:child_process";
import { appendFileSync, existsSync, readFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

export const root = fileURLToPath(new URL("../", import.meta.url));
export const catalogue = JSON.parse(readFileSync(path.join(root, "apps/web/lib/guide-series.json"), "utf8"));
const origin = "https://mokaair.com";
const json = (filename) => JSON.parse(readFileSync(filename, "utf8"));
export const seriesSlugs = (series) => [...series.articles.map((entry) => entry.slug), series.hubSlug];

export function validateCatalogue(series) {
  const errors = [];
  const numbers = series.articles.map((entry) => entry.number);
  const slugs = seriesSlugs(series);
  if (numbers.length !== 50 || numbers.some((number, index) => number !== index + 1)) errors.push("Lessons must be ordered 1–50 exactly once.");
  if (new Set(slugs).size !== 51) errors.push("Expected 51 distinct slugs including the hub.");
  if (series.groups.length !== 8 || new Set(series.groups.map((entry) => entry.id)).size !== 8) errors.push("Expected eight distinct groups.");
  if (series.paths.length !== 5) errors.push("Expected five learning paths.");
  for (const entry of series.articles) {
    if (!series.groups.some((group) => group.id === entry.group)) errors.push(`${entry.slug}: unknown group`);
    if (!entry.title || !entry.purpose || !entry.level || !entry.platforms.length || !entry.keywords.length || entry.minutes < 1) errors.push(`${entry.slug}: incomplete discovery metadata`);
    if (entry.related.length < 2 || entry.related.length > 4) errors.push(`${entry.slug}: expected 2–4 related lessons`);
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

export function checkPacks(series = catalogue, workspace = root) {
  const errors = validateCatalogue(series);
  const packs = new Map();
  for (const slug of seriesSlugs(series)) {
    const filename = path.join(workspace, "apps/api/app/guides/content", `${slug}.json`);
    if (!existsSync(filename)) { errors.push(`${slug}: missing content pack`); continue; }
    let pack;
    try { pack = json(filename); } catch { errors.push(`${slug}: invalid JSON`); continue; }
    const document = pack.locales?.[series.locale];
    if (pack.slug !== slug || pack.kind !== "life" || !document) { errors.push(`${slug}: wrong identity or locale`); continue; }
    packs.set(slug, pack);
    const blocks = document.blocks;
    if (slug !== series.hubSlug) {
      const length = bodyLength(blocks);
      if (slug !== "gemini-cli-command-reference" && (length < 1800 || length > 3000)) errors.push(`${slug}: ${length} body characters; expected 1800–3000`);
      if (!blocks.some((block) => block.type === "code")) errors.push(`${slug}: missing copyable example`);
      if (!blocks.some((block) => block.type === "rich_paragraph")) errors.push(`${slug}: missing inline links`);
      if (!blocks.some((block) => block.type === "heading" && /常見問題/.test(block.text))) errors.push(`${slug}: missing FAQ section`);
    }
    if (!document.sources?.length || document.sources.some((source) => !/^\d{4}-\d{2}-\d{2}$/.test(source.checked_on))) errors.push(`${slug}: missing source verification dates`);
    if (!document.hero || !blocks.some((block) => block.type === "image")) errors.push(`${slug}: missing cover or diagram`);
    for (const asset of [document.hero, ...blocks.filter((block) => block.type === "image")].filter(Boolean)) {
      const src = asset.src;
      const disk = path.resolve(workspace, "apps/web/public", `.${src}`);
      const publicRoot = path.resolve(workspace, "apps/web/public") + path.sep;
      if (!disk.startsWith(publicRoot) || !existsSync(disk)) errors.push(`${slug}: missing or invalid asset ${src}`);
    }
  }
  for (const [slug, pack] of packs) {
    for (const block of pack.locales[series.locale].blocks) {
      const links = block.type === "rich_paragraph" ? block.inlines.filter((child) => child.type === "link") : block.type === "link" ? [block] : [];
      for (const link of links) {
        const url = new URL(link.url, origin);
        if (url.origin !== origin || !url.pathname.startsWith(`/${series.locale}/life/`)) continue;
        const target = url.pathname.split("/").at(-1);
        if (!packs.has(target)) errors.push(`${slug}: missing linked lesson ${target}`);
        else if (url.hash && !hasAnchor(packs.get(target), url.hash.slice(1), series.locale)) errors.push(`${slug}: missing anchor ${target}${url.hash}`);
      }
    }
  }
  for (const command of series.commands) {
    const lesson = series.articles.find((entry) => entry.number === command.article);
    const pack = lesson && packs.get(lesson.slug);
    if (pack && command.anchor && !hasAnchor(pack, command.anchor, series.locale)) errors.push(`${command.command}: missing section ${command.anchor}`);
  }
  return { errors, packs };
}

function hasAnchor(pack, anchor, locale) {
  const count = pack.locales[locale].blocks.filter((block) => block.type === "heading" && block.level === 2).length;
  return /^section-\d+$/.test(anchor) && Number(anchor.slice(8)) >= 1 && Number(anchor.slice(8)) <= count;
}

export function importArguments(slugs, { dryRun = false, actorEmail } = {}) {
  const args = ["-m", "app.cli", "guides-import", "--locale", "zh-TW", ...slugs.flatMap((slug) => ["--slug", slug])];
  if (dryRun) args.push("--dry-run");
  else {
    if (!actorEmail) throw new Error("An administrator actor email is required.");
    args.push("--publish", "--actor-email", actorEmail);
  }
  return args;
}

/** Injectable functions keep the ordering and partial-commit behavior independently testable. */
export async function releaseSeries(series, { importPack, verifyPublic, journal }) {
  const preflight = await importPack(seriesSlugs(series), true);
  if (preflight.failed) throw new Error(`dry-run stopped: ${preflight.failed}`);
  for (const slug of series.articles.map((entry) => entry.slug)) {
    await journal({ slug, state: "starting" });
    const result = await importPack([slug], false);
    if (result.failed) throw new Error(`${slug}: import stopped: ${result.failed}`);
    await verifyPublic(slug);
    await journal({ slug, state: "verified" });
  }
  // Re-read every child immediately before exposing the directory.
  for (const entry of series.articles) await verifyPublic(entry.slug);
  await journal({ slug: series.hubSlug, state: "starting" });
  const result = await importPack([series.hubSlug], false);
  if (result.failed) throw new Error(`${series.hubSlug}: import stopped: ${result.failed}`);
  await verifyPublic(series.hubSlug);
  await journal({ slug: series.hubSlug, state: "verified" });
}

async function main() {
  const [command = "check", ...args] = process.argv.slice(2);
  const options = Object.fromEntries(args.reduce((pairs, item, index) => item.startsWith("--") ? [...pairs, [item.slice(2), args[index + 1]]] : pairs, []));
  const { errors, packs } = checkPacks();
  if (errors.length) throw new Error(errors.join("\n"));
  if (command === "check") { console.log("51 Gemini pages: catalogue, length, assets and internal links passed."); return; }
  if (!["dry-run", "publish"].includes(command)) throw new Error("Usage: node tools/gemini-series.mjs check|dry-run|publish [--python path] [--actor-email email] [--api-origin URL] [--journal path]");
  const python = options.python || path.join(root, "apps/api/.venv", process.platform === "win32" ? "Scripts/python.exe" : "bin/python");
  const importPack = async (slugs, dryRun) => {
    const run = spawnSync(python, importArguments(slugs, { dryRun, actorEmail: options["actor-email"] }), { cwd: path.join(root, "apps/api"), encoding: "utf8", windowsHide: true, maxBuffer: 10 * 1024 * 1024 });
    if (run.status !== 0) throw new Error(`guides-import failed (${run.status}); inspect stderr in the deployment environment before resuming.`);
    let report;
    try { report = JSON.parse(run.stdout); } catch { throw new Error("guides-import did not return a JSON report; stop and inspect before resuming."); }
    if (report.failed) throw new Error(`guides-import reported partial failure: ${report.failed}`);
    return report;
  };
  if (command === "dry-run") { console.log(JSON.stringify(await importPack(seriesSlugs(catalogue), true), null, 2)); return; }
  if (!options["actor-email"] || !options["api-origin"] || !options.journal) throw new Error("publish requires --actor-email, --api-origin and --journal. Use the approved deployment environment.");
  const api = new URL(options["api-origin"]);
  if (api.protocol !== "https:" && !["127.0.0.1", "localhost"].includes(api.hostname)) throw new Error("Public verification requires HTTPS.");
  const verifyPublic = async (slug) => {
    const response = await fetch(new URL(`/api/v1/guides/life/${slug}?locale=zh-TW&verify=${Date.now()}`, api), { cache: "no-store", signal: AbortSignal.timeout(20000) });
    if (!response.ok) throw new Error(`${slug}: public API returned ${response.status}`);
    const state = await response.json();
    if (state.status !== "published" || !state.document) throw new Error(`${slug}: not publicly readable`);
    const expected = packs.get(slug).locales["zh-TW"];
    for (const key of ["title", "description", "hero", "blocks", "sources"]) {
      if (stable(state.document[key]) !== stable(expected[key])) throw new Error(`${slug}: public ${key} differs from the reviewed pack`);
    }
  };
  await releaseSeries(catalogue, {
    importPack, verifyPublic,
    journal: async (event) => appendFileSync(path.resolve(options.journal), JSON.stringify({ ...event, at: new Date().toISOString() }) + "\n"),
  });
  console.log("All 50 children and the hub are published and match reviewed content. Browser and sitemap verification remain required.");
}

function stable(value) {
  return JSON.stringify(value, (_, item) => item && typeof item === "object" && !Array.isArray(item) ? Object.fromEntries(Object.keys(item).sort().map((key) => [key, item[key]])) : item);
}

if (process.argv[1] && pathToFileURL(path.resolve(process.argv[1])).href === import.meta.url) {
  main().catch((error) => { console.error(error.message); process.exitCode = 1; });
}
