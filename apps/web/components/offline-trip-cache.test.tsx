import { render, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { OfflineTripCache } from "./offline-trip-cache";

afterEach(() => vi.unstubAllGlobals());

function stubWorker({ controlling = true } = {}) {
  const posted: Array<{ message: unknown; ports: MessagePort[] }> = [];
  const worker = {
    postMessage(message: unknown, ports: MessagePort[] = []) {
      posted.push({ message, ports });
      // The real worker answers on the port once it has a cache name.
      ports[0]?.postMessage({ type: "ready" });
    },
  };
  const events = new EventTarget();
  const container = {
    register: vi.fn(async () => ({ active: worker })),
    ready: Promise.resolve({ active: worker }),
    controller: controlling ? worker : null,
    addEventListener: events.addEventListener.bind(events),
  };
  vi.stubGlobal("navigator", { serviceWorker: container });
  /** What the browser does once the activated worker has claimed this page. */
  const claim = () => {
    container.controller = worker;
    events.dispatchEvent(new Event("controllerchange"));
  };
  return { posted, claim };
}

function stubFetch() {
  const urls: string[] = [];
  vi.stubGlobal("fetch", vi.fn(async (input: RequestInfo | URL) => {
    urls.push(String(input));
    const body = String(input).includes("/auth/me") ? { id: "member-1" } : { id: "trip-1", items: [] };
    return new Response(JSON.stringify(body), { status: 200, headers: { "Content-Type": "application/json" } });
  }));
  return urls;
}

const types = (posted: Array<{ message: unknown }>) => posted.map(({ message }) => (message as { type: string }).type);

describe("OfflineTripCache", () => {
  /**
   * TodayView asks for the trip the moment it mounts, before the worker exists, let
   * alone knows who is signed in — and the worker stores nothing while it has no
   * cache name. So the first online visit cached nothing, and the traveller found
   * an empty page on the platform with no signal.
   */
  it("fetches the trip once the worker has answered, so something is actually cached", async () => {
    const { posted } = stubWorker();
    const urls = stubFetch();

    render(<OfflineTripCache tripId="trip-1" />);

    await waitFor(() => expect(urls.some((url) => url.includes("/trips/trip-1"))).toBe(true));
    expect(posted[0]?.message).toEqual({ type: "signed-in", member: "member-1" });
    // Order matters: a trip fetched before the worker has a name is not stored.
    expect(urls.findIndex((url) => url.includes("/auth/me")))
      .toBeLessThan(urls.findIndex((url) => url.includes("/trips/trip-1")));
  });

  /**
   * A stored trip alone never reached a traveller whose tab had been closed: with no
   * document and no scripts stored, the browser showed its own offline page. The worker
   * keeps the page itself only when asked, and only after it knows whose cache to use.
   */
  it("asks the worker to keep this page after the trip, so a cold open has something to draw", async () => {
    const { posted } = stubWorker();
    const urls = stubFetch();

    render(<OfflineTripCache tripId="trip-1" />);

    await waitFor(() => expect(types(posted)).toEqual(["signed-in", "keep-day"]));
    expect(posted[1]?.message).toEqual({ type: "keep-day", url: window.location.href });
    expect(urls.filter((url) => url.includes("/trips/trip-1"))).toHaveLength(1);
  });

  /**
   * On a first visit the page is not yet controlled when the worker answers, and a trip
   * fetched in that moment goes around the worker and is never stored.
   */
  it("waits until the worker controls the page before fetching the trip", async () => {
    const { posted, claim } = stubWorker({ controlling: false });
    const urls = stubFetch();

    render(<OfflineTripCache tripId="trip-1" />);

    await waitFor(() => expect(types(posted)).toEqual(["signed-in"]));
    await new Promise((resolve) => setTimeout(resolve, 50));
    expect(urls.filter((url) => url.includes("/trips/trip-1"))).toEqual([]);

    claim();

    await waitFor(() => expect(types(posted)).toEqual(["signed-in", "keep-day"]));
    expect(urls.filter((url) => url.includes("/trips/trip-1"))).toHaveLength(1);
  });

  it("still names the member when no trip is on screen, and asks for nothing more", async () => {
    const { posted } = stubWorker();
    const urls = stubFetch();

    render(<OfflineTripCache />);

    await waitFor(() => expect(posted).toHaveLength(1));
    await new Promise((resolve) => setTimeout(resolve, 50));
    expect(types(posted)).toEqual(["signed-in"]);
    expect(urls.filter((url) => url.includes("/trips/"))).toEqual([]);
  });
});
