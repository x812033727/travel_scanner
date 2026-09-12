import { render, screen } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { TravelExplore } from "./explore";
import { openSiteVisibility } from "@/lib/site-features";

/**
 * Both of these grids are built from `primaryNavLinks` and titled as travel tools, so the
 * lifestyle section must not arrive in them just because it joined that list. Its entry
 * points are the header, the footer and the phone header.
 */

const mocks = vi.hoisted(() => ({ community: vi.fn(), visibility: vi.fn() }));
vi.mock("@/components/site-visibility-provider", () => ({ useSiteVisibility: mocks.visibility }));
vi.mock("./provider", () => ({ useCommunity: mocks.community }));

beforeEach(() => {
  vi.clearAllMocks();
  mocks.visibility.mockReturnValue({ status: "ready", features: openSiteVisibility });
  mocks.community.mockReturnValue({ flags: { enabled: true, posting_enabled: false }, unread: 0 });
});

describe("the community travel grid", () => {
  it("offers the travel sections but not the lifestyle one", () => {
    render(<TravelExplore />);
    expect(screen.getByRole("link", { name: "旅遊情報攻略" }).getAttribute("href")).toBe("/guides");
    expect(screen.queryByRole("link", { name: "生活分享" })).toBeNull();
  });
});
