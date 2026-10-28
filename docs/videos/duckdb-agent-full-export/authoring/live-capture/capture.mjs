// PREP only until Root supplies the separate exact local dispatch record.
import fs from 'node:fs';
import path from 'node:path';
import http from 'node:http';
import {createHash} from 'node:crypto';
import {execFile,execFileSync} from 'node:child_process';
import {fileURLToPath,pathToFileURL} from 'node:url';
import {isDeepStrictEqual} from 'node:util';

const B='/workspace/work/ai-tech-next/duckdb-live-capture-20261027';
const HERE=B+'/prepare',SELF=fileURLToPath(import.meta.url),PROFILE=HERE+'/capture-plan.json';
const R='/workspace/work/travel-scanner-duckdb',E=R+'/docs/videos/duckdb-agent-full-export';
const W='/workspace/work/videos/duckdb-agent-full-export';
const D='/workspace/work/videos/_duckdb-live-capture/duckdb-agent-full-export';
const RUN=B+'/capture-once',BASE=B+'/ROOT-before-inputs.json';
const HEAD='91cf8114334de5c76f49e5ea8a0d02e3a32ffa1d';
const SOURCE='1c475c928a02a6f584dd224ecfed1c5fafd53aa4bf1795c7a3758699692a12c8';
const SCRIPT='7aac2017419c82a4b81fb40050f067c9e021312600e5d66ec70846b58946107b';
const sha=b=>createHash('sha256').update(b).digest('hex');
const check=(v,s)=>{if(!v)throw Error(s);};
const read=p=>JSON.parse(fs.readFileSync(p,'utf8'));
const desc=p=>{check(fs.lstatSync(p).isFile(),'Ordinary file required: '+p);const b=fs.readFileSync(p);return{file:p,bytes:b.length,sha256:sha(b)};};
const bind=d=>{const a=desc(d.file);check(a.bytes===d.bytes&&a.sha256===d.sha256,'Pinned bytes changed: '+d.file);return fs.readFileSync(d.file);};
const write=(p,x)=>{check(p.startsWith(B+'/')||p.startsWith(D+'/'),'Output escapes capture');fs.writeFileSync(p,Buffer.isBuffer(x)?x:typeof x==='string'?x:JSON.stringify(x,null,2)+'\n',{flag:'wx',mode:0o600});};
const walk=(root,dir=root)=>fs.readdirSync(dir,{withFileTypes:true}).flatMap(x=>{const p=path.join(dir,x.name);check(!x.isSymbolicLink(),'Protected tree symlink');return x.isDirectory()?walk(root,p):[path.relative(root,p)];}).sort();
const pause=ms=>new Promise(resolve=>setTimeout(resolve,ms));
check(process.execArgv.includes('--use-env-proxy'),'Run Node with --use-env-proxy');
check(process.env.PLAYWRIGHT_BROWSERS_PATH==='/workspace/work/playwright','Use the existing installed Playwright browser/encoder directory');
check(process.argv.length===3&&process.argv[2]==='execute','Root-only execute mode requires separate release');
check(SELF===HERE+'/capture.mjs','Fixed helper path required');
check(new Date().toISOString().slice(0,10)==='2026-10-27','Recording date label requires a fresh dated preparation');
const profile=read(PROFILE),base=read(BASE),release=read(B+'/root-capture-release.json');
check(desc(BASE).sha256==='e56fe24dfb06120587fa9896be882de397bd2243ccdaf19b62fcfca3439164f6','Root baseline changed');
check(execFileSync('git',['rev-parse','HEAD'],{cwd:R,encoding:'utf8'}).trim()===HEAD,'HEAD changed');
for(const d of profile.pins)bind(d);
check(profile.steps.length===6&&profile.source_sha256===SOURCE&&profile.script_sha256===SCRIPT,'Fixed six original steps required');
check(release.kind==='ROOT_local_DuckDB_live_capture_dispatch'&&release.owner==='/root'&&release.no_TTS_ASR_or_paid===true&&release.no_external_network===true&&release.max_cli_commands===6&&release.max_capture_seconds===120,'Separate local capture scope required');
check(release.helper?.sha256===desc(SELF).sha256&&release.plan?.sha256===desc(PROFILE).sha256&&release.baseline?.sha256===desc(BASE).sha256,'Root release must bind exact helper, plan and baseline');
for(const k of ['helper','plan','baseline','task_claim','static_review'])bind(release[k]);
check(release.helper.file===SELF&&release.plan.file===PROFILE&&release.baseline.file===BASE,'Wrong scoped paths');
const issued=Date.parse(release.issued_at_utc),expires=Date.parse(release.expires_at_utc);
check(issued<=Date.now()&&expires>Date.now()&&expires-issued<=1800000,'Capture admission expired or exceeds30min');
const task=fs.readFileSync(release.task_claim.file,'utf8');
check(/^status:\s*in-progress\s*$/m.test(task)&&/^owner:\s*codex-duckdb-20261025\s*$/m.test(task),'Own task must be normally claimed');
function stopped(){for(const p of [W+'/STOP','/workspace/work/videos/STOP',D+'/STOP',B+'/STOP'])check(!fs.existsSync(p),'STOP present');}
function original({ownLease=false}={}){
 for(const [root,rows]of[[E,base.E],[W,base.W]]){const files=walk(root).filter(p=>!(ownLease&&root===W&&p==='LEASE'));check(isDeepStrictEqual(files,rows.map(x=>x.file).sort()),'Protected file set changed');for(const x of rows){const a=desc(path.join(root,x.file));check(a.bytes===x.bytes&&a.sha256===x.sha256,'Protected file changed: '+x.file);}}
 for(const d of base.held)bind(d);
}
stopped();check(!fs.existsSync(W+'/LEASE'),'Existing project producer; no takeover');
check(!fs.existsSync(RUN)&&!fs.existsSync(D),'Capture marker/output exists; no replay or overwrite');
original();
const {acquireProjectLease}=await import(pathToFileURL(R+'/tools/video/core/project-lease.mjs'));
const lease=acquireProjectLease(W,{owner:'root-DuckDB-live-local-console-capture',io:{rename(){throw Error('Lease takeover forbidden');}}});
const critical=()=>{lease.verify();stopped();check(Date.now()<expires,'Capture scope expired');bind(release.helper);bind(release.plan);for(const d of base.held)bind(d);check(desc(E+'/video.json').sha256===SOURCE,'Source changed');};
let server=null,browser=null,context=null,error=null,manifest=null,started=null,recordingStarted=null;
let next=0,busy=false;const runs=[],children={},events=[],requests=[];let blockedExternal=0,video=null;
function event(kind,extra={}){events.push({at:new Date().toISOString(),kind,...extra});}
async function child(executable,args,{cwd=D,prefix,timeout=30000}={}){
 critical();const began=new Date().toISOString();
 return await new Promise(resolve=>{execFile(executable,args,{cwd,encoding:'buffer',maxBuffer:2*1024*1024,timeout},(err,stdout,stderr)=>{
  const out=Buffer.isBuffer(stdout)?stdout:Buffer.from(stdout??''),bad=Buffer.isBuffer(stderr)?stderr:Buffer.from(stderr??'');
  const result={executable,argv:args,cwd,started_at:began,finished_at:new Date().toISOString(),actual_exit:err?(Number.isInteger(err.code)?err.code:null):0,signal:err?.signal??null};
  try{critical();write(prefix+'.stdout',out);write(prefix+'.stderr',bad);write(prefix+'.result.json',result);result.stdout=desc(prefix+'.stdout');result.stderr=desc(prefix+'.stderr');resolve({result,out,bad});}catch(e){resolve({result:{...result,actual_exit:null,write_error:e.message},out,bad});}
 });});
}
function csvRows(file){return fs.readFileSync(file,'utf8').trim().split(/\r?\n/).length-1;}
try{
 critical();fs.mkdirSync(RUN,{mode:0o700});fs.mkdirSync(D,{recursive:true,mode:0o700});
 fs.mkdirSync(D+'/runtime/demo/input',{recursive:true});fs.mkdirSync(D+'/runtime/demo/output',{recursive:true});fs.mkdirSync(D+'/logs');fs.mkdirSync(D+'/screens');fs.mkdirSync(D+'/raw');
 started=new Date().toISOString();write(RUN+'/started.json',{at:started,pid:process.pid,helper:desc(SELF),plan:desc(PROFILE),root_dispatch:desc(B+'/root-capture-release.json'),source_sha256:SOURCE});
 for(const d of profile.inputs){critical();const target=D+'/runtime/'+d.relative;fs.mkdirSync(path.dirname(target),{recursive:true});fs.writeFileSync(target,bind(d),{flag:'wx',mode:0o600});}
 fs.symlinkSync(profile.binary.file,D+'/runtime/duckdb');
 const html=bind(profile.pins.find(x=>x.file===HERE+'/console.html'));
 const fonts={tc:profile.fonts.tc,mono:profile.fonts.mono};
 server=http.createServer(async(req,res)=>{
  const stamp={at:new Date().toISOString(),method:req.method,path:req.url};requests.push(stamp);
  try{
   critical();check(req.socket.remoteAddress==='127.0.0.1','Only loopback client');
   if(req.method==='GET'&&req.url==='/'){res.writeHead(200,{'Content-Type':'text/html;charset=utf-8'});res.end(html);return;}
   if(req.method==='GET'&&/^\/font\/(tc|mono)\/[a-zA-Z0-9_./-]+$/.test(req.url)){
    const [,font,rel]=/^\/font\/(tc|mono)\/(.+)$/.exec(req.url),root=fonts[font],file=path.resolve(root,rel);check(file.startsWith(root+'/')&&fs.realpathSync(file)===file&&/\.(css|woff2)$/.test(file),'Font path refused');res.writeHead(200,{'Content-Type':file.endsWith('.css')?'text/css':'font/woff2'});res.end(fs.readFileSync(file));return;
   }
   if(req.method==='GET'&&req.url==='/favicon.ico'){res.writeHead(204);res.end();return;}
   check(req.method==='POST'&&req.url==='/run'&&!busy&&next<6,'Only next fixed CLI step allowed');
   let raw='';for await(const chunk of req){raw+=chunk;check(raw.length<=512,'Request too large');}
   const body=JSON.parse(raw),step=profile.steps[next];check(body.step===next&&body.display===step.display,'Displayed command/order differs from fixed actual argv');
   check(recordingStarted!==null&&Date.now()-recordingStarted<=120000,'Record must be active within120s before commands');busy=true;
   event('CLI_start',{index:next,display:step.display});
   bind(profile.binary);const q=await child(D+'/runtime/duckdb',step.args,{cwd:D+'/runtime',prefix:D+'/logs/step-'+next,timeout:15000});
   const row={index:next,title:step.title,display:step.display,...q.result};runs.push(row);children['duckdb_'+next]=q.result.actual_exit;
   check(q.result.actual_exit===0,'Actual CLI failed at step '+next);let metrics={inputRows:csvRows(D+'/runtime/demo/input/parcels.csv')};
   if(next===2){check(q.out.toString('utf8').includes('1160 rows omitted')&&q.out.toString('utf8').includes('first 20 and last 20 of 1200 rows'),'Actual agent preview differs');metrics.previewRows='40 / 1,200';}
   if(next>=3)metrics.strictRows=csvRows(D+'/runtime/demo/output/late-followup.csv');
   if(next===5)metrics.inclusiveRows=csvRows(D+'/runtime/demo/output/due-or-late.csv');
   let generated_file=null;
   if(next===4){const file=D+'/runtime/demo/output/parquet-readback.csv';check(fs.readFileSync(file).equals(fs.readFileSync(D+'/runtime/demo/output/late-followup.csv')),'Current Parquet roundtrip differs');generated_file={file:'demo/output/parquet-readback.csv',rows:csvRows(file),bytes:fs.statSync(file).size};row.generated_file={...generated_file,artifact:desc(file),equals_strict_csv:true};}
   row.metrics=metrics;event('CLI_end',{index:next,actual_exit:0});next++;busy=false;
   res.writeHead(200,{'Content-Type':'application/json'});res.end(JSON.stringify({step:next-1,actual_exit:0,stdout:q.out.toString('utf8'),metrics,generated_file}));return;
  }catch(e){busy=false;event('HTTP_error',{message:e.message});res.writeHead(400,{'Content-Type':'application/json'});res.end(JSON.stringify({error:e.message,actual_exit:null}));}
 });
 await new Promise((resolve,reject)=>{server.once('error',reject);server.listen(0,'127.0.0.1',resolve);});
 const origin='http://127.0.0.1:'+server.address().port;
 const {chromium}=await import(pathToFileURL(profile.playwright.file));
 browser=await chromium.launch({executablePath:profile.browser.file,headless:true,args:['--disable-gpu','--disable-threaded-animation']});
 context=await browser.newContext({viewport:{width:1920,height:1080},deviceScaleFactor:1,recordVideo:{dir:D+'/raw',size:{width:1920,height:1080}}});
 await context.route('**/*',route=>{const url=new URL(route.request().url());if(url.origin===origin)return route.continue();blockedExternal++;return route.abort();});
 const page=await context.newPage();video=page.video();recordingStarted=Date.now();event('recording_started');
 await page.goto(origin,{waitUntil:'networkidle'});await page.evaluate(async()=>{await document.fonts.load('24px "Noto Sans TC Variable"','完整資料操作預覽錄影');await document.fonts.load('24px "JetBrains Mono Variable"','SELECT 480');await document.fonts.ready;});
 check(await page.evaluate(()=>document.fonts.check('24px "Noto Sans TC Variable"','完整資料操作預覽錄影')&&document.fonts.check('24px "JetBrains Mono Variable"','SELECT 480')),'Bundled fonts not loaded');
 await page.screenshot({path:D+'/screens/00-ready.png'});await pause(5000);
 for(let i=0;i<6;i++){
  critical();const step=profile.steps[i];await page.evaluate(({i,step})=>window.setStep(i,step.title,step.note),{i,step});
  await page.locator('#command').pressSequentially(step.display,{delay:22});event('displayed_command_ready',{index:i});
  await page.locator('#command').press('Enter');await page.waitForFunction(()=>window.lastResult!==null||window.lastError!==null,null,{timeout:20000});
  check(await page.evaluate(()=>window.lastError)===null,'Console reported command failure');
  check(await page.locator('#output').textContent()===fs.readFileSync(D+'/logs/step-'+i+'.stdout','utf8'),'Rendered stdout differs from actual current CLI stdout');
  const geometry=await page.evaluate(()=>({bodyWidth:document.body.scrollWidth,viewport:innerWidth,command:document.querySelector('#command').scrollWidth,commandWidth:document.querySelector('#command').clientWidth,terminal:document.querySelector('#output').scrollWidth,terminalWidth:document.querySelector('#output').clientWidth}));
  check(geometry.bodyWidth<=geometry.viewport&&geometry.command<=geometry.commandWidth&&geometry.terminal<=geometry.terminalWidth,'Live console horizontal text overflow');
  runs[i].rendered_stdout_equal=true;runs[i].layout=geometry;
  await page.screenshot({path:D+'/screens/'+String(i+1).padStart(2,'0')+'-result.png'});
  await pause(step.hold_ms);
  if(i===1||i===2){await page.locator('#output').evaluate((el,isAgent)=>el.scrollTo({top:isAgent?15*31:el.scrollHeight,behavior:'smooth'}),i===2);await pause(3500);await page.screenshot({path:D+'/screens/'+String(i+1).padStart(2,'0')+'-scrolled.png'});}
 }
 await page.evaluate(()=>{document.querySelector('#explanation').textContent='嚴格晚到 480 筆；加入 240 筆剛好準時後，完整名單為 720 筆。';});
 await page.screenshot({path:D+'/screens/07-summary.png'});await pause(8000);event('recording_finished');
 await context.close();context=null;await browser.close();browser=null;await new Promise(resolve=>server.close(resolve));server=null;
 check(next===6&&runs.length===6&&blockedExternal===0,'Capture incomplete or attempted external request');
 const rawPath=await video.path();fs.copyFileSync(rawPath,D+'/live-demo.raw.webm',fs.constants.COPYFILE_EXCL);
 const oracle=await child(profile.python.file,[HERE+'/oracle.py',D+'/runtime'],{prefix:D+'/logs/oracle'});children.oracle=oracle.result.actual_exit;check(oracle.result.actual_exit===0,'Full current CSV/Parquet oracle failed');
 const oracleData=JSON.parse(oracle.out.toString('utf8'));
 const rawProbe=await child('/usr/bin/ffprobe',['-v','error','-show_streams','-show_format','-of','json',D+'/live-demo.raw.webm'],{prefix:D+'/logs/ffprobe-webm'});children.ffprobe_webm=rawProbe.result.actual_exit;check(rawProbe.result.actual_exit===0,'Raw video probe failed');
 const rawInfo=JSON.parse(rawProbe.out.toString('utf8'));check(rawInfo.streams.length===1&&rawInfo.streams[0].codec_type==='video','Raw recording must be video-only');
 const encoded=await child('/usr/bin/ffmpeg',['-n','-i',D+'/live-demo.raw.webm','-map','0:v:0','-an','-c:v','libx264','-preset','medium','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',D+'/live-demo.silent.mp4'],{prefix:D+'/logs/ffmpeg-encode',timeout:90000});children.ffmpeg_encode=encoded.result.actual_exit;check(encoded.result.actual_exit===0,'One encode failed');
 const probe=await child('/usr/bin/ffprobe',['-v','error','-count_frames','-show_streams','-show_format','-of','json',D+'/live-demo.silent.mp4'],{prefix:D+'/logs/ffprobe-mp4'});children.ffprobe_mp4=probe.result.actual_exit;check(probe.result.actual_exit===0,'MP4 probe failed');
 const info=JSON.parse(probe.out.toString('utf8')),v=info.streams[0],seconds=Number(info.format.duration);
 check(info.streams.length===1&&v.codec_type==='video'&&v.codec_name==='h264'&&v.width===1920&&v.height===1080&&v.pix_fmt==='yuv420p'&&Number.isSafeInteger(Number(v.nb_read_frames))&&seconds>=75&&seconds<=100&&Math.abs(seconds-Number(rawInfo.format.duration))<=0.12,'Actual silent1080p capture duration/format outside scope');
 const decoded=await child('/usr/bin/ffmpeg',['-v','error','-i',D+'/live-demo.silent.mp4','-map','0:v:0','-f','null','-'],{prefix:D+'/logs/ffmpeg-full-decode',timeout:60000});children.ffmpeg_decode=decoded.result.actual_exit;check(decoded.result.actual_exit===0&&decoded.bad.length===0,'Full MP4 decode failed or emitted decoder errors');
 original({ownLease:true});for(const d of profile.pins)bind(d);
 manifest={kind:'actual_DuckDB_live_console_capture_v1',source_capture_date:started.slice(0,10),original_fixture_date:'2026-10-25',started_at:started,finished_at:new Date().toISOString(),pid:process.pid,source_sha256:SOURCE,script_sha256:SCRIPT,source_lines:111,ui_original_not_official:true,real_commands_during_recording:true,source_audio_or_narration_timing_claimed:false,audio_streams:0,TTS:0,ASR:0,paid_calls:0,external_requests_blocked:blockedExternal,video:desc(D+'/live-demo.silent.mp4'),native_webm:desc(D+'/live-demo.raw.webm'),ffprobe_mp4:desc(D+'/logs/ffprobe-mp4.stdout'),actual_duration_seconds:seconds,actual_avg_frame_rate:v.avg_frame_rate,actual_frame_count:Number(v.nb_read_frames),no_speed_change:true,original_binary:profile.binary,original_inputs:profile.inputs.map(({relative,...d})=>d),copied_inputs:profile.inputs.map(x=>desc(D+'/runtime/'+x.relative)),steps:runs,oracle:oracleData,child_exit_codes:children,events};
 write(D+'/recording-manifest.json',manifest);
 write(D+'/live-demo-usage.txt',['DuckDB 完整資料匯出｜本片原創實跑操作錄影','操作重現日期：'+started.slice(0,10)+'；原創虛構 fixture 建立日期：2026-10-25。','此操作視窗是本片原創介面，錄影期間逐項真正執行本機 DuckDB 2.0 CLI，呈現當次 stdout；不是 DuckDB 官方介面，也不是模型推理展示。','原始CSV及SQL逐 bytes 複製到獨立工作區；沒有複製舊輸出或重播舊runlog。','流程：工具版本→一般預覽→agent預覽→嚴格晚到完整CSV與Parquet→Parquet讀回→含準時名單。','當次完整CSV以標準csv解析器逐列逐欄對照1200筆輸入：嚴格晚到480筆，含準時720筆，新增240筆 days_late=0；Parquet讀回CSV與嚴格CSV完整bytes相同。',`實際影像：1920×1080 H.264/yuv420p，${seconds.toFixed(3)}秒，平均${v.avg_frame_rate} fps，完整解碼0 errors；0音軌、未改播放速度。`,'本片剪接用無配音來源素材；不是正式成片，不含正式片頭片尾，不是實際旁白時間軸、CC或八語配音交付。','未做效能、模型推理、token或費用比較。',...profile.steps.map((s,i)=>`${i+1}. ${s.display}`),''].join('\n'));
}catch(e){error={name:e.name,message:e.message};}
finally{
 if(context)try{await context.close();}catch{}
 if(browser)try{await browser.close();}catch{}
 if(server)try{await new Promise(resolve=>server.close(resolve));}catch{}
 try{lease.verify();lease.release();}catch(e){error??={name:e.name,message:e.message};}
 if(fs.existsSync(RUN)){
  const result={kind:'actual_DuckDB_live_capture_execution_v1',at:new Date().toISOString(),started_at:started,pid:process.pid,active:false,ok:!error&&!!manifest,error,native_lease_released:!fs.existsSync(W+'/LEASE'),source_sha256:SOURCE,script_sha256:SCRIPT,commands_completed:runs.length,child_exit_codes:children,TTS:0,ASR:0,paid_calls:0,new_server_approval:false};
  for(const [k,p]of[['manifest',D+'/recording-manifest.json'],['usage',D+'/live-demo-usage.txt'],['video',D+'/live-demo.silent.mp4'],['native_webm',D+'/live-demo.raw.webm'],['ffprobe_mp4',D+'/logs/ffprobe-mp4.stdout']])if(fs.existsSync(p))result[k]=desc(p);
  write(RUN+'/http-local-requests.json',requests);write(RUN+'/events.json',events);write(RUN+'/completion.json',result);
  console.log(JSON.stringify(result));
 }
}
if(error)process.exitCode=1;
