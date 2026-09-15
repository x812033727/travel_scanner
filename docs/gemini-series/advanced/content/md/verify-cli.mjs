/** Exercise the installed CLI implementation with isolated authored inputs, never a model. */
import assert from "node:assert/strict";
import { mkdtempSync, mkdirSync, readFileSync, writeFileSync, readdirSync, rmSync, existsSync } from "node:fs";
import { spawnSync } from "node:child_process";
import os from "node:os";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const examples = path.join(here, "examples");
const cli = path.resolve(process.argv[2] || "");
const pkg = JSON.parse(readFileSync(path.join(cli, "package.json"), "utf8"));
assert.equal(pkg.name, "@google/gemini-cli");
assert.equal(pkg.version, "0.59.0", "Revalidate bundle entry points before testing a different version.");
const temporary = mkdtempSync(path.join(os.tmpdir(), "gemini-md-real-cli-"));
assert.ok(temporary.startsWith(path.resolve(os.tmpdir()) + path.sep));
const isolated = path.join(temporary, "isolated-user");
const results = {};
const record = (n, item) => (results[n] ??= []).push(item);
const put = (file, value) => { mkdirSync(path.dirname(file), { recursive: true }); writeFileSync(file, typeof value === "string" ? value : JSON.stringify(value, null, 2) + "\n", "utf8"); };
function copy(source, target) {
  mkdirSync(target, { recursive: true });
  for (const entry of readdirSync(source, { withFileTypes: true })) {
    assert.ok(!entry.isSymbolicLink());
    const from = path.join(source, entry.name), to = path.join(target, entry.name);
    if (entry.isDirectory()) copy(from, to); else writeFileSync(to, readFileSync(from));
  }
}
const clean = (value) => {
  let text = String(value);
  for (const [source, replacement] of [[temporary, "<temporary>"], [cli, "<gemini-cli-0.59.0>"], [examples, "<examples>"], [here, "<authoring>"]]) {
    for (const spelling of [JSON.stringify(source).slice(1, -1), source, source.split(path.sep).join("/")]) text = text.split(spelling).join(replacement);
  }
  return text;
};
function run(command, args, cwd, expected = 0, env = process.env) {
  const result = spawnSync(command, args, { cwd, env, encoding: "utf8", windowsHide: true, timeout: 60000, maxBuffer: 2e6 });
  assert.equal(result.status, expected, clean(result.stderr || result.stdout || result.error));
  return clean(result.stdout + result.stderr);
}

// The process is disposable: no global user setting or credential is modified.
process.env.GEMINI_CLI_HOME = isolated;
process.env.GEMINI_CLI_SYSTEM_SETTINGS_PATH = path.join(temporary, "system.json");
process.env.GEMINI_CLI_SYSTEM_DEFAULTS_PATH = path.join(temporary, "defaults.json");
process.env.LESSON_MODEL = "offline-sentinel-not-a-real-model";
for (const key of Object.keys(process.env)) if (/^(GEMINI_API_KEY|GOOGLE_API_KEY|GOOGLE_APPLICATION_CREDENTIALS|GOOGLE_GENAI_USE_VERTEXAI)$/.test(key)) delete process.env[key];
globalThis.fetch = async () => { throw new Error("Cloud access is outside this local verification."); };
put(path.join(isolated, ".gemini/settings.json"), { telemetry: { enabled: false }, security: { folderTrust: { enabled: false } } });
put(process.env.GEMINI_CLI_SYSTEM_SETTINGS_PATH, {});
put(process.env.GEMINI_CLI_SYSTEM_DEFAULTS_PATH, {});

try {
  const core = await import(pathToFileURL(path.join(cli, "bundle/chunk-YSBB75DZ.js")));
  const settings = await import(pathToFileURL(path.join(cli, "bundle/chunk-LZ4UWPZ4.js")));
  const commands = await import(pathToFileURL(path.join(cli, "bundle/chunk-CUTHWG3H.js")));
  assert.ok(settings.USER_SETTINGS_PATH.startsWith(isolated + path.sep));
  const lab = path.join(temporary, "memory-lab");
  copy(path.join(examples, "69/memory-lab"), lab);
  copy(path.join(lab, "isolated-user/.gemini"), path.join(isolated, ".gemini"));
  const project = path.join(lab, "project");
  mkdirSync(path.join(project, ".git"));
  let trusted = true, manager;
  const config = {
    getExtensionLoader: () => ({ getExtensions: () => [] }), isTrustedFolder: () => trusted,
    getWorkspaceContext: () => ({ getDirectories: () => [project] }), getMemoryBoundaryMarkers: () => [".git"],
    storage: { getProjectMemoryDir: () => path.join(temporary, "unused-memory") }, getImportFormat: () => "tree",
    getMcpClientManager: () => undefined, getMemoryContextManager: () => manager,
    getUserMemory: () => ({ global: manager.getGlobalMemory(), project: manager.getEnvironmentMemory() }),
    getGeminiMdFileCount: () => manager.getLoadedPaths().size, getGeminiMdFilePaths: () => [...manager.getLoadedPaths()],
    updateSystemInstructionIfInitialized: () => undefined,
  };
  const markers = ["GLOBAL_RULE", "PROJECT_RULE", "IMPORT_RULE", "FRONTEND_RULE", "BACKEND_RULE"];
  function observe(step, expected, jit = "", expectedJit = []) {
    const text = core.showMemory(config).content;
    const actual = markers.filter((marker) => text.includes(marker));
    assert.deepEqual(actual, expected);
    const jitMarkers = markers.filter((marker) => jit.includes(marker));
    assert.deepEqual(jitMarkers, expectedJit);
    record(69, { step, memoryShowMarkers: actual, newToolContextMarkers: jitMarkers, fileCount: config.getGeminiMdFileCount() });
  }
  manager = new core.MemoryContextManager(config);
  await manager.refresh();
  observe("initial", markers.slice(0, 3));
  const frontendContext = await manager.discoverContext(path.join(project, "frontend/sample.txt"), [project]);
  observe("frontend-read", markers.slice(0, 3), frontendContext, ["FRONTEND_RULE"]);
  assert.equal(await manager.discoverContext(path.join(project, "frontend/sample.txt"), [project]), "");
  const backendContext = await manager.discoverContext(path.join(project, "backend/sample.txt"), [project]);
  observe("backend-read", markers.slice(0, 3), backendContext, ["BACKEND_RULE"]);
  put(path.join(project, "GEMINI.md"), "PROJECT_RULE: 改為日期待確認，不再匯入。\n");
  await core.refreshMemory(config);
  observe("reload-after-removal", markers.slice(0, 2));
  trusted = false;
  await manager.refresh();
  observe("untrusted", markers.slice(0, 1));
  assert.equal(await manager.discoverContext(path.join(project, "frontend/sample.txt"), [project]), "");

  const team = path.join(temporary, "team-rules");
  copy(path.join(examples, "70/team-rules"), team);
  record(70, { step: "valid-imports", output: run(process.execPath, ["check-rules.mjs"], team) });
  record(70, { step: "documented-tests", output: run(process.execPath, ["--test", "test.mjs"], team) });
  const original = readFileSync(path.join(team, "GEMINI.md"), "utf8");
  put(path.join(team, "GEMINI.md"), original.replace("rules/style.md", "rules/missing.md"));
  record(70, { step: "missing-import", expectedExit: 1, output: run(process.execPath, ["check-rules.mjs"], team, 1) });
  put(path.join(team, "GEMINI.md"), original);
  put(path.join(team, "rules/testing.md"), "TEST_RULE: use npm test");
  record(70, { step: "conflicting-command", expectedExit: 1, output: run(process.execPath, ["check-rules.mjs"], team, 1) });

  for (const name of readdirSync(path.join(examples, "71/settings-cases")).sort()) {
    const source = path.join(examples, "71/settings-cases", name), cwd = path.join(temporary, name);
    const user = JSON.parse(readFileSync(path.join(source, "user.json"), "utf8"));
    user.telemetry = { enabled: false };
    user.security = { folderTrust: { enabled: name === "08-untrusted" } };
    put(settings.USER_SETTINGS_PATH, user);
    put(path.join(cwd, ".gemini/settings.json"), readFileSync(path.join(source, "workspace.json"), "utf8"));
    put(process.env.GEMINI_CLI_SYSTEM_SETTINGS_PATH, readFileSync(path.join(source, "system.json"), "utf8"));
    if (name === "07-invalid-json") {
      assert.throws(() => settings.loadSettings(cwd), /configuration|JSON/i);
      record(71, { case: name, actual: "fatal configuration error" }); continue;
    }
    const loaded = settings.loadSettings(cwd);
    const expectedThemes = { "01-user": "DefaultLight", "02-workspace": "DefaultDark", "03-system": "GitHub", "08-untrusted": "DefaultLight" };
    if (expectedThemes[name]) assert.equal(loaded.merged.ui.theme, expectedThemes[name]);
    if (name === "04-variable") assert.equal(loaded.merged.model.name, process.env.LESSON_MODEL);
    if (name === "06-wrong-type") assert.ok(loaded.errors.length);
    record(71, { case: name, trusted: loaded.isTrusted, theme: loaded.merged.ui.theme,
      model: name === "04-variable" ? loaded.merged.model.name : undefined,
      unknownRetained: Object.hasOwn(loaded.merged, "lessonUnknownField"),
      hideWindowTitle: loaded.merged.ui.hideWindowTitle, diagnostics: loaded.errors.map((e) => ({ severity: e.severity, message: clean(e.message) })) });
  }
  put(settings.USER_SETTINGS_PATH, { telemetry: { enabled: false }, security: { folderTrust: { enabled: false } } });
  put(process.env.GEMINI_CLI_SYSTEM_SETTINGS_PATH, {});

  const commandProject = path.join(temporary, "command-lab");
  copy(path.join(examples, "72/command-lab"), commandProject);
  const loader = new commands.FileCommandLoader({ getFolderTrust: () => true, isTrustedFolder: () => true,
    getProjectRoot: () => commandProject, getExtensions: () => [] });
  const loaded = await loader.loadCommands(new AbortController().signal);
  assert.deepEqual(loaded.map((c) => c.name).sort(), ["lesson:docs-sync", "lesson:review", "lesson:test-plan"]);
  const argumentCases = ["", "src/title.mjs", "文件 範例/brief.md", "It's a test", 'a "quote"', "x; $(echo NEVER_EXECUTE)"];
  for (const command of loaded) {
    for (const args of argumentCases) {
      const output = await command.action({ invocation: { raw: "/" + command.name + " " + args, name: command.name, args } }, args);
      assert.equal(output.type, "submit_prompt");
      const text = output.content.map((p) => p.text).join("");
      assert.ok(text.includes("本次參數：" + args));
      assert.ok(!text.includes("{{args}}"));
      record(72, { command: command.name, args, actual: "submit_prompt", text });
    }
  }
  put(path.join(commandProject, ".gemini/commands/broken.toml"), 'description="missing prompt"');
  assert.equal((await loader.loadCommands(new AbortController().signal)).length, 3);
  const untrustedLoader = new commands.FileCommandLoader({ getFolderTrust: () => true, isTrustedFolder: () => false, getProjectRoot: () => commandProject });
  assert.deepEqual(await untrustedLoader.loadCommands(new AbortController().signal), []);
  record(72, { step: "invalid and untrusted", actual: "invalid file excluded; untrusted workspace returns zero commands", modelResponseTested: false });

  const skill = path.join(examples, "73/doc-check-1.0.0/skills/doc-check");
  assert.equal((await core.loadSkillFromFile(path.join(skill, "SKILL.md"))).name, "doc-check");
  record(73, { step: "script-good", output: run(process.execPath, ["scripts/check-doc.mjs", path.join(examples, "73/samples/good.md")], skill) });
  record(73, { step: "script-bad", expectedExit: 1, output: run(process.execPath, ["scripts/check-doc.mjs", path.join(examples, "73/samples/bad.md")], skill, 1) });
  record(73, { step: "script-missing", expectedExit: 2, output: run(process.execPath, ["scripts/check-doc.mjs", "missing.md"], skill, 2) });
  const extensionWork = path.join(temporary, "extension-work"); mkdirSync(extensionWork);
  const extensionSource = path.join(temporary, "extension-source");
  copy(path.join(examples, "73/doc-check-1.0.0"), extensionSource);
  const extensionManager = new commands.ExtensionManager({
    workspaceDir: extensionWork, settings: settings.loadSettings(extensionWork).merged,
    requestConsent: async () => true, clientVersion: pkg.version,
  });
  await extensionManager.loadExtensions();
  assert.deepEqual(extensionManager.getExtensions(), []);
  const metadata = { source: extensionSource, type: "local" };
  const inspectExtension = (step, version, active) => {
    const ext = extensionManager.getExtensions().find((e) => e.name === "mokaair-doc-check");
    assert.ok(ext);
    assert.equal(ext.version, version);
    assert.equal(ext.isActive, active);
    assert.ok(ext.path.startsWith(isolated + path.sep));
    assert.deepEqual(ext.skills.map((skill) => skill.name), ["doc-check"]);
    record(73, { step, version: ext.version, isActive: ext.isActive, skills: ext.skills.map((skill) => skill.name), method: "real ExtensionManager; no terminal wrapper" });
  };
  await extensionManager.installOrUpdateExtension(metadata);
  inspectExtension("install", "1.0.0", true);
  await extensionManager.disableExtension("mokaair-doc-check", "Workspace");
  inspectExtension("disable", "1.0.0", false);
  await extensionManager.enableExtension("mokaair-doc-check", "Workspace");
  inspectExtension("enable", "1.0.0", true);
  copy(path.join(examples, "73/doc-check-1.1.0"), extensionSource);
  await extensionManager.installOrUpdateExtension(metadata, { name: "mokaair-doc-check", version: "1.0.0" });
  inspectExtension("update", "1.1.0", true);
  await extensionManager.uninstallExtension("mokaair-doc-check");
  assert.deepEqual(extensionManager.getExtensions(), []);
  record(73, { step: "uninstall", installedCount: 0 });
  copy(path.join(examples, "73/doc-check-1.0.0"), extensionSource);
  await extensionManager.installOrUpdateExtension(metadata);
  inspectExtension("rollback-install", "1.0.0", true);
  await extensionManager.uninstallExtension("mokaair-doc-check");

  const repo = path.join(temporary, "sample-repo"); copy(path.join(examples, "74/sample-repo"), repo);
  run("git", ["init", "--quiet"], repo);
  run("git", ["config", "core.autocrlf", "false"], repo);
  run("git", ["add", "."], repo);
  run("git", ["-c", "user.name=Gemini Lesson", "-c", "user.email=lesson@example.invalid", "commit", "--quiet", "-m", "exercise baseline"], repo);
  put(path.join(repo, "docs/editor-note.md"), readFileSync(path.join(repo, "docs/editor-note.md"), "utf8") + "\nUSER_EDIT: 保留此未提交文字。\n");
  const preserved = readFileSync(path.join(repo, "docs/editor-note.md"), "utf8");
  record(74, { step: "baseline-test", expectedExit: 1, output: run(process.execPath, ["--test", "test.mjs"], repo, 1) });
  put(path.join(repo, "apps/web/limit.mjs"), readFileSync(path.join(examples, "74/expected-limit.mjs"), "utf8"));
  record(74, { step: "reference-fix-test", output: run(process.execPath, ["--test", "test.mjs"], repo) });
  assert.equal(readFileSync(path.join(repo, "docs/editor-note.md"), "utf8"), preserved);
  const changed = run("git", ["diff", "--name-only"], repo).trim().split(/\r?\n/).sort();
  assert.deepEqual(changed, ["apps/web/limit.mjs", "docs/editor-note.md"]);
  record(74, { step: "scope", changed, userEditPreserved: true, implementation: "authored reference fix applied locally; not a model-generated change", resumeModelSessionTested: false });

  const summary = { checkedOn: new Date().toISOString(), cli: pkg.version, node: process.version, platform: process.platform,
    method: "installed CLI modules including ExtensionManager; authored Node/Git fixtures", cloudCalls: 0,
    notTested: ["native extension terminal wrapper exits reliably (Windows libuv failure recorded separately)", "model response quality and actual adherence", "authenticated interactive session resume", "macOS/Linux execution", "upgrade to a different Gemini CLI version"], results };
  mkdirSync(path.join(here, "verification"), { recursive: true });
  put(path.join(here, "verification/local-cli.json"), summary);
  for (const [number, checks] of Object.entries(results)) put(path.join(examples, number, "verified-local.json"), { ...summary, results: checks });
  console.log(JSON.stringify({ ...summary, results: Object.fromEntries(Object.entries(results).map(([n, rows]) => [n, rows.length])) }, null, 2));
} finally {
  if (existsSync(temporary)) rmSync(temporary, { recursive: true, force: true });
}
