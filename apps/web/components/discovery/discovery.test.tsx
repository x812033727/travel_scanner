import { act, cleanup, fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { DiscoveryExplorer, DiscoveryHomeGate } from "./explorer";
import { DiscoveryVideoPlayer } from "./video";
import { DiscoveryCard } from "./card";
import { DiscoveryDetailBoundary } from "./detail-drawer";
import { OrganizeSavedContent } from "./saved-content-action";
import { getFrontendFlowCopy } from "@/lib/frontend-flow-copy";
import { DiscoveryCollections } from "./collections";
import { DiscoveryPreferenceEditor } from "./preferences";
import { CommunityImage } from "@/components/community/ui";
import { youtubeId, discoveryQuery, type DiscoveryItem } from "@/lib/discovery";
import { getDiscoveryCopy, getRecommendationReason } from "@/lib/discovery-copy";
import { ApiError } from "@/lib/api";
const mock = vi.hoisted(() => ({ api: vi.fn(), push: vi.fn(), query: "", enabled: true, social: false, user: null as null | { id: string }, identity: null as object | null }));
vi.mock("@/lib/api", async (original) => ({ ...await original<typeof import("@/lib/api")>(), api: mock.api }));
vi.mock("@/lib/discovery", async (original) => ({ ...await original<typeof import("@/lib/discovery")>(), useDiscoveryStatus: () => ({ enabled: mock.enabled, loading: false }) }));
vi.mock("next/navigation", () => ({ useSearchParams: () => new URLSearchParams(mock.query) }));
vi.mock("@/components/header-session", () => ({ useHeaderSession: () => ({ user: mock.user, status: mock.user ? "authenticated" : "signed_out", sessionIdentity: mock.identity }) }));
vi.mock("@/components/community/provider", () => ({ useCommunity: () => ({ flags: { enabled: mock.social }, me: null }) }));
vi.mock("@/components/search-workbench", () => ({ SearchWorkbench: () => <div>Original search workbench</div> }));
vi.mock("@/components/account-saved-items", () => ({ AccountSavedItems: () => <div>Existing saved places</div> }));
vi.mock("@/i18n/navigation", () => ({ Link: ({ href, children, scroll, ...props }: React.AnchorHTMLAttributes<HTMLAnchorElement> & { href: string; scroll?: boolean }) => { void scroll; return <a href={href} {...props}>{children}</a>; }, usePathname: () => "/explore", useRouter: () => ({ push: mock.push, replace: mock.push, back: mock.push }) }));
const item: DiscoveryItem = { id: "guide:11111111-1111-4111-8111-111111111111", kind: "article", title: "東京散步攻略", summary: "從官方步道資料開始", locale: "ja", href: "/hotspots", destination: { id: "tokyo", name: "東京" }, source: { kind: "editorial", label: "City guide", url: "https://example.org/guide" }, published_at: "2026-09-01T00:00:00Z", updated_at: null, thumbnail_url: null, collection_ref: { kind: "guide", id: "11111111-1111-4111-8111-111111111111" }, recommendation_reason: "destination_interest" };
const page = (items = [item]) => ({ enabled: true, items, query: "", next_cursor: null, filters: { kinds: [], destinations: [], topics: [] } });
beforeEach(() => {
  mock.api.mockReset(); mock.push.mockReset(); mock.query = ""; mock.enabled = true; mock.social = false; mock.user = null; mock.identity = null;
  HTMLDialogElement.prototype.showModal = vi.fn(function (this: HTMLDialogElement) { this.setAttribute("open", ""); });
  mock.api.mockImplementation(async (path: string) => path.includes("/suggestions") ? { query: "", items: [], destinations: [{ id: "tokyo", name: "東京" }], topics: [{ id: "culture", label: "文化" }] } : path.includes("/content/") ? item : path.includes("/collections") ? { items: [] } : page());
});
afterEach(() => { cleanup(); vi.restoreAllMocks(); });
describe("discovery sources and privacy", () => {
  it("preserves the original homepage and avoids discovery reads when rollout is off", () => {
    mock.enabled = false;
    render(<DiscoveryHomeGate><input aria-label="Original trip form" /></DiscoveryHomeGate>);
    expect(screen.getByLabelText("Original trip form")).toBeTruthy(); expect(mock.api).not.toHaveBeenCalled();
  });
  it("shows real source, localized recommendation reason and actual matching query", async () => {
    mock.query = "q=東京&type=article&destination=tokyo&locale=ja";
    render(<DiscoveryExplorer />);
    expect(await screen.findByText("東京散步攻略")).toBeTruthy();
    expect(screen.getByText("符合你選擇的目的地")).toBeTruthy();
    expect(screen.getByRole("heading", { name: "搜尋結果「東京」" })).toBeTruthy();
    expect(mock.api.mock.calls.some(([path]) => String(path).includes("q=%E6%9D%B1%E4%BA%AC&type=article&destination=tokyo&locale=ja"))).toBe(true);
    expect(screen.queryByRole("img")).toBeNull();
  });
  it("aborts an old filter request and excludes its late response", async () => {
    let finish!: (value: unknown) => void;
    let signal!: AbortSignal;
    mock.api.mockImplementation((path: string, init?: RequestInit) => {
      if (path.includes("q=old")) { signal = init!.signal as AbortSignal; return new Promise((resolve) => { finish = resolve; }); }
      return Promise.resolve(path.includes("/suggestions") ? { items: [], destinations: [], query: "" } : page());
    });
    mock.query = "q=old"; const view = render(<DiscoveryExplorer />);
    await waitFor(() => expect(finish).toBeTypeOf("function"));
    mock.query = "q=new"; view.rerender(<DiscoveryExplorer />);
    expect(signal.aborted).toBe(true);
    await act(async () => finish(page([{ ...item, title: "Obsolete match" }])));
    expect(await screen.findByText(item.title)).toBeTruthy(); expect(screen.queryByText("Obsolete match")).toBeNull();
  });
  it("uses available destination options, not just the server's active filters", async () => {
    render(<DiscoveryExplorer />);
    const select = await screen.findByRole("combobox", { name: "目的地" });
    await waitFor(() => expect(within(select).getByRole("option", { name: "東京" })).toBeTruthy());
    fireEvent.change(select, { target: { value: "tokyo" } });
    expect(mock.push).toHaveBeenCalledWith("/explore?destination=tokyo", { scroll: false });
  });
  it("keeps destination available and collapses advanced filters behind an accessible toggle", async () => {
    render(<DiscoveryExplorer />);
    const toggle = screen.getByRole("button", { name: getFrontendFlowCopy("zh-TW").advanced });
    expect(toggle.getAttribute("aria-expanded")).toBe("false");
    expect(document.getElementById(toggle.getAttribute("aria-controls")!)).toBeNull();
    expect(screen.getByRole("combobox", { name: "目的地" })).toBeTruthy();
    fireEvent.click(toggle);
    expect(toggle.getAttribute("aria-expanded")).toBe("true");
    expect(document.getElementById(toggle.getAttribute("aria-controls")!)).toBeTruthy();
    expect(screen.getByRole("combobox", { name: "內容類型" })).toBeTruthy();
    expect(await screen.findByText(item.title)).toBeTruthy();
  });
  it("restarts expired pagination at page one instead of retrying its expired cursor", async () => {
    mock.api.mockImplementation(async (path: string) => {
      if (path.includes("suggestions")) return { query: "", items: [], destinations: [] };
      if (path.includes("cursor=")) throw new ApiError("Expired", 409, "community_feed_expired");
      return { ...page(), next_cursor: "expired" };
    });
    render(<DiscoveryExplorer />); fireEvent.click(await screen.findByRole("button", { name: "載入更多" }));
    fireEvent.click(await screen.findByRole("button", { name: "重試" }));
    await waitFor(() => expect(mock.api.mock.calls.filter(([path]) => path === "/discovery/feed?mode=recommended")).toHaveLength(2));
    expect(mock.api.mock.calls.filter(([path]) => String(path).includes("cursor=expired"))).toHaveLength(1);
  });
  it("keeps filters in the sign-in return path for following", async () => {
    mock.social = true; mock.query = "mode=following&destination=tokyo";
    render(<DiscoveryExplorer />);
    expect((await screen.findByRole("link", { name: "登入後繼續" })).getAttribute("href")).toContain(encodeURIComponent("destination=tokyo&mode=following"));
    expect(mock.api.mock.calls.some(([path]) => String(path).includes("/feed"))).toBe(false);
  });
  it("ranks by the cumulative saved count on its own tab, without requiring a sign-in", async () => {
    render(<DiscoveryExplorer />);
    fireEvent.click(await screen.findByRole("button", { name: "蒐藏數" }));
    expect(mock.push).toHaveBeenCalledWith("/explore?mode=most_saved", { scroll: false });
    mock.push.mockReset(); mock.query = "mode=most_saved"; cleanup();
    render(<DiscoveryExplorer />);
    expect(await screen.findByText(item.title)).toBeTruthy();
    await waitFor(() => expect(mock.api.mock.calls.some(([path]) => String(path) === "/discovery/feed?mode=most_saved")).toBe(true));
    expect(screen.queryByRole("link", { name: "登入後繼續" })).toBeNull();
  });
  it("keeps the saved-count tab between latest and following", async () => {
    mock.social = true;
    render(<DiscoveryExplorer />);
    const tabs = await screen.findByLabelText("下一站，從這裡發現", { selector: "div" });
    expect(within(tabs).getAllByRole("button").map((button) => button.textContent)).toEqual(["為你推薦", "最新", "蒐藏數", "追蹤中"]);
  });
  it("shows the cumulative saved count on the card only once someone has saved it", () => {
    const view = render(<DiscoveryCard item={{ ...item, saved_count: 3 }} />);
    expect(screen.getByText("3 次收藏")).toBeTruthy();
    view.rerender(<DiscoveryCard item={{ ...item, saved_count: 0 }} />);
    expect(screen.queryByText(/次收藏$/)).toBeNull();
    view.rerender(<DiscoveryCard item={item} />);
    expect(screen.queryByText(/次收藏$/)).toBeNull();
  });
  it("exposes guide collections without community enrollment or fake hotel prices", async () => {
    mock.user = { id: "reader" }; mock.identity = {};
    render(<OrganizeSavedContent item={{ ...item, kind: "hotel", id: "hotel:1" }} onClose={vi.fn()} />);
    expect(await screen.findByRole("dialog")).toBeTruthy();
    expect(mock.api).toHaveBeenCalledWith("/saved-items/collections", expect.objectContaining({ signal: expect.any(AbortSignal) }));
    expect(screen.queryByText(/NT\$/)).toBeNull();
  });
  it("creates private collections for plain accounts while community is off", async () => {
    mock.user = { id: "reader" }; mock.identity = {};
    mock.api.mockImplementation(async (path: string, init?: RequestInit) => path.startsWith("/saved-items/collections") && init?.method === "POST" ? { id: "list-1", name: "京都" } : { items: [] });
    render(<DiscoveryCollections />);
    fireEvent.click(await screen.findByRole("button", { name: "建立清單" }));
    fireEvent.change(screen.getByLabelText("清單名稱"), { target: { value: "京都" } });
    fireEvent.click(within(screen.getByRole("dialog")).getByRole("button", { name: "建立清單" }));
    await waitFor(() => expect(mock.api.mock.calls.some(([path, init]) => path === "/saved-items/collections?expected_user_id=reader" && init?.body === '{"name":"京都"}')).toBe(true));
    expect(mock.api.mock.calls.some(([path]) => String(path).startsWith("/community"))).toBe(false);
  });
  it("renders sourced images lazily and blocks social cards when its separate flag is off", () => {
    const view = render(<DiscoveryCard item={{ ...item, thumbnail_url: "https://example.org/photo.jpg" }} />);
    expect(screen.getByRole("img").getAttribute("loading")).toBe("lazy");
    view.rerender(<DiscoveryCard item={{ ...item, kind: "post", source: { ...item.source, kind: "community" } }} />);
    expect(screen.queryByText(item.title)).toBeNull();
  });
  it("resolves a published original cover and all detail photos through the authorized media endpoint", async () => {
    mock.social = true;
    const story: DiscoveryItem = { ...item, kind: "post", source: { ...item.source, kind: "community" }, content: { text: "Original story", media: [{ id: "image-1", alt: "Morning walk", width: 1200, height: 800 }, { id: "image-2", alt: "Garden path", width: 800, height: 1200 }] } };
    mock.api.mockImplementation(async (path: string) => path.startsWith("/community/media/") ? { url: `https://media.example.org/${path.split("/").at(-1)}` } : story);
    const view = render(<DiscoveryDetailBoundary><DiscoveryCard item={story} /></DiscoveryDetailBoundary>);
    expect(await screen.findByRole("img", { name: "Morning walk" })).toBeTruthy();
    expect(mock.api).toHaveBeenCalledWith("/community/media/image-1?thumbnail=true");
    expect(mock.api).not.toHaveBeenCalledWith("/community/media/image-2?thumbnail=true");
    mock.query = `content=post:${item.id.split(":")[1]}`;
    view.rerender(<DiscoveryDetailBoundary><DiscoveryCard item={story} /></DiscoveryDetailBoundary>);
    expect(await screen.findByRole("img", { name: "Garden path" })).toBeTruthy();
    expect(mock.api).toHaveBeenCalledWith("/community/media/image-1");
    expect(mock.api).toHaveBeenCalledWith("/community/media/image-2");
  });
  it("hides an old signed media URL immediately when the active login changes", async () => {
    mock.identity = {};
    mock.api.mockResolvedValueOnce({ url: "https://media.example.org/old-signed" });
    const view = render(<CommunityImage id="image-1" alt="Private authorization" thumbnail />);
    expect(await screen.findByRole("img")).toBeTruthy();
    let finish!: (value: { url: string }) => void;
    mock.api.mockImplementation(() => new Promise((resolve) => { finish = resolve; }));
    mock.identity = {}; view.rerender(<CommunityImage id="image-1" alt="Private authorization" thumbnail />);
    expect(screen.queryByRole("img")).toBeNull();
    await act(async () => finish({ url: "https://media.example.org/new-signed" }));
    expect(screen.getByRole("img").getAttribute("src")).toBe("https://media.example.org/new-signed");
  });
  it("loads only a reviewed exact nocookie embed after explicit consent", () => {
    const video = { provider: "youtube" as const, video_id: "dQw4w9WgXcQ", source_url: "https://www.youtube.com/watch?v=dQw4w9WgXcQ", status: "embeddable" as const, embed_url: "https://www.youtube-nocookie.com/embed/dQw4w9WgXcQ" };
    const view = render(<DiscoveryVideoPlayer video={video} />);
    expect(document.querySelector("iframe")).toBeNull();
    fireEvent.click(screen.getByRole("button", { name: "載入影片" }));
    expect(document.querySelector("iframe")?.getAttribute("src")).toContain("youtube-nocookie.com/embed/dQw4w9WgXcQ?autoplay=0");
    expect(document.querySelector("iframe")?.className).toContain("min-h-[200px]");
    view.rerender(<DiscoveryVideoPlayer video={{ ...video, status: "link_only", embed_url: null }} />);
    expect(document.querySelector("iframe")).toBeNull(); expect(screen.getByRole("link")).toBeTruthy();
  });
  it("uses labelled preference choices and saves only explicit interests with version", async () => {
    mock.user = { id: "reader" }; mock.identity = {};
    const onSaved = vi.fn();
    mock.api.mockImplementation(async (path: string, init?: RequestInit) => path === "/discovery/preferences" && !init?.method ? { version: 3, destinations: [], topics: [], include_saved: false, include_following: false } : path.includes("suggestions") ? { destinations: [{ id: "tokyo", name: "東京" }], topics: [{ id: "culture", label: "文化" }] } : {});
    render(<DiscoveryPreferenceEditor onClose={vi.fn()} onSaved={onSaved} />);
    fireEvent.click(await screen.findByLabelText("東京")); fireEvent.click(screen.getByLabelText("文化"));
    fireEvent.click(screen.getByRole("button", { name: "儲存興趣" }));
    await waitFor(() => expect(onSaved).toHaveBeenCalled());
    const call = mock.api.mock.calls.find(([path, init]) => path === "/discovery/preferences" && init?.method === "PUT");
    expect(JSON.parse(call?.[1].body)).toEqual({ version: 3, destinations: ["tokyo"], topics: ["culture"], include_saved: false, include_following: false });
  });
  it("retains the preference draft on conflict and reloads only after explicit discard", async () => {
    mock.user = { id: "reader" }; mock.identity = {};
    let version = 3;
    mock.api.mockImplementation(async (path: string, init?: RequestInit) => {
      if (path.includes("suggestions")) return { destinations: [{ id: "tokyo", name: "東京" }], topics: [] };
      if (init?.method === "PUT") { version = 4; throw new ApiError("Conflict", 409, "version_conflict"); }
      return { version, destinations: [], topics: [], include_saved: false, include_following: false };
    });
    render(<DiscoveryPreferenceEditor onClose={vi.fn()} onSaved={vi.fn()} />);
    fireEvent.click(await screen.findByLabelText("東京")); fireEvent.click(screen.getByRole("button", { name: "儲存興趣" }));
    const reload = await screen.findByRole("button", { name: "載入最新版本" });
    expect((screen.getByLabelText("東京") as HTMLInputElement).checked).toBe(true);
    vi.spyOn(window, "confirm").mockReturnValueOnce(false).mockReturnValueOnce(true);
    fireEvent.click(reload); expect((screen.getByLabelText("東京") as HTMLInputElement).checked).toBe(true);
    fireEvent.click(reload);
    await waitFor(() => expect((screen.getByLabelText("東京") as HTMLInputElement).checked).toBe(false));
  });
  it("renders plain authorized details, never HTML supplied by a source", async () => {
    mock.api.mockResolvedValue({ ...item, content: { text: "<script>bad()</script>", format: "plain" } });
    mock.query = `content=article:${item.id.split(":")[1]}`;
    render(<DiscoveryDetailBoundary><DiscoveryCard item={item} /></DiscoveryDetailBoundary>);
    expect(await screen.findByText("<script>bad()</script>")).toBeTruthy();
    expect(within(screen.getByRole("dialog")).getByRole("link", { name: "查看原始來源" }).getAttribute("rel")).toBe("noopener noreferrer");
  });
  it("shows public creator video references and an allowlisted itinerary without fetching a private trip", async () => {
    const publicItem = { ...item, content: { text: "Public story", video_refs: [{ provider: "youtube", video_id: "dQw4w9WgXcQ", source_url: "https://www.youtube.com/watch?v=dQw4w9WgXcQ", status: "link_only", embed_url: null }], itinerary: { destination: "Tokyo", timezone: "Asia/Tokyo", days: 1, stops: [{ day: 1, position: 0, title: "Public stop", location_name: "Tokyo", item_type: "activity", duration_minutes: 60, names: {} }] } } };
    mock.api.mockResolvedValue(publicItem);
    mock.query = `content=article:${item.id.split(":")[1]}`;
    render(<DiscoveryDetailBoundary><DiscoveryCard item={item} /></DiscoveryDetailBoundary>);
    expect(await screen.findByText("Public stop")).toBeTruthy();
    expect(screen.getAllByRole("link", { name: "查看原始來源" }).some((link) => link.getAttribute("href")?.includes("youtube.com/watch"))).toBe(true);
    expect(document.querySelector("iframe")).toBeNull();
    expect(mock.api.mock.calls.some(([path]) => String(path).startsWith("/trips/"))).toBe(false);
  });
});
describe("discovery input contracts", () => {
  it("extracts canonical YouTube references and rejects foreign or credentialed URLs", () => {
    expect(youtubeId("https://youtu.be/dQw4w9WgXcQ?si=abc")).toBe("dQw4w9WgXcQ");
    expect(youtubeId("https://www.youtube.com/shorts/dQw4w9WgXcQ")).toBe("dQw4w9WgXcQ");
    for (const url of ["javascript:alert(1)", "https://youtube.com.evil.test/watch?v=dQw4w9WgXcQ", "https://user@youtube.com/watch?v=dQw4w9WgXcQ", "https://youtu.be/bad"]) expect(youtubeId(url)).toBeNull();
  });
  it("keeps only supported query fields and all five copy catalogs complete", () => {
    expect(discoveryQuery({ q: " tokyo ", type: "all", locale: "ja" })).toBe("q=tokyo&locale=ja");
    for (const locale of ["en", "ja", "ko", "zh-TW", "zh-CN"]) {
      expect(Object.keys(getDiscoveryCopy(locale))).toEqual(Object.keys(getDiscoveryCopy("en")));
      expect(getRecommendationReason(locale, "saved_interest")).not.toBe("saved_interest");
    }
  });
});
