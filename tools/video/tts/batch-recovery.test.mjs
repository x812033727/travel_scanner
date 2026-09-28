import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import test from "node:test";
import { EXIT, main } from "../cli.mjs";
import { fixture, sandbox } from "../core/fixtures/load.mjs";
import { hintTerms } from "./check.mjs";
import { encodeWav } from "./wav.mjs";

test("check-audio preserves a paid cross-scene batch and resumes only the unjudged lines", async () => {
  const box = sandbox();
  const doc = fixture();
  doc.target_minutes = [0.5, 20];
  doc.scenes = Array.from({ length: 90 }, (_, index) => ({
    ...structuredClone(doc.scenes[0]), id: `scene-${index}`,
    lines: [{ id: `z${String(index).padStart(3, "0")}`, text: doc.scenes[0].lines[0].text }],
  }));
  writeFileSync(path.join(box.dir, "video.json"), JSON.stringify(doc));
  mkdirSync(path.join(box.workdir, "audio"), { recursive: true });
  mkdirSync(path.join(box.workdir, "review"), { recursive: true });
  const wav = encodeWav(Int16Array.from({ length: 2400 }, (_, i) => Math.round(Math.sin(i / 16) * 3000)));
  const clip = createHash("sha256").update(wav).digest("hex").slice(0, 16);
  const cache = { lines: {} };
  const ids = doc.scenes.map(scene => scene.lines[0].id);
  for (const scene of doc.scenes) {
    const line = scene.lines[0];
    writeFileSync(path.join(box.workdir, "audio", `${line.id}.wav`), wav);
    // Previously transcribed audio needs Jev only, with no real speech/model request.
    cache.lines[line.id] = { scene: scene.id, clip, terms: hintTerms(line), heard: "完全不同的內容", noul: null };
  }
  const cacheFile = path.join(box.workdir, "review", "check.json");
  writeFileSync(cacheFile, JSON.stringify(cache));
  writeFileSync(path.join(box.workdir, "timeline.json"), JSON.stringify({ speech_hash: "synthetic", lines: [] }));
  const calls = [];
  let failing = true;
  const out = { stdout: "", stderr: "" };
  const ctx = {
    root: box.root, home: box.base,
    env: { VIDEO_WORKDIR: box.work, MOKAAIR_VIDEO_TOKEN: `mkv_${"t".repeat(43)}` },
    now: () => new Date("2026-09-28T08:00:00Z"), sleep: async () => {},
    stdout: { write: text => { out.stdout += text; } }, stderr: { write: text => { out.stderr += text; } },
    fetch: async (url, init) => {
      assert.ok(url.endsWith("/speech/judge"), `unexpected request: ${url}`);
      const { lines } = JSON.parse(init.body);
      calls.push(lines.map(line => line.id));
      if (failing && lines[0].id === "z040") return Response.json({ code: "jev_budget_exhausted", detail: "Synthetic second-batch interruption" }, { status: 429 });
      return Response.json({ results: lines.map(line => ({ id: line.id, noul: 0.95 })) });
    },
  };
  assert.equal(await main(["check-audio", "--slug", box.slug], ctx), EXIT.external, JSON.stringify(out));
  assert.deepEqual(calls, [ids.slice(0, 40), ids.slice(40, 80)]);
  const interrupted = JSON.parse(readFileSync(cacheFile, "utf8"));
  assert.deepEqual(ids.filter(id => interrupted.lines[id].noul === 0.95), ids.slice(0, 40));
  assert.ok(ids.slice(40).every(id => interrupted.lines[id].noul === null));

  failing = false;
  const beforeResume = calls.length;
  assert.equal(await main(["check-audio", "--slug", box.slug], ctx), EXIT.ok, JSON.stringify(out));
  assert.deepEqual(calls.slice(beforeResume), [ids.slice(40, 80), ids.slice(80)]);
  assert.ok(Object.values(JSON.parse(readFileSync(cacheFile, "utf8")).lines).every(line => line.noul === 0.95));
  const beforeCachedRun = calls.length;
  assert.equal(await main(["check-audio", "--slug", box.slug], ctx), EXIT.ok);
  assert.equal(calls.length, beforeCachedRun, "cached judgments must not spend another call");
});
