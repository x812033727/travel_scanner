import { render, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

const navigation = vi.hoisted(() => ({ pathname: "/zh-TW/hotspots" }));
vi.mock("next/navigation", () => ({ usePathname: () => navigation.pathname }));
vi.mock("next/script", () => ({ default: (props: { src?: string }) => <script data-src={props.src} /> }));

import { AnalyticsProvider } from "./analytics-provider";

describe("AnalyticsProvider", () => {
  afterEach(() => {
    vi.unstubAllGlobals();
    sessionStorage.clear();
    window.dataLayer = undefined;
    window.gtag = undefined;
    document.cookie = "travel_oauth_registered=; path=/; max-age=0";
    Object.defineProperty(navigator, "doNotTrack", { configurable: true, value: null });
    navigation.pathname = "/zh-TW/hotspots";
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
