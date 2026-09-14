import {defineConfig,devices} from '@playwright/test';
import {fileURLToPath} from 'node:url';
const evidence=fileURLToPath(new URL('../../../docs/claude-code-series/advanced/evidence/',import.meta.url));
process.env.CLAUDE_SERIES_EVIDENCE=evidence;
export default defineConfig({
 testDir:'../../../apps/web/e2e',testMatch:'claude-code-series.spec.ts',
 workers:1,timeout:60000,use:{...devices['Desktop Chrome'],trace:'retain-on-failure'},
 outputDir:evidence+'/browser-runs',
 reporter:[['list'],['json',{outputFile:evidence+'/'+(process.env.CLAUDE_SERIES_REPORT??'browser-tests.json')}]],
});
