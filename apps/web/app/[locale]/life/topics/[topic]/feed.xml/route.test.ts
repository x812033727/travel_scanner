import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { GET } from "./route";
import { locales } from "@/i18n/routing";
import { siteUrl } from "@/lib/seo";

const mocks = vi.hoisted(() => ({ list: vi.fn(), vocabulary: vi.fn() }));
vi.mock("@/lib/guides.server", () => ({ getGuideList: mocks.list, getGuideTopicList: mocks.vocabulary }));
const article = (over: Record<string, unknown> = {}) => ({
  slug: "new-tool", kind: "life", title: "A new tool", description: "What changed",
  published_at: "2026-11-09T10:00:00Z", valid_until: null, ...over,
});
const request = (locale = "zh-TW", topic = "ai-news") => GET(new Request(`${siteUrl}/${locale}/life/topics/${topic}/feed.xml`), { params: Promise.resolve({ locale, topic }) });
beforeEach(() => {
  vi.clearAllMocks();
  vi.useFakeTimers();
  vi.setSystemTime("2026-11-10T12:00:00Z");
  mocks.list.mockResolvedValue({ articles: [article()], available: true, next_cursor: null });
  mocks.vocabulary.mockResolvedValue({ topics: [{ slug: "ai-news", label: "AI news" }, { slug: "crypto", label: "Crypto" }, { slug: "tech-news", label: "Tech" }], available: true });
});
afterEach(() => vi.useRealTimers());

describe("localized news-topic Atom subscriptions", () => {
  it.each(locales)("requests and links only %s in a well-formed Atom feed", async (locale) => {
    const response = await request(locale);
    const body = await response.text();
    const xml = new DOMParser().parseFromString(body, "application/xml");
    expect(response.status).toBe(200);
    expect(response.headers.get("Content-Type")).toBe("application/atom+xml; charset=utf-8");
    expect(response.headers.get("Content-Language")).toBe(locale);
    expect(xml.querySelector("parsererror")).toBeNull();
    expect(xml.documentElement.namespaceURI).toBe("http://www.w3.org/2005/Atom");
    expect(xml.documentElement.getAttribute("xml:lang")).toBe(locale);
    expect(xml.querySelector("feed > author > name")?.textContent).toBe("Mokaair");
    expect(xml.querySelector("feed > id")?.textContent).toBe(`${siteUrl}/${locale}/life/topics/ai-news/feed.xml`);
    expect(xml.querySelector("entry > id")?.textContent).toBe(`${siteUrl}/${locale}/life/new-tool`);
    expect(xml.querySelector('entry > link[rel="alternate"]')?.getAttribute("href")).toBe(`${siteUrl}/${locale}/life/new-tool`);
    expect(mocks.list).toHaveBeenCalledWith(locale, { section: "life", topic: "ai-news", sort: "latest" }, 30);
    expect(mocks.vocabulary).toHaveBeenCalledWith(locale, "life");
    expect(xml.querySelector("feed > updated")?.textContent).toBe("2026-11-09T10:00:00.000Z");
  });

  it.each(["ai-news", "crypto", "tech-news"])("supports the existing %s news topic", async (topic) => {
    expect((await request("en", topic)).status).toBe(200);
    expect(mocks.list).toHaveBeenCalledWith("en", expect.objectContaining({ topic }), 30);
  });

  it.each([["fr", "ai-news"], ["zh-TW", "ai-terms"], ["en", "unknown"], ["en", "../ai-news"]])("rejects invalid locale/topic %s/%s before any API read", async (locale, topic) => {
    expect((await request(locale, topic)).status).toBe(404);
    expect(mocks.list).not.toHaveBeenCalled();
    expect(mocks.vocabulary).not.toHaveBeenCalled();
  });

  it("escapes XML text and removes illegal controls while preserving emoji", async () => {
    mocks.list.mockResolvedValue({ articles: [article({ title: 'A & B <script>"test"</script>\u0001 🗺️', description: "Less < more & \uD800" })], available: true });
    const body = await (await request()).text();
    const xml = new DOMParser().parseFromString(body, "application/xml");
    expect(xml.querySelector("parsererror")).toBeNull();
    expect(xml.querySelector("entry > title")?.textContent).toBe('A & B <script>"test"</script> 🗺️');
    expect(xml.querySelector("entry > summary")?.textContent).toBe("Less < more & ");
    expect(body).not.toContain("<script>");
  });

  it("sorts by publication and keeps stable IDs on a later poll", async () => {
    mocks.list.mockResolvedValue({ articles: [article({ slug: "older", published_at: "2026-10-01T00:00:00Z", news_date: "2026-11-10" }), article()], available: true });
    const first = await (await request()).text();
    vi.setSystemTime("2026-11-10T13:00:00Z");
    const second = await (await request()).text();
    expect(first).toBe(second);
    const xml = new DOMParser().parseFromString(first, "application/xml");
    expect([...xml.querySelectorAll("entry > id")].map((node) => node.textContent)).toEqual([`${siteUrl}/zh-TW/life/new-tool`, `${siteUrl}/zh-TW/life/older`]);
  });

  it("keeps the public validity boundary: yesterday excluded, today included", async () => {
    mocks.list.mockResolvedValue({ articles: [article({ slug: "expired", valid_until: "2026-11-09" }), article({ slug: "today", valid_until: "2026-11-10" })], available: true });
    const body = await (await request()).text();
    expect(body).not.toContain("/life/expired");
    expect(body).toContain("/life/today");
  });

  it("bounds a feed to 30 entries even if an API returns more", async () => {
    mocks.list.mockResolvedValue({ articles: Array.from({ length: 40 }, (_, n) => article({ slug: `entry-${n}` })), available: true });
    const xml = new DOMParser().parseFromString(await (await request()).text(), "application/xml");
    expect(xml.querySelectorAll("entry")).toHaveLength(30);
  });

  it.each(["list", "vocabulary"])("returns 503 when %s is unavailable", async (part) => {
    mocks[part as "list" | "vocabulary"].mockResolvedValue({ articles: [], topics: [], available: false });
    const response = await request();
    expect(response.status).toBe(503);
    expect(response.headers.get("Retry-After")).toBe("600");
    expect(response.headers.get("Cache-Control")).toBe("no-store");
  });

  it("returns 503 on a thrown read or invalid publication date instead of inventing a date", async () => {
    mocks.list.mockRejectedValueOnce(new Error("upstream down"));
    expect((await request()).status).toBe(503);
    mocks.list.mockResolvedValue({ articles: [article({ published_at: "invalid" })], available: true });
    expect((await request()).status).toBe(503);
  });

  it("distinguishes a genuine empty topic from an unknown topic", async () => {
    mocks.list.mockResolvedValue({ articles: [], available: true });
    const response = await request();
    const xml = new DOMParser().parseFromString(await response.text(), "application/xml");
    expect(response.status).toBe(200);
    expect(xml.querySelectorAll("entry")).toHaveLength(0);
    expect(xml.querySelector("feed > updated")).not.toBeNull();
    mocks.vocabulary.mockResolvedValue({ topics: [], available: true });
    expect((await request()).status).toBe(404);
  });
});
