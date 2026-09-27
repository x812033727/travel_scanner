import assert from "node:assert/strict";
import { createHash, randomBytes } from "node:crypto";
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import test from "node:test";

import { EXIT, main } from "../cli.mjs";
import { approve } from "../core/approvals.mjs";
import { fixture, fixtureLexicon, sandbox } from "../core/fixtures/load.mjs";
import { atomicWrite } from "../core/paths.mjs";
import { eachLine, LOCALES, textHash } from "../core/schema.mjs";
import { runCaptions } from "../core/stages.mjs";
import { buildTimeline, SAMPLE_RATE, speechHash, visualHash } from "../core/timeline.mjs";
import { sourceHashes } from "../core/translations.mjs";
import { COMPILATION_ITEM_IDS, ITEM_IDS } from "./checks.mjs";
import { jpegBytes } from "./test-images.mjs";
import { compilationSandbox, compileContext, EPISODE_FRAMES, EPISODES, fakeFfmpeg, writeEpisode, writeTranslations } from "../compile/fixture.mjs";

const TOKEN = `mkv_${"q".repeat(43)}`;
const SITE = "https://site.test";
const sha = (bytes) => createHash("sha256").update(bytes).digest("hex");

const VERIFY = `# verify-1: fixture-minimal

| # | claim | where | URL | HTTP | verdict | before → after |
| --- | --- | --- | --- | --- | --- | --- |
| c1 | 排行榜換第一名 | hook k7p2 | https://example.com/models | 200 | CONFIRMED | - |
| c9 | 五分鐘內決定 | hook m4qa | https://example.com/models | 200 | NOT FOUND | 刪掉數字 |
`;

/** A video that went through every stage: the files the stages write, without any media tool. */
function finishedVideo({ seconds = {} } = {}) {
  const box = sandbox();
  const doc = fixture();
  const lexicon = fixtureLexicon();
  const workdir = box.workdir;
  mkdirSync(workdir, { recursive: true });
  // Translations of every line and field, current with the zh-TW text.
  for (const locale of LOCALES.filter((each) => each !== "zh-TW")) {
    const lines = Object.fromEntries([...eachLine(doc)].map(({ line }) => [line.id, { source_hash: textHash(line.text), text: `line ${line.id}` }]));
    const chapters = Object.fromEntries(doc.scenes.filter((scene) => scene.chapter).map((scene) => [scene.id, `${locale} ${scene.id}`]));
    atomicWrite(path.join(box.dir, "i18n", `${locale}.json`), `${JSON.stringify({ title: `${locale} title`, description: `${locale} description`, tags: [`${locale} tag`], chapters, source_hashes: sourceHashes(doc), lines }, null, 2)}\n`);
  }
  writeFileSync(path.join(box.dir, "verify-1.md"), VERIFY);
  // The narration: five seconds a line unless the test says otherwise.
  const samples = {};
  for (const { line } of eachLine(doc)) samples[line.id] = (seconds[line.id] ?? 5) * SAMPLE_RATE;
  const timeline = { ...buildTimeline(doc, samples), speech_hash: speechHash(doc, lexicon) };
  atomicWrite(path.join(workdir, "timeline.json"), JSON.stringify(timeline));
  // The frames, one still per state, and a clean cache.
  const visual = visualHash(doc);
  const cache = {};
  const scenes = timeline.scenes.map((scene) => ({
    id: scene.id,
    kind: "stills",
    states: scene.states.map((state, index) => {
      const key = `${scene.id}${index}`.padEnd(16, "0");
      cache[key] = { transition: 0, problems: [] };
      return { reveal: state.reveal, still: `frames/${key}.png`, transition: [] };
    }),
  }));
  atomicWrite(path.join(workdir, "frames", "manifest.json"), JSON.stringify({ visual_hash: visual, theme_hash: "t", fps: 30, size: { width: 1920, height: 1080 }, scenes, thumbnail: "thumbnail.jpg" }));
  atomicWrite(path.join(workdir, "frames", "cache.json"), JSON.stringify(cache));
  writeFileSync(path.join(workdir, "thumbnail.jpg"), jpegBytes(1280, 720, 4000));
  // The cut and its checks.
  const final = randomBytes(2048);
  writeFileSync(path.join(workdir, "final.mp4"), final);
  atomicWrite(path.join(workdir, "checks.json"), JSON.stringify({ ok: true, speech_hash: timeline.speech_hash, visual_hash: visual, problems: [], metrics: { frames: timeline.total_frames, loudness: { integrated: -14 }, psnr: [] } }));
  runCaptions({ slug: box.slug, root: box.root, workdir, now: new Date("2026-09-27T00:00:00Z") });
  return { box, doc, workdir, finalSha: sha(final), timeline };
}

/** The site: the judge endpoint answers as told; every other URL (the description's links) opens. */
function site({ policy = () => Response.json({ detail: "Not Found" }, { status: 404 }) } = {}) {
  const calls = [];
  const fetchImpl = async (url, init = {}) => {
    calls.push({ url, init });
    if (url === `${SITE}/api/video/automation/judge/policy`) return policy(init);
    return new Response("", { status: 200 });
  };
  return { calls, fetchImpl };
}

function context(box, fetchImpl) {
  const out = { stdout: "", stderr: "" };
  return {
    out,
    ctx: {
      root: box.root,
      env: { VIDEO_WORKDIR: box.work, MOKAAIR_VIDEO_TOKEN: TOKEN, MOKAAIR_SITE: SITE },
      home: box.base,
      fetch: fetchImpl,
      sleep: async () => {},
      stdout: { write: (text) => (out.stdout += text) },
      stderr: { write: (text) => (out.stderr += text) },
      now: () => new Date("2026-09-27T02:00:00Z"),
    },
  };
}

const readReport = (workdir) => JSON.parse(readFileSync(path.join(workdir, "review", "qa.json"), "utf8"));

test("a finished video passes every check but the judge that is not built yet, and qa.json says so", async () => {
  const { box, workdir, finalSha } = finishedVideo();
  await approve({ gate: "audio", docDir: box.dir, workdir, now: new Date("2026-09-27T01:00:00Z") });
  const server = site();
  const { out, ctx } = context(box, server.fetchImpl);
  assert.equal(await main(["qa", "--slug", box.slug], ctx), EXIT.lint, out.stderr);
  const report = readReport(workdir);
  assert.deepEqual(Object.keys(report), ["ok", "final_sha256", "items"]);
  assert.equal(report.ok, false);
  assert.equal(report.final_sha256, finalSha);
  assert.deepEqual(report.items.map((item) => item.id), ITEM_IDS);
  const failed = report.items.filter((item) => !item.ok);
  assert.deepEqual(failed.map((item) => [item.id, item.detail]), [["policy", "judge endpoint not available"]]);
  const byId = Object.fromEntries(report.items.map((item) => [item.id, item]));
  assert.match(byId.pace.detail, /^5 slide states, the longest [\d.]+ s; none over 15 s$/);
  assert.match(byId.captions.detail, /caption files for zh-TW, en, ja, ko, zh-CN, every translation current/);
  assert.match(byId.metadata.detail, /for zh-TW, en, ja, ko, zh-CN; 3 chapters$/);
  assert.equal(byId.facts.detail, "verify-1.md marks 1 claims NOT FOUND (9); no scene cites them");
  assert.equal(byId.links.detail, "1 links open");
  assert.match(byId.thumbnail.detail, /^1280x720 JPEG, 4 KB; the headline is about 34 px tall at 320 px wide$/);
  assert.match(byId.disclosure.detail, /^no disclosure needed/);
  assert.match(byId.narration.detail, /approved at 2026-09-27T01:00:00/);
  // The links: the one source URL, fetched with the editorial agent and never the site token.
  const links = server.calls.filter((call) => call.url === "https://example.com/models");
  assert.equal(links.length, 1, "one URL, checked once though five descriptions list it");
  assert.equal(links[0].init.headers["User-Agent"], "Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)");
  assert.equal(links[0].init.headers.Authorization, undefined);
  // The judge: called with the script through the site client, with the token.
  const judge = server.calls.find((call) => call.url.endsWith("/judge/policy"));
  assert.equal(judge.init.headers.Authorization, `Bearer ${TOKEN}`);
  const body = JSON.parse(judge.init.body);
  assert.deepEqual(Object.keys(body), ["slug", "script", "viewpoint"], "the judge's strict request model");
  assert.equal(body.slug, box.slug);
  assert.equal(body.script.split("\n\n").length, 3, "one block per scene");
  assert.ok(body.script.startsWith("每次有新模型出來"));
  assert.equal(body.viewpoint, "排行榜只是起點；我自己是先看工作類型，再看等待時間和價格。");
  assert.doesNotMatch(out.stdout + out.stderr + readFileSync(path.join(workdir, "review", "qa.json"), "utf8"), new RegExp(TOKEN), "the token is never printed or written");
  assert.match(out.stdout, /\[ \] policy: judge endpoint not available/);
  assert.match(out.stdout, /10 of 11 checks passed/);
});

test("with the judge passing, everything passes and the exit code is 0", async () => {
  const { box, workdir } = finishedVideo();
  await approve({ gate: "audio", docDir: box.dir, workdir, now: new Date("2026-09-27T01:00:00Z") });
  const note = "Jev：符合立場 0.90、有示範 0.80、建議 0.10、業配 0.00，通過";
  const server = site({ policy: () => Response.json({ stance: 0.9, demo: 0.8, advice: 0.1, sponsored: 0, passed: true, note }) });
  const { out, ctx } = context(box, server.fetchImpl);
  assert.equal(await main(["qa", "--slug", box.slug], ctx), EXIT.ok, out.stderr);
  const report = readReport(workdir);
  assert.equal(report.ok, true);
  assert.equal(report.items.find((item) => item.id === "policy").detail, note);
  assert.match(out.stdout, /11 of 11 checks passed \(final\.mp4 sha256 [0-9a-f]{12}\)/);
});

test("a slide left up too long, a broken link, a cited NOT FOUND claim and a stale caption each fail their item", async () => {
  const { box, workdir, doc } = finishedVideo({ seconds: { k7p2: 12, m4qa: 8 } });
  await approve({ gate: "audio", docDir: box.dir, workdir, now: new Date("2026-09-27T01:00:00Z") });
  // The hook scene now cites the claim the fact-check dropped; claims change no hash.
  doc.scenes[0].claims = ["c9"];
  writeFileSync(path.join(box.dir, "video.json"), JSON.stringify(doc));
  // The English translation of one line is older than the zh-TW text.
  const en = JSON.parse(readFileSync(path.join(box.dir, "i18n", "en.json"), "utf8"));
  en.lines.k7p2.source_hash = "000000000000";
  writeFileSync(path.join(box.dir, "i18n", "en.json"), JSON.stringify(en));
  const server = site({ policy: () => Response.json({ passed: true }) });
  const broken = async (url, init) => (url.startsWith("https://example.com/") ? new Response("gone", { status: 404 }) : server.fetchImpl(url, init));
  const { ctx } = context(box, broken);
  assert.equal(await main(["qa", "--slug", box.slug], ctx), EXIT.lint);
  const report = readReport(workdir);
  const failed = Object.fromEntries(report.items.filter((item) => !item.ok).map((item) => [item.id, item.detail]));
  assert.deepEqual(Object.keys(failed), ["pace", "captions", "facts", "links"]);
  assert.match(failed.pace, /^1 of 5 slide states stay over 15 s: hook state 0 \(2[01]\.\d s\)$/);
  assert.match(failed.captions, /i18n\/en\.json: 1 translations older than the zh-TW line: k7p2/);
  assert.equal(failed.facts, "claim 9 was NOT FOUND in verify-1.md but hook still cites it");
  assert.equal(failed.links, "1 of 1 links do not open: https://example.com/models (HTTP 404)");
});

test("stages that were not run, or ran for an older script, fail their items with the command to run", async () => {
  const { box, workdir } = finishedVideo();
  // Nothing approved, no render, and the cut was checked for another script.
  const checks = JSON.parse(readFileSync(path.join(workdir, "checks.json"), "utf8"));
  writeFileSync(path.join(workdir, "checks.json"), JSON.stringify({ ...checks, speech_hash: "stale" }));
  writeFileSync(path.join(workdir, "frames", "cache.json"), JSON.stringify({ hook000000000000: { transition: 0, problems: ["text does not fit even at 60% size: \"AI 模型怎麼挑？\""] } }));
  const { ctx } = context(box, site().fetchImpl);
  assert.equal(await main(["qa", "--slug", box.slug], ctx), EXIT.lint);
  const byId = Object.fromEntries(readReport(workdir).items.map((item) => [item.id, item]));
  assert.match(byId.assemble.detail, /older script.*run assemble again/);
  assert.equal(byId.render.detail, 'hook state 0: text does not fit even at 60% size: "AI 模型怎麼挑？"');
  assert.equal(byId.narration.detail, "the narration has not been approved yet");
  assert.equal(byId.pace.ok, true);
});

test("a blank channel stance and a failed verdict are failed items, exit 1", async () => {
  const { box, workdir } = finishedVideo();
  const blank = site({ policy: () => Response.json({ code: "video_judge_not_enabled", detail: "頻道立場還是空白，Jev 沒有依據可以判斷" }, { status: 409 }) });
  const first = context(box, blank.fetchImpl);
  assert.equal(await main(["qa", "--slug", box.slug], first.ctx), EXIT.lint, first.out.stderr);
  assert.deepEqual(readReport(workdir).items.find((item) => item.id === "policy"), { id: "policy", ok: false, detail: "channel stance is blank; the judge has nothing to judge against" });
  const note = "Jev：符合立場 0.30、有示範 0.70、建議 0.05、業配 0.10，沒過";
  const failed = site({ policy: () => Response.json({ stance: 0.3, demo: 0.7, advice: 0.05, sponsored: 0.1, passed: false, note }) });
  const second = context(box, failed.fetchImpl);
  assert.equal(await main(["qa", "--slug", box.slug], second.ctx), EXIT.lint);
  assert.deepEqual(readReport(workdir).items.find((item) => item.id === "policy"), { id: "policy", ok: false, detail: note });
});

test("the judge being unreachable or out of budget is an external failure, exit 4; a revoked token is the owner's, exit 3", async () => {
  const { box, workdir } = finishedVideo();
  const down = site({ policy: () => { throw new TypeError("fetch failed"); } });
  const first = context(box, down.fetchImpl);
  assert.equal(await main(["qa", "--slug", box.slug], first.ctx), EXIT.external, first.out.stderr);
  const policy = readReport(workdir).items.find((item) => item.id === "policy");
  assert.equal(policy.ok, false);
  assert.match(policy.detail, /^the judge call failed: cannot reach https:\/\/site\.test/);
  const spent = site({ policy: () => Response.json({ code: "jev_budget_exhausted", detail: "Jev 今天的次數用完了" }, { status: 429 }) });
  const budget = context(box, spent.fetchImpl);
  assert.equal(await main(["qa", "--slug", box.slug], budget.ctx), EXIT.external);
  assert.equal(readReport(workdir).items.find((item) => item.id === "policy").detail, "the judge call failed: Jev 今天的次數用完了");
  const upstream = site({ policy: () => Response.json({ code: "video_judge_upstream_failed", detail: "Jev 暫時無法判斷" }, { status: 502 }) });
  const jev = context(box, upstream.fetchImpl);
  assert.equal(await main(["qa", "--slug", box.slug], jev.ctx), EXIT.external);
  assert.equal(readReport(workdir).items.find((item) => item.id === "policy").detail, "the judge call failed: Jev 暫時無法判斷");
  const revoked = site({ policy: () => Response.json({ code: "video_tool_token_invalid", detail: "token revoked" }, { status: 401 }) });
  const second = context(box, revoked.fetchImpl);
  assert.equal(await main(["qa", "--slug", box.slug], second.ctx), EXIT.owner);
  assert.equal(readReport(workdir).items.find((item) => item.id === "policy").detail, "the judge call failed: token revoked");
  const none = context(box, revoked.fetchImpl);
  none.ctx.env = { VIDEO_WORKDIR: box.work, MOKAAIR_SITE: SITE };
  assert.equal(await main(["qa", "--slug", box.slug], none.ctx), EXIT.owner);
  assert.match(readReport(workdir).items.find((item) => item.id === "policy").detail, /no video tool token yet/);
});

test("the disclosure answer goes into the upload package once, so the publish gate's hash holds", async () => {
  const { box, workdir } = finishedVideo();
  const metadataFile = path.join(workdir, "upload", "metadata.json");
  atomicWrite(metadataFile, `${JSON.stringify({ slug: box.slug, title: "t", final_sha256: "x" }, null, 2)}\n`);
  const server = site();
  await main(["qa", "--slug", box.slug], context(box, server.fetchImpl).ctx);
  const written = readFileSync(metadataFile, "utf8");
  const metadata = JSON.parse(written);
  assert.deepEqual(Object.keys(metadata), ["slug", "title", "final_sha256", "contains_synthetic_media", "disclosure_reason"]);
  assert.equal(metadata.contains_synthetic_media, false);
  assert.match(readReport(workdir).items.at(-1).detail, /written to upload\/metadata\.json$/);
  const again = context(box, server.fetchImpl);
  await main(["qa", "--slug", box.slug], again.ctx);
  assert.equal(readFileSync(metadataFile, "utf8"), written, "the same answer leaves the same bytes");
  assert.match(readReport(workdir).items.at(-1).detail, /already says so$/);
});

test("usage: qa needs a slug, and a script with lint errors is sent to lint first", async () => {
  const box = sandbox();
  const { out, ctx } = context(box, site().fetchImpl);
  assert.equal(await main(["qa"], ctx), EXIT.usage);
  assert.match(out.stderr, /qa needs --slug/);
  const doc = fixture();
  doc.youtube.title = "x".repeat(101);
  writeFileSync(path.join(box.dir, "video.json"), JSON.stringify(doc));
  const second = context(box, site().fetchImpl);
  assert.equal(await main(["qa", "--slug", box.slug], second.ctx), EXIT.lint);
  assert.match(second.out.stdout, /has 1 lint errors; run lint first/);
  assert.equal(existsSync(path.join(box.workdir, "review", "qa.json")), false);
});

const COMPILATION_FRAMES = EPISODES.reduce((sum, slug) => sum + EPISODE_FRAMES[slug], 0) + EPISODES.length * 60 + 120;

test("a compiled series passes its six checks without a judge, and a re-cut episode fails the join", async () => {
  const box = compilationSandbox({ captions: Object.fromEntries(EPISODES.map((slug) => [slug, LOCALES])) });
  writeTranslations(box, box.doc);
  const fake = fakeFfmpeg({ total: COMPILATION_FRAMES });
  const compiled = compileContext(box, fake);
  assert.equal(await main(["compile", "--slug", box.slug], compiled.ctx), EXIT.ok, compiled.out.stderr);
  const server = site();
  const { out, ctx } = context(box, server.fetchImpl);
  assert.equal(await main(["qa", "--slug", box.slug], ctx), EXIT.ok, out.stdout + out.stderr);
  const report = readReport(box.workdir);
  assert.deepEqual(Object.keys(report), ["ok", "final_sha256", "kind", "items"]);
  assert.equal(report.kind, "compilation");
  assert.equal(report.ok, true);
  assert.deepEqual(report.items.map((item) => item.id), COMPILATION_ITEM_IDS);
  const byId = Object.fromEntries(report.items.map((item) => [item.id, item]));
  assert.match(byId.assemble.detail, new RegExp(`^${COMPILATION_FRAMES} frames, -14.4 LUFS; every check passed$`));
  assert.equal(byId.captions.detail, "caption files for zh-TW, en, ja, ko, zh-CN, merged from every episode");
  assert.match(byId.metadata.detail, /for zh-TW, en, ja, ko, zh-CN; 3 chapters$/);
  assert.equal(byId.links.detail, "the description has no links");
  assert.match(byId.disclosure.detail, /^tick altered or synthetic content: a drama/);
  assert.equal(server.calls.some((call) => call.url.endsWith("/judge/policy")), false, "no judge for a compilation");
  assert.match(out.stdout, /6 of 6 checks passed/);

  // An episode re-cut after the join: the join is of other cuts, and so are the captions.
  writeEpisode(box.work, "wuxia-ep-2");
  const again = context(box, site().fetchImpl);
  assert.equal(await main(["qa", "--slug", box.slug], again.ctx), EXIT.lint);
  const failed = Object.fromEntries(readReport(box.workdir).items.filter((item) => !item.ok).map((item) => [item.id, item.detail]));
  assert.deepEqual(Object.keys(failed), ["assemble", "captions", "metadata"]);
  assert.equal(failed.assemble, "checks.json was written for other cuts or cards; run compile again");
  assert.equal(failed.captions, "captions were merged for other cuts; run compile again");
  assert.match(failed.metadata, /chapter times are unknown; run compile/);

  // An episode never approved is named.
  writeEpisode(box.work, "wuxia-ep-3", { approved: false });
  const never = context(box, site().fetchImpl);
  await main(["qa", "--slug", box.slug], never.ctx);
  assert.match(readReport(box.workdir).items[0].detail, /episodes not cleared for upload: wuxia-ep-3/);
});

test("a compilation missing a locale's captions in one episode fails its captions item and names the episode", async () => {
  const box = compilationSandbox({ captions: { "wuxia-ep-2": ["zh-TW"] } });
  writeTranslations(box, box.doc);
  const compiled = compileContext(box, fakeFfmpeg({ total: COMPILATION_FRAMES }));
  assert.equal(await main(["compile", "--slug", box.slug], compiled.ctx), EXIT.ok, compiled.out.stderr);
  const { ctx } = context(box, site().fetchImpl);
  assert.equal(await main(["qa", "--slug", box.slug], ctx), EXIT.lint);
  const captions = readReport(box.workdir).items.find((item) => item.id === "captions");
  assert.match(captions.detail, /en: no caption file, 1 episodes have none \(wuxia-ep-2\)/);
  assert.match(captions.detail, /ja: no caption file, 3 episodes have none/);
});
