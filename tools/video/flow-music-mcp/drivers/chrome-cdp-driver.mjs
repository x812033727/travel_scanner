/**
 * Zero-dependency Node.js 22 Chrome DevTools Protocol (CDP) driver for
 * Google Flow Music (`https://www.flowmusic.app`, Lyria 3.5).
 *
 * Security & reliability guarantees:
 *   - Uses a dedicated isolated `--user-data-dir` per profile under
 *     `%LOCALAPPDATA%\mokaair-flow-music\chrome-profiles\profile_<name>`.
 *     Never touches the owner's daily Chrome profile or passwords.
 *   - Executes Flow Music `/__api/...` calls via same-origin `fetch()` inside
 *     the signed-in page tab so auth cookies/tokens never leave Chrome.
 *   - Downloads audio bytes directly inside the page and streams chunks back
 *     over CDP, avoiding Chrome's "Allow multiple downloads" popup block and
 *     background-tab throttling.
 */

import { spawn } from "node:child_process";
import fs from "node:fs";
import net from "node:net";
import path from "node:path";
import {
  DEFAULT_DOWNLOAD_FORMAT,
  DEFAULT_MUSIC_MODEL,
  FLOW_MUSIC_ORIGIN,
  SUPPORTED_DOWNLOAD_FORMATS,
  resolveChromeBinary,
  resolveChromeProfileDir,
  resolveChromeProfilesRoot,
  resolveRuntimeHome,
  sanitizeProfileName,
} from "../config.mjs";
import { atomicWriteJson, readJsonSafe, sha256File } from "../guards/music-guards.mjs";
import { MusicDriver, MusicDriverError, classifyMusicError } from "./driver-interface.mjs";

function sleep(ms, signal = null) {
  if (ms <= 0) return Promise.resolve();
  return new Promise((resolve, reject) => {
    if (signal?.aborted) {
      reject(new MusicDriverError("Operation cancelled by caller.", { code: "cancelled" }));
      return;
    }
    const timer = setTimeout(() => {
      if (signal) signal.removeEventListener("abort", onAbort);
      resolve();
    }, ms);
    const onAbort = () => {
      clearTimeout(timer);
      reject(new MusicDriverError("Operation cancelled by caller.", { code: "cancelled" }));
    };
    if (signal) signal.addEventListener("abort", onAbort, { once: true });
  });
}

async function allocateFreePort() {
  return new Promise((resolve, reject) => {
    const server = net.createServer();
    server.unref();
    server.on("error", reject);
    server.listen(0, "127.0.0.1", () => {
      const addr = server.address();
      server.close(() => resolve(addr.port));
    });
  });
}

/**
 * Minimal CDP JSON-RPC client over Node.js 22 native WebSocket.
 */
export class CdpClient {
  constructor(wsUrl) {
    this.wsUrl = wsUrl;
    this.ws = null;
    this.nextId = 1;
    this.pending = new Map();
  }

  async connect(timeoutMs = 15_000) {
    return new Promise((resolve, reject) => {
      const ws = new WebSocket(this.wsUrl);
      this.ws = ws;
      const timer = setTimeout(() => {
        try {
          ws.close();
        } catch {
          // ignore
        }
        reject(new Error(`Timed out connecting to CDP endpoint ${this.wsUrl}`));
      }, timeoutMs);

      ws.addEventListener("open", () => {
        clearTimeout(timer);
        resolve();
      });
      ws.addEventListener("error", (ev) => {
        clearTimeout(timer);
        reject(new Error(`CDP WebSocket error: ${ev?.message || "connection failed"}`));
      });
      ws.addEventListener("message", (ev) => {
        try {
          const msg = JSON.parse(String(ev.data));
          if (msg.id && this.pending.has(msg.id)) {
            const { resolve: res, reject: rej } = this.pending.get(msg.id);
            this.pending.delete(msg.id);
            if (msg.error) {
              rej(new Error(msg.error.message || JSON.stringify(msg.error)));
            } else {
              res(msg.result);
            }
          }
        } catch {
          // ignore non-JSON frame
        }
      });
      ws.addEventListener("close", () => {
        for (const [, { reject: rej }] of this.pending) {
          rej(new Error("CDP connection closed before response arrived."));
        }
        this.pending.clear();
      });
    });
  }

  send(method, params = {}, timeoutMs = 120_000) {
    if (!this.ws || this.ws.readyState !== WebSocket.OPEN) {
      return Promise.reject(new Error("CDP WebSocket is not open."));
    }
    const id = this.nextId;
    this.nextId += 1;
    return new Promise((resolve, reject) => {
      const timer = setTimeout(() => {
        this.pending.delete(id);
        reject(new Error(`CDP call "${method}" timed out after ${timeoutMs}ms`));
      }, timeoutMs);
      this.pending.set(id, {
        resolve: (val) => {
          clearTimeout(timer);
          resolve(val);
        },
        reject: (err) => {
          clearTimeout(timer);
          reject(err);
        },
      });
      this.ws.send(JSON.stringify({ id, method, params }));
    });
  }

  async evaluate(expression, { timeoutMs = 120_000 } = {}) {
    const res = await this.send(
      "Runtime.evaluate",
      {
        expression,
        awaitPromise: true,
        returnByValue: true,
      },
      timeoutMs,
    );
    if (res?.exceptionDetails) {
      const msg =
        res.exceptionDetails.exception?.description ||
        res.exceptionDetails.text ||
        "JavaScript evaluation failed in Flow Music page";
      throw new Error(msg);
    }
    return res?.result?.value;
  }

  close() {
    try {
      this.ws?.close();
    } catch {
      // ignore
    }
  }
}

/**
 * Browser-side script probing Flow Music session & user identity without
 * exporting raw cookies or tokens.
 */
export function buildSessionProbeExpression() {
  return `(async () => {
    const candidates = [
      "/__api/user/me",
      "/__api/me",
      "/__api/auth/session",
      "/__api/session",
      "/__api/profile",
    ];
    let user = null;
    const tried = [];
    for (const url of candidates) {
      try {
        const res = await fetch(url, { credentials: "include" });
        tried.push({ url, status: res.status });
        if (res.ok) {
          const text = await res.text();
          try {
            const json = JSON.parse(text);
            const u = json?.user || json?.data?.user || json?.profile || json;
            if (u && (u.id || u.user_id || u.uid || u.email || u.username || u.handle)) {
              user = u;
              break;
            }
          } catch {}
        }
      } catch (e) {
        tried.push({ url, error: String(e?.message || e) });
      }
    }

    // Fallback: inspect Next.js / page bootstrap data for logged-in user id & handle
    if (!user) {
      try {
        const nextEl = document.querySelector("#__NEXT_DATA__");
        if (nextEl?.textContent) {
          const parsed = JSON.parse(nextEl.textContent);
          const props = parsed?.props?.pageProps || {};
          const u = props.user || props.session?.user || props.initialUser || null;
          if (u) user = u;
        }
      } catch {}
    }

    // Check DOM fallback for profile link (/u/<handle> or /user/<id>)
    let domHandle = null;
    try {
      const link = document.querySelector('a[href^="/u/"], a[href^="/profile/"], a[href^="/user/"]');
      if (link) {
        const m = link.getAttribute("href")?.match(/^\\/(?:u|profile|user)\\/([^/?#]+)/);
        if (m) domHandle = m[1];
      }
    } catch {}

    const signInBtn = Array.from(document.querySelectorAll("button, a")).find((el) =>
      /^(sign in|log in|登入)$/i.test((el.textContent || "").trim())
    );

    const userId = user?.id || user?.user_id || user?.uid || null;
    const account = user?.email || null;
    const handle = user?.username || user?.handle || user?.display_name || domHandle || null;
    const plan = user?.plan || user?.tier || user?.subscription_tier || user?.membership || null;
    const authenticated = Boolean(userId || account || (handle && !signInBtn));

    return {
      authenticated,
      url: location.href,
      userId,
      account,
      handle,
      plan,
      tried,
    };
  })()`;
}

/**
 * Browser-side script calling Flow Music's verified clips listing endpoint.
 */
export function buildListClipsExpression(userId, limit = 100) {
  return `(async () => {
    const uid = ${JSON.stringify(String(userId || ""))};
    const endpoints = uid
      ? ["/__api/clips/user/" + encodeURIComponent(uid) + "?public_only=false"]
      : ["/__api/clips/me?public_only=false", "/__api/clips?public_only=false"];
    let lastStatus = null;
    for (const url of endpoints) {
      const res = await fetch(url, { credentials: "include" });
      lastStatus = res.status;
      if (res.status === 401 || res.status === 403 || res.status === 429) {
        return { ok: false, status: res.status, error: "HTTP " + res.status + " from " + url };
      }
      if (res.ok) {
        const data = await res.json();
        const rawList = Array.isArray(data)
          ? data
          : Array.isArray(data?.clips)
            ? data.clips
            : Array.isArray(data?.items)
              ? data.items
              : Array.isArray(data?.data)
                ? data.data
                : [];
        return {
          ok: true,
          status: res.status,
          clips: rawList.slice(0, ${Math.max(1, Number(limit) || 100)}).map((c) => ({
            id: c.id || c.clip_id || c.uuid || null,
            title: c.title || c.name || "",
            status: c.status || c.state || "ready",
            duration: c.duration ?? c.seconds ?? c.duration_seconds ?? null,
            sound_prompt: c.sound_prompt || c.prompt || c.metadata?.sound_prompt || c.metadata?.prompt || "",
            created_at: c.created_at || c.createdAt || null,
            conversation_id: c.conversation_id || c.conversationId || null,
            is_public: c.is_public ?? null,
          })),
        };
      }
    }
    return { ok: false, status: lastStatus, error: "Unable to list Flow Music clips (HTTP " + lastStatus + ")" };
  })()`;
}

/**
 * Browser-side script downloading an audio clip via Flow Music's verified
 * `/__api/download/audio/<clipId>?format=<format>` endpoint and returning
 * Base64 bytes over CDP (no browser download prompt, no credential leak).
 */
export function buildDownloadClipExpression(clipId, format = DEFAULT_DOWNLOAD_FORMAT) {
  const cleanFmt = SUPPORTED_DOWNLOAD_FORMATS.includes(String(format).toLowerCase())
    ? String(format).toLowerCase()
    : DEFAULT_DOWNLOAD_FORMAT;
  return `(async () => {
    const url = "/__api/download/audio/" + encodeURIComponent(${JSON.stringify(String(clipId))}) + "?format=" + ${JSON.stringify(cleanFmt)};
    const res = await fetch(url, { credentials: "include" });
    if (!res.ok) {
      return { ok: false, status: res.status, error: "HTTP " + res.status + " downloading clip" };
    }
    const buf = new Uint8Array(await res.arrayBuffer());
    let binary = "";
    const chunkSize = 0x8000;
    for (let i = 0; i < buf.length; i += chunkSize) {
      binary += String.fromCharCode.apply(null, buf.subarray(i, i + chunkSize));
    }
    return {
      ok: true,
      status: res.status,
      contentType: res.headers.get("content-type") || "",
      byteLength: buf.length,
      base64: btoa(binary),
    };
  })()`;
}

/**
 * Browser-side script submitting a track prompt in Flow Music's composer UI.
 * Fails fast with `selector_drift` if the composer input or submit button
 * cannot be located cleanly.
 */
export function buildSubmitPromptExpression({ prompt, title = null, instrumental = true }) {
  const composedPrompt = title
    ? `Create a track titled "${title}". ${prompt}${instrumental ? " (Instrumental only, no vocals.)" : ""}`
    : `${prompt}${instrumental ? " (Instrumental only, no vocals.)" : ""}`;

  return `(async () => {
    const selectors = [
      'textarea[placeholder*="Describe" i]',
      'textarea[placeholder*="music" i]',
      'textarea[placeholder*="prompt" i]',
      'textarea[placeholder*="song" i]',
      'textarea[data-testid*="prompt" i]',
      'div[contenteditable="true"][role="textbox"]',
      'textarea',
    ];
    let input = null;
    for (const sel of selectors) {
      const candidates = Array.from(document.querySelectorAll(sel)).filter((el) => {
        const rect = el.getBoundingClientRect();
        return rect.width > 80 && rect.height > 20 && !el.disabled;
      });
      if (candidates.length > 0) {
        input = candidates[0];
        break;
      }
    }
    if (!input) {
      return { ok: false, code: "selector_drift", error: "Flow Music composer input not found on page." };
    }

    input.focus();
    const text = ${JSON.stringify(composedPrompt)};
    if (input.tagName === "TEXTAREA" || input.tagName === "INPUT") {
      const proto = Object.getOwnPropertyDescriptor(Object.getPrototypeOf(input), "value");
      if (proto?.set) proto.set.call(input, text);
      else input.value = text;
      input.dispatchEvent(new Event("input", { bubbles: true }));
      input.dispatchEvent(new Event("change", { bubbles: true }));
    } else {
      input.textContent = text;
      input.dispatchEvent(new InputEvent("input", { bubbles: true, data: text }));
    }

    await new Promise((r) => setTimeout(r, 250));

    const submitCandidates = Array.from(document.querySelectorAll('button[type="submit"], button[aria-label*="send" i], button[aria-label*="create" i], button[aria-label*="generate" i], button'))
      .filter((btn) => {
        if (btn.disabled) return false;
        const label = ((btn.getAttribute("aria-label") || "") + " " + (btn.textContent || "")).trim().toLowerCase();
        return /(send|create|generate|submit|make|go)/.test(label) || btn.type === "submit";
      });

    if (submitCandidates.length > 0) {
      submitCandidates[submitCandidates.length - 1].click();
      return { ok: true, method: "button_click", promptSent: text };
    }

    // Fallback: Enter key submission inside composer
    input.dispatchEvent(new KeyboardEvent("keydown", { key: "Enter", code: "Enter", bubbles: true }));
    return { ok: true, method: "enter_key", promptSent: text };
  })()`;
}

export class ChromeCdpMusicDriver extends MusicDriver {
  constructor({
    chromeBin = null,
    profile = null,
    runtimeHome = null,
    env = process.env,
    platform = process.platform,
    headless = false,
  } = {}) {
    super({ name: "chrome-cdp" });
    this.env = env;
    this.platform = platform;
    this.runtimeHome = runtimeHome || resolveRuntimeHome({ env, platform });
    this.profile = profile || env.MOKAAIR_FLOW_MUSIC_PROFILE || "default";
    this.chromeBin = chromeBin || resolveChromeBinary({ env, platform });
    this.headless = Boolean(headless);
  }

  profileMetaPath(profile = null) {
    return path.join(resolveChromeProfileDir(this.runtimeHome, profile || this.profile), ".mokaair_profile.json");
  }

  readProfileMeta(profile = null) {
    return readJsonSafe(this.profileMetaPath(profile), {});
  }

  writeProfileMeta(profile, patch) {
    const prev = this.readProfileMeta(profile);
    atomicWriteJson(this.profileMetaPath(profile), {
      ...prev,
      ...patch,
      profile: sanitizeProfileName(profile || this.profile),
      updatedAt: new Date().toISOString(),
    });
  }

  getLoginCommand({ profile = null } = {}) {
    const bin = this.chromeBin || resolveChromeBinary({ env: this.env, platform: this.platform });
    if (!bin) {
      throw classifyMusicError({ code: "chrome_not_found" });
    }
    const targetProfile = sanitizeProfileName(profile || this.profile);
    const userDataDir = resolveChromeProfileDir(this.runtimeHome, targetProfile);
    fs.mkdirSync(userDataDir, { recursive: true });
    const args = [
      `--user-data-dir=${userDataDir}`,
      "--no-first-run",
      "--no-default-browser-check",
      FLOW_MUSIC_ORIGIN,
    ];
    return { binary: bin, args, profile: targetProfile, userDataDir };
  }

  /**
   * Launches an isolated Chrome session on an ephemeral loopback CDP port,
   * runs `fn(cdp)`, and shuts the session down cleanly.
   */
  async withPageSession({ profile = null, headless = this.headless, navigateUrl = FLOW_MUSIC_ORIGIN, signal = null }, fn) {
    const bin = this.chromeBin || resolveChromeBinary({ env: this.env, platform: this.platform });
    if (!bin) {
      throw classifyMusicError({ code: "chrome_not_found" });
    }
    const targetProfile = sanitizeProfileName(profile || this.profile);
    const userDataDir = resolveChromeProfileDir(this.runtimeHome, targetProfile);
    fs.mkdirSync(userDataDir, { recursive: true });

    const port = await allocateFreePort();
    const args = [
      `--remote-debugging-port=${port}`,
      `--user-data-dir=${userDataDir}`,
      "--no-first-run",
      "--no-default-browser-check",
      "--disable-background-timer-throttling",
      "--disable-backgrounding-occluded-windows",
      "--disable-renderer-backgrounding",
      ...(headless ? ["--headless=new"] : ["--window-size=1280,900"]),
      navigateUrl,
    ];

    const proc = spawn(bin, args, {
      stdio: ["ignore", "ignore", "pipe"],
      windowsHide: headless,
    });

    let stderr = "";
    proc.stderr?.on("data", (d) => {
      stderr += d.toString("utf8");
    });

    const killProc = () => {
      try {
        proc.kill("SIGTERM");
      } catch {
        // ignore
      }
    };

    const onAbort = () => killProc();
    if (signal) signal.addEventListener("abort", onAbort, { once: true });

    try {
      // Wait for Chrome CDP endpoint
      const deadline = Date.now() + 25_000;
      let target = null;
      while (Date.now() < deadline) {
        if (signal?.aborted) {
          throw new MusicDriverError("Cancelled while waiting for Chrome CDP.", { code: "cancelled" });
        }
        try {
          const listRes = await fetch(`http://127.0.0.1:${port}/json/list`);
          if (listRes.ok) {
            const targets = await listRes.json();
            target =
              targets.find((t) => t.type === "page" && String(t.url || "").includes("flowmusic.app")) ||
              targets.find((t) => t.type === "page" && t.webSocketDebuggerUrl);
            if (target?.webSocketDebuggerUrl) break;
          }
        } catch {
          // Chrome still starting
        }
        await sleep(300, signal);
      }

      if (!target?.webSocketDebuggerUrl) {
        throw new MusicDriverError(
          `Chrome CDP did not become ready on port ${port}. Ensure no other Chrome window is currently using profile "${targetProfile}". ${stderr.slice(0, 200)}`,
          { code: "cdp_startup_failed", retryable: false, nextAction: "close_profile_chrome" },
        );
      }

      const cdp = new CdpClient(target.webSocketDebuggerUrl);
      await cdp.connect();
      try {
        await cdp.send("Page.enable");
        await cdp.send("Runtime.enable");
        if (!String(target.url || "").startsWith(FLOW_MUSIC_ORIGIN)) {
          await cdp.send("Page.navigate", { url: navigateUrl });
        }
        // Wait for document readyState === complete
        for (let i = 0; i < 40; i += 1) {
          const ready = await cdp.evaluate("document.readyState");
          if (ready === "complete") break;
          await sleep(250, signal);
        }
        await sleep(800, signal);
        return await fn(cdp, { profile: targetProfile });
      } finally {
        cdp.close();
      }
    } finally {
      if (signal) signal.removeEventListener("abort", onAbort);
      killProc();
    }
  }

  async listProfiles() {
    const root = resolveChromeProfilesRoot(this.runtimeHome);
    if (!fs.existsSync(root)) return [];
    const entries = fs
      .readdirSync(root, { withFileTypes: true })
      .filter((d) => d.isDirectory() && d.name.startsWith("profile_"));

    return entries.map((entry) => {
      const name = entry.name.slice("profile_".length);
      const dir = path.join(root, entry.name);
      const meta = readJsonSafe(path.join(dir, ".mokaair_profile.json"), {});
      const cookiesPath = path.join(dir, "Default", "Network", "Cookies");
      const altCookiesPath = path.join(dir, "Default", "Cookies");
      const cookiesPresent = fs.existsSync(cookiesPath) || fs.existsSync(altCookiesPath);
      return {
        profile: name,
        isDefault: name === sanitizeProfileName(this.profile),
        profileDir: dir,
        cookiesPresent,
        userId: meta.userId || null,
        account: meta.account || null,
        handle: meta.handle || null,
        plan: meta.plan || null,
        lastVerifiedAt: meta.lastVerifiedAt || null,
      };
    });
  }

  async checkAuth({ profile = null, signal = null } = {}) {
    const targetProfile = sanitizeProfileName(profile || this.profile);
    return this.withPageSession({ profile: targetProfile, headless: true, signal }, async (cdp) => {
      const probe = await cdp.evaluate(buildSessionProbeExpression(), { timeoutMs: 30_000 });
      if (probe?.authenticated) {
        this.writeProfileMeta(targetProfile, {
          userId: probe.userId,
          account: probe.account,
          handle: probe.handle,
          plan: probe.plan,
          lastVerifiedAt: new Date().toISOString(),
        });
      }
      return {
        authenticated: Boolean(probe?.authenticated),
        profile: targetProfile,
        userId: probe?.userId || null,
        account: probe?.account || null,
        handle: probe?.handle || null,
        plan: probe?.plan || null,
        url: probe?.url || FLOW_MUSIC_ORIGIN,
      };
    });
  }

  async listRemoteClips({ profile = null, userId = null, limit = 100, signal = null } = {}) {
    const targetProfile = sanitizeProfileName(profile || this.profile);
    return this.withPageSession({ profile: targetProfile, headless: true, signal }, async (cdp) => {
      let resolvedUserId = userId || this.readProfileMeta(targetProfile).userId || null;
      if (!resolvedUserId) {
        const probe = await cdp.evaluate(buildSessionProbeExpression(), { timeoutMs: 30_000 });
        if (!probe?.authenticated) {
          throw classifyMusicError({ code: "auth_expired", statusCode: 401 });
        }
        resolvedUserId = probe.userId;
        this.writeProfileMeta(targetProfile, {
          userId: probe.userId,
          account: probe.account,
          handle: probe.handle,
          plan: probe.plan,
          lastVerifiedAt: new Date().toISOString(),
        });
      }
      const res = await cdp.evaluate(buildListClipsExpression(resolvedUserId, limit), { timeoutMs: 45_000 });
      if (!res?.ok) {
        throw classifyMusicError({ statusCode: res?.status, message: res?.error });
      }
      return {
        profile: targetProfile,
        userId: resolvedUserId,
        clips: res.clips || [],
      };
    });
  }

  async downloadClip({ clipId, format = DEFAULT_DOWNLOAD_FORMAT, outFile, profile = null, signal = null }) {
    const targetProfile = sanitizeProfileName(profile || this.profile);
    const cleanFormat = SUPPORTED_DOWNLOAD_FORMATS.includes(String(format).toLowerCase())
      ? String(format).toLowerCase()
      : DEFAULT_DOWNLOAD_FORMAT;

    return this.withPageSession({ profile: targetProfile, headless: true, signal }, async (cdp) => {
      const res = await cdp.evaluate(buildDownloadClipExpression(clipId, cleanFormat), {
        timeoutMs: cleanFormat === "wav" ? 4 * 60 * 1000 : 90_000,
      });
      if (!res?.ok || !res?.base64) {
        throw classifyMusicError({ statusCode: res?.status, message: res?.error });
      }
      fs.mkdirSync(path.dirname(outFile), { recursive: true });
      const tmp = `${outFile}.${process.pid}.tmp`;
      fs.writeFileSync(tmp, Buffer.from(res.base64, "base64"));
      fs.renameSync(tmp, outFile);
      return {
        clipId,
        format: cleanFormat,
        outFile,
        byteLength: res.byteLength,
        sha256: sha256File(outFile),
      };
    });
  }

  async generateTrack({
    prompt,
    title = null,
    instrumental = true,
    model = DEFAULT_MUSIC_MODEL,
    profile = null,
    pollTimeoutMs = 4 * 60 * 1000,
    signal = null,
  }) {
    const targetProfile = sanitizeProfileName(profile || this.profile);
    // Keep window visible for generation to prevent Chrome background-tab freezing
    return this.withPageSession({ profile: targetProfile, headless: false, signal }, async (cdp) => {
      const probe = await cdp.evaluate(buildSessionProbeExpression(), { timeoutMs: 30_000 });
      if (!probe?.authenticated) {
        throw classifyMusicError({ code: "auth_expired", statusCode: 401 });
      }

      const beforeList = await cdp.evaluate(buildListClipsExpression(probe.userId, 50), { timeoutMs: 30_000 });
      const beforeIds = new Set((beforeList?.clips || []).map((c) => c.id).filter(Boolean));

      const submitRes = await cdp.evaluate(buildSubmitPromptExpression({ prompt, title, instrumental }), {
        timeoutMs: 30_000,
      });
      if (!submitRes?.ok) {
        throw classifyMusicError({ code: submitRes?.code || "selector_drift", message: submitRes?.error });
      }

      const deadline = Date.now() + pollTimeoutMs;
      while (Date.now() < deadline) {
        await sleep(5000, signal);
        const nowList = await cdp.evaluate(buildListClipsExpression(probe.userId, 50), { timeoutMs: 30_000 });
        if (!nowList?.ok) {
          throw classifyMusicError({ statusCode: nowList?.status, message: nowList?.error });
        }
        const newClips = (nowList.clips || []).filter((c) => c.id && !beforeIds.has(c.id));
        const readyClips = newClips.filter((c) => {
          const st = String(c.status || "").toLowerCase();
          return (Number(c.duration) > 0 || st === "ready" || st === "complete" || st === "completed" || st === "succeeded") && st !== "pending" && st !== "generating";
        });
        if (readyClips.length > 0) {
          return {
            ok: true,
            model,
            profile: targetProfile,
            userId: probe.userId,
            clips: readyClips,
          };
        }
      }

      throw new MusicDriverError(
        `Timed out waiting ${Math.round(pollTimeoutMs / 1000)}s for Flow Music track "${title || "untitled"}" to finish. Run music_list_remote to check if it completed in the background.`,
        { code: "generation_timeout", retryable: false, nextAction: "list_remote" },
      );
    });
  }
}
