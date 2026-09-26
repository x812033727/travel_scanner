import { act, render, waitFor } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { resetThirdPartyAudience, setThirdPartyAudience } from "@/lib/third-party-audience";

const navigation = vi.hoisted(() => ({ pathname: "/zh-TW/hotspots" }));
vi.mock("next/navigation", () => ({ usePathname: () => navigation.pathname }));
vi.mock("next/script", () => ({ default: (props: { src?: string }) => <script data-src={props.src} /> }));

import { AnalyticsProvider } from "./analytics-provider";

describe("AnalyticsProvider", () => {
  beforeEach(() => {
    // A signed-out reader, unless a case says otherwise.
    setThirdPartyAudience("allowed");
  });

  afterEach(() => {
    vi.unstubAllGlobals();
    sessionStorage.clear();
    window.dataLayer = undefined;
    window.gtag = undefined;
    document.cookie = "travel_oauth_registered=; path=/; max-age=0";
    Object.defineProperty(navigator, "doNotTrack", { configurable: true, value: null });
    navigation.pathname = "/zh-TW/hotspots";
    window.history.replaceState(null, "", "/");
    resetThirdPartyAudience();
  });

  function withGa4() {
    const fetchMock = vi.fn(async (input: RequestInfo | URL, init?: RequestInit) => {
      void init;
      if (String(input).endsWith("/analytics/config")) return new Response(JSON.stringify({ first_party_enabled: true, ga4_enabled: true, ga4_measurement_id: "G-ABCD1234" }));
      return new Response(JSON.stringify({ accepted: 1, enabled: true }), { status: 202 });
    });
    vi.stubGlobal("fetch", fetchMock);
    const sentFirstParty = () => fetchMock.mock.calls.some(([url]) => String(url).endsWith("/analytics/events"));
    return sentFirstParty;
  }

  it("never loads gtag.js for an administrator, and still counts the view first-party", async () => {
    resetThirdPartyAudience();
    setThirdPartyAudience("blocked");
    const sentFirstParty = withGa4();
    const view = render(<AnalyticsProvider><div>content</div></AnalyticsProvider>);
    await waitFor(() => expect(sentFirstParty()).toBe(true));
    expect(view.container.querySelector('script[data-src^="https://www.googletagmanager.com/"]')).toBeNull();
    expect(window.dataLayer).toBeUndefined();
  });

  it("starts GA4 once a signed-in reader clears, and sends that page's view to it once", async () => {
    resetThirdPartyAudience();
    const sentFirstParty = withGa4();
    const view = render(<AnalyticsProvider><div>content</div></AnalyticsProvider>);
    await waitFor(() => expect(sentFirstParty()).toBe(true));
    expect(window.dataLayer).toBeUndefined();

    act(() => setThirdPartyAudience("allowed"));
    await waitFor(() => expect(view.container.querySelector('script[data-src^="https://www.googletagmanager.com/"]')).not.toBeNull());
    const pageViews = (window.dataLayer || []).filter((row) => row[0] === "event" && row[1] === "page_view");
    expect(pageViews).toHaveLength(1);
    expect(pageViews[0][2]).toMatchObject({ page_path: "/zh-TW/hotspots" });
  });

  describe("a campaign-tagged landing", () => {
    const ga4PageViews = () => (window.dataLayer || []).filter((row) => row[0] === "event" && row[1] === "page_view");
    const ga4Config = () => (window.dataLayer || []).find((row) => row[0] === "config");
    // What a video description links to (tools/video/core/metadata.mjs `articleUrl`), plus a
    // search term and a click identifier that must never reach GA4.
    const landing = "/zh-TW/life/ai-notes?utm_source=youtube&utm_medium=video&utm_campaign=ai-notes&q=secret-term&fbclid=IwAR0click";

    it("gives GA4 the tags on the first page view, and on no later one", async () => {
      window.history.replaceState(null, "", landing);
      navigation.pathname = "/zh-TW/life/ai-notes";
      withGa4();
      const view = render(<AnalyticsProvider><div>content</div></AnalyticsProvider>);
      await waitFor(() => expect(ga4PageViews()).toHaveLength(1));
      // GA4 takes a session's campaign from these parameters of the location it is given,
      // not from the real address; a bare path filed the visit under its referrer.
      const tagged = `${location.origin}/zh-TW/life/ai-notes?utm_source=youtube&utm_medium=video&utm_campaign=ai-notes`;
      expect(ga4PageViews()[0][2]).toMatchObject({ page_path: "/zh-TW/life/ai-notes", page_location: tagged });
      expect(ga4Config()?.[2]).toMatchObject({ page_location: tagged });

      navigation.pathname = "/zh-TW/life/codex-cli-install-windows-guide";
      view.rerender(<AnalyticsProvider><div>content</div></AnalyticsProvider>);
      await waitFor(() => expect(ga4PageViews()).toHaveLength(2));
      expect(ga4PageViews()[1][2]).toMatchObject({ page_location: `${location.origin}/zh-TW/life/codex-cli-install-windows-guide` });
      const sent = JSON.stringify(window.dataLayer);
      expect(sent).not.toContain("secret-term");
      expect(sent).not.toContain("fbclid");
      expect(sent).not.toContain("IwAR0click");
    });

    it("cleans a tag and leaves out a missing one, the way the first-party record does", async () => {
      window.history.replaceState(null, "", "/zh-TW/life/ai-notes?utm_source=youtube&utm_campaign=ai%3Cnotes%3E");
      navigation.pathname = "/zh-TW/life/ai-notes";
      withGa4();
      render(<AnalyticsProvider><div>content</div></AnalyticsProvider>);
      await waitFor(() => expect(ga4PageViews()).toHaveLength(1));
      expect(ga4PageViews()[0][2]).toMatchObject({
        page_location: `${location.origin}/zh-TW/life/ai-notes?utm_source=youtube&utm_campaign=ainotes`,
      });
    });

    it("still gives GA4 the tags when it only starts after a signed-in reader clears", async () => {
      resetThirdPartyAudience();
      window.history.replaceState(null, "", landing);
      navigation.pathname = "/zh-TW/life/ai-notes";
      const sentFirstParty = withGa4();
      render(<AnalyticsProvider><div>content</div></AnalyticsProvider>);
      await waitFor(() => expect(sentFirstParty()).toBe(true));
      act(() => setThirdPartyAudience("allowed"));
      await waitFor(() => expect(ga4PageViews()).toHaveLength(1));
      expect(ga4PageViews()[0][2]).toMatchObject({
        page_location: `${location.origin}/zh-TW/life/ai-notes?utm_source=youtube&utm_medium=video&utm_campaign=ai-notes`,
      });
    });

    it("sends GA4 a bare location when the landing carried no tags", async () => {
      window.history.replaceState(null, "", "/zh-TW/life/ai-notes?q=secret-term");
      navigation.pathname = "/zh-TW/life/ai-notes";
      withGa4();
      render(<AnalyticsProvider><div>content</div></AnalyticsProvider>);
      await waitFor(() => expect(ga4PageViews()).toHaveLength(1));
      expect(ga4PageViews()[0][2]).toMatchObject({ page_location: `${location.origin}/zh-TW/life/ai-notes` });
      expect(ga4Config()?.[2]).toMatchObject({ page_location: `${location.origin}/zh-TW/life/ai-notes` });
    });
  });

  function firstPartyOnly() {
    const fetchMock = vi.fn(async (input: RequestInfo | URL, init?: RequestInit) => {
      void init;
      if (String(input).endsWith("/analytics/config")) return new Response(JSON.stringify({ first_party_enabled: true, ga4_enabled: false }));
      return new Response(JSON.stringify({ accepted: 1, enabled: true }), { status: 202 });
    });
    vi.stubGlobal("fetch", fetchMock);
    const pageViews = () => fetchMock.mock.calls
      .filter(([url]) => String(url).endsWith("/analytics/events"))
      .flatMap(([, init]) => JSON.parse(String(init?.body)).events)
      .filter((event: { name: string }) => event.name === "page_view")
      .map((event: { path: string }) => event.path);
    return pageViews;
  }

  it.each([
    ["/zh-TW/life/claude-code-first-project-setup", "/zh-TW/life/claude-code-first-project-setup"],
    ["/en/guides/howto/tokyo-where-to-stay-first-trip", "/en/guides/howto/tokyo-where-to-stay-first-trip"],
    ["/zh-TW/share/claude-code-first-project-setup", "/zh-TW/share/:id"],
    ["/zh-TW/life/AbCdEfGhIjKlMnOpQrStUv_", "/zh-TW/life/:id"],
    ["/zh-TW/trips/550e8400-e29b-41d4-a716-446655440000", "/zh-TW/trips/:id"],
  ])("reports %s as %s", async (pathname, expected) => {
    navigation.pathname = pathname;
    const pageViews = firstPartyOnly();
    render(<AnalyticsProvider><div>content</div></AnalyticsProvider>);
    await waitFor(() => expect(pageViews()).toEqual([expected]));
  });

  it("keeps gtag.js off a private page but still sends the first-party view", async () => {
    navigation.pathname = "/zh-TW/trips/550e8400-e29b-41d4-a716-446655440000";
    const fetchMock = vi.fn(async (input: RequestInfo | URL, init?: RequestInit) => {
      void init;
      if (String(input).endsWith("/analytics/config")) return new Response(JSON.stringify({ first_party_enabled: true, ga4_enabled: true, ga4_measurement_id: "G-ABCD1234" }));
      return new Response(JSON.stringify({ accepted: 1, enabled: true }), { status: 202 });
    });
    vi.stubGlobal("fetch", fetchMock);
    const view = render(<AnalyticsProvider><div>content</div></AnalyticsProvider>);
    await waitFor(() => expect(fetchMock.mock.calls.some(([url]) => String(url).endsWith("/analytics/events"))).toBe(true));
    const gtagScript = () => view.container.querySelector('script[data-src^="https://www.googletagmanager.com/"]');
    expect(gtagScript()).toBeNull();
    expect(window.dataLayer).toBeUndefined();

    // Reaching a public page in the same document is where GA4 may start.
    navigation.pathname = "/zh-TW/hotspots";
    view.rerender(<AnalyticsProvider><div>content</div></AnalyticsProvider>);
    await waitFor(() => expect(gtagScript()).not.toBeNull());
    expect((window.dataLayer || []).some((row) => row[0] === "config")).toBe(true);
  });

  it("counts a second long-slug article as its own page view", async () => {
    // Both slugs used to become `/life/:id`, and the repeat guard then dropped the second view.
    navigation.pathname = "/zh-TW/life/claude-code-first-project-setup";
    const pageViews = firstPartyOnly();
    const view = render(<AnalyticsProvider><div>content</div></AnalyticsProvider>);
    await waitFor(() => expect(pageViews()).toHaveLength(1));
    navigation.pathname = "/zh-TW/life/codex-cli-install-windows-guide";
    view.rerender(<AnalyticsProvider><div>content</div></AnalyticsProvider>);
    await waitFor(() => expect(pageViews()).toEqual([
      "/zh-TW/life/claude-code-first-project-setup",
      "/zh-TW/life/codex-cli-install-windows-guide",
    ]));
  });

  it("queues denied consent before GA4 config and sends a sanitized page view", async () => {
    const fetchMock = vi.fn(async (input: RequestInfo | URL, init?: RequestInit) => {
      void init;
      if (String(input).endsWith("/analytics/config")) return new Response(JSON.stringify({ first_party_enabled: true, ga4_enabled: true, ga4_measurement_id: "G-ABCD1234" }));
      return new Response(JSON.stringify({ accepted: 1, enabled: true }), { status: 202 });
    });
    vi.stubGlobal("fetch", fetchMock);
    render(<AnalyticsProvider><div>content</div></AnalyticsProvider>);
    await waitFor(() => expect(fetchMock.mock.calls.some(([url]) => String(url).endsWith("/analytics/events"))).toBe(true));
    const commands = window.dataLayer || [];
    expect(commands.findIndex((row) => row[0] === "consent")).toBeLessThan(commands.findIndex((row) => row[0] === "config"));
    expect(commands.some((row) => row[0] === "event" && row[1] === "page_view")).toBe(true);
    const eventRequest = fetchMock.mock.calls.find(([url]) => String(url).endsWith("/analytics/events"));
    const body = JSON.parse(String(eventRequest?.[1]?.body));
    expect(body.events[0].path).toBe("/zh-TW/hotspots");
    expect(body.events[0]).not.toHaveProperty("user_id");
  });

  it("does not load config when DNT is enabled", async () => {
    Object.defineProperty(navigator, "doNotTrack", { configurable: true, value: "1" });
    const fetchMock = vi.fn();
    vi.stubGlobal("fetch", fetchMock);
    render(<AnalyticsProvider><div>content</div></AnalyticsProvider>);
    await new Promise((resolve) => setTimeout(resolve, 0));
    expect(fetchMock).not.toHaveBeenCalled();
  });

  it("records a social registration once and consumes its short-lived marker", async () => {
    document.cookie = "travel_oauth_registered=1; path=/";
    const fetchMock = vi.fn(async (input: RequestInfo | URL, init?: RequestInit) => {
      void init;
      if (String(input).endsWith("/analytics/config")) return new Response(JSON.stringify({ first_party_enabled: true, ga4_enabled: false }));
      return new Response(JSON.stringify({ accepted: 1, enabled: true }), { status: 202 });
    });
    vi.stubGlobal("fetch", fetchMock);
    render(<AnalyticsProvider><div>content</div></AnalyticsProvider>);
    await waitFor(() => {
      const events = fetchMock.mock.calls
        .filter(([url]) => String(url).endsWith("/analytics/events"))
        .flatMap(([, init]) => JSON.parse(String(init?.body)).events);
      expect(events.some((event: { name: string }) => event.name === "registration_completed")).toBe(true);
    });
    expect(document.cookie).not.toContain("travel_oauth_registered=1");
  });
});
