import { render, screen, within } from "@testing-library/react";
import type React from "react";
import { describe, expect, it, vi } from "vitest";
import { SiteFooter } from "./site-footer";

const pathname = vi.hoisted(() => ({ value: "/" }));

// Declared in full rather than spread over the global mock: importing the real module pulls
// in next/navigation, which does not resolve outside a Next runtime.
vi.mock("@/i18n/navigation", () => ({
  Link: ({ href, children, ...props }: React.AnchorHTMLAttributes<HTMLAnchorElement> & { href: string }) => (
    <a href={href} {...props}>{children}</a>
  ),
  usePathname: () => pathname.value,
  useRouter: () => ({ push: vi.fn(), replace: vi.fn(), refresh: vi.fn() }),
}));

// Language controls live in the top header, not in the footer.
vi.mock("@/components/language-switcher", () => ({
  LanguageSwitcher: () => <div data-testid="language-switcher" />,
}));

function renderAt(path: string) {
  pathname.value = path;
  return render(<SiteFooter year={2026} />);
}

describe("SiteFooter", () => {
  it("carries the four links a reader goes looking for", () => {
    renderAt("/");
    const footer = screen.getByRole("contentinfo");
    for (const name of ["隱私權政策", "服務條款", "關於 Mokaair", "聯絡我們"]) {
      expect(within(footer).getByRole("link", { name }), name).toBeTruthy();
    }
  });

  it("points each link at its own page", () => {
    renderAt("/");
    const href = (name: string) =>
      screen.getByRole("link", { name }).getAttribute("href");
    expect(href("隱私權政策")).toBe("/privacy");
    expect(href("服務條款")).toBe("/terms");
    expect(href("關於 Mokaair")).toBe("/about");
    expect(href("聯絡我們")).toBe("/contact");
  });

  it("carries the only site-wide entry point to the destination guides", () => {
    // The 33 city guides are otherwise reachable only from each other and the sitemap. This
    // footer renders on the server on every public page, which the home page rail does not.
    renderAt("/");
    const link = within(screen.getByRole("contentinfo")).getByRole("link", { name: "目的地" });
    expect(link.getAttribute("href")).toBe("/destinations");
  });

  it("carries the only entry point to the guides that survives a first paint", () => {
    // The header renders the section only after the discovery switch resolves; this link is
    // in the response body of every public page regardless.
    // Through renderAt, not a bare render: the mocked pathname is module-level state that
    // the "stays out of /admin" cases below leave pointing at a path this footer refuses to
    // render on. Shuffled, those ran first and this one asserted on an empty document.
    renderAt("/");
    const footer = screen.getByRole("contentinfo");
    const link = within(footer).getByRole("link", { name: "情報攻略" });
    expect(link.getAttribute("href")).toBe("/guides");
  });

  it("keeps the year without duplicating the top-header language control", () => {
    renderAt("/");
    expect(screen.queryByTestId("language-switcher")).toBeNull();
    expect(screen.getByText("© 2026 Mokaair")).toBeTruthy();
  });

  it.each([
    ["/admin", "the admin console is not a public page"],
    ["/admin/settings", "and neither are its sections"],
    ["/trips/abc123", "the planner is a full-screen shell"],
  ])("stays out of %s", (path) => {
    const { container } = renderAt(path);
    expect(container.firstChild).toBeNull();
  });

  it.each(["/", "/hotspots", "/foods", "/trips", "/account", "/alerts", "/pricing"])(
    "appears on %s",
    (path) => {
      renderAt(path);
      expect(screen.getByRole("contentinfo")).toBeTruthy();
    },
  );

  it("keeps /trips itself, which is a listing rather than the planner", () => {
    renderAt("/trips");
    expect(screen.getByRole("contentinfo")).toBeTruthy();
  });
});
