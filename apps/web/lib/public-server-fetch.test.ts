import { afterEach, describe, expect, it, vi } from "vitest";
const { incoming } = vi.hoisted(() => ({ incoming: vi.fn() }));
vi.mock("next/headers", () => ({ headers: incoming }));
import { publicServerHeaders } from "./public-server-fetch";

afterEach(() => vi.clearAllMocks());

describe("public server fetch headers", () => {
  it("forwards the visitor's address and agent, so a server render is metered like the browser call it replaces", async () => {
    incoming.mockResolvedValue(new Headers({ "x-forwarded-for": "192.0.2.1, 198.51.100.8", "user-agent": "Mozilla/5.0" }));
    expect(await publicServerHeaders("ja")).toEqual({
      Accept: "application/json",
      "X-Travel-Locale": "ja",
      "X-Travel-Client-IP": "198.51.100.8",
      "X-Travel-User-Agent": "Mozilla/5.0",
    });
  });

  it("carries no credentials, whatever the request arrived with", async () => {
    incoming.mockResolvedValue(new Headers({ cookie: "travel_access=secret", authorization: "Bearer secret", "x-real-ip": "203.0.113.9" }));
    const forwarded = await publicServerHeaders("en");
    expect(Object.keys(forwarded)).toEqual(["Accept", "X-Travel-Locale", "X-Travel-Client-IP"]);
  });

  it("bounds the agent, which is attacker-controlled and arrives verbatim", async () => {
    incoming.mockResolvedValue(new Headers({ "user-agent": "z".repeat(900) }));
    expect((await publicServerHeaders("en"))["X-Travel-User-Agent"]).toHaveLength(512);
  });

  it("omits what was never sent rather than inventing an empty value", async () => {
    incoming.mockResolvedValue(new Headers());
    expect(await publicServerHeaders("ko")).toEqual({ Accept: "application/json", "X-Travel-Locale": "ko" });
  });
});
