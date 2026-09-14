import { readFileSync } from 'node:fs';
const tasks = JSON.parse(readFileSync(new URL('../fixtures/tasks.json', import.meta.url), 'utf8'));
export function listTasks({offset=0,limit=2,completed}={}) {
  if (!Number.isInteger(offset) || offset<0 || !Number.isInteger(limit) || limit<1 || limit>20) throw new Error('invalid pagination');
  if (completed!==undefined && typeof completed!=='boolean') throw new Error('invalid completed');
  const filtered=tasks.filter(task=>completed===undefined || task.completed===completed);
  return {items:filtered.slice(offset,offset+limit).map(task=>({...task})),nextOffset:offset+limit<filtered.length?offset+limit:null,total:filtered.length};
}
export function getTask(id) { return tasks.find(task=>task.id===id) ?? null; }
