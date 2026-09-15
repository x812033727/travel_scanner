import {createServer} from 'node:http';
const server=createServer((request,response)=>{
 const token=request.headers.authorization;
 response.setHeader('Content-Type','application/json');
 if(!token){response.writeHead(401,{'WWW-Authenticate':'Bearer realm="fixture"'});response.end('{"error":"missing_token","fixture":true}');return;}
 if(token!=='Bearer read-demo'){response.writeHead(403);response.end('{"error":"insufficient_scope","fixture":true}');return;}
 response.end(JSON.stringify({fixture:true,items:[{id:'a',title:'假資料'}]}));
});
server.listen(0,'127.0.0.1',()=>console.log('HTTP auth fixture (NOT OAuth or MCP): http://127.0.0.1:'+server.address().port));
