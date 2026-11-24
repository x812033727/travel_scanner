import test from "node:test";
import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { validateDirectory, validatePlan } from "./validate.mjs";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const readJson = async (name) => JSON.parse(await readFile(path.join(HERE, name), "utf8"));

async function loadSources() {
  const plan = await readJson("plan.json");
  const setting = await readJson("setting.json");
  const contract = await readJson("authoring-contract.json");
  const seasons = await Promise.all(
    Array.from({ length: 10 }, (_, i) => readJson(`season-${String(i + 1).padStart(2, "0")}.json`)),
  );
  return { plan, setting, contract, seasons };
}

test("current Glass Meridian 10-season 120-episode package passes all validations", async () => {
  const result = await validateDirectory(HERE);
  assert.equal(result.ok, true, result.errors.join("\n"));
  assert.equal(result.seasonCount, 10);
  assert.equal(result.episodeCount, 120);
});

test("rejects consecutive duplicate cliffhanger types", async () => {
  const data = await loadSources();
  data.seasons[0].episodes[1].cliffhanger.type = data.seasons[0].episodes[0].cliffhanger.type;
  const result = validatePlan(data);
  assert.equal(result.ok, false);
  assert.ok(result.errors.some((e) => e.includes("cliffhanger.type 連續重複")));
});

test("rejects resurrected permanently dead character", async () => {
  const data = await loadSources();
  data.seasons[8].episodes[1].characters.push("marcus-thorne");
  const result = validatePlan(data);
  assert.equal(result.ok, false);
  assert.ok(result.errors.some((e) => e.includes("永久死亡的角色 marcus-thorne")));
});

test("rejects premature mystery thread setup before introduced_in", async () => {
  const data = await loadSources();
  data.seasons[0].episodes[0].setups.push("m12");
  const result = validatePlan(data);
  assert.equal(result.ok, false);
  assert.ok(result.errors.some((e) => e.includes("引用 m12 超出")));
});

test("rejects falsified cliffhanger tension on closed finale E120", async () => {
  const data = await loadSources();
  data.seasons[9].episodes[11].tension = [3, 4, 4, 5, 5];
  const result = validatePlan(data);
  assert.equal(result.ok, false);
  assert.ok(result.errors.some((e) => e.includes("E120 末段張力")));
});
