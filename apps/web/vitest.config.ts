import { defineConfig } from "vitest/config";
export default defineConfig({
  test: {
    environment: "jsdom",
    globals: true,
    exclude: ["e2e/**", "node_modules/**"],
    pool: "threads",
    maxWorkers: 1,
    fileParallelism: false,
  },
  resolve: { alias: { "@": import.meta.dirname } },
});
