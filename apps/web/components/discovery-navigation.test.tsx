import { act, fireEvent, render, screen, within } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { AppBottomNav } from "./app-bottom-nav";
import { MobileNav } from "./mobile-nav";
import { SiteNavigation } from "./site-navigation";
import { ThemeProvider } from "./theme-provider";
import { MyDirectory } from "./community/home";
import { frontendCopy } from "@/lib/frontend-navigation";

const state = vi.hoisted(() => ({ enabled: true, community: false, posting: true, pathname: "/", trips: true }));
vi.mock("@/lib/discovery", async (original) => ({ ...await original<typeof import("@/lib/discovery")>(), useDiscoveryStatus: () => ({ enabled: state.enabled, loading: false }) }));
vi.mock("@/i18n/navigation", () => ({
  Link: ({ href, children, ...props }: React.AnchorHTMLAttributes<HTMLAnchorElement>) => <a href={href} {...props}>{children}</a>,
  usePathname: () => state.pathname,
  useRouter: () => ({ push: vi.fn(), replace: vi.fn(), refresh: vi.fn() }),
}));
vi.mock("./community/provider", () => ({ useCommunity: () => ({ flags: { enabled: state.community, posting_enabled: state.posting }, unread: 2 }) }));
vi.mock("./site-visibility-provider", () => ({ useSiteVisibility: () => ({ status: "ready", features: { trips_enabled: state.trips, hotspots_enabled: true, alerts_enabled: true, flight_status_enabled: true, airline_fares_enabled: true, pricing_enabled: true } }) }));
vi.mock("./header-auth", () => ({ HeaderAuth: () => null }));

beforeEach(() => { state.enabled = true; state.community = false; state.posting = true; state.pathname = "/"; state.trips = true; });

describe("discovery navigation", () => {
  it("keeps four useful mobile destinations without requiring community activation", () => {
    render(<AppBottomNav />);
    const links = screen.getAllByRole("link");
    const c = frontendCopy("zh-TW");
    expect(links.map((link) => link.textContent)).toEqual([c.explore, c.collections, c.trips, c.my]);
    expect(links.map((link) => link.getAttribute("href"))).toEqual(["/explore", "/explore/collections", "/trips", "/my"]);
    expect(screen.queryByRole("link", { name: "發布" })).toBeNull();
  });

  it("selects collections without also selecting explore and honors locale prefixes", () => {
    state.pathname = "/zh-TW/explore/collections";
    render(<AppBottomNav />);
    expect(screen.getByRole("link", { name: "收藏" }).getAttribute("aria-current")).toBe("page");
    expect(screen.getByRole("link", { name: "探索" }).hasAttribute("aria-current")).toBe(false);
  });

  it("does not place the general tab bar over an itinerary editor or admin screen", () => {
    state.pathname = "/trips/private-id";
    const view = render(<AppBottomNav />);
    expect(screen.queryByRole("navigation")).toBeNull();
    state.pathname = "/admin/hotspots";
    view.rerender(<AppBottomNav />);
    expect(screen.queryByRole("navigation")).toBeNull();
  });

  it("honors the existing trips visibility switch", () => {
    state.trips = false;
    render(<AppBottomNav />);
    expect(screen.queryByRole("link", { name: frontendCopy("zh-TW").trips })).toBeNull();
  });

  it("keeps original navigation when discovery is unavailable", () => {
    state.enabled = false;
    render(<AppBottomNav />);
    expect(screen.getByRole("link", { name: /探索/ }).getAttribute("href")).toBe("/hotspots");
    expect(screen.queryByRole("link", { name: "收藏" })).toBeNull();
  });

  it("routes the compact mobile header to publishing and notifications in My space", async () => {
    state.community = true;
    const header = render(<ThemeProvider><MobileNav /></ThemeProvider>);
    await act(async () => {});
    expect(screen.getByRole("link", { name: frontendCopy("zh-TW").my }).getAttribute("href")).toBe("/my");
    expect(screen.queryByRole("button", { name: "開啟導覽選單" })).toBeNull();
    header.unmount();
    const directory = render(<ThemeProvider><MyDirectory /></ThemeProvider>);
    await act(async () => {});
    const nav = screen.getByRole("navigation", { name: "我的" });
    expect(within(nav).getByRole("link", { name: "我的收藏" }).getAttribute("href")).toBe("/explore/collections");
    expect(within(nav).getByRole("link", { name: "發佈" }).getAttribute("href")).toBe("/community/new");
    expect(within(nav).getByRole("link", { name: "訊息" }).getAttribute("href")).toBe("/community/messages");
    state.posting = false; directory.rerender(<ThemeProvider><MyDirectory /></ThemeProvider>);
    expect(screen.queryByRole("link", { name: "發佈" })).toBeNull();
    expect(screen.getByRole("link", { name: "訊息" }).getAttribute("href")).toBe("/community/messages");
  });

  it("preserves the legacy menu keyboard close and focus return when discovery is off", async () => {
    state.enabled = false;
    state.community = true;
    render(<ThemeProvider><MobileNav /></ThemeProvider>);
    await act(async () => {});
    fireEvent.click(screen.getByRole("button", { name: "開啟導覽選單" }));
    await act(async () => {});
    const dialog = screen.getByRole("dialog");
    expect(within(dialog).getByRole("link", { name: "社群" }).getAttribute("href")).toBe("/community");
    expect(within(dialog).getByRole("link", { name: "我的" }).getAttribute("href")).toBe("/my");
    fireEvent.keyDown(document, { key: "Escape" });
    expect(screen.queryByRole("dialog")).toBeNull();
    expect(document.activeElement).toBe(screen.getByRole("button", { name: "開啟導覽選單" }));
  });

  it("uses the same desktop destinations", async () => {
    render(<ThemeProvider><SiteNavigation /></ThemeProvider>);
    await act(async () => {});
    const desktop = screen.getByRole("navigation");
    expect(within(desktop).getByRole("link", { name: frontendCopy("zh-TW").trips }).getAttribute("href")).toBe("/trips");
    expect(within(desktop).getByRole("link", { name: "收藏" }).getAttribute("href")).toBe("/explore/collections");
  });

  it("lets signed-out readers choose every palette even when discovery and community are off", async () => {
    state.enabled = false;
    state.community = false;
    render(<ThemeProvider><MyDirectory /></ThemeProvider>);
    await act(async () => {});
    const palettes = screen.getByRole("group", { name: "全站配色" });
    expect(within(palettes).getAllByRole("radio")).toHaveLength(3);
    fireEvent.click(within(palettes).getByRole("radio", { name: "海島藍" }));
    expect(document.documentElement.dataset.palette).toBe("lagoon");
  });
});
