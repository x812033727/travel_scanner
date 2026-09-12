import { render, screen } from "@testing-library/react";
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
  ["生活分享", "/life"],
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
      expect(screen.getByRole("link", { name: "生活分享" }).getAttribute("href")).toBe("/life");
      unmount();
    }
  });
});
