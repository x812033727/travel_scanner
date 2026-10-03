import assert from "node:assert/strict";
import test from "node:test";
import { existsSync, readFileSync } from "node:fs";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import { delimiter } from "node:path";

const directory = fileURLToPath(new URL("./dots-series/", import.meta.url));
const catalogue = JSON.parse(readFileSync(new URL("../apps/api/app/guides/series_data/dots.json", import.meta.url), "utf8"));

test("dots registry is a zh-TW API series with sixteen ordered lessons and coherent prerequisites", () => {
  const registry = JSON.parse(readFileSync(new URL("../apps/api/app/guides/series_registry.json", import.meta.url), "utf8"));
  assert.deepEqual(registry.find(row => row.slug === "dots"), { slug: "dots", section: "life", hub_slug: "dots-guide", hub_kind: "life", source: "api-series", topic: "ai-chat" });
  assert.equal(catalogue.locale, "zh-TW");
  assert.equal(catalogue.hub, "dots-guide");
  assert.deepEqual(catalogue.entries.map(row => row.number), Array.from({ length: 16 }, (_, i) => i + 1));
  assert.equal(new Set(catalogue.entries.map(row => row.slug)).size, 16);
  for (const entry of catalogue.entries) {
    assert.equal(entry.group, entry.number <= 10 ? "basics" : "applications");
    for (const prerequisite of entry.prerequisites) {
      const target = catalogue.entries.find(row => row.slug === prerequisite);
      assert.ok(target && target.number < entry.number, `${entry.slug}: prerequisite must be an earlier lesson`);
    }
  }
  assert.equal(existsSync(new URL("../apps/api/app/guides/series_data/locales/dots.json", import.meta.url)), false, "no unreviewed translations should create other-locale catalogues");
});

test("authoring and publication gate reject missing proof, stale hashes and unreadable media", t => {
  const local = fileURLToPath(new URL(process.platform === "win32" ? "../apps/api/.venv/Scripts/python.exe" : "../apps/api/.venv/bin/python", import.meta.url));
  const python = process.env.DOTS_TEST_PYTHON || (existsSync(local) ? local : process.platform === "win32" ? "python" : "python3");
  const result = spawnSync(python, ["-m", "unittest", "test_authoring", "test_readiness", "test_authoring_kit", "test_paths"], { cwd: directory, encoding: "utf8", env: { ...process.env, PYTHONIOENCODING: "utf-8", PYTHONDONTWRITEBYTECODE: "1" }, windowsHide: true });
  assert.equal(result.error, undefined, `Python is required for these dependency-free contract tests: ${result.error}`);
  assert.equal(result.status, 0, `${result.stdout}\n${result.stderr}`);
  assert.match(result.stderr, /Ran \d+ tests/);
  t.diagnostic(result.stderr.split(/\r?\n/).filter(line => /^Ran \d+ tests|^OK/.test(line)).join("; "));
});

test("API compiler and publication join run with the provisioned API runtime", t => {
  const local = fileURLToPath(new URL(process.platform === "win32" ? "../apps/api/.venv/Scripts/python.exe" : "../apps/api/.venv/bin/python", import.meta.url));
  const python = process.env.DOTS_API_TEST_PYTHON || (existsSync(local) ? local : null);
  if (!python) {
    t.skip("API environment is not provisioned in this tools-only job; CI api-checks runs test_pipeline.py after uv sync --frozen");
    return;
  }
  const api = fileURLToPath(new URL("../apps/api/", import.meta.url));
  const result = spawnSync(python, ["-m", "unittest", "test_pipeline"], { cwd: directory, encoding: "utf8", env: { ...process.env, PYTHONPATH: [api, process.env.PYTHONPATH].filter(Boolean).join(delimiter), PYTHONIOENCODING: "utf-8", PYTHONDONTWRITEBYTECODE: "1" }, windowsHide: true });
  assert.equal(result.error, undefined, `Configured API Python must be executable: ${result.error}`);
  assert.equal(result.status, 0, `${result.stdout}\n${result.stderr}`);
  assert.match(result.stderr, /Ran \d+ tests/);
  t.diagnostic(result.stderr.split(/\r?\n/).filter(line => /^Ran \d+ tests|^OK/.test(line)).join("; "));
});
