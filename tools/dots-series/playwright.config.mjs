import { defineConfig, devices } from "@playwright/test";

export default defineConfig({
  testDir: "../../apps/web/e2e",
  testMatch: "dots-series.spec.ts",
  workers: 1,
  use: { trace: "retain-on-failure" },
  projects: [
    { name: "desktop-chromium", use: { ...devices["Desktop Chrome"] } },
    { name: "mobile-chromium", use: { ...devices["Pixel 7"] } },
  ],
});
