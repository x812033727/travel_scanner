import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import test from "node:test";

test("preschool resume, package and mux reject changed artifact bytes or source", (t) => {
  const python = process.env.PRESCHOOL_TEST_PYTHON || (process.platform === "win32" ? "python" : "python3");
  // -S deliberately excludes third-party site packages. These contract tests
  // must run in tools-only CI without Pillow, edge-tts, ffmpeg, or a network.
  const result = spawnSync(python, ["-S", "-m", "unittest", "test_integrity"], {
    cwd: fileURLToPath(new URL(".", import.meta.url)), encoding: "utf8", windowsHide: true,
    env: { ...process.env, PYTHONIOENCODING: "utf-8", PYTHONDONTWRITEBYTECODE: "1" },
  });
  assert.equal(result.error, undefined, `Python is required: ${result.error}`);
  assert.equal(result.status, 0, `${result.stdout}\n${result.stderr}`);
  assert.match(result.stderr, /Ran \d+ tests/);
  t.diagnostic(result.stderr.split(/\r?\n/).filter((line) => /^Ran \d+ tests|^OK/.test(line)).join("; "));
});
