import { readFileSync } from "node:fs";
import path from "node:path";
import { describe, expect, it, vi } from "vitest";

/**
 * `public/sw.js` run against an in-memory Cache Storage and a scripted network.
 *
 * A browser cannot be made to restart a worker or to lose its signal on cue in a unit
 * test, but the script can be started twice against the same caches, and the network can
 * be switched off — which is all a cold open with no signal is.
 */

const source = readFileSync(path.join(import.meta.dirname, "../public/sw.js"), "utf8");
const ORIGIN = "https://mokaair.test";
const DAY = `${ORIGIN}/zh-TW/trips/trip-1?view=today`;
const PLANNER = `${ORIGIN}/zh-TW/trips/trip-1`;
const TRIP = `${ORIGIN}/api/travel/trips/trip-1`;

type RequestLike = { url: string; method?: string; mode?: string };

function keyOf(input: string | RequestLike) {
  return typeof input === "string" ? new URL(input, ORIGIN).href : input.url;
}

class MemoryCache {
  entries = new Map<string, Response>();
  async match(input: string | RequestLike) {
    return this.entries.get(keyOf(input))?.clone();
  }
  async put(input: string | RequestLike, response: Response) {
    this.entries.set(keyOf(input), response);
  }
  async keys() {
    return [...this.entries.keys()].map((url) => ({ url }));
  }
  async delete(input: string | RequestLike) {
    return this.entries.delete(keyOf(input));
  }
}

class MemoryCaches {
  stores = new Map<string, MemoryCache>();
  async open(name: string) {
    if (!this.stores.has(name)) this.stores.set(name, new MemoryCache());
    return this.stores.get(name) as MemoryCache;
  }
  async has(name: string) {
    return this.stores.has(name);
  }
  async keys() {
    return [...this.stores.keys()];
  }
  async delete(name: string) {
    return this.stores.delete(name);
  }
  urls(name: string) {
    return [...(this.stores.get(name)?.entries.keys() || [])];
  }
}

function html(build: string) {
  return `<!DOCTYPE html><html><head>`
    + `<link rel="stylesheet" href="/_next/static/css/${build}.css" data-precedence="next"/>`
    + `<link rel="preload" href="/_next/static/media/font-${build}.woff2" as="font" crossorigin=""/>`
    + `</head><body><main>day view ${build}</main>`
    + `<script src="/_next/static/chunks/webpack-${build}.js" async=""></script>`
    + `<script>self.__next_f.push([1,"5:I[42,[\\"static/chunks/app/%5Blocale%5D/trips/%5Bid%5D/page-${build}.js\\"],\\"TodayView\\"]"])</script>`
    + `</body></html>`;
}

function filesOf(build: string) {
  return [
    `${ORIGIN}/_next/static/css/${build}.css`,
    `${ORIGIN}/_next/static/media/font-${build}.woff2`,
    `${ORIGIN}/_next/static/chunks/webpack-${build}.js`,
    `${ORIGIN}/_next/static/chunks/app/%5Blocale%5D/trips/%5Bid%5D/page-${build}.js`,
  ];
}

/**
 * The site as the network serves it, and a switch for the signal. `pages` lists the build
 * each next document request gets, for a deploy that lands between two requests; a build's
 * files stay downloadable after the next deploy, as they do on the host.
 */
function network() {
  const state = {
    online: true, build: "a", pages: [] as string[], missing: new Set<string>(), slow: new Set<string>(),
    asked: [] as string[],
  };
  const builds = new Set(["a"]);
  const fetch = vi.fn(async (input: string | RequestLike) => {
    const url = keyOf(input);
    state.asked.push(url);
    if (state.slow.has(url)) await new Promise((resolve) => setTimeout(resolve, 20));
    if (!state.online) throw new TypeError("Failed to fetch");
    builds.add(state.build);
    if (state.missing.has(url)) return new Response("not found", { status: 404 });
    if (url.startsWith(`${ORIGIN}/zh-TW/`)) {
      const build = state.pages.shift() || state.build;
      builds.add(build);
      return new Response(html(build), { headers: { "Content-Type": "text/html; charset=utf-8" } });
    }
    if (url === TRIP) return new Response(JSON.stringify({ id: "trip-1", name: `trip ${state.build}` }));
    if ([...builds].some((build) => filesOf(build).includes(url))) return new Response(`file ${url}`);
    return new Response("not found", { status: 404 });
  });
  return { state, fetch };
}

type Listener = (event: Record<string, unknown>) => void;

/** Starts `public/sw.js` the way a browser does, as often as a test likes. */
function startWorker(caches: MemoryCaches, fetch: ReturnType<typeof network>["fetch"]) {
  const listeners = new Map<string, Listener>();
  const pages = new Map<string, string>([["day", DAY], ["planner", PLANNER]]);
  const scope = {
    location: new URL(`${ORIGIN}/sw.js`),
    addEventListener: (type: string, listener: Listener) => listeners.set(type, listener),
    skipWaiting: vi.fn(async () => undefined),
    clients: {
      claim: vi.fn(async () => undefined),
      get: vi.fn(async (id: string) => (pages.has(id) ? { url: pages.get(id) } : undefined)),
    },
  };
  new Function("self", "caches", "fetch", source)(scope, caches, fetch);

  /** The response the worker answers with, or `undefined` when it lets the browser go on. */
  function request(url: string, { mode = "cors", method = "GET", client }: { mode?: string; method?: string; client?: string } = {}) {
    let answer: Promise<Response> | undefined;
    listeners.get("fetch")?.({
      request: { url, method, mode },
      clientId: client,
      respondWith: (response: Promise<Response>) => { answer = response; },
    });
    return answer;
  }

  async function message(data: Record<string, unknown>) {
    const replies: unknown[] = [];
    const pending: Promise<unknown>[] = [];
    listeners.get("message")?.({
      data,
      ports: [{ postMessage: (reply: unknown) => replies.push(reply) }],
      waitUntil: (promise: Promise<unknown>) => pending.push(promise),
    });
    await Promise.all(pending);
    return replies;
  }

  async function activate() {
    const pending: Promise<unknown>[] = [];
    listeners.get("activate")?.({ waitUntil: (promise: Promise<unknown>) => pending.push(promise) });
    await Promise.all(pending);
  }

  return { request, message, activate, scope };
}

const MEMBER_CACHE = "mokaair-trip-v2-member-1";

/** A traveller who opened the day view online: signed in, trip read, page kept. */
async function visitOnline(caches: MemoryCaches, net: ReturnType<typeof network>) {
  const worker = startWorker(caches, net.fetch);
  await worker.message({ type: "signed-in", member: "member-1" });
  await worker.request(TRIP, { client: "day" });
  expect(await worker.message({ type: "keep-day", url: `${DAY}&utm_source=home` }))
    .toEqual([{ type: "kept", kept: true }]);
  return worker;
}

describe("public/sw.js", () => {
  it("opens the kept day view in a restarted worker with no signal: page, scripts and trip", async () => {
    const caches = new MemoryCaches();
    const net = network();
    await visitOnline(caches, net);

    net.state.online = false;
    const cold = startWorker(caches, net.fetch);

    const page = cold.request(`${DAY}&utm_source=home`, { mode: "navigate" });
    expect(page).toBeDefined();
    expect(await (await page)?.text()).toContain("day view a");
    for (const file of filesOf("a")) {
      expect(await (await cold.request(file))?.text()).toBe(`file ${file}`);
    }
    expect(await (await cold.request(TRIP, { client: "day" }))?.json()).toEqual({ id: "trip-1", name: "trip a" });
  });

  it("answers from the network whenever there is one, so a deploy is never hidden behind the cache", async () => {
    const caches = new MemoryCaches();
    const net = network();
    const worker = await visitOnline(caches, net);

    net.state.build = "b";

    expect(await (await worker.request(DAY, { mode: "navigate" }))?.text()).toContain("day view b");
    expect(await (await worker.request(TRIP, { client: "day" }))?.json()).toEqual({ id: "trip-1", name: "trip b" });
  });

  it("keeps the new build's files after a deploy and deletes the old build's", async () => {
    const caches = new MemoryCaches();
    const net = network();
    const worker = await visitOnline(caches, net);

    net.state.build = "b";
    expect(await worker.message({ type: "keep-day", url: DAY })).toEqual([{ type: "kept", kept: true }]);

    const stored = caches.urls(MEMBER_CACHE);
    for (const file of filesOf("b")) expect(stored).toContain(file);
    for (const file of filesOf("a")) expect(stored).not.toContain(file);
    expect(await (await (await caches.open(MEMBER_CACHE)).match(DAY))?.text()).toContain("day view b");
  });

  it("keeps the previous page when a script of the new one cannot be fetched", async () => {
    const caches = new MemoryCaches();
    const net = network();
    const worker = await visitOnline(caches, net);

    net.state.build = "b";
    net.state.missing.add(filesOf("b")[2]);
    expect(await worker.message({ type: "keep-day", url: DAY })).toEqual([{ type: "kept", kept: false }]);
    // Nor are the new build's files that did arrive left behind with no page to use them.
    for (const file of filesOf("b")) expect(caches.urls(MEMBER_CACHE)).not.toContain(file);

    net.state.online = false;
    const cold = startWorker(caches, net.fetch);
    expect(await (await cold.request(DAY, { mode: "navigate" }))?.text()).toContain("day view a");
    for (const file of filesOf("a")) expect(await (await cold.request(file))?.text()).toBe(`file ${file}`);
  });

  it("never leaves a page that names files it deleted when two visits keep the day at once", async () => {
    const caches = new MemoryCaches();
    const net = network();
    const worker = startWorker(caches, net.fetch);
    await worker.message({ type: "signed-in", member: "member-1" });

    // A deploy lands between the two document requests, and one new script is slow to arrive:
    // the first visit finishes, and tidies up, while the second is still storing files.
    net.state.pages = ["a", "b"];
    net.state.slow.add(filesOf("b")[3]);
    await Promise.all([worker.message({ type: "keep-day", url: DAY }), worker.message({ type: "keep-day", url: DAY })]);

    net.state.online = false;
    const cold = startWorker(caches, net.fetch);
    expect(await (await cold.request(DAY, { mode: "navigate" }))?.text()).toContain("day view b");
    for (const file of filesOf("b")) expect(await (await cold.request(file))?.text()).toBe(`file ${file}`);
  });

  it("keeps the page when only a font is missing, which changes how it looks and not whether it works", async () => {
    const caches = new MemoryCaches();
    const net = network();
    net.state.missing.add(filesOf("a")[1]);

    await visitOnline(caches, net);

    expect(caches.urls(MEMBER_CACHE)).toContain(DAY);
  });

  it("keeps nothing but a day view, and nothing before it knows who is signed in", async () => {
    const caches = new MemoryCaches();
    const net = network();
    const worker = startWorker(caches, net.fetch);

    expect(await worker.message({ type: "keep-day", url: DAY })).toEqual([{ type: "kept", kept: false }]);
    expect(worker.request(TRIP, { client: "day" })).toBeUndefined();

    await worker.message({ type: "signed-in", member: "member-1" });
    for (const url of [PLANNER, `${ORIGIN}/zh-TW/admin/users?view=today`, `${ORIGIN}/zh-TW?view=today`,
      "https://elsewhere.test/zh-TW/trips/trip-1?view=today", `${ORIGIN}/api/travel/trips/trip-1?view=today`]) {
      expect(await worker.message({ type: "keep-day", url })).toEqual([{ type: "kept", kept: false }]);
    }
    expect(net.state.asked).toEqual([]);
  });

  it("leaves every other request to the browser", async () => {
    const caches = new MemoryCaches();
    const net = network();
    const worker = await visitOnline(caches, net);

    expect(worker.request(PLANNER, { mode: "navigate" })).toBeUndefined();
    expect(worker.request(`${ORIGIN}/zh-TW`, { mode: "navigate" })).toBeUndefined();
    expect(worker.request(`${ORIGIN}/zh-TW/admin?view=today`, { mode: "navigate" })).toBeUndefined();
    expect(worker.request(`${ORIGIN}/api/travel/auth/me`)).toBeUndefined();
    expect(worker.request(`${ORIGIN}/_next/static/chunks/not-on-the-day-view.js`)).toBeUndefined();
    expect(worker.request(TRIP, { method: "PATCH", client: "day" })).toBeUndefined();
    expect(worker.request(DAY, { mode: "navigate", method: "POST" })).toBeUndefined();
  });

  it("never gives the planner a stored trip", async () => {
    const caches = new MemoryCaches();
    const net = network();
    await visitOnline(caches, net);

    net.state.online = false;
    const cold = startWorker(caches, net.fetch);
    await cold.request(DAY, { mode: "navigate" });

    await expect(cold.request(TRIP, { client: "planner" })).rejects.toThrow("Failed to fetch");
  });

  it("deletes everything on sign-out, and the previous member's cache when another signs in", async () => {
    const caches = new MemoryCaches();
    const net = network();
    const worker = await visitOnline(caches, net);

    await worker.message({ type: "signed-in", member: "member-2" });
    await worker.request(TRIP, { client: "day" });
    expect(await caches.keys()).toEqual(["mokaair-trip-v2-member-2"]);

    await worker.message({ type: "signed-out" });
    expect(await caches.keys()).toEqual([]);

    net.state.online = false;
    const cold = startWorker(caches, net.fetch);
    await expect(cold.request(DAY, { mode: "navigate" })).rejects.toThrow("Failed to fetch");
  });

  it("deletes what an older version of the worker stored when it activates", async () => {
    const caches = new MemoryCaches();
    await caches.open("mokaair-trip-member-1");
    await caches.open(MEMBER_CACHE);
    await caches.open("someone-elses-cache");
    const worker = startWorker(caches, network().fetch);

    await worker.activate();

    expect(await caches.keys()).toEqual([MEMBER_CACHE, "someone-elses-cache"]);
    expect(worker.scope.clients.claim).toHaveBeenCalled();
  });
});
