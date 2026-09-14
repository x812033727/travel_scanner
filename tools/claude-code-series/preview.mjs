// Node 22+ supports the erasable types used by this fixture.
import { startSeriesPreview, hubPath } from '../../apps/web/e2e/fixtures/claude-code-series.ts';
const preview = await startSeriesPreview();
console.log(`Local read-only preview (61 draft packs, no database import): ${preview.origin}${hubPath}`);
async function close() { await preview.stop(); process.exit(0); }
process.on('SIGINT', close);
process.on('SIGTERM', close);
