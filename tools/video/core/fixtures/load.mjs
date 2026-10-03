// Shared by the core tests: the minimal example video, and a throwaway repository layout
// (docs/videos/<slug>/) plus a work directory outside it.
import { cpSync, mkdirSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { bindAudioEvidence } from "../audio-evidence.mjs";
import { encodeWav } from "../../tts/wav.mjs";

/** Deterministic silent takes for tests which exercise timing and approvals without synthesis. */
export function writeAudioFixture(timeline, workdir) {
  mkdirSync(path.join(workdir, "audio"), { recursive: true });
  for (const line of timeline.lines) writeFileSync(path.join(workdir, "audio", `${line.id}.wav`), encodeWav(new Int16Array(line.audio_samples)));
  writeFileSync(path.join(workdir, "narration.wav"), encodeWav(new Int16Array(timeline.total_frames * 48_000 / timeline.fps)));
  Object.assign(timeline, bindAudioEvidence(timeline, workdir));
  writeFileSync(path.join(workdir, "timeline.json"), JSON.stringify(timeline));
  return timeline;
}

export const FIXTURES = path.dirname(fileURLToPath(import.meta.url));
export const FIXTURE_FILE = path.join(FIXTURES, "minimal", "video.json");
export const DRAMA_FIXTURE_FILE = path.join(FIXTURES, "drama", "video.json");
// The same three scenes narrated in English (`narration_locale: "en"`).
export const EN_FIXTURE_FILE = path.join(FIXTURES, "en", "video.json");
// A brand story (docs/videos/STORY.md): a narrator-only drama whose series.json says kind "story".
export const STORY_FIXTURE_FILE = path.join(FIXTURES, "story", "video.json");

export const fixture = () => JSON.parse(readFileSync(FIXTURE_FILE, "utf8"));
export const fixtureLexicon = () => JSON.parse(readFileSync(path.join(FIXTURES, "lexicon.json"), "utf8"));
export const fixtureBrief = () => readFileSync(path.join(FIXTURES, "minimal", "brief.md"), "utf8");
export const dramaFixture = () => JSON.parse(readFileSync(DRAMA_FIXTURE_FILE, "utf8"));
export const dramaBrief = () => readFileSync(path.join(FIXTURES, "drama", "brief.md"), "utf8");
export const enFixture = () => JSON.parse(readFileSync(EN_FIXTURE_FILE, "utf8"));
export const enBrief = () => readFileSync(path.join(FIXTURES, "en", "brief.md"), "utf8");
// A narrator-only explainer in the flat-explainer preset (docs/videos/so-thats-why/).
export const explainerFixture = () => JSON.parse(readFileSync(path.join(FIXTURES, "explainer", "video.json"), "utf8"));
export const explainerBrief = () => readFileSync(path.join(FIXTURES, "explainer", "brief.md"), "utf8");

export const storyFixture = () => JSON.parse(readFileSync(STORY_FIXTURE_FILE, "utf8"));
export const storyBrief = () => readFileSync(path.join(FIXTURES, "story", "brief.md"), "utf8");
export const storySeries = () => JSON.parse(readFileSync(path.join(FIXTURES, "story", "series.json"), "utf8"));

// Every throwaway directory made here is removed when the test process exits (node --test runs
// each test file in a process of its own), so a run leaves nothing in the system's temporary
// directory. VIDEO_KEEP_SANDBOX=1 keeps them for a look after a failure.
const made = [];

function removeMade() {
  if (process.env.VIDEO_KEEP_SANDBOX === "1") return;
  for (const dir of made) {
    // A file still open on Windows must not throw from an exit handler or change the exit code.
    try {
      rmSync(dir, { recursive: true, force: true });
    } catch {
      // Left behind; the next one may still go.
    }
  }
}

/** A new empty directory under the system's temporary directory, removed when this process exits. */
export function tempDir(prefix) {
  const dir = mkdtempSync(path.join(tmpdir(), prefix));
  if (made.length === 0) process.once("exit", removeMade);
  made.push(dir);
  return dir;
}

/** A fake repository holding a fixture (minimal, drama, explainer or story) as docs/videos/<slug>/, and a work base beside it. */
export function sandbox(slug = "fixture-minimal", name = "minimal") {
  const base = tempDir("video-core-");
  const root = path.join(base, "repo");
  const videos = path.join(root, "docs", "videos");
  mkdirSync(videos, { recursive: true });
  cpSync(path.join(FIXTURES, name), path.join(videos, slug), { recursive: true });
  cpSync(path.join(FIXTURES, "lexicon.json"), path.join(videos, "lexicon.json"));
  const work = path.join(base, "work");
  mkdirSync(work);
  return { base, root, videos, dir: path.join(videos, slug), work, workdir: path.join(work, slug), slug };
}

// Illustrated slides (docs/videos/ILLUSTRATED.md): a slides video with still shots between its
// cards, a look, a licensed music bed and a sound-effect set.
export const ILLUSTRATED_FIXTURE_FILE = path.join(FIXTURES, "illustrated", "video.json");
export const illustratedFixture = () => JSON.parse(readFileSync(ILLUSTRATED_FIXTURE_FILE, "utf8"));
export const illustratedBrief = () => readFileSync(path.join(FIXTURES, "illustrated", "brief.md"), "utf8");
