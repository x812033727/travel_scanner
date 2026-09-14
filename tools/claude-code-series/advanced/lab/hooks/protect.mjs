import {readEvent,emit} from './event.mjs';
import {safePath} from './boundary.mjs';
try {
 const e=readEvent();
 if(e.hook_event_name!=='PreToolUse') throw new Error('PreToolUse only');
 if(['Write','Edit'].includes(e.tool_name)) {
  try {
   const p=safePath(e.cwd,e.tool_input?.file_path);
   if(p.relative.toLowerCase().startsWith('private/') || p.relative.toLowerCase()==='private') throw new Error('protected fixture directory');
  } catch(error) {
   emit({hookSpecificOutput:{hookEventName:'PreToolUse',permissionDecision:'deny',permissionDecisionReason:error.message}});
  }
 }
} catch(error) {console.error(error.message);process.exitCode=2;}
