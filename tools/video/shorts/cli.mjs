#!/usr/bin/env node
import { copyFileSync, existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import path from 'node:path';
import { parseArgs } from 'node:util';
import { pathToFileURL } from 'node:url';
import { ROOT, lexiconFile, readJson } from '../core/paths.mjs';
import { validate, verifyEvidence } from './core.mjs';

const HELP = `Shorts pipeline (docs/videos/SHORTS.md)
  validate     --file SCRIPT.json [--source-base DIR]
  build        --file SCRIPT.json --workdir OUTSIDE_REPO [--source-base DIR] [--speech server|windows|files]
               [--audio-dir DIR] [--voice "Microsoft Hanhan Desktop"] [--channel msedge] [--redo BUILD_DIR]
               [--captions plain|karaoke]   (else VIDEO_SHORTS_CAPTIONS, else plain)
  check-audio  --dir BUILD_DIR [--threshold 0.5]
  qa           --dir BUILD_DIR [--verify verify.json] [--offline]
  package      --dir BUILD_DIR
  push         --dir BUILD_DIR
  import       --from DIR --workdir OUTSIDE_REPO      (final.mp4, zh-TW.srt, meta.json)
  from-episode --slug EPISODE --workdir OUTSIDE_REPO [--episode-workdir DIR] [--short 1|2] [--speech ...] [--check]
               an explainer's two Shorts (docs/videos/<slug>/shorts.json) built on its keyframes
  tick         the worker's knock: the site does what is due on the Shorts calendar
  track-init   --dir OUTSIDE_REPO --start YYYY-MM-DD
  report       --dir TRACKING_DIR [--now ISO]
Narration: server is the channel's voice through the site (needs \`node tools/video/cli.mjs login\`);
windows is the installed voice; files takes one 000.wav, 001.wav, ... per phrase from --audio-dir.
The order for one Short: build, check-audio, qa, package, push.`;
const FLAGS = ['file', 'source-base', 'workdir', 'voice', 'channel', 'audio-dir', 'dir', 'start', 'now', 'speech', 'redo', 'threshold', 'verify', 'from', 'slug', 'episode-workdir', 'short', 'captions'];
const print = (value) => console.log(typeof value === 'string' ? value : JSON.stringify(value, null, 2));
const need = (values, name) => {
  if (!values[name]) throw new Error(`--${name} required`);
  return path.resolve(values[name]);
};
// The dictionary of spoken forms, when this checkout has one; the worker's copy may be older.
const lexicon = () => readJson(lexiconFile(ROOT), null);

/** Runs one command; resolves to the exit code: 0 done, 1 a check did not pass. */
export async function main(args=process.argv.slice(2), { env = process.env, fetch: fetchImpl, home } = {}) {
  const command = args[0];
  if (!command || command==='help' || command==='--help') {
    print(HELP);
    return 0;
  }
  const {values} = parseArgs({args:args.slice(1),options:{...Object.fromEntries(FLAGS.map(k=>[k,{type:'string'}])),offline:{type:'boolean'},check:{type:'boolean'}},strict:true});
  const site = async () => (await import('./site.mjs')).siteClient({ env, home, ...(fetchImpl ? { fetch: fetchImpl } : {}) });
  if (command==='track-init' || command==='report') {
    const {initTracking,trackingReport} = await import('./tracking.mjs');
    if (!values.dir) throw new Error('--dir required');
    const result = command==='track-init' ? initTracking({directory:values.dir,startDate:values.start}) : trackingReport({directory:values.dir,now:values.now});
    print(await result);
    return 0;
  }
  if (command==='tick') {
    // A site from before the route answers 404: the knock is skipped without a word of error.
    const done = await (await site()).tick();
    print(done ?? 'the site has no Shorts calendar yet; nothing to do');
    return 0;
  }
  if (command==='check-audio') {
    const {checkAudio} = await import('./check.mjs');
    const check = await checkAudio({directory:need(values,'dir'),client:await site(),lexicon:lexicon(),threshold:values.threshold===undefined?undefined:Number(values.threshold)});
    print(`${check.checked} phrases checked, ${check.flagged} flagged${check.flagged?`; next: build --redo ${values.dir}`:''}`);
    for (const line of check.flagged_lines) print(`  #${line.index}  Jev ${line.noul ?? 'no answer'}\n    script: ${line.text}\n    heard:  ${line.heard}`);
    return check.ok ? 0 : 1;
  }
  if (command==='qa') {
    const {runQa,VERIFY_FILE} = await import('./qa.mjs');
    const directory = need(values,'dir');
    if (values.verify) copyFileSync(path.resolve(values.verify),path.join(directory,VERIFY_FILE));
    const report = await runQa({directory,client:values.offline?null:await site(),offline:Boolean(values.offline)});
    for (const each of report.items) print(`  ${each.ok?'ok  ':'FAIL'} ${each.id.padEnd(10)} ${each.detail}`);
    return report.ok ? 0 : 1;
  }
  if (command==='package') {
    const {packageBuild} = await import('./package.mjs');
    const directory = need(values,'dir');
    const doc = readJson(path.join(directory,'script.json'),null);
    // Keep the preceding package intact if the owner's current settings cannot be read.
    const client = await site();
    const settings = await client.settings();
    const source = client && doc?.source?.slug ? await client.project(doc.source.slug).catch(() => null) : null;
    const {report} = packageBuild({directory,settings,source});
    for (const each of report.items) print(`  ${each.ok?'ok  ':'FAIL'} ${each.id.padEnd(12)} ${each.detail}`);
    return report.ok ? 0 : 1;
  }
  if (command==='push') {
    const {push} = await import('./push.mjs');
    const result = await push({directory:need(values,'dir'),client:await site(),log:(line)=>console.error(line)});
    print({slug:result.slug,final:result.final?.status??null,publish:result.publish?.status??null,waits:result.waits});
    return 0;
  }
  if (command==='import') {
    const {importShort} = await import('./import.mjs');
    print(await importShort({from:need(values,'from'),workdir:values.workdir}));
    return 0;
  }
  if (command==='from-episode') return fromEpisode(values, { env, home, site });
  if (!['validate','build'].includes(command)) throw new Error(`unknown command ${command}`);
  if (!values.file) throw new Error('--file required');
  const sourceBase = path.resolve(values['source-base'] ?? path.join(ROOT,'docs/videos/ai-shorts'));
  const doc = JSON.parse(readFileSync(values.file,'utf8'));
  const errors=validate(doc);
  if (errors.length) throw new Error(errors.join('\n'));
  verifyEvidence(doc,sourceBase);
  if (command==='validate') print(`${doc.slug}: schema and source hashes OK`);
  else {
    const {build}=await import('./build.mjs');
    const {defaultSource,SOURCES}=await import('./speech.mjs');
    const speech = values.speech ?? (values['audio-dir'] ? 'files' : defaultSource());
    if (!SOURCES.includes(speech)) throw new Error(`--speech must be one of ${SOURCES.join(', ')}`);
    if (values.redo && !existsSync(path.resolve(values.redo))) throw new Error(`--redo: ${values.redo} does not exist`);
    print(await build({file:path.resolve(values.file),sourceBase,workdir:values.workdir,voice:values.voice,channel:values.channel,audioDir:values['audio-dir'],speech,client:speech==='server'?await site():null,redo:values.redo?path.resolve(values.redo):null,lexicon:lexicon(),captions:values.captions}));
  }
  return 0;
}
/**
 * An explainer's Shorts (docs/videos/so-thats-why/): shorts.json resolved against the episode's
 * keyframes (each shot becomes its keyframe, bound by hash), then each built like any other script:
 * the resolved script is written beside the builds and the episode's work directory is the source
 * base. After this, check-audio, qa, package and push take each build directory as usual.
 */
async function fromEpisode(values, { env, home, site }) {
  if (!values.slug) throw new Error('--slug required: the long episode');
  if (values.short !== undefined && !['1','2'].includes(values.short)) throw new Error('--short must be 1 or 2');
  const {loadEpisodeShorts} = await import('./episode.mjs');
  const episode = loadEpisodeShorts({slug:values.slug, workdirFlag:values['episode-workdir'], env, home});
  const picked = values.short ? [episode.shorts[Number(values.short)-1]] : episode.shorts;
  for (const doc of picked) {
    const errors = validate(doc);
    if (errors.length) throw new Error(`${doc.slug}: ${errors.join('; ')}`);
    verifyEvidence(doc, episode.workdir);
  }
  if (values.check) {
    print(`${values.slug}: ${picked.length} Shorts valid; every keyframe matches its hash`);
    return 0;
  }
  const workdir = need(values,'workdir');
  const {build} = await import('./build.mjs');
  const {SOURCES} = await import('./speech.mjs');
  const speech = values.speech ?? (values['audio-dir'] ? 'files' : 'server');
  if (!SOURCES.includes(speech)) throw new Error(`--speech must be one of ${SOURCES.join(', ')} (default server: the episode's channel voice)`);
  const client = speech==='server' ? await site() : null;
  const results = [];
  for (const doc of picked) {
    const file = path.join(workdir, 'episode-scripts', `${doc.slug}.json`);
    mkdirSync(path.dirname(file), {recursive:true});
    writeFileSync(file, `${JSON.stringify(doc,null,2)}\n`);
    results.push(await build({file, sourceBase:episode.workdir, workdir, voice:values.voice, channel:values.channel, audioDir:values['audio-dir'], speech, client, lexicon:episode.lexicon ?? lexicon(), captions:values.captions}));
  }
  print(results);
  return 0;
}

if (process.argv[1] && import.meta.url===pathToFileURL(path.resolve(process.argv[1])).href) main().then(code=>{process.exitCode=code;}).catch(error=>{console.error(error.message);process.exitCode=error.who==='owner'?3:error.who==='service'?4:1;});
