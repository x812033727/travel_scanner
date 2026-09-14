import { readFileSync } from 'node:fs';
export function readEvent() {
 const event=JSON.parse(readFileSync(0,'utf8').replace(/^\uFEFF/,''));
 if (!event || typeof event!=='object' || typeof event.cwd!=='string' || typeof event.hook_event_name!=='string') throw new Error('event needs cwd and hook_event_name');
 return event;
}
export function emit(value) { process.stdout.write(JSON.stringify(value)+'\n'); }
