import { addTask, toggleTask, removeTask, visibleTasks, decodeTasks, encodeTasks } from "./core.mjs";

const key = "mokaair-codex-todo-v1";
const form = document.querySelector("#task-form");
const input = document.querySelector("#task-title");
const filter = document.querySelector("#filter");
const list = document.querySelector("#tasks");
const message = document.querySelector("#message");
let tasks = [];
let storageAvailable = true;
try { tasks = decodeTasks(localStorage.getItem(key)); }
catch { storageAvailable = false; message.textContent = "Stored data cannot be read. Work remains temporary until you reset practice data."; }

function persist() {
  if (!storageAvailable) return;
  try { localStorage.setItem(key, encodeTasks(tasks)); }
  catch { storageAvailable = false; message.textContent = "Storage is unavailable. Changes in this tab will not survive a reload."; }
}

function render(focusRequest = null) {
  list.replaceChildren();
  const shown = visibleTasks(tasks, filter.value);
  for (const [index, task] of shown.entries()) {
    const item = document.createElement("li");
    const label = document.createElement("label");
    const check = document.createElement("input");
    check.type = "checkbox";
    check.dataset.taskId = task.id;
    check.checked = task.completed;
    check.addEventListener("change", () => {
      tasks = toggleTask(tasks, task.id); persist();
      render({ id: task.id, index, control: "input" });
    });
    const title = document.createElement("span");
    title.textContent = task.title;
    const remove = document.createElement("button");
    remove.type = "button";
    remove.dataset.taskId = task.id;
    remove.textContent = "Delete";
    remove.setAttribute("aria-label", `Delete ${task.title}`);
    remove.addEventListener("click", () => {
      tasks = removeTask(tasks, task.id); persist();
      render({ id: task.id, index, control: "button" });
    });
    label.append(check, title);
    item.append(label, remove);
    list.append(item);
  }
  document.querySelector("#count").textContent = `${tasks.filter((task) => !task.completed).length} active / ${tasks.length} total`;
  document.querySelector("#empty").hidden = shown.length > 0;
  if (focusRequest?.id) {
    const controls = [...list.querySelectorAll(focusRequest.control)];
    const target = controls.find((control) => control.dataset.taskId === focusRequest.id)
      ?? controls[Math.min(focusRequest.index, controls.length - 1)] ?? input;
    target.focus();
  }
}

form.addEventListener("submit", (event) => {
  event.preventDefault();
  try { tasks = addTask(tasks, input.value, crypto.randomUUID()); }
  catch { message.textContent = "Enter a task with 1 to 100 non-blank characters."; return; }
  if (storageAvailable) message.textContent = "";
  persist();
  input.value = "";
  render();
  input.focus();
});
filter.addEventListener("change", render);
document.querySelector("#reset").addEventListener("click", () => {
  tasks = [];
  try { localStorage.removeItem(key); storageAvailable = true; message.textContent = "Practice data reset."; }
  catch { storageAvailable = false; message.textContent = "Storage remains unavailable. This tab is temporary."; }
  render();
});
render();
