import assert from "node:assert/strict";
import test from "node:test";
import { bodyLength, catalogue, checkPacks, importArguments, releaseSeries, seriesSlugs, validateCatalogue } from "./gemini-series.mjs";

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
