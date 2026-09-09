import "@testing-library/jest-dom/vitest";
import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { StrictMode } from "react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import * as policy from "@/lib/stay22-script";
import { Stay22Script } from "./stay22-script";
const lmaId = "6aa15a455ff1d17f658d1692";

describe("isolated Stay22 loader", () => {
  beforeEach(() => {
    vi.spyOn(policy, "isStay22ScriptOrigin").mockReturnValue(true);
    Object.defineProperty(document, "referrer", { configurable: true, value: "" });
    window.history.replaceState(null, "", "/");
    Object.defineProperty(document, "referrer", { configurable: true, value: "" });
  });
  afterEach(() => {
    document.getElementById(policy.STAY22_SCRIPT_ELEMENT_ID)?.remove();
    delete window.Stay22;
    Object.defineProperty(navigator, "doNotTrack", { configurable: true, value: null });
    Object.defineProperty(navigator, "globalPrivacyControl", { configurable: true, value: undefined });
    window.history.replaceState(null, "", "/");
    vi.restoreAllMocks();
  });
  it("loads the fixed official bootstrap once under StrictMode", async () => {
    render(<StrictMode><Stay22Script enabled lmaId={lmaId} locale="zh-TW" /></StrictMode>);
    await waitFor(() => expect(document.querySelectorAll(`#${policy.STAY22_SCRIPT_ELEMENT_ID}`)).toHaveLength(1));
    expect(document.getElementById(policy.STAY22_SCRIPT_ELEMENT_ID)).toHaveAttribute("src", policy.STAY22_SCRIPT_URL);
    expect(window.Stay22?.params?.lmaID).toBe(lmaId);
  });
  it.each(["off", "origin", "dnt", "gpc", "query", "fragment"])("does not load for %s", (condition) => {
    if (condition === "origin") vi.mocked(policy.isStay22ScriptOrigin).mockReturnValue(false);
    if (condition === "dnt") Object.defineProperty(navigator, "doNotTrack", { configurable: true, value: "1" });
    if (condition === "gpc") Object.defineProperty(navigator, "globalPrivacyControl", { configurable: true, value: true });
    if (condition === "query") window.history.replaceState(null, "", "/?private=value");
    if (condition === "fragment") window.history.replaceState(null, "", "/#private");
    render(<Stay22Script enabled={condition !== "off"} lmaId={lmaId} locale="zh-TW" />);
    expect(document.getElementById(policy.STAY22_SCRIPT_ELEMENT_ID)).toBeNull();
    expect(window.Stay22).toBeUndefined();
  });
  it("reports script failure without replacing or removing original links", async () => {
    render(<><a href="https://www.booking.com/hotel/jp/example.html">Booking.com</a><Stay22Script enabled lmaId={lmaId} locale="zh-TW" /></>);
    fireEvent.error(document.getElementById(policy.STAY22_SCRIPT_ELEMENT_ID)!);
    expect(await screen.findByRole("status")).toHaveTextContent("原始飯店連結仍可使用");
    expect(screen.getByRole("link", { name: "Booking.com" })).toHaveAttribute("href", "https://www.booking.com/hotel/jp/example.html");
  });
  it("blocks private referrers before creating any vendor global or SDK request", async () => {
    Object.defineProperty(document, "referrer", { configurable: true, value: "https://mokaair.com/zh-TW/trips/private-id?note=private" });
    render(<Stay22Script enabled lmaId={lmaId} locale="zh-TW" />);
    expect(document.getElementById(policy.STAY22_SCRIPT_ELEMENT_ID)).toBeNull();
    expect(window.Stay22).toBeUndefined();
    expect(await screen.findByRole("status")).toHaveTextContent("原始飯店連結仍可使用");
  });
});
