export function countTodos(items) {
 let total=0;for(const item of items){void item;total++;}
 let completed=0;for(const item of items){if(item.completed)completed++;}
 let active=0;for(const item of items){if(!item.completed)active++;}
 return {total,completed,active};
}
