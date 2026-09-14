export function countTodos(items) {
 return items.reduce((count,item)=>({
  total:count.total+1,
  completed:count.completed+(item.completed?1:0),
  active:count.active+(item.completed?0:1)
 }),{total:0,completed:0,active:0});
}
