import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import test from "node:test";

test("elementary renderer provenance and batch failure receipts stay trustworthy", (t) => {
  const python = process.env.PRESCHOOL_TEST_PYTHON || (process.platform === "win32" ? "python" : "python3");
  const result = spawnSync(python, ["-S", "-m", "unittest", "test_profile"], {
    cwd: fileURLToPath(new URL(".", import.meta.url)), encoding: "utf8", windowsHide: true,
    env: { ...process.env, PYTHONIOENCODING: "utf-8", PYTHONDONTWRITEBYTECODE: "1" },
  });
  assert.equal(result.error, undefined, `Python is required: ${result.error}`);
  assert.equal(result.status, 0, `${result.stdout}\n${result.stderr}`);
  assert.match(result.stderr, /Ran \d+ tests/);
  t.diagnostic(result.stderr.split(/\r?\n/).filter((line) => /^Ran \d+ tests|^OK/.test(line)).join("; "));
});
