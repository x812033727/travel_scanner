// Reproduce this episode's measured AAC peak correction while retaining native assembly checks.
// Run from the repository: node docs/videos/openai-dns-containment/assemble-with-peak-guard.mjs
//   --slug openai-dns-containment --workdir <external-video-workdir>
import { run } from '../../../tools/video/assemble/cli.mjs';
import { runTool } from '../../../tools/video/assemble/ffmpeg.mjs';
import { ROOT } from '../../../tools/video/core/paths.mjs';
import { EXIT } from '../../../tools/video/cli.mjs';

async function withPeakHeadroom(binary, args, ...rest) {
  const adjusted = [...args];
  const filter = adjusted.indexOf('-af');
  if (filter >= 0 && adjusted[filter + 1].includes('loudnorm=I=-14:TP=-1:')) {
    adjusted[filter + 1] = adjusted[filter + 1].replace('loudnorm=I=-14:TP=-1:', 'loudnorm=I=-14:TP=-3:');
    if (adjusted.includes('aac')) {
      adjusted[filter + 1] = adjusted[filter + 1].replace('linear=true', 'linear=false')
        + ',alimiter=limit=0.707946:level=false:latency=true';
    }
  }
  return runTool(binary, adjusted, ...rest);
}

process.exitCode = await run('assemble', process.argv.slice(2), {
  root: ROOT, env: process.env, stdout: process.stdout, stderr: process.stderr,
  now: () => new Date(), EXIT,
}, { runTool: withPeakHeadroom });
