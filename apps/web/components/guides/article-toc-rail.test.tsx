import { act, cleanup, fireEvent, render, screen, within } from "@testing-library/react";
import { afterAll, afterEach, beforeAll, beforeEach, describe, expect, it, vi } from "vitest";
import { ArticleMobileProgress, ArticleTocRail } from "./article-toc-rail";

const headings = [{ id: "section-1", text: "重點比較" }, { id: "section-2", text: "常見問題" }];
const labels = { backToTopLabel: "回到頂部", contentsLabel: "本篇目錄", closeLabel: "關閉目錄" };

beforeEach(() => {
  vi.spyOn(Element.prototype, "clientHeight", "get").mockReturnValue(800);
  vi.spyOn(Element.prototype, "scrollHeight", "get").mockReturnValue(2000);
  vi.stubGlobal("scrollY", 600);
});

afterEach(() => {
  cleanup();
  vi.unstubAllGlobals();
  vi.restoreAllMocks();
});

// jsdom has no native top layer. Escape and native focus restoration need a browser.
const dialogPrototype = HTMLDialogElement.prototype;
const showModal = Object.getOwnPropertyDescriptor(dialogPrototype, "showModal");
const close = Object.getOwnPropertyDescriptor(dialogPrototype, "close");
beforeAll(() => {
  Object.defineProperty(dialogPrototype, "showModal", {
    configurable: true, value(this: HTMLDialogElement) { this.open = true; },
  });
  Object.defineProperty(dialogPrototype, "close", {
    configurable: true, value(this: HTMLDialogElement) {
      this.open = false;
      this.dispatchEvent(new Event("close"));
    },
  });
});
afterAll(() => {
  for (const [name, descriptor] of [["showModal", showModal], ["close", close]] as const) {
    if (descriptor) Object.defineProperty(dialogPrototype, name, descriptor);
    else Reflect.deleteProperty(dialogPrototype, name);
  }
});

describe("article reading controls", () => {
  it("keeps document progress and the separate back-to-top action on guides", () => {
    render(<ArticleMobileProgress {...labels} headings={headings} />);
    const trigger = screen.getByRole("button", { name: labels.contentsLabel });
    expect(screen.getByRole("button", { name: labels.backToTopLabel })).toBeTruthy();
    fireEvent.click(trigger);
    const dialog = screen.getByRole("dialog", { name: labels.contentsLabel });
    expect(within(dialog).getByText("50%")).toBeTruthy();
    const first = within(dialog).getByRole("link", { name: /重點比較/ });
    expect(first.getAttribute("href")).toBe("#section-1");
    fireEvent.click(first);
    expect(screen.queryByRole("dialog")).toBeNull();
    vi.stubGlobal("scrollY", 320);
    fireEvent.scroll(window);
    expect(screen.queryByRole("button", { name: labels.contentsLabel })).toBeNull();
  });

  it("finishes at the final visible news line and hides the control over further reading", () => {
    const { container } = render(<>
      <ArticleMobileProgress {...labels} newsReading />
      <ArticleTocRail {...labels} headings={headings} progressLabel="閱讀進度" newsReading />
      <article><div data-news-body>正文</div><section>延伸閱讀</section></article>
    </>);
    const story = container.querySelector("[data-news-body]")!;
    const nav = document.createElement("nav");
    nav.className = "app-bottom-nav";
    container.append(nav);
    const bodyRect = vi.spyOn(story, "getBoundingClientRect");
    bodyRect.mockReturnValue(new DOMRect(0, -400, 390, 1121));
    vi.spyOn(nav, "getBoundingClientRect").mockReturnValue(new DOMRect(0, 720, 390, 80));
    fireEvent.scroll(window);
    const progress = screen.getByRole("progressbar");
    expect(progress.getAttribute("aria-valuenow")).toBe("99");
    expect(container.querySelector("div.fixed button")?.textContent).toBe(labels.backToTopLabel);
    // Resizing or an expanding chapter can move the last line without a scroll event.
    bodyRect.mockReturnValue(new DOMRect(0, -400, 390, 1120));
    fireEvent.resize(window);
    expect(progress.getAttribute("aria-valuenow")).toBe("100");
    expect(container.querySelector("div.fixed button")).toBeNull();
    expect(container.querySelector("[aria-hidden=true].fixed > div")?.getAttribute("style")).toContain("100%");
  });

  it("offers one news trigger, wraps keyboard focus, and hands focus to the chosen chapter", () => {
    const desktop = Object.assign(new EventTarget(), { matches: false });
    vi.stubGlobal("matchMedia", () => desktop);
    const { container } = render(<>
      <ArticleMobileProgress {...labels} headings={headings} newsReading />
      <article><div data-news-body><h2 id="section-1">重點比較</h2></div></article>
      <ArticleTocRail {...labels} headings={headings} progressLabel="閱讀進度" newsReading />
    </>);
    vi.spyOn(container.querySelector("[data-news-body]")!, "getBoundingClientRect")
      .mockReturnValue(new DOMRect(0, -400, 390, 1800));
    fireEvent.scroll(window);
    const trigger = screen.getByRole("button", { name: labels.contentsLabel });
    expect(container.querySelectorAll("div.fixed button")).toHaveLength(1);
    fireEvent.click(trigger);
    const dialog = screen.getByRole("dialog", { name: labels.contentsLabel });
    const close = within(dialog).getByRole("button", { name: labels.closeLabel });
    expect(document.activeElement).toBe(close);
    fireEvent.keyDown(close, { key: "Tab", shiftKey: true });
    const top = within(dialog).getByRole("button", { name: labels.backToTopLabel });
    expect(document.activeElement).toBe(top);
    fireEvent.keyDown(top, { key: "Tab" });
    expect(document.activeElement).toBe(close);
    fireEvent.click(within(dialog).getByRole("link", { name: /重點比較/ }));
    expect(screen.queryByRole("dialog")).toBeNull();
    expect(document.activeElement?.id).toBe("section-1");
    fireEvent.click(trigger);
    desktop.matches = true;
    act(() => { desktop.dispatchEvent(new Event("change")); });
    expect(screen.queryByRole("dialog")).toBeNull();
    expect(document.activeElement).toBe(container.querySelector("[data-article-toc] a[aria-current]"));
  });
});
