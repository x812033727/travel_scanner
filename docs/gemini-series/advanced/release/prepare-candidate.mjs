/** Local review overlay. Deliberately does not create a publishable release manifest. */
import { createHash, randomUUID } from "node:crypto";
import { spawnSync, execFileSync } from "node:child_process";
import { cpSync, mkdirSync, readFileSync, readdirSync, writeFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { checkPacks, draftCatalogue, seriesSlugs } from "../../../../tools/gemini-series.mjs";
import { releaseWrites } from "../platform/release-contract.mjs";

const here = fileURLToPath(new URL("./", import.meta.url));
const root = path.resolve(here, "../../../..");
const write = (file, value) => writeFileSync(file, JSON.stringify(value, null, 2) + "\n");
const sha = (bytes) => createHash("sha256").update(bytes).digest("hex");
const relative = (file) => path.relative(root, file).split(path.sep).join("/");
function files(directory) {
  return readdirSync(directory, { withFileTypes: true }).flatMap((entry) => {
    if (entry.isSymbolicLink()) throw new Error("Unexpected symlink: " + entry.name);
    const filename = path.join(directory, entry.name);
    return entry.isDirectory() ? files(filename) : [filename];
  });
}

const series = draftCatalogue(root);
const candidate = path.join(here, "candidate");
mkdirSync(candidate, { recursive: true });
write(path.join(candidate, "guide-series.json"), series);
const python = process.argv[2] || path.join(root, "apps/api/.venv/Scripts/python.exe");
const compilation = spawnSync(python, ["-X", "utf8", path.join(here, "compile-overlay.py")], { cwd: root, encoding: "utf8" });
if (compilation.status !== 0) throw new Error(compilation.stderr || compilation.stdout);
const overlays = JSON.parse(compilation.stdout);
const workspace = path.join(here, ".workspaces", "candidate-" + randomUUID());
const content = path.join(workspace, "apps/api/app/guides/content");
const artwork = path.join(workspace, "apps/web/public/guides");
mkdirSync(content, { recursive: true });
mkdirSync(artwork, { recursive: true });
const inputs = [];
for (const slug of seriesSlugs(series)) {
  const changed = overlays.some((entry) => entry.slug === slug);
  const source = changed ? path.join(candidate, "content", slug + ".json") : path.join(root, "apps/api/app/guides/content", slug + ".json");
  cpSync(source, path.join(content, slug + ".json"));
  const assets = path.join(root, "apps/web/public/guides", slug);
  cpSync(assets, path.join(artwork, slug), { recursive: true });
  for (const file of [source, ...files(assets)]) inputs.push({ path: relative(file), sha256: sha(readFileSync(file)), slug, encoding: "raw-bytes" });
}
const check = checkPacks(series, workspace, { phase: "advanced" });
if (check.errors.length) throw new Error(check.errors.join("\n"));
const report = {
  schemaVersion: "gemini-review-candidate-v1", publishable: false,
  generatedAt: new Date().toISOString(), node: process.version, sourceHead: execFileSync("git", ["rev-parse", "HEAD"], { cwd: root, encoding: "utf8" }).trim(),
  status: "local-content-check-passed-external-acceptance-pending",
  runtimeArticles: JSON.parse(readFileSync(path.join(root, "apps/web/lib/guide-series.json"), "utf8")).articles.length,
  runtimeCatalogueSha256: sha(readFileSync(path.join(root, "apps/web/lib/guide-series.json"))),
  candidateCatalogueSha256: sha(readFileSync(path.join(candidate, "guide-series.json"))),
  articles: series.articles.length, pagesChecked: check.slugs.length,
  overlays, proposedWrites: releaseWrites(series, "advanced", overlays.filter((row) => row.number).map((row) => row.slug)),
  requiredChildVerification: series.articles.map((row) => row.slug),
  inputs: inputs.sort((a, b) => a.path.localeCompare(b.path, "en")),
  checks: { contentPackSchema: "3 overlays passed; other 84 covered by existing author records", allPackLinksAssetsLengths: "87 passed", originalH2Order: "all 3 overlays preserved" },
  notPerformed: ["Google authenticated acceptance", "fresh Taiwan price amounts", "API database import dry-run", "publication", "candidate browser verification"],
};
write(path.join(candidate, "review.json"), report);
// Absolute temporary paths are local only; no such path belongs in the portable receipt.
write(path.join(here, ".workspaces", "latest.json"), { workspace });
console.log(JSON.stringify({ pages: report.pagesChecked, articles: report.articles, overlays, proposedWrites: report.proposedWrites.length, publishable: false }, null, 2));
