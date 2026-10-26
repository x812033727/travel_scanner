import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { existsSync, readFileSync } from "node:fs";
import path from "node:path";
import test from "node:test";

import { brandingHash, currentBrandingFile, readCurrentBranding } from "../core/branding.mjs";
import { sandbox } from "../core/fixtures/load.mjs";
import { pullPackage, run } from "./cli.mjs";

const SITE = "https://mokaair.test";
const EXIT = { ok: 0, lint: 1, usage: 2, owner: 3, external: 4, missing: 5 };
const sha = (bytes) => createHash("sha256").update(bytes).digest("hex");
const INTRO = Buffer.from("site intro");
const OUTRO = Buffer.from("site outro");

const tools = { ffprobe: "probe", ffmpeg: "encode" };
const exec = async (tool, args) => ({ stdout: JSON.stringify({ streams: [
  { codec_type: "video", width: 1920, height: 1080, r_frame_rate: "30/1", nb_read_packets: path.basename(args.at(-1)) === "intro.mp4" ? "150" : "90" },
  { codec_type: "audio", sample_rate: "48000", channels: 2, duration: path.basename(args.at(-1)) === "intro.mp4" ? "5" : "3" },
] }), stderr: "" });

function view(changes = {}) {
  const clips = { intro: { sha256: sha(INTRO), frames: 150, size: INTRO.length }, outro: { sha256: sha(OUTRO), frames: 90, size: OUTRO.length } };
  return { series: null, id: "mokaair-brand-package-v4-endscreen", hash: brandingHash(clips), installed_at: "2026-10-12T10:35:01.804Z", ...clips, ...changes };
}

/** The web route in front of apps/api/app/video_media: the description, then the files by SHA-256. */
function fakeSite({ answer = view(), files = { [sha(INTRO)]: INTRO, [sha(OUTRO)]: OUTRO }, refuse = null } = {}) {
  const calls = [];
  const fetchImpl = async (url, init) => {
    assert.equal(init.headers.Authorization, "Bearer mkv_test");
    const route = url.replace(`${SITE}/api/video/media/`, "");
    calls.push(route);
    if (route === "branding" || route.startsWith("branding/series/")) {
      if (refuse) return Response.json(refuse.body, { status: refuse.status });
      return Response.json(answer);
    }
    const bytes = files[route.replace("branding/files/", "")];
    if (!bytes) return Response.json({ code: "video_branding_file_not_found", detail: "gone" }, { status: 404 });
    return new Response(bytes, { headers: { "Content-Type": "video/mp4", "Content-Length": String(bytes.length) } });
  };
  return { calls, fetchImpl };
}

function context(box, site, { token = "mkv_test" } = {}) {
  const out = [];
  const err = [];
  const env = { VIDEO_WORKDIR: box.work, MOKAAIR_SITE: SITE, ...(token ? { MOKAAIR_VIDEO_TOKEN: token } : {}) };
  return {
    out, err,
    ctx: {
      env, root: box.root, home: box.base, EXIT, now: () => new Date("2026-10-26T01:00:00Z"),
      stdout: { write: (value) => out.push(value) }, stderr: { write: (value) => err.push(value) },
      fetch: site.fetchImpl, sleep: async () => {}, ffmpeg: { locate: async () => tools, run: exec },
    },
  };
}

test("pull installs the site worker's package, then finds it current and downloads nothing", async () => {
  const box = sandbox();
  const site = fakeSite();
  const first = context(box, site);
  assert.equal(await run("branding", ["--pull"], first.ctx), EXIT.ok, first.err.join(""));
  const installed = readCurrentBranding(box.work);
  assert.equal(installed.hash, view().hash);
  assert.equal(installed.id, "mokaair-brand-package-v4-endscreen");
  assert.equal(readFileSync(installed.intro.file, "utf8"), "site intro");
  assert.match(first.out.join(""), /^Installed: mokaair-brand-package-v4-endscreen/m);
  assert.equal(existsSync(path.join(box.work, `_branding-pull-${view().hash}`)), false, "the scratch package is removed");
  assert.deepEqual(site.calls, ["branding", `branding/files/${sha(INTRO)}`, `branding/files/${sha(OUTRO)}`]);

  const again = context(box, site);
  assert.equal(await run("branding", ["--pull", "--dry-run"], again.ctx), EXIT.ok);
  assert.match(again.out.join(""), /The site's worker uses the same package\.\nCurrent: /);
  assert.equal(site.calls.length, 4, "only the description is asked for again");
});

test("dry-run downloads and checks the package but installs nothing", async () => {
  const box = sandbox();
  const site = fakeSite();
  const { ctx, out } = context(box, site);
  assert.equal(await run("branding", ["--pull", "--dry-run"], ctx), EXIT.ok);
  assert.match(out.join(""), /^Validated: mokaair-brand-package-v4-endscreen/m);
  assert.equal(readCurrentBranding(box.work), null);
  assert.equal(existsSync(path.join(box.work, `_branding-pull-${view().hash}`)), false);
});

test("bytes that do not hash, or a worker hash the files do not make, install nothing", async () => {
  const box = sandbox();
  const tampered = fakeSite({ files: { [sha(INTRO)]: Buffer.from("other bytes"), [sha(OUTRO)]: OUTRO } });
  const first = context(box, tampered);
  assert.equal(await run("branding", ["--pull"], first.ctx), EXIT.external);
  assert.match(first.err.join(""), /hash to/);
  assert.equal(readCurrentBranding(box.work), null);

  const client = { site: SITE, token: "mkv_test", fetchImpl: fakeSite({ answer: view({ hash: "f".repeat(64) }) }).fetchImpl, sleep: async () => {} };
  await assert.rejects(pullPackage({ workBase: box.work, tools, exec, client }), /files hash to .*nothing installed/);
  assert.equal(readCurrentBranding(box.work), null);
  assert.equal(existsSync(path.join(box.work, `_branding-pull-${"f".repeat(64)}`)), false);
});

test("a site with nothing to hand out, or no token, is the owner's to fix", async () => {
  const box = sandbox();
  const refused = fakeSite({ refuse: { status: 404, body: { code: "video_branding_not_installed", detail: "正式站的工人還沒有安裝片頭片尾素材包" } } });
  const first = context(box, refused);
  assert.equal(await run("branding", ["--pull"], first.ctx), EXIT.owner);
  assert.match(first.err.join(""), /branding --pull: 正式站的工人還沒有安裝/);
  const site = fakeSite();
  const noToken = context(box, site, { token: null });
  assert.equal(await run("branding", ["--pull"], noToken.ctx), EXIT.owner);
  assert.match(noToken.err.join(""), /cli\.mjs login/);
  assert.deepEqual(site.calls, []);
  assert.equal(existsSync(path.join(box.work, "_branding")), false);
});

test("an answer without a well-formed hash is refused before anything is written or removed", async () => {
  const box = sandbox();
  const site = fakeSite({ answer: view({ hash: "../../outside" }) });
  const { ctx, err } = context(box, site);
  assert.equal(await run("branding", ["--pull"], ctx), EXIT.usage);
  assert.match(err.join(""), /no package hash/);
  assert.deepEqual(site.calls, ["branding"]);
});

test("a series pull asks for the series and changes only its default", async () => {
  const box = sandbox();
  const site = fakeSite({ answer: view({ series: "sothatswhy" }) });
  const { ctx } = context(box, site);
  assert.equal(await run("branding", ["--pull", "--series", "sothatswhy"], ctx), EXIT.ok);
  assert.equal(site.calls[0], "branding/series/sothatswhy");
  assert.equal(readCurrentBranding(box.work, { series: "sothatswhy" }).hash, view().hash);
  assert.equal(existsSync(path.join(box.work, currentBrandingFile())), false);
  await assert.rejects(run("branding", ["--pull", "--install", "x"], ctx), /not both/);
});
