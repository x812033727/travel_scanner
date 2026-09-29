import { copyFileSync, existsSync, mkdirSync, readFileSync, realpathSync, writeFileSync } from 'node:fs';
import path from 'node:path';
import { fontDir, parseUnicodeRanges, covers } from '../render/fonts.mjs';
import { bedLevel, bedLoudnessArgs, checkBed, measureMixArgs, mixArgs } from '../assemble/drama.mjs';
import { locateFfmpeg, runTool } from '../assemble/ffmpeg.mjs';
import { parseEbur128, parseLoudnorm } from '../assemble/plan.mjs';
import { sfxSetHash, sfxTrackArgs } from '../assemble/sfx.mjs';
import { musicInputs, sfxInputs } from '../assemble/sound.mjs';
import { encodeWav, parseWav, requireNarrationFormat } from '../tts/wav.mjs';
import { ROOT, isInside, resolveWorkBase, stopRequested } from '../core/paths.mjs';
import { PROFILE, SCRIPT_FILE, USAGE_FILE, buildTimeline, esc, lineOf, phrasesOf, sceneHtml, sha256, srt, validate, verifyEvidence } from './core.mjs';
import { themeOf, themeText } from './layouts.mjs';
import { MOTION_VERSION, backgroundOf, cameraOf, cardsList, firstFrameArgs, lastFrameArgs, sceneSpans, segmentArgs, shortSfxPlan } from './motion.mjs';
import { WINDOWS_VOICE, defaultSource, flaggedPhrases, narrate } from './speech.mjs';

const saveJson = (file, data) => writeFileSync(file, JSON.stringify(data, null, 2) + '\n');
const number = i => String(i).padStart(3, '0');
export function loudnessResult(stderr) {
  const blocks = [...stderr.matchAll(/\{\s*"input_i"[\s\S]*?\}/g)];
  if (!blocks.length) throw new Error('ffmpeg did not report loudness');
  const data = JSON.parse(blocks.at(-1)[0]);
  if (!['input_i','input_tp','input_lra','input_thresh','target_offset'].every(k=>Number.isFinite(Number(data[k])))) throw new Error('invalid loudness measurement (silent or corrupt audio)');
  return data;
}

/** What a final cut measures as: the streams of final.mp4 and its loudness, read from the file. */
export async function measureFinal(final, { ffmpeg, ffprobe }) {
  const probe = JSON.parse((await runTool(ffprobe,['-v','error','-show_streams','-show_format','-of','json',final])).stdout);
  const video = probe.streams.find(s=>s.codec_type==='video');
  const audio = probe.streams.find(s=>s.codec_type==='audio');
  const measured = await runTool(ffmpeg,['-hide_banner','-i',final,'-af','loudnorm=I=-14:TP=-1:LRA=11:print_format=json','-f','null','-']);
  return { video, audio, format: probe.format, loudness: loudnessResult(measured.stderr) };
}

/** Why a measured cut is not a Short of `frames` frames; empty when it is one. */
export function profileProblems({ video, audio }, frames) {
  const problems = [];
  if (video?.width !== PROFILE.width || video?.height !== PROFILE.height) problems.push(`the picture is ${video?.width}×${video?.height}, not ${PROFILE.width}×${PROFILE.height}`);
  if (video?.codec_name !== 'h264') problems.push(`the video codec is ${video?.codec_name}, not h264`);
  if (video?.r_frame_rate !== `${PROFILE.fps}/1`) problems.push(`the frame rate is ${video?.r_frame_rate}, not ${PROFILE.fps}`);
  if (Number(video?.nb_frames) !== frames) problems.push(`${video?.nb_frames} frames, the timeline has ${frames}`);
  if (audio?.codec_name !== 'aac' || audio?.sample_rate !== '48000') problems.push(`the audio is ${audio?.codec_name} at ${audio?.sample_rate} Hz, not aac at 48000`);
  const seconds = frames / PROFILE.fps;
  // Less than a frame apart: an AAC stream ends on its own block, a little past the last frame.
  if (!Number.isFinite(Number(audio?.duration)) || Math.abs(Number(audio.duration) - seconds) > .08) problems.push(`the audio runs ${audio?.duration}s against ${seconds.toFixed(3)}s of picture`);
  return problems;
}

/** Why a measured loudness is outside −14 ± 1 LUFS or above −0.8 dBTP; empty when inside. */
export function loudnessProblems(loudness) {
  const problems = [];
  if (Math.abs(Number(loudness.input_i) + 14) > 1) problems.push(`${loudness.input_i} LUFS is outside −14 ± 1`);
  if (Number(loudness.input_tp) > -.8) problems.push(`the true peak ${loudness.input_tp} dBTP is above −0.8`);
  return problems;
}

// Embed only the bundled subsets used by this production. No remote font requests.
export function embeddedFont(text) {
  const dir = fontDir('noto-sans-tc');
  const points = [...new Set([...text].map(c => c.codePointAt(0)))];
  return [...readFileSync(path.join(dir, 'index.css'), 'utf8').matchAll(/@font-face\s*\{[^}]+\}/g)]
    .map(match => match[0]).filter(block => points.some(p => covers(parseUnicodeRanges(block), p)))
    .map(block => block.replace(/url\(([^)]+)\)/g, (_all, url) => {
      const bytes = readFileSync(path.resolve(dir, url.replace(/['"]/g, '')));
      return `url(data:font/woff2;base64,${bytes.toString('base64')})`;
    })).join('\n');
}

async function measurePage(page) {
  return page.evaluate(() => {
    const problems = [];
    const content = document.querySelector('.content');
    const caption = document.querySelector('.caption');
    for (const el of [content, caption]) {
      if (el.scrollHeight > el.clientHeight + 2 || el.scrollWidth > el.clientWidth + 2) problems.push(`${el.className}: overflow`);
    }
    for (const el of content.querySelectorAll('h1,.row,.big,.note,img')) {
      const box = el.getBoundingClientRect();
      if (box.left < 78 || box.right > 902 || box.bottom > 1380) problems.push(`${el.tagName}: outside safe content area`);
    }
    if (caption.getBoundingClientRect().bottom > 1600) problems.push('caption outside safe area');
    for (const img of document.images) if (!img.complete || img.naturalWidth === 0) problems.push('image failed');
    return problems;
  });
}

/**
 * Draw what the segments are made of (motion.mjs): every phrase's card as a transparent PNG in
 * frames/ (the layout measured as before), the theme's backdrop once per scene of cards in
 * backdrops/, and each picture background as a file in assets/. Returns the layout report and the
 * background of every scene.
 */
async function renderFrames(doc, timeline, evidence, directory, channel) {
  const { chromium } = await import('@playwright/test');
  const browser = await chromium.launch({ ...(channel ? { channel } : {}), headless: true });
  const context = await browser.newContext({ viewport: { width: PROFILE.width, height: PROFILE.height }, deviceScaleFactor: 1, javaScriptEnabled: false });
  await context.route('**/*', route => route.abort());
  const page = await context.newPage();
  page.setDefaultTimeout(20000);
  const ready = async label => {
    let timer;
    try {
      await Promise.race([
        page.evaluate(() => document.fonts.ready.then(() => true)),
        new Promise((_resolve,reject)=>{timer=setTimeout(()=>reject(new Error(`${label}: fonts timed out`)),20000);}),
      ]);
    } finally { clearTimeout(timer); }
  };
  const assets = new Map();
  const assetFiles = new Map();
  const layout = [];
  const backgrounds = [];
  const fontCss = embeddedFont(JSON.stringify(doc) + evidence.filter(e=>e.file.endsWith('.html')).map(e=>e.bytes.toString('utf8')).join('') + themeText() + '0123456789');
  try {
    for (const item of evidence.filter(e => doc.scenes.some(s=>s.asset===e.path))) {
      let bytes;
      if (item.file.endsWith('.html')) {
        const html = item.bytes.toString('utf8');
        if (/<(?:script|iframe|object|embed)\b/i.test(html)) throw new Error(`active HTML not allowed: ${item.path}`);
        await page.setViewportSize({ width: 800, height: 1000 });
        console.error(`render asset: ${item.path}`);
        // addStyleTag can wait indefinitely with JavaScript disabled. Put the
        // local font override in the inert document before the initial parse.
        const style = `<style>${fontCss}\nbody{font-family:'Noto Sans TC Variable',sans-serif!important}</style>`;
        await page.setContent(html.replace(/<\/head>/i,`${style}</head>`));
        await ready(item.path);
        const assetProblems = await page.evaluate(() => {
          const problems = [];
          const walker = document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);
          while (walker.nextNode()) {
            const text = walker.currentNode;
            if (!text.textContent.trim() || text.parentElement.closest('style,script')) continue;
            const range=document.createRange();range.selectNodeContents(text);
            for(const box of range.getClientRects()) {
              if(box.width && (box.left<0 || box.top<0 || box.right>800.5 || box.bottom>1000.5)) problems.push(`text clipped: ${text.textContent.slice(0,40)}`);
              for(let parent=text.parentElement;parent;parent=parent.parentElement) {
                const style=getComputedStyle(parent), bounds=parent.getBoundingClientRect();
                const clipsX=['hidden','clip','scroll','auto'].includes(style.overflowX);
                const clipsY=['hidden','clip','scroll','auto'].includes(style.overflowY);
                if((clipsX && (box.left<bounds.left-.5 || box.right>bounds.right+.5)) || (clipsY && (box.top<bounds.top-.5 || box.bottom>bounds.bottom+.5))) problems.push(`ancestor clips text: ${text.textContent.slice(0,40)}`);
              }
            }
          }
          for (const img of document.images) if (!img.complete || !img.naturalWidth) problems.push('asset image failed');
          return problems;
        });
        if(assetProblems.length) throw new Error(`${item.path}: ${assetProblems.join('; ')}`);
        bytes = await page.screenshot({ type: 'png' });
      } else {
        if (!/\.(png|jpg|jpeg)$/i.test(item.file)) throw new Error(`unsupported image: ${item.path}`);
        bytes = item.bytes;
      }
      const file = path.join(directory, 'assets', `${item.sha256.slice(0,16)}.${/\.jpe?g$/i.test(item.file)?'jpg':'png'}`);
      writeFileSync(file, bytes);
      assets.set(item.path, `data:image/${file.endsWith('.jpg')?'jpeg':'png'};base64,${bytes.toString('base64')}`);
      assetFiles.set(item.path, file);
    }
    await page.setViewportSize({ width: PROFILE.width, height: PROFILE.height });
    mkdirSync(path.join(directory, 'backdrops'), { recursive: true });
    for (const [sceneIndex, scene] of doc.scenes.entries()) {
      const background = backgroundOf(scene);
      if (background === 'picture') {
        backgrounds.push({ scene: sceneIndex, background, file: assetFiles.get(scene.asset), camera: cameraOf(scene).name });
        continue;
      }
      // The theme's background and glow alone: the still that drifts under this scene's cards.
      await page.setContent(sceneHtml(doc, { sceneIndex, text: '' }, { backdrop: true }));
      const file = path.join(directory, 'backdrops', `${number(sceneIndex)}.png`);
      await page.screenshot({ path: file });
      backgrounds.push({ scene: sceneIndex, background, file, camera: cameraOf(scene).name });
    }
    for (const cue of timeline.cues) {
      if (stopRequested(directory)) throw new Error('STOP requested');
      const scene = doc.scenes[cue.sceneIndex];
      const picture = backgroundOf(scene) === 'picture';
      // A picture scene's card carries no image: the picture is the moving background under it.
      await page.setContent(sceneHtml(doc, cue, { fontCss, assetUrl: picture ? '' : (assets.get(scene.asset) ?? ''), transparent: true, picture }));
      await ready(`cue ${cue.index}`);
      const problems = await measurePage(page);
      layout.push({ cue: cue.index, problems });
      if (problems.length) throw new Error(`scene ${cue.sceneIndex}, cue ${cue.index}: ${problems.join('; ')}`);
      await page.screenshot({ path: path.join(directory, 'frames', `${number(cue.index)}.png`), omitBackground: true });
    }
    return { layout, backgrounds };
  } finally { await browser.close(); }
}

/** One representative frame from each scene's segment, readable in a compact contact sheet. */
async function contactSheet(doc, stills, directory, fontCss, channel) {
  const { chromium } = await import('@playwright/test');
  const browser = await chromium.launch({ ...(channel ? { channel } : {}), headless: true });
  try {
    const context = await browser.newContext({ viewport: { width: 1080, height: Math.ceil(stills.length / 3) * 690 }, deviceScaleFactor: 1, javaScriptEnabled: false });
    await context.route('**/*', route => route.abort());
    const page = await context.newPage();
    const sheet = stills.map((file, i) => `<figure><img src="data:image/png;base64,${readFileSync(file).toString('base64')}"><figcaption>${esc(doc.scenes[i].headline)}</figcaption></figure>`).join('');
    await page.setContent(`<style>${fontCss}body{margin:0;background:#152b31;color:white;font:22px 'Noto Sans TC Variable';display:grid;grid-template-columns:repeat(3,1fr);gap:12px;padding:16px}figure{margin:0}img{width:100%}figcaption{padding:8px}</style>${sheet}`);
    await page.evaluate(() => document.fonts.ready.then(() => true));
    await page.screenshot({ path: path.join(directory, 'contact-sheet.png'), fullPage: true });
  } finally { await browser.close(); }
}

/**
 * The sound a Short carries under its voice (docs/videos/SHORTS.md §工具端): the owner's licensed
 * music file and sound-effect set, found and checked as the long video's are (assemble/sound.mjs);
 * a Short generates neither. `{ track, music, sfx }`, nulls for a script naming none.
 */
async function shortSound(doc, base) {
  const found = doc.music ? await musicInputs(doc, base, base) : { track: null, music: null };
  if (found.problem) throw new Error(`the music bed cannot be carried: ${found.problem}`);
  const effects = doc.sfx ? await sfxInputs(doc, base) : { sfx: null };
  if (effects.problem) throw new Error(`the sound effects cannot be carried: ${effects.problem}`);
  return { track: found.track, music: found.music, sfx: effects.sfx };
}

// Whatever the source, a clip ends on the 48 kHz mono grid the timeline counts in.
async function normalizeClips(clips, directory, ffmpeg) {
  mkdirSync(path.join(directory,'source-audio'),{recursive:true});
  const wavs = [];
  for (const [i,bytes] of clips.entries()) {
    const input = path.join(directory,'source-audio',`${number(i)}.wav`);
    const output = path.join(directory,'audio',`${number(i)}.wav`);
    writeFileSync(input,bytes);
    await runTool(ffmpeg,['-y','-v','error','-i',input,'-ac','1','-ar','48000','-c:a','pcm_s16le',output]);
    const wav = parseWav(readFileSync(output));
    requireNarrationFormat(wav);
    if (!wav.samples.some(s=>Math.abs(s)>50)) throw new Error(`silent narration ${i}`);
    wavs.push(wav);
  }
  return wavs;
}

/**
 * Build a Short from its script. `speech` names where the narration comes from (server, windows,
 * files); `client` is the site, needed for the server's voice; `redo` is a finished build whose
 * check flagged phrases, which are synthesized again while the rest come from the cache.
 */
export async function build({ file, sourceBase, workdir, voice=WINDOWS_VOICE, channel=process.platform==='win32'?'msedge':undefined, audioDir, speech, client=null, redo=null, lexicon=null, synthesizeImpl }) {
  const documentBytes = readFileSync(file);
  const doc = JSON.parse(documentBytes);
  const errors = validate(doc);
  if (errors.length) throw new Error(errors.join('\n'));
  if (lineOf(doc) === 'drama') throw new Error('a vertical drama short is made by the drama pipeline; bring its cut in with `import`');
  const evidence = verifyEvidence(doc,sourceBase);
  const base = resolveWorkBase({flag:workdir,root:ROOT});
  let ancestor = base;
  while (!existsSync(ancestor)) ancestor = path.dirname(ancestor);
  if (isInside(path.resolve(realpathSync(ancestor),path.relative(ancestor,base)),realpathSync(ROOT))) throw new Error('output symlink points inside repository');
  const source = speech ?? (audioDir ? 'files' : defaultSource());
  // The voice and the length a Short may have are the owner's settings when the site is asked.
  const settings = source === 'server' && client ? await client.settings() : null;
  const range = settings ? { minSeconds: settings.seconds_min, maxSeconds: settings.seconds_max } : PROFILE;
  const narration = await narrate({ doc, source, workBase: base, voice: settings?.voice, client, audioDir, windowsVoice: voice, lexicon, redo: redo ? flaggedPhrases(path.join(redo,'check.json')) : [], synthesizeImpl });
  const codeHash = sha256(['build.mjs','core.mjs','layouts.mjs','motion.mjs','speech.mjs','speech.ps1'].map(f=>readFileSync(new URL(f,import.meta.url),'utf8')).join('\n') + MOTION_VERSION);
  const audioHash = sha256(narration.clips.map(bytes=>sha256(bytes)).join(''));
  // The bed and the effect set are part of what was built: another file under the same name is another cut.
  const sound = await shortSound(doc, base);
  const soundHash = sha256(JSON.stringify({ track: sound.track?.sha256 ?? null, sfx: sound.sfx ? sfxSetHash(doc, sound.sfx.manifest) : null }));
  const buildId = sha256(JSON.stringify({document:sha256(documentBytes),codeHash,source,voice:narration.voice,channel,audioHash,soundHash})).slice(0,16);
  // Every attempt is separate: a failed rerun must never leave an old successful manifest next to new bytes.
  const directory = path.join(base,doc.slug,`${buildId}-${Date.now()}`);
  if (stopRequested(path.join(base,doc.slug)) || stopRequested(directory)) throw new Error('STOP requested');
  for (const sub of ['audio','frames','clips','assets','upload','evidence','build']) mkdirSync(path.join(directory,sub),{recursive:true});
  // The script and its evidence travel with the build: the checks and the push read them from
  // here, so a script edited afterwards cannot stand in for the one that was filmed.
  writeFileSync(path.join(directory,SCRIPT_FILE),documentBytes);
  for (const item of evidence) {
    const copy = path.join(directory,'evidence',item.path);
    mkdirSync(path.dirname(copy),{recursive:true});
    copyFileSync(item.file,copy);
  }
  const {ffmpeg,ffprobe,version} = await locateFfmpeg();
  console.error(`${doc.slug}: measure narration (${source})`);
  const wavs = await normalizeClips(narration.clips,directory,ffmpeg);
  const timeline = buildTimeline(doc,wavs.map(w=>w.samples.length/w.sampleRate),range);
  const samples = new Int16Array(timeline.frames*1600);
  for (const cue of timeline.cues) samples.set(wavs[cue.index].samples,cue.startFrame*1600);
  writeFileSync(path.join(directory,'narration.wav'),encodeWav(samples));
  console.error(`${doc.slug}: render ${timeline.cues.length} caption cards (${timeline.seconds.toFixed(2)}s, ${themeOf(doc).id})`);
  const { layout, backgrounds } = await renderFrames(doc,timeline,evidence,directory,channel);
  // One segment per scene (motion.mjs): the background under its camera move, the phrases' cards
  // over it, a dissolve from the previous scene; the join copies, as before.
  console.error(`${doc.slug}: encode ${backgrounds.length} moving scenes`);
  const spans = sceneSpans(timeline);
  const motion = [];
  const stills = [];
  let dissolveFrom = null;
  for (const [index, span] of spans.entries()) {
    if (stopRequested(directory) || stopRequested(path.join(base,doc.slug))) throw new Error('STOP requested');
    const background = backgrounds[span.sceneIndex];
    const list = path.join(directory,'build',`cards-${number(span.sceneIndex)}.txt`);
    writeFileSync(list, cardsList(span.cues.map(cue => ({ file: path.join(directory,'frames',`${number(cue.index)}.png`), frames: cue.frames }))));
    const segment = path.join(directory,'clips',`${number(span.sceneIndex)}.mp4`);
    await runTool(ffmpeg, segmentArgs({ background: background.file, move: background.camera, frames: span.frames, cardsList: list, dissolveFrom, outFile: segment }));
    motion.push({ scene: span.sceneIndex, frames: span.frames, camera: background.camera, background: background.background, dissolve: dissolveFrom !== null });
    const still = path.join(directory,'build',`scene-${number(span.sceneIndex)}.png`);
    await runTool(ffmpeg, firstFrameArgs(segment, still));
    stills.push(still);
    if (index < spans.length - 1) {
      dissolveFrom = path.join(directory,'build',`last-${number(span.sceneIndex)}.png`);
      await runTool(ffmpeg, lastFrameArgs(segment, span.frames, dissolveFrom));
    }
  }
  const fontCss = embeddedFont(doc.scenes.map(scene => scene.headline).join(''));
  await contactSheet(doc, stills, directory, fontCss, channel);
  const listFile = path.join(directory,'clips.txt');
  writeFileSync(listFile,spans.map(span=>`file 'clips/${number(span.sceneIndex)}.mp4'`).join('\n'));
  const narrationFile = path.join(directory,'narration.wav');
  const audioFile = path.join(directory,'build','audio.m4a');
  const totalSeconds = timeline.frames / PROFILE.fps;
  // The sound effects (motion.mjs shortSfxPlan) on one track, then the mix: the bed ducked under
  // the voice and the effects over both, to -14 LUFS as the long video's cut; a Short naming
  // neither is loudnormed as before.
  let effects = [];
  let sfxFile = null;
  if (sound.sfx) {
    effects = shortSfxPlan(doc, timeline);
    const args = sfxTrackArgs(effects, sound.sfx.files, timeline.frames, sound.sfx.gain_db, path.join(directory,'build','sfx.wav'));
    if (args) {
      await runTool(ffmpeg, args);
      sfxFile = path.join(directory,'build','sfx.wav');
    }
  }
  let bed = null;
  if (sound.track || sfxFile) {
    const file = sound.track?.file ?? null;
    const measuredMix = parseLoudnorm((await runTool(ffmpeg, measureMixArgs(narrationFile, file, sound.music, totalSeconds, sfxFile))).stderr);
    await runTool(ffmpeg, mixArgs(narrationFile, file, sound.music, totalSeconds, measuredMix, audioFile, sfxFile, ['-c:a','aac','-b:a','192k']));
    if (file) {
      const bedLoudness = parseEbur128((await runTool(ffmpeg, bedLoudnessArgs(narrationFile, file, sound.music, totalSeconds))).stderr);
      bed = bedLevel(bedLoudness.integrated, measuredMix);
      const bedWrong = checkBed(bed);
      if (bedWrong.length) throw new Error(`the music bed failed: ${bedWrong.join('; ')}`);
    }
  } else {
    const loudness = await runTool(ffmpeg,['-hide_banner','-i',narrationFile,'-af','aformat=channel_layouts=stereo,loudnorm=I=-14:TP=-1:LRA=11:print_format=json','-f','null','-']);
    const loud = loudnessResult(loudness.stderr);
    const filter = `aformat=channel_layouts=stereo,loudnorm=I=-14:TP=-1:LRA=11:measured_I=${loud.input_i}:measured_TP=${loud.input_tp}:measured_LRA=${loud.input_lra}:measured_thresh=${loud.input_thresh}:offset=${loud.target_offset}:linear=true:print_format=json`;
    await runTool(ffmpeg,['-y','-hide_banner','-i',narrationFile,'-af',filter,'-ar','48000','-ac','2','-c:a','aac','-b:a','192k',audioFile]);
  }
  const final = path.join(directory,'upload','final.mp4');
  await runTool(ffmpeg,['-y','-hide_banner','-f','concat','-safe','1','-i',listFile,'-i',audioFile,'-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','copy','-movflags','+faststart',final]);
  const measured = await measureFinal(final,{ffmpeg,ffprobe});
  const wrong = profileProblems(measured,timeline.frames);
  if (wrong.length) throw new Error(`encoded output failed profile/duration checks: ${wrong.join('; ')}`);
  const loudWrong = loudnessProblems(measured.loudness);
  if (loudWrong.length) throw new Error(`final loudness failed: ${loudWrong.join('; ')}`);
  const {video,audio} = measured;
  writeFileSync(path.join(directory,'upload','zh-TW.srt'),srt(timeline));
  // The cover is the first frame as the viewer sees it: the card over its background, not the transparent card alone.
  writeFileSync(path.join(directory,'upload','cover.png'),readFileSync(stills[0]));
  saveJson(path.join(directory,'upload','titles.json'),doc.titles);
  saveJson(path.join(directory,'timeline.json'),timeline);
  saveJson(path.join(directory,'checks.json'),{ok:true,profile:PROFILE,range,seconds:timeline.seconds,frames:timeline.frames,layout,motion,music:sound.track?{track:doc.music.track,sha256:sound.track.sha256,bed_lufs:bed}:null,sfx:sound.sfx?{set:doc.sfx.set,events:effects.length}:null,loudness:measured.loudness,video:{codec:video.codec_name,width:video.width,height:video.height,fps:video.r_frame_rate},audio:{codec:audio.codec_name,sample_rate:audio.sample_rate},evidence_verified:true,audio_sha256:sha256(wavs.map((_w,i)=>sha256(readFileSync(path.join(directory,'audio',`${number(i)}.wav`)))).join('')),final_sha256:sha256(readFileSync(final)),checked_at:new Date().toISOString()});
  // What the site's ledger is told when the final cut is approved: /video/speech takes no slug,
  // so only the tool knows which Short the narration was for (docs/videos/SHORTS.md §花費與預算).
  saveJson(path.join(directory,USAGE_FILE),{narration:{seconds:Number(wavs.reduce((sum,w)=>sum+w.samples.length/w.sampleRate,0).toFixed(3)),characters:phrasesOf(doc).reduce((sum,phrase)=>sum+[...phrase].length,0),calls:narration.calls,provider:narration.provider,...(narration.model?{model:narration.model}:{})},stages:{},checks:{}});
  const uploadFiles = ['final.mp4','zh-TW.srt','cover.png','titles.json'];
  const manifest = {schema_version:2,slug:doc.slug,line:lineOf(doc),series:doc.series,build_id:buildId,status:'built',created_at:new Date().toISOString(),document_sha256:sha256(documentBytes),code_sha256:codeHash,ffmpeg:version,narrator:{source,provider:narration.provider,voice:narration.voice},evidence:evidence.map(({file:_file,bytes:_bytes,...e})=>e),files:uploadFiles.map(name=>({name,sha256:sha256(readFileSync(path.join(directory,'upload',name)))}))};
  saveJson(path.join(directory,'upload','manifest.json'),manifest);
  return {directory,final,seconds:timeline.seconds,buildId,status:manifest.status,narration:{source,calls:narration.calls}};
}
