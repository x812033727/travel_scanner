/**
 * Test fixture only. Production code never imports this file.
 *
 * Reads the Gemini advanced-series planning documents from the repository's docs/ folder at
 * runtime instead of importing the JSON. The web image copies apps/web alone into its builder,
 * and `next build` type-checks every test file, so a static import of a path outside apps/web
 * fails that build with TS2307 even though the tests themselves only run in the full repository.
 */
import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import type { GeminiLesson, GeminiPath } from "./gemini-series-projection";

const advancedDirectory = resolve(import.meta.dirname, "../../../docs/gemini-series/advanced");

/**
 * One planned advanced lesson as the tests use it. The file carries further editorial fields
 * (steps, exercise, acceptance, sourceIds, gate, ...) that stay in the parsed objects at runtime
 * but are deliberately not declared here.
 */
export type GeminiCurriculumArticle = Omit<GeminiLesson, "minutes" | "labMinutes" | "stage" | "track"> & {
  stage: number; track: string; estimatedReadingMinutes: number; estimatedLabMinutes: number;
};
export type GeminiCurriculumRoute = Pick<GeminiPath, "id" | "title" | "articles">;
export type GeminiCurriculum = {
  locale: string; hubSlug: string;
  articles: readonly GeminiCurriculumArticle[]; routes: readonly GeminiCurriculumRoute[];
};

/** The frozen identities every enabled projection must reproduce, in order. */
export type GeminiCatalogueContract = {
  locale: string; hubSlug: string;
  articles: readonly { number: number; slug: string; stage: number }[];
  paths: readonly { id: string; stage: number }[];
};

function readAdvancedJson(file: string): unknown {
  return JSON.parse(readFileSync(resolve(advancedDirectory, file), "utf8"));
}

/** docs/gemini-series/advanced/curriculum.json */
export function loadGeminiCurriculum(): GeminiCurriculum {
  return readAdvancedJson("curriculum.json") as GeminiCurriculum;
}

/** docs/gemini-series/advanced/platform/catalogue-contract.json */
export function loadGeminiCatalogueContract(): GeminiCatalogueContract {
  return readAdvancedJson("platform/catalogue-contract.json") as GeminiCatalogueContract;
}
