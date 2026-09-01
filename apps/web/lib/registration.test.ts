import { afterEach, describe, expect, it, vi } from "vitest";
import { getRegistrationAvailability } from "./registration";

afterEach(() => vi.unstubAllGlobals());

describe("getRegistrationAvailability", () => {
  it.each([
    [true, "open"],
    [false, "closed"],
  ] as const)("maps registration_enabled=%s to %s without caching", async (enabled, expected) => {
    const fetchMock = vi.fn().mockResolvedValue(
      new Response(JSON.stringify({ registration_enabled: enabled }), { status: 200 }),
    );
    vi.stubGlobal("fetch", fetchMock);

    await expect(getRegistrationAvailability()).resolves.toBe(expected);
    expect(fetchMock).toHaveBeenCalledWith(
      "http://localhost:8000/api/v1/auth/registration-status",
      expect.objectContaining({ cache: "no-store" }),
    );
  });

  it("fails closed when the status service errors or returns an invalid payload", async () => {
    vi.stubGlobal("fetch", vi.fn().mockRejectedValue(new Error("offline")));
    await expect(getRegistrationAvailability()).resolves.toBe("unavailable");

    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(
      new Response(JSON.stringify({ registration_enabled: "yes" }), { status: 200 }),
    ));
    await expect(getRegistrationAvailability()).resolves.toBe("unavailable");
  });
});
