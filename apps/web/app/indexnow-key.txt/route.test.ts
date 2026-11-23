import { afterEach, describe, expect, it, vi } from "vitest";
import { dynamic, GET, HEAD } from "./route";

afterEach(() => vi.unstubAllEnvs());

describe("/indexnow-key.txt", () => {
  it("is evaluated per request and returns 404 when unconfigured or malformed", async () => {
    expect(dynamic).toBe("force-dynamic");
    vi.stubEnv("INDEXNOW_KEY", "");
    expect((await GET()).status).toBe(404);
    expect((await HEAD()).status).toBe(404);

    vi.stubEnv("INDEXNOW_KEY", "bad key!");
    expect((await GET()).status).toBe(404);
  });

  it("serves the configured IndexNow verification key as plain text for GET and HEAD", async () => {
    vi.stubEnv("INDEXNOW_KEY", "  a1b2c3d4e5f60718293a4b5c6d7e8f90  ");
    const response = await GET();
    expect(response.status).toBe(200);
    expect(response.headers.get("content-type")).toBe("text/plain; charset=utf-8");
    expect(response.headers.get("cache-control")).toBe("public, max-age=3600");
    expect(await response.text()).toBe("a1b2c3d4e5f60718293a4b5c6d7e8f90");

    const head = await HEAD();
    expect(head.status).toBe(200);
    expect(head.headers.get("content-type")).toBe("text/plain; charset=utf-8");
  });
});
