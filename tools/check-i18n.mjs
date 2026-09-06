import { execFileSync } from "node:child_process";
import { readFileSync, readdirSync } from "node:fs";
import { join, relative, resolve } from "node:path";

import { duplicateKeys } from "./json-duplicate-keys.mjs";

const root = resolve(import.meta.dirname, "..");
const messagesRoot = join(root, "apps", "web", "messages");
const locales = ["en", "ja", "ko", "zh-TW", "zh-CN"];

function flatten(value, prefix = "", result = new Map()) {
  for (const [key, child] of Object.entries(value)) {
    const path = prefix ? `${prefix}.${key}` : key;
    if (child && typeof child === "object" && !Array.isArray(child)) flatten(child, path, result);
    else result.set(path, String(child));
  }
  return result;
}

function parameters(message) {
  return [...message.matchAll(/\{([A-Za-z_][\w]*)/g)].map((match) => match[1]).sort();
}

const errors = [];
const namespaces = readdirSync(join(messagesRoot, locales[0])).filter((name) => name.endsWith(".json")).sort();
const referenceNamespaces = new Set(namespaces);
const reference = new Map();

for (const namespace of namespaces) {
  const parsed = JSON.parse(readFileSync(join(messagesRoot, locales[0], namespace), "utf8"));
  reference.set(namespace, flatten(parsed));
}

for (const locale of locales) {
  const localeNamespaces = readdirSync(join(messagesRoot, locale)).filter((name) => name.endsWith(".json")).sort();
  if (localeNamespaces.join("\n") !== namespaces.join("\n")) {
    errors.push(`${locale}: namespace files differ from en`);
    continue;
  }
  for (const namespace of referenceNamespaces) {
    const source = readFileSync(join(messagesRoot, locale, namespace), "utf8");
    // Read the text, not the parsed value: JSON.parse keeps the last of two identical keys
    // and reports nothing, so every check below this line is blind to a duplicate. All five
    // trips.json files carried two transfersCount entries for months without anything
    // displaying wrongly — the damage was that any tool round-tripping the file collapsed
    // the pair, and the collapse reached the diff looking like a copy change nobody made.
    for (const key of duplicateKeys(source)) {
      errors.push(`${locale}/${namespace}:${key}: duplicate key, JSON.parse silently keeps the last one`);
    }
    const localized = flatten(JSON.parse(source));
    const expected = reference.get(namespace);
    if ([...localized.keys()].sort().join("\n") !== [...expected.keys()].sort().join("\n")) {
      errors.push(`${locale}/${namespace}: translation keys differ from en`);
      continue;
    }
    for (const [key, sourceMessage] of expected) {
      if (parameters(localized.get(key)).join(",") !== parameters(sourceMessage).join(",")) {
        errors.push(`${locale}/${namespace}:${key}: ICU parameters differ from en`);
      }
    }
  }
}

function runGit(args) {
  return execFileSync("git", args, { cwd: root, encoding: "utf8" }).trim();
}

function hanRuns(source) {
  const counts = new Map();
  for (const value of source.match(/[\p{Script=Han}]+/gu) || []) {
    counts.set(value, (counts.get(value) || 0) + 1);
  }
  return counts;
}

let staged = false;
try {
  execFileSync("git", ["diff", "--cached", "--quiet"], { cwd: root });
} catch {
  staged = true;
}

if (process.env.CI || staged) {
  const base = process.env.CI ? "HEAD^" : "HEAD";
  const diffArgs = process.env.CI
    ? ["diff", "-M", "--name-status", base, "HEAD", "--", "apps/web"]
    : ["diff", "-M", "--cached", "--name-status", "--", "apps/web"];
  let changed = "";
  try { changed = runGit(diffArgs); } catch { /* first commit */ }
  for (const line of changed.split(/\r?\n/).filter(Boolean)) {
    const [status, first, second] = line.split("\t");
    if (status === "D") continue;
    const currentFile = status.startsWith("R") ? second : first;
    const previousFile = status.startsWith("R") ? first : currentFile;
    if (!/^apps\/web\/(app|components|lib)\//.test(currentFile) || !/\.(tsx?|jsx?)$/.test(currentFile) || /\.(test|spec)\.[jt]sx?$/.test(currentFile)) continue;
    const current = readFileSync(join(root, currentFile), "utf8");
    let previous = "";
    if (!status.startsWith("A")) {
      try { previous = runGit(["show", `${base}:${previousFile}`]); } catch { /* new file */ }
    }
    const before = hanRuns(previous);
    for (const [value, count] of hanRuns(current)) {
      if (count > (before.get(value) || 0)) {
        errors.push(`${relative(root, join(root, currentFile))}: newly added display text '${value}' must use a message catalog`);
      }
    }
  }
}

if (errors.length) {
  console.error(errors.join("\n"));
  process.exit(1);
}
console.log(`Validated ${locales.length} locales across ${namespaces.length} namespaces.`);
