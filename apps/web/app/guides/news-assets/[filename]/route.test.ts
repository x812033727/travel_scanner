import { NextRequest } from "next/server";
import { afterEach, describe, expect, it, vi } from "vitest";
import { GET, HEAD } from "./route";

const filename = "0123456789abcdef0123456789abcdef-hero.webp";
const context = (name = filename) => ({ params: Promise.resolve({ filename: name }) });
const page = (name = filename, init?: ConstructorParameters<typeof NextRequest>[1]) =>
  // The production shape: an https URL for a server that speaks plain HTTP behind nginx.
  new NextRequest(`https://localhost:3000/guides/news-assets/${name}`, init);
/** The upstream calls a stubbed `fetch` received, as `[url, init]`. */
const calls = (fetcher: ReturnType<typeof vi.fn>) => fetcher.mock.calls as unknown as [string, RequestInit | undefined][];
const webp = (init: ResponseInit & { body?: BodyInit } = {}) =>
  new Response(init.body ?? new Uint8Array([82, 73, 70, 70]), {
    status: init.status,
    headers: {
      "Content-Type": "image/webp",
      "Cache-Control": "public, max-age=31536000, immutable",
      ETag: '"digest"',
      ...(init.headers as Record<string, string> | undefined),
    },
  });

describe("news asset route", () => {
  afterEach(() => {
    vi.unstubAllGlobals();
    vi.unstubAllEnvs();
  });

  it("reads the asset from API_INTERNAL_URL, never from the request's own origin", async () => {
    vi.stubEnv("API_INTERNAL_URL", "http://api:8000");
    vi.stubEnv("INTERNAL_PROXY_TOKEN", "proxy-token");
    const fetcher = vi.fn(async () => webp());
    vi.stubGlobal("fetch", fetcher);
    const response = await GET(
      page(filename, { headers: { "X-Forwarded-For": "203.0.113.9", "User-Agent": "Reader/1.0" } }),
      context(),
    );
    const [target, init] = calls(fetcher)[0];
    expect(target).toBe(`http://api:8000/api/v1/news-assets/${filename}`);
    expect(init?.method ?? "GET").toBe("GET");
    expect(init?.redirect).toBe("manual");
    const sent = new Headers(init?.headers);
    // Metered against the visitor, as the BFF and the server-rendered pages are.
    expect(sent.get("X-Travel-Client-IP")).toBe("203.0.113.9");
    expect(sent.get("X-Travel-Proxy-Token")).toBe("proxy-token");
    expect(sent.get("X-Travel-User-Agent")).toBe("Reader/1.0");
    expect(sent.get("Cookie")).toBeNull();
    expect(response.status).toBe(200);
    expect(response.headers.get("content-type")).toBe("image/webp");
    expect(response.headers.get("cache-control")).toBe("public, max-age=31536000, immutable");
    expect(response.headers.get("etag")).toBe('"digest"');
    expect(response.headers.get("x-content-type-options")).toBe("nosniff");
    expect([...new Uint8Array(await response.arrayBuffer())]).toEqual([82, 73, 70, 70]);
  });

  it("falls back to the local API when API_INTERNAL_URL is unset", async () => {
    vi.stubEnv("API_INTERNAL_URL", "");
    const fetcher = vi.fn(async () => webp());
    vi.stubGlobal("fetch", fetcher);
    await GET(page(), context());
    expect(calls(fetcher)[0][0]).toBe(`http://localhost:8000/api/v1/news-assets/${filename}`);
  });

  it("serves the SVG diagrams with their own type", async () => {
    const name = "0123456789abcdef0123456789abcdef-diagram-zh-tw.svg";
    vi.stubGlobal("fetch", vi.fn(async () => new Response("<svg/>", {
      headers: { "Content-Type": "image/svg+xml; charset=utf-8" },
    })));
    const response = await GET(page(name), context(name));
    expect(response.status).toBe(200);
    expect(response.headers.get("content-type")).toBe("image/svg+xml");
    expect(await response.text()).toBe("<svg/>");
  });

  it("passes a missing asset's 404 through without the API's body", async () => {
    vi.stubGlobal("fetch", vi.fn(async () => Response.json(
      { code: "news_asset_not_found" },
      { status: 404, headers: { "Cache-Control": "public, max-age=60" } },
    )));
    const response = await GET(page(), context());
    expect(response.status).toBe(404);
    expect(response.headers.get("cache-control")).toBe("no-store");
    expect(await response.text()).toBe("");
  });

  it("does not follow or pass on an upstream redirect", async () => {
    vi.stubGlobal("fetch", vi.fn(async () => new Response(null, {
      status: 302, headers: { Location: "https://elsewhere.example/hero.webp" },
    })));
    const response = await GET(page(), context());
    expect(response.status).toBe(502);
    expect(response.headers.get("location")).toBeNull();
  });

  it("refuses a type outside the image allow-list", async () => {
    vi.stubGlobal("fetch", vi.fn(async () => new Response("<script>alert(1)</script>", {
      headers: { "Content-Type": "text/html" },
    })));
    const response = await GET(page(), context());
    expect(response.status).toBe(502);
    expect(await response.text()).toBe("");
  });

  it("answers 502 instead of throwing when the API cannot be reached", async () => {
    vi.stubGlobal("fetch", vi.fn(async () => {
      throw new TypeError("fetch failed", { cause: { code: "ERR_SSL_WRONG_VERSION_NUMBER" } });
    }));
    const response = await GET(page(), context());
    expect(response.status).toBe(502);
    expect(response.headers.get("cache-control")).toBe("no-store");
  });

  it("refuses an asset over 5 MiB, declared or not", async () => {
    vi.stubGlobal("fetch", vi.fn(async () => webp({
      body: new Uint8Array(),
      headers: { "Content-Length": String(5 * 1024 * 1024 + 1) },
    })));
    expect((await GET(page(), context())).status).toBe(502);

    const chunk = new Uint8Array(1024 * 1024);
    const stream = new ReadableStream<Uint8Array>({
      start(controller) {
        for (let index = 0; index < 6; index += 1) controller.enqueue(chunk);
        controller.close();
      },
    });
    vi.stubGlobal("fetch", vi.fn(async () => webp({ body: stream })));
    expect((await GET(page(), context())).status).toBe(502);
  });

  it("answers HEAD through the same GET and checks, without a body", async () => {
    const fetcher = vi.fn(async () => webp());
    vi.stubGlobal("fetch", fetcher);
    const response = await HEAD(page(filename, { method: "HEAD" }), context());
    expect(calls(fetcher)[0][1]?.method ?? "GET").toBe("GET");
    expect(response.status).toBe(200);
    expect(response.headers.get("content-type")).toBe("image/webp");
    expect((await response.arrayBuffer()).byteLength).toBe(0);

    vi.stubGlobal("fetch", vi.fn(async () => new Response("{}", { headers: { "Content-Type": "application/json" } })));
    expect((await HEAD(page(filename, { method: "HEAD" }), context())).status).toBe(502);
  });

  it("answers 404 for a name outside the pattern without asking the API", async () => {
    const fetcher = vi.fn();
    vi.stubGlobal("fetch", fetcher);
    for (const name of ["Hero.webp", "hero.png", "..%2Fsecret.webp", "-hero.webp", `${"a".repeat(161)}.webp`]) {
      expect((await GET(page(encodeURIComponent(name)), context(name))).status).toBe(404);
    }
    expect(fetcher).not.toHaveBeenCalled();
  });
});
