import { renderHook, waitFor } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { savedTripsAtCapacity, useAccountUsage } from "./usage-catalog-provider";

const summary = {
  remaining_uses: 5,
  reserved_uses: 1,
  available_uses: 4,
  limits: { saved_trips: 20, price_alerts: 20 },
  counts: { saved_trips: 20, price_alerts: 2 },
};

function stub(value: unknown, status = 200) {
  vi.stubGlobal("fetch", vi.fn(() => Promise.resolve(
    new Response(JSON.stringify(value), { status, headers: { "Content-Type": "application/json" } }),
  )));
}

describe("useAccountUsage", () => {
  beforeEach(() => vi.unstubAllGlobals());

  it("reads the balance, the cap and the current count from one request", async () => {
    stub(summary);
    const { result } = renderHook(() => useAccountUsage());

    await waitFor(() => expect(result.current.status).toBe("ready"));
    expect(result.current.availableUses).toBe(4);
    expect(result.current.savedTrips).toBe(20);
    expect(result.current.savedTripLimit).toBe(20);
    expect(vi.mocked(fetch)).toHaveBeenCalledTimes(1);
  });

  it("asks nobody about a member who is not signed in", async () => {
    stub(summary);
    const { result } = renderHook(() => useAccountUsage(false));

    expect(vi.mocked(fetch)).not.toHaveBeenCalled();
    expect(result.current.status).toBe("loading");
  });

  it("reports the summary as unavailable rather than guessing at a balance", async () => {
    vi.stubGlobal("fetch", vi.fn(() => Promise.reject(new Error("offline"))));
    const { result } = renderHook(() => useAccountUsage());

    await waitFor(() => expect(result.current.status).toBe("unavailable"));
    expect(result.current.availableUses).toBeNull();
  });
});

describe("savedTripsAtCapacity", () => {
  it("is true only when the cap is known and reached", () => {
    const ready = { status: "ready" as const, availableUses: 4, savedTrips: 20, savedTripLimit: 20 };
    expect(savedTripsAtCapacity(ready)).toBe(true);
    expect(savedTripsAtCapacity({ ...ready, savedTrips: 19 })).toBe(false);
    // An unreadable summary must never block the form: the server enforces the cap.
    expect(savedTripsAtCapacity({ status: "unavailable", availableUses: null, savedTrips: null, savedTripLimit: null })).toBe(false);
    expect(savedTripsAtCapacity({ status: "loading", availableUses: null, savedTrips: null, savedTripLimit: null })).toBe(false);
  });
});
