export function addTask(tasks, rawTitle, id) {
  const title = String(rawTitle).trim();
  if (!title || title.length > 100) throw new Error("title-length");
  if (typeof id !== "string" || !id || tasks.some((task) => task.id === id)) throw new Error("task-id");
  return [...tasks, { id, title, completed: false }];
}

export function toggleTask(tasks, id) {
  return tasks.map((task) => task.id === id ? { ...task, completed: !task.completed } : task);
}

export function removeTask(tasks, id) {
  return tasks.filter((task) => task.id !== id);
}

// EXERCISE: implement the Active and Completed filters.
export function visibleTasks(tasks, filter) {
  return tasks;
}

export function decodeTasks(raw) {
  if (raw === null) return [];
  const value = JSON.parse(raw);
  if (value?.version !== 1 || !Array.isArray(value.tasks)) throw new Error("storage-format");
  const ids = new Set();
  return value.tasks.map((task) => {
    if (typeof task?.id !== "string" || !task.id || ids.has(task.id)
      || typeof task.title !== "string" || !task.title.trim() || task.title.length > 100
      || typeof task.completed !== "boolean") throw new Error("storage-format");
    ids.add(task.id);
    return { id: task.id, title: task.title.trim(), completed: task.completed };
  });
}

export function encodeTasks(tasks) {
  return JSON.stringify({ version: 1, tasks });
}
