import assert from "node:assert/strict";
import { execFileSync } from "node:child_process";
import { existsSync, mkdirSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import test from "node:test";

import {
  buildDelegateCommand,
  classifyPath,
  detectAgent,
  isRcloneRemote,
  listWorkspaces,
  pullWorkspace,
  pushWorkspace,
  verifyCapsuleDir,
} from "./workspace-sync.mjs";

function initTempGitRepo() {
  const dir = mkdtempSync(join(tmpdir(), "ws-repo-"));
  execFileSync("git", ["init", "-b", "main"], { cwd: dir });
  execFileSync("git", ["config", "user.name", "Test Agent"], { cwd: dir });
  execFileSync("git", ["config", "user.email", "agent@example.com"], { cwd: dir });
  mkdirSync(join(dir, "tasks", "open"), { recursive: true });
  writeFileSync(
    join(dir, "tasks", "open", "2026-11-20-demo.md"),
    "---\nid: 2026-11-20-demo\nbranch: claude/demo-task\n---\n# Demo\n",
    "utf8",
  );
  writeFileSync(join(dir, "README.md"), "# Demo repo\n", "utf8");
  execFileSync("git", ["add", "."], { cwd: dir });
  execFileSync("git", ["commit", "-m", "initial"], { cwd: dir });
  execFileSync("git", ["checkout", "-b", "claude/demo-task"], { cwd: dir });
  return dir;
}

test("detectAgent identifies Claude, Codex and Gemini from environment variables", () => {
  assert.equal(detectAgent({ CLAUDE_CODE: "1" }), "claude");
  assert.equal(detectAgent({ CODEX_HOME: "/var/lib/mokaair-ai-accounts/codex-a" }), "codex");
  assert.equal(detectAgent({ USER: "antigravity" }), "gemini");
  assert.equal(detectAgent({ WORKSPACE_AGENT: "Codex", USER: "antigravity" }), "codex");
});

test("isRcloneRemote distinguishes rclone remotes from Windows drive paths and POSIX paths", () => {
  assert.equal(isRcloneRemote("videobackup:工作區"), true);
  assert.equal(isRcloneRemote("G:/我的雲端硬碟/AI/工作區"), false);
  assert.equal(isRcloneRemote("C:\\Users\\Public\\workspace"), false);
  assert.equal(isRcloneRemote("/content/drive/MyDrive/AI/工作區"), false);
});

test("classifyPath excludes secrets and rebuildable directories while keeping work files", () => {
  assert.deepEqual(classifyPath(".env"), { excluded: true, reason: "credential-or-secret" });
  assert.deepEqual(classifyPath("apps/web/.env.local"), { excluded: true, reason: "credential-or-secret" });
  assert.deepEqual(classifyPath("oauth-token.json"), { excluded: true, reason: "credential-or-secret" });
  assert.deepEqual(classifyPath("mokaair-backup.key"), { excluded: true, reason: "credential-or-secret" });
  assert.deepEqual(classifyPath("node_modules/pkg/index.js"), { excluded: true, reason: "rebuildable-dependency" });
  assert.deepEqual(classifyPath("apps/api/.venv/pyvenv.cfg"), { excluded: true, reason: "rebuildable-dependency" });
  assert.deepEqual(classifyPath("docs/videos/curio-h01/draft.md"), { excluded: false, reason: null });
});

test("pushWorkspace and pullWorkspace round-trip tracked diffs, untracked drafts and handoff notes across agents", (t) => {
  const repoA = initTempGitRepo();
  const driveDir = mkdtempSync(join(tmpdir(), "ws-drive-"));
  const repoB = initTempGitRepo();
  t.after(() => {
    rmSync(repoA, { recursive: true, force: true });
    rmSync(driveDir, { recursive: true, force: true });
    rmSync(repoB, { recursive: true, force: true });
  });

  // Agent 1 (Claude) modifies a tracked file, writes an untracked draft, and has a local .env secret
  writeFileSync(join(repoA, "README.md"), "# Demo repo\nEdited by Claude\n", "utf8");
  mkdirSync(join(repoA, "scratch"), { recursive: true });
  writeFileSync(join(repoA, "scratch", "storyboard-notes.md"), "Scene 1 camera pan right\n", "utf8");
  writeFileSync(join(repoA, ".env.local"), "SECRET_KEY=do-not-upload\n", "utf8");

  const pushed = pushWorkspace(repoA, {
    dest: driveDir,
    agent: "claude",
    note: "Claude finished scene 1 notes; Gemini please audit keyframes.",
  });

  assert.equal(pushed.meta.workspaceId, "2026-11-20-demo");
  assert.equal(pushed.meta.agent, "claude");
  assert.equal(pushed.meta.trackedChanges.length, 1);
  assert.deepEqual(
    pushed.meta.untrackedFiles.map((f) => f.path),
    ["scratch/storyboard-notes.md"],
  );
  assert.ok(pushed.meta.excluded.some((e) => e.path === ".env.local"));
  assert.equal(existsSync(join(driveDir, "2026-11-20-demo", "untracked", ".env.local")), false);

  const listed = listWorkspaces({ dest: driveDir });
  assert.equal(listed.length, 1);
  assert.equal(listed[0].workspaceId, "2026-11-20-demo");
  assert.equal(listed[0].agent, "claude");

  // Agent 2 (Gemini) pulls the capsule into a clean clone on main
  execFileSync("git", ["checkout", "main"], { cwd: repoB });
  const pulled = pullWorkspace(repoB, "2026-11-20-demo", { dest: driveDir });

  assert.equal(pulled.meta.branch, "claude/demo-task");
  assert.match(pulled.handoff, /Gemini please audit keyframes/);
  assert.equal(readFileSync(join(repoB, "README.md"), "utf8"), "# Demo repo\nEdited by Claude\n");
  assert.equal(
    readFileSync(join(repoB, "scratch", "storyboard-notes.md"), "utf8"),
    "Scene 1 camera pan right\n",
  );
});

test("verifyCapsuleDir rejects a tampered wip.patch or untracked file", (t) => {
  const repo = initTempGitRepo();
  const driveDir = mkdtempSync(join(tmpdir(), "ws-tamper-"));
  t.after(() => {
    rmSync(repo, { recursive: true, force: true });
    rmSync(driveDir, { recursive: true, force: true });
  });

  writeFileSync(join(repo, "draft.txt"), "original content\n", "utf8");
  pushWorkspace(repo, { dest: driveDir, id: "tamper-check", agent: "codex" });

  const capsuleDir = join(driveDir, "tamper-check");
  writeFileSync(join(capsuleDir, "untracked", "draft.txt"), "corrupted content\n", "utf8");
  assert.throws(() => verifyCapsuleDir(capsuleDir), /SHA-256 mismatch for draft\.txt/);
});

test("pushWorkspace supports rclone remote targets with copy and one-way check", (t) => {
  const repo = initTempGitRepo();
  t.after(() => rmSync(repo, { recursive: true, force: true }));

  writeFileSync(join(repo, "notes.md"), "handoff via rclone\n", "utf8");
  const calls = [];
  const fakeRunner = (cmd, args) => {
    calls.push([cmd, ...args]);
    return "";
  };

  const result = pushWorkspace(repo, {
    dest: "videobackup:工作區",
    id: "rclone-capsule",
    agent: "gemini",
    runner: fakeRunner,
  });

  assert.equal(result.mode, "rclone");
  assert.equal(result.destination, "videobackup:工作區/rclone-capsule");
  assert.equal(calls.length, 2);
  assert.equal(calls[0][0], "rclone");
  assert.equal(calls[0][1], "copy");
  assert.equal(calls[1][1], "check");
});

test("buildDelegateCommand targets host account wrappers when present and safe CLI flags otherwise", (t) => {
  const fakeHostPool = mkdtempSync(join(tmpdir(), "ai-accounts-"));
  t.after(() => rmSync(fakeHostPool, { recursive: true, force: true }));

  assert.deepEqual(
    buildDelegateCommand({
      to: "codex",
      slot: "b",
      prompt: "Audit facts in article pack",
      hostAccountsDir: fakeHostPool,
    }),
    {
      binary: "/usr/local/bin/codex-b",
      args: ["exec", "--sandbox", "read-only", "Audit facts in article pack"],
    },
  );

  assert.deepEqual(
    buildDelegateCommand({
      to: "claude",
      slot: "c",
      prompt: "Review storyboard continuity",
      hostAccountsDir: fakeHostPool,
    }),
    {
      binary: "/usr/local/bin/claude-c",
      args: ["-p", "Review storyboard continuity"],
    },
  );

  assert.deepEqual(
    buildDelegateCommand({
      to: "gemini",
      slot: "a",
      prompt: "Check 2x zoom keyframes",
      hostAccountsDir: fakeHostPool,
    }),
    {
      binary: "/usr/local/bin/agy-a",
      args: ["-p", "Check 2x zoom keyframes"],
    },
  );
});
