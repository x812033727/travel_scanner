import { act, cleanup, fireEvent, render, screen } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { SiteSearchDialog, openSiteSearch } from "./site-search-dialog";

const mock = vi.hoisted(() => ({ api: vi.fn(), push: vi.fn() }));
vi.mock("@/lib/api", async (original) => ({ ...await original<typeof import("@/lib/api")>(), api: mock.api }));
vi.mock("@/i18n/navigation", () => ({ useRouter: () => ({ push: mock.push }), usePathname: () => "/" }));

beforeEach(() => vi.clearAllMocks());
afterEach(cleanup);

describe("SiteSearchDialog", () => {
  it("renders nothing until asked", () => {
    render(<SiteSearchDialog />);
    expect(screen.queryByRole("dialog")).toBeNull();
    expect(screen.queryByRole("search")).toBeNull();
  });

  it("opens on ⌘K or Ctrl+K with focus in the box, toggles on the same key, and closes on Escape", () => {
    render(<><button type="button">opener</button><SiteSearchDialog /></>);
    const opener = screen.getByRole("button", { name: "opener" });
    opener.focus();
    fireEvent.keyDown(window, { key: "k", metaKey: true });
    const dialog = screen.getByRole("dialog", { name: "搜尋文章" });
    expect(dialog.getAttribute("aria-modal")).toBe("true");
    expect(document.activeElement).toBe(screen.getByRole("combobox"));
    expect(document.body.style.overflow).toBe("hidden");
    fireEvent.keyDown(window, { key: "K", ctrlKey: true });
    expect(screen.queryByRole("dialog")).toBeNull();
    fireEvent.keyDown(window, { key: "k", ctrlKey: true });
    expect(screen.getByRole("dialog")).toBeTruthy();
    fireEvent.keyDown(document, { key: "Escape" });
    expect(screen.queryByRole("dialog")).toBeNull();
    expect(document.body.style.overflow).toBe("");
    // Focus goes back to where it was, not to the top of the page.
    expect(document.activeElement).toBe(opener);
  });

  it("opens from the shared verb the phone header calls, and closes from its own button", () => {
    render(<SiteSearchDialog />);
    act(() => openSiteSearch());
    expect(screen.getByRole("dialog")).toBeTruthy();
    fireEvent.click(screen.getByRole("button", { name: "關閉搜尋" }));
    expect(screen.queryByRole("dialog")).toBeNull();
  });

  it("leaves a shortcut alone when something else already handled it, and ignores Shift/Alt variants", () => {
    render(<SiteSearchDialog />);
    const handled = new KeyboardEvent("keydown", { key: "k", metaKey: true, cancelable: true });
    handled.preventDefault();
    act(() => { window.dispatchEvent(handled); });
    fireEvent.keyDown(window, { key: "k", metaKey: true, shiftKey: true });
    fireEvent.keyDown(window, { key: "k", ctrlKey: true, altKey: true });
    expect(screen.queryByRole("dialog")).toBeNull();
  });
});
