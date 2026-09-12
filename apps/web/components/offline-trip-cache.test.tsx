import { render, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { OfflineTripCache } from "./offline-trip-cache";

afterEach(() => vi.unstubAllGlobals());

function stubWorker() {
  const posted: Array<{ message: unknown; ports: MessagePort[] }> = [];
  const worker = {
    postMessage(message: unknown, ports: MessagePort[] = []) {
      posted.push({ message, ports });
      // The real worker answers on the port once it has a cache name.
      ports[0]?.postMessage({ type: "ready" });
    },
  };
  vi.stubGlobal("navigator", {
    serviceWorker: {
      register: vi.fn(async () => ({ active: worker })),
      ready: Promise.resolve({ active: worker }),
      controller: worker,
    },
  });
  return posted;
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

describe("OfflineTripCache", () => {
  /**
   * TodayView asks for the trip the moment it mounts, before the worker exists, let
   * alone knows who is signed in — and the worker stores nothing while it has no
   * cache name. So the first online visit cached nothing, and the traveller found
   * an empty page on the platform with no signal.
   */
  it("fetches the trip once the worker has answered, so something is actually cached", async () => {
    const posted = stubWorker();
    const urls = stubFetch();

    render(<OfflineTripCache tripId="trip-1" />);

    await waitFor(() => expect(urls.some((url) => url.includes("/trips/trip-1"))).toBe(true));
    const message = posted.at(-1)?.message as { type: string; member: string };
    expect(message).toEqual({ type: "signed-in", member: "member-1" });
    // Order matters: a trip fetched before the worker has a name is not stored.
    expect(urls.findIndex((url) => url.includes("/auth/me")))
      .toBeLessThan(urls.findIndex((url) => url.includes("/trips/trip-1")));
  });

  it("still names the member when no trip is on screen, and asks for nothing more", async () => {
    const posted = stubWorker();
    const urls = stubFetch();

    render(<OfflineTripCache />);

    await waitFor(() => expect(posted).toHaveLength(1));
    expect(urls.filter((url) => url.includes("/trips/"))).toEqual([]);
  });
});
