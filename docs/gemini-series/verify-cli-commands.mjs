import assert from "node:assert/strict";
import { readFile, writeFile } from "node:fs/promises";
import path from "node:path";
import { pathToFileURL } from "node:url";

const bundle = path.resolve(process.argv[2]);
const version = JSON.parse(await readFile(path.join(bundle, "../package.json"), "utf8")).version;
assert.equal(version, "0.59.0");
// The loader detects release channel from cwd package metadata. Use the CLI package,
// not this repository's unrelated package.json.
process.chdir(bundle);
const { BuiltinCommandLoader } = await import(pathToFileURL(path.join(bundle, "chunk-CUTHWG3H.js")));
const { AuthType } = await import(pathToFileURL(path.join(bundle, "chunk-YSBB75DZ.js")));
const enabled = new Set(["isAgentsEnabled", "getExtensionsEnabled", "getEnableExtensionReloading", "getEnableHooksUI", "getMcpEnabled", "getFolderTrust", "isPlanEnabled", "isSkillsSupportEnabled", "isVoiceModeEnabled", "getCheckpointingEnabled"]);
const config = new Proxy({}, { get: (_, key) => key === "getSkillManager" ? () => ({ isAdminEnabled: () => true }) : key === "getContentGeneratorConfig" ? () => ({ authType: AuthType.LOGIN_WITH_GOOGLE }) : () => enabled.has(key) });
const raw = await new BuiltinCommandLoader(config).loadCommands(new AbortController().signal);
function summarize(command) {
  return { name: command.name, aliases: command.altNames || [], description: command.description, subcommands: (command.subCommands || []).map(summarize) };
}
const commands = raw.map(summarize);
const report = { version, checkedOn: new Date().toISOString(), platform: process.platform, method: "real BuiltinCommandLoader with optional user features enabled; command actions not executed", commands };
await writeFile(new URL("./cli-command-inventory.json", import.meta.url), JSON.stringify(report, null, 2) + "\n");
console.log(commands.map((entry) => `/${entry.name}${entry.aliases.length ? ` (${entry.aliases.join(", ")})` : ""}`).join("\n"));
