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
import common from "@/messages/zh-TW/common.json";
import copy from "@/messages/zh-TW/travelServices.json";
import { adminHotelsCopy } from "@/lib/admin-hotels-copy";
import { klookAffiliateCopy } from "@/lib/klook-affiliate-copy";

const { request, router } = vi.hoisted(() => ({ request: vi.fn(), router: { replace: vi.fn() } }));
vi.mock("next/navigation", () => ({ useSearchParams: () => null, usePathname: () => window.location.pathname }));
vi.mock("@/components/header-session", () => ({ useHeaderSession: () => ({ user: { id: "admin-test" }, status: "authenticated" }) }));
vi.mock("@/components/admin-settings-panel", () => ({ AdminSettingsPanel: () => <div /> }));
vi.mock("next-intl", async () => {
  const { createTranslator, createFormatter } =
    await vi.importActual<typeof import("next-intl")>("next-intl");
  return {
    useLocale: () => "zh-TW",
    // The workspace reads its own namespace plus `common` for the guide-section label.
    useTranslations: (namespace?: string) =>
      createTranslator({ locale: "zh-TW", messages: namespace === "common" ? common : copy }),
    useFormatter: () =>
      createFormatter({ locale: "zh-TW", timeZone: "Asia/Taipei" }),
  };
});
vi.mock("@/lib/api", async (original) => ({
  ...(await original<typeof import("@/lib/api")>()),
  api: request,
}));
vi.mock("@/i18n/navigation", () => ({
  useRouter: () => router,
  Link: ({ href, children }: { href: string; children: React.ReactNode }) => (
    <a href={href}>{children}</a>
  ),
}));
afterEach(() => {
  cleanup();
  vi.clearAllMocks();
  window.history.replaceState(null, "", "/zh-TW/admin/travel-services");
  sessionStorage.clear();
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

const klookDefinition = { name: "Klook", kinds: ["hotel", "tour", "transfer"], modules: ["hotel", "activities", "transport"], hosts: ["klook.com"], api_supported: false };
const legacyKlook = { id: "legacy-brand", code: "klook", name: "Klook", approval: "approved", enabled: true, evidence_url: "https://app.travelpayouts.com/programs/approved", verified_at: null, version: 7 };
const directKlook = { ...legacyKlook, id: "direct-brand", channel: "klook_direct", approval: "pending", enabled: false, evidence_url: "https://www.klook.com/affiliate/approval", version: 2 };

it("keeps direct Klook evidence, activation and version separate from the legacy channel", async () => {
  request.mockResolvedValue({ ...overview, brands: [legacyKlook, directKlook], brand_definitions: { klook: klookDefinition }, channels: { travelpayouts: { configured: false }, klook_direct: { configured: true } } });
  window.history.replaceState(null, "", "/zh-TW/admin/partners");
  render(<TravelServicesAdmin workspace="partners" />);
  const affiliate = klookAffiliateCopy("zh-TW");
  fireEvent.click(await screen.findByRole("button", { name: "Klook · Klook 直接分潤" }));
  expect((screen.getByLabelText(affiliate.evidence) as HTMLInputElement).value).toBe(directKlook.evidence_url);
  expect((screen.getByLabelText(copy.enabled) as HTMLInputElement).checked).toBe(false);
  expect(screen.getByText(affiliate.noApi)).toBeTruthy();
  expect(screen.getByRole("link", { name: affiliate.configure }).getAttribute("href")).toBe("/admin/settings?provider=klook&field=klook_affiliate_id");
  fireEvent.change(screen.getByLabelText(copy.approval), { target: { value: "approved" } });
  fireEvent.click(screen.getByLabelText(copy.enabled));
  fireEvent.click(screen.getByRole("button", { name: copy.apply }));
  await waitFor(() => expect(request.mock.calls.some(([, opts]) => opts?.method === "PUT")).toBe(true));
  const [, options] = request.mock.calls.find(([, opts]) => opts?.method === "PUT")!;
  expect(JSON.parse(options.body)).toEqual({ code: "klook", channel: "klook_direct", approval: "approved", enabled: true, evidence_url: directKlook.evidence_url, version: 2 });
  await waitFor(() => expect((screen.getByRole("button", { name: copy.apply }) as HTMLButtonElement).disabled).toBe(false));
  fireEvent.click(screen.getByRole("button", { name: "Klook · Travelpayouts" }));
  expect((screen.getByLabelText(affiliate.evidence) as HTMLInputElement).value).toBe(legacyKlook.evidence_url);
  expect((screen.getByLabelText(copy.enabled) as HTMLInputElement).checked).toBe(true);
  expect(request.mock.calls.filter(([, opts]) => opts?.method === "PUT")).toHaveLength(1);
});

it("does not inherit legacy approval or invent evidence when the direct brand does not exist", async () => {
  request.mockResolvedValue({ ...overview, brands: [legacyKlook], brand_definitions: { klook: klookDefinition } });
  window.history.replaceState(null, "", "/zh-TW/admin/partners");
  render(<TravelServicesAdmin workspace="partners" />);
  fireEvent.click(await screen.findByRole("button", { name: "Klook · Klook 直接分潤" }));
  expect((screen.getByLabelText(klookAffiliateCopy("zh-TW").evidence) as HTMLInputElement).value).toBe("");
  expect((screen.getByLabelText(copy.approval) as HTMLSelectElement).value).toBe("pending");
  expect((screen.getByRole("button", { name: copy.apply }) as HTMLButtonElement).disabled).toBe(true);
});

it("labels both channels and omits static tracking URLs when creating a direct destination offer", async () => {
  request.mockResolvedValue({ ...overview, brands: [legacyKlook, { ...directKlook, approval: "approved" }], brand_definitions: { klook: klookDefinition } });
  render(<TravelServicesAdmin />);
  fireEvent.click(await screen.findByRole("tab", { name: copy.destinationOffers }));
  const create = screen.getByRole("heading", { name: copy.destinationOfferCreate }).parentElement!;
  expect(within(create).getByRole("option", { name: /Klook · Travelpayouts/ })).toBeTruthy();
  expect(within(create).getByRole("option", { name: /Klook · Klook 直接分潤/ })).toBeTruthy();
  fireEvent.change(within(create).getByLabelText(copy.brands), { target: { value: "direct-brand" } });
  expect(within(create).queryByLabelText(copy.staticUrl)).toBeNull();
  fireEvent.change(within(create).getByLabelText(copy.destinationLink), { target: { value: "tokyo" } });
  fireEvent.change(within(create).getByLabelText(copy.originalUrl), { target: { value: "https://www.klook.com/city/28-tokyo/" } });
  fireEvent.click(within(create).getByRole("button", { name: copy.addDestinationOffer }));
  await waitFor(() => expect(request.mock.calls.some(([, opts]) => opts?.method === "POST")).toBe(true));
  const [, options] = request.mock.calls.find(([, opts]) => opts?.method === "POST")!;
  expect(JSON.parse(options.body)).toEqual({ brand_id: "direct-brand", destination_id: "tokyo", module: "activities", target_url: "https://www.klook.com/city/28-tokyo/" });
});

it.each(["product", "destination"])("records explicit direct %s browser evidence for only the reviewed version", async (kind) => {
  const offer = { id: "reviewed-offer", product_id: product.id, brand_id: "direct-brand", destination_id: "tokyo", module: "activities", status: "pending", version: 3, target_url: "https://www.klook.com/activity/12345-tokyo/", static_url: null, verified_at: null, scope: "product" };
  let data = { ...overview, brands: [directKlook], brand_definitions: { klook: klookDefinition }, offers: kind === "product" ? [offer] : [], destination_offers: kind === "destination" ? [offer] : [] };
  request.mockImplementation(async () => data);
  render(<TravelServicesAdmin />);
  if (kind === "destination") fireEvent.click(await screen.findByRole("tab", { name: copy.destinationOffers }));
  const affiliate = klookAffiliateCopy("zh-TW");
  const checkbox = await screen.findByLabelText(affiliate.browserVerified);
  expect((checkbox as HTMLInputElement).checked).toBe(false);
  expect(request.mock.calls.some(([, opts]) => opts?.method === "POST")).toBe(false);
  fireEvent.click(checkbox);
  expect((screen.getByLabelText(affiliate.browserEvidence) as HTMLInputElement).value).toBe(offer.target_url);
  data = { ...data, offers: data.offers.map((row) => ({ ...row, version: 4 })), destination_offers: data.destination_offers.map((row) => ({ ...row, version: 4 })) };
  fireEvent.click(screen.getByRole("button", { name: kind === "product" ? copy.verifyOffer : copy.approve }));
  await waitFor(() => expect(request.mock.calls.some(([, opts]) => opts?.method === "POST")).toBe(true));
  const [path, options] = request.mock.calls.find(([, opts]) => opts?.method === "POST")!;
  expect(path).toBe(`/admin/travel-services/${kind === "product" ? "offers" : "destination-offers"}/reviewed-offer/review`);
  expect(JSON.parse(options.body)).toEqual({ version: 3, status: "approved", browser_verified: true, evidence_url: offer.target_url });
  await waitFor(() => expect((screen.getByLabelText(affiliate.browserVerified) as HTMLInputElement).checked).toBe(false));
});

it("edits exact hotel links without a network account and preserves other reviewed facts", async () => {
  request.mockResolvedValue(overview);
  window.history.replaceState(null, "", "/zh-TW/admin/hotels?tab=review&section=platforms");
  render(<TravelServicesAdmin workspace="hotels" />);
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
  window.history.replaceState(null, "", "/zh-TW/admin/hotels");
  render(<TravelServicesAdmin workspace="hotels" />);
  await screen.findByRole("heading", { name: product.title });
  fireEvent.click(screen.getByRole("tab", { name: adminHotelsCopy("zh-TW").settings }));
  fireEvent.click(screen.getByLabelText(copy.directEnabled));
  const checkbox = screen.getByLabelText(copy.directEnabled);
  fireEvent.click(
    within(checkbox.closest("section")!).getByRole("button", {
      name: copy.apply,
    }),
  );
  await waitFor(() =>
    expect(request.mock.calls.some(([, opts]) => opts?.method === "PATCH")).toBe(
      true,
    ),
  );
  const [, options] = request.mock.calls.find(
    ([, opts]) => opts?.method === "PATCH",
  )!;
  expect(JSON.parse(options.body)).toEqual({
    direct_hotel_links_enabled: true,
    hotel_enabled: false,
    hotel_quote_policies: {},
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
  window.history.replaceState(null, "", "/zh-TW/admin/hotels?tab=review&section=platforms");
  render(<TravelServicesAdmin workspace="hotels" />);
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

it("lets an operator open the guide and city surfaces for destination offers without dropping the legacy ones", async () => {
  request.mockResolvedValue(overview);
  // The workspace reads its tab from the URL; `config` is the release-controls panel.
  window.history.replaceState(null, "", "/zh-TW/admin/travel-services?tab=config");
  render(<TravelServicesAdmin workspace="services" />);
  const guide = await screen.findByLabelText(common.guides.hubTitle);
  expect((guide as HTMLInputElement).checked).toBe(false);
  const share = screen.getByLabelText(common.cardActions.share);
  expect((share as HTMLInputElement).checked).toBe(false);
  fireEvent.click(guide);
  fireEvent.click(share);
  fireEvent.click(screen.getByRole("button", { name: copy.apply }));
  await waitFor(() => expect(request.mock.calls.some(([path, opts]) => String(path).endsWith("/config") && opts?.method === "PUT")).toBe(true));
  const [, options] = request.mock.calls.find(([path, opts]) => String(path).endsWith("/config") && opts?.method === "PUT")!;
  const saved = JSON.parse(String(options.body));
  expect(saved.affiliate_placements).toEqual(["destination", "hotspot", "trip", "stay", "checklist", "discovery", "guide", "share"]);
  expect(saved.public_enabled).toBe(false);
});
