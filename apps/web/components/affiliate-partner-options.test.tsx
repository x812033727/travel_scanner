import { render, screen, waitFor, within } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { AffiliatePartnerOptions } from "./affiliate-partner-options";

const ok = (value: unknown) => new Response(JSON.stringify(value), {
  status: 200,
  headers: { "Content-Type": "application/json" },
});

afterEach(() => vi.unstubAllGlobals());

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

    const section = await screen.findByRole("region", { name: "合作平台" });
    expect(within(section).getByRole("button", { name: /Booking.com/ })).toBeTruthy();
    expect(within(section).getByRole("button", { name: /Agoda/ })).toBeTruthy();
    expect(within(section).getByText(/本站可能獲得分潤/)).toBeTruthy();
    expect(within(section).getByText(/不扣使用次數/)).toBeTruthy();
    const forms = section.querySelectorAll("form");
    expect(forms[0].getAttribute("method")).toBe("post");
    expect(forms[0].getAttribute("target")).toBe("_blank");
  });

  it("hides disabled or failed partners without rendering invalid buttons", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(ok({
      module: "connectivity",
      disclosure: "",
      options: [],
    })));
    render(<AffiliatePartnerOptions tripId="trip-1" modules={["connectivity"]} />);
    await waitFor(() => expect(fetch).toHaveBeenCalledTimes(1));
    expect(screen.queryByRole("region", { name: "合作平台" })).toBeNull();
  });
});
