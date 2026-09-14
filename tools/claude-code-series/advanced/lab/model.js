export function addTodo(items, title, id) {
  const cleaned = title.trim();
  if (!cleaned || cleaned.length > 100) return items;
  return [...items, { id, title: cleaned, completed: false }];
}
export function toggleTodo(items, id) {
  return items.map(item => item.id === id ? { ...item, completed: !item.completed } : item);
}
export function removeTodo(items, id) {
  return items.filter(item => item.id !== id);
}
