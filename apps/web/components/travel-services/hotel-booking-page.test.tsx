import "@testing-library/jest-dom/vitest";
import { act, cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, beforeEach, expect, it, vi } from "vitest";
import { ApiError } from "@/lib/api";
import { stay22AllezCopy } from "@/lib/stay22-allez-copy";
import { Stay22BookingContextProvider } from "@/lib/stay22-booking-context";
import messages from "@/messages/zh-TW/travelServices.json";
import common from "@/messages/zh-TW/common.json";
import HotelPage from "@/app/[locale]/hotels/[productId]/page";
import { HotelBookingPage } from "./hotel-booking-page";
import type { Product } from "./catalog";

const { request, missing } = vi.hoisted(() => ({
  request: vi.fn(),
  missing: vi.fn(() => { throw new Error("NEXT_NOT_FOUND"); }),
}));
vi.mock("@/lib/api", async (original) => ({ ...(await original<typeof import("@/lib/api")>()), api: request }));
vi.mock("next/navigation", () => ({ notFound: missing }));
vi.mock("@/components/site-header", () => ({ SiteHeader: () => null }));
// A Discovery-dependent implementation must not silently pass this regression.
vi.mock("@/lib/discovery", () => { throw new Error("Independent booking must not import Discovery"); });
vi.mock("@/components/stay22-script", () => { throw new Error("Independent booking must not import the SDK"); });

const copy = stay22AllezCopy("zh-TW");
const productId = "90000000-abcd-4000-8000-000000000009";
const otherId = "90000000-0000-4000-8000-000000000010";
const product: Product = {
  id: productId, kind: "hotel", title: "Reviewed independent hotel", destination_id: "kyoto",
  source_url: "https://hotel.example.com", distance_km: null, reason: "",
  offers: [], facts: {
    area_code: null, country_codes: ["JP"], facilities: [], airport: null, direction: null,
    passengers: null, luggage: null, languages: [], duration_minutes: null, meeting_point: null,
    data_gb: null, validity_days: null, unlimited: null, tethering: null, reference_price: null, currency: null,
    hotel_operating_rules: { unavailable_stays: [{ start_date: "2099-11-10", end_date: "2099-11-12", reason: "Maintenance", source_url: "https://hotel.example.com/notice" }] },
  },
  booking_options: [{ id: "90000000-0000-4000-8000-000000000011", provider: "booking", name: "Booking.com", mode: "direct", quote_status: "not_configured" }],
};

beforeEach(() => {
  request.mockResolvedValue(product);
  window.history.replaceState({}, "", `/zh-TW/hotels/${productId}`);
});
afterEach(() => { cleanup(); vi.resetAllMocks(); window.history.replaceState({}, "", "/"); });

it("loads one public product and opens date controls without Discovery or inherited booking dates", async () => {
  render(<Stay22BookingContextProvider value={{ check_in: "2099-12-01", check_out: "2099-12-03", adults: 4 }}>
    <HotelBookingPage productId={productId} />
  </Stay22BookingContextProvider>);
  expect(screen.getByRole("status")).toHaveTextContent(messages.loading);
  expect(await screen.findByRole("dialog", { name: product.title })).toBeVisible();
  expect(screen.getByRole("heading", { level: 1 })).toHaveTextContent(product.title);
  expect(screen.getByLabelText(copy.checkIn)).toHaveValue("");
  expect(screen.getByLabelText(copy.adults)).toHaveValue(null);
  expect(screen.getByRole("alert")).toHaveTextContent(copy.operatingDatesRequired);
  expect(screen.queryByRole("checkbox", { name: copy.omitDates })).toBeNull();
  expect(request).toHaveBeenCalledTimes(1);
  expect(request).toHaveBeenCalledWith(`/travel-services/${productId}/booking-details`, { signal: expect.any(AbortSignal) });
  const button = screen.getByRole("button", { name: /前往 Booking.com 查價格/ });
  expect(button.closest("form")).toHaveAttribute("action", expect.stringContaining("placement=destination"));
  expect(fireEvent.submit(button.closest("form")!)).toBe(false);
  expect(document.querySelectorAll("script,iframe")).toHaveLength(0);
});

it("keeps a native clean catalog return and allows reopening after closing", async () => {
  render(<HotelBookingPage productId={productId} />);
  await screen.findByRole("dialog", { name: product.title });
  const back = screen.getByRole("link", { name: copy.back });
  expect(back).toHaveAttribute("href", "/zh-TW/destinations/kyoto/services?type=hotel");
  expect(back).not.toHaveAttribute("target");
  fireEvent.click(screen.getByRole("button", { name: common.close }));
  await waitFor(() => expect(screen.queryByRole("dialog")).toBeNull());
  fireEvent.click(screen.getByRole("button", { name: messages.platforms }));
  expect(screen.getByRole("dialog", { name: product.title })).toBeVisible();
});

it("shows unavailable products without a misleading retry or any booking form", async () => {
  request.mockRejectedValue(new ApiError("Private upstream trace", 404, "service_unavailable"));
  render(<HotelBookingPage productId={productId} />);
  await waitFor(() => expect(screen.getByRole("status")).toHaveTextContent(messages.noOffers));
  expect(screen.queryByRole("button", { name: messages.retry })).toBeNull();
  expect(screen.queryByRole("dialog")).toBeNull();
  expect(screen.queryByText("Private upstream trace")).toBeNull();
  expect(screen.getByRole("link", { name: copy.back })).toHaveAttribute("href", "/zh-TW/destinations");
});

it("retries a transport failure explicitly without showing upstream details", async () => {
  request.mockRejectedValueOnce(new Error("Sensitive transport detail")).mockResolvedValue(product);
  render(<HotelBookingPage productId={productId} />);
  expect(await screen.findByRole("alert")).toHaveTextContent(copy.errorTitle);
  expect(screen.queryByText("Sensitive transport detail")).toBeNull();
  fireEvent.click(screen.getByRole("button", { name: messages.retry }));
  expect(await screen.findByRole("dialog", { name: product.title })).toBeVisible();
  expect(request).toHaveBeenCalledTimes(2);
});

it.each([{ ...product, kind: "tour" }, { ...product, id: otherId }])("does not open an unexpected product", async (unexpected) => {
  request.mockResolvedValue(unexpected);
  render(<HotelBookingPage productId={productId} />);
  await waitFor(() => expect(screen.getByRole("status")).toHaveTextContent(messages.noOffers));
  expect(screen.queryByRole("dialog")).toBeNull();
});

it("discards a prior hotel's pending response when the product changes", async () => {
  let resolveFirst!: (value: Product) => void;
  request.mockImplementationOnce(() => new Promise<Product>((resolve) => { resolveFirst = resolve; }))
    .mockResolvedValueOnce({ ...product, id: otherId, title: "Second hotel" });
  const { rerender } = render(<HotelBookingPage productId={productId} />);
  const firstSignal = request.mock.calls[0][1].signal as AbortSignal;
  rerender(<HotelBookingPage productId={otherId} />);
  expect(firstSignal.aborted).toBe(true);
  await screen.findByRole("dialog", { name: "Second hotel" });
  await act(async () => resolveFirst(product));
  expect(screen.queryByRole("heading", { name: product.title })).toBeNull();
});

it("validates UUID route params before rendering and normalizes uppercase", async () => {
  for (const invalid of ["not-a-hotel", "../admin", "90000000-0000-4000-8000-00000000000z"]) {
    await expect(HotelPage({ params: Promise.resolve({ locale: "zh-TW", productId: invalid }) })).rejects.toThrow("NEXT_NOT_FOUND");
  }
  expect(missing).toHaveBeenCalledTimes(3);
  render(await HotelPage({ params: Promise.resolve({ locale: "zh-TW", productId: productId.toUpperCase() }) }));
  expect(await screen.findByRole("dialog", { name: product.title })).toBeVisible();
});
