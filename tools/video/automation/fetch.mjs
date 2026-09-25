// Reading the pages a script cites, as the fact-checking agents did with curl: the editorial
// User-Agent (never anyone's name or email), one request per host a second at most, https only,
// the HTTP status checked, and the page reduced to its readable text for the model.
export const EDITORIAL_USER_AGENT = "Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)";
export const MAX_PAGE_BYTES = 3 * 1024 * 1024;
export const MAX_PAGE_CHARS = 40_000;
const HOST_GAP_MS = 1100;
const TIMEOUT_MS = 20_000;

const ENTITIES = { amp: "&", lt: "<", gt: ">", quot: '"', apos: "'", nbsp: " " };

/** The readable text of an HTML page: no scripts, styles, comments or tags; whitespace folded. */
export function pageText(html) {
  return String(html)
    .replace(/<!--[\s\S]*?-->/g, " ")
    .replace(/<(script|style|noscript|svg|template)\b[\s\S]*?<\/\1>/gi, " ")
    .replace(/<(br|\/p|\/div|\/li|\/h[1-6]|\/tr|\/section|\/article)\b[^>]*>/gi, "\n")
    .replace(/<[^>]+>/g, " ")
    .replace(/&(#x[0-9a-f]+|#\d+|[a-z]+);/gi, (entity, name) => {
      if (name[0] === "#") {
        const code = name[1].toLowerCase() === "x" ? Number.parseInt(name.slice(2), 16) : Number(name.slice(1));
        return Number.isFinite(code) && code > 0 && code < 0x110000 ? String.fromCodePoint(code) : " ";
      }
      return ENTITIES[name.toLowerCase()] ?? entity;
    })
    .replace(/[ \t\f\v ]+/g, " ")
    .replace(/\s*\n\s*/g, "\n")
    .trim();
}

export function pageTitle(html) {
  const match = /<title[^>]*>([\s\S]*?)<\/title>/i.exec(String(html));
  return match ? pageText(match[1]).slice(0, 300) : "";
}

/** A fetcher that keeps the per-host gap across calls; `now` and `sleep` are injectable. */
export function pageReader({ fetchImpl = globalThis.fetch, sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms)), now = () => Date.now() } = {}) {
  const lastByHost = new Map();
  return async function read(url) {
    let parsed;
    try {
      parsed = new URL(url);
    } catch {
      return { url, ok: false, status: 0, error: "not a URL" };
    }
    if (parsed.protocol !== "https:") return { url, ok: false, status: 0, error: "only https pages are read" };
    const wait = (lastByHost.get(parsed.host) ?? 0) + HOST_GAP_MS - now();
    if (wait > 0) await sleep(wait);
    lastByHost.set(parsed.host, now());
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), TIMEOUT_MS);
    try {
      const response = await fetchImpl(parsed.href, {
        headers: { "User-Agent": EDITORIAL_USER_AGENT, Accept: "text/html,application/xhtml+xml,text/plain;q=0.9,*/*;q=0.5", "Accept-Language": "zh-TW,en;q=0.8" },
        redirect: "follow",
        signal: controller.signal,
      });
      const type = response.headers.get("content-type") ?? "";
      const bytes = new Uint8Array(await response.arrayBuffer());
      if (!response.ok) return { url, final_url: response.url || url, ok: false, status: response.status, error: `HTTP ${response.status}` };
      if (bytes.length > MAX_PAGE_BYTES) return { url, ok: false, status: response.status, error: "page too large" };
      if (!/text\/|html|xml|json/.test(type)) return { url, ok: false, status: response.status, error: `not a text page (${type || "no type"})` };
      const html = new TextDecoder("utf-8").decode(bytes);
      const text = type.includes("html") ? pageText(html) : html.trim();
      return { url, final_url: response.url || url, ok: true, status: response.status, title: type.includes("html") ? pageTitle(html) : "", text: text.slice(0, MAX_PAGE_CHARS), truncated: text.length > MAX_PAGE_CHARS };
    } catch (error) {
      return { url, ok: false, status: 0, error: error.name === "AbortError" ? "timed out" : error.message };
    } finally {
      clearTimeout(timer);
    }
  };
}

/** Every https URL a text mentions, once each, in order. */
export function urlsIn(text) {
  const seen = new Set();
  for (const match of String(text).matchAll(/https:\/\/[^\s｜|<>"'）)\]，。、；：！？「」]+/g)) {
    const url = match[0].replace(/[.,;:。，、]+$/, "");
    seen.add(url);
  }
  return [...seen];
}
