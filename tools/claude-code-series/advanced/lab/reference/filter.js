export function filterTasks(items,mode='all') {
 if(!['all','active','completed'].includes(mode))throw new Error('Unknown filter mode');
 return items.filter(item=>mode==='all'||item.completed===(mode==='completed'));
}
