import {spawnSync} from 'node:child_process';
import {readEvent,emit} from './event.mjs';
try {
 const e=readEvent();if(e.hook_event_name!=='Stop') throw new Error('Stop only');
 if(!e.stop_hook_active) {
  const env={...process.env};delete env.NODE_TEST_CONTEXT;
  const result=spawnSync(process.execPath,['--test','tests/model.test.mjs'],{cwd:e.cwd,encoding:'utf8',timeout:15000,windowsHide:true,env});
  if(result.status!==0) emit({decision:'block',reason:'Core tests did not pass. Inspect the test output, fix the cause, and run node --test tests/model.test.mjs. This hook will not block recursively.'});
 } else { console.error('Repeated Stop: finish with explicit unresolved test status.'); }
} catch(error) {console.error(error.message);process.exitCode=1;}
