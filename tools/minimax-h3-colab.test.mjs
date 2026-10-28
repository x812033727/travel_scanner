/**
 * The minimax-h3-colab skill's own scripts (.agents/skills/minimax-h3-colab/scripts/): the
 * headless pairing helper, the bootstrap's token and verify steps, and the runner wrapper.
 *
 * Everything runs against a fake `colab` on PATH and a temporary HOME, so no Google account,
 * no network and no compute units are involved. What is pinned: the pairing helper prints the
 * sign-in URL the CLI emits and feeds the code back to the same waiting process; `export`
 * prints the saved token as one base64 line that `bootstrap.sh token` accepts (raw JSON too)
 * and writes with mode 600; `verify` judges the pairing by the balance line, not the exit code
 * (the real CLI exits 0 after printing a sign-in URL to a closed stdin); the wrapper refuses
 * without the upstream runner and otherwise forwards arguments unchanged.
 */
import assert from "node:assert/strict";
import { spawn, spawnSync } from "node:child_process";
import { chmodSync, existsSync, mkdirSync, mkdtempSync, readFileSync, rmSync, statSync, writeFileSync } from "node:fs";
import { createServer } from "node:http";
import { tmpdir } from "node:os";
import path from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

const ROOT = fileURLToPath(new URL("../", import.meta.url));
const SCRIPTS = path.join(ROOT, ".agents", "skills", "minimax-h3-colab", "scripts");
const PAIR = path.join(SCRIPTS, "pair.py");
const BOOTSTRAP = path.join(SCRIPTS, "bootstrap.sh");
const H3 = path.join(SCRIPTS, "h3.sh");
const POSIX = process.platform !== "win32";
const PYTHON = process.env.MINIMAX_H3_TEST_PYTHON || "python3";

const TOKEN = { token: "t", refresh_token: "r", client_id: "c", client_secret: "s", scopes: ["x"] };

// A colab CLI that behaves like 0.7.5 for the three things the scripts look at: `version`,
// a paired `usage` (balance lines), and an unpaired `usage` (sign-in URL, then a code on stdin).
const FAKE_COLAB = `#!/usr/bin/env bash
cfg="\${COLAB_CLI_CONFIG_DIR:-$HOME/.config/colab-cli}"
case "$*" in
  *version*) echo "Version: 0.7.5" ;;
  *usage*)
    if [ -s "$cfg/token.json" ]; then
      printf 'Current balance: 123.4 compute units\\nUsage rate: 0 / hr\\nActive assignments: 0\\n'
    else
      echo; echo "To authorize colab-cli, visit this URL in any browser:"; echo
      echo "  https://accounts.google.com/o/oauth2/auth?client_id=fake&state=abc"; echo
      echo "After approving, Google will display an authorization code."
      printf 'Enter the authorization code: '
      if ! read -r code; then echo "[colab] Warning: failed to fetch compute-unit info: EOF when reading a line"; exit 0; fi
      if [ "$code" = "4/good" ]; then
        mkdir -p "$cfg"; printf '%s' '${JSON.stringify(TOKEN)}' > "$cfg/token.json"
        printf 'Current balance: 123.4 compute units\\nUsage rate: 0 / hr\\nActive assignments: 0\\n'
      else
        echo "invalid_grant: Bad Request"; exit 1
      fi
    fi ;;
  *) echo "fake colab: unexpected $*" >&2; exit 9 ;;
esac
`;

function sandbox() {
  const home = mkdtempSync(path.join(tmpdir(), "h3-colab-"));
  const bin = path.join(home, "bin");
  mkdirSync(bin);
  writeFileSync(path.join(bin, "colab"), FAKE_COLAB);
  chmodSync(path.join(bin, "colab"), 0o755);
  const env = { ...process.env, HOME: home, PATH: `${bin}${path.delimiter}${process.env.PATH}`, COLAB_CLI_TOKEN_JSON: "" };
  delete env.COLAB_CLI_TOKEN_JSON;
  delete env.COLAB_CLI_CONFIG_DIR;
  delete env.COLAB_PAIR_STATE;
  delete env.MINIMAX_H3_COLAB_HOME;
  return { home, env, token: path.join(home, ".config", "colab-cli", "token.json") };
}

function run(cmd, args, env, options = {}) {
  const result = spawnSync(cmd, args, { env, encoding: "utf8", timeout: 60_000, ...options });
  return { code: result.status, out: result.stdout ?? "", err: result.stderr ?? "" };
}

/** Like run, but without blocking the event loop: a test that also serves HTTP needs it. */
function runAsync(cmd, args, env) {
  return new Promise((resolve) => {
    const child = spawn(cmd, args, { env });
    let out = "";
    let err = "";
    child.stdout.on("data", (chunk) => { out += chunk; });
    child.stderr.on("data", (chunk) => { err += chunk; });
    child.on("close", (code) => resolve({ code, out, err }));
  });
}

test("pair.py: start prints the sign-in URL, code feeds the same waiting CLI, export gives base64 of the token", { skip: !POSIX }, () => {
  const { home, env, token } = sandbox();
  try {
    const started = run(PYTHON, [PAIR, "start"], env);
    assert.equal(started.code, 0, started.err);
    assert.match(started.out, /https:\/\/accounts\.google\.com\/o\/oauth2\/auth\?client_id=fake/);
    assert.ok(!existsSync(token), "no token before the code");

    const status = run(PYTHON, [PAIR, "status"], env);
    assert.match(status.out, /^waiting_for_code/);

    const paired = run(PYTHON, [PAIR, "code", "4/good"], env);
    assert.equal(paired.code, 0, paired.out + paired.err);
    assert.match(paired.out, /Paired\./);
    assert.match(paired.out, /Current balance: 123\.4/);
    assert.deepEqual(JSON.parse(readFileSync(token, "utf8")), TOKEN);
    // The code is handed over and forgotten; the state keeps only the URL, result and log.
    assert.ok(!existsSync(path.join(home, ".config", "colab-cli", "pair", "code.txt")));

    const exported = run(PYTHON, [PAIR, "export"], env);
    assert.equal(exported.code, 0, exported.err);
    const line = exported.out.trim();
    assert.ok(!line.includes("\n"), "one line");
    assert.deepEqual(JSON.parse(Buffer.from(line, "base64").toString("utf8")), TOKEN);
    assert.match(exported.err, /COLAB_CLI_TOKEN_JSON/);

    const cleared = run(PYTHON, [PAIR, "clear"], env);
    assert.equal(cleared.code, 0);
    assert.ok(existsSync(token), "clear leaves the token alone");
    assert.match(run(PYTHON, [PAIR, "status"], env).out, /^paired_token_present/);
  } finally {
    rmSync(home, { recursive: true, force: true });
  }
});

test("pair.py: a wrong code is reported, and code without a waiting pairing is refused", { skip: !POSIX }, () => {
  const { home, env, token } = sandbox();
  try {
    assert.equal(run(PYTHON, [PAIR, "code", "4/x"], env).code, 2, "nothing waiting");
    assert.equal(run(PYTHON, [PAIR, "start"], env).code, 0);
    const failed = run(PYTHON, [PAIR, "code", "4/wrong"], env);
    assert.equal(failed.code, 1);
    assert.match(failed.out, /invalid_grant/);
    assert.ok(!existsSync(token));
    assert.equal(run(PYTHON, [PAIR, "export"], env).code, 1, "nothing to export");
  } finally {
    rmSync(home, { recursive: true, force: true });
  }
});

test("bootstrap.sh token: base64 or raw JSON from the secret lands as a 600 token file; junk is refused with 3", { skip: !POSIX }, () => {
  const { home, env, token } = sandbox();
  try {
    const b64 = Buffer.from(JSON.stringify(TOKEN)).toString("base64");
    const fromB64 = run("bash", [BOOTSTRAP, "token"], { ...env, COLAB_CLI_TOKEN_JSON: `${b64}\n` });
    assert.equal(fromB64.code, 0, fromB64.err);
    assert.deepEqual(JSON.parse(readFileSync(token, "utf8")), TOKEN);
    assert.equal(statSync(token).mode & 0o777, 0o600);
    assert.equal(statSync(path.dirname(token)).mode & 0o777, 0o700);

    const fromJson = run("bash", [BOOTSTRAP, "token"], { ...env, COLAB_CLI_TOKEN_JSON: JSON.stringify({ ...TOKEN, token: "t2" }) });
    assert.equal(fromJson.code, 0, fromJson.err);
    assert.equal(JSON.parse(readFileSync(token, "utf8")).token, "t2");

    const junk = run("bash", [BOOTSTRAP, "token"], { ...env, COLAB_CLI_TOKEN_JSON: "not json at all" });
    assert.equal(junk.code, 3);
    assert.equal(JSON.parse(readFileSync(token, "utf8")).token, "t2", "a bad secret never overwrites a good token");

    const noRefresh = run("bash", [BOOTSTRAP, "token"], { ...env, COLAB_CLI_TOKEN_JSON: JSON.stringify({ token: "only" }) });
    assert.equal(noRefresh.code, 3);

    const unset = run("bash", [BOOTSTRAP, "token"], env);
    assert.equal(unset.code, 0);
    assert.match(unset.out, /keeping the token already/);
  } finally {
    rmSync(home, { recursive: true, force: true });
  }
});

test("bootstrap.sh token: with a paired video tool token it fetches the account's token.json from the site", { skip: !POSIX }, async () => {
  const { home, env, token } = sandbox();
  const requests = [];
  const server = createServer((request, response) => {
    requests.push({ url: request.url, authorization: request.headers.authorization });
    if (request.headers.authorization !== "Bearer mkv_paired") {
      response.writeHead(401, { "Content-Type": "application/json" });
      response.end(JSON.stringify({ code: "video_tool_token_invalid", detail: "bad token" }));
      return;
    }
    if (request.url === "/api/video/colab-credentials?slot=c") {
      response.writeHead(404, { "Content-Type": "application/json" });
      response.end(JSON.stringify({ code: "colab_not_signed_in", detail: "colab-c has no saved sign-in" }));
      return;
    }
    response.writeHead(200, { "Content-Type": "application/json" });
    response.end(JSON.stringify({ tool: "colab", slot: "b", credentials: TOKEN }));
  });
  await new Promise((resolve) => server.listen(0, "127.0.0.1", resolve));
  const site = `http://127.0.0.1:${server.address().port}`;
  try {
    const fetched = await runAsync("bash", [BOOTSTRAP, "token"], { ...env, MOKAAIR_SITE: site, MOKAAIR_VIDEO_TOKEN: "mkv_paired" });
    assert.equal(fetched.code, 0, fetched.out + fetched.err);
    assert.match(fetched.out, /from the site/);
    assert.match(fetched.err, /account slot b/);
    assert.deepEqual(JSON.parse(readFileSync(token, "utf8")), TOKEN);
    assert.equal(statSync(token).mode & 0o777, 0o600);
    assert.deepEqual(requests.map((item) => item.url), ["/api/video/colab-credentials?slot=default"]);

    const missing = await runAsync("bash", [BOOTSTRAP, "token"], { ...env, MOKAAIR_SITE: site, MOKAAIR_VIDEO_TOKEN: "mkv_paired", COLAB_ACCOUNT_SLOT: "c" });
    assert.equal(missing.code, 0, "a refusal keeps the token already there");
    assert.match(missing.err, /HTTP 404/);
    assert.match(missing.err, /colab_not_signed_in/);
    assert.deepEqual(JSON.parse(readFileSync(token, "utf8")), TOKEN);

    // The file `login` writes is read when the environment names no token.
    mkdirSync(path.join(home, ".mokaair"), { recursive: true });
    writeFileSync(path.join(home, ".mokaair", "video-tool.json"), JSON.stringify({ site: "https://mokaair.com", token: "mkv_paired" }));
    rmSync(token);
    const fromFile = await runAsync("bash", [BOOTSTRAP, "token"], { ...env, MOKAAIR_SITE: site });
    assert.equal(fromFile.code, 0, fromFile.out + fromFile.err);
    assert.deepEqual(JSON.parse(readFileSync(token, "utf8")), TOKEN);
    // A secret in the environment wins over the site.
    const secret = await runAsync("bash", [BOOTSTRAP, "token"], { ...env, MOKAAIR_SITE: site, MOKAAIR_VIDEO_TOKEN: "mkv_paired", COLAB_CLI_TOKEN_JSON: JSON.stringify({ ...TOKEN, token: "from-secret" }) });
    assert.equal(secret.code, 0);
    assert.equal(JSON.parse(readFileSync(token, "utf8")).token, "from-secret");
    assert.equal(requests.length, 3);
  } finally {
    server.close();
    rmSync(home, { recursive: true, force: true });
  }
});

test("bootstrap.sh verify: a balance means paired; a sign-in URL means exit 4 even though the CLI exits 0", { skip: !POSIX }, () => {
  const { home, env, token } = sandbox();
  try {
    const unpaired = run("bash", [BOOTSTRAP, "verify"], env);
    assert.equal(unpaired.code, 4);
    assert.match(unpaired.err, /not paired/);
    mkdirSync(path.dirname(token), { recursive: true });
    writeFileSync(token, JSON.stringify(TOKEN));
    const paired = run("bash", [BOOTSTRAP, "verify"], env);
    assert.equal(paired.code, 0, paired.err);
    assert.match(paired.out, /Current balance: 123\.4/);
    assert.match(paired.out, /paired/);
  } finally {
    rmSync(home, { recursive: true, force: true });
  }
});

test("h3.sh: refuses without the upstream runner, otherwise forwards arguments and adds --json to usage", { skip: !POSIX }, () => {
  const { home, env } = sandbox();
  try {
    const missing = run("bash", [H3, "usage"], env);
    assert.equal(missing.code, 2);
    assert.match(missing.err, /bootstrap\.sh install/);

    const upstream = path.join(home, "upstream");
    mkdirSync(path.join(upstream, "scripts"), { recursive: true });
    writeFileSync(path.join(upstream, "scripts", "runner.py"), 'import json, os, sys\nprint(json.dumps({"argv": sys.argv[1:], "gpu": os.environ.get("COLAB_GPU"), "auth": os.environ.get("COLAB_AUTH")}))\n');
    const withHome = { ...env, MINIMAX_H3_COLAB_HOME: upstream };
    const usage = JSON.parse(run("bash", [H3, "usage"], withHome).out);
    assert.deepEqual(usage, { argv: ["usage", "--json"], gpu: "A100", auth: "oauth2" });
    const single = JSON.parse(run("bash", [H3, "single", "--image", "a.png", "--prompt", "p.txt", "--mode", "first_frame"], { ...withHome, COLAB_GPU: "L4" }).out);
    assert.deepEqual(single.argv, ["single", "--image", "a.png", "--prompt", "p.txt", "--mode", "first_frame"]);
    assert.equal(single.gpu, "L4");
  } finally {
    rmSync(home, { recursive: true, force: true });
  }
});
