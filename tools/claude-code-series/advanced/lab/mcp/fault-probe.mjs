import {Client} from '@modelcontextprotocol/client';
import {StdioClientTransport} from '@modelcontextprotocol/client/stdio';
import {fileURLToPath} from 'node:url';
const mode=process.argv[2]??'exit';
if(!['exit','invalid','hang'].includes(mode)){console.error('Expected exit, invalid or hang');process.exit(2);}
const transport=new StdioClientTransport({command:process.execPath,args:[fileURLToPath(new URL('./fault.mjs',import.meta.url)),mode],stderr:'pipe'});
const client=new Client({name:'fault-probe',version:'1.0.0'});
const errors=[];transport.onerror=error=>errors.push(error.message);
let timer;
try{
 await Promise.race([client.connect(transport),new Promise((_,reject)=>{timer=setTimeout(()=>reject(new Error('Connection timeout after 1500 ms')),1500);})]);
 throw new Error('Fault fixture unexpectedly connected');
}catch(error){console.error(JSON.stringify({mode,connected:false,error:error.message,transportErrors:errors}));process.exitCode=1;}
finally{clearTimeout(timer);await client.close();}
