import { act, cleanup, render, screen, waitFor, within } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import * as intl from "next-intl";
import { AffiliatePartnerOptions } from "./affiliate-partner-options";

const ok = (value: unknown) => new Response(JSON.stringify(value), {
  status: 200,
  headers: { "Content-Type": "application/json" },
});

afterEach(() => { cleanup(); vi.unstubAllGlobals(); vi.restoreAllMocks(); });

describe("AffiliatePartnerOptions", () => {
  it("shows parallel partner CTAs and the affiliate disclosure", async () => {
    const fetchMock = vi.fn().mockResolvedValue(ok({
      module: "hotel",
      disclosure: "透過合作連結預訂，本站可能獲得分潤，價格不因此增加。",
      options: [
        { partner: "booking", display_name: "Booking.com", module: "hotel", cta: "到 Booking.com 查看", clickout_url: "/api/travel/affiliates/booking/clickout?token=a" },
        { partner: "agoda", display_name: "Agoda", module: "hotel", cta: "到 Agoda 查看", clickout_url: "/api/travel/affiliates/agoda/clickout?token=b" },
      ],
    }));
    vi.stubGlobal("fetch", fetchMock);

    render(<AffiliatePartnerOptions searchId="search-1" modules={["hotel"]} />);

    // The heading now defaults to the catalog title rather than a Chinese literal.
    const section = await screen.findByRole("region", { name: "旅行服務" });
    expect(within(section).getByRole("button", { name: /Booking.com/ })).toBeTruthy();
    expect(within(section).getByRole("button", { name: /Agoda/ })).toBeTruthy();
    expect(within(section).getByText(/本站可能獲得分潤/)).toBeTruthy();
    expect(within(section).getByText(/不扣使用次數/)).toBeTruthy();
    expect(within(section).getByText("住宿")).toBeTruthy();
    const forms = section.querySelectorAll("form");
    expect(forms[0].getAttribute("method")).toBe("post");
    expect(forms[0].getAttribute("target")).toBe("_blank");
    expect(forms[0].getAttribute("rel")).toBe("noopener");
    expect(forms[0].getAttribute("action")).toBe("/api/travel/affiliates/booking/clickout?token=a&locale=zh-TW");
    expect(forms[1].getAttribute("action")).toBe("/api/travel/affiliates/agoda/clickout?token=b&locale=zh-TW");
  });

  it("hides disabled or failed partners without rendering invalid buttons", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(ok({
      module: "connectivity",
      disclosure: "",
      options: [],
    })));
    render(<AffiliatePartnerOptions tripId="trip-1" modules={["connectivity"]} />);
    await waitFor(() => expect(fetch).toHaveBeenCalledTimes(1));
    expect(screen.queryByRole("region", { name: "旅行服務" })).toBeNull();
  });

  it("hides offers immediately after a source or module change, aborts old reads and ignores late results", async () => {
    const pending: { url: string; signal: AbortSignal; resolve: (value: Response) => void }[] = [];
    vi.stubGlobal("fetch", vi.fn((input: RequestInfo | URL, init: RequestInit) => new Promise<Response>((resolve) => {
      pending.push({ url: String(input), signal: init.signal as AbortSignal, resolve });
    })));
    const response = (module: string, cta: string) => ok({ module, disclosure: "Disclosure", options: [{ partner: "booking", cta, clickout_url: "/api/travel/affiliates/booking/clickout?token=opaque%2Ftoken" }] });
    const view = render(<AffiliatePartnerOptions searchId="search-1" modules={["hotel"]} />);
    await act(async () => { pending[0].resolve(response("hotel", "Search hotel")); });
    expect(await screen.findByRole("button", { name: /Search hotel/ })).toBeTruthy();
    view.rerender(<AffiliatePartnerOptions tripId="trip-1" modules={["activities"]} />);
    expect(screen.queryByRole("button", { name: /Search hotel/ })).toBeNull();
    expect(pending[0].signal.aborted).toBe(true);
    expect(pending[1].url).toContain("module=activities&trip_id=trip-1");
    view.rerender(<AffiliatePartnerOptions tripId="trip-2" modules={["hotel"]} />);
    expect(pending[1].signal.aborted).toBe(true);
    await act(async () => { pending[2].resolve(response("hotel", "Current trip hotel")); });
    await act(async () => { pending[1].resolve(response("activities", "Old trip activity")); });
    expect(screen.getByRole("button", { name: /Current trip hotel/ })).toBeTruthy();
    expect(screen.queryByRole("button", { name: /Old trip activity/ })).toBeNull();
    view.rerender(<AffiliatePartnerOptions modules={["hotel"]} />);
    expect(screen.queryByRole("region")).toBeNull();
    expect(pending[2].signal.aborted).toBe(true);
    expect(pending).toHaveLength(3);
  });

  it("uses the displayed locale for both reads and POSTs instead of retaining the previous locale's offers", async () => {
    const locale = vi.spyOn(intl, "useLocale").mockReturnValue("zh-TW");
    const pending: { headers: Headers; signal: AbortSignal; resolve: (value: Response) => void }[] = [];
    vi.stubGlobal("fetch", vi.fn((_input: RequestInfo | URL, init: RequestInit) => new Promise<Response>((resolve) => {
      pending.push({ headers: new Headers(init.headers), signal: init.signal as AbortSignal, resolve });
    })));
    const response = (cta: string) => ok({ module: "hotel", disclosure: "Disclosure", options: [{ partner: "booking", cta, clickout_url: "/api/travel/affiliates/booking/clickout?token=opaque%2Ftoken" }] });
    const view = render(<AffiliatePartnerOptions searchId="search-1" modules={["hotel"]} />);
    await act(async () => { pending[0].resolve(response("Old hotel")); });
    locale.mockReturnValue("ko");
    view.rerender(<AffiliatePartnerOptions searchId="search-1" modules={["hotel"]} />);
    expect(screen.queryByRole("button", { name: /Old hotel/ })).toBeNull();
    expect(pending[0].signal.aborted).toBe(true);
    expect(pending[1].headers.get("X-Travel-Locale")).toBe("ko");
    await act(async () => { pending[1].resolve(response("Korean hotel")); });
    expect(screen.getByRole("button", { name: /Korean hotel/ }).closest("form")?.getAttribute("action"))
      .toBe("/api/travel/affiliates/booking/clickout?token=opaque%2Ftoken&locale=ko");
  });

  it("deduplicates modules and removes offers when the current request has no valid modules", async () => {
    const fetcher = vi.fn().mockResolvedValue(ok({ module: "hotel", disclosure: "Disclosure", options: [{ partner: "booking", cta: "Book hotel", clickout_url: "/api/travel/affiliates/booking/clickout?token=a" }] }));
    vi.stubGlobal("fetch", fetcher);
    const view = render(<AffiliatePartnerOptions tripId="trip-1" modules={["hotel", "hotel"]} />);
    expect(await screen.findByRole("button", { name: /Book hotel/ })).toBeTruthy();
    expect(fetcher).toHaveBeenCalledTimes(1);
    view.rerender(<AffiliatePartnerOptions tripId="trip-1" modules={[]} />);
    expect(screen.queryByRole("region")).toBeNull();
    expect(fetcher).toHaveBeenCalledTimes(1);
  });
});
