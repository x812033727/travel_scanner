import { test } from "node:test";
import assert from "node:assert/strict";
import { mkdtempSync, rmSync, writeFileSync } from "node:fs";
import os from "node:os";
import path from "node:path";
import { chromium } from "playwright";
import { Studio, readSelectors } from "../src/studio.mjs";

// Synthetic DOM contract, not a representation or acceptance test of live Studio.
// Every request is intercepted. No Google account, cookies or real upload is used.
const CHANNEL = "UC" + "a".repeat(22);
const ID = "abcdefghijk";
test("browser adapter checks channel/privacy, replaces fields and confirms saved text", async (t) => {
  const directory = mkdtempSync(path.join(os.tmpdir(), "studio-contract-"));
  const studio = new Studio({ store: {}, profile: directory, chromium, headless: true,
    selectors: { title: "#title", description: "#description", tags: "#tags",
      language: "#language", category: "#category", syntheticGroup: "#synthetic", visibility: "#visibility" } });
  t.after(async () => {
    await studio.close();
    assert.ok(path.resolve(directory).startsWith(path.resolve(os.tmpdir(), "studio-contract-")));
    rmSync(directory, { recursive: true });
  });
  await studio.connect();
  let title = "Old title"; let description = "Old description"; let privacy = "Private";
  let channel = CHANNEL;
  await studio.context.route("**/*", async (route) => {
    assert.equal(new URL(route.request().url()).hostname, "studio.youtube.com");
    await route.fulfill({ contentType: "text/html", body: `
      <a href="/channel/${channel}/videos">Content</a>
      <div id="title" contenteditable="true"></div><div id="description" contenteditable="true" style="white-space:pre-wrap"></div>
      <div id="visibility">${privacy}</div>
      <label><input name="audience" type="radio">No, it's not made for kids</label>
      <label><input name="audience" type="radio">Yes, it's made for kids</label>
      <div id="synthetic"><fieldset><legend>Altered content</legend>
        <label><input name="altered" type="radio">No</label>
        <label><input name="altered" type="radio">Yes</label>
      </fieldset></div>
      <div id="tags-container"><ytcp-chip><button id="delete-button" onclick="this.parentElement.remove()">Remove old tag</button></ytcp-chip><input id="tags"></div>
      <select id="language"><option>English</option><option>Chinese (Taiwan)</option></select>
      <select id="category"><option>Science &amp; Technology</option></select>
      <button onclick="this.disabled=true">Save</button>
      <script>
        document.getElementById('title').textContent = ${JSON.stringify(title)};
        document.getElementById('description').textContent = ${JSON.stringify(description)};
      </script>` });
  });
  const metadata = { title: "New title", description: "Full text\n00:00 Introduction", tags: [],
    default_language: "zh-TW", category_id: "28", made_for_kids: false, contains_synthetic_media: false };
  await studio.channel(CHANNEL);
  await studio.openPrivate(ID);
  await studio.details(metadata);
  assert.equal(await studio.page.locator("#title").innerText(), metadata.title);
  assert.equal(await studio.page.locator("ytcp-chip").count(), 0, "empty tags clear prior tags too");
  assert.equal(await studio.page.locator('#synthetic input').first().isChecked(), true);
  await studio.saved();
  assert.equal(await studio.button("Save").isDisabled(), true);
  title = metadata.title; description = metadata.description;
  await studio.step("verify", { video_id: ID, manifest: { metadata } });
  description = "Old description survived";
  await assert.rejects(studio.step("verify", { video_id: ID, manifest: { metadata } }), { code: "save_unconfirmed" });
  privacy = "Public";
  await assert.rejects(studio.openPrivate(ID), { code: "private_required" });
  privacy = "Private"; channel = "UC" + "b".repeat(22);
  studio.page.setDefaultTimeout(100);
  studio.page.setDefaultNavigationTimeout(15_000);
  await assert.rejects(studio.openPrivate(ID), { code: "channel_unconfirmed" });
  studio.page.setDefaultTimeout(15_000);
  channel = CHANNEL;
  await studio.openPrivate(ID);
  await studio.page.evaluate(() => { document.body.append(document.getElementById("title").cloneNode(true)); });
  await assert.rejects(studio.fill(studio.control("title"), "do not pick the first"), { code: "studio_changed" });
  await studio.page.evaluate(() => { const i = document.createElement("iframe"); i.src = "https://studio.youtube.com/challenge"; document.body.append(i); });
  await assert.rejects(studio.guard(), { code: "verification_required" });
  await studio.context.unrouteAll({ behavior: "wait" });
  await studio.context.route("**/*", (route) => route.fulfill({ body: "<h1>Sign in</h1>" }));
  await studio.page.goto("https://accounts.google.com/", { waitUntil: "commit" });
  await assert.rejects(studio.guard(), { code: "login_required" });
});

test("operator selector overrides are limited to documented fields", (t) => {
  const directory = mkdtempSync(path.join(os.tmpdir(), "studio-selectors-"));
  t.after(() => {
    assert.ok(path.resolve(directory).startsWith(path.resolve(os.tmpdir(), "studio-selectors-")));
    rmSync(directory, { recursive: true });
  });
  const file = path.join(directory, "selectors.json");
  writeFileSync(file, JSON.stringify({ title: "#confirmed-title" }));
  assert.deepEqual(readSelectors(file), { title: "#confirmed-title" });
  writeFileSync(file, JSON.stringify({ unknown: "anything" }));
  assert.throws(() => readSelectors(file));
});
