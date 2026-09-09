import { cleanup, render, screen, within } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import type { DiscoveryItem } from "@/lib/discovery";
import { getDiscoveryCopy } from "@/lib/discovery-copy";
import { getFrontendFlowCopy } from "@/lib/frontend-flow-copy";
import { DiscoveryCard, DiscoveryDetails } from "./card";

const mock = vi.hoisted(() => ({ locale: "zh-TW", detail: undefined as DiscoveryItem | undefined }));
vi.mock("next-intl", () => ({ useLocale: () => mock.locale, useTranslations: () => (key: string) => key }));
vi.mock("next/navigation", () => ({ useSearchParams: () => new URLSearchParams("destination=taipei&q=walk") }));
vi.mock("@/i18n/navigation", () => ({
  usePathname: () => "/explore",
  Link: ({ href, children, scroll, ...props }: React.AnchorHTMLAttributes<HTMLAnchorElement> & { href: string; scroll?: boolean }) => {
    void scroll; return <a href={href} {...props}>{children}</a>;
  },
}));
vi.mock("@/components/community/provider", () => ({ useCommunity: () => ({ flags: { enabled: false } }) }));
vi.mock("./saved-content-action", () => ({ SavedContentAction: () => <button>Save fixture</button> }));
vi.mock("@/components/travel-card-actions", () => ({ TravelPlanAction: () => <button>Plan fixture</button> }));
vi.mock("@/lib/discovery", async (original) => ({
  ...await original<typeof import("@/lib/discovery")>(),
  useDiscoveryResource: () => ({ data: mock.detail, error: undefined, reload: vi.fn() }),
}));

const item: DiscoveryItem = {
  id: "hotspot:11111111-1111-4111-8111-111111111111", kind: "hotspot", title: "A sourced city walk",
  summary: "Existing public content", locale: "zh-TW", href: "/explore?content=hotspot%3A11111111-1111-4111-8111-111111111111",
  destination: { id: "taipei", name: "台北" }, source: { kind: "editorial", label: "City", url: null },
  published_at: null, updated_at: null, thumbnail_url: null,
};
const topic = (id: string, label: string) => ({ id, label });
function guide(id: string, url: string | null, label = "City tourism"): DiscoveryItem {
  return { ...item, id: `guide:${id}`, kind: "article", title: `Guide ${id}`, source: { kind: "editorial", label, url } };
}
function detail(guides: DiscoveryItem[] = []) {
  return { ...item, detail: { guides, merchants: [], place: {
    status: "ready" as const, address: "Verified address", opening_hours: { weekday_descriptions: ["Monday 09:00–18:00"] },
    coordinates: { latitude: 25.033, longitude: 121.5654, source: "wikidata" },
    google_maps_url: "https://maps.google.com/?q=25.033,121.5654", official_website_url: "https://city.example.test/official",
  } } };
}
beforeEach(() => { mock.locale = "zh-TW"; mock.detail = detail(); });
afterEach(cleanup);

describe("compact discovery cards", () => {
  it.each([null, "", "javascript:alert(1)", "http://images.example.test/photo.jpg", "/photo.jpg"])("omits the entire media link without an authorized image: %s", (thumbnail_url) => {
    const { container } = render(<DiscoveryCard item={{ ...item, thumbnail_url }} />);
    expect(screen.queryByRole("img")).toBeNull();
    expect(container.querySelector("article > a")).toBeNull();
    expect(screen.getAllByRole("link")).toHaveLength(1);
    const title = screen.getByRole("link", { name: item.title });
    expect(title.getAttribute("href")).toBe("/explore?destination=taipei&q=walk&content=hotspot%3A11111111-1111-4111-8111-111111111111");
    expect(screen.getAllByRole("button")).toHaveLength(2);
  });
  it("retains a lazy authorized photo and both meaningful detail links", () => {
    const { container } = render(<DiscoveryCard item={{ ...item, thumbnail_url: "https://images.example.test/photo.jpg" }} />);
    const image = screen.getByRole("img", { name: item.title });
    expect(image.getAttribute("loading")).toBe("lazy");
    expect(image.getAttribute("referrerpolicy")).toBe("no-referrer");
    expect(container.querySelector("article > a")?.contains(image)).toBe(true);
    expect(screen.getAllByRole("link")).toHaveLength(2);
  });
  it.each([undefined, []])("does not invent topics or append an empty separator: %j", (display_topics) => {
    const { container } = render(<DiscoveryCard item={{ ...item, display_topics, topics: ["unknown_raw_slug"] }} />);
    expect(container.querySelector("article p")?.textContent).toBe("台北·景點");
    expect(screen.queryByText("unknown_raw_slug")).toBeNull();
  });
  it.each([1, 2])("shows %i labels without a remaining count", (count) => {
    const display_topics = [topic("category:culture", "文化"), topic("theme:sakura", "賞櫻")].slice(0, count);
    const { container } = render(<DiscoveryCard item={{ ...item, display_topics }} />);
    const meta = container.querySelector("article p")!;
    for (const entry of display_topics) expect(within(meta as HTMLElement).getByText(entry.label)).toBeTruthy();
    expect(meta.textContent).not.toContain("+");
  });
  it("deduplicates kinds, labels and IDs and shows every topic without truncation", () => {
    const display_topics = [topic("kind", "景點"), topic("blank", " "), topic("category:culture", "文化"), topic("theme:duplicate", " 文化 "), topic("theme:sakura", "賞櫻"), topic("theme:sakura", "Duplicate ID"), topic("theme:autumn", "賞楓"), topic("theme:market", "市場")];
    const { container } = render(<DiscoveryCard item={{ ...item, display_topics }} />);
    const meta = container.querySelector("article p")!;
    expect(meta.querySelectorAll('[aria-hidden="true"]')).toHaveLength(6); // map and five separators
    expect(screen.getByText("文化")).toBeTruthy(); expect(screen.getByText("賞櫻")).toBeTruthy();
    expect(screen.queryByText("+2")).toBeNull();
    expect(screen.getByText("市場")).toBeTruthy();
    expect(screen.queryByText("Duplicate ID")).toBeNull();
    expect(screen.getByText("賞楓", { exact: true })).toBeTruthy();
  });
  it("has no leading separator when a destination is missing", () => {
    const { container } = render(<DiscoveryCard item={{ ...item, destination: null, display_topics: [topic("category:culture", "文化")] }} />);
    expect(container.querySelector("article p")?.textContent).toBe("景點·文化");
  });
  it.each([
    ["zh-TW", "文化", "賞櫻"], ["zh-CN", "文化", "赏樱"], ["en", "Culture", "Cherry Blossoms"],
    ["ja", "文化", "桜"], ["ko", "문화", "벚꽃"],
  ])("uses the current localized projection and kind in %s", (locale, category, theme) => {
    mock.locale = locale;
    const { container } = render(<DiscoveryCard item={{ ...item, display_topics: [topic("category:culture", category), topic("theme:sakura", theme)] }} />);
    const meta = within(container.querySelector("article p") as HTMLElement);
    expect(meta.getByText(getDiscoveryCopy(locale).kinds.hotspot)).toBeTruthy();
    expect(meta.getByText(category)).toBeTruthy(); expect(meta.getByText(theme)).toBeTruthy();
  });
});

describe("source-linked discovery details", () => {
  it("separates source articles and videos by type and hides empty groups", () => {
    mock.detail = detail([guide("article", "https://source.test/article"), { ...guide("video", "https://source.test/video"), kind: "video" }]);
    const { rerender } = render(<DiscoveryDetails kind="hotspot" id="place" />);
    expect(within(screen.getByRole("region", { name: "articleGroup" })).getByRole("link", { name: /Guide article/ })).toBeTruthy();
    expect(within(screen.getByRole("region", { name: "videoGroup" })).getByRole("link", { name: /Guide video/ })).toBeTruthy();
    mock.detail = detail([guide("article", "https://source.test/article")]);
    rerender(<DiscoveryDetails kind="hotspot" id="place" />);
    expect(screen.queryByRole("region", { name: "videoGroup" })).toBeNull();
  });
  it("omits empty descriptions and coordinate-only place sections without placeholder copy", () => {
    mock.detail = { ...item, summary: "  ", detail: { guides: [], merchants: [], place: { status: "ready", coordinates: { latitude: 25, longitude: 121, source: "wikidata" } } } };
    const { container } = render(<DiscoveryDetails kind="hotspot" id="place" />);
    expect(screen.queryByRole("heading", { name: "關於這裡" })).toBeNull();
    expect(container.textContent).not.toContain("目前尚未提供更多資訊");
    expect(container.querySelectorAll("section")).toHaveLength(1); // sources only
  });
  it("omits coordinate text and copy controls but keeps map coordinates and official links", () => {
    const { container } = render(<DiscoveryDetails kind="hotspot" id="place" />);
    expect(container.textContent).not.toMatch(/25\.033|121\.5654|經緯度/);
    expect(screen.queryByRole("button", { name: "複製" })).toBeNull();
    expect(screen.getByText("Verified address")).toBeTruthy(); expect(screen.getByText("Monday 09:00–18:00")).toBeTruthy();
    expect(screen.getByRole("link", { name: "開啟地圖" }).getAttribute("href")).toContain("25.033,121.5654");
    expect(screen.getByRole("link", { name: "官方網站" }).getAttribute("href")).toBe("https://city.example.test/official");
  });
  it("links HTTP/S guides directly to source with labels, preserving query and fragments", () => {
    mock.detail = detail([guide("one", "https://tourism.example.test/read?a=1#walk", " City tourism "), guide("two", "http://archive.example.test/read", " "), guide("bad", "javascript:alert(1)"), guide("missing", null)]);
    render(<DiscoveryDetails kind="hotspot" id="place" />);
    const link = screen.getByRole("link", { name: "Guide one (City tourism)" });
    expect(link.getAttribute("href")).toBe("https://tourism.example.test/read?a=1#walk");
    expect(link.getAttribute("target")).toBe("_blank"); expect(link.getAttribute("rel")).toBe("noopener noreferrer");
    expect(screen.getByRole("link", { name: "Guide two (archive.example.test)" }).getAttribute("href")).toBe("http://archive.example.test/read");
    expect(screen.queryByText(/Guide bad|Guide missing/)).toBeNull();
  });
  it.each([null, "", "javascript:alert(1)", "data:text/html,hello", "/internal", "https://"])("omits the whole related-guides section when all sources are unusable: %s", (url) => {
    mock.detail = detail([guide("invalid", url)]);
    render(<DiscoveryDetails kind="hotspot" id="place" />);
    expect(screen.queryByRole("heading", { name: getFrontendFlowCopy(mock.locale).relatedGuides })).toBeNull();
    expect(screen.queryByText(/Guide invalid/)).toBeNull();
  });
  it("falls back to the hostname for a legacy null publisher label", () => {
    mock.detail = detail([guide("legacy", "https://legacy.example.test/read", null as unknown as string)]);
    render(<DiscoveryDetails kind="hotspot" id="place" />);
    expect(screen.getByRole("link", { name: "Guide legacy (legacy.example.test)" })).toBeTruthy();
  });
});
