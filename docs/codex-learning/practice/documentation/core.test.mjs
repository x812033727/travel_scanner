import test from "node:test";
import assert from "node:assert/strict";
import { addTask, toggleTask, removeTask, visibleTasks, decodeTasks, encodeTasks } from "./core.mjs";

test("add trims, preserves unicode, rejects empty/long text and does not mutate input", () => {
  const before = [];
  assert.deepEqual(addTask(before, "  寫作 ✨  ", "a"), [{ id: "a", title: "寫作 ✨", completed: false }]);
  assert.deepEqual(before, []);
  assert.throws(() => addTask(before, "   ", "a"));
  assert.throws(() => addTask(before, "x".repeat(101), "a"));
  assert.throws(() => addTask(addTask(before, "a", "a"), "b", "a"));
});
test("toggle and delete affect the requested task; filters agree with completion", () => {
  const original = addTask(addTask([], "Read", "a"), "Build", "b");
  const changed = toggleTask(original, "a");
  assert.equal(original[0].completed, false);
  assert.deepEqual(visibleTasks(changed, "active").map(t => t.id), ["b"]);
  assert.deepEqual(visibleTasks(changed, "completed").map(t => t.id), ["a"]);
  assert.deepEqual(removeTask(changed, "a").map(t => t.id), ["b"]);
  assert.deepEqual(toggleTask(changed, "missing"), changed);
});
test("storage round trips a versioned document and rejects corrupt or duplicate identities", () => {
  const tasks = addTask([], "<img src=x>", "a");
  assert.deepEqual(decodeTasks(encodeTasks(tasks)), tasks);
  assert.deepEqual(decodeTasks(null), []);
  for (const raw of ["bad-json", "{}", '{"version":2,"tasks":[]}', encodeTasks([...tasks, ...tasks]), encodeTasks([{ ...tasks[0], completed: "false" }])]) {
    assert.throws(() => decodeTasks(raw));
  }
});
