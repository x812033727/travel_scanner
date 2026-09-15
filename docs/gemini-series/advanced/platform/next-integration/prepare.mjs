/** Prepare a complete Next checkout with 86 catalogue entries, without touching the live catalogue. */
import { execFileSync } from "node:child_process";
import { mkdir, writeFile, readFile, symlink } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { createHash } from "node:crypto";
import { draftCatalogue } from "../release-contract.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, "../../../../..");
const target = path.join(here, ".workspaces", `next-${Date.now()}`);
const files = execFileSync("git", ["ls-files", "--cached", "--others", "--exclude-standard", "-z", "apps/web"], { cwd: root, encoding: "utf8" }).split("\0").filter(Boolean);
const sha = data => createHash("sha256").update(data).digest("hex");
const catalogueFile = path.join(root, "apps/web/lib/guide-series.json");
const originalSha = sha(await readFile(catalogueFile));
const copied = [];
await mkdir(target, { recursive: true });
for (const file of [...new Set(files), "package.json", "package-lock.json", "docs/gemini-series/advanced/curriculum.json", "docs/gemini-series/advanced/platform/catalogue-contract.json"]) {
  if (file.startsWith("apps/web/public/") || /(?:^|\/)(?:node_modules|\.next|test-results|playwright-report|\.env[^/]*)(?:\/|$)/.test(file)) continue;
  const output = path.join(target, file);
  await mkdir(path.dirname(output), { recursive: true });
  const bytes = await readFile(path.join(root, file));
  await writeFile(output, bytes);
  copied.push({ path: file, sha256: sha(bytes) });
}
await symlink(path.join(root, "node_modules"), path.join(target, "node_modules"), "junction");
await symlink(path.join(root, "apps/web/public"), path.join(target, "apps/web/public"), "junction");
const catalogue = draftCatalogue(root);
const fixtureCatalogueBytes = JSON.stringify(catalogue, null, 2) + "\n";
await writeFile(path.join(target, "apps/web/lib/guide-series.json"), fixtureCatalogueBytes);
const contentPacks = [];
for (const slug of [catalogue.hubSlug, ...catalogue.articles.map(article => article.slug)]) {
  const file = `apps/api/app/guides/content/${slug}.json`;
  const output = path.join(target, file);
  await mkdir(path.dirname(output), { recursive: true });
  const bytes = await readFile(path.join(root, file));
  await writeFile(output, bytes);
  contentPacks.push({ path: file, sha256: sha(bytes) });
}
if (sha(await readFile(catalogueFile)) !== originalSha) throw new Error("Live catalogue changed while preparing fixture");
const result = { preparedAt: new Date().toISOString(), workspace: target, web: path.join(target, "apps/web"),
  originalCatalogueSha256: originalSha, fixtureCatalogueSha256: sha(fixtureCatalogueBytes), fixtureArticles: catalogue.articles.length, sourceFiles: copied, contentPacks };
await writeFile(path.join(here, "prepared.json"), JSON.stringify(result, null, 2) + "\n");
console.log(JSON.stringify({ web: result.web, originalCatalogueSha256: originalSha, fixtureArticles: result.fixtureArticles }));
