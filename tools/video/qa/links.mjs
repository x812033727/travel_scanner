// The links check: every URL in the description opens.
//
// A GET that follows redirects, as a viewer's browser would; anything but a 2xx answer, a
// timeout or a refused connection is listed. The requests carry the editorial User-Agent the
// fact-checkers use (never a person's name or e-mail), leave a second between two requests to
// the same host, and give up after 15 s. The URLs come from the composed descriptions only,
// so no personal data can ride in a query string.
import { EDITORIAL_USER_AGENT } from "../automation/fetch.mjs";

export const USER_AGENT = EDITORIAL_USER_AGENT;
export const HOST_GAP_MS = 1000;
export const TIMEOUT_MS = 15_000;
// Answers that say the page is there but will not serve a program: a login wall, a bot block, a
// rate limit. The Verge answers every editorial request 403; on 2026-10-31 that alone failed the
// links item of daily-ai-20261028 (two of 29 links), so a brief citing it never passed QA on its
// own. Such a link passes, named in the detail; a 404, a 5xx or no answer still fails.
export const REFUSED_STATUSES = new Set([401, 403, 429]);

/** Every http(s) URL in some texts, once each, in order of first appearance. */
export function descriptionUrls(texts) {
  const seen = new Set();
  for (const text of texts) {
    for (const match of String(text ?? "").matchAll(/https?:\/\/[^\s｜|<>"'）\]，。、；：！？「」]+/g)) {
      seen.add(trimUrl(match[0]));
    }
  }
  return [...seen];
}

/**
 * A URL without the sentence punctuation after it. A closing parenthesis belongs to the URL only
 * while it closes one the URL opened, as in Wikimedia's `File:Plane_Ticket_(28379315406).jpg`;
 * otherwise it closes the Markdown link or the aside around it.
 */
function trimUrl(url) {
  let trimmed = url;
  for (;;) {
    const before = trimmed;
    trimmed = trimmed.replace(/[.,;:。，、]+$/, "");
    if (trimmed.endsWith(")") && trimmed.split(")").length > trimmed.split("(").length) trimmed = trimmed.slice(0, -1);
    if (trimmed === before) return trimmed;
  }
}

/**
 * A checker that keeps the per-host gap across calls; `fetchImpl`, `sleep` and `now` (ms) are
 * injectable so the tests never touch the network. `check(url)` resolves to
 * { url, ok, status, final_url?, error? } and never rejects.
 */
export function linkChecker({ fetchImpl = globalThis.fetch, sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms)), now = () => Date.now(), timeoutMs = TIMEOUT_MS, gapMs = HOST_GAP_MS } = {}) {
  const lastByHost = new Map();
  return async function check(url) {
    let parsed;
    try {
      parsed = new URL(url);
    } catch {
      return { url, ok: false, status: 0, error: "not a URL" };
    }
    const wait = (lastByHost.get(parsed.host) ?? Number.NEGATIVE_INFINITY) + gapMs - now();
    if (wait > 0) await sleep(wait);
    lastByHost.set(parsed.host, now());
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), timeoutMs);
    try {
      const response = await fetchImpl(parsed.href, {
        method: "GET",
        redirect: "follow",
        headers: { "User-Agent": USER_AGENT, Accept: "text/html,application/xhtml+xml,application/pdf;q=0.9,*/*;q=0.5", "Accept-Language": "zh-TW,en;q=0.8" },
        signal: controller.signal,
      });
      // The status is the answer; the page itself is not needed.
      await response.body?.cancel?.().catch(() => {});
      const result = { url, ok: response.ok, status: response.status, final_url: response.url || url };
      if (REFUSED_STATUSES.has(response.status)) return { ...result, ok: true, refused: true };
      return response.ok ? result : { ...result, error: `HTTP ${response.status}` };
    } catch (error) {
      return { url, ok: false, status: 0, error: error?.name === "AbortError" ? `timed out after ${Math.round(timeoutMs / 1000)} s` : String(error?.message ?? error) };
    } finally {
      clearTimeout(timer);
      lastByHost.set(parsed.host, now());
    }
  };
}

/** Check the URLs one after another (the host gap serializes them anyway); returns the results. */
export async function checkLinks(urls, check) {
  const results = [];
  for (const url of urls) results.push(await check(url));
  return results;
}

/** The links item's detail line. */
export function linksDetail(results) {
  const broken = results.filter((result) => !result.ok);
  if (!results.length) return "the description has no links";
  const refused = results.filter((result) => result.refused);
  const note = refused.length ? `; ${refused.length} refuse automated checks and were not opened: ${refused.map((result) => `${result.url} (HTTP ${result.status})`).join(", ")}` : "";
  if (!broken.length) return `${results.length} links open${note}`;
  return `${broken.length} of ${results.length} links do not open: ${broken.map((result) => `${result.url} (${result.error})`).join(", ")}${note}`;
}
