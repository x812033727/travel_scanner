import { fireEvent, render, screen } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { PartnerLink } from "./partner-link";

const link = {
  key: "0123456789abcdef",
  partner: "hostinger",
  display_name: "Hostinger",
  url: "https://www.hostinger.com/tw/vps-hosting?aff_id=12345",
};
const clickPath = "/api/travel/guides/life/claude-code-vps/partner-links/0123456789abcdef/click?locale=zh-TW";
const labels = { badge: "合作連結", newTab: "另開新分頁" };

function draw(note?: string) {
  render(<PartnerLink link={link} label="看 VPS 方案" note={note} clickPath={clickPath} labels={labels} />);
  return screen.getByRole("link", { name: /看 VPS 方案/ });
}

/** Stops jsdom from attempting the cross-origin navigation, after the component's own handler ran. */
function swallowNavigation(event: Event) {
  if (event.target instanceof Element && event.target.closest("a")) event.preventDefault();
}

let fetchMock: ReturnType<typeof vi.fn>;
beforeEach(() => {
  fetchMock = vi.fn().mockResolvedValue({ ok: true, status: 204 });
  vi.stubGlobal("fetch", fetchMock);
  window.addEventListener("click", swallowNavigation);
});
afterEach(() => {
  window.removeEventListener("click", swallowNavigation);
  vi.unstubAllGlobals();
});

describe("PartnerLink", () => {
  it("goes straight to the partner as a sponsored link that keeps this site as the referrer", () => {
    const anchor = draw();
    expect(anchor.getAttribute("href")).toBe(link.url);
    expect(anchor.getAttribute("target")).toBe("_blank");
    const rel = (anchor.getAttribute("rel") ?? "").split(/\s+/);
    expect(rel).toContain("sponsored");
    expect(rel).toContain("noopener");
    // The partner's terms forbid hiding the traffic source; noreferrer would do exactly that.
    expect(rel).not.toContain("noreferrer");
    expect(anchor.getAttribute("referrerpolicy")).toBe("strict-origin-when-cross-origin");
    expect(anchor.getAttribute("aria-label")).toBe("看 VPS 方案 · Hostinger · 另開新分頁");
  });

  it("marks the link as paid beside it and names the partner", () => {
    draw("本站就架在這個方案上");
    expect(screen.getByText("合作連結")).toBeTruthy();
    expect(screen.getByText("Hostinger")).toBeTruthy();
    expect(screen.getByText("本站就架在這個方案上")).toBeTruthy();
  });

  it("counts a click with a keepalive POST and never holds the navigation back", () => {
    const anchor = draw();
    // The document sees the event after the component's handler and before the window-level
    // swallow, so this is what a browser would act on.
    let prevented: boolean | null = null;
    const observe = (event: Event) => { prevented = event.defaultPrevented; };
    document.addEventListener("click", observe);
    try {
      fireEvent.click(anchor);
    } finally {
      document.removeEventListener("click", observe);
    }
    expect(prevented).toBe(false);
    expect(fetchMock).toHaveBeenCalledTimes(1);
    const [path, init] = fetchMock.mock.calls[0];
    expect(path).toBe(clickPath);
    expect(init).toMatchObject({ method: "POST", keepalive: true, credentials: "same-origin", cache: "no-store" });
  });

  it("counts a middle click, which opens the link without a click event, but not a right click", () => {
    const anchor = draw();
    fireEvent(anchor, new MouseEvent("auxclick", { bubbles: true, button: 2 }));
    expect(fetchMock).not.toHaveBeenCalled();
    fireEvent(anchor, new MouseEvent("auxclick", { bubbles: true, button: 1 }));
    expect(fetchMock).toHaveBeenCalledTimes(1);
  });

  it("swallows a count that fails, whether the request rejects or fetch itself throws", async () => {
    // A rejection left unhandled here would fail the whole vitest run, which is the assertion.
    fetchMock.mockRejectedValueOnce(new Error("offline"));
    const anchor = draw();
    fireEvent.click(anchor);
    await new Promise((resolve) => setTimeout(resolve, 0));
    vi.stubGlobal("fetch", vi.fn(() => { throw new TypeError("keepalive body quota exceeded"); }));
    expect(() => fireEvent.click(anchor)).not.toThrow();
  });
});
