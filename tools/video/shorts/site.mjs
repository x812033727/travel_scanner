// The calls the Shorts tool makes to the site (apps/web/app/api/video → apps/api): the Shorts
// settings, the videos the site knows, a video's reviews and files, Jev's policy reading, and the
// worker's knock. The same video tool token as narration and review-push, and nothing of the
// owner's session; on the host MOKAAIR_SITE points at the web container.
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

export function siteClient({ env = process.env, home, fetch: fetchImpl = globalThis.fetch, sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms)), attempts = 4 } = {}) {
  const { site, token } = readCredentials({ env, home });
  if (!token) throw new SiteError('no video tool token yet: run `node tools/video/cli.mjs login`', { who: 'owner' });
  async function request(method, route, { json, bytes, query } = {}) {
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
        last = new SiteError(`cannot reach ${site}: ${error.message}`, { code: 'network' });
        await sleep(2 ** attempt * 1000);
        continue;
      }
      if (response.ok) return response.json();
      const problem = await response.json().catch(() => ({}));
      const who = response.status === 401 || OWNER_CODES.has(problem.code) ? 'owner' : 'service';
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
    judgePolicy: (body) => request('POST', 'automation/judge/policy', { json: body }),
  };
}
