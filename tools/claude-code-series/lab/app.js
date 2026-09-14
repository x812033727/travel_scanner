import { addTodo, toggleTodo, removeTodo } from './model.js';

const form = document.querySelector('#todo-form');
const input = document.querySelector('#todo-title');
const list = document.querySelector('#todo-list');
const message = document.querySelector('#message');
let items = [];

function render() {
  list.replaceChildren();
  for (const item of items) {
    const row = document.createElement('li');
    const label = document.createElement('label');
    const checkbox = document.createElement('input');
    checkbox.type = 'checkbox';
    checkbox.checked = item.completed;
    checkbox.addEventListener('change', () => { items = toggleTodo(items, item.id); render(); });
    const title = document.createElement('span');
    title.textContent = item.title;
    if (item.completed) title.className = 'completed';
    label.append(checkbox, title);
    const remove = document.createElement('button');
    remove.type = 'button';
    remove.textContent = '刪除';
    remove.setAttribute('aria-label', `刪除 ${item.title}`);
    remove.addEventListener('click', () => { items = removeTodo(items, item.id); render(); });
    row.append(label, remove);
    list.append(row);
  }
  message.textContent = items.length ? `共 ${items.length} 件，已完成 ${items.filter(item => item.completed).length} 件` : '目前沒有待辦。';
}
form.addEventListener('submit', event => {
  event.preventDefault();
  const next = addTodo(items, input.value, crypto.randomUUID());
  if (next === items) { message.textContent = '請輸入一到一百字的待辦。'; return; }
  items = next;
  input.value = '';
  render();
  input.focus();
});
render();
