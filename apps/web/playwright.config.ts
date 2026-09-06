import { defineConfig, devices } from "@playwright/test";

const port = process.env.PLAYWRIGHT_PORT || "3000";
const baseURL = `http://127.0.0.1:${port}`;
const reuseExistingServer = process.env.PLAYWRIGHT_REUSE_EXISTING === "true";
// CI builds the app right before this suite runs. Serving that build (`next start`)
// instead of compiling every page on its first visit, under a 30-second test timeout
// and next to a second server, is what keeps the navigation cases from timing out
// at random. Locally the dev server stays the default so an edit shows up without a
// rebuild; set PLAYWRIGHT_SERVE_BUILD=true after `npm run build` to run it the CI way.
const serveBuild = process.env.PLAYWRIGHT_SERVE_BUILD === "true";

export default defineConfig({
  testDir: "./e2e",
  use: { baseURL, trace: "on-first-retry" },
  webServer: [
    ...(!reuseExistingServer ? [{
      command: "node ../../tools/e2e-runtime-api.mjs",
      url: "http://127.0.0.1:8000/api/v1/runtime/site-visibility",
      reuseExistingServer: true,
      timeout: 30_000,
    }] : []),
    {
      command: serveBuild ? `npm run start -- --port ${port}` : `npm run dev -- --port ${port}`,
      url: baseURL,
      reuseExistingServer,
      timeout: 120_000,
      env: { API_INTERNAL_URL: process.env.API_INTERNAL_URL || "http://127.0.0.1:8000" },
    },
  ],
  projects: [
    { name: "desktop-chromium", use: { ...devices["Desktop Chrome"] } },
    { name: "mobile-chromium", use: { ...devices["Pixel 7"] } },
  ],
});

