import { render } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { documentNavigation } from "@/lib/private-routes";
import { TRAVELPAYOUTS_DRIVE_SCRIPT_URL } from "@/lib/travelpayouts-drive";

const navigation = vi.hoisted(() => ({ pathname: "/zh-TW/life/n8n-ai-automation-guide" }));
vi.mock("next/navigation", () => ({ usePathname: () => navigation.pathname }));

import { PrivateRouteIsolation } from "./private-route-isolation";

describe("PrivateRouteIsolation", () => {
  let assign: ReturnType<typeof vi.spyOn>;
  let reload: ReturnType<typeof vi.spyOn>;
  // jsdom logs "not implemented: navigation" for a click nobody prevents; this keeps the
  // clicks the component lets through from reaching it, after the component has decided.
  const swallow = (event: Event) => event.preventDefault();

  beforeEach(() => {
    assign = vi.spyOn(documentNavigation, "assign").mockImplementation(() => undefined);
    reload = vi.spyOn(documentNavigation, "reload").mockImplementation(() => undefined);
    document.addEventListener("click", swallow);
  });

  afterEach(() => {
    vi.restoreAllMocks();
    document.removeEventListener("click", swallow);
    document.querySelectorAll("script, a").forEach((element) => element.remove());
    sessionStorage.clear();
    navigation.pathname = "/zh-TW/life/n8n-ai-automation-guide";
  });

  function loadDrive() {
    const script = document.createElement("script");
    script.src = TRAVELPAYOUTS_DRIVE_SCRIPT_URL;
    document.head.append(script);
  }

  function link(href: string, attributes: Record<string, string> = {}) {
    const anchor = document.createElement("a");
    anchor.href = href;
    anchor.textContent = "go";
    for (const [name, value] of Object.entries(attributes)) anchor.setAttribute(name, value);
    document.body.append(anchor);
    return anchor;
  }

  it("turns a link into a private page into a full load once a third-party script ran", () => {
    loadDrive();
    render(<PrivateRouteIsolation />);
    link("/zh-TW/trips").click();
    expect(assign).toHaveBeenCalledWith(`${location.origin}/zh-TW/trips`);
  });

  it("leaves the router alone when no third-party script ran", () => {
    render(<PrivateRouteIsolation />);
    link("/zh-TW/trips").click();
    expect(assign).not.toHaveBeenCalled();
  });

  it("leaves public pages, new tabs and modified clicks alone", () => {
    loadDrive();
    render(<PrivateRouteIsolation />);
    link("/zh-TW/life/another-long-article-slug").click();
    link("/zh-TW/trips", { target: "_blank" }).click();
    link("https://example.com/zh-TW/trips").click();
    link("/zh-TW/trips").dispatchEvent(new MouseEvent("click", { bubbles: true, cancelable: true, ctrlKey: true }));
    expect(assign).not.toHaveBeenCalled();
  });

  it("reloads once when a navigation no link started lands on a private page", () => {
    loadDrive();
    const view = render(<PrivateRouteIsolation />);
    expect(reload).not.toHaveBeenCalled();
    navigation.pathname = "/zh-TW/trips/550e8400-e29b-41d4-a716-446655440000";
    view.rerender(<PrivateRouteIsolation />);
    expect(reload).toHaveBeenCalledTimes(1);
    // The script is somehow still there after that reload: do not loop.
    view.unmount();
    render(<PrivateRouteIsolation />);
    expect(reload).toHaveBeenCalledTimes(1);
  });

  it("clears the guard once a private page is reached in a clean document", () => {
    sessionStorage.setItem("travel:private-route-reload", "/zh-TW/trips");
    navigation.pathname = "/zh-TW/trips";
    render(<PrivateRouteIsolation />);
    expect(reload).not.toHaveBeenCalled();
    expect(sessionStorage.getItem("travel:private-route-reload")).toBeNull();
  });
});
