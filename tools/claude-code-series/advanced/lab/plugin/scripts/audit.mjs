import { appendFileSync,mkdirSync } from 'node:fs';
import path from 'node:path';
import {readEvent} from './event.mjs';
try {
 const e=readEvent();
 const logDir=path.join(e.cwd,'run-data');mkdirSync(logDir,{recursive:true});
 const record={event:e.hook_event_name,tool:e.tool_name??null,session:e.session_id??null,at:new Date().toISOString()};
 appendFileSync(path.join(logDir,'events.jsonl'),JSON.stringify(record)+'\n');
} catch(error) {console.error(error.message);process.exitCode=1;}
