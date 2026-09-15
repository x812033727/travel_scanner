import assert from "node:assert/strict";
import test from "node:test";
import { mkdtempSync, mkdirSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import path from "node:path";
import { bodyLength, catalogue, checkPacks, draftCatalogue, freezeRelease, importArguments, parseOptions, releaseSeries, seriesSlugs, validateCatalogue, verifyFrozenRelease } from "./gemini-series.mjs";
import { releaseWrites } from "../docs/gemini-series/advanced/platform/release-contract.mjs";

test("catalogue is one ordered, acyclic, complete series", () => {
  assert.deepEqual(validateCatalogue(catalogue), []);
  assert.equal(seriesSlugs(catalogue).at(-1), "gemini-guide");
});

test("all reviewed pages, assets and cross-links exist in the repository", () => {
  const checked = checkPacks();
  assert.deepEqual(checked.errors, []);
  assert.equal(checked.packs.size, 51);
});
test("invalid destinations and prerequisite cycles fail", () => {
  const broken = structuredClone(catalogue);
  broken.articles[0].prerequisites = [2];
  broken.articles[1].prerequisites = [1];
  broken.articles[0].related = [999, 999];
  assert.ok(validateCatalogue(broken).some((line) => line.includes("cycle")));
  assert.ok(validateCatalogue(broken).some((line) => line.includes("invalid reference")));
});
test("body length counts rich prose but excludes code and labels", () => {
  assert.equal(bodyLength([{ type: "rich_paragraph", inlines: [{ text: "甲 " }, { text: "乙" }] }, { type: "code", code: "ignored" }, { type: "heading", text: "ignored" }]), 2);
});
test("dry-run and publication stay in the supplied whitelist", () => {
  const args = importArguments(seriesSlugs(catalogue), { dryRun: true });
  assert.equal(args.filter((arg) => arg === "--slug").length, 51);
  assert.ok(args.includes("--dry-run"));
  assert.ok(!args.includes("--publish"));
  assert.throws(() => importArguments(["gemini-guide"]), /actor/);
});
test("hub is imported only after all children are verified twice", async () => {
  const calls = [];
  await releaseSeries(catalogue, {
    importPack: async (slugs, dryRun) => { calls.push({ type: "import", slugs, dryRun }); return {}; },
    verifyPublic: async (slug) => { calls.push({ type: "verify", slug }); },
    journal: async () => undefined,
  });
  assert.equal(calls[0].dryRun, true);
  const hub = calls.findIndex((call) => call.type === "import" && !call.dryRun && call.slugs[0] === catalogue.hubSlug);
  assert.equal(calls.slice(0, hub).filter((call) => call.type === "verify").length, 100);
  assert.equal(calls.at(-1).slug, catalogue.hubSlug);
});
test("partial import failure stops before the next child or hub", async () => {
  const imports = [];
  await assert.rejects(releaseSeries(catalogue, {
    importPack: async (slugs, dryRun) => { if (!dryRun) imports.push(slugs[0]); return { failed: dryRun ? null : "refused" }; },
    verifyPublic: async () => assert.fail("must stop before verification"),
    journal: async () => undefined,
  }), /refused/);
  assert.deepEqual(imports, [catalogue.articles[0].slug]);
});
test("failed public verification stops publication", async () => {
  const imports = [];
  await assert.rejects(releaseSeries(catalogue, {
    importPack: async (slugs, dryRun) => { if (!dryRun) imports.push(slugs[0]); return {}; },
    verifyPublic: async () => { throw new Error("stale content"); },
    journal: async () => undefined,
  }), /stale content/);
  assert.equal(imports.length, 1);
});

test("dry-run partial failure prevents every write", async () => {
  await assert.rejects(releaseSeries(catalogue, {
    importPack: async (_, dryRun) => { assert.equal(dryRun, true); return { failed: "invalid draft" }; },
    verifyPublic: async () => assert.fail("no publication"),
    journal: async () => assert.fail("no publication"),
  }), /dry-run stopped/);
});

test("advanced identities, paths and metadata cannot silently lose or replace a lesson", () => {
  const series = draftCatalogue();
  assert.deepEqual(validateCatalogue(series, "advanced"), []);
  assert.equal(series.articles.length, 86);
  const missing = structuredClone(series);
  missing.articles.pop();
  assert.ok(validateCatalogue(missing, "advanced").some((error) => error.includes("frozen")));
  const replaced = structuredClone(series);
  replaced.articles[68].slug = "unexpected-slug";
  assert.ok(validateCatalogue(replaced, "advanced").some((error) => error.includes("frozen")));
  const noStage = structuredClone(series);
  delete noStage.articles[50].stage;
  assert.ok(validateCatalogue(noStage, "advanced").some((error) => error.includes("stage")));
  assert.ok(validateCatalogue(series).length, "86 entries never pass the base contract");
  const missingRoute = structuredClone(series);
  missingRoute.paths.pop();
  assert.ok(validateCatalogue(missingRoute, "advanced").some((error) => error.includes("paths")));
});

test("CLI parsing refuses ambiguous or misspelled options before any import", () => {
  assert.deepEqual(parseOptions(["--draft", "--track", "md"]), { draft: true, track: "md" });
  for (const args of [["--publsh"], ["--manifest"], ["--track", "--draft"], ["--phase", "base", "--phase", "advanced"], ["stray"]]) {
    assert.throws(() => parseOptions(args));
  }
  assert.throws(() => importArguments([]), /whitelist/);
  assert.throws(() => importArguments(["gemini-guide", "gemini-guide"]), /whitelist/);
});

test("authoring checks reject a broken downloadable exercise before release freeze", (t) => {
  const workspace = mkdtempSync(path.join(tmpdir(), "gemini-download-test-"));
  t.after(() => rmSync(workspace, { recursive: true, force: true }));
  const slug = catalogue.articles[35].slug;
  const packPath = path.join(workspace, "apps/api/app/guides/content", slug + ".json");
  mkdirSync(path.dirname(packPath), { recursive: true });
  const assets = path.join(workspace, "apps/web/public/guides", slug);
  mkdirSync(assets, { recursive: true });
  for (const name of ["hero.jpg", "diagram-1.svg"]) {
    writeFileSync(path.join(assets, name), readFileSync(new URL("../apps/web/public/guides/" + slug + "/" + name, import.meta.url)));
  }
  const pack = JSON.parse(readFileSync(new URL("../apps/api/app/guides/content/" + slug + ".json", import.meta.url), "utf8"));
  pack.locales["zh-TW"].blocks.push({ type: "link", text: "下載練習包", url: "https://mokaair.com/guides/" + slug + "/exercise.zip" });
  writeFileSync(packPath, JSON.stringify(pack));
  assert.ok(checkPacks(catalogue, workspace, { slugs: [slug] }).errors.some((error) => error.includes("missing or invalid download")));
  writeFileSync(path.join(workspace, "apps/web/public/guides", slug, "exercise.zip"), "synthetic fixture");
  assert.deepEqual(checkPacks(catalogue, workspace, { slugs: [slug] }).errors, []);
});

function fixtureRelease(t) {
  const workspace = mkdtempSync(path.join(tmpdir(), "gemini-release-test-"));
  t.after(() => rmSync(workspace, { recursive: true, force: true }));
  const series = draftCatalogue();
  for (const slug of seriesSlugs(series)) {
    const content = path.join(workspace, "apps/api/app/guides/content");
    const assets = path.join(workspace, "apps/web/public/guides", slug);
    mkdirSync(content, { recursive: true });
    mkdirSync(assets, { recursive: true });
    writeFileSync(path.join(content, slug + ".json"), JSON.stringify({ slug, syntheticFixture: true }) + "\n");
    writeFileSync(path.join(assets, "hero.jpg"), Buffer.from([0, 1, 2]));
    writeFileSync(path.join(assets, "diagram-1.svg"), "<svg>fixture</svg>\n");
    writeFileSync(path.join(assets, "practice.zip"), Buffer.from([3, 4, 5]));
  }
  return { series, workspace };
}

test("a frozen advanced release writes exactly 36 children plus declared updates and hub", (t) => {
  const { series, workspace } = fixtureRelease(t);
  const manifest = freezeRelease(series, workspace, { phase: "advanced", updates: [series.articles[48].slug] });
  assert.equal(manifest.writes.length, 38);
  assert.deepEqual(manifest.writes.slice(0, 36), series.articles.slice(50).map((entry) => entry.slug));
  assert.deepEqual(manifest.writes.slice(-2), [series.articles[48].slug, series.hubSlug]);
  assert.equal(manifest.verifySlugs.length, 86);
  assert.equal(manifest.files.length, 87 * 4);
  assert.equal(verifyFrozenRelease(manifest, series, workspace).releaseId, manifest.releaseId);
  assert.throws(() => freezeRelease(series, workspace, { phase: "advanced", updates: [series.articles[0].slug] }), /declared/);
  assert.throws(() => freezeRelease(series, workspace, { phase: "advanced", updates: [series.articles[1].slug, series.articles[1].slug] }), /declared/);
});

test("freeze detects changed packs, added assets, downloads and catalogue metadata", (t) => {
  const { series, workspace } = fixtureRelease(t);
  const manifest = freezeRelease(series, workspace, { phase: "advanced" });
  const changed = structuredClone(series);
  changed.articles[50].title += " changed";
  assert.throws(() => verifyFrozenRelease(manifest, changed, workspace), /Catalogue changed/);
  const download = path.join(workspace, "apps/web/public/guides", series.articles[50].slug, "practice.zip");
  const original = readFileSync(download);
  writeFileSync(download, "changed");
  assert.throws(() => verifyFrozenRelease(manifest, series, workspace), /changed after freeze/);
  writeFileSync(download, original);
  const added = path.join(workspace, "apps/web/public/guides", series.articles[50].slug, "extra.txt");
  writeFileSync(added, "unexpected");
  assert.throws(() => verifyFrozenRelease(manifest, series, workspace), /changed after freeze/);
  rmSync(added);
  const content = path.join(workspace, "apps/api/app/guides/content", series.articles[50].slug + ".json");
  writeFileSync(content, '{"changed":true}');
  assert.throws(() => verifyFrozenRelease(manifest, series, workspace), /changed after freeze/);
});

test("frozen text hashes survive CRLF checkouts but edited manifests are rejected", (t) => {
  const { series, workspace } = fixtureRelease(t);
  const manifest = freezeRelease(series, workspace, { phase: "advanced" });
  const svg = path.join(workspace, "apps/web/public/guides", series.articles[0].slug, "diagram-1.svg");
  writeFileSync(svg, readFileSync(svg, "utf8").replace(/\n/g, "\r\n"));
  assert.equal(verifyFrozenRelease(manifest, series, workspace).releaseId, manifest.releaseId);
  const edited = structuredClone(manifest);
  edited.writes.unshift(series.articles[0].slug);
  assert.throws(() => verifyFrozenRelease(edited, series, workspace), /edited/);
});

test("advanced publication rechecks all 86 children before updating the hub", async () => {
  const series = draftCatalogue(), writes = releaseWrites(series, "advanced", [series.articles[48].slug]);
  const calls = [];
  await releaseSeries(series, {
    importPack: async (slugs, dryRun) => { calls.push({ type: "import", slugs, dryRun }); return {}; },
    verifyPublic: async (slug) => calls.push({ type: "verify", slug }),
    beforeWrite: async (slug) => calls.push({ type: "frozen", slug }),
    journal: async () => undefined,
  }, writes);
  assert.deepEqual(calls[0].slugs, writes);
  assert.deepEqual(calls.filter((call) => call.type === "import" && !call.dryRun).map((call) => call.slugs[0]), writes);
  const hubIndex = calls.findIndex((call) => call.type === "import" && !call.dryRun && call.slugs[0] === series.hubSlug);
  assert.equal(calls.slice(0, hubIndex).filter((call) => call.type === "verify").length, 37 + 86);
  assert.equal(calls.filter((call) => call.type === "frozen").length, writes.length);
});

test("a post-dry-run file change stops the first write and a missing old child prevents hub release", async () => {
  const series = draftCatalogue(), writes = releaseWrites(series, "advanced");
  const imported = [];
  await assert.rejects(releaseSeries(series, {
    importPack: async (slugs, dryRun) => { if (!dryRun) imported.push(slugs[0]); return {}; },
    beforeWrite: async () => { throw new Error("files changed"); },
    verifyPublic: async () => assert.fail("nothing written"), journal: async () => undefined,
  }, writes), /files changed/);
  assert.deepEqual(imported, []);
  await assert.rejects(releaseSeries(series, {
    importPack: async (slugs, dryRun) => { if (!dryRun) imported.push(slugs[0]); return {}; },
    verifyPublic: async (slug) => { if (slug === series.articles[0].slug) throw new Error("old article unavailable"); },
    journal: async () => undefined,
  }, writes), /old article unavailable/);
  assert.equal(imported.length, 36);
  assert.ok(!imported.includes(series.hubSlug));
});
