import { afterEach, describe, expect, it, vi } from "vitest";
import {
  cleanup,
  fireEvent,
  render,
  screen,
  waitFor,
} from "@testing-library/react";
import copy from "@/messages/zh-TW/travelServices.json";
import { HotelQuotes } from "./hotel-quotes";
const { request } = vi.hoisted(() => ({ request: vi.fn() }));
vi.mock("@/lib/api", () => ({ api: request }));
vi.mock("next-intl", () => ({
  useFormatter: () => ({
    number: (v: number, o: Intl.NumberFormatOptions) =>
      new Intl.NumberFormat("zh-TW", o).format(v),
    dateTime: (v: Date, o: Intl.DateTimeFormatOptions) =>
      new Intl.DateTimeFormat("zh-TW", o).format(v),
  }),
  useTranslations:
    () =>
    (key: string, args: Record<string, string | number> = {}) => {
      let v: unknown = copy;
      for (const p of key.split(".")) v = (v as Record<string, unknown>)[p];
      return Object.entries(args).reduce(
        (s, [k, val]) => s.replaceAll(`{${k}}`, String(val)),
        String(v),
      );
    },
}));
afterEach(() => {
  cleanup();
  vi.clearAllMocks();
});
describe("hotel quote readiness", () => {
  it("does not request APIs or require dates when unconfigured", () => {
    render(<HotelQuotes productId="fixture" enabled={false} />);
    expect(screen.getByText(copy.quoteNotConfigured)).toBeTruthy();
    expect(screen.queryByRole("button")).toBeNull();
    expect(request).not.toHaveBeenCalled();
  });
  it("only sends explicit occupancy and distinguishes provider failures", async () => {
    request.mockResolvedValue({
      status: "partial",
      providers: [
        { provider: "booking", status: "available" },
        { provider: "trip_com", status: "timeout" },
      ],
      quotes: [],
    });
    render(
      <HotelQuotes
        productId="fixture"
        enabled
        startDate="2027-11-11"
        endDate="2027-11-13"
      />,
    );
    expect(request).not.toHaveBeenCalled();
    fireEvent.change(screen.getByLabelText(copy.quoteCountry), {
      target: { value: "TW" },
    });
    fireEvent.click(screen.getByText(copy.quoteAddChild));
    fireEvent.change(
      screen.getByLabelText(copy.quoteChildAge.replace("{number}", "1")),
      { target: { value: "7" } },
    );
    fireEvent.click(screen.getByRole("button", { name: copy.quoteSearch }));
    await waitFor(() => expect(request).toHaveBeenCalledTimes(1));
    const body = JSON.parse(request.mock.calls[0][1].body);
    expect(body.rooms).toEqual([{ adults: 2, children_ages: [7] }]);
    expect(body).not.toHaveProperty("url");
    await screen.findByText(`Trip.com · ${copy.quoteProviderState.timeout}`);
    expect(screen.queryByText(copy.quoteLowest)).toBeNull();
  });
});
