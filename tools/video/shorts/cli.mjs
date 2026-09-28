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
    console.log('Shorts local pilot pipeline\n  validate --file SCRIPT.json [--source-base DIR]\n  build --file SCRIPT.json --workdir OUTSIDE_REPO [--source-base DIR] [--voice "Microsoft Hanhan Desktop"] [--channel msedge] [--audio-dir DIR]\n  from-episode --slug EPISODE --workdir OUTSIDE_REPO [--episode-workdir DIR] [--short 1|2] [--voice server|"Windows voice"] [--audio-dir DIR] [--check]\n  track-init --dir OUTSIDE_REPO --start YYYY-MM-DD\n  report --dir TRACKING_DIR [--now ISO]\nAudio inputs: one 000.wav, 001.wav, ... for each narration phrase. No publishing. build makes no paid API calls; from-episode with --voice server (its default) is billed by the narration server.');
    return 0;
  }
  const {values} = parseArgs({args:args.slice(1),options:{...Object.fromEntries(['file','source-base','workdir','voice','channel','audio-dir','dir','start','now','slug','episode-workdir','short'].map(k=>[k,{type:'string'}])),check:{type:'boolean'}},strict:true});
  if (command==='from-episode') return fromEpisode(values);
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
/**
 * An explainer episode's Shorts (docs/videos/so-thats-why/): shorts.json resolved against the
 * episode's keyframes, read in the channel voice by the narration server unless a Windows voice
 * or measured WAVs are given, then built one by one like any other Short.
 */
async function fromEpisode(values, ctx = {}) {
  if (!values.slug) throw new Error('--slug required: the long episode');
  const {loadEpisodeShorts} = await import('./episode.mjs');
  const episode = loadEpisodeShorts({slug:values.slug, workdirFlag:values['episode-workdir'], env:ctx.env ?? process.env, home:ctx.home});
  if (values.short !== undefined && !['1','2'].includes(values.short)) throw new Error('--short must be 1 or 2');
  const picked = values.short ? [episode.shorts[Number(values.short)-1]] : episode.shorts;
  for (const doc of picked) verifyEvidence(doc, episode.workdir);
  if (values.check) {
    console.log(`${values.slug}: ${picked.length} Shorts valid; every keyframe matches its hash`);
    return 0;
  }
  if (!values.workdir) throw new Error('--workdir required: an output directory outside the repository');
  const voice = values.voice ?? 'server';
  const {build} = await import('./build.mjs');
  const {serverOptions, serverPhrases} = await import('./voice.mjs');
  const videoId = episode.video.youtube?.video_id ?? null;
  const results = [];
  for (const doc of picked) {
    const phrases = doc.scenes.flatMap(scene=>scene.narration);
    let wavs;
    let narrator;
    if (!values['audio-dir'] && voice==='server') {
      const spoken = await serverPhrases({phrases, voice:episode.video.voice, lexicon:episode.lexicon, ...serverOptions({env:ctx.env ?? process.env, home:ctx.home, fetchImpl:ctx.fetch})});
      wavs = spoken.wavs;
      narrator = `server:${episode.video.voice.name}`;
      console.error(`${doc.slug}: ${phrases.length} phrases synthesized, ${spoken.billable} billable characters`);
    }
    results.push(await build({document:doc, sourceBase:episode.workdir, workdir:values.workdir, voice:voice==='server'?undefined:voice, channel:values.channel, audioDir:values['audio-dir'], wavs, narrator, longVideoId:videoId}));
  }
  console.log(JSON.stringify(results,null,2));
  return 0;
}

if (process.argv[1] && import.meta.url===pathToFileURL(path.resolve(process.argv[1])).href) main().catch(error=>{console.error(error.message);process.exitCode=1;});
