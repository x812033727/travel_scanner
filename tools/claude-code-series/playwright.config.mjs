import { defineConfig, devices } from '@playwright/test';
import { fileURLToPath } from 'node:url';
export default defineConfig({
  testDir: '../../apps/web/e2e', testMatch: 'claude-code-series.spec.ts',
  workers: 1, timeout: 60000, use: { ...devices['Desktop Chrome'], trace: 'retain-on-failure' },
  outputDir: '../../docs/claude-code-series/evidence/browser-runs',
  reporter: [['list'], ['json', { outputFile: fileURLToPath(new URL('../../docs/claude-code-series/evidence/browser-tests.json', import.meta.url)) }]],
});
