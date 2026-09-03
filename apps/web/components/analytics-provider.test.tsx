import { render, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

vi.mock("next/navigation", () => ({ usePathname: () => "/zh-TW/hotspots" }));
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
