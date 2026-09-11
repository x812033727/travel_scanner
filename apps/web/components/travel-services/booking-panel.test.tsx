import { afterEach, describe, expect, it, vi } from "vitest";
import { cleanup, fireEvent, render, screen } from "@testing-library/react";
import { BookingPanel, SourceCredits, type BookingOption } from "./booking-panel";
import type { Product } from "./catalog";
import { Stay22BookingContextProvider } from "@/lib/stay22-booking-context";
import { stay22AllezCopy } from "@/lib/stay22-allez-copy";
import { hotelBookingPlacements } from "@/lib/hotel-booking-placement";

const copy = stay22AllezCopy("zh-TW");
const options: BookingOption[] = [
  { id: "booking-1", provider: "booking", name: "Booking.com", mode: "affiliate", affiliate_channel: "stay22", quote_status: "not_configured" },
  { id: "agoda-1", provider: "agoda", name: "Agoda", mode: "affiliate", affiliate_channel: "existing", quote_status: "not_configured" },
];
const product = { id: "hotel-1", title: "Reviewed hotel", offers: [], facts: {}, booking_options: options } as unknown as Product;

afterEach(() => { cleanup(); vi.restoreAllMocks(); window.history.replaceState({}, "", "/"); });

function button() { return screen.getByRole("button", { name: /前往 Booking.com 查價格/ }); }
function form() { return button().closest("form")!; }

describe("direct hotel booking panel", () => {
  it("offers an explicit same-tab native POST only after an attempt, revalidating edited values", () => {
    const fetch = vi.spyOn(globalThis, "fetch");
    const open = vi.spyOn(window, "open");
    render(<BookingPanel product={product} placement="destination" onClose={vi.fn()} />);
    expect(screen.queryByRole("button", { name: /未開啟/ })).toBeNull();
    fireEvent.submit(form());
    const fallback = screen.getByRole("button", { name: "未開啟？在目前分頁前往 Booking.com" });
    expect(fallback.getAttribute("formtarget")).toBe("_self");
    expect(fallback.closest("form")).toBe(form());
    expect(form().method).toBe("post");
    expect(form().target).toBe("_blank");
    fireEvent.change(screen.getByLabelText(copy.checkIn), { target: { value: "2099-11-10" } });
    expect(fireEvent.submit(fallback.closest("form")!)).toBe(false);
    fireEvent.change(screen.getByLabelText(copy.checkOut), { target: { value: "2099-11-12" } });
    expect(fireEvent.submit(fallback.closest("form")!)).toBe(true);
    expect(Object.fromEntries(new FormData(form()))).toEqual({ check_in: "2099-11-10", check_out: "2099-11-12" });
    expect(fetch).not.toHaveBeenCalled();
    expect(open).not.toHaveBeenCalled();
  });

  it("requires dates for restricted hotels, blocks both clickout targets, and allows boundary stays", () => {
    const restricted = { ...product, facts: { ...product.facts, hotel_operating_rules: { unavailable_stays: [{ start_date: "2099-11-10", end_date: "2099-11-12", reason: "Maintenance exclusion", source_url: "https://hotel.example.com/maintenance" }], last_checkout_date: "2099-12-01", last_checkout_reason: "Operations ending", last_checkout_source_url: "https://hotel.example.com/closure" } } };
    render(<BookingPanel product={restricted} placement="trip" onClose={vi.fn()} />);
    expect(screen.getByRole("alert").textContent).toBe(copy.operatingDatesRequired);
    expect(screen.queryByRole("checkbox", { name: copy.omitDates })).toBeNull();
    expect(fireEvent.submit(form())).toBe(false);
    expect(screen.getByText("Maintenance exclusion")).toBeTruthy();
    expect(screen.getByRole("link", { name: /查看限制來源 · 2099-11-10/ }).getAttribute("rel")).toBe("noopener noreferrer");
    fireEvent.change(screen.getByLabelText(copy.checkIn), { target: { value: "2099-11-09" } });
    fireEvent.change(screen.getByLabelText(copy.checkOut), { target: { value: "2099-11-10" } });
    expect(fireEvent.submit(form())).toBe(true);
    const fallback = screen.getByRole("button", { name: /未開啟/ });
    fireEvent.change(screen.getByLabelText(copy.checkOut), { target: { value: "2099-11-11" } });
    expect(screen.getByRole("alert").textContent).toBe(copy.operatingUnavailable);
    expect(fireEvent.submit(fallback.closest("form")!)).toBe(false);
    fireEvent.change(screen.getByLabelText(copy.checkIn), { target: { value: "2099-11-12" } });
    fireEvent.change(screen.getByLabelText(copy.checkOut), { target: { value: "2099-12-01" } });
    expect(fireEvent.submit(form())).toBe(true);
    fireEvent.change(screen.getByLabelText(copy.checkOut), { target: { value: "2099-12-02" } });
    expect(fireEvent.submit(form())).toBe(false);
    expect(screen.getByRole("alert").textContent).toBe(copy.operatingUnavailable);
  });

  it("fails closed for malformed persisted rules without rendering unsafe source URLs", () => {
    const invalid = { ...product, facts: { ...product.facts, hotel_operating_rules: { unavailable_stays: [{ start_date: "2099-11-10", end_date: "2099-11-12", reason: "Untrusted", source_url: "javascript:alert(1)" }] } } };
    render(<BookingPanel product={invalid} placement="destination" onClose={vi.fn()} />);
    expect(screen.getByRole("alert").textContent).toBe(copy.operatingInvalid);
    expect(fireEvent.submit(form())).toBe(false);
    expect(document.querySelector('a[href^="javascript:"]')).toBeNull();
  });
  it.each(hotelBookingPlacements)("keeps the %s entry on the first submission", (placement) => {
    window.history.replaceState({}, "", "/zh-TW/explore?category=hotels");
    render(<BookingPanel product={product} placement={placement} onClose={vi.fn()} />);
    fireEvent.submit(form());
    const action = new URL(form().action);
    expect(action.searchParams.get("placement")).toBe(placement);
    expect(action.searchParams.get("return_to")).toBe("/zh-TW/explore?category=hotels");
  });
  it("uses a first-party POST and only explicit optional fields, without fetching affiliate or quote APIs", () => {
    const fetch = vi.spyOn(globalThis, "fetch");
    render(<BookingPanel product={product} placement="destination" onClose={vi.fn()} />);
    expect(form().getAttribute("action")).toBe("/api/travel/travel-services/hotel-1/booking-options/booking-1/clickout?locale=zh-TW&placement=destination");
    expect(form().getAttribute("method")).toBe("post");
    expect(form().getAttribute("target")).toBe("_blank");
    expect(form().getAttribute("rel")).toBe("noopener");
    expect([...new FormData(form()).keys()]).toEqual([]);
    expect(screen.queryByText("透過 Stay22 合作連結")).toBeNull();
    expect(screen.getByText(copy.disclosure)).toBeTruthy();
    expect(document.querySelector("iframe, a[href*='stay22.com']")).toBeNull();
    expect(fetch).not.toHaveBeenCalled();
    window.history.replaceState({}, "", "/zh-TW/destinations/tokyo/services?type=hotel");
    fireEvent.submit(form());
    expect(new URL(form().action).searchParams.get("return_to")).toBe("/zh-TW/destinations/tokyo/services?type=hotel");
    expect([...new FormData(form()).keys()]).toEqual([]);
  });

  it("preserves the original trip stay and party context rather than truncated live-search dates", () => {
    render(<Stay22BookingContextProvider value={{ check_in: "2099-11-10", check_out: "2099-12-20", adults: 3, children: 2, rooms: 2, children_ages: [4, 9] }}>
      <BookingPanel product={product} startDate="2099-11-10" endDate="2099-12-10" placement="trip" onClose={vi.fn()} />
    </Stay22BookingContextProvider>);
    expect((screen.getByLabelText(copy.checkOut) as HTMLInputElement).value).toBe("2099-12-20");
    expect(Object.fromEntries(new FormData(form()))).toEqual({ check_in: "2099-11-10", check_out: "2099-12-20", adults: "3", children: "2" });
    expect(screen.getByText("原設定：2 間房")).toBeTruthy();
    expect(screen.getByText("原設定兒童年齡：4, 9 歲")).toBeTruthy();
    expect(screen.getByText(copy.confirmOccupancy)).toBeTruthy();
    fireEvent.change(screen.getByLabelText(copy.adults), { target: { value: "4" } });
    expect(new FormData(form()).get("adults")).toBe("4");
  });

  it("blocks invalid, partial or past dates without silently replacing them, then explicitly omits them", () => {
    render(<BookingPanel product={product} startDate="2020-11-10" endDate="2020-11-12" placement="trip" onClose={vi.fn()} />);
    expect(screen.getByRole("alert").textContent).toBe(copy.pastDates);
    expect(fireEvent.submit(form())).toBe(false);
    expect((screen.getByLabelText(copy.checkIn) as HTMLInputElement).value).toBe("2020-11-10");
    fireEvent.click(screen.getByRole("checkbox", { name: copy.omitDates }));
    expect(screen.queryByRole("alert")).toBeNull();
    expect(new FormData(form()).has("check_in")).toBe(false);
    expect(new FormData(form()).has("check_out")).toBe(false);
    expect((screen.getByLabelText(copy.checkIn) as HTMLInputElement).disabled).toBe(true);
    fireEvent.click(screen.getByRole("checkbox", { name: copy.omitDates }));
    fireEvent.change(screen.getByLabelText(copy.checkOut), { target: { value: "" } });
    expect(screen.getByRole("alert").textContent).toBe(copy.invalidDates);
    expect(fireEvent.submit(form())).toBe(false);
  });

  it("validates guest counts and retains all values when submission is blocked", () => {
    render(<BookingPanel product={product} placement="hotspot" onClose={vi.fn()} />);
    fireEvent.change(screen.getByLabelText(copy.adults), { target: { value: "0" } });
    expect(screen.getByRole("alert").textContent).toBe(copy.invalidGuests);
    expect(fireEvent.submit(form())).toBe(false);
    expect((screen.getByLabelText(copy.adults) as HTMLInputElement).value).toBe("0");
    fireEvent.change(screen.getByLabelText(copy.adults), { target: { value: "2" } });
    fireEvent.change(screen.getByLabelText(copy.children), { target: { value: "1.5" } });
    expect(screen.getByRole("alert").textContent).toBe(copy.invalidGuests);
    fireEvent.change(screen.getByLabelText(copy.children), { target: { value: "10" } });
    expect(screen.getByRole("alert").textContent).toBe(copy.invalidGuests);
  });

  it("labels missing precise links and keeps live quotes separate from affiliate platforms", () => {
    const { rerender } = render(<BookingPanel product={{ ...product, booking_options: [] }} placement="destination" onClose={vi.fn()} />);
    expect(screen.getByText(copy.noExactLink)).toBeTruthy();
    rerender(<BookingPanel product={{ ...product, booking_options: [{ ...options[0], quote_status: "ready" }] }} placement="destination" onClose={vi.fn()} />);
    expect(screen.getByText(copy.quotesTitle)).toBeTruthy();
    const quoteDetails = screen.getByText(copy.quotesTitle).closest("details");
    expect(quoteDetails?.open).toBe(false);
    expect(screen.getByText(copy.quotesNote)).toBeTruthy();
    expect(button().closest("details")).toBeNull();
  });
});

describe("hotel source credits", () => {
  it("uses the concise source label and preserves source and license links without rendering editorial changes", () => {
    const changes = "Mokaair 將公開資料整理為飯店介紹，補充地址並調整格式；這是保留於來源資料的整理備註。";
    const credit = Object.freeze({
      title: "Reviewed hotel source", publisher: "Fixture publisher",
      url: "https://source.example.test/hotel", license_name: "Fixture license",
      license_url: "https://source.example.test/license", changes,
    });
    render(<SourceCredits credits={[credit]} />);
    const summary = screen.getByText("資料來源", { exact: true });
    expect(summary.tagName).toBe("SUMMARY");
    expect(screen.queryByText("資料來源與授權")).toBeNull();
    fireEvent.click(summary);
    expect(summary.closest("details")?.open).toBe(true);
    const source = screen.getByRole("link", { name: `${credit.title} · 另開新分頁` });
    const license = screen.getByRole("link", { name: `${credit.license_name} · 另開新分頁` });
    expect(source.getAttribute("href")).toBe(credit.url);
    expect(license.getAttribute("href")).toBe(credit.license_url);
    for (const link of [source, license]) {
      expect(link.getAttribute("target")).toBe("_blank");
      expect(link.getAttribute("rel")).toBe("noopener noreferrer");
    }
    expect(screen.getByText(credit.publisher, { exact: false })).toBeTruthy();
    expect(screen.queryByText(changes)).toBeNull();
    expect(credit.changes).toBe(changes);
  });

  it("does not add an empty source disclosure when source data is absent", () => {
    const { container, rerender } = render(<SourceCredits />);
    expect(container.innerHTML).toBe("");
    rerender(<SourceCredits credits={[]} />);
    expect(container.innerHTML).toBe("");
  });
});
