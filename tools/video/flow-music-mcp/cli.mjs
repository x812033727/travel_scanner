#!/usr/bin/env node
/**
 * Companion CLI for Mokaair's local Google Flow Music MCP (`npm run flow-music -- <cmd>`).
 *
 * Commands:
 *   npm run flow-music -- doctor
 *   npm run flow-music -- login [--profile <name>]
 *   npm run flow-music -- status [--profile <name>]
 *   npm run flow-music -- profiles
 *   npm run flow-music -- setup [--client all|claude-code|claude-desktop|codex|antigravity] [--platform win32|darwin|linux] [--write]
 *   npm run flow-music -- measure --collection <slug> [--series curio|sothatswhy|...]
 *   npm run flow-music -- gallery --collection <slug> [--series curio|sothatswhy|...]
 *   npm run flow-music -- mcp
 */

import { spawn, spawnSync } from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";
import {
  FLOW_MUSIC_ORIGIN,
  MCP_SERVER_NAME,
  REPO_ROOT,
  detectSyncFolderHazard,
  resolveChromeBinary,
  resolveLocalDriveAiDramaRoot,
  resolveRuntimeHome,
} from "./config.mjs";
import { ChromeCdpMusicDriver } from "./drivers/chrome-cdp-driver.mjs";
import { FlowMusicOrchestrator } from "./orchestrator.mjs";
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

/**
 * Generates exact MCP client config snippets and file destinations for Windows,
 * macOS, and Linux, using Antigravity's `~/.gemini/config/mcp_config.json`.
 */
export function buildClientSetupPlan({
  repoRoot = REPO_ROOT,
  platform = process.platform,
  env = process.env,
  homedir = os.homedir(),
  serverName = MCP_SERVER_NAME,
} = {}) {
  const pathMod = platform === "win32" ? path.win32 : path.posix;
  const serverScript = pathMod.join(repoRoot, "tools", "video", "flow-music-mcp", "server.mjs");
  const runtimeHome = resolveRuntimeHome({ env, platform, homedir });

  const jsonServerEntry = {
    command: "node",
    args: [serverScript],
    env: {
      MOKAAIR_FLOW_MUSIC_HOME: runtimeHome,
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
    `MOKAAIR_FLOW_MUSIC_HOME = "${tomlEscape(runtimeHome)}"`,
  ].join("\n");

  const claudeCodeCommand =
    platform === "win32"
      ? `claude mcp add --scope user ${serverName} -e "MOKAAIR_FLOW_MUSIC_HOME=${runtimeHome}" -- node "${serverScript}"`
      : `claude mcp add --scope user ${serverName} -e MOKAAIR_FLOW_MUSIC_HOME="${runtimeHome}" -- node "${serverScript}"`;

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
      "claude-code": { kind: "cli", command: claudeCodeCommand },
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
 * Safely merges the `mokaair-flow-music` entry into an existing JSON or TOML
 * MCP config file (including 0-byte empty JSON files), backing up to `.bak`.
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
  const chromeBin = resolveChromeBinary();
  const runtimeHome = resolveRuntimeHome();
  const driveRoot = resolveLocalDriveAiDramaRoot();

  const checks = {
    node: { ok: nodeMajor >= 22, version: process.versions.node, required: ">=22" },
    websocket: { ok: typeof WebSocket === "function", note: "Node.js 22 native WebSocket for Chrome CDP" },
    chrome: chromeBin
      ? { ok: true, path: chromeBin }
      : { ok: false, hint: "Install Google Chrome (https://www.google.com/chrome/) or set MOKAAIR_CHROME_BIN." },
    ffmpeg: probeCommand(process.env.FFMPEG_BIN || "ffmpeg", ["-version"]),
    driveMount: {
      ok: Boolean(driveRoot),
      path: driveRoot,
      hint: driveRoot ? null : "Optional: mount Google Drive (G:\\我的雲端硬碟\\AI\\備份\\AI劇) or set VDRIVE_ROOT.",
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

  const allReady = checks.node.ok && checks.websocket.ok && checks.chrome.ok && checks.ffmpeg.ok;
  console.log(
    JSON.stringify(
      {
        ok: allReady,
        platform: process.platform,
        origin: FLOW_MUSIC_ORIGIN,
        checks,
        nextSteps: allReady
          ? ["Run `npm run flow-music -- login` to sign into www.flowmusic.app, then `npm run flow-music -- setup --write`."]
          : ["Fix the failed checks above and re-run `npm run flow-music -- doctor`."],
      },
      null,
      2,
    ),
  );
}

async function runLogin(flags) {
  const driver = new ChromeCdpMusicDriver({ profile: flags.profile || null });
  const cmd = driver.getLoginCommand({ profile: flags.profile || null });
  console.log(`[${MCP_SERVER_NAME}] Opening isolated Chrome profile "${cmd.profile}" -> ${FLOW_MUSIC_ORIGIN}`);
  console.log(`[${MCP_SERVER_NAME}] Profile directory: ${cmd.userDataDir}`);
  console.log(`[${MCP_SERVER_NAME}] Sign into your Google / Flow Music account, then CLOSE that Chrome window.`);

  await new Promise((resolve, reject) => {
    const child = spawn(cmd.binary, cmd.args, { stdio: "inherit" });
    child.on("error", reject);
    child.on("close", () => resolve());
  });

  console.log(`[${MCP_SERVER_NAME}] Verifying saved session...`);
  const status = await new FlowMusicOrchestrator({ driver }).musicStatus({ profile: cmd.profile });
  console.log(JSON.stringify(status, null, 2));
}

async function main() {
  const { command, flags } = parseArgs(process.argv.slice(2));

  switch (command) {
    case "doctor":
      runDoctor();
      return;

    case "login":
      await runLogin(flags);
      return;

    case "status": {
      const orchestrator = new FlowMusicOrchestrator();
      const res = await orchestrator.musicStatus({
        profile: flags.profile || null,
        probeRemote: flags["no-probe"] ? false : true,
      });
      console.log(JSON.stringify(res, null, 2));
      return;
    }

    case "profiles": {
      const orchestrator = new FlowMusicOrchestrator();
      console.log(JSON.stringify(await orchestrator.musicProfiles(), null, 2));
      return;
    }

    case "setup": {
      const plan = buildClientSetupPlan({
        repoRoot: flags["repo-root"] || REPO_ROOT,
        platform: flags.platform || process.platform,
      });
      const targetClient = flags.client || "all";
      const selectedKeys = targetClient === "all" ? Object.keys(plan.clients) : [targetClient];
      const results = {};
      if (flags.write) {
        for (const key of selectedKeys) {
          if (!plan.clients[key]) throw new Error(`Unknown client "${key}".`);
          results[key] = applyClientConfigWrite(plan.clients[key], plan.serverName);
        }
      }
      console.log(JSON.stringify({ plan, ...(flags.write ? { written: results } : {}) }, null, 2));
      return;
    }

    case "measure": {
      if (!flags.collection) throw new Error("Pass --collection <slug>");
      const orchestrator = new FlowMusicOrchestrator();
      const res = await orchestrator.musicMeasure({
        collection: flags.collection,
        series: flags.series || "curio",
      });
      console.log(JSON.stringify(res, null, 2));
      return;
    }

    case "gallery": {
      if (!flags.collection) throw new Error("Pass --collection <slug>");
      const orchestrator = new FlowMusicOrchestrator();
      const res = await orchestrator.musicQaGallery({
        collection: flags.collection,
        series: flags.series || "curio",
      });
      console.log(JSON.stringify(res, null, 2));
      return;
    }

    case "mcp":
      startStdioServer();
      return;

    default:
      console.log(`Mokaair Google Flow Music MCP CLI (npm run flow-music -- <command>)

Commands:
  doctor                                Check Node >= 22, Chrome, FFmpeg, Drive mount, and path hazards
  login [--profile <name>]              Open isolated Chrome window to sign into www.flowmusic.app
  status [--profile <name>]             Verify saved Flow Music session via Chrome CDP
  profiles                              List all isolated Flow Music Chrome profiles & lock status
  setup [--client all|antigravity|claude-desktop|claude-code|codex] [--write]
                                        Print or write MCP client configs (with .bak backup)
  measure --collection <slug>           Measure duration, LUFS, peak, silences, and SHA-256
  gallery --collection <slug>           Generate interactive HTML audition & sign-off gallery
  mcp                                   Start JSON-RPC 2.0 MCP server on stdio
`);
  }
}

if (process.argv[1] && fileURLToPath(import.meta.url) === path.resolve(process.argv[1])) {
  main().catch((err) => {
    console.error(`[${MCP_SERVER_NAME}] ${err?.message || err}`);
    process.exit(1);
  });
}
