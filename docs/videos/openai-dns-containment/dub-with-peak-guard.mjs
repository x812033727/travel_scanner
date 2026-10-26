// Episode-specific AAC headroom; retain the native dub timing, caching and check machinery.
// Run like the native CLI: node <this-file> dub --slug openai-dns-containment --locale en ...
import path from 'node:path';
import { pathToFileURL } from 'node:url';
import { main } from '../../../tools/video/cli.mjs';
import { runTool } from '../../../tools/video/assemble/ffmpeg.mjs';

export async function withDubPeakHeadroom(binary, args, ...rest) {
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

if (process.argv[1] && import.meta.url === pathToFileURL(path.resolve(process.argv[1])).href) {
  process.exitCode = await main(process.argv.slice(2), { ffmpeg: { run: withDubPeakHeadroom } });
}
