#!/usr/bin/env node
/**
 * Companion CLI for Mokaair's local Google Flow MCP (`npm run flow -- <cmd>`).
 *
 * Commands:
 *   npm run flow -- doctor
 *   npm run flow -- login [--profile <name>]
 *   npm run flow -- status [--profile <name>]
 *   npm run flow -- setup [--client all|claude-code|claude-desktop|codex|antigravity] [--platform win32|darwin|linux] [--write]
 *   npm run flow -- preflight --slug <slug> [--series curio|sothatswhy|shorts]
 *   npm run flow -- ledger --slug <slug> [--series curio|sothatswhy|shorts]
 *   npm run flow -- mcp
 */

import { spawnSync } from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";
import {
  MCP_SERVER_NAME,
  REPO_ROOT,
  detectSyncFolderHazard,
  resolveRulesCacheRoot,
  resolveRuntimeHome,
} from "./config.mjs";
import { GflowCliDriver, resolveGflowBinary } from "./drivers/gflow-cli-driver.mjs";
import { resolveEpisodePaths } from "./guards/path-boundary.mjs";
import { FlowOrchestrator } from "./orchestrator.mjs";
import { startStdioServer } from "./server.mjs";

function parseArgs(argv) {
  const positionals = [];
  const flags = {};
  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg.startsWith("--")) {
      const key = arg.slice(2);
      const next = argv[i + 1];
      if (!next || next.startsWith("--")) {
        flags[key] = true;
      } else {
        flags[key] = next;
        i += 1;
      }
    } else {
      positionals.push(arg);
    }
  }
  return { command: positionals[0] || "help", positionals: positionals.slice(1), flags };
}

function probeCommand(cmd, args = ["--version"]) {
  const res = spawnSync(cmd, args, { encoding: "utf8", windowsHide: true });
  if (res.error) {
    return { ok: false, command: cmd, error: res.error.code || res.error.message };
  }
  const firstLine = `${res.stdout || ""}${res.stderr || ""}`.trim().split(/\r?\n/)[0] || "";
  return { ok: res.status === 0, command: cmd, version: firstLine };
}

function probeChrome(platform = process.platform, env = process.env) {
  if (platform === "win32") {
    const candidates = [
      path.win32.join(env.PROGRAMFILES || "C:\\Program Files", "Google", "Chrome", "Application", "chrome.exe"),
      path.win32.join(env["PROGRAMFILES(X86)"] || "C:\\Program Files (x86)", "Google", "Chrome", "Application", "chrome.exe"),
      path.win32.join(env.LOCALAPPDATA || "", "Google", "Chrome", "Application", "chrome.exe"),
    ];
    for (const c of candidates) {
      if (c && fs.existsSync(c)) return { ok: true, path: c };
    }
    return { ok: false, hint: "Install Google Chrome (https://www.google.com/chrome/)." };
  }
  if (platform === "darwin") {
    const macPath = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
    if (fs.existsSync(macPath)) return { ok: true, path: macPath };
    return { ok: false, hint: "Install Google Chrome in /Applications." };
  }
  for (const bin of ["google-chrome", "google-chrome-stable", "chromium", "chromium-browser"]) {
    const p = probeCommand(bin);
    if (p.ok) return { ok: true, path: bin, version: p.version };
  }
  return { ok: false, hint: "Install Google Chrome on the desktop machine that drives Flow." };
}

/**
 * Generates exact MCP client config snippets and file destinations for Windows,
 * macOS, and Linux. Handles Windows backslash escaping cleanly.
 */
export function buildClientSetupPlan({
  repoRoot = REPO_ROOT,
  platform = process.platform,
  env = process.env,
  homedir = os.homedir(),
  serverName = MCP_SERVER_NAME,
} = {}) {
  const pathMod = platform === "win32" ? path.win32 : path.posix;
  const serverScript = pathMod.join(repoRoot, "tools", "video", "flow-mcp", "server.mjs");
  const runtimeHome = resolveRuntimeHome({ env, platform, homedir });

  const jsonServerEntry = {
    command: "node",
    args: [serverScript],
    env: {
      MOKAAIR_FLOW_HOME: runtimeHome,
    },
  };

  const userProfile = platform === "win32" ? env.USERPROFILE || homedir : homedir;
  const appData =
    platform === "win32"
      ? env.APPDATA || path.win32.join(userProfile, "AppData", "Roaming")
      : path.posix.join(homedir, "Library", "Application Support");

  const claudeDesktopConfigPath =
    platform === "win32"
      ? path.win32.join(appData, "Claude", "claude_desktop_config.json")
      : platform === "darwin"
        ? path.posix.join(appData, "Claude", "claude_desktop_config.json")
        : path.posix.join(homedir, ".config", "Claude", "claude_desktop_config.json");

  const antigravityConfigPath = pathMod.join(userProfile, ".gemini", "config", "mcp_config.json");
  const codexConfigPath = pathMod.join(userProfile, ".codex", "config.toml");

  const tomlEscape = (value) => String(value).replace(/\\/g, "\\\\").replace(/"/g, '\\"');
  const codexTomlSnippet = [
    `[mcp_servers.${serverName}]`,
    `command = "node"`,
    `args = ["${tomlEscape(serverScript)}"]`,
    ``,
    `[mcp_servers.${serverName}.env]`,
    `MOKAAIR_FLOW_HOME = "${tomlEscape(runtimeHome)}"`,
  ].join("\n");

  const claudeCodeCommand =
    platform === "win32"
      ? `claude mcp add --scope user ${serverName} -e "MOKAAIR_FLOW_HOME=${runtimeHome}" -- node "${serverScript}"`
      : `claude mcp add --scope user ${serverName} -e MOKAAIR_FLOW_HOME="${runtimeHome}" -- node "${serverScript}"`;

  return {
    platform,
    serverName,
    serverScript,
    runtimeHome,
    hazards: [
      detectSyncFolderHazard(repoRoot, platform),
      detectSyncFolderHazard(runtimeHome, platform),
    ].filter(Boolean),
    clients: {
      "claude-code": {
        kind: "cli",
        command: claudeCodeCommand,
      },
      "claude-desktop": {
        kind: "json",
        configPath: claudeDesktopConfigPath,
        snippet: { mcpServers: { [serverName]: jsonServerEntry } },
      },
      antigravity: {
        kind: "json",
        configPath: antigravityConfigPath,
        snippet: { mcpServers: { [serverName]: jsonServerEntry } },
      },
      codex: {
        kind: "toml",
        configPath: codexConfigPath,
        snippet: codexTomlSnippet,
      },
    },
  };
}

/**
 * Safely merges the `mokaair-flow` entry into an existing JSON or TOML MCP
 * config file, writing a timestamped `.bak` copy first when overwriting.
 */
export function applyClientConfigWrite(clientSpec, serverName = MCP_SERVER_NAME) {
  if (clientSpec.kind === "cli") {
    return {
      written: false,
      skipped: true,
      reason: "Run the printed `claude mcp add` command in your terminal.",
      command: clientSpec.command,
    };
  }

  const target = clientSpec.configPath;
  fs.mkdirSync(path.dirname(target), { recursive: true });

  let backupPath = null;
  if (fs.existsSync(target)) {
    backupPath = `${target}.bak`;
    fs.copyFileSync(target, backupPath);
  }

  if (clientSpec.kind === "json") {
    const raw = fs.existsSync(target) ? fs.readFileSync(target, "utf8").trim() : "";
    const existing = raw ? JSON.parse(raw) : {};
    existing.mcpServers = existing.mcpServers && typeof existing.mcpServers === "object" ? existing.mcpServers : {};
    existing.mcpServers[serverName] = clientSpec.snippet.mcpServers[serverName];
    fs.writeFileSync(target, `${JSON.stringify(existing, null, 2)}\n`, "utf8");
    return { written: true, configPath: target, backupPath };
  }

  if (clientSpec.kind === "toml") {
    const existing = fs.existsSync(target) ? fs.readFileSync(target, "utf8") : "";
    const sectionHeader = `[mcp_servers.${serverName}]`;
    const envHeader = `[mcp_servers.${serverName}.env]`;

    // Strip any previous block for this server cleanly before appending
    const lines = existing.split(/\r?\n/);
    const kept = [];
    let skipping = false;
    for (const line of lines) {
      const trimmed = line.trim();
      if (trimmed === sectionHeader || trimmed === envHeader) {
        skipping = true;
        continue;
      }
      if (skipping && trimmed.startsWith("[")) {
        skipping = false;
      }
      if (!skipping) kept.push(line);
    }

    const base = kept.join("\n").trimEnd();
    const updated = base ? `${base}\n\n${clientSpec.snippet}\n` : `${clientSpec.snippet}\n`;
    fs.writeFileSync(target, updated, "utf8");
    return { written: true, configPath: target, backupPath };
  }

  return { written: false, reason: `Unsupported client config kind "${clientSpec.kind}".` };
}

function runDoctor() {
  const nodeMajor = Number(process.versions.node.split(".")[0]);
  const gflowBin = resolveGflowBinary();
  const runtimeHome = resolveRuntimeHome();
  const rulesRoot = resolveRulesCacheRoot(REPO_ROOT);

  const checks = {
    node: { ok: nodeMajor >= 22, version: process.versions.node, required: ">=22" },
    uv: probeCommand("uv"),
    gflow: probeCommand(gflowBin),
    ffmpeg: probeCommand(process.env.FFMPEG_BIN || "ffmpeg", ["-version"]),
    chrome: probeChrome(),
    rulesCache: {
      ok: fs.existsSync(rulesRoot),
      path: rulesRoot,
      hint: fs.existsSync(rulesRoot) ? null : "Run `npm run vdrive -- pull-rules explainer` to pull canon sheets & rules.",
    },
    runtimeHome: {
      ok: !detectSyncFolderHazard(runtimeHome),
      path: runtimeHome,
      hazard: detectSyncFolderHazard(runtimeHome),
    },
    repoHazard: {
      ok: !detectSyncFolderHazard(REPO_ROOT),
      path: REPO_ROOT,
      hazard: detectSyncFolderHazard(REPO_ROOT),
    },
  };

  const missingSteps = [];
  if (!checks.uv.ok) {
    missingSteps.push(
      process.platform === "win32"
        ? 'Install uv (PowerShell): powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"'
        : "Install uv: curl -LsSf https://astral.sh/uv/install.sh | sh",
    );
  }
  if (!checks.gflow.ok) {
    missingSteps.push("Install gflow-cli: uv tool install gflow-cli");
  }
  if (!checks.ffmpeg.ok) {
    missingSteps.push(
      process.platform === "win32"
        ? "Install FFmpeg: winget install Gyan.FFmpeg"
        : "Install FFmpeg: brew install ffmpeg (macOS) or sudo apt-get install ffmpeg (Linux)",
    );
  }
  if (!checks.rulesCache.ok) {
    missingSteps.push("Pull Drive rules & canon sheets: npm run vdrive -- pull-rules explainer");
  }

  const allReady = checks.node.ok && checks.gflow.ok && checks.ffmpeg.ok && checks.chrome.ok;
  console.log(
    JSON.stringify(
      {
        ok: allReady,
        platform: process.platform,
        checks,
        nextSteps: missingSteps.length > 0 ? missingSteps : ["Run `npm run flow -- login` then `npm run flow -- setup --write`."],
      },
      null,
      2,
    ),
  );
}

/**
 * Batch-executes `tools/video/cli.mjs clips import` for every ready clip listed
 * in `work/video-episodes/<slug>/flow-clips/import-bridge.json`.
 */
export function runImportBridgeBatch({
  slug,
  repoRoot = REPO_ROOT,
  dryRun = false,
  spawnFn = spawnSync,
} = {}) {
  const paths = resolveEpisodePaths(slug, { repoRoot });
  if (!fs.existsSync(paths.clipsImportBridgeFile)) {
    return {
      ok: false,
      reason: "missing_import_bridge",
      message: `import-bridge.json not found at "${paths.clipsImportBridgeFile}". Run flow_generate_clips or flow_select_take first.`,
    };
  }

  const bridge = JSON.parse(fs.readFileSync(paths.clipsImportBridgeFile, "utf8"));
  const clipEntries = (bridge.entries || []).filter((e) => e.mode === "clip" && e.ready && e.filePath);
  const videoCliPath = path.join(repoRoot, "tools", "video", "cli.mjs");

  const imported = [];
  const failed = [];

  for (const entry of clipEntries) {
    const args = [
      videoCliPath,
      "clips",
      "import",
      "--slug",
      paths.slug,
      "--shot",
      entry.shotId,
      "--file",
      entry.filePath,
      "--provider",
      "external",
      "--note",
      `route=google-flow-mcp model=${entry.model || "omni-1.2-flash"} credits=${entry.credits ?? 12} dur=${entry.durationSec ?? 4}s take=${entry.selectedTake ?? 1}`,
    ];

    if (dryRun) {
      imported.push({ shotId: entry.shotId, dryRun: true, command: `node ${args.join(" ")}` });
      continue;
    }

    const res = spawnFn(process.execPath, args, {
      cwd: repoRoot,
      encoding: "utf8",
      windowsHide: true,
    });
    if (res.status === 0) {
      imported.push({ shotId: entry.shotId, filePath: entry.filePath, take: entry.selectedTake ?? 1 });
    } else {
      failed.push({
        shotId: entry.shotId,
        exitCode: res.status ?? 1,
        stderr: (res.stderr || res.error?.message || "").trim().slice(0, 400),
      });
    }
  }

  return {
    ok: failed.length === 0,
    slug: paths.slug,
    dryRun,
    totalClips: clipEntries.length,
    importedCount: imported.length,
    failedCount: failed.length,
    imported,
    failed,
  };
}

/**
 * Validates episode ledger readiness (0 missing clips, 0 rejected stills,
 * 0 unresolved `maybe` credits) before delegating to `vdrive.mjs push-episode`.
 */
export async function runValidatedDrivePush({
  slug,
  driveSeries,
  drivePath,
  series = null,
  repoRoot = REPO_ROOT,
  dryRun = false,
  force = false,
  orchestrator = null,
  spawnFn = spawnSync,
} = {}) {
  const orch = orchestrator || new FlowOrchestrator({ repoRoot });
  const ledger = await orch.flowEpisodeLedger({ slug, series });

  if (!force && !ledger.readyForDrivePush) {
    return {
      ok: false,
      reason: "episode_not_ready_for_push",
      message:
        "Refused Drive push: episode has missing clips, rejected stills, or unresolved `maybe` credits. Run flow_reconcile / finish missing shots, or pass --force.",
      ledger,
    };
  }

  const targetSeries = driveSeries || ledger.series;
  if (!drivePath) {
    return {
      ok: false,
      reason: "missing_drive_path",
      message: "Missing required --path \"<Drive relative path>\" (e.g. \"第033集/製作檔/<slug>\" or \"H-歷史懸案/H01/製作檔/<slug>\").",
      suggestedCommand: ledger.drivePushCommand,
    };
  }

  const vdriveScript = path.join(repoRoot, "tools", "video", "vdrive.mjs");
  const args = [
    vdriveScript,
    "push-episode",
    "--series",
    String(targetSeries),
    "--path",
    String(drivePath),
    "--from",
    ledger.workdir,
  ];
  if (dryRun) args.push("--dry-run");

  const res = spawnFn(process.execPath, args, {
    cwd: repoRoot,
    encoding: "utf8",
    windowsHide: true,
  });

  return {
    ok: res.status === 0,
    slug: ledger.slug,
    series: targetSeries,
    drivePath,
    dryRun,
    exitCode: res.status ?? 1,
    stdout: (res.stdout || "").trim(),
    stderr: (res.stderr || res.error?.message || "").trim(),
  };
}

function printHelp() {
  console.log(`Mokaair Google Flow MCP & CLI v2 (Route A — Explainers + AI Dramas + Vertical Shorts)

Usage:
  npm run flow -- doctor                                  Check Node 22+, uv, gflow-cli, Chrome, FFmpeg & hazards
  npm run flow -- login [--profile NAME]                  Open visible Chrome to sign into Google Flow manually
  npm run flow -- status [--profile NAME]                 Check Flow session, gflow version, credits & lock
  npm run flow -- profiles [--refresh]                    List all signed-in Google AI subscription profiles & credits
  npm run flow -- setup [--client all|claude-code|claude-desktop|codex|antigravity] [--platform win32|darwin|linux] [--repo-root PATH] [--write]
  npm run flow -- import-video-json --slug <slug> [--file <video.json>] [--series drama-16x9|drama-9x16|shorts|curio|sothatswhy]
  npm run flow -- preflight --slug <slug> [--series curio|sothatswhy|drama-16x9|drama-9x16|shorts] [--pilot]
  npm run flow -- reconcile --slug <slug> [--profile NAME]
  npm run flow -- import-all --slug <slug> [--dry-run]    Batch-import ready clips from import-bridge.json into tools/video
  npm run flow -- push --slug <slug> --path "<relDest>" [--drive-series <name>] [--dry-run] [--force]
  npm run flow -- ledger --slug <slug> [--series curio|sothatswhy|drama-16x9|drama-9x16|shorts]
  npm run flow -- mcp                                     Start JSON-RPC 2.0 stdio MCP server`);
}

async function main() {
  const { command, flags } = parseArgs(process.argv.slice(2));

  if (command === "help" || flags.help) {
    printHelp();
    return;
  }

  if (command === "mcp") {
    startStdioServer();
    return;
  }

  if (command === "doctor") {
    runDoctor();
    return;
  }

  if (command === "login") {
    const driver = new GflowCliDriver({ profile: flags.profile || null });
    const cmd = driver.getLoginCommand({ profile: flags.profile || null });
    console.error(`[mokaair-flow] Launching visible Chrome sign-in via: ${cmd.binary} ${cmd.args.join(" ")}`);
    console.error("[mokaair-flow] Sign into Google manually and open flow.google.com; passwords are never handled by MCP.");
    const res = spawnSync(cmd.binary, cmd.args, { env: cmd.env, stdio: "inherit" });
    if (res.error) {
      console.error(`[mokaair-flow] Failed to run ${cmd.binary}: ${res.error.message}`);
      console.error("Install gflow-cli first with: uv tool install gflow-cli");
      process.exit(1);
    }
    process.exit(res.status ?? 0);
  }

  if (command === "setup") {
    const platform = flags.platform || process.platform;
    const plan = buildClientSetupPlan({
      platform,
      repoRoot: flags["repo-root"] || REPO_ROOT,
    });
    const targetClient = flags.client || "all";
    const selectedNames =
      targetClient === "all" ? Object.keys(plan.clients) : [String(targetClient)];

    const output = {
      platform: plan.platform,
      serverName: plan.serverName,
      serverScript: plan.serverScript,
      runtimeHome: plan.runtimeHome,
      hazards: plan.hazards,
      clients: {},
      writes: {},
    };

    for (const name of selectedNames) {
      const spec = plan.clients[name];
      if (!spec) {
        console.error(`Unknown client "${name}". Choose from: all, ${Object.keys(plan.clients).join(", ")}`);
        process.exit(2);
      }
      output.clients[name] = spec;
      if (flags.write) {
        output.writes[name] = applyClientConfigWrite(spec, plan.serverName);
      }
    }

    console.log(JSON.stringify(output, null, 2));
    return;
  }

  if (command === "import-all") {
    if (!flags.slug) {
      console.error("Missing required flag: --slug <episode-slug>");
      process.exit(2);
    }
    const result = runImportBridgeBatch({
      slug: flags.slug,
      dryRun: Boolean(flags["dry-run"]),
    });
    console.log(JSON.stringify(result, null, 2));
    if (!result.ok) process.exit(1);
    return;
  }

  if (command === "push") {
    if (!flags.slug) {
      console.error("Missing required flag: --slug <episode-slug>");
      process.exit(2);
    }
    const result = await runValidatedDrivePush({
      slug: flags.slug,
      driveSeries: flags["drive-series"] || flags.series || null,
      drivePath: flags.path || null,
      series: flags.series || null,
      dryRun: Boolean(flags["dry-run"]),
      force: Boolean(flags.force),
    });
    console.log(JSON.stringify(result, null, 2));
    if (!result.ok) process.exit(1);
    return;
  }

  const orchestrator = new FlowOrchestrator();

  if (command === "status") {
    const result = await orchestrator.flowStatus({
      profile: flags.profile || null,
      refreshCredits: Boolean(flags.refresh),
    });
    console.log(JSON.stringify(result, null, 2));
    if (!result.ok) process.exit(1);
    return;
  }

  if (command === "profiles") {
    const result = await orchestrator.flowProfiles({
      refreshCredits: Boolean(flags.refresh),
    });
    console.log(JSON.stringify(result, null, 2));
    return;
  }

  if (command === "import-video-json") {
    if (!flags.slug) {
      console.error("Missing required flag: --slug <episode-slug>");
      process.exit(2);
    }
    const result = await orchestrator.flowImportVideoJson({
      slug: flags.slug,
      series: flags.series || null,
      videoJsonPath: flags.file || null,
    });
    console.log(JSON.stringify(result, null, 2));
    return;
  }

  if (command === "preflight") {
    if (!flags.slug) {
      console.error("Missing required flag: --slug <episode-slug>");
      process.exit(2);
    }
    const result = await orchestrator.flowPreflightShotlist({
      slug: flags.slug,
      series: flags.series || null,
      pilot: Boolean(flags.pilot),
    });
    console.log(JSON.stringify(result, null, 2));
    if (!result.ok) process.exit(1);
    return;
  }

  if (command === "reconcile") {
    if (!flags.slug) {
      console.error("Missing required flag: --slug <episode-slug>");
      process.exit(2);
    }
    const result = await orchestrator.flowReconcile({
      slug: flags.slug,
      series: flags.series || null,
      profile: flags.profile || null,
    });
    console.log(JSON.stringify(result, null, 2));
    if (!result.ok) process.exit(1);
    return;
  }

  if (command === "ledger") {
    if (!flags.slug) {
      console.error("Missing required flag: --slug <episode-slug>");
      process.exit(2);
    }
    const result = await orchestrator.flowEpisodeLedger({
      slug: flags.slug,
      series: flags.series || null,
    });
    console.log(JSON.stringify(result, null, 2));
    return;
  }

  console.error(`Unknown command "${command}".`);
  printHelp();
  process.exit(2);
}

const isMain = process.argv[1] && fileURLToPath(import.meta.url) === process.argv[1];
if (isMain) {
  main().catch((err) => {
    console.error(`[mokaair-flow] ${err.message}`);
    process.exit(1);
  });
}
