import { act, cleanup, render, screen, waitFor, within } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import * as intl from "next-intl";
import { AFFILIATE_PREFETCH_MARGIN, DestinationAffiliateOptions } from "./destination-affiliate-options";

const ok = (value: unknown) =>
  new Response(JSON.stringify(value), {
    status: 200,
    headers: { "Content-Type": "application/json" },
  });

afterEach(() => { cleanup(); vi.unstubAllGlobals(); vi.restoreAllMocks(); });

describe("DestinationAffiliateOptions", () => {
  it("requests only the selected category, cancels old requests and ignores late results", async () => {
    const pending: { url: string; signal: AbortSignal; resolve: (value: Response) => void }[] = [];
    vi.stubGlobal("fetch", vi.fn((input: RequestInfo | URL, init: RequestInit) => new Promise<Response>((resolve) => {
      pending.push({ url: String(input), signal: init.signal as AbortSignal, resolve });
    })));
    const response = (destination: string, module: string, name: string) => ok({ destination_id: destination, module, disclosure: "Disclosure", options: [{ id: name, cta: name, clickout_url: "/api/travel/affiliates/destination-offers/verified/clickout" }] });
    const view = render(<DestinationAffiliateOptions destinationId="tokyo" modules={["hotel"]} contextual />);
    expect(pending[0].url).toContain("destination_id=tokyo&module=hotel&placement=destination");
    view.rerender(<DestinationAffiliateOptions destinationId="seoul" modules={["transport"]} contextual />);
    expect(pending[0].signal.aborted).toBe(true);
    expect(pending[1].url).toContain("destination_id=seoul&module=transport&placement=destination");
    await act(async () => { pending[1].resolve(response("seoul", "transport", "Seoul transfer")); });
    expect(await screen.findByRole("button", { name: /Seoul transfer/ })).toBeTruthy();
    await act(async () => { pending[0].resolve(response("tokyo", "hotel", "Old Tokyo hotel")); });
    expect(screen.queryByRole("button", { name: /Old Tokyo hotel/ })).toBeNull();
    view.rerender(<DestinationAffiliateOptions destinationId="tokyo" modules={["activities"]} contextual />);
    expect(screen.queryByRole("button", { name: /Seoul transfer/ })).toBeNull();
    expect(pending).toHaveLength(3);
    expect(pending.every(({ url }) => !url.includes("hotel-quotes"))).toBe(true);
    // The surface is part of the request identity: a different placement is a new request.
    view.rerender(<DestinationAffiliateOptions destinationId="tokyo" modules={["activities"]} contextual placement="guide" />);
    expect(pending[2].signal.aborted).toBe(true);
    expect(pending[3].url).toContain("destination_id=tokyo&module=activities&placement=guide");
  });
  it("shows verified brand names without exposing Travelpayouts", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn((input: RequestInfo | URL) => {
        const url = String(input);
        const serviceModule = new URL(
          url,
          "https://mokaair.test",
        ).searchParams.get("module");
        return Promise.resolve(
          ok({
            destination_id: "tokyo",
            module: serviceModule,
            disclosure: "透過合作連結預訂，價格不因此增加。",
            options:
              serviceModule === "activities"
                ? [
                    {
                      id: "offer-1",
                      brand: "klook",
                      display_name: "Klook",
                      destination_id: "tokyo",
                      module: serviceModule,
                      cta: "到 Klook 查看",
                      clickout_url:
                        "/api/travel/affiliates/destination-offers/offer-1/clickout",
                    },
                  ]
                : [],
          }),
        );
      }),
    );

    render(<DestinationAffiliateOptions destinationId="tokyo" />);

    const section = await screen.findByRole("region", {
      name: "這個目的地的合作平台",
    });
    const button = within(section).getByRole("button", { name: /Klook/ });
    expect(button).toBeTruthy();
    expect(section.textContent).not.toContain("Travelpayouts");
    const form = button.closest("form");
    expect(form?.getAttribute("method")).toBe("post");
    expect(form?.getAttribute("target")).toBe("_blank");
    // Never `noreferrer`: that POST carries `Origin: null` and the BFF refuses the click.
    expect(form?.getAttribute("rel")).toBe("noopener");
    expect(form?.getAttribute("action")).toContain("destination-offers");
    await waitFor(() => expect(fetch).toHaveBeenCalledTimes(5));
  });

  it("appends the article that placed the buttons to the clickout URL, and only then", async () => {
    vi.stubGlobal("fetch", vi.fn(() => Promise.resolve(ok({
      destination_id: "tokyo", module: "activities", disclosure: "Disclosure",
      options: [{ id: "offer-1", brand: "klook", display_name: "Klook", destination_id: "tokyo", module: "activities", cta: "到 Klook 查看", clickout_url: "/api/travel/affiliates/destination-offers/offer-1/clickout?placement=guide" }],
    }))));
    const view = render(<DestinationAffiliateOptions destinationId="tokyo" modules={["activities"]} contextual placement="guide" article="tokyo-esim" />);
    const button = await screen.findByRole("button", { name: /Klook/ });
    expect(button.closest("form")?.getAttribute("action")).toBe("/api/travel/affiliates/destination-offers/offer-1/clickout?placement=guide&locale=zh-TW&article=tokyo-esim");
    // Without an article the URL is exactly what the API built, and the article is not part
    // of the request identity: the offers are not fetched again.
    view.rerender(<DestinationAffiliateOptions destinationId="tokyo" modules={["activities"]} contextual placement="guide" />);
    expect(screen.getByRole("button", { name: /Klook/ }).closest("form")?.getAttribute("action")).toBe("/api/travel/affiliates/destination-offers/offer-1/clickout?placement=guide&locale=zh-TW");
    expect(fetch).toHaveBeenCalledTimes(1);
  });

  it("renders nothing when no reviewed destination offer is public", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue(
        ok({
          destination_id: "tokyo",
          module: "hotel",
          disclosure: "",
          options: [],
        }),
      ),
    );
    const { container } = render(
      <DestinationAffiliateOptions destinationId="tokyo" />,
    );
    await waitFor(() => expect(fetch).toHaveBeenCalledTimes(5));
    expect(container.innerHTML).toBe("");
  });

  it("waits until the placement approaches the viewport, then requests once and removes an empty placement", async () => {
    let notify: IntersectionObserverCallback = () => undefined;
    const observe = vi.fn();
    const disconnect = vi.fn();
    const observer = { observe, disconnect } as unknown as IntersectionObserver;
    const constructor = vi.fn(function (callback: IntersectionObserverCallback) {
      notify = callback;
      return observer;
    });
    vi.stubGlobal("IntersectionObserver", constructor);
    const fetcher = vi.fn().mockResolvedValue(ok({ destination_id: "tokyo", module: "hotel", disclosure: "", options: [] }));
    vi.stubGlobal("fetch", fetcher);
    const { container } = render(<DestinationAffiliateOptions destinationId="tokyo" modules={["hotel"]} />);
    expect(constructor).toHaveBeenCalledWith(expect.any(Function), { rootMargin: AFFILIATE_PREFETCH_MARGIN });
    expect(observe).toHaveBeenCalledTimes(1);
    expect(screen.queryByRole("region")).toBeNull();
    expect(fetcher).not.toHaveBeenCalled();
    await act(async () => {
      notify([{ isIntersecting: false, boundingClientRect: new DOMRect(0, 2400, 320, 1) }] as IntersectionObserverEntry[], observer);
    });
    expect(fetcher).not.toHaveBeenCalled();
    await act(async () => {
      notify([{ isIntersecting: true }] as IntersectionObserverEntry[], observer);
      notify([{ isIntersecting: true }] as IntersectionObserverEntry[], observer);
    });
    expect(fetcher).toHaveBeenCalledTimes(1);
    expect(disconnect).toHaveBeenCalled();
    expect(container.innerHTML).toBe("");
  });

  it("loads a placement above restored scroll without intersection, requests once and shows its card", async () => {
    let notify: IntersectionObserverCallback = () => undefined;
    const disconnect = vi.fn();
    const observer = { observe: vi.fn(), disconnect } as unknown as IntersectionObserver;
    vi.stubGlobal("IntersectionObserver", vi.fn(function (callback: IntersectionObserverCallback) {
      notify = callback;
      return observer;
    }));
    const fetcher = vi.fn().mockResolvedValue(ok({
      destination_id: "tokyo", module: "connectivity", disclosure: "Disclosure",
      options: [{ id: "offer-1", brand: "klook", display_name: "Klook", destination_id: "tokyo", module: "connectivity", cta: "Klook connectivity", clickout_url: "/api/travel/affiliates/destination-offers/offer-1/clickout" }],
    }));
    vi.stubGlobal("fetch", fetcher);
    render(<DestinationAffiliateOptions destinationId="tokyo" modules={["connectivity"]} />);
    expect(fetcher).not.toHaveBeenCalled();
    expect(screen.queryByRole("region")).toBeNull();
    const passedMarker = [{ isIntersecting: false, boundingClientRect: new DOMRect(0, -801, 320, 1) }] as IntersectionObserverEntry[];
    await act(async () => {
      notify(passedMarker, observer);
      notify(passedMarker, observer);
    });
    expect(fetcher).toHaveBeenCalledTimes(1);
    expect(disconnect).toHaveBeenCalledTimes(1);
    const section = await screen.findByRole("region", { name: "這個目的地的合作平台" });
    expect(within(section).getByRole("button", { name: /Klook connectivity/ })).toBeTruthy();
  });

  it("loads once after scrolling past the prefetch window without another intersection notification", async () => {
    let notify: IntersectionObserverCallback = () => undefined;
    const observe = vi.fn();
    const disconnect = vi.fn();
    const observer = { observe, disconnect } as unknown as IntersectionObserver;
    vi.stubGlobal("IntersectionObserver", vi.fn(function (callback: IntersectionObserverCallback) {
      notify = callback;
      return observer;
    }));
    const frames: FrameRequestCallback[] = [];
    const requestFrame = vi.fn((callback: FrameRequestCallback) => { frames.push(callback); return frames.length; });
    vi.stubGlobal("requestAnimationFrame", requestFrame);
    vi.stubGlobal("cancelAnimationFrame", vi.fn());
    const fetcher = vi.fn().mockResolvedValue(ok({
      destination_id: "tokyo", module: "connectivity", disclosure: "Disclosure",
      options: [{ id: "offer-1", brand: "klook", display_name: "Klook", destination_id: "tokyo", module: "connectivity", cta: "Klook connectivity", clickout_url: "/api/travel/affiliates/destination-offers/offer-1/clickout" }],
    }));
    vi.stubGlobal("fetch", fetcher);
    render(<DestinationAffiliateOptions destinationId="tokyo" modules={["connectivity"]} />);
    const bounds = vi.spyOn(observe.mock.calls[0][0] as Element, "getBoundingClientRect").mockReturnValue(new DOMRect(0, 2400, 320, 1));
    await act(async () => {
      notify([{ isIntersecting: false, boundingClientRect: bounds() }] as IntersectionObserverEntry[], observer);
      window.dispatchEvent(new Event("scroll"));
      frames[0]?.(0);
    });
    expect(fetcher).not.toHaveBeenCalled();
    bounds.mockReturnValue(new DOMRect(0, -801, 320, 1));
    // Intersection stays false across this jump, so there is no second observer callback.
    await act(async () => {
      window.dispatchEvent(new Event("scroll"));
      window.dispatchEvent(new Event("scroll"));
      frames[1]?.(16);
    });
    expect(fetcher).toHaveBeenCalledTimes(1);
    expect(requestFrame).toHaveBeenCalledTimes(2);
    expect(disconnect).toHaveBeenCalledTimes(1);
    const section = await screen.findByRole("region", { name: "這個目的地的合作平台" });
    expect(within(section).getByRole("button", { name: /Klook connectivity/ })).toBeTruthy();
    window.dispatchEvent(new Event("scroll"));
    expect(requestFrame).toHaveBeenCalledTimes(2);
    expect(fetcher).toHaveBeenCalledTimes(1);
  });

  it("cancels a pending passed-marker check on unmount and prevents late requests", async () => {
    const observe = vi.fn();
    const disconnect = vi.fn();
    vi.stubGlobal("IntersectionObserver", vi.fn(function () {
      return { observe, disconnect };
    }));
    const frames: FrameRequestCallback[] = [];
    const requestFrame = vi.fn((callback: FrameRequestCallback) => { frames.push(callback); return frames.length; });
    const cancelFrame = vi.fn();
    vi.stubGlobal("requestAnimationFrame", requestFrame);
    vi.stubGlobal("cancelAnimationFrame", cancelFrame);
    const fetcher = vi.fn();
    vi.stubGlobal("fetch", fetcher);
    const view = render(<DestinationAffiliateOptions destinationId="tokyo" modules={["hotel"]} />);
    vi.spyOn(observe.mock.calls[0][0] as Element, "getBoundingClientRect").mockReturnValue(new DOMRect(0, -801, 320, 1));
    window.dispatchEvent(new Event("scroll"));
    expect(requestFrame).toHaveBeenCalledTimes(1);
    expect(fetcher).not.toHaveBeenCalled();
    view.unmount();
    expect(disconnect).toHaveBeenCalledTimes(1);
    expect(cancelFrame).toHaveBeenCalledWith(1);
    await act(async () => { frames[0](0); });
    window.dispatchEvent(new Event("scroll"));
    expect(requestFrame).toHaveBeenCalledTimes(1);
    expect(fetcher).not.toHaveBeenCalled();
  });

  it("disconnects a waiting placement on unmount without making a request", () => {
    const disconnect = vi.fn();
    vi.stubGlobal("IntersectionObserver", vi.fn(function () {
      return { observe: vi.fn(), disconnect };
    }));
    const fetcher = vi.fn();
    vi.stubGlobal("fetch", fetcher);
    const view = render(<DestinationAffiliateOptions destinationId="tokyo" modules={["hotel"]} />);
    view.unmount();
    expect(disconnect).toHaveBeenCalledTimes(1);
    expect(fetcher).not.toHaveBeenCalled();
  });

  it("refetches for the displayed locale and preserves attribution in that locale's POST action", async () => {
    const locale = vi.spyOn(intl, "useLocale").mockReturnValue("zh-TW");
    const pending: { headers: Headers; signal: AbortSignal; resolve: (value: Response) => void }[] = [];
    vi.stubGlobal("fetch", vi.fn((_input: RequestInfo | URL, init: RequestInit) => new Promise<Response>((resolve) => {
      pending.push({ headers: new Headers(init.headers), signal: init.signal as AbortSignal, resolve });
    })));
    const response = (cta: string) => ok({ destination_id: "tokyo", module: "hotel", disclosure: "Disclosure", options: [{ id: "offer-1", cta, clickout_url: "/api/travel/affiliates/destination-offers/offer-1/clickout?placement=guide&token=a%2Fb" }] });
    const view = render(<DestinationAffiliateOptions destinationId="tokyo" modules={["hotel"]} placement="guide" article="tokyo-hotels" />);
    await act(async () => { pending[0].resolve(response("Old hotel")); });
    expect(await screen.findByRole("button", { name: /Old hotel/ })).toBeTruthy();
    locale.mockReturnValue("ja");
    view.rerender(<DestinationAffiliateOptions destinationId="tokyo" modules={["hotel"]} placement="guide" article="tokyo-hotels" />);
    expect(screen.queryByRole("button", { name: /Old hotel/ })).toBeNull();
    expect(pending[0].signal.aborted).toBe(true);
    expect(pending[1].headers.get("X-Travel-Locale")).toBe("ja");
    await act(async () => { pending[1].resolve(response("Japanese hotel")); });
    expect(screen.getByRole("button", { name: /Japanese hotel/ }).closest("form")?.getAttribute("action"))
      .toBe("/api/travel/affiliates/destination-offers/offer-1/clickout?placement=guide&token=a%2Fb&locale=ja&article=tokyo-hotels");
  });
});
