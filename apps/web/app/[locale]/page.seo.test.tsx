import { renderToString } from "react-dom/server";
import { beforeEach, describe, expect, it, vi } from "vitest";
import Home from "./page";

const state = vi.hoisted(() => ({ enabled: false, featuresEnabled: true, feed: null as unknown }));
vi.mock("@/lib/discovery-status.server", () => ({ getDiscoveryStatus: async () => ({ enabled: state.enabled }) }));
vi.mock("@/lib/site-visibility.server", () => ({ getSiteVisibility: async () => ({
  status: "ready", features: { hotspots_enabled: state.featuresEnabled, trips_enabled: state.featuresEnabled },
}) }));
vi.mock("@/lib/discovery", async (original) => ({
  ...await original<typeof import("@/lib/discovery")>(), useDiscoveryStatus: () => ({ enabled: false, loading: true }),
}));
vi.mock("@/components/site-header", () => ({ SiteHeader: () => null }));
vi.mock("@/components/search-workbench", () => ({ SearchWorkbench: () => <form id="trip-search" /> }));
vi.mock("@/components/community/home", () => ({ CommunityHero: () => null, CommunityHome: () => null }));
// The feed the server hands the gate. `/explore` has always fetched this; the home page did
// not, which is the whole bug these cases cover.
vi.mock("@/lib/discovery.server", async (original) => ({
  ...await original<typeof import("@/lib/discovery.server")>(),
  getInitialDiscoveryFeed: async () => state.feed,
}));
// What the explorer needs to render outside a Next request. Only reached by the
// discovery-on cases; the marketing cases never mount it.
vi.mock("@/lib/api", () => ({ api: vi.fn() }));
vi.mock("next/navigation", () => ({ useSearchParams: () => new URLSearchParams("") }));
vi.mock("@/components/header-session", () => ({
  useHeaderSession: () => ({ user: null, status: "signed_out", sessionIdentity: null }),
}));
vi.mock("@/components/community/provider", () => ({ useCommunity: () => ({ flags: { enabled: false }, me: null }) }));

beforeEach(() => { state.enabled = false; state.featuresEnabled = true; state.feed = null; });

describe("marketing homepage server HTML", () => {
  it("contains heading, localized destination rail, and safe JSON-LD without client effects", async () => {
    const html = renderToString(await Home());
    expect(html).toContain("<h1");
    expect(html).toContain('href="/destinations/tokyo"');
    expect(html).toContain('id="trip-search"');
    expect(html).toContain('"@type":"Organization"');
    expect(html).toContain('"@type":"SearchAction"');
  });

  it("does not render closed module links or structured search actions", async () => {
    state.featuresEnabled = false;
    const html = renderToString(await Home());
    expect(html).not.toContain('href="/hotspots"');
    expect(html).not.toContain('href="/trips"');
    expect(html).not.toContain('"@type":"SearchAction"');
    expect(html).toContain('href="/foods"');
    expect(html).toContain('href="/destinations/tokyo"');
  });
});

/** The skeleton's own accessible name, from `lib/frontend-flow-copy.ts`. */
const SKELETON = "正在載入旅行靈感";
const item = {
  id: "guide:11111111-1111-4111-8111-111111111111", kind: "article", title: "東京散步攻略",
  summary: "從官方步道資料開始", locale: "ja", href: "/hotspots",
  destination: { id: "tokyo", name: "東京" },
  source: { kind: "editorial", label: "City guide", url: "https://example.org/guide" },
  published_at: "2026-09-01T00:00:00Z", updated_at: null, thumbnail_url: null,
  collection_ref: { kind: "guide", id: "11111111-1111-4111-8111-111111111111" },
};
const seededFeed = {
  path: "/discovery/feed?mode=recommended",
  page: { enabled: true, items: [item], next_cursor: null, query: "", filters: { kinds: [], destinations: [], topics: [] } },
};

describe("discovery homepage server HTML", () => {
  it("carries the feed's first page, not a skeleton", async () => {
    state.enabled = true; state.feed = seededFeed;
    const html = renderToString(await Home());
    expect(html).toContain("東京散步攻略");
    expect(html).not.toContain(SKELETON);
  });

  it("falls back to the marketing body when the feed cannot be read", async () => {
    state.enabled = true; state.feed = null;
    const html = renderToString(await Home());
    // A failed or empty feed read must never cost a crawler the whole page.
    expect(html).not.toContain(SKELETON);
    expect(html).toContain('href="/destinations/tokyo"');
    expect(html).toContain("<h1");
  });
});
