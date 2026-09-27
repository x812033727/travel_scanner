import assert from "node:assert/strict";
import { mkdirSync, writeFileSync } from "node:fs";
import path from "node:path";
import test from "node:test";

import { EXIT, freshIds, main } from "./cli.mjs";
import { FIXTURE_FILE, sandbox } from "./core/fixtures/load.mjs";

function capture(overrides = {}) {
  const out = { stdout: "", stderr: "" };
  const ctx = {
    stdout: { write: (text) => (out.stdout += text) },
    stderr: { write: (text) => (out.stderr += text) },
    now: () => new Date("2026-09-24T04:00:00Z"),
    ...overrides,
  };
  return { out, ctx };
}

test("lint on the example exits 0 and prints the estimate", async () => {
  const { out, ctx } = capture();
  assert.equal(await main(["lint", "--file", FIXTURE_FILE], ctx), EXIT.ok);
  assert.match(out.stdout, /fixture-minimal: 0 errors, 0 warnings/);
  assert.match(out.stdout, /00:00 開場/);
});

test("lint --json is machine-readable and a broken script exits 1", async () => {
  const box = sandbox();
  const file = path.join(box.dir, "video.json");
  writeFileSync(file, JSON.stringify({ schema_version: 1 }));
  const { out, ctx } = capture({ root: box.root });
  assert.equal(await main(["lint", "--slug", box.slug, "--json"], ctx), EXIT.lint);
  assert.ok(JSON.parse(out.stdout).errors.length > 0);
});

test("a media stage that is not built yet names its ticket and exits 5", async () => {
  const { out, ctx } = capture({ here: path.join(path.dirname(FIXTURE_FILE), "nowhere") });
  assert.equal(await main(["render", "--slug", "x"], ctx), EXIT.missing);
  assert.match(out.stderr, /2026-09-24-video-render-slides/);
});

test("a built media stage receives the command, its arguments and the exit codes", async () => {
  const box = sandbox();
  const here = path.join(box.base, "tools-video");
  mkdirSync(path.join(here, "tts"), { recursive: true });
  writeFileSync(path.join(here, "tts", "cli.mjs"), "export async function run(command, args, ctx) { ctx.stdout.write(`${command} ${args.join(' ')}`); return ctx.EXIT.external; }\n");
  const { out, ctx } = capture({ here });
  assert.equal(await main(["audition", "--voices", "a,b"], ctx), EXIT.external);
  assert.equal(out.stdout, "audition --voices a,b");
});

test("usage mistakes exit 2 with a message", async () => {
  for (const argv of [["frobnicate"], ["lint"], ["lint", "--bogus"], ["approve", "--slug", "x", "--gate", "maybe"], ["ids", "--count", "0"]]) {
    const { out, ctx } = capture();
    assert.equal(await main(argv, ctx), EXIT.usage, argv.join(" "));
    assert.ok(out.stderr.length > 0);
  }
  const { ctx } = capture();
  assert.equal(await main([], ctx), EXIT.usage);
});

test("status and approve work against VIDEO_WORKDIR", async () => {
  const box = sandbox();
  const env = { VIDEO_WORKDIR: box.work };
  const first = capture({ root: box.root, env });
  assert.equal(await main(["status", "--slug", box.slug], first.ctx), EXIT.ok);
  assert.match(first.out.stdout, /\[x\] brief\n {2}\[ \] outline approved: not approved yet/);
  const approval = capture({ root: box.root, env });
  assert.equal(await main(["approve", "--slug", box.slug, "--gate", "outline", "--note", "outline B"], approval.ctx), EXIT.ok);
  assert.match(approval.out.stdout, /approved outline: brief\.md sha256 [0-9a-f]{12} at 2026-09-24T04:00:00\.000Z/);
  const second = capture({ root: box.root, env });
  await main(["status", "--slug", box.slug], second.ctx);
  assert.match(second.out.stdout, /Next: a different agent fact-checks/);
});

test("a work directory inside the repository is refused", async () => {
  const box = sandbox();
  const { out, ctx } = capture({ root: box.root, env: { VIDEO_WORKDIR: path.join(box.root, "media") } });
  assert.equal(await main(["status", "--slug", box.slug], ctx), EXIT.usage);
  assert.match(out.stderr, /inside the repository/);
});

test("fresh ids avoid ids in use and look-alike characters", () => {
  let counter = 0;
  const sequence = [0, 0, 0, 0, 1, 1, 1, 1];
  assert.deepEqual(freshIds(1, new Set(["aaaa"]), () => sequence[counter++]), ["bbbb"]);
  for (const id of freshIds(50, new Set())) assert.match(id, /^[a-km-np-z2-9]{4}$/);
});
