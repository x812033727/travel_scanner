import { defineConfig } from "@playwright/test";
import { readFileSync } from "node:fs";
import path from "node:path";

const prepared = JSON.parse(readFileSync(path.join(import.meta.dirname, "prepared.json"), "utf8"));
export default defineConfig({
  testDir: path.join(prepared.web, "e2e"), testMatch: "gemini-series.spec.ts", workers: 1,
  timeout: 45000, reporter: [["list"], ["json", { outputFile: path.join(import.meta.dirname, process.env.GEMINI_E2E_ADVANCED === "true" ? "advanced-results.json" : "base-results.json") }]],
  outputDir: path.join(import.meta.dirname, ".workspaces", process.env.GEMINI_E2E_ADVANCED === "true" ? "advanced-results" : "base-results"),
  use: { trace: "retain-on-failure" }, projects: [
    { name: "desktop", use: { browserName: "chromium", viewport: { width: 1200, height: 900 } } },
    { name: "mobile", use: { browserName: "chromium", viewport: { width: 360, height: 800 } } },
  ],
});
