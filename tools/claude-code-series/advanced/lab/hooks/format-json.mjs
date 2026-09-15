import {readFileSync,writeFileSync} from 'node:fs';
import {readEvent,emit} from './event.mjs';
import {safePath} from './boundary.mjs';
try {
 const e=readEvent(); if(e.hook_event_name!=='PostToolUse') throw new Error('PostToolUse only');
 const p=safePath(e.cwd,e.tool_input?.file_path);
 if(p.relative.startsWith('fixtures/') && p.relative.endsWith('.json')) {
  const original=readFileSync(p.target,'utf8');const formatted=JSON.stringify(JSON.parse(original),null,2)+'\n';
  if(original!==formatted) writeFileSync(p.target,formatted);
 }
} catch(error) {
 emit({hookSpecificOutput:{hookEventName:'PostToolUse',additionalContext:'JSON formatting failed: '+error.message}});
}
