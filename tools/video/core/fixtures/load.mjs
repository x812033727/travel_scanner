// Shared by the core tests: the minimal example video, and a throwaway repository layout
// (docs/videos/<slug>/) plus a work directory outside it.
import { cpSync, mkdirSync, mkdtempSync, readFileSync } from "node:fs";
import { tmpdir } from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

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

/** A fake repository holding a fixture (minimal, drama, explainer or story) as docs/videos/<slug>/, and a work base beside it. */
export function sandbox(slug = "fixture-minimal", name = "minimal") {
  const base = mkdtempSync(path.join(tmpdir(), "video-core-"));
  const root = path.join(base, "repo");
  const videos = path.join(root, "docs", "videos");
  mkdirSync(videos, { recursive: true });
  cpSync(path.join(FIXTURES, name), path.join(videos, slug), { recursive: true });
  cpSync(path.join(FIXTURES, "lexicon.json"), path.join(videos, "lexicon.json"));
  const work = path.join(base, "work");
  mkdirSync(work);
  return { base, root, videos, dir: path.join(videos, slug), work, workdir: path.join(work, slug), slug };
}
