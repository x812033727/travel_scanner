import {readFileSync} from 'node:fs';
const target=process.argv[2];
if(!target){console.error('usage: node check-doc.mjs <markdown-file>');process.exitCode=2;}
else {
  try {
    const text=readFileSync(target,'utf8'), errors=[];
    if(!/^# .+/m.test(text))errors.push('missing_title');
    if(!/^## 來源/m.test(text))errors.push('missing_sources');
    console.log(JSON.stringify({file:target,errors},null,2));
    process.exitCode=errors.length?1:0;
  }catch(error){console.error(error.code||'read_failed');process.exitCode=2;}
}
