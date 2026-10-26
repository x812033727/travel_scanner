import assert from "node:assert/strict";
import { mkdirSync, mkdtempSync, rmSync, writeFileSync } from "node:fs";
import os from "node:os";
import path from "node:path";
import test from "node:test";

import { siteBrandingNotice, sitePackage } from "./site.mjs";

const SITE = "https://mokaair.test";
const pkg = (id, hash) => ({ series: null, id, hash, installed_at: null, intro: { sha256: "1".repeat(64), frames: 150, size: 1 }, outro: { sha256: "2".repeat(64), frames: 630, size: 1 } });
const V4 = pkg("mokaair-brand-package-v4-endscreen", "4".repeat(64));
const V2 = pkg("mokaair-brand-package-v2-cc", "2".repeat(64));
const SERIES = pkg("mokaair-sothatswhy-bookends-v3-endscreen", "3".repeat(64));
const curio = { format: "drama", look: { preset: "cute-mystery" } };
const explainer = { format: "drama", look: { preset: "flat-explainer" } };

/** The web route in front of GET /video/media/branding: a route → [status, body] table. */
function fakeSite(routes) {
  const calls = [];
  const fetch = async (url, init) => {
    const route = url.replace(`${SITE}/api/video/media/`, "");
    calls.push({ route, signal: init.signal });
    const answer = routes[route];
    if (answer instanceof Error) throw answer;
    const [status, body] = answer ?? [404, { code: "video_media_route_unknown" }];
    return Response.json(body, { status });
  };
  return { calls, fetch };
}

const ctxFor = (site, env = { MOKAAIR_SITE: SITE, MOKAAIR_VIDEO_TOKEN: "mkv_test" }) => ({ env, home: "/nonexistent-home", fetch: site.fetch });
const notInstalled = [404, { code: "video_branding_not_installed", detail: "none" }];

test("the same package as the site's worker says nothing", async () => {
  const site = fakeSite({ branding: [200, V4] });
  assert.equal(await siteBrandingNotice({ doc: curio, local: V4, ctx: ctxFor(site) }), null);
  assert.equal(site.calls.length, 1);
  assert.ok(site.calls[0].signal instanceof AbortSignal, "the question has a deadline");
});

test("an older package or none at all names both and says how to match the site", async () => {
  const site = fakeSite({ branding: [200, V4] });
  const older = await siteBrandingNotice({ doc: curio, local: V2, ctx: ctxFor(site) });
  assert.equal(older, `WARN branding: this build pins mokaair-brand-package-v2-cc (${"2".repeat(12)}) but the site's worker uses mokaair-brand-package-v4-endscreen (${"4".repeat(12)}); to match it, stop and run \`node tools/video/cli.mjs branding --pull\`, then build again`);
  const none = await siteBrandingNotice({ doc: curio, local: null, ctx: ctxFor(site) });
  assert.match(none, /^WARN branding: this build pins no bookends but the site's worker uses mokaair-brand-package-v4-endscreen/);
});

test("a site worker without a package is named as such, and none on both sides agrees", async () => {
  const site = fakeSite({ branding: notInstalled });
  assert.match(await siteBrandingNotice({ doc: curio, local: V4, ctx: ctxFor(site) }), /the site's worker uses no bookends; it has none installed or has them switched off; check `branding --json` on the host$/);
  assert.equal(await siteBrandingNotice({ doc: curio, local: null, ctx: ctxFor(site) }), null);
});

test("an explainer asks for its series first and falls back to the channel only when the series has none", async () => {
  const series = fakeSite({ "branding/series/sothatswhy": [200, SERIES], branding: [200, V4] });
  assert.equal((await sitePackage(explainer, { site: SITE, token: "t", fetchImpl: series.fetch, attempts: 1 })).id, SERIES.id);
  assert.deepEqual(series.calls.map((call) => call.route), ["branding/series/sothatswhy"]);
  const fallback = fakeSite({ "branding/series/sothatswhy": notInstalled, branding: [200, V4] });
  assert.equal((await sitePackage(explainer, { site: SITE, token: "t", fetchImpl: fallback.fetch, attempts: 1 })).id, V4.id);
  const off = fakeSite({ "branding/series/sothatswhy": [404, { code: "video_branding_disabled" }], branding: [200, V4] });
  assert.equal(await sitePackage(explainer, { site: SITE, token: "t", fetchImpl: off.fetch, attempts: 1 }), null);
  assert.deepEqual(off.calls.map((call) => call.route), ["branding/series/sothatswhy"], "switched off is not a fallback");
  const channel = fakeSite({ branding: [200, V4] });
  await sitePackage(curio, { site: SITE, token: "t", fetchImpl: channel.fetch, attempts: 1 });
  assert.deepEqual(channel.calls.map((call) => call.route), ["branding"], "奇聞檔案局 uses the channel's");
});

test("no token, no site or a failing site only says the comparison was not made", async () => {
  const site = fakeSite({ branding: [200, V4] });
  assert.match(await siteBrandingNotice({ doc: curio, local: V4, ctx: ctxFor(site, {}) }), /^branding: not compared .*no video tool token/);
  assert.equal(site.calls.length, 0);
  const down = fakeSite({ branding: new TypeError("fetch failed") });
  assert.match(await siteBrandingNotice({ doc: curio, local: V4, ctx: ctxFor(down) }), /^branding: could not compare .*cannot reach https:\/\/mokaair\.test: fetch failed.*branding --pull --dry-run/);
  assert.equal(down.calls.length, 1, "one try: a build does not wait out retries");
  const broken = fakeSite({ branding: [503, { code: "video_branding_broken", detail: "current.json is not JSON" }] });
  assert.match(await siteBrandingNotice({ doc: curio, local: V4, ctx: ctxFor(broken) }), /could not compare .*current\.json is not JSON/);
});

test("a credentials file that does not parse only says the comparison was not made", async (t) => {
  const home = mkdtempSync(path.join(os.tmpdir(), "video-site-home-"));
  t.after(() => rmSync(home, { recursive: true, force: true }));
  mkdirSync(path.join(home, ".mokaair"));
  writeFileSync(path.join(home, ".mokaair", "video-tool.json"), "{not json");
  const site = fakeSite({ branding: [200, V4] });
  assert.match(await siteBrandingNotice({ doc: curio, local: V4, ctx: { env: {}, home, fetch: site.fetch } }), /^branding: could not compare with the site's worker \(/);
  assert.equal(site.calls.length, 0);
});
