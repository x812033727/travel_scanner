import { cleanup, fireEvent, render, screen } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { SiteNavigation } from "@/components/site-navigation";
import { openSiteVisibility } from "@/lib/site-features";

/**
 * The header has three mutually exclusive modes and only one of them reads
 * `primaryNavLinks`. A section added to that list alone is invisible in the other two --
 * the defect 2026-09-11-no-sign-in-entry-in-discovery records. These cases exist so neither
 * content section can regress into that shape.
 */

const mocks = vi.hoisted(() => ({ discovery: vi.fn(), community: vi.fn(), visibility: vi.fn() }));
vi.mock("@/components/mobile-nav", () => ({ MobileNav: () => null }));
vi.mock("@/components/header-auth", () => ({ HeaderAuth: () => null }));
vi.mock("@/components/text-size-switcher", () => ({ TextSizeSwitcher: () => null }));
vi.mock("@/components/theme-switcher", () => ({ ThemeSwitcher: () => null }));
vi.mock("@/components/site-visibility-provider", () => ({ useSiteVisibility: mocks.visibility }));
vi.mock("@/components/community/provider", () => ({ useCommunity: mocks.community }));
vi.mock("@/lib/discovery", () => ({ useDiscoveryStatus: mocks.discovery }));

const flags = (enabled: boolean) => ({
  flags: { enabled, posting_enabled: false }, unread: 0,
});

beforeEach(() => {
  vi.clearAllMocks();
  mocks.visibility.mockReturnValue({ status: "ready", features: openSiteVisibility });
  mocks.community.mockReturnValue(flags(false));
  mocks.discovery.mockReturnValue({ loading: false, enabled: false });
});

// Both first-party content sections are reached the same way and must hold the same line.
describe.each([
  ["旅遊情報攻略", "/guides"],
  ["生活科技", "/life"],
  ["AI 應用", "/ai"],
  ["影片", "/videos"],
])("reaching %s from the header", (name, href) => {
  it("is offered in the default mode", () => {
    render(<SiteNavigation />);
    expect(screen.getByRole("link", { name }).getAttribute("href")).toBe(href);
  });

  it("is offered when discovery mode replaces the primary links", () => {
    mocks.discovery.mockReturnValue({ loading: false, enabled: true });
    render(<SiteNavigation />);
    expect(screen.getByRole("link", { name }).getAttribute("href")).toBe(href);
  });

  it("is offered when the community navigation replaces the primary links", () => {
    mocks.community.mockReturnValue(flags(true));
    render(<SiteNavigation />);
    expect(screen.getByRole("link", { name }).getAttribute("href")).toBe(href);
  });

  it("appears exactly once, so no mode renders it twice", () => {
    for (const mode of [{ discovery: true, community: false }, { discovery: false, community: true }, { discovery: false, community: false }]) {
      mocks.discovery.mockReturnValue({ loading: false, enabled: mode.discovery });
      mocks.community.mockReturnValue(flags(mode.community));
      const { unmount } = render(<SiteNavigation />);
      expect(screen.getAllByRole("link", { name })).toHaveLength(1);
      unmount();
    }
  });

  it("is held back only while the mode is still unknown", () => {
    mocks.discovery.mockReturnValue({ loading: true, enabled: false });
    render(<SiteNavigation />);
    expect(screen.queryByRole("link", { name })).toBeNull();
  });

  it("survives a closed catalog module, because it is first-party content", () => {
    mocks.visibility.mockReturnValue({
      status: "ready",
      features: { ...openSiteVisibility, hotspots_enabled: false },
    });
    render(<SiteNavigation />);
    expect(screen.getByRole("link", { name })).toBeTruthy();
    expect(screen.queryByRole("link", { name: "熱門景點" })).toBeNull();
  });
});

describe("the two sections side by side", () => {
  it("offers both in every mode, so neither hides the other", () => {
    for (const mode of [{ discovery: true, community: false }, { discovery: false, community: true }, { discovery: false, community: false }]) {
      mocks.discovery.mockReturnValue({ loading: false, enabled: mode.discovery });
      mocks.community.mockReturnValue(flags(mode.community));
      const { unmount } = render(<SiteNavigation />);
      expect(screen.getByRole("link", { name: "旅遊情報攻略" }).getAttribute("href")).toBe("/guides");
      expect(screen.getByRole("link", { name: "生活科技" }).getAttribute("href")).toBe("/life");
      unmount();
    }
  });
});

describe("the grouped menus", () => {
  it("puts each section's pages under it, in the document whether or not the menu is open", () => {
    render(<SiteNavigation />);
    expect(screen.getByRole("link", { name: "AI 新聞" }).getAttribute("href")).toBe("/life/topics/ai-news");
    expect(screen.getByRole("link", { name: "旅遊攻略" }).getAttribute("href")).toBe("/guides/howto");
    expect(screen.getByRole("link", { name: "理財投資" }).getAttribute("href")).toBe("/life/topics/finance");
  });

  it("opens and closes a group from its button, and Escape closes it", () => {
    render(<SiteNavigation />);
    const toggle = screen.getByRole("button", { name: "AI 應用選單" });
    expect(toggle.getAttribute("aria-expanded")).toBe("false");
    fireEvent.click(toggle);
    expect(toggle.getAttribute("aria-expanded")).toBe("true");
    fireEvent.keyDown(toggle, { key: "Escape" });
    expect(toggle.getAttribute("aria-expanded")).toBe("false");
  });

  it("keeps the travel tools out of the modes that carry their own", () => {
    render(<SiteNavigation />);
    expect(screen.getByRole("button", { name: "旅行工具選單" })).toBeTruthy();
    cleanup();
    mocks.discovery.mockReturnValue({ loading: false, enabled: true });
    render(<SiteNavigation />);
    expect(screen.queryByRole("button", { name: "旅行工具選單" })).toBeNull();
    expect(screen.getByRole("button", { name: "AI 應用選單" })).toBeTruthy();
  });

  it("drops a group whose every page is switched off", () => {
    mocks.visibility.mockReturnValue({
      status: "ready",
      features: { ...openSiteVisibility, trips_enabled: false, alerts_enabled: false, flight_status_enabled: false, airline_fares_enabled: false, pricing_enabled: false },
    });
    render(<SiteNavigation />);
    expect(screen.queryByText("旅行工具")).toBeNull();
  });
});
