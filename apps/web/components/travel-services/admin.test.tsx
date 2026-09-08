import { afterEach, expect, it, vi } from "vitest";
import {
  cleanup,
  fireEvent,
  render,
  screen,
  waitFor,
  within,
} from "@testing-library/react";
import { TravelServicesAdmin } from "./admin";
import copy from "@/messages/zh-TW/travelServices.json";

const { request } = vi.hoisted(() => ({ request: vi.fn() }));
vi.mock("next-intl", async () => {
  const { createTranslator, createFormatter } =
    await vi.importActual<typeof import("next-intl")>("next-intl");
  return {
    useTranslations: () =>
      createTranslator({ locale: "zh-TW", messages: copy }),
    useFormatter: () =>
      createFormatter({ locale: "zh-TW", timeZone: "Asia/Taipei" }),
  };
});
vi.mock("@/lib/api", async (original) => ({
  ...(await original<typeof import("@/lib/api")>()),
  api: request,
}));
vi.mock("@/i18n/navigation", () => ({
  Link: ({ href, children }: { href: string; children: React.ReactNode }) => (
    <a href={href}>{children}</a>
  ),
}));
afterEach(() => {
  cleanup();
  vi.clearAllMocks();
});

const product = {
  id: "hotel-1",
  kind: "hotel",
  title: "Reviewed fixture",
  source_key: "fixture-1",
  source_url: "https://hotel.example.com/",
  destination_id: "tokyo",
  names_json: {},
  status: "approved",
  version: 3,
  facts: { area_code: "marunouchi", hotel_links: [] },
};
const overview = {
  products: [product],
  offers: [],
  destination_offers: [],
  destinations: [
    { id: "tokyo", city: "東京", country: "日本", role: "primary" },
  ],
  brands: [],
  network_configured: false,
  project_id: null,
  config: {
    public_enabled: false,
    enabled_kinds: [],
    enabled_destinations: [],
    direct_hotel_links_enabled: false,
  },
  version: 2,
  brand_definitions: {
    booking: {
      name: "Booking.com",
      kinds: ["hotel"],
      modules: ["hotel"],
      hosts: ["booking.com"],
      api_supported: true,
    },
  },
  coverage: [],
  review_due: 0,
  imports: [],
  operations: {},
};

it("edits exact hotel links without a network account and preserves other reviewed facts", async () => {
  request.mockResolvedValue(overview);
  render(<TravelServicesAdmin />);
  expect(
    await screen.findByText(copy.directIndependent, { exact: false }),
  ).toBeTruthy();
  fireEvent.click(screen.getByText(copy.platformReview));
  fireEvent.change(screen.getByLabelText(copy.hotelPageUrl), {
    target: { value: "https://hotel.example.com/stay" },
  });
  fireEvent.change(screen.getByLabelText(copy.hotelLinkEvidence), {
    target: { value: "https://hotel.example.com/location" },
  });
  fireEvent.click(screen.getByRole("button", { name: copy.saveHotelLinks }));
  await waitFor(() =>
    expect(request.mock.calls.some(([, opts]) => opts?.method === "PUT")).toBe(
      true,
    ),
  );
  const [path, options] = request.mock.calls.find(
    ([, opts]) => opts?.method === "PUT",
  )!;
  expect(path).toBe("/admin/travel-services/products/hotel-1/booking-options");
  const saved = JSON.parse(options.body);
  expect(saved.facts).toBeUndefined(); // Independent edit cannot rewrite hotel facts.
  expect(saved).toMatchObject({
    version: 0,
    provider: "official",
    url: "https://hotel.example.com/stay",
    evidence_url: "https://hotel.example.com/location",
  });
  expect(saved.status).toBeUndefined(); // Saving cannot self-approve the change.
});

it("has an independent ordinary-link switch without enabling public destinations", async () => {
  request.mockResolvedValue(overview);
  render(<TravelServicesAdmin />);
  await screen.findByRole("heading", { name: product.title });
  fireEvent.click(screen.getByRole("tab", { name: copy.config }));
  fireEvent.click(screen.getByLabelText(copy.directEnabled));
  const checkbox = screen.getByLabelText(copy.directEnabled);
  fireEvent.click(
    within(checkbox.closest("section")!).getByRole("button", {
      name: copy.apply,
    }),
  );
  await waitFor(() =>
    expect(request.mock.calls.some(([, opts]) => opts?.method === "PUT")).toBe(
      true,
    ),
  );
  const [, options] = request.mock.calls.find(
    ([, opts]) => opts?.method === "PUT",
  )!;
  expect(JSON.parse(options.body)).toMatchObject({
    direct_hotel_links_enabled: true,
    public_enabled: false,
    enabled_destinations: [],
    version: 2,
  });
});

it("loads saved identity evidence before an independent platform recheck", async () => {
  request.mockResolvedValue({
    ...overview,
    products: [
      {
        ...product,
        booking_options: [
          {
            id: "official-option",
            provider: "official",
            version: 4,
            url: "https://hotel.example.com/stay",
            property_id: "official-42",
            evidence_url: "https://hotel.example.com/location",
            identity_note: "Reviewed official name and address",
            discovery_status: "found",
            status: "approved",
            health_status: "healthy",
            verified_at: "2026-08-01T00:00:00Z",
          },
        ],
      },
    ],
  });
  render(<TravelServicesAdmin />);
  fireEvent.click(await screen.findByText(copy.platformReview));
  expect(
    (screen.getByLabelText(copy.identityNote) as HTMLTextAreaElement).value,
  ).toBe("Reviewed official name and address");
  expect(
    (screen.getByLabelText(copy.platformPropertyId) as HTMLInputElement).value,
  ).toBe("official-42");
  expect(
    (
      screen.getByRole("button", {
        name: copy.verifyOffer,
      }) as HTMLButtonElement
    ).disabled,
  ).toBe(false);
});

it("creates and batch-reviews destination offers without exposing arbitrary brands", async () => {
  const brand = {
    id: "11111111-1111-1111-1111-111111111111",
    code: "klook",
    name: "Klook",
    approval: "approved",
    enabled: true,
    evidence_url: "https://app.travelpayouts.com/programs?source=570089",
    verified_at: "2026-09-08T00:00:00Z",
    version: 2,
  };
  request.mockResolvedValue({
    ...overview,
    network_configured: true,
    brands: [brand],
    destination_offers: [
      {
        id: "22222222-2222-2222-2222-222222222222",
        brand_id: brand.id,
        destination_id: "tokyo",
        module: "activities",
        status: "pending",
        version: 1,
        target_url: "https://www.klook.com/city/28-tokyo/",
        static_url: null,
        verified_at: null,
      },
    ],
    brand_definitions: {
      klook: {
        name: "Klook",
        kinds: ["tour"],
        modules: ["activities"],
        hosts: ["klook.com"],
        api_supported: true,
      },
    },
  });
  render(<TravelServicesAdmin />);
  fireEvent.click(
    await screen.findByRole("tab", { name: copy.destinationOffers }),
  );
  fireEvent.click(screen.getByLabelText(copy.selectAll));
  fireEvent.click(screen.getByRole("button", { name: copy.batchApprove }));
  await waitFor(() =>
    expect(request).toHaveBeenCalledWith(
      "/admin/travel-services/destination-offers/batch-review",
      expect.objectContaining({ method: "POST" }),
    ),
  );
  const [, options] = request.mock.calls.find(
    ([path]) =>
      path === "/admin/travel-services/destination-offers/batch-review",
  )!;
  expect(JSON.parse(options.body)).toEqual({
    status: "approved",
    offers: [{ id: "22222222-2222-2222-2222-222222222222", version: 1 }],
  });
});
