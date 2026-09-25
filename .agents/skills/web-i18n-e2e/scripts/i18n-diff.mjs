// Name the keys behind "translation keys differ from en" and the placeholders behind
// "ICU parameters differ from en". tools/check-i18n.mjs reports only the namespace for the
// first and skips the rest of that file; this prints every missing and extra key per locale.
//
//   node .agents/skills/web-i18n-e2e/scripts/i18n-diff.mjs            # every namespace
//   node .agents/skills/web-i18n-e2e/scripts/i18n-diff.mjs trips foods
//
// Read-only. Same flattening and placeholder expression as tools/check-i18n.mjs.
import { existsSync, readFileSync, readdirSync } from "node:fs";
import { join, resolve } from "node:path";

const root = resolve(import.meta.dirname, "..", "..", "..", "..");
const messages = join(root, "apps", "web", "messages");
const locales = ["ja", "ko", "zh-TW", "zh-CN"];

function flatten(value, prefix = "", result = new Map()) {
  for (const [key, child] of Object.entries(value)) {
    const path = prefix ? `${prefix}.${key}` : key;
    if (child && typeof child === "object" && !Array.isArray(child)) flatten(child, path, result);
    else result.set(path, String(child));
  }
  return result;
}

const parameters = (message) =>
  [...message.matchAll(/\{([A-Za-z_][\w]*)/g)].map((match) => match[1]).sort().join(",");

const requested = process.argv.slice(2);
const namespaces = requested.length
  ? requested
  : readdirSync(join(messages, "en")).filter((name) => name.endsWith(".json")).map((name) => name.slice(0, -5));

let problems = 0;
for (const namespace of namespaces) {
  const reference = flatten(JSON.parse(readFileSync(join(messages, "en", `${namespace}.json`), "utf8")));
  for (const locale of locales) {
    const file = join(messages, locale, `${namespace}.json`);
    if (!existsSync(file)) {
      console.log(`${locale}/${namespace}.json: file missing`);
      problems += 1;
      continue;
    }
    const localized = flatten(JSON.parse(readFileSync(file, "utf8")));
    for (const [key, message] of reference) {
      if (!localized.has(key)) {
        console.log(`${locale}/${namespace}: missing ${key}`);
        problems += 1;
      } else if (parameters(localized.get(key)) !== parameters(message)) {
        console.log(`${locale}/${namespace}:${key}: {${parameters(localized.get(key))}} but en has {${parameters(message)}}`);
        problems += 1;
      }
    }
    for (const key of localized.keys()) {
      if (!reference.has(key)) {
        console.log(`${locale}/${namespace}: extra ${key} (not in en)`);
        problems += 1;
      }
    }
  }
}
console.log(problems ? `${problems} difference(s).` : `No differences across ${namespaces.length} namespace(s).`);
process.exitCode = problems ? 1 : 0;
