// Calls to the automation endpoints (apps/web/app/api/video/automation → apps/api/app/video_automation):
// the owner's settings, one writing stage run with the model the settings name, and topic
// candidates. The same token as tts and review-push; on the host the worker sets MOKAAIR_SITE to
// the web container, so these never leave the compose network.
import { readCredentials } from "../tts/credentials.mjs";
import { USER_AGENT } from "../tts/client.mjs";

export class AutomationError extends Error {
  constructor(message, { status = 0, code = "", who = "service" } = {}) {
    super(message);
    this.status = status;
    this.code = code;
    // "owner": needs the site owner (token, keys, a budget they set); "service": try again later.
    this.who = who;
  }
}

const OWNER_CODES = new Set([
  "video_tool_token_invalid",
  "video_ai_provider_not_configured",
  "video_ai_budget_exhausted",
  "video_automation_settings_invalid",
]);
const RETRYABLE_CODES = new Set(["video_ai_upstream_busy", "video_ai_upstream_unreachable", "rate_limit_exceeded", "upstream_unavailable"]);
// Every subscription account is at the owner's cap: nothing ran, and retrying within minutes will
// not help. This run of `auto` ends; the worker's loop tries again on its next round.
const PAUSE_CODES = new Set(["video_ai_subscription_paused"]);

async function problemOf(response) {
  try {
    const body = await response.json();
    return { code: body.code ?? "", detail: body.detail ?? body.title ?? "" };
  } catch {
    return { code: "", detail: "" };
  }
}

function delayMs(response, attempt) {
  const header = Number(response?.headers.get("retry-after"));
  if (Number.isFinite(header) && header > 0) return Math.min(header, 120) * 1000;
  return Math.min(2 ** attempt * 5, 120) * 1000;
}

/** A client bound to the stored site and token; `attempts` covers busy vendors and restarts. */
export function automationClient(ctx, { attempts = 4 } = {}) {
  const { site, token } = readCredentials({ env: ctx.env, home: ctx.home });
  if (!token) throw new AutomationError("no video tool token yet: run `node tools/video/cli.mjs login`", { who: "owner" });
  const fetchImpl = ctx.fetch ?? globalThis.fetch;
  const sleep = ctx.sleep ?? ((ms) => new Promise((resolve) => setTimeout(resolve, ms)));
  async function request(method, route, json) {
    let last;
    for (let attempt = 0; attempt < attempts; attempt++) {
      let response;
      try {
        response = await fetchImpl(`${site}/api/video/${route}`, {
          method,
          headers: {
            Authorization: `Bearer ${token}`,
            "User-Agent": USER_AGENT,
            "Accept-Language": "zh-TW",
            ...(json ? { "Content-Type": "application/json" } : {}),
          },
          body: json ? JSON.stringify(json) : undefined,
        });
      } catch (error) {
        last = new AutomationError(`cannot reach ${site}: ${error.message}`, { code: "network" });
        await sleep(delayMs(null, attempt));
        continue;
      }
      if (response.ok) return response.json();
      const problem = await problemOf(response);
      const message = problem.detail || `HTTP ${response.status}`;
      if (response.status === 401 || OWNER_CODES.has(problem.code)) throw new AutomationError(message, { status: response.status, code: problem.code, who: "owner" });
      if (PAUSE_CODES.has(problem.code)) throw new AutomationError(message, { status: response.status, code: problem.code });
      last = new AutomationError(message, { status: response.status, code: problem.code });
      if (!(RETRYABLE_CODES.has(problem.code) || response.status === 429 || response.status >= 500)) throw last;
      await sleep(delayMs(response, attempt));
    }
    throw last;
  }
  return {
    settings: () => request("GET", "automation/settings"),
    topics: () => request("GET", "automation/topics"),
    /** Every video on /admin/videos, dropped ones too: slug, title, source_guide, dropped_at. */
    videos: () => request("GET", "automation/videos"),
    /** One stage: the server answers with the model the owner chose; returns { text, usage, … }. */
    run: (stage, slug, instructions, payload, maxOutputTokens = 16_000) =>
      request("POST", "automation/run", { stage, slug, instructions, payload, max_output_tokens: maxOutputTokens }),
    /** Report the video's title, stage and checklist to /admin/videos. */
    report: (slug, project) => request("PUT", `reviews/${slug}`, project),
    /** Submit one review; the same content twice returns the review that exists. */
    submit: (slug, review) => request("POST", `reviews/${slug}/reviews`, review),
    /** The video's reviews as the owner left them, newest first. */
    reviews: async (slug) => {
      try {
        return await request("GET", `reviews/${slug}`);
      } catch (error) {
        if (error.status === 404) return null;
        throw error;
      }
    },
    // The owner's drama requests (docs/videos/DRAMA.md): filed on /admin/videos, made before any scheduled draft.
    /** The oldest request nobody has started, or null. */
    dramaNext: async () => (await request("GET", "automation/drama-requests/next")).request ?? null,
    /** Claim a request for the video about to be made under `slug`. */
    dramaStart: (id, slug) => request("POST", `automation/drama-requests/${id}/start`, { slug }),
    /** Report a request's video finished and confirmed for upload. */
    dramaDone: (id) => request("POST", `automation/drama-requests/${id}/done`),
  };
}
