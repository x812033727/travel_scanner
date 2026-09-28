import { execFile } from 'node:child_process';
import { existsSync, mkdirSync, readFileSync, realpathSync, writeFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { promisify } from 'node:util';
import { fontDir, parseUnicodeRanges, covers } from '../render/fonts.mjs';
import { locateFfmpeg, runTool } from '../assemble/ffmpeg.mjs';
import { encodeWav, parseWav, requireNarrationFormat } from '../tts/wav.mjs';
import { ROOT, isInside, resolveWorkBase, stopRequested } from '../core/paths.mjs';
import { EPISODE_SERIES, PROFILE, SERIES_BRAND, buildTimeline, esc, sceneHtml, sha256, srt, validate, verifyEvidence } from './core.mjs';

const exec = promisify(execFile);
const HERE = path.dirname(fileURLToPath(import.meta.url));
const saveJson = (file, data) => writeFileSync(file, JSON.stringify(data, null, 2) + '\n');
const number = i => String(i).padStart(3, '0');
export function loudnessResult(stderr) {
  const blocks = [...stderr.matchAll(/\{\s*"input_i"[\s\S]*?\}/g)];
  if (!blocks.length) throw new Error('ffmpeg did not report loudness');
  const data = JSON.parse(blocks.at(-1)[0]);
  if (!['input_i','input_tp','input_lra','input_thresh','target_offset'].every(k=>Number.isFinite(Number(data[k])))) throw new Error('invalid loudness measurement (silent or corrupt audio)');
  return data;
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
  const layout = [];
  const fontCss = embeddedFont(JSON.stringify(doc) + evidence.filter(e=>e.file.endsWith('.html')).map(e=>e.bytes.toString('utf8')).join('') + JSON.stringify(SERIES_BRAND) + '0123456789');
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
    }
    await page.setViewportSize({ width: PROFILE.width, height: PROFILE.height });
    for (const cue of timeline.cues) {
      if (stopRequested(directory)) throw new Error('STOP requested');
      const scene = doc.scenes[cue.sceneIndex];
      await page.setContent(sceneHtml(doc, cue, { fontCss, assetUrl: assets.get(scene.asset) ?? '' }));
      await ready(`cue ${cue.index}`);
      const problems = await measurePage(page);
      layout.push({ cue: cue.index, problems });
      if (problems.length) throw new Error(`scene ${cue.sceneIndex}, cue ${cue.index}: ${problems.join('; ')}`);
      await page.screenshot({ path: path.join(directory, 'frames', `${number(cue.index)}.png`) });
    }
    // One representative cue from each scene, readable in a compact contact sheet.
    const representatives = doc.scenes.map((_s, i) => timeline.cues.find(c => c.sceneIndex === i));
    const sheet = representatives.map(c => `<figure><img src="data:image/png;base64,${readFileSync(path.join(directory,'frames',`${number(c.index)}.png`)).toString('base64')}"><figcaption>${esc(doc.scenes[c.sceneIndex].headline)}</figcaption></figure>`).join('');
    await page.setViewportSize({ width: 1080, height: Math.ceil(representatives.length / 3) * 690 });
    await page.setContent(`<style>${fontCss}body{margin:0;background:#152b31;color:white;font:22px 'Noto Sans TC Variable';display:grid;grid-template-columns:repeat(3,1fr);gap:12px;padding:16px}figure{margin:0}img{width:100%}figcaption{padding:8px}</style>${sheet}`);
    await ready('contact sheet');
    await page.screenshot({ path: path.join(directory, 'contact-sheet.png'), fullPage: true });
    return layout;
  } finally { await browser.close(); }
}

async function speech(doc, directory, voice, ffmpeg, externalAudio) {
  const phrases = doc.scenes.flatMap(s=>s.narration);
  const speechKey = sha256(JSON.stringify({phrases, voice, rate:1, speechScript:readFileSync(path.join(HERE,'speech.ps1'),'utf8')}));
  const cache = path.join(path.dirname(directory), '.speech', speechKey.slice(0,16));
  mkdirSync(cache, { recursive:true });
  if (externalAudio) {
    mkdirSync(path.join(directory,'external-audio'),{recursive:true});
    for(const [i,bytes] of externalAudio.entries()) writeFileSync(path.join(directory,'external-audio',`${number(i)}.wav`),bytes);
  } else if (!existsSync(path.join(cache,'complete.json'))) {
    if (process.platform !== 'win32') throw new Error('supply --audio-dir with measured per-phrase WAVs, or run the Windows local narrator');
    writeFileSync(path.join(cache,'phrases.json'), JSON.stringify(phrases));
    await exec('powershell.exe', ['-NoProfile','-NonInteractive','-ExecutionPolicy','Bypass','-File',path.join(HERE,'speech.ps1'),'-InputJson',path.join(cache,'phrases.json'),'-OutputDirectory',cache,'-Voice',voice], { windowsHide:true, maxBuffer:1024*1024 });
    saveJson(path.join(cache,'complete.json'),{voice,rate:1,phrases:phrases.length,provider:'Windows installed speech',incremental_api_cost_ntd:0});
  }
  const wavs = [];
  for (const [i] of phrases.entries()) {
    const input = path.join(externalAudio ? path.join(directory,'external-audio') : cache,`${number(i)}.wav`);
    const output = path.join(directory,'audio',`${number(i)}.wav`);
    await runTool(ffmpeg,['-y','-v','error','-i',input,'-ac','1','-ar','48000','-c:a','pcm_s16le',output]);
    const wav = parseWav(readFileSync(output));
    requireNarrationFormat(wav);
    if (!wav.samples.some(s=>Math.abs(s)>50)) throw new Error(`silent narration ${i}`);
    wavs.push(wav);
  }
  return wavs;
}

/**
 * Build one Short. `document` (with `file` unset) is a script already resolved in memory, such
 * as an episode's Short with its shots turned into keyframe evidence; `wavs` are its phrases'
 * WAVs already synthesized (the channel voice), `narrator` how the manifest names them, and
 * `longVideoId` the long episode's YouTube id for the description.
 */
export async function build({ file, document, sourceBase, workdir, voice='Microsoft Hanhan Desktop', channel=process.platform==='win32'?'msedge':undefined, audioDir, wavs: givenWavs, narrator, longVideoId }) {
  const documentBytes = document ? Buffer.from(JSON.stringify(document)) : readFileSync(file);
  const doc = document ?? JSON.parse(documentBytes);
  const errors = validate(doc);
  if (errors.length) throw new Error(errors.join('\n'));
  const evidence = verifyEvidence(doc,sourceBase);
  const base = resolveWorkBase({flag:workdir,root:ROOT});
  let ancestor = base;
  while (!existsSync(ancestor)) ancestor = path.dirname(ancestor);
  if (isInside(path.resolve(realpathSync(ancestor),path.relative(ancestor,base)),realpathSync(ROOT))) throw new Error('output symlink points inside repository');
  const codeHash = sha256(['build.mjs','core.mjs','speech.ps1'].map(f=>readFileSync(path.join(HERE,f),'utf8')).join('\n'));
  const externalAudio = givenWavs ?? (audioDir ? doc.scenes.flatMap(s=>s.narration).map((_s,i)=>readFileSync(path.join(audioDir,`${number(i)}.wav`))) : null);
  if (externalAudio && externalAudio.length !== doc.scenes.flatMap(s=>s.narration).length) throw new Error('one WAV per narration phrase required');
  const external = Boolean(externalAudio);
  const narratorLabel = narrator ?? (external ? 'external' : voice);
  const audioHash = externalAudio ? sha256(externalAudio.map(bytes=>sha256(bytes)).join('')) : null;
  const buildId = sha256(JSON.stringify({document:sha256(documentBytes),codeHash,voice,channel,audioHash})).slice(0,16);
  // Every attempt is separate: a failed rerun must never leave an old successful manifest next to new bytes.
  const directory = path.join(base,doc.slug,`${buildId}-${Date.now()}`);
  if (stopRequested(path.join(base,doc.slug)) || stopRequested(directory)) throw new Error('STOP requested');
  for (const sub of ['audio','frames','clips','assets','upload']) mkdirSync(path.join(directory,sub),{recursive:true});
  const {ffmpeg,ffprobe,version} = await locateFfmpeg();
  console.error(`${doc.slug}: synthesize/measure narration`);
  const wavs = await speech(doc,directory,voice,ffmpeg,externalAudio);
  const timeline = buildTimeline(doc,wavs.map(w=>w.samples.length/w.sampleRate));
  const samples = new Int16Array(timeline.frames*1600);
  for (const cue of timeline.cues) samples.set(wavs[cue.index].samples,cue.startFrame*1600);
  writeFileSync(path.join(directory,'narration.wav'),encodeWav(samples));
  console.error(`${doc.slug}: render ${timeline.cues.length} caption frames (${timeline.seconds.toFixed(2)}s)`);
  const layout = await renderFrames(doc,timeline,evidence,directory,channel);
  console.error(`${doc.slug}: encode portrait video`);
  for (const cue of timeline.cues) {
    if (stopRequested(directory) || stopRequested(path.join(base,doc.slug))) throw new Error('STOP requested');
    await runTool(ffmpeg,['-y','-v','error','-loop','1','-framerate','30','-i',path.join(directory,'frames',`${number(cue.index)}.png`),'-frames:v',String(cue.frames),'-an','-c:v','libx264','-threads','2','-preset','fast','-tune','stillimage','-crf','20','-profile:v','high','-pix_fmt','yuv420p','-g','60','-keyint_min','60','-sc_threshold','0','-flags','+cgop','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709',path.join(directory,'clips',`${number(cue.index)}.mp4`)]);
  }
  const listFile = path.join(directory,'clips.txt');
  writeFileSync(listFile,timeline.cues.map(c=>`file 'clips/${number(c.index)}.mp4'`).join('\n'));
  const loudness = await runTool(ffmpeg,['-hide_banner','-i',path.join(directory,'narration.wav'),'-af','aformat=channel_layouts=stereo,loudnorm=I=-14:TP=-1:LRA=11:print_format=json','-f','null','-']);
  const loud = loudnessResult(loudness.stderr);
  const filter = `aformat=channel_layouts=stereo,loudnorm=I=-14:TP=-1:LRA=11:measured_I=${loud.input_i}:measured_TP=${loud.input_tp}:measured_LRA=${loud.input_lra}:measured_thresh=${loud.input_thresh}:offset=${loud.target_offset}:linear=true:print_format=json`;
  const final = path.join(directory,'upload','final.mp4');
  await runTool(ffmpeg,['-y','-hide_banner','-f','concat','-safe','1','-i',listFile,'-i',path.join(directory,'narration.wav'),'-map','0:v:0','-map','1:a:0','-c:v','copy','-af',filter,'-ar','48000','-ac','2','-c:a','aac','-b:a','192k','-movflags','+faststart',final]);
  const probe = JSON.parse((await runTool(ffprobe,['-v','error','-show_streams','-show_format','-of','json',final])).stdout);
  const video = probe.streams.find(s=>s.codec_type==='video');
  const audio = probe.streams.find(s=>s.codec_type==='audio');
  if (video?.width!==1080 || video?.height!==1920 || video?.codec_name!=='h264' || video?.r_frame_rate!=='30/1' || Number(video.nb_frames)!==timeline.frames || audio?.codec_name!=='aac' || audio?.sample_rate!=='48000' || !Number.isFinite(Number(audio?.duration)) || Math.abs(Number(audio.duration)-timeline.seconds)>.08) throw new Error('encoded output failed profile/duration checks');
  const measured = await runTool(ffmpeg,['-hide_banner','-i',final,'-af','loudnorm=I=-14:TP=-1:LRA=11:print_format=json','-f','null','-']);
  const finalLoud = loudnessResult(measured.stderr);
  if (Math.abs(Number(finalLoud.input_i)+14)>1 || Number(finalLoud.input_tp)>-.8) throw new Error(`final loudness failed: ${finalLoud.input_i} LUFS, ${finalLoud.input_tp} dBTP`);
  writeFileSync(path.join(directory,'upload','zh-TW.srt'),srt(timeline));
  writeFileSync(path.join(directory,'upload','cover.png'),readFileSync(path.join(directory,'frames','000.png')));
  const episode = doc.series === EPISODE_SERIES;
  const narration = narrator ? `${narrator}（需聽審）` : external ? '外部提供旁白（需聽審）' : `${voice} 本機合成（試片）`;
  const longLink = longVideoId ? `https://youtu.be/${longVideoId}` : null;
  const description = episode
    ? `完整版：${longLink ?? '長片上架後補上連結'}\n\n${doc.titles[0]}\n\n${doc.description}\n\n#原來如此事務所 #為什麼 #Shorts\n`
    : `${doc.titles[0]}\n\n${doc.description}\n\n實測範圍：${doc.experiment_summary}\n限制：${doc.limitations}\n旁白：${narration}\n\n#AI #實測 #Shorts\n`;
  writeFileSync(path.join(directory,'upload','description.zh-TW.txt'),description);
  saveJson(path.join(directory,'upload','titles.json'),doc.titles);
  saveJson(path.join(directory,'timeline.json'),timeline);
  saveJson(path.join(directory,'checks.json'),{ok:true,profile:PROFILE,seconds:timeline.seconds,frames:timeline.frames,layout,loudness:finalLoud,video:{codec:video.codec_name,width:video.width,height:video.height,fps:video.r_frame_rate},audio:{codec:audio.codec_name,sample_rate:audio.sample_rate},evidence_verified:true,checked_at:new Date().toISOString()});
  const uploadFiles = ['final.mp4','zh-TW.srt','cover.png','description.zh-TW.txt','titles.json'];
  const manifest = {schema_version:1,slug:doc.slug,build_id:buildId,status:'owner-review-required',created_at:new Date().toISOString(),document_sha256:sha256(documentBytes),code_sha256:codeHash,ffmpeg:version,narrator:narratorLabel,incremental_api_cost_ntd:external?null:0,...(episode?{episode:doc.episode,long_video_id:longVideoId??null}:{}),evidence:evidence.map(({file:_file,bytes:_bytes,...e})=>e),files:uploadFiles.map(name=>({name,sha256:sha256(readFileSync(path.join(directory,'upload',name)))}))};
  saveJson(path.join(directory,'upload','manifest.json'),manifest);
  const episodeSteps = episode ? `\n長片：${doc.episode}。${longLink ? `說明欄第一行已連到 ${longLink}；上傳後在 Studio 的「相關影片」也選這支長片。` : '長片還沒有 YouTube id：長片上架後把說明欄第一行換成它的網址，並在「相關影片」選它，再公開這支 Short。'}\n` : '';
  writeFileSync(path.join(directory,'upload','UPLOAD.md'),`# ${doc.titles[0]}\n\n狀態：試片完成，待站主審片。尚未上傳、發布或排程。\n${episodeSteps}\n1. 播放 final.mp4，核對台灣中文旁白、字幕、每次揭曉和手機介面遮擋。\n2. 使用 titles.json 的標題與 description.zh-TW.txt；在 Studio 上傳成私人。\n3. 上傳 zh-TW.srt，使用 cover.png 作封面參考。Shorts 封面能否選取，以手機版 Studio／YouTube 的實際介面為準。\n4. 由站主決定合成內容揭露、兒童與付費宣傳欄位、公開時間。${episode ? '畫面是長片的 AI 生成插圖，要勾合成內容揭露。' : '影片為工具測試與原創圖形，海報活動為虛構。'}\n5. 公開後記錄影片 ID 和時間，24h／72h／7d 匯出 Studio 指標。\n\n${doc.limitations ?? ''}\n\nSHA-256 見 manifest.json。技術檢查通過不等於真人聽審或發布成功。\n`);
  return {directory,final,seconds:timeline.seconds,buildId,status:manifest.status};
}
