import { afterEach, describe, expect, it, vi } from "vitest";
import { NextRequest } from "next/server";
import { POST } from "./route";

vi.mock("next/headers", () => ({ cookies: async () => ({ get: () => undefined }) }));
afterEach(() => vi.unstubAllGlobals());
const id = "00000000-0000-4000-8000-000000000001";
const path = ["travel-services", id, "booking-options", id, "clickout"];
function request(accept = "text/html") {
  return new NextRequest(`https://mokaair.test/api/travel/${path.join("/")}?locale=en&placement=trip&return_to=%2Fen%2Ftrips%2Fprivate-id`, {
    method: "POST", headers: { origin: "https://mokaair.test", accept, "content-type": "application/x-www-form-urlencoded", "sec-gpc": "1", dnt: "1", referer: "https://mokaair.test/en/trips/a?tab=stay" },
    body: "check_in=2030-11-01&check_out=2030-11-30&adults=2&children=0",
  });
}
describe("booking-option error boundary", () => {
  it("returns useful HTML for failed browser forms, not raw provider details", async () => {
    vi.stubGlobal("fetch", vi.fn(async () => Response.json({ detail: "secret upstream trace" }, { status: 422 })));
    const response = await POST(request(), { params: Promise.resolve({ path }) });
    const html = await response.text();
    expect(response.status).toBe(422);
    expect(response.headers.get("content-type")).toContain("text/html");
    expect(html).toContain('value="2030-11-30"');
    expect(html).not.toContain("secret upstream trace");
  });
  it("leaves JSON clients on the existing Problem Details contract", async () => {
    vi.stubGlobal("fetch", vi.fn(async () => Response.json({ code: "service_unavailable" }, { status: 404 })));
    const response = await POST(request("application/json"), { params: Promise.resolve({ path }) });
    expect(await response.json()).toEqual({ code: "service_unavailable" });
  });
  it("preserves approved 303 without following affiliate redirects, forwards privacy signals", async () => {
    const fetcher = vi.fn(async () => new Response(null, { status: 303, headers: { location: "https://www.booking.com/hotel/jp/fixture.html" } }));
    vi.stubGlobal("fetch", fetcher);
    const response = await POST(request(), { params: Promise.resolve({ path }) });
    expect(response.status).toBe(303);
    expect(response.headers.get("referrer-policy")).toBe("no-referrer");
    expect(fetcher).toHaveBeenCalledTimes(1);
    const options = (fetcher.mock.calls as unknown as [string, RequestInit][])[0][1];
    expect((fetcher.mock.calls as unknown as [string, RequestInit][])[0][0]).not.toContain("private-id");
    expect((fetcher.mock.calls as unknown as [string, RequestInit][])[0][0]).not.toContain("return_to");
    expect(options.redirect).toBe("manual");
    expect(new Headers(options.headers).get("sec-gpc")).toBe("1");
    expect(new Headers(options.headers).get("dnt")).toBe("1");
  });
  it("offers retry even when upstream is offline", async () => {
    vi.stubGlobal("fetch", vi.fn(async () => { throw new Error("offline"); }));
    const response = await POST(request(), { params: Promise.resolve({ path }) });
    expect(response.status).toBe(502);
    expect(await response.text()).toContain("Retry opening the platform");
  });
});
