import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import test from "node:test";

import { compilationHash } from "../core/compilation.mjs";
import { approvedEpisodes } from "../core/state.mjs";
import { dramaFixture } from "../core/fixtures/load.mjs";
import { atomicWrite, readJson } from "../core/paths.mjs";
import { LOCALES } from "../core/schema.mjs";
import { visualHash } from "../core/timeline.mjs";
import { compilationSandbox, EPISODES, renderCards, SERIES, TITLES } from "../compile/fixture.mjs";
import { automationClient } from "./client.mjs";
import { descriptionBudget, metadataProblem, thumbnailCandidates, translationProblem } from "./compilation.mjs";
import { Automation, automatedVideos } from "./flow.mjs";

const TOKEN = `mkv_${"c".repeat(43)}`;
const SITE = "https://site.test";
const sha = (bytes) => createHash("sha256").update(bytes).digest("hex");
const shaFile = (file) => sha(readFileSync(file));
const OTHER_LOCALES = LOCALES.filter((locale) => locale !== "zh-TW");

test("the description budget leaves room for the chapter lines, and the planner's fields are held to YouTube's limits", () => {
  assert.equal(descriptionBudget(40), 5000 - 400 - 40 * 64);
  assert.equal(descriptionBudget(120), 500, "never less than a short paragraph");
  const candidates = [{ episode: "e1", shot: "opening" }];
  const good = { title: "重生回開服當天，她磨好了刀", titles: ["a", "b"], description: "她死在背叛者的慶功宴上。", tags: ["漫劇", "AI漫劇"], thumbnail: { headline: "她磨好了刀", tag: "重生", episode: "e1", shot: "opening" } };
  assert.equal(metadataProblem(good, candidates), null);
  assert.match(metadataProblem({ ...good, title: "x".repeat(101) }, candidates), /title/);
  assert.match(metadataProblem({ ...good, title: "（合集標題待企劃）" }, candidates), /placeholder/);
  assert.match(metadataProblem({ ...good, thumbnail: { ...good.thumbnail, headline: "這個標題有十三個字實在太長" } }, candidates), /headline/);
  assert.match(metadataProblem({ ...good, thumbnail: { ...good.thumbnail, shot: "other" } }, candidates), /thumbnail_candidates/);
  assert.equal(metadataProblem({ ...good, thumbnail: { ...good.thumbnail, shot: "other" } }, []), null, "no candidates: any picture name passes and the thumb draws on the theme");
  assert.match(metadataProblem({ ...good, tags: ["x".repeat(501)] }, candidates), /tags/);
  const chapters = { e1: "一", e2: "二" };
  assert.equal(translationProblem({ title: "Reborn", description: "d", tags: ["t"], chapters: { e1: "One", e2: "Two" } }, chapters), null);
  assert.match(translationProblem({ title: "Reborn", description: "d", tags: ["t"], chapters: { e1: "One" } }, chapters), /chapters lack e2/);
});

/** A site with what a compilation touches: the stages, the reviews, the series' done call. */
function fakeSite({ answers = {} } = {}) {
  const calls = { run: [], reports: [], reviews: [], compilations: [] };
  const projects = new Map();
  const reviewsOf = (slug) => projects.get(slug) ?? projects.set(slug, []).get(slug);
  const settings = {
    enabled: true, draft_interval_hours: 72, topics_per_run: 1, max_waiting_drafts: 3, topic_scope: ["AI"], topic_avoid: [], topic_from_site: true, topic_from_search: false,
    stage_models: {}, voice: { provider: "gemini", name: "Sulafat", style: "Relaxed", model: null, rate: "+0%" }, target_minutes_min: 1, target_minutes_max: 12, caption_locales: ["en"],
    max_drafts_per_month: 8, monthly_token_budget_millions: 20, max_verify_rounds: 3, max_retake_rounds: 2, auto_approve_audio: true,
    drama: { drama_enabled: true, style_preset: "cinematic-3d", subtitle_burn_in: true, music_enabled: false, character_voice_pool: [] },
  };
  const json = (body, status = 200) => Response.json(body, { status });
  const fetchImpl = async (url, init = {}) => {
    const { pathname } = new URL(url);
    const body = init.body ? JSON.parse(init.body) : null;
    if (pathname === "/api/video/automation/settings") return json(settings);
    if (pathname === "/api/video/automation/videos") return json([]);
    if (pathname === "/api/video/automation/series/next") return json({ job: null });
    if (pathname === "/api/video/automation/drama-requests/next") return json({ request: null });
    if (pathname === "/api/video/automation/run") {
      calls.run.push(body);
      const answer = answers[body.variant ? `${body.stage}:${body.variant}` : body.stage]?.(body) ?? {};
      return json({ text: JSON.stringify(answer), provider: "anthropic", model: "claude-sonnet-5", input_tokens: 10, output_tokens: 5, usage: { tokens: 15, token_budget: 20_000_000, drafts: 1, draft_budget: 8, calls: 1, failed_calls: 0 } });
    }
    const compiling = /^\/api\/video\/automation\/series\/([a-z0-9-]+)\/compilation\/done$/.exec(pathname);
    if (compiling) {
      calls.compilations.push({ series: compiling[1], action: "done" });
      return json({ slug: compiling[1] });
    }
    const match = /^\/api\/video\/reviews\/([a-z0-9-]+)(\/reviews)?$/.exec(pathname);
    if (match) {
      const [, slug, sub] = match;
      if (init.method === "PUT") {
        calls.reports.push({ slug, ...body });
        return json({ slug, reviews: reviewsOf(slug) });
      }
      if (sub && init.method === "POST") {
        const review = { id: `r${reviewsOf(slug).length + 1}`, status: "pending", choice: null, note: null, decided_at: null, created_at: new Date().toISOString(), ...body };
        reviewsOf(slug).unshift(review);
        calls.reviews.push(review);
        return json(review);
      }
      return json({ slug, title: slug, stage: "x", checklist: [], youtube_video_id: null, reviews: reviewsOf(slug) });
    }
    return json({ code: "not_found", detail: pathname }, 404);
  };
  return { calls, fetchImpl, reviewsOf, settings };
}

test("a compilation goes from the placeholder document to the confirmed upload without the owner, and the series is told", async () => {
  const box = compilationSandbox({ planned: false, rendered: false });
  const slug = `${SERIES}-full`;
  // The worker's context file, as startCompilation writes it, and one episode with a drawn
  // keyframe of a shot with a character in it: the thumbnail's picture.
  const episodes = EPISODES.map((each, index) => ({ slug: each, number: index + 1, title: TITLES[each], logline: `L${index + 1}`, recap: `R${index + 1}` }));
  atomicWrite(path.join(box.dir, "compilation.json"), JSON.stringify({ series: { slug: SERIES, title: "仙門風雲", genre: "rebirth-revenge" }, episodes, all_recaps: episodes.map(({ number, title, recap }) => ({ number, title, recap })), genre: "rebirth-revenge" }));
  const example = dramaFixture();
  const shot = example.scenes.find((scene) => scene.template === "shot" && scene.data?.characters?.length);
  const episodeDocs = path.join(box.root, "docs", "videos", EPISODES[0]);
  mkdirSync(episodeDocs, { recursive: true });
  writeFileSync(path.join(episodeDocs, "video.json"), JSON.stringify({ ...example, slug: EPISODES[0] }));
  const keyframes = path.join(box.work, EPISODES[0], "keyframes");
  mkdirSync(keyframes, { recursive: true });
  writeFileSync(path.join(keyframes, `${shot.id}.png`), Buffer.from("keyframe-png"));
  atomicWrite(path.join(keyframes, "manifest.json"), JSON.stringify({ shots: { [shot.id]: { file: `keyframes/${shot.id}.png`, sha256: sha(Buffer.from("keyframe-png")), judge: { overall: 9, passed: true, problems: [] } } } }));
  const candidates = thumbnailCandidates(box.work, box.root, episodes);
  assert.deepEqual(candidates.map((candidate) => [candidate.episode, candidate.shot, candidate.judge]), [[EPISODES[0], shot.id, 9]]);

  const state = { slug, title: "仙門風雲（合集）", status: "active", created_at: "2026-09-27T05:00:00Z", format: "drama", compilation: { series: SERIES, episodes: EPISODES }, series: { slug: SERIES, genre: "rebirth-revenge", lead: "female", visual_tier: "hybrid", compilation: true, hands_off: true }, replans: 0, verify_rounds: 0, verified: true, listener_done: true, retakes: 0, rewrites: 0, prompt_fixes: {}, notes: [] };
  mkdirSync(box.workdir, { recursive: true });
  atomicWrite(path.join(box.workdir, "auto.json"), JSON.stringify(state));

  const answers = {
    "planner:compilation": (body) => {
      assert.equal(body.payload.episodes.length, 3);
      assert.equal(body.payload.description_budget_bytes, descriptionBudget(3));
      assert.equal(body.payload.thumbnail_candidates[0].shot, shot.id);
      return { title: "重生回開服當天，她磨好了刀", titles: ["她已磨好刀", "背叛者還在做夢"], description: "她死在背叛者的慶功宴上，醒來是開服那天。", tags: ["漫劇", "AI漫劇", "一口氣看完"], thumbnail: { headline: "她磨好了刀", tag: "重生", episode: EPISODES[0], shot: shot.id } };
    },
    "translator:compilation": (body) => ({ title: `${body.payload.locale} title`, description: `${body.payload.locale} description`, tags: [`${body.payload.locale}`], chapters: Object.fromEntries(Object.keys(body.payload.chapters).map((key) => [key, `${body.payload.locale} ${key}`])) }),
  };
  const site = fakeSite({ answers });
  const out = { stdout: "", stderr: "" };
  const ctx = {
    root: box.root,
    env: { VIDEO_WORKDIR: box.work, MOKAAIR_VIDEO_TOKEN: TOKEN, MOKAAIR_SITE: SITE },
    home: box.base,
    fetch: site.fetchImpl,
    stdout: { write: (text) => (out.stdout += text) },
    stderr: { write: (text) => (out.stderr += text) },
    now: () => new Date("2026-09-27T05:00:00Z"),
    sleep: async () => {},
    EXIT: { ok: 0, lint: 1, usage: 2, owner: 3, external: 4, missing: 5 },
  };
  const runs = [];
  ctx.runCommand = async (command, runCtx) => {
    runs.push(command[0]);
    const doc = readJson(path.join(box.dir, "video.json"));
    if (command[0] === "render") {
      renderCards(box, doc);
      return { code: 0, out: "rendered" };
    }
    if (command[0] === "compile") {
      const cut = Buffer.from("the joined cut");
      writeFileSync(path.join(box.workdir, "final.mp4"), cut);
      const hash = compilationHash(doc, approvedEpisodes(doc, box.work));
      atomicWrite(path.join(box.workdir, "checks.json"), JSON.stringify({ ok: true, compilation_hash: hash, visual_hash: visualHash(doc), problems: [], metrics: { frames: 13411 } }));
      mkdirSync(path.join(box.workdir, "captions"), { recursive: true });
      atomicWrite(path.join(box.workdir, "captions", "manifest.json"), JSON.stringify({ compilation_hash: hash, locales: {}, skipped: {} }));
      atomicWrite(path.join(box.workdir, "timeline.json"), JSON.stringify({ fps: 30, sample_rate: 48000, total_frames: 13411, scenes: [], lines: [], chapters: [], speech_hash: null, compilation_hash: hash }));
      return { code: 0, out: "compiled" };
    }
    if (command[0] === "package") {
      mkdirSync(path.join(box.workdir, "upload"), { recursive: true });
      atomicWrite(path.join(box.workdir, "upload", "metadata.json"), JSON.stringify({ final_sha256: shaFile(path.join(box.workdir, "final.mp4")), compilation: true, download: "upload/final.mp4" }));
      return { code: 0, out: "packaged" };
    }
    if (command[0] === "review-push") {
      // The site approves the final cut on its quality check and the upload on its package check.
      const gate = command[command.indexOf("--gate") + 1];
      const file = gate === "final" ? path.join(box.workdir, "final.mp4") : path.join(box.workdir, "upload", "metadata.json");
      site.reviewsOf(slug).unshift({ id: `${gate}-1`, gate, status: "approved", choice: null, note: "依設定自動核准", decided_at: "2026-09-27T06:00:00Z", content_sha256: shaFile(file), payload: {} });
      return { code: 0, out: `${gate} submitted` };
    }
    const { main: cli } = await import("../cli.mjs");
    let text = "";
    const sink = { write: (chunk) => (text += chunk) };
    const code = await cli(command, { ...runCtx, runCommand: undefined, stdout: sink, stderr: sink });
    return { code, out: text };
  };
  const automation = new Automation(ctx, automationClient(ctx), site.settings);
  automation.refs = { script_writing: "short", formats: "tutorial", channel: "Mokaair", showcase: { scenes: [] }, minimal: example, drama: "the drama route", drama_example: example, drama_brief: "# brief", series: "the series route" };

  assert.match(await automation.step(), /title, description, tags and thumbnail planned \(重生回開服當天，她磨好了刀\)/);
  const planned = readJson(path.join(box.dir, "video.json"));
  assert.equal(planned.youtube.title, "重生回開服當天，她磨好了刀");
  assert.deepEqual(planned.thumbnail.data, { headline: "她磨好了刀", tag: "重生", shot: "thumb" });
  assert.equal(readFileSync(path.join(box.workdir, "keyframes", "thumb-source.png"), "utf8"), "keyframe-png");
  assert.equal(readJson(path.join(box.workdir, "keyframes", "manifest.json")).shots.thumb.source.shot, shot.id);
  assert.match(site.calls.run[0].instructions, /UPLOAD FIELDS of a COMPILATION[\s\S]*Genre and retention/);
  assert.match(await automation.step(), /chapter cards and thumbnail rendered/);
  assert.match(await automation.step(), /episodes joined into one cut/);
  for (const locale of OTHER_LOCALES) assert.match(await automation.step(), new RegExp(`${locale} title and description translated`));
  assert.deepEqual(readJson(path.join(box.dir, "i18n", "ja.json")).chapters, Object.fromEntries(EPISODES.map((each) => [each, `ja ${each}`])));
  assert.match(await automation.step(), /final sent to \/admin\/videos/);
  assert.match(await automation.step(), /the final is approved/);
  assert.match(await automation.step(), /upload package written/);
  assert.match(await automation.step(), /publish confirmation sent/);
  assert.match(await automation.step(), /the upload is confirmed/);
  assert.deepEqual(site.calls.compilations, [{ series: SERIES, action: "done" }]);
  const finished = automatedVideos(box.work).find((each) => each.slug === slug);
  assert.equal(finished.status, "done");
  assert.deepEqual(runs.filter((run) => ["render", "compile", "package"].includes(run)), ["render", "compile", "package"]);
  const report = site.calls.reports.at(-1);
  assert.equal(report.series_slug, SERIES);
  assert.equal(report.episode_number, undefined);
  assert.ok(existsSync(path.join(box.workdir, "approvals.json")));
});
