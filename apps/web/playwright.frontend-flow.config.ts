import { defineConfig } from "@playwright/test";
import base from "./playwright.config";
export default defineConfig({ ...base, testMatch: /frontend-flow\.spec\.ts$/, workers:1, timeout:60_000, expect:{timeout:15_000} });
