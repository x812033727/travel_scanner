import { renderToString } from "react-dom/server";
import { beforeEach, describe, expect, it, vi } from "vitest";
import Home from "./page";

const state = vi.hoisted(() => ({ enabled: false, featuresEnabled: true }));
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

beforeEach(() => { state.enabled = false; state.featuresEnabled = true; });

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
