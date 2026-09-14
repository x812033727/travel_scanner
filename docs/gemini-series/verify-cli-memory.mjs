/** Exercise the installed 0.59.0 memory implementation without auth or model calls.
 * Usage: node docs/gemini-series/verify-cli-memory.mjs /path/to/cli/bundle
 * The adapter supplies only Config getters; discovery/import/JIT/reload are the real CLI code.
 */
import assert from "node:assert/strict";
import { mkdtemp, mkdir, readFile, writeFile } from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import { pathToFileURL } from "node:url";

const bundle = path.resolve(process.argv[2]);
const packageInfo = JSON.parse(await readFile(path.join(bundle, "../package.json"), "utf8"));
assert.equal(packageInfo.version, "0.59.0", "Recheck module names and semantics when upgrading.");
const temporary = await mkdtemp(path.join(os.tmpdir(), "gemini-memory-lesson-"));
process.env.GEMINI_CLI_HOME = path.join(temporary, "isolated-user");
const project = path.join(temporary, "project");
const nested = path.join(project, "drafts");
for (const directory of [path.join(process.env.GEMINI_CLI_HOME, ".gemini"), path.join(project, ".git"), nested, path.join(project, "docs")]) {
  await mkdir(directory, { recursive: true });
}
await writeFile(path.join(process.env.GEMINI_CLI_HOME, ".gemini/GEMINI.md"), "GLOBAL_RULE: use Traditional Chinese.\n");
await writeFile(path.join(project, "GEMINI.md"), "PROJECT_RULE: preserve sources.\n@./docs/writing-rules.md\n");
await writeFile(path.join(project, "docs/writing-rules.md"), "IMPORT_RULE: mark unknown dates.\n");
await writeFile(path.join(nested, "GEMINI.md"), "NESTED_RULE: drafts need review.\n");
await writeFile(path.join(nested, "sample.txt"), "Fictional workshop announcement.\n");
const core = await import(pathToFileURL(path.join(bundle, "chunk-YSBB75DZ.js")));
let trusted = true;
let manager;
const config = {
  getExtensionLoader: () => ({ getExtensions: () => [] }),
  isTrustedFolder: () => trusted,
  getWorkspaceContext: () => ({ getDirectories: () => [project] }),
  getMemoryBoundaryMarkers: () => [".git"],
  storage: { getProjectMemoryDir: () => path.join(temporary, "unused-memory") },
  getImportFormat: () => "tree",
  getMcpClientManager: () => undefined,
  getMemoryContextManager: () => manager,
  getUserMemory: () => ({ global: manager.getGlobalMemory(), project: manager.getEnvironmentMemory() }),
  getGeminiMdFileCount: () => manager.getLoadedPaths().size,
  getGeminiMdFilePaths: () => [...manager.getLoadedPaths()],
  updateSystemInstructionIfInitialized: () => undefined,
};
manager = new core.MemoryContextManager(config);
await manager.refresh();
assert.match(manager.getGlobalMemory(), /GLOBAL_RULE/);
assert.match(manager.getEnvironmentMemory(), /PROJECT_RULE/);
assert.match(manager.getEnvironmentMemory(), /IMPORT_RULE/);
assert.doesNotMatch(manager.getEnvironmentMemory(), /NESTED_RULE/);
const initialFiles = config.getGeminiMdFileCount();
const jit = await manager.discoverContext(path.join(nested, "sample.txt"), [project]);
assert.match(jit, /NESTED_RULE/);
assert.equal(await manager.discoverContext(path.join(nested, "sample.txt"), [project]), "");
await writeFile(path.join(project, "GEMINI.md"), "PROJECT_RULE_UPDATED: keep dates unknown.\n");
const reload = await core.refreshMemory(config);
assert.match(reload.content, /reloaded successfully/);
assert.match(core.showMemory(config).content, /PROJECT_RULE_UPDATED/);
assert.doesNotMatch(core.showMemory(config).content, /IMPORT_RULE/);
assert.equal(config.getGeminiMdFileCount(), initialFiles);
trusted = false;
await manager.refresh();
assert.equal(manager.getEnvironmentMemory(), "");
assert.match(manager.getGlobalMemory(), /GLOBAL_RULE/);
assert.equal(await manager.discoverContext(path.join(nested, "sample.txt"), [project]), "");
const commandSource = await readFile(path.join(bundle, "chunk-CUTHWG3H.js"), "utf8");
assert.match(commandSource, /name: "reload",\s+altNames: \["refresh"\]/);
const report = {
  checkedOn: new Date().toISOString(), platform: process.platform, node: process.version,
  cli: packageInfo.version, method: "installed CLI memory implementation; no model call or interactive UI",
  passed: ["global", "project", "relative import", "nested JIT", "JIT deduplication", "reload after edit", "removed import cleared", "untrusted workspace isolation", "reload/refresh alias"],
};
await writeFile(new URL("./cli-memory-verification.json", import.meta.url), JSON.stringify(report, null, 2) + "\n");
console.log(JSON.stringify(report, null, 2));
