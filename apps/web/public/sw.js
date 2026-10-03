/**
 * The day view (`/{locale}/trips/{id}?view=today`) opens with no signal at all — a cold
 * open, after the phone has thrown the tab away — and nothing else on the site is served
 * from here.
 *
 * What the worker keeps, in one cache named after the signed-in member:
 *
 * - the trip, `GET /api/travel/trips/{id}`, stored whenever a page reads it online;
 * - the day view's own document, which the day view asks the worker to keep (`keep-day`);
 * - the `/_next/static` files that document names: its scripts, styles and fonts.
 *
 * Without the last two the browser cannot draw the page offline and the stored trip is
 * never read; `tasks/done/2026-09-11-offline-today-e2e.md` measured exactly that.
 *
 * Four rules keep the blast radius small:
 *
 * 1. Online, the worker changes nothing. Every request it answers goes to the network
 *    first, and its cache is read only when the network fails, so nobody is served stale
 *    HTML or held on an old frontend after a deploy.
 * 2. It answers three kinds of GET and lets everything else go straight to the network:
 *    a day view's document, the trip, and the static files a kept day view names. No other
 *    page, no admin page and no other API response is ever stored.
 * 3. A trip payload and the page around it carry hotel addresses, private notes and the
 *    member's header, so nothing is stored until a page tells the worker who is signed in,
 *    a new member's announcement deletes the previous member's cache, and signing out
 *    deletes it all. A worker the browser has restarted reads the one member cache that
 *    exists, because on a cold open no page is running yet to say who that is, but it
 *    stores nothing until it is told again.
 * 4. The cache name carries a version. Change what is stored or how, bump `CACHE_VERSION`,
 *    and the next worker deletes every older cache when it activates.
 */

const CACHE_FAMILY = "mokaair-trip-";
const CACHE_VERSION = 2;
const CACHE_PREFIX = `${CACHE_FAMILY}v${CACHE_VERSION}-`;
const LOCALES = "en|ja|ko|zh-TW|zh-CN";
const DAY_VIEW_PATH = new RegExp(`^/(?:${LOCALES})/trips/[^/]+$`);
const TRIP_PATH = /^\/api\/travel\/trips\/[^/]+$/;

/** Set by a page's announcement, and the only name the worker ever writes to. */
let cacheName = null;
/** The member cache this worker reads when the network fails. */
let readName = null;
/** Static files a kept day view names; requests for any other file are left alone. */
let keptFiles = new Set();
/** Bumped by every announcement, so a slower lookup started before it cannot undo it. */
let generation = 0;
/** The `keep-day` run in progress, if any. */
let keeping = Promise.resolve(false);

function sameOrigin(url) {
  return url.origin === self.location.origin;
}

function isStaticFile(url) {
  return sameOrigin(url) && url.pathname.startsWith("/_next/static/");
}

function isDayView(url) {
  return sameOrigin(url) && DAY_VIEW_PATH.test(url.pathname) && url.searchParams.get("view") === "today";
}

function isTripRequest(url) {
  return sameOrigin(url) && TRIP_PATH.test(url.pathname);
}

/** One key per day view, however the traveller reached it (`?view=today&utm_source=…`). */
function dayKey(url) {
  return `${url.origin}${url.pathname}?view=today`;
}

/**
 * Every `/_next/static` file a document names: its script and stylesheet tags, and the
 * client chunks the React payload lists relative to `/_next/` (`"static/chunks/…"`).
 */
function filesNamedIn(html) {
  const files = new Set();
  const text = html.replace(/&amp;/g, "&");
  for (const match of text.matchAll(/\/_next\/static\/[^"'\s\\)<>]+/g)) {
    files.add(new URL(match[0], self.location.origin).href);
  }
  for (const match of text.matchAll(/(^|[^\w/])(static\/(?:chunks|css|media)\/[^"'\s\\)<>]+)/g)) {
    files.add(new URL(`/_next/${match[2]}`, self.location.origin).href);
  }
  return files;
}

async function filesIn(name) {
  if (!name || !(await caches.has(name))) return new Set();
  const requests = await (await caches.open(name)).keys();
  return new Set(requests.map((request) => request.url).filter((url) => isStaticFile(new URL(url))));
}

/** A restarted worker has heard no announcement: find what an earlier one stored. */
const restored = (async () => {
  const started = generation;
  try {
    const name = (await caches.keys()).find((candidate) => candidate.startsWith(CACHE_PREFIX)) || null;
    const files = await filesIn(name);
    if (generation !== started) return;
    readName = name;
    keptFiles = files;
  } catch {
    // No cache storage: there is simply nothing to fall back on.
  }
})();

async function readableCache() {
  await restored;
  const name = cacheName || readName;
  return name && (await caches.has(name)) ? caches.open(name) : null;
}

async function dropCachesExcept(keep) {
  const names = await caches.keys();
  await Promise.all(
    names
      .filter((name) => name.startsWith(CACHE_FAMILY) && name !== keep)
      .map((name) => caches.delete(name)),
  );
}

/** Missing fonts or images only change how the page looks; a missing script or style breaks it. */
function isRequiredFile(href) {
  return /\.(?:js|css)$/.test(new URL(href).pathname);
}

async function keepFile(cache, href) {
  if (await cache.match(href, { ignoreVary: true })) return true;
  try {
    const response = await fetch(href);
    if (!response.ok) return !isRequiredFile(href);
    await cache.put(href, response);
    return true;
  } catch {
    return !isRequiredFile(href);
  }
}

/**
 * Keeps the day view at `href` readable offline. The static files the fresh document names
 * are stored first and the document last, so a stored document never names a script the
 * cache lacks; if one cannot be fetched, the previous document and its files stay as they
 * were. Either way, files no stored document names, such as the previous build's chunks
 * after a deploy, are deleted.
 */
async function keepDay(href) {
  const name = cacheName;
  if (!name || typeof href !== "string") return false;
  const url = new URL(href, self.location.origin);
  if (!isDayView(url)) return false;
  const key = dayKey(url);
  const response = await fetch(key, { credentials: "same-origin", headers: { Accept: "text/html" } });
  const type = response.headers.get("content-type") || "";
  if (!response.ok || response.redirected || !type.includes("text/html")) return false;
  const cache = await caches.open(name);
  const files = filesNamedIn(await response.clone().text());
  const kept = await Promise.all([...files].map((file) => keepFile(cache, file)));
  if (cacheName !== name) return false;
  const complete = !kept.includes(false);
  if (complete) await cache.put(key, response);
  await forgetUnnamedFiles(cache);
  if (cacheName === name) keptFiles = await filesIn(name);
  return complete;
}

async function forgetUnnamedFiles(cache) {
  const requests = await cache.keys();
  const named = new Set();
  for (const request of requests) {
    if (!isDayView(new URL(request.url))) continue;
    const document = await cache.match(request, { ignoreVary: true });
    if (document) for (const file of filesNamedIn(await document.text())) named.add(file);
  }
  await Promise.all(
    requests
      .filter((request) => isStaticFile(new URL(request.url)) && !named.has(request.url))
      .map((request) => cache.delete(request)),
  );
}

self.addEventListener("install", (event) => {
  event.waitUntil(self.skipWaiting());
});

self.addEventListener("activate", (event) => {
  event.waitUntil((async () => {
    // Whatever an earlier version of this worker stored, in whatever shape it stored it.
    const names = await caches.keys();
    await Promise.all(
      names
        .filter((name) => name.startsWith(CACHE_FAMILY) && !name.startsWith(CACHE_PREFIX))
        .map((name) => caches.delete(name)),
    );
    await self.clients.claim();
  })());
});

self.addEventListener("message", (event) => {
  const data = event.data || {};
  const reply = event.ports && event.ports[0];
  if (data.type === "signed-in" && typeof data.member === "string" && data.member) {
    generation += 1;
    const name = `${CACHE_PREFIX}${data.member}`;
    if (readName !== name) keptFiles = new Set();
    cacheName = name;
    readName = name;
    // The page waits for this before priming the cache: until the name is set nothing
    // is stored, so anything fetched first would be lost.
    if (reply) reply.postMessage({ type: "ready" });
    event.waitUntil((async () => {
      await dropCachesExcept(name);
      const files = await filesIn(name);
      if (cacheName === name) keptFiles = files;
    })());
    return;
  }
  if (data.type === "keep-day") {
    // One at a time: a second run deleting the files of a first one's document before
    // that document is stored would leave a page that names scripts the cache lacks.
    const run = keeping.then(() => keepDay(data.url)).catch(() => false);
    keeping = run;
    event.waitUntil(run.then((kept) => {
      if (reply) reply.postMessage({ type: "kept", kept });
    }));
    return;
  }
  if (data.type === "signed-out") {
    generation += 1;
    cacheName = null;
    readName = null;
    keptFiles = new Set();
    event.waitUntil(dropCachesExcept(null));
  }
});

/** Network first; the kept document only when the network fails. */
async function dayDocument(request) {
  try {
    return await fetch(request);
  } catch (error) {
    const cache = await readableCache();
    const kept = cache && await cache.match(dayKey(new URL(request.url)), { ignoreVary: true });
    if (kept) return kept;
    throw error;
  }
}

/** The planner is an editing surface and never reads a stored trip; only the day view does. */
async function fromDayView(clientId) {
  const client = clientId ? await self.clients.get(clientId) : null;
  return Boolean(client && isDayView(new URL(client.url)));
}

async function trip(event) {
  const name = cacheName;
  try {
    const response = await fetch(event.request);
    if (name && response.ok) await (await caches.open(name)).put(event.request, response.clone());
    return response;
  } catch (error) {
    // Offline: the day the traveller last opened is still readable.
    const cache = await readableCache();
    const kept = cache && await cache.match(event.request, { ignoreVary: true });
    if (kept && await fromDayView(event.clientId)) return kept;
    throw error;
  }
}

async function staticFile(request) {
  try {
    return await fetch(request);
  } catch (error) {
    const cache = await readableCache();
    const kept = cache && await cache.match(request.url, { ignoreVary: true });
    if (kept) return kept;
    throw error;
  }
}

self.addEventListener("fetch", (event) => {
  const request = event.request;
  if (request.method !== "GET") return;
  const url = new URL(request.url);
  if (request.mode === "navigate") {
    if (isDayView(url)) event.respondWith(dayDocument(request));
    return;
  }
  if (isTripRequest(url)) {
    if (cacheName || readName) event.respondWith(trip(event));
    return;
  }
  if (keptFiles.has(url.href)) event.respondWith(staticFile(request));
});
