import { defineConfig } from "vitest/config";
export default defineConfig({
  test: {
    environment: "jsdom",
    globals: true,
    setupFiles: ["./vitest.setup.tsx"],
    exclude: ["e2e/**", "node_modules/**", ".next/**"],
    pool: "threads",
    maxWorkers: 1,
    fileParallelism: false,
    // OneDrive filesystem hooks make the interaction-heavy jsdom suites slower on Windows.
    // Keep the existing fail-fast budget in Linux CI.
    testTimeout: process.platform === "win32" ? 15_000 : 5_000,
  },
  resolve: { alias: { "@": import.meta.dirname } },
});
