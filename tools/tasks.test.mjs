import assert from "node:assert/strict";
import { mkdtempSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import path from "node:path";
import test from "node:test";

import { parseTask, renderBoard, runCommand, selectReady, serializeTask, slugify, validate } from "./tasks.mjs";

const AT = (iso) => new Date(iso);

function workspace() {
  const root = mkdtempSync(path.join(tmpdir(), "tasks-"));
  mkdirSync(path.join(root, "tasks", "open"), { recursive: true });
  mkdirSync(path.join(root, "tasks", "done"), { recursive: true });
  return root;
}

function run(root, argv, iso = "2026-09-05T09:00:00Z") {
  return runCommand(argv, { root, now: AT(iso) });
}

function file(root, folder, name) {
  return readFileSync(path.join(root, "tasks", folder, name), "utf8");
}

test("reads and rewrites a task file without changing it", () => {
  const source = [
    "---",
    "id: 2026-09-05-example",
    "title: Example",
    "status: open",
    "priority: P2",
    "area: web",
    "owner:",
    "claimed_at:",
    "created_at: 2026-09-05T09:00:00Z",
    "completed_at:",
    "branch:",
    "depends_on: []",
    "scope:",
    "  - apps/web/app",
    "  - apps/web/lib",
    "---",
    "",
    "# Example",
    "",
  ].join("\n");
  const task = parseTask(source);
  assert.equal(task.title, "Example");
  assert.deepEqual(task.scope, ["apps/web/app", "apps/web/lib"]);
  assert.deepEqual(task.depends_on, []);
  assert.equal(serializeTask(task), source);
});

test("rejects front matter a later reader could not trust", () => {
  const header = (...lines) => `---\n${lines.join("\n")}\n---\n\nbody\n`;
  assert.throws(() => parseTask("no front matter"), /front matter/);
  assert.throws(() => parseTask(header("id: a", "colour: red")), /unknown front matter field 'colour'/);
  assert.throws(() => parseTask(header("id: a", "id: b")), /appears twice/);
  assert.throws(() => parseTask(header("id: a")), /missing title/);
  assert.throws(() => parseTask(header("scope: apps/web")), /takes '\[\]' or indented/);
  assert.throws(() => parseTask(header("  - stray")), /does not belong to a list field/);
});

test("builds short ids and refuses titles with nothing to slug", () => {
  assert.equal(slugify("Cache the hotel search results for repeat queries"), "cache-the-hotel-search-results-for");
  assert.equal(slugify("Fix /ready when Redis is down!"), "fix-ready-when-redis-is-down");
  assert.equal(slugify("旅館快取"), "");
  const root = workspace();
  const failed = run(root, ["new", "--title", "旅館快取", "--area", "api", "--scope", "apps/api"]);
  assert.equal(failed.code, 1);
  assert.match(failed.lines[0], /--slug/);
  assert.equal(run(root, ["new", "--title", "旅館快取", "--slug", "hotel-cache", "--area", "api", "--scope", "apps/api"]).code, 0);
  assert.match(file(root, "open", "2026-09-05-hotel-cache.md"), /title: 旅館快取/);
});

test("two tasks filed the same day never collide on an id", () => {
  const root = workspace();
  const args = ["new", "--title", "Same title", "--area", "web", "--scope", "apps/web/app"];
  run(root, args);
  const second = run(root, [...args.slice(0, -1), "apps/web/lib"]);
  assert.match(second.lines[0], /2026-09-05-same-title-2\.md/);
});

test("hands out work that does not touch files another agent is changing", () => {
  const root = workspace();
  run(root, ["new", "--title", "Hotel cache", "--area", "api", "--scope", "apps/api/app/services", "--priority", "P1"]);
  run(root, ["new", "--title", "Hotel rates", "--area", "api", "--scope", "apps/api/app/services/hotels.py"]);
  run(root, ["new", "--title", "Alert list", "--area", "web", "--scope", "apps/web/components/alerts"]);

  assert.match(run(root, ["next"]).lines[0], /2026-09-05-hotel-cache/);
  assert.equal(run(root, ["claim", "2026-09-05-hotel-cache", "--owner", "claude-a"]).code, 0);

  // A nested scope counts as the same scope, so the second agent is sent elsewhere.
  assert.match(run(root, ["next"]).lines[0], /2026-09-05-alert-list/);
  const refused = run(root, ["claim", "2026-09-05-hotel-rates", "--owner", "gpt-b"]);
  assert.equal(refused.code, 1);
  assert.match(refused.lines[0], /already being changed by 2026-09-05-hotel-cache \(claude-a\)/);
  assert.equal(run(root, ["claim", "2026-09-05-hotel-rates", "--owner", "gpt-b", "--force"]).code, 0);
  assert.match(run(root, ["check"]).lines[0], /warning: 2026-09-05-hotel-cache and 2026-09-05-hotel-rates are both active/);
});

test("a claim nobody comes back to is reclaimable after a day", () => {
  const root = workspace();
  run(root, ["new", "--title", "Hotel cache", "--area", "api", "--scope", "apps/api"]);
  run(root, ["claim", "2026-09-05-hotel-cache", "--owner", "claude-a", "--branch", "claude/hotel-cache"]);

  const early = run(root, ["claim", "2026-09-05-hotel-cache", "--owner", "gpt-b"], "2026-09-05T20:00:00Z");
  assert.equal(early.code, 1);
  assert.match(early.lines[0], /held by claude-a/);

  const late = run(root, ["claim", "2026-09-05-hotel-cache", "--owner", "gpt-b"], "2026-09-06T10:00:00Z");
  assert.equal(late.code, 0);
  assert.match(late.lines[0], /Taking over a stale claim from claude-a/);
  const taken = parseTask(file(root, "open", "2026-09-05-hotel-cache.md"));
  assert.equal(taken.owner, "gpt-b");
  assert.equal(taken.branch, "", "the previous agent's branch must not follow the task");
});

test("a task waits for the tasks it depends on", () => {
  const root = workspace();
  run(root, ["new", "--title", "Schema", "--area", "api", "--scope", "apps/api/migrations", "--priority", "P1"]);
  run(root, ["new", "--title", "Endpoint", "--area", "api", "--scope", "apps/api/app/routers", "--priority", "P0", "--depends-on", "2026-09-05-schema"]);

  assert.match(run(root, ["next"]).lines[0], /2026-09-05-schema/, "the P0 task depends on the P1 task");
  const blocked = run(root, ["claim", "2026-09-05-endpoint", "--owner", "claude-a"]);
  assert.equal(blocked.code, 1);
  assert.match(blocked.lines[0], /depends on 2026-09-05-schema/);

  run(root, ["claim", "2026-09-05-schema", "--owner", "claude-a"]);
  run(root, ["done", "2026-09-05-schema"], "2026-09-05T11:00:00Z");
  assert.equal(run(root, ["claim", "2026-09-05-endpoint", "--owner", "claude-b"]).code, 0);
});

test("finishing a task archives it and keeps the board honest", () => {
  const root = workspace();
  run(root, ["new", "--title", "Alert list", "--area", "web", "--scope", "apps/web/components/alerts"]);
  run(root, ["claim", "2026-09-05-alert-list", "--owner", "claude-a"]);
  const finished = run(root, ["done", "2026-09-05-alert-list"], "2026-09-05T18:00:00Z");
  assert.match(finished.lines[0], /moved to tasks\/done/);
  assert.match(finished.lines[1], /3 checklist item\(s\) are still unticked/);
  const archived = parseTask(file(root, "done", "2026-09-05-alert-list.md"));
  assert.equal(archived.status, "done");
  assert.equal(archived.completed_at, "2026-09-05T18:00:00Z");
  const board = file(root, "", "BOARD.md").replace("tasks//", "tasks/");
  assert.match(board, /0 open · 0 in progress · 0 blocked · 0 in review · 1 done/);
  assert.match(board, /- 2026-09-05 \[Alert list\]\(done\/2026-09-05-alert-list\.md\)/);
});

test("check fails on a hand-edited board and passes once it is regenerated", () => {
  const root = workspace();
  run(root, ["new", "--title", "Alert list", "--area", "web", "--scope", "apps/web/components/alerts"]);
  writeFileSync(path.join(root, "tasks", "BOARD.md"), "# Task board\n\nsomeone typed this\n");
  const stale = run(root, ["check"]);
  assert.equal(stale.code, 1);
  assert.match(stale.lines[0], /BOARD\.md is out of date/);
  assert.equal(run(root, ["board"]).code, 0);
  assert.equal(run(root, ["check"]).code, 0);
});

test("check names every way a task file can be wrong", () => {
  const base = {
    id: "2026-09-05-example",
    title: "Example",
    status: "open",
    priority: "P2",
    area: "web",
    owner: "",
    claimed_at: "",
    created_at: "2026-09-05T09:00:00Z",
    completed_at: "",
    branch: "",
    depends_on: [],
    scope: ["apps/web/app"],
    body: "# Example\n",
    folder: "open",
    name: "2026-09-05-example.md",
    file: "tasks/open/2026-09-05-example.md",
  };
  const errorsFor = (patch) => validate([{ ...base, ...patch }], { now: AT("2026-09-05T10:00:00Z") }).errors.join("\n");

  assert.equal(errorsFor({}), "");
  assert.match(errorsFor({ id: "example", name: "example.md", file: "tasks/open/example.md" }), /id must look like/);
  assert.match(errorsFor({ name: "other.md" }), /file name must match the id/);
  assert.match(errorsFor({ priority: "urgent" }), /priority must be one of/);
  assert.match(errorsFor({ area: "database" }), /area must be one of/);
  assert.match(errorsFor({ created_at: "yesterday" }), /created_at must be a UTC stamp/);
  assert.match(errorsFor({ status: "done" }), /a done task belongs in tasks\/done\//);
  assert.match(errorsFor({ owner: "claude-a" }), /owner and claimed_at are always set together/);
  assert.match(errorsFor({ owner: "claude-a", claimed_at: "2026-09-05T09:30:00Z" }), /an open task has no owner/);
  assert.match(errorsFor({ status: "in-progress" }), /a in-progress task needs an owner/);
  assert.match(errorsFor({ scope: [] }), /scope needs at least one path/);
  assert.match(errorsFor({ scope: ["/etc/passwd"] }), /must be a repository-relative path/);
  assert.match(errorsFor({ scope: ["apps/../../secrets"] }), /must be a repository-relative path/);
  assert.match(errorsFor({ completed_at: "2026-09-05T10:00:00Z" }), /completed_at is only set once/);
  assert.match(errorsFor({ body: "   " }), /body must describe the work/);
  assert.match(errorsFor({ depends_on: ["2026-09-05-example"] }), /cannot depend on itself/);
  assert.match(errorsFor({ depends_on: ["2026-01-01-ghost"] }), /depends_on '2026-01-01-ghost' is not a task/);
});

test("check refuses two files claiming the same id and a dependency cycle", () => {
  const first = {
    id: "2026-09-05-a",
    title: "A",
    status: "open",
    priority: "P2",
    area: "web",
    owner: "",
    claimed_at: "",
    created_at: "2026-09-05T09:00:00Z",
    completed_at: "",
    branch: "",
    depends_on: ["2026-09-05-b"],
    scope: ["apps/web/a"],
    body: "A\n",
    folder: "open",
    name: "2026-09-05-a.md",
    file: "tasks/open/2026-09-05-a.md",
  };
  const second = {
    ...first,
    id: "2026-09-05-b",
    title: "B",
    depends_on: ["2026-09-05-a"],
    scope: ["apps/web/b"],
    name: "2026-09-05-b.md",
    file: "tasks/open/2026-09-05-b.md",
  };
  assert.match(validate([first, second]).errors.join("\n"), /dependency cycle 2026-09-05-a -> 2026-09-05-b -> 2026-09-05-a/);
  const duplicate = { ...first, file: "tasks/done/2026-09-05-a.md", folder: "done" };
  assert.match(validate([first, duplicate]).errors.join("\n"), /task id '2026-09-05-a' is already used by/);
});

test("the board is a pure function of the task files", () => {
  const root = workspace();
  run(root, ["new", "--title", "Alert list", "--area", "web", "--scope", "apps/web/components/alerts"]);
  run(root, ["claim", "2026-09-05-alert-list", "--owner", "claude-a"]);
  const tasks = [parseTask(file(root, "open", "2026-09-05-alert-list.md"))];
  const withPaths = tasks.map((task) => ({ ...task, folder: "open", name: `${task.id}.md`, file: `tasks/open/${task.id}.md` }));
  assert.equal(renderBoard(withPaths), renderBoard(withPaths), "no timestamp or other drift may leak into the board");
  assert.match(renderBoard(withPaths), /\| \[Alert list\]\(open\/2026-09-05-alert-list\.md\) \| claude-a \|/);
  assert.deepEqual(selectReady(withPaths), [], "an owned task is not offered to anyone else");
});

test("a pipe in a title cannot break the board table", () => {
  const root = workspace();
  run(root, ["new", "--title", "Split a|b routing", "--area", "web", "--scope", "apps/web/app"]);
  assert.match(file(root, "", "BOARD.md"), /\[Split a\\\|b routing\]/);
});

test("release puts a task back and status moves it without losing the owner", () => {
  const root = workspace();
  run(root, ["new", "--title", "Alert list", "--area", "web", "--scope", "apps/web/components/alerts"]);
  run(root, ["claim", "2026-09-05-alert-list", "--owner", "claude-a"]);
  run(root, ["status", "2026-09-05-alert-list", "review", "--branch", "claude/alert-list"]);
  const reviewing = parseTask(file(root, "open", "2026-09-05-alert-list.md"));
  assert.equal(reviewing.status, "review");
  assert.equal(reviewing.owner, "claude-a");
  assert.equal(reviewing.branch, "claude/alert-list");

  run(root, ["release", "2026-09-05-alert-list"]);
  const released = parseTask(file(root, "open", "2026-09-05-alert-list.md"));
  assert.equal(released.status, "open");
  assert.equal(released.owner, "");
  assert.equal(released.claimed_at, "");
  assert.equal(run(root, ["check"]).code, 0);
  assert.match(run(root, ["status", "2026-09-05-alert-list", "done"]).lines[0], /use 'npm run tasks -- done/);
  assert.match(run(root, ["claim", "missing-task", "--owner", "claude-a"]).lines[0], /no task 'missing-task'/);
});

test("an empty backlog says so instead of blaming another agent", () => {
  const root = workspace();
  assert.match(run(root, ["next"]).lines[0], /The backlog has no open task\./);
  run(root, ["new", "--title", "Alert list", "--area", "web", "--scope", "apps/web/components/alerts"]);
  assert.match(run(root, ["next", "--area", "api"]).lines[0], /no open task in api/);
  run(root, ["new", "--title", "Alert empty state", "--area", "web", "--scope", "apps/web/components/alerts/list.tsx"]);
  run(root, ["claim", "2026-09-05-alert-list", "--owner", "claude-a"]);
  assert.match(run(root, ["next"]).lines[1], /another agent is changing/);
  assert.equal(run(root, ["list", "--owner", "claude-a"]).lines.length, 1);
  assert.deepEqual(run(root, ["list", "--owner", "gpt-b"]).lines, ["No task matches."]);
});
