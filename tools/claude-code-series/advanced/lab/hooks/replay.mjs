import {readFileSync} from 'node:fs';
import {spawnSync} from 'node:child_process';
import path from 'node:path';
const modes=new Set(['audit','protect','format-json','quality']);
const [mode,eventFile]=process.argv.slice(2);
if(!modes.has(mode)||!eventFile){console.error('node hooks/replay.mjs <audit|protect|format-json|quality> <event.json>');process.exit(2);}
const event=JSON.parse(readFileSync(eventFile,'utf8').replace(/^\uFEFF/,''));event.cwd=process.cwd();
if(event.tool_input?.file_path)event.tool_input.file_path=path.resolve(event.tool_input.file_path);
const result=spawnSync(process.execPath,[`hooks/${mode}.mjs`],{input:JSON.stringify(event),encoding:'utf8',timeout:20000,windowsHide:true});
process.stdout.write(result.stdout??'');process.stderr.write(result.stderr??'');process.exitCode=result.status??1;
