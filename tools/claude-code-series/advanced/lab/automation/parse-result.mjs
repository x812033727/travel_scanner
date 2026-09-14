import {readFileSync} from 'node:fs';import {parseResult,lastResult} from './result.mjs';
try {
 const [file,format='json']=process.argv.slice(2);if(!file)throw new Error('Provide a result file');
 const text=readFileSync(file,'utf8').replace(/^\uFEFF/,'');
 console.log(JSON.stringify(format==='stream'?lastResult(text):parseResult(text),null,2));
}catch(error){console.error(error.message);process.exitCode=2;}
