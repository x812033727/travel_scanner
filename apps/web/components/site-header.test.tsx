import { render, screen, within } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import { SiteHeader } from "./site-header";

vi.mock("./site-navigation", () => ({ SiteNavigation: () => <nav aria-label="Destinations" /> }));
vi.mock("./language-switcher", () => ({ LanguageSwitcher: () => <select aria-label="Language"><option>English</option></select> }));
vi.mock("./theme-switcher", () => ({ ThemeSwitcher: () => <select aria-label="Theme"><option>System</option></select> }));
vi.mock("./site-search/site-search", () => ({ SiteSearch: ({ className }: { className?: string }) => <form role="search" className={className} /> }));
vi.mock("./site-search/site-search-dialog", () => ({ SiteSearchDialog: () => <div data-testid="search-dialog" /> }));

describe("SiteHeader", () => {
  it("always places the desktop language control in the top header", () => {
    render(<SiteHeader />);
    const header = screen.getByRole("banner");
    const language = within(header).getByRole("combobox", { name: "Language" });
    expect(language.parentElement?.className).toContain("hidden lg:flex");
    expect(within(header).getByRole("link", { name: "Mokaair" }).getAttribute("href")).toBe("/");
  });

  it("carries exactly one article search box, for wide screens, and the sheet that opens it elsewhere", () => {
    // One box, whatever navigation mode is on: the search is not a nav link, so it must not
    // depend on which of the three link sets SiteNavigation happens to render.
    render(<SiteHeader />);
    const header = screen.getByRole("banner");
    const boxes = within(header).getAllByRole("search");
    expect(boxes).toHaveLength(1);
    expect(boxes[0].className).toContain("hidden lg:block");
    expect(within(header).getByTestId("search-dialog")).toBeTruthy();
  });

  it("always shows the theme control to the left of the language control", () => {
    // SiteNavigation's own ThemeSwitcher disappears when discovery mode is on
    // (it's mocked away here), so this header copy is the only reachable one
    // in that mode -- it must not be gated the same way.
    render(<SiteHeader />);
    const header = screen.getByRole("banner");
    const theme = within(header).getByRole("combobox", { name: "Theme" });
    const language = within(header).getByRole("combobox", { name: "Language" });
    expect(theme.parentElement).toBe(language.parentElement);
    expect(theme.compareDocumentPosition(language) & Node.DOCUMENT_POSITION_FOLLOWING).toBeTruthy();
  });
});
