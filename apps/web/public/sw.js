/**
 * The only thing this worker caches is the trip you are travelling on today.
 *
 * A trip payload carries hotel addresses and private notes, so the cache is named after
 * the signed-in member and nothing is stored until a page tells the worker who that is.
 * Signing out deletes it. Everything else — every other request, every method that is not
 * GET — goes straight to the network with no interception at all, so a bug here can only
 * affect one URL shape.
 */

const CACHE_PREFIX = "mokaair-trip-";
let cacheName = null;

async function dropCachesExcept(keep) {
  const names = await caches.keys();
  await Promise.all(
    names
      .filter((name) => name.startsWith(CACHE_PREFIX) && name !== keep)
      .map((name) => caches.delete(name)),
  );
}

self.addEventListener("install", (event) => {
  event.waitUntil(self.skipWaiting());
});

self.addEventListener("activate", (event) => {
  event.waitUntil(self.clients.claim());
});

self.addEventListener("message", (event) => {
  const data = event.data || {};
  if (data.type === "signed-in" && typeof data.member === "string" && data.member) {
    cacheName = `${CACHE_PREFIX}${data.member}`;
    event.waitUntil(dropCachesExcept(cacheName));
    return;
  }
  if (data.type === "signed-out") {
    cacheName = null;
    event.waitUntil(dropCachesExcept(null));
  }
});

function isTripRequest(url) {
  return url.origin === self.location.origin && /^\/api\/travel\/trips\/[^/]+$/.test(url.pathname);
}

self.addEventListener("fetch", (event) => {
  if (event.request.method !== "GET" || !cacheName) return;
  const url = new URL(event.request.url);
  if (!isTripRequest(url)) return;
  event.respondWith(
    (async () => {
      const cache = await caches.open(cacheName);
      try {
        const response = await fetch(event.request);
        if (response.ok) await cache.put(event.request, response.clone());
        return response;
      } catch (error) {
        // Offline: the day the traveller last opened is still readable.
        const cached = await cache.match(event.request);
        if (cached) return cached;
        throw error;
      }
    })(),
  );
});
