#!/usr/bin/env node
// One shared backlog for humans and for whichever model picks up the work next.
//
// Every unfinished task is a single file in tasks/open, so two agents working on two
// tasks never write the same file and never wait for each other. tasks/BOARD.md is the
// one file they all touch, so it is generated rather than edited: a conflict there is
// resolved by re-running this tool, not by hand-merging.
import { existsSync, mkdirSync, readFileSync, readdirSync, rmSync, writeFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

export const STATUSES = ["open", "in-progress", "blocked", "review", "done"];
export const PRIORITIES = ["P0", "P1", "P2", "P3"];
export const AREAS = ["api", "web", "ops", "tools", "docs", "meta"];
export const FIELDS = [
  "id",
  "title",
  "status",
  "priority",
  "area",
  "owner",
  "claimed_at",
  "created_at",
  "completed_at",
  "branch",
  "depends_on",
  "scope",
];
export const STALE_CLAIM_HOURS = 24;

const LIST_FIELDS = new Set(["depends_on", "scope"]);
const HOLDS_SCOPE = new Set(["in-progress", "review"]);
const ID_PATTERN = /^\d{4}-\d{2}-\d{2}-[a-z0-9]+(?:-[a-z0-9]+)*$/;
const STAMP_PATTERN = /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$/;

const openDir = (root) => path.join(root, "tasks", "open");
const doneDir = (root) => path.join(root, "tasks", "done");
const boardFile = (root) => path.join(root, "tasks", "BOARD.md");

export function stamp(now) {
  return now.toISOString().replace(/\.\d{3}Z$/, "Z");
}

export function slugify(title) {
  return title
    .toLowerCase()
    .normalize("NFKD")
    .replace(/[^a-z0-9]+/g, "-")
    .split("-")
    .filter(Boolean)
    .slice(0, 6)
    .join("-");
}

export function parseTask(source, file = "task") {
  const normalized = source.replace(/\r\n/g, "\n");
  if (!normalized.startsWith("---\n")) throw new Error(`${file}: the file must start with a '---' front matter block`);
  const end = normalized.indexOf("\n---\n", 3);
  if (end === -1) throw new Error(`${file}: the front matter block is never closed by '---'`);
  const task = {};
  let listField = null;
  for (const line of normalized.slice(4, end + 1).split("\n").slice(0, -1)) {
    if (line.startsWith("  - ")) {
      if (!listField) throw new Error(`${file}: list item '${line.trim()}' does not belong to a list field`);
      const item = line.slice(4).trim();
      if (!item) throw new Error(`${file}: '${listField}' has an empty list item`);
      task[listField].push(item);
      continue;
    }
    const match = /^([a-z_]+):(.*)$/.exec(line);
    if (!match) throw new Error(`${file}: cannot read front matter line '${line}'`);
    const [, key, rest] = match;
    if (!FIELDS.includes(key)) throw new Error(`${file}: unknown front matter field '${key}'`);
    if (key in task) throw new Error(`${file}: front matter field '${key}' appears twice`);
    const value = rest.trim();
    listField = null;
    if (!LIST_FIELDS.has(key)) {
      task[key] = value;
      continue;
    }
    if (value && value !== "[]") throw new Error(`${file}: '${key}' takes '[]' or indented '  - ' items`);
    task[key] = [];
    if (!value) listField = key;
  }
  const missing = FIELDS.filter((field) => !(field in task));
  if (missing.length) throw new Error(`${file}: front matter is missing ${missing.join(", ")}`);
  task.body = normalized.slice(end + 5);
  return task;
}

export function serializeTask(task) {
  const lines = ["---"];
  for (const field of FIELDS) {
    if (!LIST_FIELDS.has(field)) {
      lines.push(`${field}: ${task[field] ?? ""}`.trimEnd());
      continue;
    }
    const items = task[field] ?? [];
    if (!items.length) {
      lines.push(`${field}: []`);
      continue;
    }
    lines.push(`${field}:`);
    for (const item of items) lines.push(`  - ${item}`);
  }
  lines.push("---");
  const body = (task.body ?? "").replace(/^\n+/, "").replace(/\s+$/, "");
  return `${lines.join("\n")}\n\n${body}\n`;
}

export function loadTasks(root) {
  const tasks = [];
  for (const folder of ["open", "done"]) {
    const dir = folder === "open" ? openDir(root) : doneDir(root);
    if (!existsSync(dir)) continue;
    for (const name of readdirSync(dir).filter((entry) => entry.endsWith(".md")).sort()) {
      const file = `tasks/${folder}/${name}`;
      tasks.push({ ...parseTask(readFileSync(path.join(dir, name), "utf8"), file), folder, name, file });
    }
  }
  return tasks;
}

function normalizeScope(entry) {
  return entry.replace(/\/\*\*$/, "").replace(/\/+$/, "");
}

export function scopesOverlap(left, right) {
  const first = normalizeScope(left);
  const second = normalizeScope(right);
  return first === second || first.startsWith(`${second}/`) || second.startsWith(`${first}/`);
}

export function sharedScope(left, right) {
  return left.scope.filter((entry) => right.scope.some((other) => scopesOverlap(entry, other)));
}

function claimAgeHours(task, now) {
  if (!task.claimed_at) return 0;
  return (now.getTime() - Date.parse(task.claimed_at)) / 3_600_000;
}

export function isStale(task, now) {
  return HOLDS_SCOPE.has(task.status) && claimAgeHours(task, now) >= STALE_CLAIM_HOURS;
}

function dependencyCycle(byId) {
  const state = new Map();
  const stack = [];
  let cycle = null;
  const visit = (id) => {
    if (cycle || state.get(id) === "left") return;
    if (state.get(id) === "entered") {
      cycle = [...stack.slice(stack.indexOf(id)), id];
      return;
    }
    state.set(id, "entered");
    stack.push(id);
    for (const next of byId.get(id)?.depends_on ?? []) if (byId.has(next)) visit(next);
    stack.pop();
    state.set(id, "left");
  };
  for (const id of byId.keys()) visit(id);
  return cycle;
}

export function validate(tasks, { now = new Date() } = {}) {
  const errors = [];
  const warnings = [];
  const byId = new Map();
  for (const task of tasks) {
    const where = task.file;
    if (byId.has(task.id)) errors.push(`${where}: task id '${task.id}' is already used by ${byId.get(task.id).file}`);
    else byId.set(task.id, task);
    if (!ID_PATTERN.test(task.id)) errors.push(`${where}: id must look like 2026-09-05-short-slug`);
    else if (task.name !== `${task.id}.md`) errors.push(`${where}: the file name must match the id (${task.id}.md)`);
    if (!task.title) errors.push(`${where}: title is required`);
    if (!STATUSES.includes(task.status)) errors.push(`${where}: status must be one of ${STATUSES.join(", ")}`);
    if (!PRIORITIES.includes(task.priority)) errors.push(`${where}: priority must be one of ${PRIORITIES.join(", ")}`);
    if (!AREAS.includes(task.area)) errors.push(`${where}: area must be one of ${AREAS.join(", ")}`);
    if (!STAMP_PATTERN.test(task.created_at)) errors.push(`${where}: created_at must be a UTC stamp like 2026-09-05T08:30:00Z`);
    const finished = task.status === "done";
    if (STATUSES.includes(task.status) && finished !== (task.folder === "done")) {
      errors.push(`${where}: a ${task.status} task belongs in tasks/${finished ? "done" : "open"}/`);
    }
    if (finished && !STAMP_PATTERN.test(task.completed_at)) errors.push(`${where}: a done task needs a completed_at stamp`);
    if (!finished && task.completed_at) errors.push(`${where}: completed_at is only set once the task is done`);
    if (Boolean(task.owner) !== Boolean(task.claimed_at)) errors.push(`${where}: owner and claimed_at are always set together`);
    if (task.claimed_at && !STAMP_PATTERN.test(task.claimed_at)) errors.push(`${where}: claimed_at must be a UTC stamp like 2026-09-05T08:30:00Z`);
    if (task.status === "open" && task.owner) errors.push(`${where}: an open task has no owner; claim it or release it`);
    if (HOLDS_SCOPE.has(task.status) && !task.owner) errors.push(`${where}: a ${task.status} task needs an owner`);
    if (!task.scope.length) errors.push(`${where}: scope needs at least one path this task is allowed to change`);
    for (const entry of task.scope) {
      if (entry.startsWith("/") || entry.split("/").includes("..")) {
        errors.push(`${where}: scope entry '${entry}' must be a repository-relative path`);
      }
    }
    if (!task.body.trim()) errors.push(`${where}: the body must describe the work`);
  }
  for (const task of tasks) {
    for (const id of task.depends_on) {
      if (id === task.id) errors.push(`${task.file}: a task cannot depend on itself`);
      else if (!byId.has(id)) errors.push(`${task.file}: depends_on '${id}' is not a task`);
    }
  }
  const cycle = dependencyCycle(byId);
  if (cycle) errors.push(`tasks: dependency cycle ${cycle.join(" -> ")}`);
  const active = tasks.filter((task) => HOLDS_SCOPE.has(task.status));
  for (const task of active) {
    if (isStale(task, now)) {
      warnings.push(`${task.file}: ${task.owner} has held this task for ${Math.floor(claimAgeHours(task, now))}h; it can be claimed by someone else`);
    }
  }
  for (let index = 0; index < active.length; index += 1) {
    for (let other = index + 1; other < active.length; other += 1) {
      const shared = sharedScope(active[index], active[other]);
      if (shared.length) {
        warnings.push(`${active[index].id} and ${active[other].id} are both active and both cover ${shared.join(", ")}`);
      }
    }
  }
  return { errors, warnings };
}

function comparePriority(left, right) {
  return (
    PRIORITIES.indexOf(left.priority) - PRIORITIES.indexOf(right.priority) ||
    left.created_at.localeCompare(right.created_at) ||
    left.id.localeCompare(right.id)
  );
}

export function blockedReason(task, byId) {
  const waiting = task.depends_on.filter((id) => byId.get(id)?.status !== "done");
  return waiting.length ? `depends on ${waiting.join(", ")}` : "";
}

export function selectReady(tasks, { area = "" } = {}) {
  const byId = new Map(tasks.map((task) => [task.id, task]));
  const held = tasks.filter((task) => HOLDS_SCOPE.has(task.status));
  return tasks
    .filter((task) => task.status === "open")
    .filter((task) => !area || task.area === area)
    .filter((task) => !blockedReason(task, byId))
    .filter((task) => !held.some((other) => sharedScope(task, other).length))
    .sort(comparePriority);
}

function cell(value) {
  return String(value ?? "").replaceAll("|", "\\|");
}

function link(task) {
  return `[${cell(task.title)}](${task.folder}/${task.name})`;
}

function table(header, rows) {
  if (!rows.length) return ["_Nothing here._"];
  return [`| ${header.join(" | ")} |`, `| ${header.map(() => "---").join(" | ")} |`, ...rows.map((row) => `| ${row.join(" | ")} |`)];
}

// Deliberately free of timestamps and of anything else that changes on its own: the board
// is a pure function of the task files, so `tasks check` can prove it is up to date.
export function renderBoard(tasks) {
  const byId = new Map(tasks.map((task) => [task.id, task]));
  const counts = Object.fromEntries(STATUSES.map((status) => [status, tasks.filter((task) => task.status === status).length]));
  const ready = selectReady(tasks);
  const readyIds = new Set(ready.map((task) => task.id));
  const waiting = tasks.filter((task) => task.status === "open" && !readyIds.has(task.id)).sort(comparePriority);
  const active = tasks.filter((task) => task.status === "in-progress").sort(comparePriority);
  const review = tasks.filter((task) => task.status === "review").sort(comparePriority);
  const blocked = tasks.filter((task) => task.status === "blocked").sort(comparePriority);
  const finished = tasks.filter((task) => task.status === "done").sort((left, right) => right.completed_at.localeCompare(left.completed_at));

  const lines = [
    "# Task board",
    "",
    "<!-- Generated by tools/tasks.mjs. Run `npm run tasks:board` instead of editing this file by hand. -->",
    "",
    "Every unfinished task is one file in [`open/`](open); finished tasks move to [`done/`](done).",
    "Read [`README.md`](README.md) before claiming anything.",
    "",
    `**${counts.open} open · ${counts["in-progress"]} in progress · ${counts.blocked} blocked · ${counts.review} in review · ${counts.done} done**`,
    "",
    "## Ready to claim",
    "",
    "Nothing here is owned, blocked by a dependency, or overlapping active work. Take the top one.",
    "",
    ...table(
      ["Priority", "Task", "Area", "Scope"],
      ready.map((task) => [task.priority, link(task), task.area, task.scope.map((entry) => `\`${cell(entry)}\``).join("<br>")]),
    ),
    "",
    "## In progress",
    "",
    ...table(
      ["Task", "Owner", "Claimed (UTC)", "Branch"],
      active.map((task) => [link(task), cell(task.owner), cell(task.claimed_at), task.branch ? `\`${cell(task.branch)}\`` : "—"]),
    ),
    "",
    "## In review",
    "",
    ...table(
      ["Task", "Owner", "Branch"],
      review.map((task) => [link(task), cell(task.owner), task.branch ? `\`${cell(task.branch)}\`` : "—"]),
    ),
    "",
    "## Waiting",
    "",
    ...table(
      ["Priority", "Task", "Waiting on"],
      [...blocked, ...waiting].map((task) => [
        task.priority,
        link(task),
        cell(blockedReason(task, byId) || (task.status === "blocked" ? "see the task notes" : "active work in the same scope")),
      ]),
    ),
    "",
    "## Recently finished",
    "",
    ...(finished.length
      ? finished.slice(0, 10).map((task) => `- ${task.completed_at.slice(0, 10)} ${link(task)}`)
      : ["_Nothing here._"]),
    "",
  ];
  return `${lines.join("\n")}`;
}

function writeTask(root, task) {
  const dir = task.status === "done" ? doneDir(root) : openDir(root);
  mkdirSync(dir, { recursive: true });
  writeFileSync(path.join(dir, `${task.id}.md`), serializeTask(task));
}

export function writeBoard(root) {
  writeFileSync(boardFile(root), renderBoard(loadTasks(root)));
}

function findTask(root, id) {
  if (!id) throw new Error("this command needs a task id");
  const task = loadTasks(root).find((candidate) => candidate.id === id);
  if (!task) throw new Error(`no task '${id}'; run 'npm run tasks -- list'`);
  return task;
}

function describe(task, now) {
  const held = task.owner ? ` (${task.owner}${isStale(task, now) ? ", stale" : ""})` : "";
  return `${task.priority}  ${task.status.padEnd(11)} ${task.id.padEnd(42)} ${task.area.padEnd(5)} ${task.title}${held}`;
}

function commandList(root, options, now) {
  const tasks = loadTasks(root)
    .filter((task) => (options.status ? task.status === options.status : task.status !== "done"))
    .filter((task) => !options.area || task.area === options.area)
    .filter((task) => !options.owner || task.owner === options.owner)
    .sort(comparePriority);
  if (!tasks.length) return { code: 0, lines: ["No task matches."] };
  return { code: 0, lines: tasks.map((task) => describe(task, now)) };
}

function commandNext(root, options, now) {
  const tasks = loadTasks(root);
  const ready = selectReady(tasks, { area: options.area });
  if (!ready.length) {
    const where = options.area ? ` in ${options.area}` : "";
    const open = tasks.filter((task) => task.status === "open" && (!options.area || task.area === options.area));
    return {
      code: 0,
      lines: open.length
        ? [
            `Nothing${where} is ready to claim right now.`,
            "Every open task is waiting on a dependency or on files another agent is changing — see 'tasks list'.",
          ]
        : [
            `The backlog has no open task${where}.`,
            "File one with: npm run tasks -- new --title \"...\" --area <area> --scope <paths>",
          ],
    };
  }
  const [task] = ready;
  return {
    code: 0,
    lines: [
      describe(task, now),
      `  file:  tasks/open/${task.name}`,
      `  scope: ${task.scope.join(", ")}`,
      `  claim: npm run tasks -- claim ${task.id} --owner <your-agent-name>`,
    ],
  };
}

function commandNew(root, options, now) {
  if (!options.title) throw new Error("'new' needs --title");
  const slug = options.slug ? slugify(options.slug) : slugify(options.title);
  if (!slug) throw new Error("the title has no ASCII words to build an id from; pass --slug short-english-slug");
  if (!options.area) throw new Error(`'new' needs --area (${AREAS.join(", ")})`);
  if (!AREAS.includes(options.area)) throw new Error(`--area must be one of ${AREAS.join(", ")}`);
  const priority = options.priority ?? "P2";
  if (!PRIORITIES.includes(priority)) throw new Error(`--priority must be one of ${PRIORITIES.join(", ")}`);
  const scope = (options.scope ?? "").split(",").map((entry) => entry.trim()).filter(Boolean);
  if (!scope.length) throw new Error("'new' needs --scope with the paths this task may change, comma separated");
  const day = stamp(now).slice(0, 10);
  // Two agents filing a task on the same day must not collide the way sequential ids do.
  let id = `${day}-${slug}`;
  for (let suffix = 2; existsSync(path.join(openDir(root), `${id}.md`)) || existsSync(path.join(doneDir(root), `${id}.md`)); suffix += 1) {
    id = `${day}-${slug}-${suffix}`;
  }
  const task = {
    id,
    title: options.title,
    status: "open",
    priority,
    area: options.area,
    owner: "",
    claimed_at: "",
    created_at: stamp(now),
    completed_at: "",
    branch: "",
    depends_on: (options.depends_on ?? "").split(",").map((entry) => entry.trim()).filter(Boolean),
    scope,
    body: `# ${options.title}

## Why

Describe the problem in the terms someone who has never seen it would need.

## Definition of done

- [ ] The observable outcome, not the implementation.

## Steps

- [ ] First sub-task.
- [ ] Second sub-task.

## How to verify

The exact commands or clicks that prove it works.

## Notes

Findings, decisions and dead ends, so the next agent does not repeat them.
`,
  };
  writeTask(root, task);
  writeBoard(root);
  return { code: 0, lines: [`Created tasks/open/${id}.md`, `Claim it with: npm run tasks -- claim ${id} --owner <your-agent-name>`] };
}

function commandClaim(root, id, options, now) {
  const task = findTask(root, id);
  const owner = options.owner;
  if (!owner) throw new Error("'claim' needs --owner, the name of the model or person taking the task");
  if (task.status === "done") throw new Error(`${task.id} is already done`);
  if (task.status === "blocked") throw new Error(`${task.id} is blocked; resolve the blocker and run 'status ${task.id} open' first`);
  if (task.owner && task.owner !== owner && !isStale(task, now) && !options.force) {
    throw new Error(`${task.id} is held by ${task.owner} since ${task.claimed_at}; pick another task or pass --force`);
  }
  const byId = new Map(loadTasks(root).map((entry) => [entry.id, entry]));
  const waiting = blockedReason(task, byId);
  if (waiting && !options.force) throw new Error(`${task.id} ${waiting}; finish those first or pass --force`);
  const lines = [];
  const takeover = Boolean(task.owner) && task.owner !== owner;
  if (takeover) lines.push(`Taking over a stale claim from ${task.owner} (held since ${task.claimed_at}).`);
  const overlapping = loadTasks(root)
    .filter((other) => other.id !== task.id && HOLDS_SCOPE.has(other.status) && sharedScope(task, other).length)
    .map((other) => `${other.id} (${other.owner})`);
  // Refusing here is the whole point of the board: two agents editing the same files at the
  // same time is the one thing a task list cannot untangle afterwards.
  if (overlapping.length && !options.force) {
    throw new Error(`${task.id} covers files already being changed by ${overlapping.join(", ")}; run 'next' for a task that is free, or pass --force`);
  }
  const branch = options.branch ?? (takeover ? "" : task.branch);
  writeTask(root, { ...task, status: "in-progress", owner, claimed_at: stamp(now), branch });
  writeBoard(root);
  return { code: 0, lines: [...lines, `${task.id} is yours. Update it as you go and finish with 'npm run tasks -- done ${task.id}'.`] };
}

function commandRelease(root, id) {
  const task = findTask(root, id);
  if (task.status === "done") throw new Error(`${task.id} is already done`);
  writeTask(root, { ...task, status: "open", owner: "", claimed_at: "" });
  writeBoard(root);
  return { code: 0, lines: [`${task.id} is open again.`] };
}

function commandStatus(root, id, value, options, now) {
  const task = findTask(root, id);
  if (!STATUSES.includes(value)) throw new Error(`status must be one of ${STATUSES.join(", ")}`);
  if (value === "done") throw new Error(`use 'npm run tasks -- done ${task.id}' so the file is archived`);
  if (task.status === "done") throw new Error(`${task.id} is already done`);
  if (HOLDS_SCOPE.has(value) && !task.owner && !options.owner) {
    throw new Error(`a ${value} task needs an owner; claim it first or pass --owner NAME`);
  }
  const next = { ...task, status: value, branch: options.branch ?? task.branch };
  if (options.owner) {
    next.owner = options.owner;
    next.claimed_at = task.claimed_at || stamp(now);
  }
  if (value === "open") {
    next.owner = "";
    next.claimed_at = "";
  }
  writeTask(root, next);
  writeBoard(root);
  return { code: 0, lines: [`${task.id} is now ${value}.`] };
}

function commandDone(root, id, now) {
  const task = findTask(root, id);
  if (task.status === "done") return { code: 0, lines: [`${task.id} was already done.`] };
  const unchecked = (task.body.match(/^\s*- \[ \]/gm) ?? []).length;
  writeTask(root, { ...task, status: "done", completed_at: stamp(now) });
  rmSync(path.join(openDir(root), `${task.id}.md`), { force: true });
  writeBoard(root);
  const lines = [`${task.id} moved to tasks/done/.`];
  if (unchecked) lines.push(`Note: ${unchecked} checklist item(s) are still unticked in the archived file.`);
  return { code: 0, lines };
}

function commandCheck(root, now) {
  const tasks = loadTasks(root);
  const { errors, warnings } = validate(tasks, { now });
  const expected = renderBoard(tasks);
  const current = existsSync(boardFile(root)) ? readFileSync(boardFile(root), "utf8") : "";
  if (current !== expected) errors.push("tasks/BOARD.md is out of date; run 'npm run tasks:board' (never hand-merge it)");
  const lines = [...errors, ...warnings.map((warning) => `warning: ${warning}`)];
  if (errors.length) return { code: 1, lines };
  lines.push(`Validated ${tasks.length} task file(s); the board is up to date.`);
  return { code: 0, lines };
}

export function helpText() {
  return `Mokaair task board

Usage:
  npm run tasks -- <command> [options]

Commands:
  list [--status S] [--area A] [--owner NAME]   Show tasks (open ones by default)
  next [--area A]                               The best task nobody else is on
  new --title T --area A --scope a,b            File a new task
       [--priority P2] [--depends-on id,id] [--slug s]
  claim <id> --owner NAME [--branch B] [--force] Take a task
  release <id>                                  Give it back
  status <id> <open|in-progress|blocked|review> Move a task, optionally --owner/--branch
  done <id>                                     Archive it into tasks/done/
  board                                         Regenerate tasks/BOARD.md
  check                                         Validate every task and the board

Areas: ${AREAS.join(", ")}      Priorities: ${PRIORITIES.join(", ")}
A claim older than ${STALE_CLAIM_HOURS}h is stale and can be taken over without --force.
`;
}

export function runCommand(argv, { root, now = new Date() } = {}) {
  const { positional, options } = parseArgs(argv);
  const [command, ...rest] = positional;
  try {
    switch (command) {
      case undefined:
      case "help":
        return { code: 0, lines: [helpText()] };
      case "list":
        return commandList(root, options, now);
      case "next":
        return commandNext(root, options, now);
      case "new":
        return commandNew(root, options, now);
      case "claim":
        return commandClaim(root, rest[0], options, now);
      case "release":
        return commandRelease(root, rest[0]);
      case "status":
        return commandStatus(root, rest[0], rest[1], options, now);
      case "done":
        return commandDone(root, rest[0], now);
      case "board":
        writeBoard(root);
        return { code: 0, lines: ["Rewrote tasks/BOARD.md."] };
      case "check":
        return commandCheck(root, now);
      default:
        return { code: 1, lines: [`unknown command '${command}'`, helpText()] };
    }
  } catch (error) {
    return { code: 1, lines: [error.message] };
  }
}

export function parseArgs(argv) {
  const positional = [];
  const options = {};
  for (let index = 0; index < argv.length; index += 1) {
    const token = argv[index];
    if (!token.startsWith("--")) {
      positional.push(token);
      continue;
    }
    const raw = token.slice(2);
    const equals = raw.indexOf("=");
    const flag = (equals === -1 ? raw : raw.slice(0, equals)).replaceAll("-", "_");
    let value = equals === -1 ? null : raw.slice(equals + 1);
    if (value === null) {
      const next = argv[index + 1];
      if (next !== undefined && !next.startsWith("--")) {
        value = next;
        index += 1;
      } else value = "true";
    }
    options[flag] = value;
  }
  return { positional, options };
}

const isMain = process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url);
if (isMain) {
  const now = process.env.TASKS_NOW ? new Date(process.env.TASKS_NOW) : new Date();
  const result = runCommand(process.argv.slice(2), { root: path.resolve(import.meta.dirname, ".."), now });
  const text = result.lines.join("\n");
  if (result.code) console.error(text);
  else console.log(text);
  process.exitCode = result.code;
}
