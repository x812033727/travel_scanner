import { realpathSync, existsSync } from 'node:fs';
import path from 'node:path';
export function safePath(base,input) {
 if (typeof input!=='string' || input.includes('\0')) throw new Error('invalid path');
 const root=realpathSync(base),target=path.resolve(root,input);
 let ancestor=target;
 while(!existsSync(ancestor)) {
  const parent=path.dirname(ancestor);
  if(parent===ancestor) throw new Error('no existing parent');
  ancestor=parent;
 }
 const resolved=path.resolve(realpathSync(ancestor),path.relative(ancestor,target));
 const relative=path.relative(root,resolved);
 if(relative==='..' || relative.startsWith('..'+path.sep) || path.isAbsolute(relative)) throw new Error('outside exercise');
 return {target:resolved,relative:relative.split(path.sep).join('/')};
}
