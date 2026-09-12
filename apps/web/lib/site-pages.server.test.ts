import { afterEach, describe, expect, it, vi } from "vitest";
const { incoming } = vi.hoisted(() => ({ incoming: vi.fn() }));
// The loaders read the visitor's address out of the request so the API can meter reads
// per source. Nothing here depends on the value; it just has to be readable.
vi.mock("next/headers", () => ({ headers: incoming }));
incoming.mockResolvedValue(new Headers({ "x-forwarded-for": "203.0.113.9" }));
import { loadSitePage } from "./site-pages.server";
import { sitePageLink } from "./site-pages";

const document = {
  title: "Confirmed privacy policy", description: "Published summary", blocks: [{ type: "paragraph", text: "Published only" }],
  effective_date: "2026-09-09", requirements: { operator: "Operator", location: "Location", contact: "Contact", retention: "Retention", legal: "Legal" },
  version: 3, published_at: "2026-09-09T00:00:00Z",
};
afterEach(() => { vi.unstubAllGlobals(); vi.unstubAllEnvs(); });
describe("public site page loader", () => {
  it("uses no-store and a bounded request without authentication, preserving locale", async () => {
    const fetch = vi.fn().mockResolvedValue(new Response(JSON.stringify({ slug: "privacy", locale: "ja", status: "published", document })));
    vi.stubGlobal("fetch", fetch); vi.stubEnv("API_INTERNAL_URL", "http://api.test/");
    expect((await loadSitePage("privacy", "ja")).document?.title).toBe(document.title);
    // Matched exactly, not partially: the point of the case is what is absent. No cookie,
    // no authorization -- only the locale and the address the read is metered against.
    expect(fetch).toHaveBeenCalledWith("http://api.test/api/v1/site-pages/privacy?locale=ja", expect.objectContaining({ cache: "no-store", headers: { Accept: "application/json", "X-Travel-Locale": "ja", "X-Travel-Client-IP": "203.0.113.9" }, signal: expect.any(AbortSignal) }));
  });
  it.each([
    { slug: "privacy", locale: "en", status: "draft", document },
    { slug: "privacy", locale: "ja", status: "published", document },
    { slug: "terms", locale: "en", status: "published", document },
    { slug: "privacy", locale: "en", status: "published", document: { ...document, blocks: [{ type: "html", text: "script" }] } },
    { slug: "privacy", locale: "en", status: "published", document: { ...document, blocks: [{ type: "link", text: "unsafe", url: "javascript:alert(1)" }] } },
  ])("does not expose mismatched, draft or invalid documents", async (payload) => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(new Response(JSON.stringify(payload))));
    expect(await loadSitePage("privacy", "en")).toMatchObject({ status: "unavailable", document: null });
  });
  it("distinguishes not published from a failed service without falling back to bundled legal text", async () => {
    const fetch = vi.fn().mockResolvedValueOnce(new Response(JSON.stringify({ slug: "terms", locale: "en", status: "unpublished", document: null }))).mockRejectedValueOnce(new Error("offline"));
    vi.stubGlobal("fetch", fetch);
    expect((await loadSitePage("terms", "en")).status).toBe("unpublished");
    expect((await loadSitePage("terms", "en")).status).toBe("unavailable");
  });
});
describe("information page links", () => {
  it.each(["javascript:alert(1)", "data:text/html,evil", "/relative", "https://user:secret@example.com/", "https://a.test/\nfoo", "mailto:help%0d%0aBcc%3Avictim@example.com", "mailto:help%00@example.com", "mailto:help%C2%85@example.com"])("rejects unsafe URLs: %s", (url) => expect(sitePageLink(url)).toBeNull());
  it("accepts explicit web and email destinations", () => {
    expect(sitePageLink("https://example.com/contact")).toBe("https://example.com/contact");
    expect(sitePageLink("mailto:help@example.com")).toBe("mailto:help@example.com");
  });
});
