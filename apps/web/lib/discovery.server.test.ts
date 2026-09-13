import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
const { incoming } = vi.hoisted(() => ({ incoming: vi.fn() }));
// The loader reads the visitor's address out of the request so the API can meter reads per
// source. Nothing here depends on the value; it just has to be readable.
vi.mock("next/headers", () => ({ headers: incoming }));
incoming.mockResolvedValue(new Headers({ "x-forwarded-for": "203.0.113.9" }));
import { discoveryFeedPath, discoveryMode, loadInitialDiscoveryFeed } from "./discovery.server";
import { discoveryQuery } from "./discovery";

const page = { enabled: true, items: [{ id: "guide:1" }], next_cursor: null, query: "", filters: { kinds: [], destinations: [], topics: [] } };

function respond(body: unknown, ok = true) {
  return vi.fn().mockResolvedValue({ ok, json: async () => body });
}

beforeEach(() => { vi.stubGlobal("fetch", respond(page)); });
afterEach(() => { vi.unstubAllGlobals(); });

/**
 * What the explorer itself would request for the same URL. `lib/discovery.ts` is a client
 * module, so the server cannot call into it at runtime -- but a test can import both, which is
 * the only thing keeping the two query builders from drifting apart. They have to agree
 * character for character: the component matches the server's answer by path, and a mismatch
 * means it quietly fetches again and the reader sees the swap this module exists to remove.
 */
function clientPath(search: Record<string, string>): string {
  const value = Object.fromEntries(
    ["q", "type", "category", "destination", "topic", "locale", "mode"].map((key) => [key, search[key] || ""]),
  );
  const mode = ["recommended", "latest", "most_saved", "following"].includes(value.mode || "") ? value.mode! : "recommended";
  return `/discovery/${value.q ? "search" : "feed"}?${discoveryQuery({ ...value, mode })}`;
}

describe("the path the server prefetches", () => {
  it.each([
    {},
    { category: "hotspots" },
    { mode: "latest" },
    { mode: "most_saved", destination: "tokyo", topic: "culture", locale: "ja" },
    // "all" is the explorer's own default for these two and is left out of the query.
    { type: "all", category: "all" },
    { type: "article" },
    // Not one of the four rankings: the explorer falls back to `recommended`, and so must this.
    { mode: "nonsense" },
  ])("matches the request the explorer would make for %o", (search) => {
    expect(discoveryFeedPath(search, true)).toBe(clientPath(search as Record<string, string>));
  });

  it("reads a repeated parameter the way the browser does, first value only", () => {
    expect(discoveryFeedPath({ destination: ["tokyo", "osaka"] }, true)).toBe(clientPath({ destination: "tokyo" }));
    expect(discoveryMode({ mode: ["latest", "recommended"] })).toBe("latest");
  });

  it("asks for nothing when there is nothing the server can usefully answer", () => {
    // The switch is off: the page renders the fallback link grid, with no feed in it.
    expect(discoveryFeedPath({}, false)).toBeNull();
    // A search records an analytics event on its first page, and a signed-in reader's client
    // repeats it under their own identity. Serving it here would count one search twice.
    expect(discoveryFeedPath({ q: "tokyo" }, true)).toBeNull();
    expect(discoveryFeedPath({ q: "   " }, true)).not.toBeNull();
    // `following` needs a session, and the server render reads no cookies.
    expect(discoveryFeedPath({ mode: "following" }, true)).toBeNull();
  });
});

describe("the prefetch itself", () => {
  it("never caches a feed an editor can withdraw from, and gives up rather than hanging the page", async () => {
    const fetchMock = respond(page);
    vi.stubGlobal("fetch", fetchMock);
    const result = await loadInitialDiscoveryFeed("ja", "/discovery/feed?mode=latest");
    const [url, init] = fetchMock.mock.calls[0];
    expect(new URL(url).pathname).toBe("/api/v1/discovery/feed");
    expect(new URL(url).searchParams.get("mode")).toBe("latest");
    expect(init.cache).toBe("no-store");
    expect(init.signal).toBeInstanceOf(AbortSignal);
    expect(init.headers["X-Travel-Locale"]).toBe("ja");
    // No cookie or authorization header: this is the public ranking, not anyone's own.
    expect(Object.keys(init.headers).map((key) => key.toLowerCase())).not.toContain("cookie");
    expect(result).toEqual({ path: "/discovery/feed?mode=latest", page });
  });

  it("makes no request at all when there is no path", async () => {
    const fetchMock = respond(page);
    vi.stubGlobal("fetch", fetchMock);
    await expect(loadInitialDiscoveryFeed("en", null)).resolves.toBeNull();
    expect(fetchMock).not.toHaveBeenCalled();
  });

  it("degrades to no initial page rather than failing the render", async () => {
    vi.stubGlobal("fetch", respond(null, false));
    await expect(loadInitialDiscoveryFeed("en", "/discovery/feed?")).resolves.toBeNull();
    vi.stubGlobal("fetch", vi.fn().mockRejectedValue(new Error("connection reset")));
    await expect(loadInitialDiscoveryFeed("en", "/discovery/feed?")).resolves.toBeNull();
  });
});
