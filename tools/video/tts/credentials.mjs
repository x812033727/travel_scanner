// Where the video tool token lives on this computer: a file in the user's home directory, never in
// the repository and never an environment variable the owner has to set. The token itself is made
// on the admin card 「Azure 語音（影片旁白）」 and can only synthesize narration.
import { chmodSync, existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import os from "node:os";
import path from "node:path";

export const DEFAULT_SITE = "https://mokaair.com";
export const TOKEN_PATTERN = /^mkv_[A-Za-z0-9_-]{36,76}$/;

export const credentialsFile = (home = os.homedir()) => path.join(home, ".mokaair", "video-tool.json");

export function validSite(site) {
  try {
    const url = new URL(site);
    const local = ["localhost", "127.0.0.1"].includes(url.hostname);
    return (url.protocol === "https:" || (local && url.protocol === "http:")) && !url.username && !url.password && url.pathname === "/";
  } catch {
    return false;
  }
}

/** The stored site and token; MOKAAIR_SITE / MOKAAIR_VIDEO_TOKEN override them, e.g. in CI. */
export function readCredentials({ env = process.env, home } = {}) {
  const file = credentialsFile(home);
  const stored = existsSync(file) ? JSON.parse(readFileSync(file, "utf8")) : {};
  const site = (env.MOKAAIR_SITE || stored.site || DEFAULT_SITE).replace(/\/+$/, "");
  const token = env.MOKAAIR_VIDEO_TOKEN || stored.token || null;
  return { site, token, file };
}

export function writeCredentials({ site, token }, { home } = {}) {
  if (!TOKEN_PATTERN.test(token)) throw new Error("that does not look like a video tool token (it starts with mkv_)");
  if (!validSite(`${site}/`)) throw new Error(`${site} is not an https site address`);
  const file = credentialsFile(home);
  mkdirSync(path.dirname(file), { recursive: true });
  writeFileSync(file, `${JSON.stringify({ site, token, saved_at: new Date().toISOString() }, null, 2)}\n`, { mode: 0o600 });
  try {
    chmodSync(file, 0o600);
  } catch {
    // Windows keeps the file private to the user profile; chmod is best effort there.
  }
  return file;
}
