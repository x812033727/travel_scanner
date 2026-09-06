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

// The switcher writes the choice back through the API; the footer only has to place it.
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

  it("offers the language choice and the year", () => {
    renderAt("/");
    expect(screen.getByTestId("language-switcher")).toBeTruthy();
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
