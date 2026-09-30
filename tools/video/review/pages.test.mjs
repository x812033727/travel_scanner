import assert from "node:assert/strict";
import test from "node:test";
import { JSDOM } from "jsdom";

import { presentationTimeline } from "../core/branding.mjs";
import { fixture } from "../core/fixtures/load.mjs";
import { estimateTimeline, frameToSeconds } from "../core/timeline.mjs";
import { audioReviewHtml, finalReviewHtml } from "./pages.mjs";

test("the branded final review seeks on presentation timing while audio review keeps the narration clock", () => {
  const doc = fixture();
  const timeline = { ...estimateTimeline(doc), speech_hash: "speech-v1" };
  const before = JSON.stringify(timeline);
  const applied = { hash: "a".repeat(64), id: "brand-v1", intro_frames: 150, outro_frames: 90, body_frames: timeline.total_frames };
  const checks = { ok: true, speech_hash: timeline.speech_hash, branding: applied, problems: [] };
  const html = finalReviewHtml(doc, timeline, checks);
  const dom = new JSDOM(html, { runScripts: "dangerously" });
  try {
    const { document, Event, MouseEvent, HTMLElement } = dom.window;
    HTMLElement.prototype.scrollIntoView = () => {};
    const video = document.getElementById("video");
    let played = 0;
    video.play = () => { played += 1; return Promise.resolve(); };
    const lines = [...document.querySelectorAll("#lines .cue")];
    const chapters = [...document.querySelectorAll("h2 + ol:not(#lines) .cue")];
    assert.equal(Number(chapters[0].dataset.start), 0, "the first chapter includes the brand opening");
    assert.equal(chapters.length, timeline.chapters.length, "no extra five-second chapter");
    lines[0].dispatchEvent(new MouseEvent("click", { bubbles: true }));
    assert.equal(video.currentTime, frameToSeconds(timeline.lines[0].start_frame + 150) + .01);
    assert.equal(lines[0].querySelector(".time").textContent, "00:05");
    chapters[1].dispatchEvent(new MouseEvent("click", { bubbles: true }));
    assert.equal(video.currentTime, frameToSeconds(timeline.chapters[1].start_frame + 150) + .01);
    assert.equal(played, 2);

    video.currentTime = 1;
    video.dispatchEvent(new Event("timeupdate"));
    assert.equal(document.querySelectorAll("#lines .now").length, 0, "the intro highlights no body dialogue");
    video.currentTime = 5.1;
    video.dispatchEvent(new Event("timeupdate"));
    assert.equal(lines[0].classList.contains("now"), true);
    video.currentTime = frameToSeconds(timeline.total_frames + 150) + .1;
    video.dispatchEvent(new Event("timeupdate"));
    assert.equal(document.querySelectorAll("#lines .now").length, 0, "the CTA highlights no body dialogue");

    assert.equal(finalReviewHtml(doc, presentationTimeline(timeline, applied), checks), html, "an already presented timeline is not offset twice");
    assert.equal(JSON.stringify(timeline), before, "the approved narration timeline is untouched");
    const audio = new JSDOM(audioReviewHtml(doc, timeline));
    try {
      assert.equal(audio.window.document.querySelector(".time").textContent, "00:00");
      assert.equal(audio.window.document.querySelector("audio").getAttribute("src"), `../audio/${timeline.lines[0].id}.wav`);
    } finally { audio.window.close(); }
  } finally { dom.window.close(); }
});

test("a branded final review refuses a stale body and legacy review timing stays unchanged", () => {
  const doc = fixture();
  const timeline = { ...estimateTimeline(doc), speech_hash: "speech-v1" };
  const checks = { speech_hash: timeline.speech_hash, branding: { hash: "a".repeat(64), intro_frames: 150, outro_frames: 90, body_frames: timeline.total_frames } };
  assert.throws(() => finalReviewHtml(doc, timeline, { ...checks, speech_hash: "old" }), /another body timeline/);
  assert.throws(() => finalReviewHtml(doc, timeline, { ...checks, branding: { ...checks.branding, body_frames: timeline.total_frames + 1 } }), /another body timeline/);
  const legacy = new JSDOM(finalReviewHtml(doc, timeline, { problems: [] }));
  try {
    assert.equal(Number(legacy.window.document.querySelector("#lines .cue").dataset.start), frameToSeconds(timeline.lines[0].start_frame));
  } finally { legacy.window.close(); }
});
