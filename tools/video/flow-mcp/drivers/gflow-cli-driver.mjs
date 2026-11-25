/**
 * Route A Google Flow driver wrapping `gflow-cli` (`ffroliva/gflow-cli`).
 *
 * Uses `gflow --json` subcommands with per-subcommand `--profile`, `--project`,
 * `--out-file`, `--max-credits`, and `GFLOW_CLI_EXIT_CODES=2`.
 * Supports Windows (`gflow.exe` in PATH or `%USERPROFILE%\.local\bin`), macOS,
 * and Linux, plus full async abort support for `flow_cancel`.
 */

import { spawn } from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import {
  DEFAULT_IMAGE_MODEL,
  DEFAULT_MAX_CREDITS_PER_CLIP,
  DEFAULT_VIDEO_DURATION_SEC,
  DEFAULT_VIDEO_MODEL,
  DEFAULT_VIDEO_RESOLUTION,
  resolveRuntimeHome,
} from "../config.mjs";
import { FlowDriver, FlowDriverError, classifyDriverError } from "./driver-interface.mjs";

/**
 * Resolves the `gflow` executable path, checking explicit overrides and
 * Windows `uv tool install` shim locations (`%USERPROFILE%\.local\bin\gflow.exe`).
 */
export function resolveGflowBinary({
  env = process.env,
  platform = process.platform,
  homedir = os.homedir(),
  existsSync = fs.existsSync,
} = {}) {
  if (env.MOKAAIR_GFLOW_BIN && env.MOKAAIR_GFLOW_BIN.trim()) {
    return env.MOKAAIR_GFLOW_BIN.trim();
  }

  if (platform === "win32") {
    const userProfile = env.USERPROFILE || homedir;
    const candidates = [
      path.win32.join(userProfile, ".local", "bin", "gflow.exe"),
      path.win32.join(env.LOCALAPPDATA || path.win32.join(userProfile, "AppData", "Local"), "uv", "bin", "gflow.exe"),
    ];
    for (const candidate of candidates) {
      if (existsSync(candidate)) return candidate;
    }
    return "gflow.exe";
  }

  const unixLocal = path.join(homedir, ".local", "bin", "gflow");
  if (existsSync(unixLocal)) return unixLocal;
  return "gflow";
}

function parseLastJson(stdout) {
  const trimmed = String(stdout || "").trim();
  if (!trimmed) return null;
  try {
    return JSON.parse(trimmed);
  } catch {
    // Some CLI invocations print preamble lines before a final JSON object
    const lines = trimmed.split(/\r?\n/).reverse();
    for (const line of lines) {
      const candidate = line.trim();
      if (candidate.startsWith("{") && candidate.endsWith("}")) {
        try {
          return JSON.parse(candidate);
        } catch {
          // continue searching
        }
      }
    }
    return null;
  }
}

export function defaultRunProcess(binary, args, { env, signal, timeoutMs = 10 * 60 * 1000 } = {}) {
  return new Promise((resolve, reject) => {
    const child = spawn(binary, args, {
      env,
      stdio: ["ignore", "pipe", "pipe"],
      windowsHide: true,
    });

    let stdout = "";
    let stderr = "";
    let finished = false;
    let timer = null;

    const cleanup = () => {
      if (timer) clearTimeout(timer);
      if (signal) signal.removeEventListener("abort", onAbort);
    };

    const onAbort = () => {
      if (finished) return;
      finished = true;
      cleanup();
      try {
        child.kill("SIGTERM");
      } catch {
        // ignore kill error
      }
      reject(
        new FlowDriverError("Operation cancelled by caller.", {
          code: "cancelled",
          exitCode: 130,
          retryable: false,
          charged: "maybe",
          nextAction: "reconcile",
        }),
      );
    };

    if (signal) {
      if (signal.aborted) {
        onAbort();
        return;
      }
      signal.addEventListener("abort", onAbort, { once: true });
    }

    if (timeoutMs > 0) {
      timer = setTimeout(() => {
        if (finished) return;
        finished = true;
        cleanup();
        try {
          child.kill("SIGTERM");
        } catch {
          // ignore
        }
        reject(
          new FlowDriverError(`gflow command timed out after ${timeoutMs}ms.`, {
            code: "process_timeout",
            exitCode: 9,
            retryable: false,
            charged: "maybe",
            nextAction: "reconcile",
          }),
        );
      }, timeoutMs);
    }

    child.stdout.on("data", (chunk) => {
      stdout += chunk.toString("utf8");
    });
    child.stderr.on("data", (chunk) => {
      stderr += chunk.toString("utf8");
    });

    child.on("error", (err) => {
      if (finished) return;
      finished = true;
      cleanup();
      if (err.code === "ENOENT") {
        reject(
          new FlowDriverError(
            `gflow executable "${binary}" was not found on PATH. Install it with: uv tool install gflow-cli`,
            {
              code: "gflow_not_installed",
              exitCode: 127,
              retryable: false,
              charged: "no",
              nextAction: "fix_input",
              remediation: "Install uv (https://docs.astral.sh/uv/) then run `uv tool install gflow-cli`.",
            },
          ),
        );
        return;
      }
      reject(
        new FlowDriverError(`Failed to spawn gflow: ${err.message}`, {
          code: "spawn_error",
          exitCode: 1,
          retryable: false,
          charged: "no",
          nextAction: "fix_input",
        }),
      );
    });

    child.on("close", (code) => {
      if (finished) return;
      finished = true;
      cleanup();
      resolve({ exitCode: code ?? 1, stdout, stderr });
    });
  });
}

export class GflowCliDriver extends FlowDriver {
  constructor({
    binary,
    profile = null,
    runtimeHome,
    env = process.env,
    platform = process.platform,
    runProcess = defaultRunProcess,
  } = {}) {
    super({ name: "gflow-cli" });
    this.env = env;
    this.platform = platform;
    this.binary = binary || resolveGflowBinary({ env, platform });
    this.profile = profile || env.MOKAAIR_FLOW_PROFILE || null;
    this.runtimeHome = runtimeHome || resolveRuntimeHome({ env, platform });
    this.runProcess = runProcess;
  }

  buildEnv() {
    const gflowHome =
      this.env.GFLOW_CLI_HOME ||
      (this.platform === "win32"
        ? path.win32.join(this.runtimeHome, "gflow-home")
        : path.join(this.runtimeHome, "gflow-home"));
    return {
      ...this.env,
      GFLOW_CLI_HOME: gflowHome,
      GFLOW_CLI_EXIT_CODES: "2",
    };
  }

  /**
   * Appends per-subcommand `--profile NAME` when configured (per gflow-cli docs,
   * `--profile` must come after the subcommand, never globally).
   */
  withProfile(args, overrideProfile = null) {
    const p = overrideProfile || this.profile;
    return p ? [...args, "--profile", p] : [...args];
  }

  async execJson(args, { signal, timeoutMs, allowNonZeroJson = false } = {}) {
    const result = await this.runProcess(this.binary, args, {
      env: this.buildEnv(),
      signal,
      timeoutMs,
    });
    const parsed = parseLastJson(result.stdout);

    if (result.exitCode !== 0) {
      if (allowNonZeroJson && parsed) {
        return { exitCode: result.exitCode, json: parsed, stderr: result.stderr };
      }
      throw classifyDriverError({
        exitCode: result.exitCode,
        json: parsed,
        stderr: result.stderr,
        command: `${this.binary} ${args.join(" ")}`,
      });
    }

    if (parsed && (parsed.status === "fail" || parsed.status === "error")) {
      throw classifyDriverError({
        exitCode: parsed.error?.exit_code ?? 1,
        json: parsed,
        stderr: result.stderr,
        command: `${this.binary} ${args.join(" ")}`,
      });
    }

    return { exitCode: 0, json: parsed ?? { rawStdout: result.stdout.trim() }, stderr: result.stderr };
  }

  getLoginCommand({ profile = null } = {}) {
    const args = this.withProfile(["auth", "login", "--browser", "chrome"], profile);
    return { binary: this.binary, args, env: this.buildEnv() };
  }

  async checkAuth({ profile = null, signal } = {}) {
    const args = this.withProfile(["auth", "status", "--json"], profile);
    const { exitCode, json } = await this.execJson(args, { signal, allowNonZeroJson: true, timeoutMs: 30_000 });
    const authenticated =
      exitCode === 0 &&
      (json?.authenticated === true ||
        json?.status === "authenticated" ||
        json?.status === "ok" ||
        json?.logged_in === true);
    return {
      authenticated,
      profile: profile || this.profile || json?.profile || "default",
      account: json?.email || json?.account || null,
      plan: json?.plan || json?.tier || null,
      raw: json,
    };
  }

  async getCredits({ profile = null, refresh = false, signal } = {}) {
    const base = ["credits", "user", "--json"];
    if (refresh) base.push("--refresh");
    const args = this.withProfile(base, profile);
    const { json } = await this.execJson(args, { signal, timeoutMs: 45_000 });
    const balance =
      json?.credits ??
      json?.balance ??
      json?.remaining_credits ??
      json?.remaining ??
      null;
    return {
      credits: balance != null ? Number(balance) : null,
      plan: json?.plan || json?.tier || null,
      raw: json,
    };
  }

  async createProject({ name, profile = null, signal }) {
    const args = this.withProfile(["project", "create", "--name", String(name), "--json"], profile);
    const { json } = await this.execJson(args, { signal, timeoutMs: 90_000 });
    const projectId = json?.project_id || json?.id || json?.project?.id || null;
    if (!projectId) {
      throw new FlowDriverError("gflow project create succeeded without returning a project_id.", {
        code: "missing_project_id",
        exitCode: 1,
        retryable: false,
        charged: "no",
        nextAction: "fix_input",
        raw: json,
      });
    }
    return { projectId, name, raw: json };
  }

  async uploadAsset({ filePath, projectId = null, profile = null, signal }) {
    const base = ["image", "upload", filePath, "--json"];
    if (projectId) base.push("--project", String(projectId));
    const args = this.withProfile(base, profile);
    const { json } = await this.execJson(args, { signal, timeoutMs: 120_000 });
    return {
      assetUuid: json?.asset_uuid || json?.media_id || json?.uuid || json?.id || null,
      filePath,
      projectId,
      raw: json,
    };
  }

  buildImageArgs({
    prompt,
    refs = [],
    model = DEFAULT_IMAGE_MODEL,
    aspect = "16:9",
    projectId = null,
    outFile,
    profile = null,
  }) {
    const cleanRefs = (refs || []).filter(Boolean);
    const base = cleanRefs.length > 0 ? ["image", "i2i", prompt] : ["image", "t2i", prompt];
    for (const ref of cleanRefs) {
      base.push("--ref", String(ref));
    }
    base.push("--model", String(model), "--aspect", String(aspect));
    if (projectId) base.push("--project", String(projectId));
    if (outFile) base.push("--out-file", String(outFile));
    base.push("--json");
    return this.withProfile(base, profile);
  }

  async generateImage(params) {
    const args = this.buildImageArgs(params);
    const { json } = await this.execJson(args, {
      signal: params.signal,
      timeoutMs: params.timeoutMs ?? 5 * 60 * 1000,
    });
    return {
      outFile: params.outFile || json?.out_file || json?.path || json?.files?.[0] || null,
      mediaId: json?.media_id || json?.id || json?.images?.[0]?.media_id || null,
      projectId: params.projectId || json?.project_id || null,
      model: params.model || DEFAULT_IMAGE_MODEL,
      charged: "no",
      raw: json,
    };
  }

  buildVideoArgs({
    prompt,
    initialFrame = null,
    endFrame = null,
    refs = [],
    model = DEFAULT_VIDEO_MODEL,
    aspect = "16:9",
    durationSec = DEFAULT_VIDEO_DURATION_SEC,
    resolution = DEFAULT_VIDEO_RESOLUTION,
    maxCredits = DEFAULT_MAX_CREDITS_PER_CLIP,
    projectId = null,
    outFile,
    profile = null,
  }) {
    const cleanRefs = (refs || []).filter(Boolean);
    let base;
    if (initialFrame) {
      base = ["video", "i2v", "--initial-frame", String(initialFrame)];
      if (endFrame) base.push("--end-frame", String(endFrame));
      base.push(prompt);
    } else if (cleanRefs.length > 0) {
      base = ["video", "r2v", prompt];
      for (const ref of cleanRefs) {
        base.push("--ref", String(ref));
      }
    } else {
      base = ["video", "t2v", prompt];
    }

    base.push("--model", String(model), "--aspect", String(aspect));
    if (durationSec != null) base.push("--duration", String(durationSec));
    if (resolution && /^omni/i.test(String(model))) {
      base.push("--resolution", String(resolution));
    }
    if (maxCredits != null) base.push("--max-credits", String(maxCredits));
    if (projectId) base.push("--project", String(projectId));
    if (outFile) base.push("--out-file", String(outFile));
    base.push("--json");
    return this.withProfile(base, profile);
  }

  async generateVideo(params) {
    const args = this.buildVideoArgs(params);
    const { json } = await this.execJson(args, {
      signal: params.signal,
      timeoutMs: params.timeoutMs ?? 8 * 60 * 1000,
    });
    return {
      outFile: params.outFile || json?.out_file || json?.path || json?.video_path || null,
      mediaId: json?.media_id || json?.id || null,
      projectId: params.projectId || json?.project_id || null,
      model: params.model || DEFAULT_VIDEO_MODEL,
      creditsSpent: json?.credits_spent ?? json?.quoted_credits ?? null,
      charged: json?.charged || "yes",
      raw: json,
    };
  }

  async getVersion({ signal } = {}) {
    try {
      const res = await this.runProcess(this.binary, ["--version"], {
        env: this.buildEnv(),
        signal,
        timeoutMs: 10_000,
      });
      if (res.exitCode !== 0) return null;
      return `${res.stdout || ""}${res.stderr || ""}`.trim().split(/\r?\n/)[0] || null;
    } catch {
      return null;
    }
  }

  async listProfiles({ refreshCredits = false, signal } = {}) {
    const authRes = await this.execJson(["auth", "list", "--json"], {
      signal,
      allowNonZeroJson: true,
      timeoutMs: 30_000,
    });
    const rawProfiles = Array.isArray(authRes.json)
      ? authRes.json
      : Array.isArray(authRes.json?.profiles)
        ? authRes.json.profiles
        : [];

    let creditsMap = {};
    try {
      const credArgs = ["credits", "list", "--json"];
      if (refreshCredits) credArgs.push("--refresh");
      const credRes = await this.execJson(credArgs, { signal, timeoutMs: 45_000 });
      const rows = Array.isArray(credRes.json)
        ? credRes.json
        : Array.isArray(credRes.json?.profiles)
          ? credRes.json.profiles
          : [];
      for (const row of rows) {
        const key = row?.profile || row?.name;
        if (key) creditsMap[key] = row;
      }
    } catch {
      creditsMap = {};
    }

    return rawProfiles.map((p) => {
      const name = typeof p === "string" ? p : p.name || p.profile || "default";
      const cred = creditsMap[name] || {};
      return {
        profile: name,
        isDefault: Boolean(p?.default || p?.is_default),
        authenticated: p?.authenticated ?? true,
        account: p?.email || p?.account || cred?.email || null,
        plan: p?.plan || cred?.plan || cred?.tier || null,
        credits: cred?.credits ?? cred?.balance ?? cred?.remaining ?? null,
      };
    });
  }

  buildCreateCharacterArgs({
    projectId,
    name,
    imagePath = null,
    bodyImagePath = null,
    facePrompt = null,
    bodyPrompt = null,
    voice = null,
    profile = null,
  }) {
    const base = ["character", "create", "--project", String(projectId), "--name", String(name)];
    if (imagePath) base.push("--image", String(imagePath));
    if (bodyImagePath) base.push("--body-image", String(bodyImagePath));
    if (facePrompt) base.push("--face-prompt", String(facePrompt));
    if (bodyPrompt) base.push("--body-prompt", String(bodyPrompt));
    if (voice) base.push("--voice", String(voice));
    base.push("--json");
    return this.withProfile(base, profile);
  }

  async createCharacter(params) {
    const args = this.buildCreateCharacterArgs(params);
    const { json } = await this.execJson(args, {
      signal: params.signal,
      timeoutMs: params.timeoutMs ?? 4 * 60 * 1000,
    });
    return {
      entityId: json?.entity_id || json?.id || null,
      name: json?.name || params.name,
      projectId: params.projectId,
      raw: json,
    };
  }

  async listCharacters({ projectId, profile = null, signal }) {
    const args = this.withProfile(["character", "list", "--project", String(projectId), "--json"], profile);
    const { json } = await this.execJson(args, { signal, timeoutMs: 45_000 });
    return Array.isArray(json) ? json : Array.isArray(json?.characters) ? json.characters : [];
  }

  buildExtendVideoArgs({
    source,
    prompt,
    projectId = null,
    durationSec = null,
    refs = [],
    maxCredits = DEFAULT_MAX_CREDITS_PER_CLIP,
    outFile = null,
    profile = null,
  }) {
    const base = ["video", "extend", String(source), String(prompt)];
    if (projectId) base.push("--project", String(projectId));
    if (durationSec != null) base.push("--duration", String(durationSec));
    for (const ref of (refs || []).filter(Boolean)) {
      base.push("--ref", String(ref));
    }
    if (maxCredits != null) base.push("--max-credits", String(maxCredits));
    if (outFile) base.push("--out-file", String(outFile));
    base.push("--json");
    return this.withProfile(base, profile);
  }

  async extendVideo(params) {
    const args = this.buildExtendVideoArgs(params);
    const { json } = await this.execJson(args, {
      signal: params.signal,
      timeoutMs: params.timeoutMs ?? 8 * 60 * 1000,
    });
    return {
      outFile: params.outFile || json?.out_file || json?.path || json?.video_path || null,
      mediaId: json?.media_id || json?.id || null,
      projectId: params.projectId || json?.project_id || null,
      creditsSpent: json?.credits_spent ?? json?.quoted_credits ?? null,
      charged: json?.charged || "yes",
      raw: json,
    };
  }

  async listRemoteVideos({ limit = 50, profile = null, signal } = {}) {
    const args = this.withProfile(["data", "list", "videos", "--limit", String(limit), "--json"], profile);
    const { json } = await this.execJson(args, { signal, timeoutMs: 45_000 });
    return Array.isArray(json) ? json : Array.isArray(json?.videos) ? json.videos : Array.isArray(json?.items) ? json.items : [];
  }

  async downloadMedia({ mediaId, outDir, profile = null, signal }) {
    const base = ["data", "download", String(mediaId)];
    if (outDir) base.push("--out", String(outDir));
    base.push("--json");
    const args = this.withProfile(base, profile);
    const { json } = await this.execJson(args, { signal, timeoutMs: 3 * 60 * 1000 });
    return {
      mediaId,
      outFile: json?.out_file || json?.path || json?.file || null,
      raw: json,
    };
  }

  buildUpscaleImageArgs({
    mediaId,
    scale = "2k",
    projectId = null,
    outFile = null,
    profile = null,
  }) {
    const cleanScale = String(scale || "2k").toLowerCase();
    if (cleanScale !== "2k" && cleanScale !== "4k") {
      throw new Error(`Invalid upscale scale "${scale}". Expected "2k" or "4k".`);
    }
    const base = ["image", "upscale", String(mediaId), "--scale", cleanScale];
    if (projectId) base.push("--project", String(projectId));
    if (outFile) base.push("--out-file", String(outFile));
    base.push("--json");
    return this.withProfile(base, profile);
  }

  async upscaleImage(params) {
    const args = this.buildUpscaleImageArgs(params);
    const { json } = await this.execJson(args, {
      signal: params.signal,
      timeoutMs: params.timeoutMs ?? 4 * 60 * 1000,
    });
    return {
      mediaId: params.mediaId,
      scale: String(params.scale || "2k").toLowerCase(),
      outFile: params.outFile || json?.out_file || json?.path || null,
      raw: json,
    };
  }
}
