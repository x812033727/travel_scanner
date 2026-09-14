import test from 'node:test';import assert from 'node:assert/strict';
import {spawn,spawnSync} from 'node:child_process';import {fileURLToPath} from 'node:url';
const root=fileURLToPath(new URL('../',import.meta.url));
test('course configuration rejects unsupported keys and wrong permission types',()=>{
 for(const [file,status] of [['settings.shared.json',0],['settings.bad.json',2]]){
  const result=spawnSync(process.execPath,['config/check-config.mjs','config/'+file],{cwd:root,encoding:'utf8',windowsHide:true,timeout:5000});
  assert.equal(result.status,status,result.stderr);
 }
});
test('local auth fixture distinguishes missing token, wrong scope and accepted fake token',async()=>{
 const child=spawn(process.execPath,['mcp/auth-fixture.mjs'],{cwd:root,windowsHide:true,stdio:['ignore','pipe','pipe']});
 try{
  const url=await new Promise((resolve,reject)=>{
   const timer=setTimeout(()=>reject(new Error('Fixture did not start')),5000);
   child.once('error',error=>{clearTimeout(timer);reject(error);});
   child.stdout.once('data',data=>{clearTimeout(timer);const match=data.toString().match(/http:\/\/127\.0\.0\.1:\d+/);match?resolve(match[0]):reject(new Error('No URL'));});
  });
  assert.equal((await fetch(url)).status,401);
  assert.equal((await fetch(url,{headers:{Authorization:'Bearer wrong'}})).status,403);
  const ok=await fetch(url,{headers:{Authorization:'Bearer read-demo'}});
  assert.equal(ok.status,200);assert.equal((await ok.json()).fixture,true);
 }finally{child.kill();await new Promise(resolve=>child.once('exit',resolve));}
});
test('MCP fault clients fail closed for exit, invalid output and hung server',()=>{
 for(const mode of ['exit','invalid','hang']){
  // The protocol deadline remains 1500 ms; allow process startup and SDK cleanup separately.
  const result=spawnSync(process.execPath,['mcp/fault-probe.mjs',mode],{cwd:root,encoding:'utf8',windowsHide:true,timeout:20000});
  assert.equal(result.status,1,result.stderr);assert.match(result.stderr,/connected.*false/);
 }
});
