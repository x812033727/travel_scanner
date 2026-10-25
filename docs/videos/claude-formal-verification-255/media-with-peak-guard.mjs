// Retain native timing, caching and QA; reuse the measured AAC headroom adapter.
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { main, EXIT } from '../../../tools/video/cli.mjs';
import { run as assemble } from '../../../tools/video/assemble/cli.mjs';
import { withDubPeakHeadroom } from '../openai-dns-containment/dub-with-peak-guard.mjs';

const root = fileURLToPath(new URL('../../../', import.meta.url));
export async function runMedia(argv, overrides = {}) {
  if (argv[0] === 'assemble') {
    return assemble('assemble', argv.slice(1), {
      root, env: process.env, stdout: process.stdout, stderr: process.stderr,
      now: () => new Date(), EXIT, ...overrides,
    }, { runTool: withDubPeakHeadroom });
  }
  return main(argv, {
    root, ...overrides,
    ...(argv[0] === 'dub' ? { ffmpeg: { run: withDubPeakHeadroom } } : {}),
  });
}
if (process.argv[1] && import.meta.url === pathToFileURL(path.resolve(process.argv[1])).href) {
  process.exitCode = await runMedia(process.argv.slice(2));
}
