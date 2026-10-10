// Author-built teaching reference. This file is not evidence of a Codex model run.
export const STORAGE_KEY = 'mokaair-codex-practical-v2';
export function instant(value) {
  if (typeof value !== 'string' || !/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z$/.test(value)
      || !Number.isFinite(Date.parse(value)) || new Date(value).toISOString() !== value) throw new Error('utc-instant');
  return value;
}
function validTask(task, version) {
  if (!task || typeof task.id !== 'string' || !task.id || typeof task.title !== 'string'
      || !task.title.trim() || task.title.trim().length > 100 || typeof task.completed !== 'boolean') throw new Error('task-format');
  const completedAt = version === 1 ? null : task.completedAt;
  if (completedAt !== null) instant(completedAt);
  if (!task.completed && completedAt !== null) throw new Error('pending-date');
  return { id: task.id, title: task.title.trim(), completed: task.completed, completedAt };
}
export function documentFrom(value) {
  if (!value || ![1, 2].includes(value.version) || !Array.isArray(value.tasks)) throw new Error('storage-format');
  const ids = new Set();
  const tasks = value.tasks.map(task => {
    const item = validTask(task, value.version);
    if (ids.has(item.id)) throw new Error('duplicate-id');
    ids.add(item.id); return item;
  });
  return { version: 2, tasks };
}
export function decodeTasks(raw) { return raw === null ? [] : documentFrom(JSON.parse(raw)).tasks; }
export function encodeTasks(tasks) { return JSON.stringify(documentFrom({ version: 2, tasks }), null, 2) + '\n'; }
export function addTask(tasks, rawTitle, id) {
  const candidate = validTask({ id, title: String(rawTitle), completed: false, completedAt: null }, 2);
  if (tasks.some(task => task.id === id)) throw new Error('duplicate-id');
  return [...tasks, candidate];
}
export function toggleTask(tasks, id, now = new Date().toISOString()) {
  instant(now);
  return tasks.map(task => task.id === id
    ? { ...task, completed: !task.completed, completedAt: task.completed ? null : now } : { ...task });
}
export function removeTask(tasks, id) { return tasks.filter(task => task.id !== id); }
export function visibleTasks(tasks, filter = 'all', query = '') {
  const needle = String(query).trim().toLocaleLowerCase();
  return tasks.filter(task => (filter === 'active' ? !task.completed : filter === 'completed' ? task.completed : true)
    && task.title.toLocaleLowerCase().includes(needle));
}
export function mergeTasks(existing, incoming) {
  const validated = documentFrom({ version: 2, tasks: incoming }).tasks;
  const ids = new Set(existing.map(task => task.id));
  if (validated.some(task => ids.has(task.id))) throw new Error('duplicate-id');
  return [...existing.map(task => ({ ...task })), ...validated];
}
export function importJson(existing, raw) { return mergeTasks(existing, decodeTasks(raw)); }
function parseCsv(raw) {
  if (typeof raw !== 'string') throw new Error('csv-input');
  const rows = []; let row = [], field = '', quoted = false, closed = false;
  raw = raw.replace(/^\uFEFF/, '');
  for (let i = 0; i < raw.length; i++) {
    const char = raw[i];
    if (quoted) {
      if (char === '"' && raw[i + 1] === '"') { field += '"'; i++; }
      else if (char === '"') { quoted = false; closed = true; }
      else field += char;
    } else if (char === '"') {
      if (field || closed) throw new Error('csv-quote'); quoted = true;
    } else if (char === ',' || char === '\n' || (char === '\r' && raw[i + 1] === '\n')) {
      row.push(field); field = ''; closed = false;
      if (char !== ',') { rows.push(row); row = []; if (char === '\r') i++; }
    } else {
      if (closed) throw new Error('csv-after-quote');
      if (char === '\r') throw new Error('csv-line-ending');
      field += char;
    }
  }
  if (quoted) throw new Error('csv-unclosed-quote');
  if (field || row.length || closed) { row.push(field); rows.push(row); }
  return rows;
}
export function decodeCsv(raw) {
  const [header, ...rows] = parseCsv(raw);
  if (JSON.stringify(header) !== JSON.stringify(['id', 'title', 'completed', 'completedAt'])) throw new Error('csv-header');
  const tasks = rows.map(row => {
    if (row.length !== 4 || !['true', 'false'].includes(row[2])) throw new Error('csv-row');
    return { id: row[0], title: row[1], completed: row[2] === 'true', completedAt: row[3] || null };
  });
  return documentFrom({ version: 2, tasks }).tasks;
}
export function encodeCsv(tasks) {
  const valid = documentFrom({ version: 2, tasks }).tasks;
  const quote = value => /[",\r\n]/.test(value) ? '"' + value.replace(/"/g, '""') + '"' : value;
  return 'id,title,completed,completedAt\n' + valid.map(task =>
    [task.id, task.title, String(task.completed), task.completedAt || ''].map(quote).join(',')).join('\n') + (valid.length ? '\n' : '');
}
export function importCsv(existing, raw) { return mergeTasks(existing, decodeCsv(raw)); }
function taipeiDate(date) {
  if (typeof date !== 'string' || !/^\d{4}-\d{2}-\d{2}$/.test(date)) throw new Error('calendar-date');
  const utc = Date.parse(date + 'T00:00:00.000Z');
  if (!Number.isFinite(utc) || new Date(utc).toISOString().slice(0, 10) !== date) throw new Error('calendar-date');
  return utc - 8 * 60 * 60 * 1000;
}
export function weeklyReport(tasks, from, to) {
  const valid = documentFrom({ version: 2, tasks }).tasks;
  const begin = taipeiDate(from), end = taipeiDate(to) + 86400000;
  if (begin >= end) throw new Error('date-order');
  return { revision: 'weekly-report-v2', timezone: 'Asia/Taipei', weekStart: from, weekEnd: to,
    total: valid.length, completedInWeek: valid.filter(task => task.completed && task.completedAt
      && Date.parse(task.completedAt) >= begin && Date.parse(task.completedAt) < end).length,
    pending: valid.filter(task => !task.completed).length,
    unknownCompleted: valid.filter(task => task.completed && task.completedAt === null).length };
}
export function archiveTasks(tasks, cutoff) {
  instant(cutoff);
  const valid = documentFrom({ version: 2, tasks }).tasks;
  const selected = task => task.completed && task.completedAt !== null && task.completedAt <= cutoff;
  return { archived: valid.filter(selected), retained: valid.filter(task => !selected(task)) };
}
export function restoreTasks(backupRaw) { return decodeTasks(backupRaw); }
