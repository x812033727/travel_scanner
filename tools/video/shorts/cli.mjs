#!/usr/bin/env node
import { readFileSync } from 'node:fs';
import path from 'node:path';
import { parseArgs } from 'node:util';
import { pathToFileURL } from 'node:url';
import { ROOT } from '../core/paths.mjs';
import { validate, verifyEvidence } from './core.mjs';

export async function main(args=process.argv.slice(2)) {
  const command = args[0];
  if (!command || command==='help' || command==='--help') {
    console.log('Shorts local pilot pipeline\n  validate --file SCRIPT.json [--source-base DIR]\n  build --file SCRIPT.json --workdir OUTSIDE_REPO [--source-base DIR] [--voice "Microsoft Hanhan Desktop"] [--channel msedge] [--audio-dir DIR]\n  track-init --dir OUTSIDE_REPO --start YYYY-MM-DD\n  report --dir TRACKING_DIR [--now ISO]\nAudio inputs: one 000.wav, 001.wav, ... for each narration phrase. No publishing or paid API calls.');
    return 0;
  }
  const {values} = parseArgs({args:args.slice(1),options:Object.fromEntries(['file','source-base','workdir','voice','channel','audio-dir','dir','start','now'].map(k=>[k,{type:'string'}])),strict:true});
  if (command==='track-init' || command==='report') {
    const {initTracking,trackingReport} = await import('./tracking.mjs');
    if (!values.dir) throw new Error('--dir required');
    const result = command==='track-init' ? initTracking({directory:values.dir,startDate:values.start}) : trackingReport({directory:values.dir,now:values.now});
    console.log(JSON.stringify(await result,null,2));
    return 0;
  }
  if (!['validate','build'].includes(command)) throw new Error(`unknown command ${command}`);
  if (!values.file) throw new Error('--file required');
  const sourceBase = path.resolve(values['source-base'] ?? path.join(ROOT,'docs/videos/ai-shorts'));
  const doc = JSON.parse(readFileSync(values.file,'utf8'));
  const errors=validate(doc);
  if (errors.length) throw new Error(errors.join('\n'));
  verifyEvidence(doc,sourceBase);
  if (command==='validate') console.log(`${doc.slug}: schema and source hashes OK`);
  else {
    const {build}=await import('./build.mjs');
    console.log(JSON.stringify(await build({file:path.resolve(values.file),sourceBase,workdir:values.workdir,voice:values.voice,channel:values.channel,audioDir:values['audio-dir']}),null,2));
  }
  return 0;
}
if (process.argv[1] && import.meta.url===pathToFileURL(path.resolve(process.argv[1])).href) main().catch(error=>{console.error(error.message);process.exitCode=1;});
