import type { AnchorHTMLAttributes } from "react";
import { act, cleanup, fireEvent, render, screen } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { SiteSearchDialog, openSiteSearch } from "./site-search-dialog";

const mock = vi.hoisted(() => ({ api: vi.fn(), push: vi.fn() }));
vi.mock("@/lib/api", async (original) => ({ ...await original<typeof import("@/lib/api")>(), api: mock.api }));
vi.mock("@/i18n/navigation", () => ({
  Link: ({ href, children, ...props }: AnchorHTMLAttributes<HTMLAnchorElement> & { href: string }) => (
    <a href={href} {...props}>{children}</a>
  ),
  useRouter: () => ({ push: mock.push }),
  usePathname: () => "/",
}));

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

  it("opens from the shared verb the phone header calls, offers hot-topic shortcuts, and closes when clicked", () => {
    render(<SiteSearchDialog />);
    act(() => openSiteSearch());
    expect(screen.getByRole("dialog")).toBeTruthy();
    const techNews = screen.getByRole("link", { name: "科技新聞" });
    expect(techNews.getAttribute("href")).toBe("/life/topics/tech-news");
    fireEvent.click(techNews);
    expect(screen.queryByRole("dialog")).toBeNull();
    act(() => openSiteSearch());
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

  it("loads live trending articles when opened and closes on click", async () => {
    mock.api.mockResolvedValueOnce({
      articles: [
        {
          kind: "life",
          slug: "gemini-cli-guide",
          title: "Gemini CLI 完整教學",
          description: "快速上手",
          published_at: "2026-11-10T00:00:00Z",
          updated_at: "2026-11-10T00:00:00Z",
          topics: [{ slug: "ai", label: "AI 專區" }],
        },
      ],
    });
    render(<SiteSearchDialog />);
    await act(async () => {
      openSiteSearch();
    });
    const trending = await screen.findByTestId("search-trending");
    expect(trending).toBeTruthy();
    const link = screen.getByRole("link", { name: /Gemini CLI 完整教學/ });
    expect(link.getAttribute("href")).toBe("/life/gemini-cli-guide");
    fireEvent.click(link);
    expect(screen.queryByRole("dialog")).toBeNull();
  });
});
