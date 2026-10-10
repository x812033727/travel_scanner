// Offline UI contract checks. Media decoding is mocked; validate MP4s with ffprobe/ffmpeg.
// Usage: node check-player.mjs index.html [--expect-episodes 48] [--expect-seasons 4] [--expect-per-season 12]
import fs from "node:fs";
import path from "node:path";
import { pathToFileURL } from "node:url";
import assert from "node:assert/strict";
import { JSDOM, VirtualConsole } from "jsdom";

const [file, ...arguments_] = process.argv.slice(2);
if (!file) throw new Error("Pass the generated index.html path");
const expected = {};
const accepted = new Set(["--expect-episodes", "--expect-seasons", "--expect-per-season"]);
for (let index = 0; index < arguments_.length; index += 2) {
  const flag = arguments_[index], value = Number(arguments_[index + 1]);
  if (!accepted.has(flag) || !Number.isInteger(value) || value < 1) {
    throw new Error(`Invalid expectation: ${flag}; use a positive integer`);
  }
  expected[flag] = value;
}
const errors = [];
const virtualConsole = new VirtualConsole();
virtualConsole.on("jsdomError", (error) => errors.push(error.message));
const dom = new JSDOM(fs.readFileSync(file, "utf8"), {
  url: pathToFileURL(path.resolve(file)).href,
  runScripts: "dangerously", pretendToBeVisual: true, virtualConsole,
  beforeParse(window) {
    const states = new WeakMap();
    const state = (element) => {
      if (!states.has(element)) states.set(element, { paused: true, time: 0 });
      return states.get(element);
    };
    const prototype = window.HTMLMediaElement.prototype;
    for (const [key, getter] of Object.entries({
      paused() { return state(this).paused; },
      duration() {
        const id = this.src.match(/\/(ep\d+)\//)?.[1];
        const data = JSON.parse(window.document.getElementById("episode-data")?.textContent || "[]");
        return data.find((episode) => episode.id === id)?.duration || 180;
      },
      readyState() { return 4; }, ended() { return false; }, seeking() { return false; },
    })) Object.defineProperty(prototype, key, { configurable: true, get: getter });
    Object.defineProperty(prototype, "currentTime", {
      configurable: true, get() { return state(this).time; }, set(value) { state(this).time = value; },
    });
    prototype.load = function () {
      state(this).time = 0;
      queueMicrotask(() => this.dispatchEvent(new window.Event("loadedmetadata")));
    };
    prototype.play = function () {
      state(this).paused = false;
      this.dispatchEvent(new window.Event("playing"));
      return Promise.resolve();
    };
    prototype.pause = function () {
      if (!state(this).paused) {
        state(this).paused = true;
        this.dispatchEvent(new window.Event("pause"));
      }
    };
  },
});
const settle = () => new Promise((resolve) => setTimeout(resolve, 10));
try {
  await settle();
  const { window } = dom;
  const document = window.document;
  const $ = (selector) => document.querySelector(selector);
  const event = (type) => new window.Event(type, { bubbles: true });
  const episodes = JSON.parse($("#episode-data").textContent);
  assert.ok(episodes.length > 0, "the embedded catalog is nonempty");
  assert.equal(new Set(episodes.map((episode) => episode.id)).size, episodes.length, "episode IDs are unique");
  if (expected["--expect-episodes"]) assert.equal(episodes.length, expected["--expect-episodes"]);
  assert.equal(document.querySelectorAll(".episode-card").length, episodes.length);
  assert.equal($("#episode-count").textContent, `共 ${episodes.length} 集`);
  const seasons = [...new Set(episodes.map((episode) => String(episode.season)))];
  const seasonCounts = Object.fromEntries(seasons.map((season) => [season, episodes.filter((episode) => String(episode.season) === season).length]));
  assert.deepEqual(Array.from($("#season").options, (option) => option.value), seasons);
  if (expected["--expect-seasons"]) assert.equal(seasons.length, expected["--expect-seasons"]);
  if (expected["--expect-per-season"]) {
    for (const count of Object.values(seasonCounts)) assert.equal(count, expected["--expect-per-season"]);
  }
  const visibleIds = () => Array.from(document.querySelectorAll(".episode-card:not([hidden])"), (card) => card.dataset.id);
  const assertSeasonCards = (season) => {
    assert.deepEqual(visibleIds(), episodes.filter((episode) => String(episode.season) === season).map((episode) => episode.id));
  };
  const assertCurrent = (episode, locale) => {
    assert.ok($("#video").src.endsWith(`/${episode.id}/final.mp4`), "picture follows selected episode");
    assert.ok($("#audio").src.endsWith(`/${episode.id}/audio/${locale}.m4a`), "audio follows selected episode and locale");
    assert.equal($("#episode-title").textContent, episode.title);
    assert.equal($("#goal").textContent, episode.goal);
    assert.equal($("#parent-tip").textContent, episode.parentTip);
    assert.ok($("#download").href.endsWith(`/${episode.id}/final.mp4`));
    assert.deepEqual(Array.from(document.querySelectorAll('.episode-card[aria-current="true"]'), (card) => card.dataset.id), [episode.id]);
    assert.ok(visibleIds().includes(episode.id), "selected episode is visible in its season");
  };
  assertSeasonCards(seasons[0]);
  assert.deepEqual(Array.from($("#voice").options, (option) => option.value), ["zh-TW", "zh-CN", "ja", "ko", "en"]);
  assert.deepEqual(Array.from($("#cc").options, (option) => option.value), ["zh-TW", "zh-CN", "ja", "ko", "off"]);
  assert.equal($("#voice").value, "zh-TW");
  assert.equal($("#cc").value, "zh-TW");
  assert.equal(document.querySelectorAll('#cc option[value="en"]').length, 0);
  const first = episodes[0];
  assertCurrent(first, "zh-TW");
  for (const episode of episodes) {
    for (const locale of ["zh-TW", "zh-CN", "ja", "ko"]) {
      assert.ok(episode.captions[locale]?.length > 0, `${episode.id} has embedded ${locale} captions`);
    }
  }
  const cueAt = (episode, locale, time) => episode.captions[locale].find((cue) => time >= cue.start && time < cue.end)?.text || "";
  const firstCue = first.captions["zh-TW"][0];
  const captionTime = (firstCue.start + firstCue.end) / 2;
  $("#video").currentTime = captionTime;
  $("#video").dispatchEvent(event("timeupdate"));
  assert.equal($("#caption-text").textContent, firstCue.text);
  assert.equal($("#caption-text").classList.contains("visible"), true);
  const pictureSource = $("#video").src;
  $("#voice").value = "ja";
  $("#voice").dispatchEvent(event("change"));
  await settle();
  assertCurrent(first, "ja");
  assert.equal($("#video").src, pictureSource);
  assert.equal($("#video").currentTime, captionTime);
  assert.equal($("#audio").currentTime, captionTime);
  assert.equal($("#cc").value, "zh-TW", "voice changes do not change CC selection");
  assert.equal($("#caption-text").textContent, firstCue.text);
  const audioSource = $("#audio").src;
  $("#cc").value = "ko";
  $("#cc").dispatchEvent(event("change"));
  assert.equal($("#caption-text").textContent, cueAt(first, "ko", captionTime));
  assert.equal($("#voice").value, "ja");
  assert.equal($("#audio").src, audioSource, "CC changes do not reload audio");
  $("#cc").value = "off";
  $("#cc").dispatchEvent(event("change"));
  assert.equal($("#caption-text").textContent, "");
  assert.equal($("#caption-text").classList.contains("visible"), false);
  assert.equal($("#audio").src, audioSource);
  $("#cc").value = "ko";
  $("#cc").dispatchEvent(event("change"));
  $("#play").click();
  await settle();
  assert.equal($("#video").paused, false);
  assert.equal($("#audio").paused, false);
  $("#voice").value = "en";
  $("#voice").dispatchEvent(event("change"));
  await settle();
  assertCurrent(first, "en");
  assert.equal($("#video").currentTime, captionTime);
  assert.equal($("#audio").currentTime, captionTime);
  assert.equal($("#video").paused, false, "voice switch preserves playing state");
  assert.equal($("#audio").paused, false);
  assert.equal($("#cc").value, "ko", "English audio still permits Korean CC");
  $("#play").click();
  assert.equal($("#video").paused, true);
  assert.equal($("#audio").paused, true);
  const seekTime = Math.min(52, first.duration / 2);
  $("#seek").value = String(seekTime);
  $("#seek").dispatchEvent(event("input"));
  assert.equal($("#video").currentTime, seekTime);
  assert.equal($("#audio").currentTime, seekTime);
  assert.equal($("#video").paused, true, "seeking a paused video does not autoplay");
  const sameSeason = episodes.filter((episode) => String(episode.season) === seasons[0]);
  const next = sameSeason[Math.min(3, sameSeason.length - 1)];
  document.querySelector(`[data-id="${next.id}"]`).click();
  await settle();
  assertCurrent(next, "en");
  assert.equal($("#video").currentTime, 0);
  assert.equal($("#audio").currentTime, 0);
  for (const season of seasons.slice(1).concat(seasons[0])) {
    $("#seek").value = "17";
    $("#seek").dispatchEvent(event("input"));
    $("#play").click();
    await settle();
    assert.equal($("#video").paused, false);
    $("#season").value = season;
    $("#season").dispatchEvent(event("change"));
    await settle();
    assertSeasonCards(season);
    assertCurrent(episodes.find((episode) => String(episode.season) === season), "en");
    assert.equal($("#video").currentTime, 0, "season change starts its first episode at zero");
    assert.equal($("#audio").currentTime, 0);
    assert.equal($("#video").paused, true, "season change pauses playback");
    assert.equal($("#audio").paused, true);
    assert.equal($("#voice").value, "en");
    assert.equal($("#cc").value, "ko", "season change preserves independent language selections");
  }
  assert.deepEqual(errors, []);
  console.log(JSON.stringify({ passed: true, engine: "jsdom; media decoding and media events mocked; not a real-browser playback test", episodes: episodes.length, seasons: seasons.length, episodesPerSeason: seasonCounts, checks: [
    "catalog-derived episode count and unique IDs", "season selector and visible episode cards",
    "cross-season selection loads first episode and resets time", "selected title, goals, parent tips and download",
    "five audio choices; four CC choices plus off; no English CC", "all episodes contain four embedded caption languages",
    "independent audio and CC; English audio with Korean CC", "captions follow time; CC off hides captions",
    "voice switch retains time and playing state", "play and pause both elements", "seek synchronizes audio without autoplay",
    "episode and season changes reset time and preserve language selections",
  ] }, null, 2));
} finally {
  dom.window.close();
}
