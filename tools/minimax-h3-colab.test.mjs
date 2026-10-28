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
 * without the upstream runner and otherwise forwards arguments unchanged; the sampling-profile
 * patcher rewrites exactly the eight upstream lines and refuses anything else; the manifest
 * check names every error that would otherwise cost compute units.
 */
import assert from "node:assert/strict";
import { spawn, spawnSync } from "node:child_process";
import { createHash } from "node:crypto";
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
    // first_frame without a size gets the 16:9-safe canvas appended (see the wrapper test below).
    const single = JSON.parse(run("bash", [H3, "single", "--image", "a.png", "--prompt", "p.txt", "--mode", "first_frame"], { ...withHome, COLAB_GPU: "L4" }).out);
    assert.deepEqual(single.argv, ["single", "--image", "a.png", "--prompt", "p.txt", "--mode", "first_frame", "--width", "1312", "--height", "736"]);
    assert.equal(single.gpu, "L4");
  } finally {
    rmSync(home, { recursive: true, force: true });
  }
});

// ---- sampling profile patch and the offline manifest check (added 2026-10-28) ----

const PATCH = path.join(SCRIPTS, "patch_notebook.py");
const CHECK = path.join(SCRIPTS, "check_manifest.py");

// The eight lines of the pinned upstream notebook (killkli @ 0a0d3b9c) that the patcher rewrites,
// in the two code cells they live in. A fixture, so the test needs no clone and no network.
function fixtureNotebook() {
  return {
    cells: [
      { cell_type: "markdown", metadata: {}, source: ["# fixture"] },
      { cell_type: "code", metadata: {}, outputs: [], execution_count: null, source: [
        'INFERENCE_MODE = os.environ.get("H3_INFERENCE_MODE", "first_frame").strip().lower()\n',
        'STEPS = 4 if INFERENCE_MODE == "reference" else 8\n',
        "LORA_STRENGTH = 1.0\n", 'SAMPLER_NAME = "euler"\n', 'SCHEDULER_NAME = "beta"\n', "DENOISE = 1.0\n",
      ] },
      { cell_type: "code", metadata: {}, outputs: [], execution_count: null, source: [
        'BASE_REPO = "Comfy-Org/MiniMax-H3"\n', 'if INFERENCE_MODE == "reference":\n',
        "    LORA_REPO = BASE_REPO\n", '    LORA_REMOTE = "loras/minimax_h3_ref2v_turbo_4step_v0.1_comfyui_bf16.safetensors"\n',
        "else:\n", '    LORA_REPO = "drbaph/MiniMax-H3-Turbo-Lora-ComfyUI"\n',
        '    LORA_REMOTE = "minimax_h3_turbo_v4_step600_ema_pruned_comfyui.safetensors"\n', "LORA = Path(LORA_REMOTE).name\n",
      ] },
    ],
    metadata: {}, nbformat: 4, nbformat_minor: 5,
  };
}
const codeOf = (file) => JSON.parse(readFileSync(file, "utf8")).cells.filter((c) => c.cell_type === "code").map((c) => c.source.join("")).join("\n");

test("patch_notebook.py: smooth swaps both LoRAs to the 8-step files once, is idempotent, and stops with 2 when upstream's lines are gone", { skip: !POSIX }, () => {
  const { home, env } = sandbox();
  const nb = path.join(home, "nb.ipynb");
  writeFileSync(nb, JSON.stringify(fixtureNotebook(), null, 1));
  const first = run(PYTHON, ["-I", PATCH, "--notebook", nb], env);
  assert.equal(first.code, 0, first.err);
  assert.match(first.out, /patched steps, ref_repo, ref_file, ff_repo, ff_file, strength, scheduler: profile=smooth/);
  const code = codeOf(nb);
  assert.match(code, /STEPS = 8 if INFERENCE_MODE == "reference" else 8/);
  assert.match(code, /LORA_REPO = "lightx2v\/Minimax-h3-Turbo"\n\s+LORA_REMOTE = "minimax_h3_ref2v_turbo_8step_v1\.0_768p_comfyui_bf16\.safetensors"/);
  assert.match(code, /LORA_REPO = "Comfy-Org\/MiniMax-H3"\n\s+LORA_REMOTE = "loras\/minimax_h3_fl2v_turbo_8step_v1\.0_comfyui_bf16\.safetensors"/);
  assert.match(code, /SCHEDULER_NAME = "simple"/);
  assert.match(code, /SAMPLER_NAME = "euler"/);
  assert.doesNotMatch(code, /4step_v0\.1|drbaph/);
  const again = run(PYTHON, ["-I", PATCH, "--notebook", nb], env);
  assert.equal(again.code, 0, again.err);
  assert.match(again.out, /already applied: profile=smooth/);
  assert.equal(codeOf(nb), code, "a second run changes nothing");
  // A different profile on an already patched notebook is upstream drift from the patcher's view.
  const drift = run(PYTHON, ["-I", PATCH, "--notebook", nb, "--profile", "hero"], env);
  assert.equal(drift.code, 2);
  assert.match(drift.err, /expected exactly one `STEPS = 4 if INFERENCE_MODE == "reference" else 8`.*found 0/);
  assert.equal(codeOf(nb), code, "a refused run writes nothing");
});

test("patch_notebook.py: hero is 20 steps with the LoRA at strength 0, draft leaves upstream's text, --dry-run writes nothing, env overrides win", { skip: !POSIX }, () => {
  const { home, env } = sandbox();
  const nb = path.join(home, "nb.ipynb");
  const pristine = JSON.stringify(fixtureNotebook(), null, 1);
  writeFileSync(nb, pristine);
  const hero = run(PYTHON, ["-I", PATCH, "--notebook", nb], { ...env, H3_PROFILE: "hero" });
  assert.equal(hero.code, 0, hero.err);
  const code = codeOf(nb);
  assert.match(code, /STEPS = 20 if INFERENCE_MODE == "reference" else 20/);
  assert.match(code, /LORA_STRENGTH = 0\n/);
  assert.match(code, /SAMPLER_NAME = "res_multistep"/);

  writeFileSync(nb, pristine);
  const draft = run(PYTHON, ["-I", PATCH, "--notebook", nb, "--profile", "draft"], env);
  assert.equal(draft.code, 0, draft.err);
  const draftCode = codeOf(nb);
  assert.match(draftCode, /STEPS = 4 if INFERENCE_MODE == "reference" else 8/);
  assert.match(draftCode, /ref2v_turbo_4step_v0\.1/);
  assert.match(draftCode, /drbaph\/MiniMax-H3-Turbo-Lora-ComfyUI/);
  assert.match(draftCode, /SCHEDULER_NAME = "beta"/);

  writeFileSync(nb, pristine);
  const dry = run(PYTHON, ["-I", PATCH, "--notebook", nb, "--dry-run"], env);
  assert.equal(dry.code, 0, dry.err);
  assert.match(dry.out, /^\+\s+"STEPS = 8 if INFERENCE_MODE/m);
  assert.equal(readFileSync(nb, "utf8"), pristine, "--dry-run leaves the notebook alone");

  const custom = run(PYTHON, ["-I", PATCH, "--notebook", nb], { ...env, H3_REF_STEPS: "6", H3_SCHEDULER: "beta" });
  assert.equal(custom.code, 0, custom.err);
  assert.match(codeOf(nb), /STEPS = 6 if INFERENCE_MODE == "reference" else 8/);
  assert.match(codeOf(nb), /SCHEDULER_NAME = "beta"/);

  const bad = run(PYTHON, ["-I", PATCH, "--notebook", nb], { ...env, H3_REF_STEPS: "many" });
  assert.equal(bad.code, 2);
  assert.match(bad.err, /H3_REF_STEPS='many' is not a int/);
  const unknown = run(PYTHON, ["-I", PATCH, "--notebook", nb, "--profile", "fastest"], env);
  assert.equal(unknown.code, 2);
  assert.match(unknown.err, /unknown profile 'fastest'/);
});

function manifestDir() {
  const { home, env } = sandbox();
  const dir = path.join(home, "batch");
  mkdirSync(path.join(dir, "first-frames"), { recursive: true });
  mkdirSync(path.join(dir, "prompts"));
  // a 1312x736 PNG is not needed: only existence and size are checked without ffprobe, and ffprobe
  // (when present) is fed a real picture written by ffmpeg below if it is available.
  const png = path.join(dir, "first-frames", "s01.png");
  const made = spawnSync("ffmpeg", ["-v", "error", "-y", "-f", "lavfi", "-i", "color=c=gray:s=1920x1080", "-frames:v", "1", png], { encoding: "utf8" });
  if (made.status !== 0) writeFileSync(png, "not really a png but non-empty");
  const prompt = "For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced.\n\nintegrated_multimodal_description: [Shot 1] 3D CG. test.\noverall_soundscape: N/A\nnon_diegetic_music: N/A\n";
  writeFileSync(path.join(dir, "prompts", "s01.txt"), prompt);
  const sha = createHash("sha256").update(prompt).digest("hex");
  return { dir, env, sha, hasFfprobe: spawnSync("ffprobe", ["-version"], { encoding: "utf8" }).status === 0 };
}

test("check_manifest.py: a sound manifest passes; 4 seconds and a stretched first frame only warn", { skip: !POSIX }, () => {
  const { dir, env, sha, hasFfprobe } = manifestDir();
  const good = path.join(dir, "jobs.json");
  writeFileSync(good, JSON.stringify({ jobs: [{ id: "s01", inference_mode: "first_frame", reference_images: ["first-frames/s01.png"], prompt_file: "prompts/s01.txt", duration_seconds: 5, width: 1312, height: 736, output_name: "s01-t1.mp4", prompt_sha256: sha }] }));
  const ok = run(PYTHON, ["-I", CHECK, good], env);
  assert.equal(ok.code, 0, ok.err + ok.out);
  // Without ffprobe (CI's web-checks runner has none) the only warning is that the aspect ratio went unchecked.
  assert.match(ok.out, hasFfprobe ? /0 error\(s\), 0 warning\(s\)/ : /ffprobe is not on PATH[\s\S]*0 error\(s\), 1 warning\(s\)/);

  const short = path.join(dir, "short.json");
  writeFileSync(short, JSON.stringify({ jobs: [{ id: "s01", inference_mode: "first_frame", reference_images: ["first-frames/s01.png"], prompt_file: "prompts/s01.txt", duration_seconds: 4, width: 1344, height: 768, output_name: "s01-t1.mp4" }] }));
  const warned = run(PYTHON, ["-I", CHECK, short], env);
  assert.equal(warned.code, 0, warned.err);
  assert.match(warned.out, /4 s is 107 frames, under the 124-frame range/);
  if (hasFfprobe) assert.match(warned.out, /first frame 1920x1080 \(1\.778\) does not match the 1344x768 canvas/);
  assert.match(warned.out, /0 error\(s\), [12] warning\(s\)/);
});

test("check_manifest.py: the errors that would otherwise cost compute units exit 1 and are all named", { skip: !POSIX }, () => {
  const { dir, env } = manifestDir();
  const bad = path.join(dir, "bad.json");
  writeFileSync(bad, JSON.stringify({ jobs: [
    { id: "s01", inference_mode: "first_frame", reference_images: ["first-frames/s01.png"], prompt_file: "prompts/s01.txt", duration_seconds: 5, width: 1280, height: 720, output_name: "s01-t1.mp4", prompt_sha256: "deadbeef" },
    { id: "s01", reference_images: ["first-frames/s01.png", "first-frames/missing.png"], prompt: "<Picture 3> walks [Shot 2] then the camera pans", duration_seconds: 16, width: 1344, height: 768, output_name: "s01-t1.mp4" },
    { id: "s02", inference_mode: "first_frame", reference_images: ["first-frames/s01.png", "first-frames/s01.png"], prompt: "no picture cited", duration_seconds: 6 },
  ] }));
  const result = run(PYTHON, ["-I", CHECK, bad], env);
  assert.equal(result.code, 1);
  for (const expected of [
    /height=720 must be a positive multiple of 32/, /prompt_sha256 deadbeef… does not match/, /duplicate id/, /reference image missing or empty: first-frames\/missing\.png/,
    /duration_seconds=16 must be 4-15/, /cites <Picture 3> but the job has 2 image\(s\)/, /duplicate output_name s01-t1\.mp4/, /first_frame needs exactly one image, got 2/,
  ]) assert.match(result.err, expected);
  assert.match(result.out, /prompt has \[Shot 2\]/);
  assert.match(result.out, /chains camera moves with 'then'/);
  assert.match(result.out, /s02: first_frame prompt never cites <Picture 1>/);
  const none = run(PYTHON, ["-I", CHECK, path.join(dir, "nope.json")], env);
  assert.equal(none.code, 1);
  assert.match(none.err, /cannot read as JSON/);
});

test("h3.sh: check runs the manifest checker without the upstream runner; batch refuses a broken manifest before calling it", { skip: !POSIX }, () => {
  const { dir, env } = manifestDir();
  const bad = path.join(dir, "bad.json");
  writeFileSync(bad, JSON.stringify({ jobs: [{ id: "s01", reference_images: ["first-frames/s01.png"], prompt: "x", duration_seconds: 5, width: 1000, height: 768 }] }));
  const noRunner = { ...env, MINIMAX_H3_COLAB_HOME: path.join(dir, "no-upstream") };
  const check = run("bash", [H3, "check", "--manifest", bad], noRunner);
  assert.equal(check.code, 1);
  assert.match(check.err, /width=1000 must be a positive multiple of 32/);
  // A fake upstream runner that records what it was called with.
  const home = path.join(dir, "upstream");
  mkdirSync(path.join(home, "scripts"), { recursive: true });
  writeFileSync(path.join(home, "scripts", "runner.py"), "import sys, pathlib\npathlib.Path(sys.argv[0]).with_name('calls.txt').write_text(' '.join(sys.argv[1:]))\n");
  const withRunner = { ...env, MINIMAX_H3_COLAB_HOME: home };
  const refused = run("bash", [H3, "batch", "--manifest", bad, "--output-dir", dir], withRunner);
  assert.equal(refused.code, 1);
  assert.match(refused.err, /fix the manifest or pass --no-check/);
  assert.ok(!existsSync(path.join(home, "scripts", "calls.txt")), "the runner was not called");
  const forced = run("bash", [H3, "batch", "--manifest", bad, "--no-check", "--output-dir", dir], withRunner);
  assert.equal(forced.code, 0, forced.err);
  assert.equal(readFileSync(path.join(home, "scripts", "calls.txt"), "utf8"), `batch --manifest ${bad} --output-dir ${dir}`);
  // single --mode first_frame without a size gets the 16:9-safe canvas; an explicit size is kept.
  run("bash", [H3, "single", "--mode", "first_frame", "--image", "a.png", "--prompt", "p.txt", "--output", "o.mp4"], withRunner);
  assert.equal(readFileSync(path.join(home, "scripts", "calls.txt"), "utf8"), "single --mode first_frame --image a.png --prompt p.txt --output o.mp4 --width 1312 --height 736");
  run("bash", [H3, "single", "--mode", "first_frame", "--width", "1344", "--height", "768", "--image", "a.png"], withRunner);
  assert.equal(readFileSync(path.join(home, "scripts", "calls.txt"), "utf8"), "single --mode first_frame --width 1344 --height 768 --image a.png");
  run("bash", [H3, "single", "--mode", "reference", "--image", "a.png"], withRunner);
  assert.equal(readFileSync(path.join(home, "scripts", "calls.txt"), "utf8"), "single --mode reference --image a.png");
});
