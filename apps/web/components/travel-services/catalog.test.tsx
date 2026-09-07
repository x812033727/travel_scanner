import { afterEach, describe, expect, it, vi } from "vitest";
import {
  cleanup,
  fireEvent,
  render,
  screen,
  waitFor,
} from "@testing-library/react";
import { ServiceCatalog, TripTravelServices } from "./catalog";
import copy from "@/messages/zh-TW/travelServices.json";

const { request, navigate } = vi.hoisted(() => ({
  request: vi.fn(),
  navigate: vi.fn(),
}));
vi.mock("@/lib/api", async (original) => ({
  ...(await original<typeof import("@/lib/api")>()),
  api: request,
}));
vi.mock("@/i18n/navigation", () => ({
  Link: ({ href, children }: { href: string; children: React.ReactNode }) => (
    <a href={href}>{children}</a>
  ),
  useRouter: () => ({ push: navigate }),
}));

const hotel = {
  id: "hotel-1",
  kind: "hotel",
  destination_id: "tokyo",
  title: "Reviewed hotel",
  source_url: "https://official.example.com",
  distance_km: 1.23,
  reason: "trip_distance",
  facts: {
    languages: [],
    facilities: [],
    country_codes: ["JP"],
    reference_price: null,
    currency: null,
    tethering: null,
  },
  offers: [
    { id: "offer-1", brand_name: "Klook", brand: "klook", scope: "product" },
    {
      id: "offer-2",
      brand_name: "KKday",
      brand: "kkday",
      scope: "destination",
    },
  ],
};
const result = {
  enabled: true,
  enabled_kinds: ["hotel", "tour", "esim"],
  items: [hotel],
  areas: [],
  version: 2,
  start_date: "2026-11-11",
  end_date: "2026-11-13",
};

afterEach(() => {
  cleanup();
  vi.clearAllMocks();
  window.history.replaceState({}, "", "/");
});

describe("reviewed travel services", () => {
  it("ordinary hotel links work without partner offers or a commission disclosure", async () => {
    request.mockResolvedValue({
      ...result,
      items: [
        {
          ...hotel,
          offers: [],
          direct_links: [
            { provider: "official", name: null },
            { provider: "booking", name: "Booking.com" },
          ],
        },
      ],
    });
    render(<ServiceCatalog destinationId="tokyo" />);
    fireEvent.click(
      await screen.findByRole("button", { name: copy.platforms }),
    );
    expect(screen.getByText(copy.directDisclosure)).toBeTruthy();
    expect(screen.queryByText(copy.disclosure)).toBeNull();
    expect(screen.queryByText(copy.noOffers)).toBeNull();
    const form = screen
      .getByRole("button", {
        name: `${copy.officialHotel} · ${copy.ordinaryLink} · ${copy.newTab}`,
      })
      .closest("form");
    expect(form?.getAttribute("action")).toBe(
      "/api/travel/travel-services/hotel-1/hotel-links/official/clickout?locale=zh-TW",
    );
    expect(form?.getAttribute("method")).toBe("post");
    expect(form?.getAttribute("target")).toBe("_blank");
    expect(form?.getAttribute("rel")).toBe("noopener noreferrer");
    expect(
      screen
        .getByRole("button", { name: copy.selectHotel })
        .hasAttribute("disabled"),
    ).toBe(false);
    expect(request.mock.calls.some(([, opts]) => opts?.method === "POST")).toBe(
      false,
    );
  });

  it("keeps hotel selection available when reviewed links are missing or expired", async () => {
    request.mockResolvedValue({
      ...result,
      items: [{ ...hotel, offers: [], direct_links: [] }],
    });
    render(<ServiceCatalog destinationId="tokyo" />);
    fireEvent.click(
      await screen.findByRole("button", { name: copy.platforms }),
    );
    expect(screen.getByText(copy.noOffers)).toBeTruthy();
    expect(screen.queryByText(copy.disclosure)).toBeNull();
    expect(
      screen
        .getByRole("button", { name: copy.selectHotel })
        .hasAttribute("disabled"),
    ).toBe(false);
  });

  it("distinguishes exact and area links with safe new-tab POST forms and disclosure", async () => {
    request.mockResolvedValue(result);
    render(<ServiceCatalog destinationId="tokyo" />);
    expect(await screen.findByText("Reviewed hotel")).toBeTruthy();
    expect(screen.getByText(copy.externalPrices)).toBeTruthy();
    fireEvent.click(screen.getByRole("button", { name: copy.platforms }));
    expect(screen.getByText(copy.disclosure)).toBeTruthy();
    expect(screen.getByText(copy.productScope)).toBeTruthy();
    expect(screen.getByText(copy.destinationScope)).toBeTruthy();
    const link = screen
      .getByRole("button", {
        name: `Klook · ${copy.productScope} · ${copy.newTab}`,
      })
      .closest("form");
    expect(link?.getAttribute("method")).toBe("post");
    expect(link?.getAttribute("action")).toBe(
      "/api/travel/affiliates/offers/offer-1/clickout?locale=zh-TW&placement=destination",
    );
    expect(link?.getAttribute("target")).toBe("_blank");
    expect(link?.getAttribute("rel")).toBe("noopener noreferrer");
  });

  it("shows three cards and expands only on request", async () => {
    request.mockResolvedValue({
      ...result,
      items: [1, 2, 3, 4].map((id) => ({
        ...hotel,
        id: `hotel-${id}`,
        title: `Hotel ${id}`,
      })),
    });
    render(<ServiceCatalog destinationId="tokyo" />);
    await screen.findByText("Hotel 1");
    expect(screen.queryByText("Hotel 4")).toBeNull();
    fireEvent.click(
      screen.getByRole("button", {
        name: copy.viewAll.replace("{count}", "4"),
      }),
    );
    expect(screen.getByText("Hotel 4")).toBeTruthy();
  });

  it("flushes draft before selection, preserves unknown quote and releases mutation lock", async () => {
    const prepare = vi.fn(async () => ({ version: 9 }));
    const changed = vi.fn(async () => undefined);
    const onBusy = vi.fn();
    request.mockImplementation(async (_path: string, options?: RequestInit) =>
      options?.method === "POST" ? { version: 10 } : result,
    );
    render(
      <ServiceCatalog
        tripId="trip-1"
        prepare={prepare}
        onChanged={changed}
        onBusy={onBusy}
      />,
    );
    fireEvent.click(
      await screen.findByRole("button", { name: copy.selectHotel }),
    );
    expect(screen.getByText(/2026-11-11.*2026-11-13/)).toBeTruthy();
    fireEvent.click(screen.getByRole("button", { name: copy.confirm }));
    await waitFor(() => expect(changed).toHaveBeenCalledTimes(1));
    const post = request.mock.calls.find(
      ([, options]) => options?.method === "POST",
    );
    expect(JSON.parse(post?.[1].body)).toEqual({
      product_id: "hotel-1",
      version: 9,
    });
    expect(post?.[1].headers["Idempotency-Key"]).toBeTruthy();
    expect(prepare.mock.invocationCallOrder[0]).toBeLessThan(
      changed.mock.invocationCallOrder[0],
    );
    expect(onBusy.mock.calls).toEqual([[true], [false]]);
  });

  it("does not mutate if draft cannot be saved", async () => {
    request.mockResolvedValue(result);
    render(<ServiceCatalog tripId="trip-1" prepare={async () => false} />);
    fireEvent.click(
      await screen.findByRole("button", { name: copy.selectHotel }),
    );
    fireEvent.click(screen.getByRole("button", { name: copy.confirm }));
    await waitFor(() =>
      expect(
        screen
          .getByRole("button", { name: copy.confirm })
          .hasAttribute("disabled"),
      ).toBe(false),
    );
    expect(
      request.mock.calls.some(([, options]) => options?.method === "POST"),
    ).toBe(false);
  });

  it("failed collection renders an explicit retry without fabricated cards", async () => {
    request.mockRejectedValue(new Error("Unavailable fixture"));
    render(<ServiceCatalog destinationId="tokyo" />);
    expect(await screen.findByRole("alert")).toBeTruthy();
    expect(screen.queryByText("Reviewed hotel")).toBeNull();
    request.mockResolvedValue({ ...result, items: [] });
    fireEvent.click(screen.getByRole("button", { name: copy.retry }));
    expect(await screen.findByText(copy.empty)).toBeTruthy();
  });

  it("uses the shared modal with back state and closes on browser navigation", async () => {
    request.mockImplementation(async (path: string) =>
      path.endsWith("/config")
        ? { enabled_kinds: ["hotel"], enabled_destinations: ["tokyo"] }
        : result,
    );
    render(<TripTravelServices tripId="trip-1" />);
    fireEvent.click(await screen.findByRole("button", { name: copy.hotel }));
    const dialog = await screen.findByRole("dialog");
    expect(dialog.getAttribute("aria-modal")).toBe("true");
    expect(window.history.state.serviceSheet).toBeTruthy();
    fireEvent(window, new PopStateEvent("popstate"));
    expect(screen.queryByRole("dialog")).toBeNull();
  });
});
