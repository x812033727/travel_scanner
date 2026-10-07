// The calls the Shorts tool makes to the site (apps/web/app/api/video → apps/api): the Shorts
// settings, the videos the site knows, a video's reviews and files, Jev's policy reading, and the
// worker's knock. The same video tool token as narration and review-push, and nothing of the
// owner's session; on the host MOKAAIR_SITE points at the web container.
import { RUN_UNCERTAIN } from '../automation/client.mjs';
import { STORY_VOICE_STYLE } from '../automation/register.mjs';
import { readCredentials } from '../tts/credentials.mjs';
import { USER_AGENT } from '../tts/client.mjs';
import { PROFILE } from './core.mjs';

export class SiteError extends Error {
  constructor(message, { status = 0, code = '', who = 'service' } = {}) {
    super(message);
    this.status = status;
    this.code = code;
    // "owner": needs the site owner (the token, a setting); "service": try again later.
    this.who = who;
  }
}

// The channel voice the owner chose on 2026-09-24 (docs/videos/README.md) in the storytelling
// register of 2026-09-29 (docs/videos/ILLUSTRATED.md §說書式旁白), for a site that has neither
// Shorts settings nor automation settings to read yet.
export const CHANNEL_VOICE = Object.freeze({
  provider: 'gemini',
  name: 'Sulafat',
  style: STORY_VOICE_STYLE,
});
export const DEFAULT_SETTINGS = Object.freeze({ voice: CHANNEL_VOICE, seconds_min: PROFILE.minSeconds, seconds_max: PROFILE.maxSeconds, locales: [], made_for_kids: false });

const OWNER_CODES = new Set(['video_tool_token_invalid']);
// Jev's policy reading takes one call off the daily Jev budget before Jev is asked
// (apps/api/app/video_automation/judge.py `_ask`), so it is `paid`, as in
// tools/video/automation/client.mjs: once sent, it is asked again only after a 429, the API's own
// 502 once its Jev call failed (no verdict was lost on the way back), or the judge route's 502
// `upstream_unavailable`, which now means only an API the route never reached: a request the API
// took and whose answer was lost is the route's 504 `video_judge_answer_lost` (JUDGE_LOST in
// apps/web/app/api/video/speech/forward.ts). That 504, a dropped connection, an unreadable answer
// and any other 5xx (a gateway's page, a 502 with another code such as the API's
// `video_judge_outcome_uncertain`) leave its outcome unknown: RUN_UNCERTAIN, the automation
// client's code, which the QA's policy item reports instead of asking Jev again. A host from before
// that route change answers the 502 for both, so this client needs a host that serves it:
// production does since a9e4c3851, deployed 2026-10-05.
const SETTLED_JUDGE_CODES = new Set(['video_judge_upstream_failed', 'upstream_unavailable']);
// Connection errors that mean the request never reached a server, so nothing it asks has started.
const NEVER_SENT = new Set(['ECONNREFUSED', 'ENOTFOUND', 'EAI_AGAIN', 'EHOSTUNREACH', 'ENETUNREACH', 'UND_ERR_CONNECT_TIMEOUT']);
const neverSent = (error) => NEVER_SENT.has(error?.cause?.code ?? error?.code);

export function siteClient({ env = process.env, home, fetch: fetchImpl = globalThis.fetch, sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms)), attempts = 4 } = {}) {
  const { site, token } = readCredentials({ env, home });
  if (!token) throw new SiteError('no video tool token yet: run `node tools/video/cli.mjs login`', { who: 'owner' });
  const uncertain = (route, why, status = 0) =>
    new SiteError(`${route} was sent and no answer came back (${why}); Jev may have judged it, so the outcome is unknown and it is not sent again`, { status, code: RUN_UNCERTAIN });
  async function request(method, route, { json, bytes, query, paid = false } = {}) {
    const url = `${site}/api/video/${route}${query ? `?${new URLSearchParams(query)}` : ''}`;
    let last;
    for (let attempt = 0; attempt < attempts; attempt++) {
      let response;
      try {
        response = await fetchImpl(url, {
          method,
          headers: {
            Authorization: `Bearer ${token}`,
            'User-Agent': USER_AGENT,
            Accept: 'application/json',
            'Accept-Language': 'zh-TW',
            ...(json ? { 'Content-Type': 'application/json' } : bytes ? { 'Content-Type': 'application/octet-stream' } : {}),
          },
          body: json ? JSON.stringify(json) : bytes,
        });
      } catch (error) {
        if (paid && !neverSent(error)) throw uncertain(route, error.cause?.message ?? error.message);
        last = new SiteError(`cannot reach ${site}: ${error.message}`, { code: 'network' });
        await sleep(2 ** attempt * 1000);
        continue;
      }
      if (response.ok) {
        if (!paid) return response.json();
        try {
          return await response.json();
        } catch (error) {
          throw uncertain(route, `the answer could not be read: ${error.message}`, response.status);
        }
      }
      const problem = await response.json().catch(() => ({}));
      const who = response.status === 401 || OWNER_CODES.has(problem.code) ? 'owner' : 'service';
      if (paid && response.status >= 500 && !SETTLED_JUDGE_CODES.has(problem.code)) {
        throw uncertain(route, `HTTP ${response.status}${problem.detail ? `: ${problem.detail}` : ''}`, response.status);
      }
      last = new SiteError(problem.detail || `HTTP ${response.status}`, { status: response.status, code: problem.code ?? '', who });
      if (!(response.status === 429 || response.status >= 500)) throw last;
      await sleep(Math.min(Number(response.headers.get('retry-after')) || 2 ** attempt, 30) * 1000);
    }
    throw last;
  }
  const orNull = async (call) => {
    try {
      return await call();
    } catch (error) {
      if (error instanceof SiteError && error.status === 404) return null;
      throw error;
    }
  };
  return {
    site,
    token,
    // The narration calls (tools/video/tts/client.mjs) take the same fetch and sleep.
    fetch: fetchImpl,
    sleep,
    request,
    /**
     * What a Short is made with: the Shorts settings, or on a site from before them the
     * channel's own voice, or the defaults; the length a Short may have comes with it.
     */
    settings: async () => {
      const own = await orNull(() => request('GET', 'automation/shorts/settings'));
      if (own) return own;
      const channel = await orNull(() => request('GET', 'automation/settings'));
      return { ...DEFAULT_SETTINGS, ...(channel?.voice ? { voice: channel.voice } : {}) };
    },
    /** The worker's knock; null on a site that has no such route yet. */
    tick: () => orNull(() => request('POST', 'automation/shorts/tick')),
    videos: (query) => request('GET', 'automation/videos', { query }),
    project: (slug) => orNull(() => request('GET', `reviews/${slug}`)),
    report: (slug, body) => request('PUT', `reviews/${slug}`, { json: body }),
    part: (slug, sha, bytes, query) => request('PUT', `reviews/${slug}/files/${sha}`, { bytes, query }),
    submit: (slug, review) => request('POST', `reviews/${slug}/reviews`, { json: review }),
    /** Jev's policy reading; an answer lost on the way throws RUN_UNCERTAIN instead of asking Jev again. */
    judgePolicy: (body) => request('POST', 'automation/judge/policy', { json: body, paid: true }),
  };
}
