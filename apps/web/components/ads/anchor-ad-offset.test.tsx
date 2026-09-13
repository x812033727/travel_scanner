import { render } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { ANCHOR_BOTTOM_PROPERTY, ANCHOR_TOP_PROPERTY, AnchorAdOffset, measureAnchorAds } from "./anchor-ad-offset";

const VIEWPORT = 800;

/** An `ins.adsbygoogle` the way the tag inserts it, occupying `top`..`bottom` of the viewport. */
function unit({ top, bottom, fixed = true }: { top: number; bottom: number; fixed?: boolean }) {
  const element = document.createElement("ins");
  element.className = "adsbygoogle";
  if (fixed) element.style.position = "fixed";
  element.getBoundingClientRect = () => ({
    top, bottom, height: bottom - top, left: 0, right: 400, width: 400, x: 0, y: top, toJSON: () => ({}),
  });
  document.body.append(element);
  return element;
}

beforeEach(() => {
  vi.stubGlobal("innerHeight", VIEWPORT);
  // jsdom paints no frames. Like the real thing, the callback must run after the call returns.
  vi.stubGlobal("requestAnimationFrame", (callback: FrameRequestCallback) => window.setTimeout(() => callback(0), 0));
  vi.stubGlobal("cancelAnimationFrame", (handle: number) => window.clearTimeout(handle));
});

afterEach(() => {
  vi.unstubAllGlobals();
  document.body.innerHTML = "";
  document.documentElement.style.removeProperty(ANCHOR_TOP_PROPERTY);
  document.documentElement.style.removeProperty(ANCHOR_BOTTOM_PROPERTY);
});

describe("measureAnchorAds", () => {
  it("measures an anchor at either edge", () => {
    unit({ top: VIEWPORT - 90, bottom: VIEWPORT });
    expect(measureAnchorAds(document, VIEWPORT)).toEqual({ top: 0, bottom: 90 });
    document.body.innerHTML = "";
    unit({ top: 0, bottom: 60 });
    expect(measureAnchorAds(document, VIEWPORT)).toEqual({ top: 60, bottom: 0 });
  });

  it("counts only the part of a collapsed anchor still on screen", () => {
    unit({ top: VIEWPORT - 20, bottom: VIEWPORT + 70 });
    expect(measureAnchorAds(document, VIEWPORT)).toEqual({ top: 0, bottom: 20 });
  });

  it("ignores in-article units, vignettes and anything off screen", () => {
    unit({ top: 300, bottom: VIEWPORT, fixed: false });
    unit({ top: 0, bottom: VIEWPORT }); // a vignette covers the whole viewport
    unit({ top: VIEWPORT, bottom: VIEWPORT + 90 }); // a closed anchor slid fully away
    unit({ top: 300, bottom: 400 }); // fixed, but touching neither edge
    expect(measureAnchorAds(document, VIEWPORT)).toEqual({ top: 0, bottom: 0 });
  });
});

describe("AnchorAdOffset", () => {
  const property = (name: string) => document.documentElement.style.getPropertyValue(name);

  it("publishes the anchor's height once the tag inserts it, and clears it when it goes", async () => {
    const { unmount } = render(<AnchorAdOffset />);
    expect(property(ANCHOR_BOTTOM_PROPERTY)).toBe("");

    const anchor = unit({ top: VIEWPORT - 90, bottom: VIEWPORT });
    await vi.waitFor(() => expect(property(ANCHOR_BOTTOM_PROPERTY)).toBe("90px"));
    expect(property(ANCHOR_TOP_PROPERTY)).toBe("");

    anchor.remove();
    await vi.waitFor(() => expect(property(ANCHOR_BOTTOM_PROPERTY)).toBe(""));

    unit({ top: 0, bottom: 50 });
    await vi.waitFor(() => expect(property(ANCHOR_TOP_PROPERTY)).toBe("50px"));
    unmount();
    expect(property(ANCHOR_TOP_PROPERTY)).toBe("");
  });

  it("follows the anchor when the reader collapses it", async () => {
    render(<AnchorAdOffset />);
    const anchor = unit({ top: VIEWPORT - 90, bottom: VIEWPORT });
    await vi.waitFor(() => expect(property(ANCHOR_BOTTOM_PROPERTY)).toBe("90px"));
    anchor.getBoundingClientRect = () => ({
      top: VIEWPORT - 20, bottom: VIEWPORT + 70, height: 90, left: 0, right: 400, width: 400, x: 0, y: VIEWPORT - 20, toJSON: () => ({}),
    });
    anchor.style.transform = "translateY(70px)";
    await vi.waitFor(() => expect(property(ANCHOR_BOTTOM_PROPERTY)).toBe("20px"));
  });
});
