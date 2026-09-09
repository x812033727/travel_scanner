import { cleanup, fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { SavedItemsProvider } from "@/components/saved-items-provider";
import { SavedContentAction } from "./saved-content-action";
import { DiscoveryCollections } from "./collections";
import { DiscoveryExplorer, DiscoveryHomeGate } from "./explorer";
import { DiscoveryDetails, discoveryDetailHref } from "./card";
import { getFrontendFlowCopy } from "@/lib/frontend-flow-copy";
import type { DiscoveryItem } from "@/lib/discovery";
const mock = vi.hoisted(() => ({ api: vi.fn(), push: vi.fn(), replace: vi.fn(), back: vi.fn(), query: "", path: "/explore", user: { id: "user-a" } as { id: string } | null, identity: {} as object | null, states: new Map<string, { saved: boolean; collection_ids: string[] }>() }));
vi.mock("@/lib/api", async (original) => ({ ...await original<typeof import("@/lib/api")>(), api: mock.api }));
vi.mock("@/lib/discovery", async (original) => ({ ...await original<typeof import("@/lib/discovery")>(), useDiscoveryStatus: () => ({ enabled: true, loading: false }) }));
vi.mock("next/navigation", () => ({ useSearchParams: () => new URLSearchParams(mock.query) }));
vi.mock("@/components/header-session", () => ({ useHeaderSession: () => ({ user: mock.user, sessionIdentity: mock.identity, status: mock.user ? "authenticated" : "signed_out" }) }));
vi.mock("@/components/community/provider", () => ({ useCommunity: () => ({ flags: { enabled: false } }) }));
vi.mock("@/components/travel-card-actions", () => ({ TravelPlanAction: () => <button>Plan confirmation</button> }));
vi.mock("@/i18n/navigation", () => ({ Link: ({ href, children, scroll, ...props }: React.AnchorHTMLAttributes<HTMLAnchorElement> & { href: string; scroll?: boolean }) => { void scroll; return <a href={href} {...props}>{children}</a>; }, usePathname: () => mock.path, useRouter: () => ({ push: mock.push, replace: mock.replace, back: mock.back }) }));
const id = "11111111-1111-4111-8111-111111111111";
const item: DiscoveryItem = { id: `hotspot:${id}`, kind: "hotspot", title: "River walk", summary: "A real source", locale: "en", href: "/hotspots", destination: { id: "tokyo", name: "Tokyo" }, source: { kind: "editorial", label: "City", url: "https://example.com/source" }, published_at: null, updated_at: null, thumbnail_url: null, collection_ref: { kind: "hotspot", id } };
function response(path: string, init?: RequestInit): unknown {
  if (path === "/saved-items?limit=100") return { items: [] };
  if (path === "/saved-items/states") return { items: JSON.parse(String(init?.body)).keys.map((key: string) => ({ key, ...(mock.states.get(key) || { saved: false, collection_ids: [] }) })) };
  if (path.startsWith("/saved-items/collections")) return { items: [{ id: "list-a", name: "Japan" }] };
  if (path.startsWith("/saved-items/") && ["PUT", "DELETE"].includes(init?.method || "")) { const [, , type, target] = path.split("?")[0].split("/"); const key = `${type}:${decodeURIComponent(target)}`; const state = { saved: init?.method === "PUT", collection_ids: [] }; mock.states.set(key, state); return state; }
  if (path.includes("suggestions")) return { items: [], query: "", destinations: [{ id: "tokyo", name: "Tokyo" }], topics: [] };
  if (path.includes("/content/")) return item;
  return { items: [], total: 0, next_cursor: null, filters: { kinds: [], destinations: [], topics: [] } };
}
beforeEach(() => { mock.api.mockReset(); mock.push.mockReset(); mock.replace.mockReset(); mock.back.mockReset(); mock.query = ""; mock.path = "/explore"; mock.user = { id: "user-a" }; mock.identity = {}; mock.states.clear(); mock.api.mockImplementation(async (path: string, init?: RequestInit) => response(path, init)); HTMLDialogElement.prototype.showModal = vi.fn(function (this: HTMLDialogElement) { this.setAttribute("open", ""); }); });
afterEach(() => { cleanup(); vi.restoreAllMocks(); });
describe("unified discovery interactions", () => {
  it("shows one search form and five categories; category resets legacy type but keeps destination", async () => {
    mock.query = "type=video&destination=tokyo";
    render(<DiscoveryHomeGate><form aria-label="Old flight form" /></DiscoveryHomeGate>);
    expect(screen.getAllByRole("search")).toHaveLength(1); expect(screen.queryByRole("form", { name: "Old flight form" })).toBeNull();
    const nav = screen.getByRole("navigation", { name: "縮小探索範圍" }); expect(within(nav).getAllByRole("button")).toHaveLength(5);
    fireEvent.click(within(nav).getByRole("button", { name: "美食" }));
    expect(mock.push).toHaveBeenCalledWith("/explore?category=foods&destination=tokyo", { scroll: false });
    await waitFor(() => expect(mock.api).toHaveBeenCalled());
  });
  it("preserves exact query in image/title detail links and closes a direct URL without losing filters", async () => {
    mock.user = null; mock.query = `q=Tokyo&category=hotspots&destination=tokyo&content=hotspot:${id}`;
    render(<DiscoveryExplorer />);
    expect(await screen.findByRole("dialog", { name: "閱讀詳情" })).toBeTruthy();
    fireEvent.click(within(screen.getByRole("dialog")).getByRole("button", { name: "關閉" }));
    expect(mock.replace).toHaveBeenCalledWith("/explore?q=Tokyo&category=hotspots&destination=tokyo", { scroll: false });
    expect(discoveryDetailHref(item, "/explore?q=Tokyo&category=hotspots")).toBe(`/explore?q=Tokyo&category=hotspots&content=hotspot%3A${id}`);
  });
  it("saves hotel/service once across two cards and offers an explicit undo", async () => {
    render(<SavedItemsProvider><SavedContentAction item={{ type: "hotel", id, title: "Hotel" }} returnTo="/explore" compact /><SavedContentAction item={{ type: "service", id, title: "Hotel" }} returnTo="/explore" compact /></SavedItemsProvider>);
    await waitFor(() => expect(screen.getAllByRole("button", { name: "收藏" }).every((button) => !(button as HTMLButtonElement).disabled)).toBe(true));
    fireEvent.click(screen.getAllByRole("button", { name: "收藏" })[0]);
    await waitFor(() => expect(screen.getAllByRole("button", { name: "已收藏" })).toHaveLength(2));
    expect(mock.api.mock.calls.filter(([, init]) => init?.method === "PUT")).toHaveLength(1);
    expect(mock.states.get(`service:${id}`)?.saved).toBe(true);
    fireEvent.click(screen.getByRole("button", { name: "復原" }));
    await waitFor(() => expect(screen.getAllByRole("button", { name: "收藏" })).toHaveLength(2));
    expect(mock.api.mock.calls.filter(([, init]) => init?.method === "DELETE")).toHaveLength(1);
  });
  it("auth resume is confirm-only and does not toggle off an already saved item", async () => {
    mock.query = `save_key=hotspot:${id}`; mock.states.set(`hotspot:${id}`, { saved: true, collection_ids: [] });
    render(<SavedItemsProvider><SavedContentAction item={item} returnTo="/explore?destination=tokyo" /></SavedItemsProvider>);
    const dialog = await screen.findByRole("dialog", { name: "收藏這個靈感" });
    await waitFor(() => expect(within(dialog).getByRole("button", { name: "繼續探索" })).toBeTruthy());
    expect(mock.api.mock.calls.some(([, init]) => ["PUT", "DELETE"].includes(init?.method))).toBe(false);
    fireEvent.click(within(dialog).getByRole("button", { name: "繼續探索" }));
    expect(mock.replace).toHaveBeenCalledWith("/explore", { scroll: false });
    expect(mock.states.get(`hotspot:${id}`)?.saved).toBe(true);
  });
  it("removes collection membership without globally unsaving", async () => {
    mock.states.set(`hotspot:${id}`, { saved: true, collection_ids: ["list-a"] });
    mock.api.mockImplementation(async (path: string, init?: RequestInit) => {
      if (path === "/saved-items/collections/list-a") return { items: [{ id: "membership-a", kind: "hotspot", target: id }] };
      if (path.includes("/items/membership-a")) { mock.states.set(`hotspot:${id}`, { saved: true, collection_ids: [] }); return { deleted: true }; }
      return response(path, init);
    });
    render(<SavedItemsProvider><SavedContentAction item={item} returnTo="/explore" /></SavedItemsProvider>);
    fireEvent.click(await screen.findByRole("button", { name: `整理: ${item.title}` }));
    fireEvent.click(await screen.findByRole("button", { name: "從這份清單移除" }));
    await waitFor(() => expect(screen.getByRole("button", { name: "加入清單" })).toBeTruthy());
    expect(mock.states.get(`hotspot:${id}`)).toEqual({ saved: true, collection_ids: [] });
    expect(mock.api.mock.calls.filter(([, init]) => init?.method === "DELETE").map(([path]) => path)).toEqual(["/saved-items/collections/list-a/items/membership-a?expected_user_id=user-a"]);
  });
  it("defaults to all saved, appends cursor pages and keeps unavailable content removable", async () => {
    mock.path = "/explore/collections";
    const first = { key: `hotspot:${id}`, type: "hotspot", id, title: item.title, discovery: item, collection_ids: [], unavailable: false };
    const second = { key: "guide:missing", type: "guide", id: "missing", title: "Withdrawn guide", collection_ids: [], unavailable: true };
    mock.states.set(first.key, { saved: true, collection_ids: [] }); mock.states.set(second.key, { saved: true, collection_ids: [] });
    mock.api.mockImplementation(async (path: string, init?: RequestInit) => path.startsWith("/saved-items/all") ? { items: path.includes("cursor=") ? [second] : [first], next_cursor: path.includes("cursor=") ? null : "page-two", total: 2, has_more: !path.includes("cursor=") } : response(path, init));
    render(<SavedItemsProvider><DiscoveryCollections /></SavedItemsProvider>);
    expect(await screen.findByRole("link", { name: item.title })).toBeTruthy();
    expect(mock.api).toHaveBeenCalledWith("/saved-items/all?limit=24", expect.anything());
    fireEvent.click(screen.getByRole("button", { name: "載入更多" }));
    expect(await screen.findByRole("heading", { name: "Withdrawn guide" })).toBeTruthy(); expect(screen.getByRole("link", { name: item.title })).toBeTruthy();
    expect(screen.queryByRole("link", { name: "Withdrawn guide" })).toBeNull();
    vi.spyOn(window, "confirm").mockReturnValue(true);
    fireEvent.click(screen.getByRole("button", { name: "取消收藏" }));
    await waitFor(() => expect(mock.states.get(second.key)?.saved).toBe(false));
  });
  it("renders current source fields and rejects unsafe outgoing links", async () => {
    mock.user = null;
    mock.api.mockResolvedValue({ ...item, detail: { intro: null, merchants: [], guides: [], hotel: null, planning: null, place: { status: "ready", address: "Hiroshima, Japan", opening_hours: { weekday_descriptions: ["Monday: Open 24 hours"] }, coordinates: { latitude: 34.395483, longitude: 132.453592, source: "wikidata" }, google_maps_url: "https://maps.google.com/?q=Hiroshima", official_website_url: "javascript:alert(1)", fetched_at: "2026-09-09T00:00:00Z", attribution: { provider: "Google Maps", provider_url: "https://maps.google.com/", third_party: [{ provider: "City", providerUri: "https://example.com/city" }] } } } });
    render(<DiscoveryDetails kind="hotspot" id={id} />);
    expect(await screen.findByText("Hiroshima, Japan")).toBeTruthy(); expect(screen.getByText("Monday: Open 24 hours")).toBeTruthy();
    expect(screen.getByText(/34.395483, 132.453592/)).toBeTruthy(); expect(screen.getByRole("link", { name: "Google Maps" }).getAttribute("rel")).toBe("noopener noreferrer");
    expect(screen.queryByRole("link", { name: "官方網站" })).toBeNull();
  });
  it("keeps the independent copy complete in all five languages", () => { for (const locale of ["en", "zh-TW", "zh-CN", "ja", "ko"]) expect(Object.keys(getFrontendFlowCopy(locale))).toEqual(Object.keys(getFrontendFlowCopy("en"))); });
});
