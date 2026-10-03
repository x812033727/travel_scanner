import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { mkdtempSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { basename, dirname, join, resolve } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

const INSTALLER = fileURLToPath(new URL("../ops/nginx/install.sh", import.meta.url));
const source = readFileSync(INSTALLER, "utf8").replaceAll("\r\n", "\n");
// Exercise the real detector without the installer's root check or /etc writes.
const detector = source.match(/^SITE_MARKERS=.*\n\nlooks_like_mokaair_site\(\) \{\n[\s\S]*?^\}/m)?.[0];
assert.ok(detector, "could not find the site's marker declaration and detector");

const probe = spawnSync("bash", ["-c", 'test -r "$1" && command -v grep >/dev/null', "probe", INSTALLER.replaceAll("\\", "/")], {
  encoding: "utf8",
  timeout: 10_000,
});
const bashUnavailable = probe.error
  ? `bash unavailable: ${probe.error.code}`
  : probe.status === 0 ? false : "bash cannot read the installer or run grep";

function detect(t, contents, expected, attempts = 1) {
  const fixtureDir = mkdtempSync(join(resolve(tmpdir()), "nginx-install-"));
  t.after(() => {
    assert.equal(dirname(fixtureDir), resolve(tmpdir()));
    assert.ok(basename(fixtureDir).startsWith("nginx-install-"));
    rmSync(fixtureDir, { recursive: true, force: true });
  });
  const fixture = join(fixtureDir, "operator-site.conf");
  if (contents !== null) writeFileSync(fixture, contents);
  const result = spawnSync("bash", ["-euo", "pipefail", "-c", `${detector}
for (( attempt=1; attempt<=$2; attempt++ )); do
  actual=1
  if looks_like_mokaair_site "$1"; then actual=0; fi
  if [[ "$actual" != "$3" ]]; then
    echo "site detection mismatch on attempt $attempt: expected $3, got $actual" >&2
    exit 1
  fi
done`, "detect", fixture.replaceAll("\\", "/"), String(attempts), expected ? "0" : "1"], {
    encoding: "utf8",
    timeout: 90_000,
  });
  assert.ifError(result.error);
  assert.equal(result.status, 0, `${result.stdout}${result.stderr}`);
}

// Un-commented lines exceed even a 64 KiB pipe, so an early match must still drain
// the producer. A tiny fixture misses the SIGPIPE race under `set -o pipefail`.
const padding = "set $fixture 0123456789abcdef;\n".repeat(65_536);
assert.ok(Buffer.byteLength(padding) > 1_048_576);

test("nginx detector never misses an early marker in a large site under pipefail", { skip: bashUnavailable }, (t) => {
  detect(t, `server_name mokaair.com;\n${padding}`, true, 300);
});

test("nginx detector finds a marker after a large site's other directives", { skip: bashUnavailable }, (t) => {
  detect(t, `${padding}proxy_pass http://mokaair_web;\n`, true);
});

test("nginx detector ignores markers that occur only in comments", { skip: bashUnavailable }, (t) => {
  detect(t, "  # server_name mokaair.com;\n# include mokaair-proxy-headers.conf;\nserver_name example.com;\n", false);
});

test("nginx detector does not mistake its rate-limit declarations for a site", { skip: bashUnavailable }, (t) => {
  detect(t, "limit_req_zone $binary_remote_addr zone=mokaair_page:10m rate=5r/s;\n", false);
});

test("nginx detector leaves an unrelated site alone", { skip: bashUnavailable }, (t) => {
  detect(t, "server_name example.com;\nproxy_pass http://unrelated_web;\n", false);
});

test("nginx detector treats an absent file as absent", { skip: bashUnavailable }, (t) => {
  detect(t, null, false);
});
