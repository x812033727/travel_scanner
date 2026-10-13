#!/usr/bin/env node
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
const folder=path.resolve(process.argv[2]||'C:/Users/x8120/mokaair-work/videos/ou-de-jianghu-e001/plan/preflight-20261008-v3');
const port=Number(process.argv[3]||8767);
http.createServer((req,res)=>{
 const u=new URL(req.url,'http://127.0.0.1');
 const f=path.resolve(folder,'.'+decodeURIComponent(u.pathname==='/'?'/animatic.html':u.pathname));
 if(!f.startsWith(folder+path.sep)||!fs.existsSync(f)||!fs.statSync(f).isFile()){res.writeHead(404);res.end('Not found');return;}
 res.writeHead(200,{'Content-Type':f.endsWith('.html')?'text/html; charset=utf-8':f.endsWith('.json')?'application/json; charset=utf-8':'text/plain; charset=utf-8','Cache-Control':'no-store'});
 fs.createReadStream(f).pipe(res);
}).listen(port,'127.0.0.1',()=>console.log(`http://127.0.0.1:${port}/animatic.html`));
