export const listTasks = items => ({items: items.map(item => ({...item})), total: items.length});
