import { test } from "node:test";
import assert from "node:assert/strict";
import { existsSync, mkdtempSync, rmSync } from "node:fs";
import os from "node:os";
import path from "node:path";
import { chromium } from "playwright";
import { Store } from "../src/store.mjs";
import { Refused, dubLocale, hash, jobSteps, validateManifest } from "../src/contract.mjs";
import { Runner } from "../src/runner.mjs";
import { Studio } from "../src/studio.mjs";

// Synthetic DOM contract for the dub (audio track) step, not a representation or acceptance
// test of live Studio. Every request is intercepted. No Google account or real upload is used.
const CHANNEL = "UC" + "a".repeat(22);
const ID = "abcdefghijk";
const SECOND = "lmnopqrstuv";
const EN = Buffer.from("fixture-english-dub");
const JA = Buffer.from("fixture-japanese-dub");
const NAMES = { en: "English", ja: "Japanese", ko: "Korean" };

function manifest(overrides = {}) {
  return validateManifest({
    version: 1, slug: "dubbed-video", review_sha256: hash("approved"), channel_id: CHANNEL, video_id: ID,
    metadata: { title: "Title", description: "Description", tags: [], default_language: "zh-TW", category_id: "28",
      made_for_kids: false, contains_synthetic_media: true, localizations: {} },
    files: [{ role: "dub_en", sha256: hash(EN), size: EN.length, content_type: "audio/mp4" }],
    ...overrides,
  }, CHANNEL);
}

/** One video's language page, kept on this side so a reload shows what was published. */
function translations(video, state) {
  const row = (locale) => {
    const dub = state.dubs[video + locale];
    const cell = state.changed ? "" : `<div id="audio">${state.auto === locale ? "Auto-dubbed" : state.draft === locale
      ? 'Draft <button>Edit</button>' : dub ? "Published" : '<button data-add>Add</button>'}</div>`;
    return `<ytcp-video-translation-row data-locale="${locale}"><span>${NAMES[locale]}</span><div id="captions"></div><div id="metadata"></div>${cell}</ytcp-video-translation-row>`;
  };
  return `<a href="/channel/${CHANNEL}/videos">Content</a>
    <button id="add-language">Add language</button>
    <div id="choices" hidden>${Object.entries(NAMES).map(([locale, name]) => `<div role="option" data-locale="${locale}">${name}</div>`).join("")}</div>
    <div id="rows">${state.rows.map(row).join("")}</div>
    <div role="dialog" hidden><button>Select file</button><input type="file" accept="audio/*,.m4a,.mp3,.wav"><button id="publish" disabled>Publish</button></div>
    <script>
      const dialog = document.querySelector('[role="dialog"]'); const input = dialog.querySelector("input");
      const publish = document.getElementById("publish"); let cell = null;
      const template = ${JSON.stringify(row("LOCALE"))};
      document.getElementById("add-language").onclick = () => { document.getElementById("choices").hidden = false; };
      document.getElementById("choices").onclick = (event) => {
        const locale = event.target.dataset.locale; if (!locale) return;
        document.getElementById("rows").insertAdjacentHTML("beforeend",
          template.replaceAll("LOCALE", locale).replace("undefined", event.target.textContent));
        document.getElementById("choices").hidden = true;
      };
      document.getElementById("rows").onclick = (event) => {
        if (!event.target.matches("[data-add]")) return;
        cell = event.target.parentElement; input.value = ""; publish.disabled = true; dialog.hidden = false;
      };
      // Studio takes a moment with the file before Publish can be pressed.
      input.onchange = () => setTimeout(() => { publish.disabled = false; }, 700);
      publish.onclick = async () => {
        const file = input.files[0]; const locale = cell.parentElement.dataset.locale;
        await fetch("/synthetic/dub?locale=" + locale + "&name=" + encodeURIComponent(file.name) + "&size=" + file.size, { method: "POST" });
        ${state.unconfirmed ? "" : 'cell.textContent = "Published";'} dialog.hidden = true;
      };
    </script>`;
}

async function fixture(t) {
  const directory = mkdtempSync(path.join(os.tmpdir(), "studio-dub-"));
  const store = new Store(path.join(directory, "jobs"));
  const studio = new Studio({ store, profile: path.join(directory, "browser"), chromium, headless: true,
    selectors: { title: "#title", description: "#description", visibility: "#visibility" } });
  t.after(async () => {
    await studio.close(); store.close();
    assert.ok(path.resolve(directory).startsWith(path.resolve(os.tmpdir(), "studio-dub-")));
    rmSync(directory, { recursive: true });
  });
  const state = { rows: ["en"], dubs: {}, posts: [], privacy: "Private", changed: false, auto: null, draft: null, unconfirmed: false };
  await studio.connect();
  await studio.context.route("**/*", async (route) => {
    const url = new URL(route.request().url());
    assert.equal(url.hostname, "studio.youtube.com");
    const video = /^\/video\/([A-Za-z0-9_-]{11})\/(edit|translations)$/.exec(url.pathname);
    if (url.pathname === "/synthetic/dub") {
      assert.equal(route.request().method(), "POST");
      const video = new URL(route.request().headers().referer).pathname.split("/")[2];
      state.posts.push({ video, locale: url.searchParams.get("locale"), name: url.searchParams.get("name"), size: Number(url.searchParams.get("size")) });
      state.dubs[video + url.searchParams.get("locale")] = true;
      if (!state.rows.includes(url.searchParams.get("locale"))) state.rows.push(url.searchParams.get("locale"));
      return route.fulfill({ contentType: "application/json", body: "{}" });
    }
    if (video?.[2] === "translations") return route.fulfill({ contentType: "text/html", body: translations(video[1], state) });
    return route.fulfill({ contentType: "text/html", body: `<a href="/channel/${CHANNEL}/videos">Content</a>
      <div id="title" contenteditable="true">Title</div><div id="description" contenteditable="true">Description</div>
      <div id="visibility">${state.privacy}</div>` });
  });
  // A missing control should pause quickly here; navigation keeps its normal allowance.
  studio.page.setDefaultTimeout(1500);
  studio.page.setDefaultNavigationTimeout(15_000);
  return { store, studio, state, runner: new Runner(store, studio) };
}
/** A queued job with everything before its language steps already recorded. */
async function queued(store, m, bytes = { [hash(EN)]: EN }) {
  const id = hash(m.slug + m.review_sha256);
  store.create(id, m);
  for (const [sha, body] of Object.entries(bytes)) await store.put(id, sha, 0, body);
  await store.queue(id);
  store.patch(id, { completed: ["details"] });
  return id;
}

test("dub roles are validated, sized and ordered after the captions and translations", () => {
  assert.equal(dubLocale("dub_en"), "en");
  assert.equal(dubLocale("dub_zh_cn"), "zh-CN");
  for (const role of ["dub_zh-CN", "dub_fr", "dub_", "captions_en", "dub_../browser"]) assert.equal(dubLocale(role), null);
  const dub = { role: "dub_en", sha256: hash(EN), size: EN.length, content_type: "audio/mp4" };
  const m = manifest({ metadata: { ...manifest().metadata, localizations: { en: { title: "English", description: "Text" } } },
    files: [dub, { role: "captions_en", sha256: hash("srt"), size: 3, content_type: "text/plain" },
      { role: "dub_ja", sha256: hash(JA), size: 30 * 1024 ** 2, content_type: "audio/x-wav" }] });
  assert.deepEqual(jobSteps(m), ["video", "details", "captions_en", "localization_en", "dub_en", "dub_ja", "verify"]);
  for (const files of [
    [{ ...dub, content_type: "video/mp4" }], [{ ...dub, content_type: "audio/flac" }], [{ ...dub, role: "dub_fr" }],
    [{ ...dub, role: "dub_zh_tw" }], // the narration's own language is the original audio
    [{ ...dub, size: 1024 ** 3 + 1 }], [dub, { ...dub, sha256: hash(JA) }],
  ]) assert.throws(() => manifest({ files }), Refused);
});

test("the dub step adds the track once, skips a published one and adds a missing language", async (t) => {
  const { store, studio, state, runner } = await fixture(t);
  const id = await queued(store, manifest());
  await runner.tick();
  let job = store.get(id);
  assert.equal(job.state, "done");
  assert.deepEqual(state.posts, [{ video: ID, locale: "en", name: "dub_en.m4a", size: EN.length }]);
  assert.ok(existsSync(path.join(store.directory, id, "dub_en.m4a")));
  assert.deepEqual(store.view(job).dubs, [{ locale: "en", sha256: hash(EN), state: "placed" }]);
  assert.deepEqual(store.view(job).steps.map((s) => s.id + ":" + s.done), ["video:true", "details:true", "dub_en:true", "verify:true"]);

  // A newer approved package for the same video: the published English track is left alone,
  // and Japanese, which has no row yet, is added through "Add language".
  const next = manifest({ review_sha256: hash("newer approval"), files: [
    { role: "dub_en", sha256: hash(EN), size: EN.length, content_type: "audio/mp4" },
    { role: "dub_ja", sha256: hash(JA), size: JA.length, content_type: "audio/mpeg" }] });
  const second = await queued(store, next, { [hash(EN)]: EN, [hash(JA)]: JA });
  await runner.tick();
  job = store.get(second);
  assert.equal(job.state, "done");
  assert.deepEqual(state.posts.slice(1), [{ video: ID, locale: "ja", name: "dub_ja.mp3", size: JA.length }]);
  assert.deepEqual(store.view(job).dubs, [
    { locale: "en", sha256: hash(EN), state: "present" }, { locale: "ja", sha256: hash(JA), state: "placed" }]);
  assert.deepEqual(await studio.step("dub_ja", job), { dub: "present" });
  assert.equal(state.posts.length, 2);
});

test("an unexpected language page pauses the job without sending the file", async (t) => {
  const { store, state, runner } = await fixture(t);
  const id = await queued(store, manifest());
  const paused = async (code) => {
    await runner.tick();
    const job = store.get(id);
    assert.deepEqual([job.state, job.code, job.current_step], ["needs_action", code, "dub_en"]);
    assert.ok(!job.completed.includes("dub_en"));
    assert.deepEqual(store.view(job).dubs, [{ locale: "en", sha256: hash(EN), state: "pending" }]);
    store.resume(id);
  };
  state.changed = true; // the row has no dub cell any more
  await paused("studio_changed");
  state.changed = false; state.draft = "en"; // a draft offers Edit, not Add: never a blind second file
  await paused("studio_changed");
  state.draft = null; state.auto = "en"; // an automatic dub has to be deleted by the owner first
  await paused("dub_needs_review");
  state.auto = null; state.privacy = "Public";
  await paused("private_required");
  assert.deepEqual(state.posts, []);
  state.privacy = "Private"; state.unconfirmed = true; // Publish pressed, the row never says so
  await paused("save_unconfirmed");
  assert.equal(state.posts.length, 1);
  state.unconfirmed = false;
  // The owner looked: Studio does hold the track. Resuming reads the row, it sends nothing.
  await runner.tick();
  assert.equal(store.get(id).state, "done");
  assert.equal(state.posts.length, 1);
  assert.deepEqual(store.view(store.get(id)).dubs, [{ locale: "en", sha256: hash(EN), state: "present" }]);
});

test("a run interrupted after Publish resumes without a second upload", async (t) => {
  const { store, studio, state } = await fixture(t);
  const id = await queued(store, manifest({ slug: "second-video", video_id: SECOND }));
  let crash = true;
  // The service dies between Studio's confirmation and the durable checkpoint.
  const dying = new Proxy(studio, { get: (target, name) => name !== "step" ? Reflect.get(target, name).bind?.(target) ?? Reflect.get(target, name)
    : async (step, job) => { const result = await target.step(step, job); if (crash && step === "dub_en") throw new Error("killed"); return result; } });
  const runner = new Runner(store, dying);
  await runner.tick();
  let job = store.get(id);
  assert.deepEqual([job.state, job.current_step, job.completed.includes("dub_en")], ["needs_action", "dub_en", false]);
  assert.equal(state.posts.length, 1);
  crash = false;
  store.resume(id);
  await runner.tick();
  job = store.get(id);
  assert.equal(job.state, "done");
  assert.deepEqual(state.posts, [{ video: SECOND, locale: "en", name: "dub_en.m4a", size: EN.length }]);
  assert.deepEqual(store.view(job).dubs, [{ locale: "en", sha256: hash(EN), state: "present" }]);
});
