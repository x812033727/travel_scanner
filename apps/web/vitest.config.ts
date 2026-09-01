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
  },
  resolve: { alias: { "@": import.meta.dirname } },
});
