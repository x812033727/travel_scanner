// Pairing: how `login` gets a video tool token without anyone copying one
// (apps/api/app/video_speech/pairing.py, through apps/web/app/api/video/pairings).
//
// The tool opens a pairing and prints a short code and a link to the admin card; the owner
// compares the code and allows it there; the tool, polling with a device code only it holds,
// collects the token. The token goes straight into the credentials file and is never printed,
// so it cannot end up in a terminal's scrollback or in a chat with an assistant.
import os from "node:os";

import { SpeechError, USER_AGENT } from "./client.mjs";

const CLIENT_NAME_MAX = 60;

/** Shown on the admin card so the owner can tell their own machine's request apart. */
export function defaultClientName() {
  return `影片工具 @ ${os.hostname()}`.slice(0, CLIENT_NAME_MAX);
}

async function post(site, path, body, fetchImpl) {
  return fetchImpl(`${site}/api/video/${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json", "User-Agent": USER_AGENT, "Accept-Language": "zh-TW" },
    body: JSON.stringify(body),
  });
}

async function detail(response) {
  try {
    const body = await response.json();
    return body.detail || body.title || `HTTP ${response.status}`;
  } catch {
    return `HTTP ${response.status}`;
  }
}

/** Open a pairing; resolves to { device_code, user_code, verification_path, expires_in, interval }. */
export async function startPairing({ site, clientName, fetchImpl = globalThis.fetch }) {
  let response;
  try {
    response = await post(site, "pairings", { client_name: clientName.slice(0, CLIENT_NAME_MAX) }, fetchImpl);
  } catch (error) {
    throw new SpeechError(`cannot reach ${site}: ${error.message}`, { code: "network" });
  }
  if (response.status === 404) {
    throw new SpeechError(`${site} does not offer pairing yet (deploy the server first), or use login --paste`, { status: 404, code: "video_pairing_unavailable" });
  }
  if (!response.ok) throw new SpeechError(await detail(response), { status: response.status });
  return response.json();
}

/**
 * Poll until the owner answers or the code expires. Resolves to { token, token_name }; rejects with
 * a SpeechError for the owner when the pairing was denied or ran out of time.
 */
export async function waitForPairing({ site, started, fetchImpl = globalThis.fetch, sleep, now = () => new Date() }) {
  const deadline = now().getTime() + started.expires_in * 1000;
  let interval = Math.max(1, started.interval) * 1000;
  while (now().getTime() < deadline) {
    await sleep(interval);
    let response;
    try {
      response = await post(site, "pairings/poll", { device_code: started.device_code }, fetchImpl);
    } catch {
      continue; // A dropped connection is not an answer; try again until the code expires.
    }
    if (response.status === 429) {
      const retry = Number(response.headers.get("retry-after"));
      interval = Math.min(Number.isFinite(retry) && retry > 0 ? retry * 1000 : interval * 2, 30_000);
      continue;
    }
    if (!response.ok) {
      if (response.status >= 500) continue;
      throw new SpeechError(await detail(response), { status: response.status });
    }
    const body = await response.json();
    if (body.status === "approved" && body.token) return { token: body.token, token_name: body.token_name ?? "" };
    if (body.status === "denied") throw new SpeechError("the pairing was denied on the admin card", { code: "video_pairing_denied", who: "owner" });
    if (body.status === "expired") break;
  }
  throw new SpeechError("the code expired before anyone allowed it; run login again", { code: "video_pairing_expired", who: "owner" });
}
