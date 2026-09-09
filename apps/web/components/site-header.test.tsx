import { render, screen, within } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import { SiteHeader } from "./site-header";

vi.mock("./site-navigation", () => ({ SiteNavigation: () => <nav aria-label="Destinations" /> }));
vi.mock("./language-switcher", () => ({ LanguageSwitcher: () => <select aria-label="Language"><option>English</option></select> }));

describe("SiteHeader", () => {
  it("always places the desktop language control in the top header", () => {
    render(<SiteHeader />);
    const header = screen.getByRole("banner");
    const language = within(header).getByRole("combobox", { name: "Language" });
    expect(language.parentElement?.className).toContain("hidden lg:flex");
    expect(within(header).getByRole("link", { name: "Mokaair" }).getAttribute("href")).toBe("/");
  });
});
