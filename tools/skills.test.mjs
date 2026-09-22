/**
 * Skills that Codex and Claude Code share.
 *
 * Codex discovers a repository skill at `.agents/skills/<name>/SKILL.md`; Claude Code only at
 * `.claude/skills/<name>/SKILL.md`. Neither reads the other's directory, SKILL.md has no import
 * mechanism, and a git symlink does not survive a Windows checkout — so the Claude copy is a
 * byte-identical duplicate of the canonical file, and this test is what keeps the two in step.
 * Everything else (references, scripts) lives once, under `.agents/`, and the body points at it
 * by repository-root path so either harness finds it from any working directory.
 *
 * The other checks encode the contract both harnesses accept. Codex's validator refuses any
 * frontmatter key outside its allow-list, angle brackets in the description, or more than 1,024
 * characters of it; Claude Code substitutes `$ARGUMENTS` and Codex does not. A skill that names
 * a path on one machine, or a person's mailbox, works for one person and misleads everyone else
 * without failing anywhere — which is why this is a test and not a convention.
 */
import assert from "node:assert/strict";
import test from "node:test";
import { existsSync, readdirSync, readFileSync } from "node:fs";
import { join, relative } from "node:path";
import { fileURLToPath } from "node:url";
import { load as parseYaml } from "js-yaml";

const ROOT = fileURLToPath(new URL("../", import.meta.url));
const CANONICAL = join(ROOT, ".agents", "skills");
const CLAUDE = join(ROOT, ".claude", "skills");

// What Codex's `quick_validate.py` allows in the frontmatter. Claude Code ignores keys it does
// not know, so staying inside this set is what keeps one file valid for both.
const SHARED_KEYS = new Set(["name", "description", "license", "allowed-tools", "metadata"]);
const DESCRIPTION_LIMIT = 1024;
const BODY_LINE_LIMIT = 300;
// The editorial mailbox is part of the User-Agent every fetch must carry; any other address is
// somebody's personal one.
const EDITORIAL_MAILBOX = "support@mokaair.com";
const MAILBOX = /[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}/g;
const MACHINE_PATH = /C:\\Users|\/c\/Users|\/Users\/|\/home\/|AppData|mokaair-work/;
// A repository path as prose or code mentions it: a top-level directory this repository has,
// then anything path-like. Placeholders such as `<ROOT>/docs/x.md` are unwrapped first.
const PLACEHOLDER_PREFIX = /<[A-Z_]+>\//g;
const REPO_PATH = /(?<![\w./-])((?:\.agents|\.claude|docs|apps|ops|tools|tasks)\/[\w./-]+)/g;
const TRAILING_PUNCTUATION = /[.,;:)」』`]+$/u;
const TEXT_FILES = /\.(md|py|yaml|yml|json|mjs|txt)$/;

function skillNames(base) {
  if (!existsSync(base)) return [];
  return readdirSync(base, { withFileTypes: true })
    .filter((entry) => entry.isDirectory() && existsSync(join(base, entry.name, "SKILL.md")))
    .map((entry) => entry.name)
    .sort();
}

function walk(dir) {
  return readdirSync(dir, { withFileTypes: true }).flatMap((entry) => {
    const path = join(dir, entry.name);
    return entry.isDirectory() ? walk(path) : [path];
  });
}

function textFiles(name) {
  return walk(join(CANONICAL, name)).filter((file) => TEXT_FILES.test(file));
}

function frontmatter(text) {
  const match = /^---\r?\n([\s\S]*?)\r?\n---\r?\n/.exec(text);
  assert.ok(match, "SKILL.md must start with a YAML frontmatter block");
  const data = parseYaml(match[1]);
  assert.ok(data && typeof data === "object", "frontmatter must be a YAML mapping");
  return { data, body: text.slice(match[0].length) };
}

const skills = skillNames(CANONICAL);

test("at least one shared skill exists, so the scan itself is not broken", () => {
  assert.ok(skills.length > 0, `no skill under ${relative(ROOT, CANONICAL)}`);
});

test("every shared skill has a byte-identical copy for Claude Code, and nothing lives only there", () => {
  for (const name of skills) {
    const canonical = join(CANONICAL, name, "SKILL.md");
    const copy = join(CLAUDE, name, "SKILL.md");
    const fix = `cp ${relative(ROOT, canonical)} ${relative(ROOT, copy)}`;
    assert.ok(existsSync(copy), `missing ${relative(ROOT, copy)}; run: ${fix}`);
    assert.ok(
      readFileSync(canonical).equals(readFileSync(copy)),
      `${relative(ROOT, copy)} differs from the canonical file; run: ${fix}`,
    );
  }
  assert.deepEqual(
    skillNames(CLAUDE),
    skills,
    "every skill under .claude/skills must be the copy of one under .agents/skills",
  );
});

test("frontmatter stays inside what both harnesses accept", () => {
  for (const name of skills) {
    const { data } = frontmatter(readFileSync(join(CANONICAL, name, "SKILL.md"), "utf8"));
    const extra = Object.keys(data).filter((key) => !SHARED_KEYS.has(key));
    assert.deepEqual(extra, [], `${name}: frontmatter keys Codex refuses`);
    assert.equal(data.name, name, `${name}: the frontmatter name must equal the directory name`);
    assert.match(data.name, /^[a-z0-9]+(?:-[a-z0-9]+)*$/, `${name}: hyphen-case only`);
    assert.ok(data.name.length <= 64, `${name}: name longer than 64 characters`);
    assert.equal(typeof data.description, "string", `${name}: description must be a string`);
    const description = data.description.trim();
    assert.ok(
      description.length > 0 && description.length <= DESCRIPTION_LIMIT,
      `${name}: description is ${description.length} characters; Codex allows ${DESCRIPTION_LIMIT}`,
    );
    assert.ok(!/[<>]/.test(description), `${name}: Codex refuses angle brackets in the description`);
  }
});

test("every repository path a skill mentions exists", () => {
  const missing = [];
  for (const name of skills) {
    for (const file of textFiles(name)) {
      const text = readFileSync(file, "utf8").replace(PLACEHOLDER_PREFIX, "");
      for (const match of text.matchAll(REPO_PATH)) {
        const path = match[1].replace(TRAILING_PUNCTUATION, "");
        if (!existsSync(join(ROOT, path))) missing.push(`${relative(ROOT, file)}: ${path}`);
      }
    }
  }
  assert.deepEqual(missing, [], "paths that do not exist; rename them or point at what replaced them");
});

test("no machine path, personal mailbox or harness-only placeholder in a skill", () => {
  const offences = [];
  for (const name of skills) {
    for (const file of textFiles(name)) {
      const text = readFileSync(file, "utf8");
      const where = relative(ROOT, file);
      if (MACHINE_PATH.test(text)) offences.push(`${where}: a path that only exists on one machine`);
      for (const mailbox of text.match(MAILBOX) ?? []) {
        if (mailbox !== EDITORIAL_MAILBOX) offences.push(`${where}: ${mailbox}`);
      }
      if (text.includes("$ARGUMENTS")) offences.push(`${where}: $ARGUMENTS is Claude-only`);
    }
  }
  assert.deepEqual(offences, []);
});

test("the entrypoint stays short enough to load on every invocation", () => {
  for (const name of skills) {
    const { body } = frontmatter(readFileSync(join(CANONICAL, name, "SKILL.md"), "utf8"));
    const lines = body.split(/\r?\n/).length;
    assert.ok(
      lines <= BODY_LINE_LIMIT,
      `${name}: SKILL.md body is ${lines} lines; move detail into references/`,
    );
  }
});
