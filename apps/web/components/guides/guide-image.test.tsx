import { act, fireEvent, render, screen } from "@testing-library/react";
import { renderToString } from "react-dom/server";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { GuideImage } from "./guide-image";

const src = "/guides/sample/hero.jpg";
const props = { src, alt: "Article cover", width: 1600, height: 900, loading: "lazy" as const };
const advance = (ms: number) => act(() => { vi.advanceTimersByTime(ms); });

beforeEach(() => {
  vi.useFakeTimers();
  vi.spyOn(Math, "random").mockReturnValue(0);
});
afterEach(() => { vi.restoreAllMocks(); vi.useRealTimers(); });

describe("GuideImage", () => {
  it("keeps the original URL and reserved dimensions in server HTML", () => {
    const html = renderToString(<GuideImage {...props} />);
    expect(html).toContain(`src="${src}"`);
    expect(html).toContain('width="1600"');
    expect(html).toContain('height="900"');
    expect(html).toContain('loading="lazy"');
    expect(html).not.toContain("image_retry");
  });

  it("backs off twice, deduplicates errors and stops after persistent failure", () => {
    render(<GuideImage {...props} />);
    const img = screen.getByRole("img");
    fireEvent.error(img);
    fireEvent.error(img);
    advance(1999);
    expect(img.getAttribute("src")).toBe(src);
    advance(1);
    expect(img.getAttribute("src")).toBe(`${src}?image_retry=1`);
    fireEvent.error(img);
    advance(4999);
    expect(img.getAttribute("src")).toBe(`${src}?image_retry=1`);
    advance(1);
    expect(img.getAttribute("src")).toBe(`${src}?image_retry=2`);
    fireEvent.error(img);
    advance(60_000);
    expect(img.getAttribute("src")).toBe(`${src}?image_retry=2`);
    expect(vi.getTimerCount()).toBe(0);
  });

  it("recovers when an error happened before hydration attached handlers", () => {
    vi.spyOn(HTMLImageElement.prototype, "complete", "get").mockReturnValue(true);
    vi.spyOn(HTMLImageElement.prototype, "naturalWidth", "get").mockReturnValue(0);
    render(<GuideImage {...props} />);
    advance(2000);
    expect(screen.getByRole("img").getAttribute("src")).toBe(`${src}?image_retry=1`);
    fireEvent.load(screen.getByRole("img"));
    advance(60_000);
    expect(screen.getByRole("img").getAttribute("src")).toBe(`${src}?image_retry=1`);
  });

  it("leaves pending lazy images alone and cancels a retry after success", () => {
    render(<GuideImage {...props} />);
    advance(60_000);
    expect(screen.getByRole("img").getAttribute("src")).toBe(src);
    fireEvent.error(screen.getByRole("img"));
    fireEvent.load(screen.getByRole("img"));
    advance(60_000);
    expect(screen.getByRole("img").getAttribute("src")).toBe(src);
  });

  it("cancels old retries on article changes and unmount", () => {
    const { rerender, unmount } = render(<GuideImage {...props} />);
    fireEvent.error(screen.getByRole("img"));
    rerender(<GuideImage {...props} src="/guides/other/diagram-1.svg" />);
    advance(60_000);
    expect(screen.getByRole("img").getAttribute("src")).toBe("/guides/other/diagram-1.svg");
    fireEvent.error(screen.getByRole("img"));
    advance(2000);
    expect(screen.getByRole("img").getAttribute("src")).toBe("/guides/other/diagram-1.svg?image_retry=1");
    fireEvent.error(screen.getByRole("img"));
    unmount();
    expect(vi.getTimerCount()).toBe(0);
  });
});
