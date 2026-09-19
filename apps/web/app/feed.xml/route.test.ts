import { beforeEach, describe, expect, it, vi } from "vitest";

import { GET } from "./route";

const lists = vi.hoisted(() => ({
  travel: { articles: [] as unknown[], next_cursor: null, available: true },
  life: { articles: [] as unknown[], next_cursor: null, available: true },
}));

vi.mock("@/lib/guides.server", () => ({
  getGuideList: async (_locale: string, filters: { section?: "travel" | "life" }) =>
    filters.section === "life" ? lists.life : lists.travel,
}));

const article = (over: Record<string, unknown>) => ({
  slug: "a", kind: "howto", destination_id: null, destination_label: null, topics: [],
  title: "T", description: "D", published_at: "2026-09-01T00:00:00Z", valid_until: null,
  featured: false, ...over,
});

beforeEach(() => {
  lists.travel = { articles: [], next_cursor: null, available: true };
  lists.life = { articles: [], next_cursor: null, available: true };
});

describe("/feed.xml", () => {
  it("merges both sections newest first", async () => {
    lists.travel.articles = [article({ slug: "older", title: "Older", published_at: "2026-09-01T00:00:00Z" })];
    lists.life.articles = [article({ slug: "newer", kind: "life", title: "Newer", published_at: "2026-09-18T00:00:00Z" })];

    const body = await (await GET()).text();
    expect(body.indexOf("Newer")).toBeLessThan(body.indexOf("Older"));
    // Each kind builds its own URL shape.
    expect(body).toContain("/zh-TW/life/newer");
    expect(body).toContain("/zh-TW/guides/howto/older");
    // The feed's own timestamp is the newest article's, not "now".
    expect(body).toContain("<updated>2026-09-18T00:00:00.000Z</updated>");
  });

  it("escapes text and attributes so one bad title cannot break the file", async () => {
    lists.travel.articles = [article({
      slug: "x", title: 'Tokyo & Kyoto <b>"best"</b>', description: "a & b",
    })];

    const body = await (await GET()).text();
    expect(body).toContain("<title>Tokyo &amp; Kyoto &lt;b&gt;&quot;best&quot;&lt;/b&gt;</title>");
    expect(body).toContain("<summary>a &amp; b</summary>");
    expect(body).not.toContain("<b>");
  });

  it("answers 503 rather than an empty feed when a read fails", async () => {
    // An empty 200 would tell a poller there is nothing new, which is a thing this handler
    // does not know when the API did not answer.
    lists.life = { articles: [], next_cursor: null, available: false };

    const response = await GET();
    expect(response.status).toBe(503);
    expect(response.headers.get("Retry-After")).toBe("600");
  });

  it("serves a valid empty feed when there genuinely are no articles", async () => {
    const response = await GET();
    const body = await response.text();
    expect(response.status).toBe(200);
    expect(response.headers.get("Content-Type")).toBe("application/atom+xml; charset=utf-8");
    expect(body).toContain('<feed xmlns="http://www.w3.org/2005/Atom">');
    expect(body).toContain('<link rel="self" href=');
    expect(body).not.toContain("<entry>");
  });
});
