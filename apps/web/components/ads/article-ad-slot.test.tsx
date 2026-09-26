import { act, render } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { AdsenseDocument } from "./adsense-loader";
import { ArticleAdSlot, LAZY_ROOT_MARGIN } from "./article-ad-slot";

const PUBLISHER = "ca-pub-4140966684432854";
const SLOT = "1234567890";

type Callback = (entries: { isIntersecting: boolean }[]) => void;
const observers: { callback: Callback; options?: IntersectionObserverInit; disconnect: ReturnType<typeof vi.fn> }[] = [];

beforeEach(() => {
  window.adsbygoogle = [];
  observers.length = 0;
  vi.stubGlobal("IntersectionObserver", class {
    disconnect = vi.fn();
    constructor(callback: Callback, options?: IntersectionObserverInit) {
      observers.push({ callback, options, disconnect: this.disconnect });
    }
    observe() {}
  });
});

afterEach(() => {
  vi.unstubAllGlobals();
  delete window.adsbygoogle;
});

describe("ArticleAdSlot", () => {
  it("requests an ad as soon as an eager unit mounts", () => {
    render(<ArticleAdSlot publisherId={PUBLISHER} slotId={SLOT} label="廣告" cmpEnabled />, { wrapper: AdsenseDocument });
    expect(window.adsbygoogle).toHaveLength(1);
    expect(observers).toHaveLength(0);
  });

  it("waits until a lazy unit is near the viewport, then asks exactly once", () => {
    const { container } = render(
      <ArticleAdSlot publisherId={PUBLISHER} slotId={SLOT} label="廣告" cmpEnabled={false} lazy />,
      { wrapper: AdsenseDocument },
    );
    expect(container.querySelector("ins.adsbygoogle")).toBeTruthy();
    // The box is reserved from the start; only the request waits.
    expect(window.adsbygoogle).toHaveLength(0);
    expect(observers).toHaveLength(1);
    expect(observers[0].options?.rootMargin).toBe(LAZY_ROOT_MARGIN);

    act(() => observers[0].callback([{ isIntersecting: false }]));
    expect(window.adsbygoogle).toHaveLength(0);

    act(() => observers[0].callback([{ isIntersecting: true }]));
    expect(window.adsbygoogle).toHaveLength(1);
    expect(window.adsbygoogle?.requestNonPersonalizedAds).toBe(1);
    expect(observers[0].disconnect).toHaveBeenCalled();
  });

  it("renders nothing, and asks for nothing, in a document that never loaded the tag", () => {
    // A tutorial hub or a URL with a query string opens a document without the tag, and the
    // root layout is not rendered again when the reader moves on to another article. That
    // article's units would be boxes nothing ever fills.
    const { container } = render(<ArticleAdSlot publisherId={PUBLISHER} slotId={SLOT} label="廣告" cmpEnabled />);
    expect(container.innerHTML).toBe("");
    expect(window.adsbygoogle).toHaveLength(0);
    expect(observers).toHaveLength(0);
  });

  it("renders nothing for identifiers Google would reject", () => {
    const { container } = render(<ArticleAdSlot publisherId="pub-1" slotId={SLOT} label="廣告" cmpEnabled lazy />, { wrapper: AdsenseDocument });
    expect(container.innerHTML).toBe("");
    expect(window.adsbygoogle).toHaveLength(0);
  });
});
