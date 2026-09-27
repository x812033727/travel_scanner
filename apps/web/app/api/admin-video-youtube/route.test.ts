import { NextRequest } from "next/server";
import { afterEach, describe, expect, it, vi } from "vitest";
import { siteUrl } from "@/lib/seo";
import { encodeFlow, FLOW_COOKIE } from "./_shared";
import { GET as callback } from "./callback/route";
import { GET as start } from "./start/route";

// Behind the reverse proxy the request reaches Next at the container's bind address; every
// redirect must be built on the public site URL instead.
const BIND = "https://0.0.0.0:3000/api/admin-video-youtube";
const publicOrigin = new URL(siteUrl).origin;
const AUTHORIZE = "https://accounts.google.com/o/oauth2/v2/auth?client_id=x&state=s";

function request(path: string, cookies: Record<string, string> = {}) {
  const headers = new Headers();
  const cookie = Object.entries(cookies).map(([name, value]) => `${name}=${value}`).join("; ");
  if (cookie) headers.set("cookie", cookie);
  return new NextRequest(`${BIND}${path}`, { headers });
}

function outcome(response: Response) {
  const location = new URL(response.headers.get("location") ?? "");
  return { origin: location.origin, path: location.pathname, tab: location.searchParams.get("tab"), linked: location.searchParams.get("youtube"), error: location.searchParams.get("youtube_error") };
}

afterEach(() => {
  vi.unstubAllGlobals();
});

describe("starting the link", () => {
  it("opens a flow with the admin's session, keeps it in a cookie scoped to these routes, and goes to Google", async () => {
    const fetchMock = vi.fn().mockResolvedValue(Response.json({ authorization_url: AUTHORIZE, flow_id: "flow-1", state: "state-1", expires_in: 600 }));
    vi.stubGlobal("fetch", fetchMock);
    const response = await start(request("/start?locale=ja", { travel_access: "session", admin_step_up: "step" }));
    expect(response.headers.get("location")).toBe(AUTHORIZE);
    const [url, init] = fetchMock.mock.calls[0] as [string, RequestInit];
    expect(url).toMatch(/\/api\/v1\/admin\/video-youtube\/oauth\/start$/);
    expect(new Headers(init.headers).get("cookie")).toBe("travel_access=session; admin_step_up=step");
    const binding = JSON.parse(String(init.body)).browser_binding as string;
    expect(binding.length).toBeGreaterThanOrEqual(32);
    const flow = response.headers.get("set-cookie") ?? "";
    expect(flow).toContain(`${FLOW_COOKIE}=`);
    expect(flow).toContain("Path=/api/admin-video-youtube");
    expect(flow).toContain("HttpOnly");
    expect(flow.toLowerCase()).toContain("samesite=lax");
  });

  it("sends a signed-out browser back to the settings tab without asking the API", async () => {
    const fetchMock = vi.fn();
    vi.stubGlobal("fetch", fetchMock);
    expect(outcome(await start(request("/start?locale=en")))).toEqual({ origin: publicOrigin, path: "/en/admin/videos", tab: "settings", linked: null, error: "authentication_required" });
    expect(fetchMock).not.toHaveBeenCalled();
  });

  it("returns a refusal's code, and never follows an address that is not Google's consent screen", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(Response.json({ code: "video_youtube_client_missing" }, { status: 409 })));
    expect(outcome(await start(request("/start?locale=zh-TW", { travel_access: "s" }))).error).toBe("video_youtube_client_missing");
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(Response.json({ authorization_url: "https://evil.example/auth", flow_id: "f", state: "s" })));
    expect(outcome(await start(request("/start?locale=zh-TW", { travel_access: "s" }))).error).toBe("video_youtube_unavailable");
    vi.stubGlobal("fetch", vi.fn().mockRejectedValue(new Error("connection refused")));
    expect(outcome(await start(request("/start?locale=zh-TW", { travel_access: "s" }))).error).toBe("video_youtube_unavailable");
  });
});

describe("coming back from Google", () => {
  const flow = encodeFlow({ flowId: "flow-1", state: "state-1", binding: "b".repeat(43), locale: "ko" });

  it("hands the code and the binding to the API, lands on the settings tab, and drops the flow cookie", async () => {
    const fetchMock = vi.fn().mockResolvedValue(Response.json({ linked: true }));
    vi.stubGlobal("fetch", fetchMock);
    const response = await callback(request("/callback?code=the-code&state=state-1", { [FLOW_COOKIE]: flow, travel_access: "session" }));
    expect(outcome(response)).toEqual({ origin: publicOrigin, path: "/ko/admin/videos", tab: "settings", linked: "linked", error: null });
    const [url, init] = fetchMock.mock.calls[0] as [string, RequestInit];
    expect(url).toMatch(/\/api\/v1\/admin\/video-youtube\/oauth\/exchange$/);
    expect(JSON.parse(String(init.body))).toEqual({ flow_id: "flow-1", state: "state-1", code: "the-code", browser_binding: "b".repeat(43) });
    const cleared = response.headers.get("set-cookie") ?? "";
    expect(cleared).toContain(`${FLOW_COOKIE}=;`);
    expect(cleared).toContain("Path=/api/admin-video-youtube");
  });

  it("says the owner cancelled, and refuses a state this browser did not start", async () => {
    const fetchMock = vi.fn();
    vi.stubGlobal("fetch", fetchMock);
    expect(outcome(await callback(request("/callback?error=access_denied&state=state-1", { [FLOW_COOKIE]: flow }))).error).toBe("video_youtube_cancelled");
    expect(outcome(await callback(request("/callback?code=c&state=other", { [FLOW_COOKIE]: flow }))).error).toBe("video_youtube_state_invalid");
    expect(outcome(await callback(request("/callback?code=c&state=state-1"))).error).toBe("video_youtube_state_invalid");
    expect(fetchMock).not.toHaveBeenCalled();
  });

  it("passes the API's refusal code through, and only a well-formed one", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(Response.json({ code: "video_youtube_no_channel" }, { status: 422 })));
    expect(outcome(await callback(request("/callback?code=c&state=state-1", { [FLOW_COOKIE]: flow }))).error).toBe("video_youtube_no_channel");
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(Response.json({ code: "<script>" }, { status: 422 })));
    expect(outcome(await callback(request("/callback?code=c&state=state-1", { [FLOW_COOKIE]: flow }))).error).toBe("video_youtube_unavailable");
  });
});
