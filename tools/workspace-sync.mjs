#!/usr/bin/env node
/**
 * Multi-agent Google Drive workspace capsule (`npm run ws`).
 *
 * Keeps live `.git`, `node_modules` and `.venv` on fast local/VPS disk while packing a
 * lightweight, hash-verified workspace capsule (`meta.json`, `wip.patch`, `untracked/`,
 * `HANDOFF.md`) into Google Drive (`AI/工作區/<id>/` via a local Drive mount or `rclone`
 * remote `videobackup:工作區`). This lets Claude Code, Codex and Gemini (`agy` / Antigravity)
 * hand off uncommitted work in seconds and delegate cross-model reviews through the host's
 * shared subscription accounts (`/var/lib/mokaair-ai-accounts`).
 */

import { createHash } from "node:crypto";
import { execFileSync } from "node:child_process";
import {
  cpSync,
  existsSync,
  mkdirSync,
  mkdtempSync,
  readdirSync,
  readFileSync,
  rmSync,
  statSync,
  writeFileSync,
} from "node:fs";
import { tmpdir } from "node:os";
import { dirname, isAbsolute, join, posix, relative, resolve, sep } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = fileURLToPath(new URL("../", import.meta.url));
const VALID_AGENTS = new Set(["claude", "codex", "gemini"]);
const VALID_SLOTS = new Set(["a", "b", "c", "d", "e", "default"]);

const SECRET_PATTERNS = [
  /(?:^|\/)\.env(?:\.|$)/i,
  /(?:^|\/)rclone\.conf$/i,
  /(?:^|\/)[^/]*(?:secret|token|credential|password|passwd)[^/]*\.(?:json|txt|env|ya?ml|toml|conf|ini)$/i,
  /\.(?:pem|key|p12|pfx|agekey)$/i,
  /(?:^|\/)id_(?:rsa|ed25519|ecdsa)$/i,
];

const REBUILDABLE_PREFIXES = [
  ".git/",
  "node_modules/",
  ".venv/",
  "venv/",
  ".next/",
  "apps/web/.next/",
  "apps/api/.venv/",
  "__pycache__/",
  ".pytest_cache/",
  ".mypy_cache/",
  ".ruff_cache/",
];

export function toPosixPath(p) {
  return p.split(sep).join("/");
}

export function sha256Buffer(buf) {
  return createHash("sha256").update(buf).digest("hex");
}

export function sha256File(filePath) {
  return sha256Buffer(readFileSync(filePath));
}

export function detectAgent(env = process.env) {
  if (env.WORKSPACE_AGENT && VALID_AGENTS.has(env.WORKSPACE_AGENT.toLowerCase())) {
    return env.WORKSPACE_AGENT.toLowerCase();
  }
  if (env.CLAUDE_CODE || env.CLAUDE_CONFIG_DIR || env.ANTHROPIC_MODEL) return "claude";
  if (env.CODEX_HOME || env.CODEX_SANDBOX_TYPE || env.CODEX_CI) return "codex";
  if (
    env.ANTIGRAVITY_AGENT ||
    env.GEMINI_API_KEY ||
    env.USER === "antigravity" ||
    (env.HOME && env.HOME.includes("antigravity"))
  ) {
    return "gemini";
  }
  return "unknown";
}

export function isRcloneRemote(target) {
  if (!target || typeof target !== "string") return false;
  // Windows drive letter like C:/ or G:\ is a local path, not an rclone remote.
  if (/^[A-Za-z]:[\\/]/.test(target)) return false;
  return /^[A-Za-z0-9_.-]+:/.test(target);
}

export function resolveDriveTarget(explicitDest, env = process.env) {
  if (explicitDest) return explicitDest;
  if (env.WORKSPACE_DRIVE_TARGET) return env.WORKSPACE_DRIVE_TARGET;
  const localCandidates = [
    "G:/我的雲端硬碟/AI/工作區",
    "G:/My Drive/AI/工作區",
    "/content/drive/MyDrive/AI/工作區",
  ];
  for (const candidate of localCandidates) {
    const parent = dirname(candidate);
    if (existsSync(candidate) || existsSync(parent)) return candidate;
  }
  if (env.RCLONE_CONFIG_VIDEOBACKUP_TYPE || existsSync("/etc/travel-scanner/rclone-videos/rclone.conf")) {
    return "videobackup:工作區";
  }
  return "videobackup:工作區";
}

export function classifyPath(relPath) {
  const normalized = toPosixPath(relPath).replace(/^\/+/, "");
  if (!normalized || normalized.includes("..")) {
    return { excluded: true, reason: "invalid-path" };
  }
  for (const prefix of REBUILDABLE_PREFIXES) {
    if (normalized.startsWith(prefix) || normalized.includes(`/${prefix}`)) {
      return { excluded: true, reason: "rebuildable-dependency" };
    }
  }
  for (const pattern of SECRET_PATTERNS) {
    if (pattern.test(normalized)) {
      return { excluded: true, reason: "credential-or-secret" };
    }
  }
  return { excluded: false, reason: null };
}

export function sanitizeWorkspaceId(raw) {
  const cleaned = String(raw ?? "")
    .trim()
    .replace(/[^A-Za-z0-9._-]+/g, "-")
    .replace(/^-+|-+$/g, "");
  if (!cleaned) {
    throw new Error("Workspace ID cannot be empty.");
  }
  return cleaned;
}

function runGit(cwd, args, options = {}) {
  return execFileSync("git", args, {
    cwd,
    encoding: options.encoding ?? "utf8",
    maxBuffer: 64 * 1024 * 1024,
    stdio: ["ignore", "pipe", "pipe"],
  });
}

export function findClaimedTaskForBranch(repoRoot, branch) {
  const openDir = join(repoRoot, "tasks", "open");
  if (!existsSync(openDir) || !branch) return null;
  for (const name of readdirSync(openDir).filter((f) => f.endsWith(".md")).sort()) {
    const text = readFileSync(join(openDir, name), "utf8");
    const branchMatch = /^branch:\s*(\S+)\s*$/m.exec(text);
    const idMatch = /^id:\s*(\S+)\s*$/m.exec(text);
    if (branchMatch?.[1] === branch && idMatch?.[1]) {
      return idMatch[1];
    }
  }
  return null;
}

export function inspectWorktree(repoRoot = ROOT, options = {}) {
  const branch = runGit(repoRoot, ["rev-parse", "--abbrev-ref", "HEAD"]).trim();
  const baseSha = runGit(repoRoot, ["rev-parse", "HEAD"]).trim();
  const taskId = findClaimedTaskForBranch(repoRoot, branch);
  const defaultId = sanitizeWorkspaceId(
    options.id || taskId || (branch !== "HEAD" ? branch.replace(/\//g, "-") : baseSha.slice(0, 12)),
  );

  const trackedRaw = runGit(repoRoot, ["diff", "--name-status", "HEAD"]).trim();
  const trackedChanges = trackedRaw
    ? trackedRaw.split(/\r?\n/).map((line) => {
        const [status, ...rest] = line.trim().split(/\t+/);
        return { status, path: rest.join("\t") };
      })
    : [];

  const untrackedRaw = runGit(repoRoot, ["ls-files", "-z", "--others", "--exclude-standard"]);
  const untrackedCandidates = untrackedRaw.split("\0").filter(Boolean).map(toPosixPath);
  for (const extra of options.includePaths ?? []) {
    const rel = toPosixPath(extra);
    if (!untrackedCandidates.includes(rel)) untrackedCandidates.push(rel);
  }

  const untrackedFiles = [];
  const excluded = [];
  for (const rel of untrackedCandidates.sort()) {
    const check = classifyPath(rel);
    if (check.excluded) {
      excluded.push({ path: rel, reason: check.reason });
      continue;
    }
    const abs = join(repoRoot, rel);
    if (!existsSync(abs) || !statSync(abs).isFile()) continue;
    const buf = readFileSync(abs);
    untrackedFiles.push({
      path: rel,
      size: buf.length,
      sha256: sha256Buffer(buf),
    });
  }

  return {
    workspaceId: defaultId,
    agent: options.agent || detectAgent(),
    branch,
    baseSha,
    taskId,
    trackedChanges,
    untrackedFiles,
    excluded,
  };
}

export function buildHandoffMarkdown(meta) {
  const lines = [
    `# Workspace Capsule: \`${meta.workspaceId}\``,
    "",
    `- **Last Agent**: \`${meta.agent}\``,
    `- **Branch**: \`${meta.branch}\``,
    `- **Base Commit (` + "HEAD" + `)**: \`${meta.baseSha}\``,
    `- **Task ID**: \`${meta.taskId ?? "none"}\``,
    `- **Updated At**: \`${meta.updatedAt}\``,
    `- **WIP Patch**: \`wip.patch\` (${meta.patch.size} bytes, sha256 \`${meta.patch.sha256.slice(0, 16)}…\`)`,
    "",
    "## Handoff Note",
    "",
    meta.note || "No handoff note provided.",
    "",
    "## Tracked Uncommitted Changes",
    "",
    ...(meta.trackedChanges.length
      ? meta.trackedChanges.map((item) => `- \`${item.status}\` \`${item.path}\``)
      : ["- (clean tracked tree)"]),
    "",
    "## Untracked Capsule Files",
    "",
    ...(meta.untrackedFiles.length
      ? meta.untrackedFiles.map((item) => `- \`${item.path}\` (${item.size} bytes)`)
      : ["- (no untracked files)"]),
    "",
    "## Resume in Claude Code, Codex or Gemini",
    "",
    "```bash",
    `npm run ws -- pull ${meta.workspaceId}`,
    "```",
    "",
  ];
  return lines.join("\n");
}

export function packCapsuleToStage(repoRoot, stageDir, options = {}) {
  const info = inspectWorktree(repoRoot, options);
  const capsuleDir = join(stageDir, info.workspaceId);
  mkdirSync(capsuleDir, { recursive: true });

  const patchBuffer = execFileSync("git", ["diff", "--binary", "HEAD"], {
    cwd: repoRoot,
    maxBuffer: 64 * 1024 * 1024,
    stdio: ["ignore", "pipe", "pipe"],
  });
  const patchPath = join(capsuleDir, "wip.patch");
  writeFileSync(patchPath, patchBuffer);

  const untrackedRoot = join(capsuleDir, "untracked");
  mkdirSync(untrackedRoot, { recursive: true });
  for (const item of info.untrackedFiles) {
    const src = join(repoRoot, item.path);
    const dst = join(untrackedRoot, item.path);
    mkdirSync(dirname(dst), { recursive: true });
    cpSync(src, dst);
  }

  const meta = {
    schemaVersion: 1,
    workspaceId: info.workspaceId,
    agent: info.agent,
    branch: info.branch,
    baseSha: info.baseSha,
    taskId: info.taskId,
    updatedAt: options.now || new Date().toISOString(),
    note: options.note || "",
    patch: {
      size: patchBuffer.length,
      sha256: sha256Buffer(patchBuffer),
    },
    trackedChanges: info.trackedChanges,
    untrackedFiles: info.untrackedFiles,
    excluded: info.excluded,
  };

  writeFileSync(join(capsuleDir, "meta.json"), `${JSON.stringify(meta, null, 2)}\n`, "utf8");
  writeFileSync(join(capsuleDir, "HANDOFF.md"), buildHandoffMarkdown(meta), "utf8");
  return { capsuleDir, meta };
}

export function verifyCapsuleDir(capsuleDir) {
  const metaPath = join(capsuleDir, "meta.json");
  if (!existsSync(metaPath)) {
    throw new Error(`Missing meta.json in capsule directory: ${capsuleDir}`);
  }
  const meta = JSON.parse(readFileSync(metaPath, "utf8"));
  const patchPath = join(capsuleDir, "wip.patch");
  if (!existsSync(patchPath)) {
    throw new Error("Missing wip.patch in capsule directory");
  }
  const actualPatchSha = sha256File(patchPath);
  if (actualPatchSha !== meta.patch?.sha256) {
    throw new Error(`wip.patch sha256 mismatch: expected ${meta.patch?.sha256}, got ${actualPatchSha}`);
  }
  for (const item of meta.untrackedFiles ?? []) {
    const check = classifyPath(item.path);
    if (check.excluded) {
      throw new Error(`Refusing excluded path in capsule untracked list: ${item.path} (${check.reason})`);
    }
    const filePath = join(capsuleDir, "untracked", item.path);
    if (!existsSync(filePath)) {
      throw new Error(`Missing untracked file in capsule: ${item.path}`);
    }
    const actualSha = sha256File(filePath);
    if (actualSha !== item.sha256) {
      throw new Error(`SHA-256 mismatch for ${item.path}: expected ${item.sha256}, got ${actualSha}`);
    }
  }
  return meta;
}

function syncCapsuleToTarget(capsuleDir, targetBase, workspaceId, { dryRun = false, runner = execFileSync } = {}) {
  if (isRcloneRemote(targetBase)) {
    const remoteDest = `${targetBase.replace(/\/+$/, "")}/${workspaceId}`;
    const copyArgs = ["copy", "--checksum", capsuleDir, remoteDest];
    const checkArgs = ["check", "--one-way", capsuleDir, remoteDest];
    if (!dryRun) {
      runner("rclone", copyArgs, { stdio: "inherit" });
      runner("rclone", checkArgs, { stdio: "inherit" });
    }
    return { mode: "rclone", destination: remoteDest, commands: [["rclone", ...copyArgs], ["rclone", ...checkArgs]] };
  }

  const destDir = join(resolve(targetBase), workspaceId);
  if (!dryRun) {
    rmSync(destDir, { recursive: true, force: true });
    mkdirSync(dirname(destDir), { recursive: true });
    cpSync(capsuleDir, destDir, { recursive: true });
    verifyCapsuleDir(destDir);
  }
  return { mode: "local", destination: destDir, commands: [] };
}

function fetchCapsuleFromTarget(targetBase, workspaceId, tempStage, { runner = execFileSync } = {}) {
  const id = sanitizeWorkspaceId(workspaceId);
  if (isRcloneRemote(targetBase)) {
    const remoteSrc = `${targetBase.replace(/\/+$/, "")}/${id}`;
    const localCapsule = join(tempStage, id);
    mkdirSync(localCapsule, { recursive: true });
    runner("rclone", ["copy", "--checksum", remoteSrc, localCapsule], { stdio: "inherit" });
    return localCapsule;
  }
  const localCapsule = join(resolve(targetBase), id);
  if (!existsSync(localCapsule)) {
    throw new Error(`Capsule not found at ${localCapsule}`);
  }
  return localCapsule;
}

export function pushWorkspace(repoRoot, options = {}) {
  const targetBase = resolveDriveTarget(options.dest);
  const stage = mkdtempSync(join(tmpdir(), "ws-capsule-push-"));
  try {
    const { capsuleDir, meta } = packCapsuleToStage(repoRoot, stage, options);
    verifyCapsuleDir(capsuleDir);
    const syncResult = syncCapsuleToTarget(capsuleDir, targetBase, meta.workspaceId, {
      dryRun: Boolean(options.dryRun),
      runner: options.runner,
    });
    return { meta, ...syncResult };
  } finally {
    rmSync(stage, { recursive: true, force: true });
  }
}

export function pullWorkspace(repoRoot, workspaceId, options = {}) {
  const targetBase = resolveDriveTarget(options.dest);
  const stage = mkdtempSync(join(tmpdir(), "ws-capsule-pull-"));
  try {
    const capsuleDir = fetchCapsuleFromTarget(targetBase, workspaceId, stage, {
      runner: options.runner,
    });
    const meta = verifyCapsuleDir(capsuleDir);
    const handoff = existsSync(join(capsuleDir, "HANDOFF.md"))
      ? readFileSync(join(capsuleDir, "HANDOFF.md"), "utf8")
      : buildHandoffMarkdown(meta);

    if (!options.dryRun) {
      const currentBranch = runGit(repoRoot, ["rev-parse", "--abbrev-ref", "HEAD"]).trim();
      if (!options.noCheckout && meta.branch && meta.branch !== "HEAD" && currentBranch !== meta.branch) {
        const dirty = runGit(repoRoot, ["status", "--porcelain"]).trim();
        if (dirty) {
          throw new Error(
            `Worktree has uncommitted changes on ${currentBranch}; commit/stash or pass --no-checkout before pulling ${meta.branch}`,
          );
        }
        try {
          runGit(repoRoot, ["checkout", meta.branch]);
        } catch {
          runGit(repoRoot, ["checkout", "-b", meta.branch, meta.baseSha]);
        }
      }

      const patchPath = join(capsuleDir, "wip.patch");
      if (meta.patch?.size > 0) {
        runGit(repoRoot, ["apply", "--whitespace=nowarn", patchPath]);
      }

      for (const item of meta.untrackedFiles ?? []) {
        const src = join(capsuleDir, "untracked", item.path);
        const dst = join(repoRoot, item.path);
        mkdirSync(dirname(dst), { recursive: true });
        cpSync(src, dst);
      }
    }

    return { meta, handoff };
  } finally {
    rmSync(stage, { recursive: true, force: true });
  }
}

export function listWorkspaces(options = {}) {
  const targetBase = resolveDriveTarget(options.dest);
  if (isRcloneRemote(targetBase)) {
    const runner = options.runner ?? execFileSync;
    const raw = runner("rclone", ["lsf", "--dirs-only", targetBase], { encoding: "utf8" });
    return raw
      .split(/\r?\n/)
      .map((line) => line.trim().replace(/\/+$/, ""))
      .filter(Boolean)
      .map((id) => ({ workspaceId: id, source: `${targetBase.replace(/\/+$/, "")}/${id}` }));
  }

  const baseDir = resolve(targetBase);
  if (!existsSync(baseDir)) return [];
  const entries = [];
  for (const entry of readdirSync(baseDir, { withFileTypes: true })) {
    if (!entry.isDirectory()) continue;
    const metaPath = join(baseDir, entry.name, "meta.json");
    if (!existsSync(metaPath)) continue;
    try {
      const meta = JSON.parse(readFileSync(metaPath, "utf8"));
      entries.push({
        workspaceId: meta.workspaceId,
        agent: meta.agent,
        branch: meta.branch,
        baseSha: meta.baseSha,
        updatedAt: meta.updatedAt,
        note: meta.note,
        source: join(baseDir, entry.name),
      });
    } catch {
      // skip malformed directory
    }
  }
  return entries.sort((a, b) => String(b.updatedAt).localeCompare(String(a.updatedAt)));
}

export function buildDelegateCommand({ to, prompt, slot = "default", hostAccountsDir = "/var/lib/mokaair-ai-accounts" }) {
  const target = String(to ?? "").toLowerCase();
  if (!VALID_AGENTS.has(target)) {
    throw new Error(`Invalid target agent "${to}"; expected one of: claude, codex, gemini`);
  }
  const chosenSlot = String(slot ?? "default").toLowerCase();
  if (!VALID_SLOTS.has(chosenSlot)) {
    throw new Error(`Invalid account slot "${slot}"; expected a..e or default`);
  }
  if (!prompt || !String(prompt).trim()) {
    throw new Error("Delegation prompt cannot be empty.");
  }

  const hasHostPool = existsSync(hostAccountsDir);
  if (target === "claude") {
    const bin = hasHostPool && chosenSlot !== "default" ? `/usr/local/bin/claude-${chosenSlot}` : "claude";
    return { binary: bin, args: ["-p", String(prompt)] };
  }
  if (target === "codex") {
    const bin = hasHostPool && chosenSlot !== "default" ? `/usr/local/bin/codex-${chosenSlot}` : "codex";
    return { binary: bin, args: ["exec", "--sandbox", "read-only", String(prompt)] };
  }
  // Gemini / Antigravity CLI (`agy` on the host, or `gemini` CLI locally)
  const bin = hasHostPool
    ? chosenSlot !== "default"
      ? `/usr/local/bin/agy-${chosenSlot}`
      : "agy"
    : "gemini";
  return { binary: bin, args: ["-p", String(prompt)] };
}

function parseCliArgs(argv) {
  const positional = [];
  const flags = { includePaths: [] };
  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg === "--dry-run") flags.dryRun = true;
    else if (arg === "--no-checkout") flags.noCheckout = true;
    else if (arg === "--id") flags.id = argv[++i];
    else if (arg === "--agent") flags.agent = argv[++i];
    else if (arg === "--note") flags.note = argv[++i];
    else if (arg === "--dest") flags.dest = argv[++i];
    else if (arg === "--include") flags.includePaths.push(argv[++i]);
    else if (arg === "--to") flags.to = argv[++i];
    else if (arg === "--prompt") flags.prompt = argv[++i];
    else if (arg === "--slot") flags.slot = argv[++i];
    else positional.push(arg);
  }
  return { command: positional[0] || "status", positional: positional.slice(1), flags };
}

export function main(argv = process.argv.slice(2), repoRoot = ROOT) {
  const { command, positional, flags } = parseCliArgs(argv);
  if (command === "status") {
    const info = inspectWorktree(repoRoot, flags);
    const dest = resolveDriveTarget(flags.dest);
    console.log(
      JSON.stringify(
        {
          ...info,
          driveTarget: dest,
          transport: isRcloneRemote(dest) ? "rclone" : "local-drive",
        },
        null,
        2,
      ),
    );
    return 0;
  }
  if (command === "push") {
    const id = positional[0] || flags.id;
    const result = pushWorkspace(repoRoot, { ...flags, id });
    console.log(
      `ws push: ${result.meta.workspaceId} (${result.meta.trackedChanges.length} tracked, ${result.meta.untrackedFiles.length} untracked) -> ${result.destination}${flags.dryRun ? " [dry-run]" : ""}`,
    );
    return 0;
  }
  if (command === "pull") {
    const id = positional[0] || flags.id;
    if (!id) throw new Error("Usage: npm run ws -- pull <workspace-id> [--dest <target>]");
    const result = pullWorkspace(repoRoot, id, flags);
    console.log(`ws pull: ${result.meta.workspaceId} (branch ${result.meta.branch} @ ${result.meta.baseSha.slice(0, 12)})`);
    console.log(result.handoff);
    return 0;
  }
  if (command === "list") {
    const items = listWorkspaces(flags);
    console.log(JSON.stringify(items, null, 2));
    return 0;
  }
  if (command === "delegate") {
    const spec = buildDelegateCommand(flags);
    if (flags.dryRun) {
      console.log(JSON.stringify(spec, null, 2));
      return 0;
    }
    const out = execFileSync(spec.binary, spec.args, { cwd: repoRoot, encoding: "utf8" });
    process.stdout.write(out);
    return 0;
  }
  throw new Error(`Unknown ws command "${command}". Supported: status, push, pull, list, delegate`);
}

if (process.argv[1] && resolve(process.argv[1]) === resolve(fileURLToPath(import.meta.url))) {
  try {
    process.exitCode = main();
  } catch (err) {
    console.error(`ws error: ${err instanceof Error ? err.message : String(err)}`);
    process.exitCode = 1;
  }
}
