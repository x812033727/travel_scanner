import { render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import { closedSiteVisibility, openSiteVisibility } from "@/lib/site-features";
import { ExploreSwitch } from "./explore-switch";
import { SiteVisibilityProvider } from "./site-visibility-provider";

const { pathname } = vi.hoisted(() => ({ pathname: { current: "/foods" } }));
vi.mock("@/i18n/navigation", () => ({
  Link: ({ href, children, ...props }: React.AnchorHTMLAttributes<HTMLAnchorElement> & { href: string }) => <a href={href} {...props}>{children}</a>,
  usePathname: () => pathname.current,
}));

describe("ExploreSwitch", () => {
  it("shows hotspots and foods as sibling tabs and marks the current one", () => {
    render(<ExploreSwitch />);
    const links = screen.getAllByRole("link");
    expect(links.map((link) => link.getAttribute("href"))).toEqual(["/hotspots", "/foods"]);
    expect(links[1].getAttribute("aria-current")).toBe("page");
    expect(links[0].getAttribute("aria-current")).toBeNull();
  });

  it("renders nothing when hotspots are turned off, leaving foods on its own", () => {
    render(
      <SiteVisibilityProvider state={{ status: "ready", features: { ...openSiteVisibility, hotspots_enabled: false } }}>
        <ExploreSwitch />
      </SiteVisibilityProvider>,
    );
    expect(screen.queryByRole("link")).toBeNull();
  });

  it("keeps both tabs when the switches could not be read", () => {
    render(
      <SiteVisibilityProvider state={{ status: "unavailable", features: closedSiteVisibility }}>
        <ExploreSwitch />
      </SiteVisibilityProvider>,
    );
    expect(screen.getAllByRole("link")).toHaveLength(2);
  });
});
