import { execFileSync } from "node:child_process";
import { readFileSync, readdirSync } from "node:fs";
import { join, relative, resolve } from "node:path";
import { fileURLToPath } from "node:url";

import { IntlMessageFormat } from "intl-messageformat";

import { duplicateKeys } from "./json-duplicate-keys.mjs";

function flatten(value, prefix = "", result = new Map()) {
  for (const [key, child] of Object.entries(value)) {
    const path = prefix ? `${prefix}.${key}` : key;
    if (child && typeof child === "object" && !Array.isArray(child)) flatten(child, path, result);
    else result.set(path, String(child));
  }
  return result;
}

export function parameters(message) {
  const names = new Set();
  // Read ICU's arguments, not brace-shaped text: '{name}' is a literal. Inspect
  // every branch, since rendering sample values only visits one plural/select
  // option and cannot use string markers for number/date/time arguments.
  // Tags are outside this parameter check; help copy also has literal <slug> paths.
  const ast = new IntlMessageFormat(message, "en", undefined, { ignoreTag: true }).getAst();
  function visit(elements) {
    for (const element of elements) {
      // ICU node types 0 (literal) and 7 (#) do not introduce named arguments.
      // With ignoreTag, all other nodes are argument/number/date/time/select/plural.
      if (element.type !== 0 && element.type !== 7) names.add(element.value);
      for (const option of Object.values(element.options ?? {})) visit(option.value);
    }
  }
  visit(ast);
  return [...names].sort();
}

function lexicalParameters(message) {
  // Retain the existing token contract shared with the API and admin editor.
  // In particular, a translation must not lose/rename literal URL-template tokens
  // such as '{destination}', even though they are not runtime ICU arguments.
  return [...message.matchAll(/\{([A-Za-z_][\w]*)/g)].map((match) => match[1]).sort().join(",");
}

export function checkI18n(root = resolve(import.meta.dirname, "..")) {
  const messagesRoot = join(root, "apps", "web", "messages");
  const locales = ["en", "ja", "ko", "zh-TW", "zh-CN"];
  const errors = [];
  const namespaces = readdirSync(join(messagesRoot, locales[0])).filter((name) => name.endsWith(".json")).sort();
  const referenceNamespaces = new Set(namespaces);
  const reference = new Map();
  const referenceParameters = new Map();

  for (const namespace of namespaces) {
    const parsed = JSON.parse(readFileSync(join(messagesRoot, locales[0], namespace), "utf8"));
    const messages = flatten(parsed);
    reference.set(namespace, messages);
    const expectedParameters = new Map();
    for (const [key, message] of messages) {
      try {
        expectedParameters.set(key, {
          arguments: parameters(message).join(","),
          tokens: lexicalParameters(message),
        });
      } catch (error) {
        errors.push(`en/${namespace}:${key}: invalid ICU message: ${error.message}`);
      }
    }
    referenceParameters.set(namespace, expectedParameters);
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
      if (locale === "en") continue; // Parsed above, with errors attributed to en.
      for (const key of expected.keys()) {
        try {
          const actual = parameters(localized.get(key)).join(",");
          const wanted = referenceParameters.get(namespace).get(key);
          if (wanted !== undefined && (actual !== wanted.arguments || lexicalParameters(localized.get(key)) !== wanted.tokens)) {
            errors.push(`${locale}/${namespace}:${key}: ICU parameters differ from en`);
          }
        } catch (error) {
          errors.push(`${locale}/${namespace}:${key}: invalid ICU message: ${error.message}`);
        }
      }
    }
  }

  // Administrator copy overrides are keyed by namespace, and the API keeps its own allowlist
  // because it never sees these files. A namespace added here but not there is silently
  // uneditable; one removed here but left there lets an override outlive its catalog.
  const editable = namespaces.map((name) => name.replace(/\.json$/, "")).filter((name) => name !== "legacy");
  const allowlists = [
    ["apps/api/app/ui_text/schemas.py", /UI_TEXT_NAMESPACES:[^=]*=\s*\(([^)]*)\)/],
    ["apps/web/lib/ui-text.ts", /EDITABLE_NAMESPACES\s*=\s*\[([^\]]*)\]/],
  ];
  for (const [file, pattern] of allowlists) {
    const source = readFileSync(join(root, file), "utf8");
    const declared = (source.match(pattern)?.[1].match(/"([A-Za-z]+)"/g) || [])
      .map((quoted) => quoted.slice(1, -1))
      .sort();
    if (declared.join(",") !== [...editable].sort().join(",")) {
      errors.push(
        `${file}: the editable namespace allowlist differs from apps/web/messages minus legacy ` +
          `(missing: ${editable.filter((name) => !declared.includes(name)).join(", ") || "none"}; ` +
          `extra: ${declared.filter((name) => !editable.includes(name)).join(", ") || "none"})`,
      );
    }
  }

  // The copy editor names every group it can edit in a select. A namespace with no entry
  // here renders its raw key path as the option label, which no other check would catch.
  const described = Object.keys(
    JSON.parse(readFileSync(join(messagesRoot, locales[0], "admin.json"), "utf8")).uiText
      ?.namespaces ?? {},
  ).sort();
  if (described.join(",") !== [...editable].sort().join(",")) {
    errors.push(
      `admin.json: uiText.namespaces does not describe every editable namespace ` +
        `(missing: ${editable.filter((name) => !described.includes(name)).join(", ") || "none"}; ` +
        `extra: ${described.filter((name) => !editable.includes(name)).join(", ") || "none"})`,
    );
  }

  function runGit(args) {
    return execFileSync("git", args, { cwd: root, encoding: "utf8", stdio: ["ignore", "pipe", "pipe"] }).trim();
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
    execFileSync("git", ["diff", "--cached", "--quiet"], { cwd: root, stdio: ["ignore", "pipe", "pipe"] });
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

  return { errors, localeCount: locales.length, namespaceCount: namespaces.length };
}

if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const { errors, localeCount, namespaceCount } = checkI18n();
  if (errors.length) {
    console.error(errors.join("\n"));
    process.exitCode = 1;
  } else {
    console.log(`Validated ${localeCount} locales across ${namespaceCount} namespaces.`);
  }
}
