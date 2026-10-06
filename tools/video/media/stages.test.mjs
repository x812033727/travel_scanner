import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { existsSync, rmSync, writeFileSync } from "node:fs";
import path from "node:path";
import test from "node:test";

import { tempDir } from "../core/fixtures/load.mjs";
import { readCache, readJobs } from "./cache.mjs";
import { statusText } from "./cli.mjs";
import { MediaError } from "./client.mjs";
import { capProblem, ledgerTotals, readLedger, reservedEntries } from "./ledger.mjs";
import { choiceFor, IMAGE_SIZES, imagePrice, imageSizeFor, imageStatus, JUDGE_USD_PER_CALL, Stage, statusProblem, takesStyleReference } from "./stages.mjs";

const PRO = "gemini-3-pro-image";
const FLASH = "gemini-3.1-flash-image";
const MINI = "image-01";
const SHA = (bytes) => createHash("sha256").update(bytes).digest("hex");
const story = (model = FLASH) => ({ kind: "story", image_model: model });
const errorCode = (code) => (error) => error instanceof MediaError && error.code === code && error.who === "owner";

function status() {
  return {
    enabled: true,
    music_enabled: true,
    image: { provider: "gemini", model: PRO, configured: true },
    clip: { provider: "gemini", model: "clip-model", configured: true, seconds: 8, resolution: "1080p" },
    music: { provider: "gemini", model: "music-model", configured: true },
    models: {
      images: {
        gemini: [{ value: PRO, status: "stable", usd_per_image: 0.134 }, { value: FLASH, status: "stable", usd_per_image: 0.067 }],
        minimax: [{ value: MINI, status: "stable", usd_per_image: 0.0035 }],
      },
      clips: {},
      music: {},
    },
    max_usd_per_video: 25,
    budgets: { images: { used: 3, limit: 20, remaining: 17, unit: "images" } },
  };
}

test("no series image override leaves the status object and legacy model unchanged", () => {
  const original = status();
  for (const series of [undefined, null, {}, { kind: "story" }, story(null), story("")]) {
    assert.strictEqual(imageStatus(original, series), original);
    assert.equal(imagePrice(imageStatus(original, series)), 0.134);
  }
});

test("a story uses the catalog's Flash price without changing other media or the shared status", () => {
  const original = status();
  const before = structuredClone(original);
  const effective = imageStatus(original, story());
  assert.deepEqual(effective.image, { provider: "gemini", model: FLASH, configured: true });
  assert.equal(imagePrice(effective), 0.067);
  assert.deepEqual(effective.clip, before.clip);
  assert.deepEqual(effective.music, before.music);
  assert.deepEqual(effective.budgets, before.budgets);
  assert.equal(effective.max_usd_per_video, 25);
  assert.deepEqual(original, before, "one story must not change another video's default model");
});

test("an override prefers the selected image vendor when the same model id exists in two catalogs", () => {
  const original = status();
  original.image = { provider: "minimax", model: MINI, configured: false };
  original.models.images.minimax.push({ value: FLASH, status: "stable", usd_per_image: 0.05 });
  const effective = imageStatus(original, story());
  assert.deepEqual(effective.image, { provider: "minimax", model: FLASH, configured: false });
  assert.equal(imagePrice(effective), 0.05);
  assert.match(statusProblem(effective), /no minimax key/);
});

test("cross-vendor overrides use that vendor's reported credentials, or explicitly keep them unknown", () => {
  for (const kind of ["clip", "music"]) {
    for (const configured of [true, false]) {
      const original = status();
      original[kind] = { ...original[kind], provider: "minimax", configured };
      const effective = imageStatus(original, story(MINI));
      assert.deepEqual(effective.image, { provider: "minimax", model: MINI, configured });
      assert.equal(imagePrice(effective), 0.0035);
      if (configured) assert.equal(statusProblem(effective), null);
      else assert.match(statusProblem(effective), /no minimax key/);
    }
  }
  const unknown = imageStatus(status(), story(MINI));
  assert.equal(unknown.image.configured, null, "the global Gemini key says nothing about MiniMax");
  assert.equal(statusProblem(unknown), null, "the API can reject an unavailable vendor before calling it");
});

test("an unknown or retired series model is refused instead of silently falling back", () => {
  assert.throws(() => imageStatus(status(), story("missing-image-model")), errorCode("video_media_model_not_allowed"));
  const retired = status();
  retired.models.images.gemini.find((model) => model.value === FLASH).status = "retired";
  assert.throws(() => imageStatus(retired, story()), errorCode("video_media_model_not_allowed"));
});

test("an overridden model cannot pass the spending guard with an absent, invalid or nonpositive price", () => {
  for (const price of [undefined, null, 0, -0.1, NaN, Infinity, -Infinity, "not-a-price"]) {
    const original = status();
    original.models.images.gemini.find((model) => model.value === FLASH).usd_per_image = price;
    assert.throws(() => imageStatus(original, story()), errorCode("video_media_price_unavailable"), `price ${String(price)}`);
  }
});

test("only explicit unknown credentials bypass the local key check, not false or a missing field", () => {
  const unknown = status();
  unknown.image.configured = null;
  assert.equal(statusProblem(unknown), null);
  assert.match(statusProblem({ ...unknown, enabled: false }), /drama route is off/);
  for (const configured of [false, undefined]) {
    const unavailable = status();
    unavailable.image.configured = configured;
    assert.match(statusProblem(unavailable), /no gemini key/);
  }
  const missing = status();
  delete missing.image.configured;
  assert.match(statusProblem(missing), /no gemini key/);
  assert.match(statusProblem({ ...status(), music_enabled: false }, "music"), /music generation is off/);
});

/**
 * A stage against a fake site whose one image job is answered ready at once; `overrides` maps a
 * route ("POST images", "GET jobs/image-job-1") to a function of the request that answers (or
 * throws) in its place, and may be changed between calls.
 */
function fakeStage(effective, { actualModel = effective.image.model, actualProvider = effective.image.provider, actualPrice = imagePrice(effective), format = null, overrides = {} } = {}) {
  const workdir = tempDir("video-image-stage-");
  const bytes = Buffer.from(`synthetic image from ${actualProvider}/${actualModel}`);
  const ready = {
    id: "image-job-1", slug: "story-fixture", kind: "image", status: "ready", provider: actualProvider, model: actualModel,
    file: { sha256: SHA(bytes), size: bytes.length, content_type: "image/png" },
    usd_estimate: actualPrice, error: null, retry_after_seconds: 0,
  };
  const calls = [];
  const bodies = [];
  const fetchImpl = async (url, init = {}) => {
    const parsed = new URL(url);
    assert.equal(parsed.origin, "https://mokaair.test");
    const route = `${init.method ?? "GET"} ${parsed.pathname.replace("/api/video/media/", "")}`;
    calls.push(route);
    if (overrides[route]) return overrides[route]({ init, route });
    if (route === "POST images") {
      bodies.push(JSON.parse(init.body));
      return Response.json(ready);
    }
    if (route === "GET jobs/image-job-1") return Response.json(ready);
    if (route === `GET files/story-fixture/${SHA(bytes)}`) return new Response(bytes);
    if (route === "POST judge") return Response.json({ scores: {}, overall: 8, passed: true, problems: [], notes: "", model: "gemini-judge" });
    assert.fail(`unexpected media request: ${route}`);
  };
  const stage = new Stage({
    slug: "story-fixture", workdir, status: effective, stage: "keyframes", format,
    options: { site: "https://mokaair.test", token: "synthetic-token", fetchImpl, sleep: async () => {} },
    now: () => new Date("2026-09-29T00:00:00Z"),
  });
  const generate = (extra = {}) => stage.image({ id: "opening", purpose: "keyframe", prompt: "synthetic drawing", seed: 1, target: "keyframes/opening-1", ...extra });
  return { stage, workdir, calls, bodies, ready, generate };
}

test("a slides video draws with the slides choice only while the slides switch is on; off, it is the drama's model, size and price", () => {
  const off = status();
  off.image.usd_per_image_2k = 0.134;
  off.slides_enabled = false;
  off.slides_image = { provider: "gemini", model: FLASH, configured: true, usd_per_image_2k: 0.101 };
  // The server draws a slides video under the drama's switch with the drama's model when the
  // slides switch is off (jobs.py `slides_on`); expecting Flash here booked the first Pro
  // picture as video_media_model_changed and stopped every illustrated video after one paid picture.
  assert.equal(choiceFor(off, "image", "slides"), off.image);
  assert.equal(imageSizeFor(off, "slides"), "2K", "the drama's Pro choice sells 2K, so the still is still asked at 2K");
  assert.equal(imagePrice(off, "slides", "2K"), 0.134);
  const on = { ...off, slides_enabled: true };
  assert.equal(choiceFor(on, "image", "slides"), on.slides_image);
  assert.equal(imagePrice(on, "slides", "2K"), 0.101);
  const before = { ...off };
  delete before.slides_enabled;
  assert.equal(choiceFor(before, "image", "slides"), before.image, "a site from before the slides switch has no slides choice to draw with");
  assert.equal(choiceFor(off, "image", "drama"), off.image);
  assert.equal(choiceFor(on, "clip", "slides"), on.clip);
});

test("a 2K picture is asked for by size, keyed apart from the 1K one and priced at the choice's 2K price", async () => {
  assert.deepEqual(IMAGE_SIZES, { "1K": { width: 1920, height: 1080 }, "2K": { width: 2048, height: 1152 } });
  const effective = status();
  effective.slides_enabled = true;
  effective.slides_image = { provider: "gemini", model: FLASH, configured: true, usd_per_image_2k: 0.101 };
  assert.equal(imageSizeFor(effective, "slides"), "2K");
  assert.equal(imageSizeFor(effective), null, "the drama's choice carries no 2K price, so a drama draws at 1K");
  assert.equal(imagePrice(effective, "slides", "2K"), 0.101);
  assert.equal(imagePrice(effective, "slides"), 0.067);
  assert.equal(imagePrice(effective, null, "2K"), 0, "no 2K price, no 2K estimate");
  // A series' own image model is drawn and priced at 1K: the 2K price on the settings' choice
  // belongs to the settings' model, and asking a model that sells no 2K picture is a 422.
  const global = status();
  global.image.usd_per_image_2k = 0.134;
  assert.equal(imageSizeFor(global), "2K");
  for (const model of [MINI, FLASH]) {
    const overridden = imageStatus(global, story(model));
    assert.equal(overridden.image.model, model);
    assert.equal(overridden.image.usd_per_image_2k, null);
    assert.equal(imageSizeFor(overridden), null, `${model} as a series override draws at 1K`);
  }
  assert.equal(global.image.usd_per_image_2k, 0.134, "the shared status is not changed");
  const fake = fakeStage(effective, { actualModel: FLASH, actualPrice: 0.101, format: "slides" });
  const large = await fake.generate({ size: "2K" });
  assert.equal(large.cost_usd, 0.101);
  assert.equal(fake.bodies[0].size, "2K");
  assert.equal(readLedger(fake.workdir).totals.usd, 0.101);
  const again = await fake.generate({ size: "2K" });
  assert.equal(again.reused, true, "the same 2K request is answered from the cache");
  fake.ready.usd_estimate = 0.067;
  const small = await fake.generate();
  assert.equal(small.reused, false, "the 1K picture of the same prompt is another key");
  assert.equal(fake.bodies[1].size, undefined);
  assert.equal(fake.calls.filter((call) => call === "POST images").length, 2);
});

test("the Flash estimate permits a generation below the cap that the default Pro estimate would block", async () => {
  const limited = status();
  limited.max_usd_per_video = 0.1;
  const flash = fakeStage(imageStatus(limited, story()));
  const picture = await flash.generate();
  assert.equal(picture.model, FLASH);
  assert.equal(picture.cost_usd, 0.067);
  assert.equal(readLedger(flash.workdir).totals.usd, 0.067);
  assert.equal(readLedger(flash.workdir).entries[0].model, FLASH);
  assert.equal(flash.calls.filter((call) => call === "POST images").length, 1);
  const again = await flash.generate();
  assert.equal(again.reused, true);
  assert.equal(flash.calls.filter((call) => call === "POST images").length, 1);
  assert.equal(readLedger(flash.workdir).entries.length, 1, "a cache hit is not charged again");

  const pro = fakeStage(imageStatus(limited, null));
  await assert.rejects(pro.generate(), errorCode("video_media_cap"));
  assert.deepEqual(pro.calls, [], "the expensive default is refused before a server request");
});

test("a different server model is charged by its actual identity, held for the owner and never downloaded or cached", async () => {
  const fake = fakeStage(imageStatus(status(), story()), { actualModel: PRO, actualPrice: 0.134 });
  await assert.rejects(fake.generate(), errorCode("video_media_model_changed"));
  assert.deepEqual(fake.calls, ["POST images"]);
  assert.equal(existsSync(path.join(fake.workdir, "keyframes", "opening-1.png")), false);
  assert.deepEqual(readCache(fake.workdir).entries, {});
  const firstLedger = readLedger(fake.workdir);
  assert.equal(firstLedger.entries.length, 1);
  assert.equal(firstLedger.entries[0].provider, "gemini");
  assert.equal(firstLedger.entries[0].model, PRO);
  assert.equal(firstLedger.entries[0].job_id, fake.ready.id);
  assert.equal(firstLedger.totals.usd, 0.134);
  assert.deepEqual(Object.values(readJobs(fake.workdir).jobs).map((job) => job.job_id), [fake.ready.id]);

  await assert.rejects(fake.generate(), errorCode("video_media_model_changed"));
  assert.deepEqual(fake.calls, ["POST images", "GET jobs/image-job-1"], "a retry polls the paid-for job instead of submitting another generation");
  assert.equal(readLedger(fake.workdir).entries.length, 1, "seeing the same mismatched job twice must not charge it twice");
  assert.equal(readLedger(fake.workdir).totals.usd, 0.134);
  assert.deepEqual(readCache(fake.workdir).entries, {});
  assert.equal(Object.values(readJobs(fake.workdir).jobs)[0].job_id, fake.ready.id);
});

test("a different server provider is not mislabeled as the requested image provider", async () => {
  const fake = fakeStage(imageStatus(status(), story()), { actualProvider: "minimax", actualModel: MINI, actualPrice: 0.0035 });
  await assert.rejects(fake.generate(), errorCode("video_media_model_changed"));
  assert.deepEqual(fake.calls, ["POST images"]);
  const ledger = readLedger(fake.workdir);
  assert.equal(ledger.entries[0].provider, "minimax");
  assert.equal(ledger.entries[0].model, MINI);
  assert.equal(ledger.totals.usd, 0.0035);
  assert.deepEqual(readCache(fake.workdir).entries, {});
});

test("reconciling the series model does not charge a previously recorded server job again", async () => {
  const fake = fakeStage(imageStatus(status(), story()), { actualModel: PRO, actualPrice: 0.134 });
  await assert.rejects(fake.generate(), errorCode("video_media_model_changed"));
  // Once the owner corrects series.json, its model produces a different local cache key.
  // The same server-side request hash still returns the already-paid-for job.
  fake.stage.status = imageStatus(status(), story(PRO));
  const picture = await fake.generate();
  assert.equal(picture.job_id, fake.ready.id);
  assert.equal(picture.model, PRO);
  assert.equal(fake.calls.filter((call) => call === "POST images").length, 2);
  assert.equal(readLedger(fake.workdir).entries.length, 1, "reusing a server job is not a second purchase");
  assert.equal(readLedger(fake.workdir).totals.usd, 0.134);
  assert.equal(readLedger(fake.workdir).entries[0].model, PRO);
  assert.deepEqual(readJobs(fake.workdir).jobs, {}, "accepting the job clears its pending aliases under the former model too");
});

test("a failed server job retried under the same id updates its zero charge when the retry succeeds", async () => {
  const fake = fakeStage(imageStatus(status(), story()));
  const completedFile = fake.ready.file;
  Object.assign(fake.ready, {
    status: "failed", attempts: 1, file: null, usd_estimate: 0,
    error: { code: "video_media_upstream_failed", detail: "the first attempt failed before producing an image" },
  });
  await assert.rejects(fake.generate(), (error) => error instanceof MediaError && error.code === "video_media_upstream_failed");
  assert.equal(readLedger(fake.workdir).entries.length, 1);
  assert.equal(readLedger(fake.workdir).entries[0].job_id, fake.ready.id);
  assert.equal(readLedger(fake.workdir).totals.usd, 0);
  assert.deepEqual(readJobs(fake.workdir).jobs, {});

  // The API retries the existing row (attempts += 1); it does not allocate a new job id.
  // This positive ready price proves the worker contract. The API's restoration
  // is independently covered by test_video_media_jobs.py, not by this fake response.
  Object.assign(fake.ready, { status: "ready", attempts: 2, file: completedFile, usd_estimate: 0.067, error: null });
  const picture = await fake.generate();
  assert.equal(picture.job_id, fake.ready.id);
  assert.equal(fake.calls.filter((call) => call === "POST images").length, 2);
  const ledger = readLedger(fake.workdir);
  assert.equal(ledger.entries.length, 1, "the retry updates the existing job's entry instead of duplicating it");
  assert.equal(ledger.entries[0].cost_usd, 0.067, "the successful retry replaces the initial zero charge");
  assert.equal(ledger.entries[0].status, "ready");
  assert.equal(ledger.entries[0].provider, "gemini");
  assert.equal(ledger.entries[0].model, FLASH);
  assert.equal(ledger.totals.usd, 0.067, "totals must be recomputed after replacing the failed entry");
  const cached = await fake.generate();
  assert.equal(cached.reused, true);
  assert.equal(readLedger(fake.workdir).entries.length, 1);
  assert.equal(readLedger(fake.workdir).totals.usd, 0.067);
});

test("a generation holds its list price in the ledger before it is submitted, and the server's charge replaces the hold", async () => {
  const effective = imageStatus(status(), story());
  let heldAtSubmit = null;
  const fake = fakeStage(effective, {
    overrides: {
      "POST images": ({ init }) => {
        heldAtSubmit = readLedger(fake.workdir).entries;
        fake.bodies.push(JSON.parse(init.body));
        return Response.json(fake.ready);
      },
    },
  });
  const picture = await fake.generate();
  assert.equal(heldAtSubmit.length, 1, "one row was written before the request went out");
  const [hold] = heldAtSubmit;
  assert.deepEqual([hold.status, hold.kind, hold.id, hold.stage, hold.provider, hold.model, hold.cost_usd, hold.key, hold.job_id], ["reserved", "image", "opening", "keyframes", "gemini", FLASH, 0.067, picture.key, undefined]);
  const ledger = readLedger(fake.workdir);
  assert.deepEqual(ledger.entries.map((entry) => [entry.status, entry.job_id, entry.key, entry.cost_usd]), [["ready", "image-job-1", picture.key, 0.067]], "the job's row took the hold's place");
  assert.deepEqual([ledger.totals.usd, ledger.totals.reserved, ledger.totals.reservations], [0.067, 0, 0]);
  const again = await fake.generate();
  assert.equal(again.reused, true);
  assert.equal(readLedger(fake.workdir).entries.length, 1, "a cache hit holds nothing");
});

test("a refusal from the server releases the hold; a lost connection keeps it until a rerun books the job it may have left", async () => {
  const effective = imageStatus(status(), story());
  const overrides = { "POST images": () => Response.json({ code: "video_media_budget_exhausted", detail: "the month's images are spent" }, { status: 429 }) };
  const fake = fakeStage(effective, { overrides });
  await assert.rejects(fake.generate(), errorCode("video_media_budget_exhausted"));
  assert.deepEqual(readLedger(fake.workdir).entries, [], "the server answered and took nothing: nothing is held");
  assert.deepEqual(readJobs(fake.workdir).jobs, {});
  overrides["POST images"] = () => {
    throw new TypeError("fetch failed");
  };
  await assert.rejects(fake.generate(), (error) => error instanceof MediaError && error.code === "network");
  const held = reservedEntries(readLedger(fake.workdir).entries);
  assert.equal(held.length, 1, "the server may have taken the request: the hold stays");
  assert.equal(held[0].cost_usd, 0.067);
  assert.deepEqual(readJobs(fake.workdir).jobs, {}, "no job id came back");
  delete overrides["POST images"];
  const picture = await fake.generate();
  assert.equal(picture.reused, false);
  const ledger = readLedger(fake.workdir);
  assert.deepEqual(ledger.entries.map((entry) => [entry.status, entry.job_id, entry.cost_usd]), [["ready", "image-job-1", 0.067]], "the rerun held the same key once and the job's row replaced it");
  assert.equal(ledger.totals.reserved, 0);
});

test("a run that stops between submit and reconcile leaves a visible reserved row, counted by the cap and media-status, that the next run books", async () => {
  const effective = imageStatus(status(), story());
  effective.max_usd_per_video = 0.1;
  const overrides = {};
  const fake = fakeStage(effective, { overrides });
  overrides["POST images"] = () => Response.json({ ...fake.ready, status: "queued", file: null }, { status: 202 });
  overrides["GET jobs/image-job-1"] = () => {
    // The STOP file arrives while the job runs on the server.
    writeFileSync(path.join(fake.workdir, "STOP"), "");
    return Response.json({ ...fake.ready, status: "submitted", file: null });
  };
  await assert.rejects(fake.generate(), (error) => error instanceof MediaError && error.code === "stopped");
  const key = fake.stage.imageKey({ prompt: "synthetic drawing", seed: 1 });
  const ledger = readLedger(fake.workdir);
  assert.deepEqual(ledger.entries.map((entry) => [entry.status, entry.key, entry.cost_usd, entry.id]), [["reserved", key, 0.067, "opening"]]);
  assert.deepEqual(Object.values(readJobs(fake.workdir).jobs).map((job) => job.job_id), ["image-job-1"], "the pending job sits beside the hold");
  assert.deepEqual([ledger.totals.usd, ledger.totals.reserved, ledger.totals.reservations], [0.067, 0.067, 1]);
  // The hold is money: the cap counts it, and media-status prints it as this video's spend.
  assert.match(capProblem(fake.workdir, 0.067, 0.1), /spent US\$0\.07 \(US\$0\.07 of it reserved for 1 request not yet reconciled\) and the next generation costs about US\$0\.07, past the per-video cap of US\$0\.1/);
  assert.match(statusText({ ...effective, budgets: {}, store: { used_bytes: 0, max_total_bytes: 1e9, writable: true } }, ledgerTotals(fake.workdir)), /this video: US\$0\.07 \(1 images, 0 clip seconds, 0 tracks, 0 judge calls\)/);
  // The next run picks the job up by its key and books what it cost: one row, nothing held.
  rmSync(path.join(fake.workdir, "STOP"));
  overrides["GET jobs/image-job-1"] = () => Response.json(fake.ready);
  const picture = await fake.generate();
  assert.equal(picture.job_id, "image-job-1");
  assert.equal(fake.calls.filter((call) => call === "POST images").length, 1, "the pending job is polled, not submitted again");
  const after = readLedger(fake.workdir);
  assert.deepEqual(after.entries.map((entry) => [entry.status, entry.job_id, entry.cost_usd]), [["ready", "image-job-1", 0.067]]);
  assert.deepEqual([after.totals.reserved, after.totals.reservations], [0, 0]);
  assert.deepEqual(readJobs(fake.workdir).jobs, {});
  assert.equal(capProblem(fake.workdir, 0.03, 0.1), null);
});

test("a judge call is money: it is refused past the per-video cap before the server is asked, and booked once it answers", async () => {
  const effective = imageStatus(status(), story());
  effective.max_usd_per_video = 0.07;
  const fake = fakeStage(effective);
  const picture = await fake.generate();
  assert.equal(readLedger(fake.workdir).totals.usd, 0.067);
  const ask = () => fake.stage.judge({ id: "opening", kind: "keyframe", files: [{ sha256: picture.sha256, label: "keyframe" }], rubric: [{ key: "clean", question: "Is it clean?", weight: 1 }] });
  await assert.rejects(ask(), (error) => errorCode("video_media_cap")(error) && /the next judge call costs about US\$0\.01, past the per-video cap of US\$0\.07/.test(error.message));
  assert.equal(fake.calls.filter((call) => call === "POST judge").length, 0, "refused before the server is asked");
  assert.equal(readLedger(fake.workdir).totals.judge_calls, 0);
  fake.stage.status = { ...effective, max_usd_per_video: 0.08 };
  const verdict = await ask();
  assert.equal(verdict.passed, true);
  assert.equal(fake.calls.filter((call) => call === "POST judge").length, 1);
  const ledger = readLedger(fake.workdir);
  assert.deepEqual([ledger.totals.judge_calls, ledger.totals.usd, ledger.totals.reserved], [1, 0.077, 0]);
  assert.equal(ledger.entries.at(-1).cost_usd, JUDGE_USD_PER_CALL);
  assert.equal(JUDGE_USD_PER_CALL, 0.01, "mirrors JUDGE_USD_PER_CALL in apps/api/app/video_media/catalog.py");
});

test("an image model takes a style reference when the catalog says so; a server from before the field forwards one through Gemini alone", () => {
  const on = status();
  on.slides_enabled = true;
  on.slides_image = { provider: "minimax", model: "image-01", configured: true };
  on.models.images.minimax = [{ value: "image-01", label: "MiniMax image-01", description: null, status: "stable", resolutions: [], durations: [], reference_images: 1, style_references: 0, native_audio: false, usd_per_second: null, usd_per_image: 0.0035, usd_per_track: null }];
  on.models.images.gemini = on.models.images.gemini.map((entry) => ({ ...entry, style_references: 1 }));
  assert.equal(takesStyleReference(on, "slides"), false, "image-01 is sent a character reference alone");
  assert.equal(takesStyleReference(on, "drama"), true, "the drama's Pro choice reads a plate");
  assert.equal(takesStyleReference(on), true);
  const flashWithout = { ...on, slides_image: { provider: "gemini", model: FLASH, configured: true }, models: { ...on.models, images: { ...on.models.images, gemini: on.models.images.gemini.map((entry) => (entry.value === FLASH ? { ...entry, style_references: 0 } : entry)) } } };
  assert.equal(takesStyleReference(flashWithout, "slides"), false, "the catalog's word, not the vendor's name");
  // A server from before the field says nothing: the vendor decides, as the adapters did.
  const before = status();
  before.slides_enabled = true;
  before.slides_image = { provider: "minimax", model: "image-01", configured: true };
  assert.equal(takesStyleReference(before, "slides"), false);
  assert.equal(takesStyleReference(before, "drama"), true);
  assert.equal(takesStyleReference({ ...before, image: { provider: "minimax", model: "image-01", configured: true } }, "drama"), false);
});
