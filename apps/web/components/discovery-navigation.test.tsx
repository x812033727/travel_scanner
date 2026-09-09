import { act, fireEvent, render, screen, within } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { AppBottomNav } from "./app-bottom-nav";
import { MobileNav } from "./mobile-nav";
import { SiteNavigation } from "./site-navigation";
import { ThemeProvider } from "./theme-provider";

const state = vi.hoisted(() => ({ enabled: true, community: false, pathname: "/", trips: true }));
vi.mock("@/lib/discovery", () => ({ useDiscoveryStatus: () => ({ enabled: state.enabled, loading: false }) }));
vi.mock("@/lib/discovery-copy", () => ({ getDiscoveryCopy: () => ({ explore: "探索", collections: "收藏", trips: "我的旅行", my: "我的", publish: "發布", notifications: "通知" }) }));
vi.mock("@/i18n/navigation", () => ({
  Link: ({ href, children, ...props }: React.AnchorHTMLAttributes<HTMLAnchorElement>) => <a href={href} {...props}>{children}</a>,
  usePathname: () => state.pathname,
  useRouter: () => ({ push: vi.fn(), replace: vi.fn(), refresh: vi.fn() }),
}));
vi.mock("./community/provider", () => ({ useCommunity: () => ({ flags: { enabled: state.community, posting_enabled: true }, unread: 2 }) }));
vi.mock("./site-visibility-provider", () => ({ useSiteVisibility: () => ({ status: "ready", features: { trips_enabled: state.trips, hotspots_enabled: true, alerts_enabled: true, flight_status_enabled: true, airline_fares_enabled: true, pricing_enabled: true } }) }));
vi.mock("./header-auth", () => ({ HeaderAuth: () => null }));

beforeEach(() => { state.enabled = true; state.community = false; state.pathname = "/"; state.trips = true; });

describe("discovery navigation", () => {
  it("keeps four useful mobile destinations without requiring community activation", () => {
    render(<AppBottomNav />);
    const links = screen.getAllByRole("link");
    expect(links.map((link) => link.textContent)).toEqual(["探索", "收藏", "我的旅行", "我的"]);
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
    expect(screen.queryByRole("link", { name: "我的旅行" })).toBeNull();
  });

  it("keeps original navigation when discovery is unavailable", () => {
    state.enabled = false;
    render(<AppBottomNav />);
    expect(screen.getByRole("link", { name: /探索/ }).getAttribute("href")).toBe("/hotspots");
    expect(screen.queryByRole("link", { name: "收藏" })).toBeNull();
  });

  it("exposes publishing and notifications outside the four mobile tabs", async () => {
    state.community = true;
    render(<ThemeProvider><MobileNav /></ThemeProvider>);
    await act(async () => {});
    fireEvent.click(screen.getByRole("button", { name: "開啟導覽選單" }));
    const dialog = screen.getByRole("dialog");
    expect(within(dialog).getByRole("link", { name: "收藏" }).getAttribute("href")).toBe("/explore/collections");
    expect(within(dialog).getByRole("link", { name: "發布" }).getAttribute("href")).toBe("/community/new");
    expect(within(dialog).getByRole("link", { name: "通知 (2)" }).getAttribute("href")).toBe("/community/messages");
    fireEvent.keyDown(document, { key: "Escape" });
    expect(screen.queryByRole("dialog")).toBeNull();
    expect(document.activeElement).toBe(screen.getByRole("button", { name: "開啟導覽選單" }));
  });

  it("uses the same desktop destinations", () => {
    render(<SiteNavigation />);
    const desktop = screen.getByRole("navigation");
    expect(within(desktop).getByRole("link", { name: "我的旅行" }).getAttribute("href")).toBe("/trips");
    expect(within(desktop).getByRole("link", { name: "收藏" }).getAttribute("href")).toBe("/explore/collections");
  });
});
