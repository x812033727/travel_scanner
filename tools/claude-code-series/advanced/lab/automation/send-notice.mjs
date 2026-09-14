import {readFileSync} from 'node:fs';import {notify} from './notify.mjs';
try{
 const event=JSON.parse(readFileSync(process.argv[2]??'fixtures/notice.json','utf8'));
 console.log(JSON.stringify(notify(event,process.argv[3]??'run-data/notifications')));
}catch(error){console.error(error.message);process.exitCode=2;}
