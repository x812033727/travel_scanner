import { defineConfig, devices } from "@playwright/test";

const port = process.env.PLAYWRIGHT_PORT || "3000";
const baseURL = `http://127.0.0.1:${port}`;
const reuseExistingServer = process.env.PLAYWRIGHT_REUSE_EXISTING === "true";

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
      command: `npm run dev -- --port ${port}`,
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

