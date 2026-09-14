import {mkdirSync,writeFileSync,existsSync,readFileSync} from 'node:fs';import path from 'node:path';
export function notify(event,root='run-data/notifications') {
 if(!event || !/^[a-z0-9-]{1,64}$/.test(event.id) || !['completed','failed'].includes(event.status))throw new Error('Invalid event');
 mkdirSync(root,{recursive:true});const file=path.join(root,event.id+'.json');
 const safe={id:event.id,status:event.status};
 try{writeFileSync(file,JSON.stringify(safe)+'\n',{flag:'wx'});return {delivered:true};}
 catch(error){
  if(error.code!=='EEXIST')throw error;
  if(JSON.parse(readFileSync(file,'utf8')).status!==event.status)throw new Error('Event id reused for another state');
  return {delivered:false,duplicate:true};
 }
}
