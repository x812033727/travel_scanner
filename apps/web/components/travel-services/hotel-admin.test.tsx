import { afterEach, expect, it, vi } from "vitest";
import "@testing-library/jest-dom/vitest";
import { act, cleanup, fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { TravelServicesAdmin } from "./admin";
import messages from "@/messages/zh-TW/travelServices.json";
import { adminHotelsCopy } from "@/lib/admin-hotels-copy";
import { ApiError } from "@/lib/api";

const { request, router, member } = vi.hoisted(() => ({ request: vi.fn(), router: { replace: vi.fn() }, member: { id: "admin-test" } }));
vi.mock("next/navigation", () => ({ useSearchParams: () => null, usePathname: () => window.location.pathname }));
vi.mock("@/components/header-session", () => ({ useHeaderSession: () => ({ user: member, status: "authenticated" }) }));
vi.mock("next-intl", async () => {
  const { createTranslator, createFormatter } = await vi.importActual<typeof import("next-intl")>("next-intl");
  return {
    useLocale: () => "zh-TW",
    useTranslations: () => createTranslator({ locale: "zh-TW", messages }),
    useFormatter: () => createFormatter({ locale: "zh-TW", timeZone: "Asia/Taipei" }),
  };
});
vi.mock("@/lib/api", async (original) => ({ ...(await original<typeof import("@/lib/api")>()), api: request }));
vi.mock("@/i18n/navigation", () => ({
  useRouter: () => router,
  Link: ({ href, children }: { href: string; children: React.ReactNode }) => <a href={href}>{children}</a>,
}));
vi.mock("@/components/admin-settings-panel", () => ({
  AdminSettingsPanel: ({ scope }: { scope: string }) => <label>{scope} provider draft<input aria-label="Provider draft" defaultValue="" /></label>,
}));
const copy = adminHotelsCopy("zh-TW");
const hotel = {
  id: "hotel-one", source_key: "hotel-one", kind: "hotel", title: "Reviewed hotel",
  source_url: "https://hotel.example.com", destination_id: "tokyo", names_json: {},
  facts: {}, status: "pending", version: 3, booking_options: [],
};
const overview = {
  summary: { total: 1, pending: 1, approved: 0, disabled: 0 },
  products: [hotel], offers: [], destination_offers: [],
  destinations: [{ id: "tokyo", city: "東京", country: "日本", role: "primary" }],
  brands: [], network_configured: true, project_id: "fixture", version: 4,
  config: { public_enabled: false, enabled_destinations: ["tokyo"], enabled_kinds: [], direct_hotel_links_enabled: false, hotel_quote_policies: {} },
  quote_providers: {},
  brand_definitions: {
    klook: { name: "Klook", kinds: ["hotel", "tour"], modules: ["hotel", "activities"], hosts: ["klook.com"] },
    kkday: { name: "KKday", kinds: ["hotel", "tour"], modules: ["hotel", "activities"], hosts: ["kkday.com"] },
  },
  coverage: [], review_due: 0, imports: [], operations: {},
};
afterEach(() => {
  cleanup(); vi.clearAllMocks();
  window.history.replaceState(null, "", "/zh-TW/admin/hotels");
  sessionStorage.clear();
  member.id = "admin-test";
});
function openHotel(query = "") {
  window.history.replaceState(null, "", `/zh-TW/admin/hotels${query}`);
  request.mockResolvedValue(overview);
  render(<TravelServicesAdmin workspace="hotels" />);
}

it("uses a hotel-only endpoint and exposes five canonical workspace tabs", async () => {
  openHotel();
  await screen.findByRole("heading", { name: hotel.title });
  expect(request.mock.calls[0][0]).toMatch(/^\/admin\/hotels\?/);
  expect(screen.getAllByRole("tab")).toHaveLength(5);
  expect(screen.queryByRole("button", { name: messages.approve })).toBeNull();
  expect(screen.getByRole("link", { name: copy.partners })).toHaveAttribute("href", "/admin/partners");
  fireEvent.click(screen.getByRole("tab", { name: copy.review }));
  expect(new URL(window.location.href).searchParams.get("tab")).toBe("review");
  expect(screen.getByRole("button", { name: messages.approve })).toBeTruthy();
  fireEvent.click(screen.getByRole("button", { name: copy.platforms }));
  expect(new URL(window.location.href).searchParams.get("section")).toBe("platforms");
  expect(screen.queryByRole("button", { name: messages.approve })).toBeNull();
  fireEvent.click(screen.getByText(messages.platformReview));
  const options = within(screen.getByLabelText(messages.bookingProvider)).getAllByRole("option");
  expect(options).toHaveLength(8);
  expect(options.map((option) => (option as HTMLOptionElement).value)).toContain("klook");
  expect(options.map((option) => (option as HTMLOptionElement).value)).toContain("kkday");
  fireEvent.change(screen.getByLabelText(messages.hotelPageUrl), { target: { value: "https://hotel.example.com/draft" } });
  fireEvent.keyDown(screen.getByRole("tab", { name: copy.review }), { key: "End" });
  expect(screen.getByRole("tab", { name: copy.settings })).toHaveFocus();
  fireEvent.click(screen.getByRole("tab", { name: copy.review }));
  fireEvent.click(screen.getByRole("button", { name: copy.platforms }));
  expect(screen.getByLabelText(messages.hotelPageUrl)).toHaveValue("https://hotel.example.com/draft");
});

it("keeps hotel and provider drafts across tabs while locking shared gates and unavailable quote adapters", async () => {
  openHotel("?tab=settings&section=catalog");
  const direct = await screen.findByLabelText(messages.directEnabled);
  expect(screen.getByLabelText(messages.publicEnabled)).toBeDisabled();
  expect(screen.getByLabelText("日本 · 東京")).toBeDisabled();
  expect(screen.queryByLabelText(messages.feedEnabled)).toBeNull();
  fireEvent.click(direct);
  fireEvent.click(screen.getByText(messages.quotePermissions));
  expect(screen.getAllByLabelText(messages.enabled).every((input) => (input as HTMLInputElement).disabled)).toBe(true);
  fireEvent.click(screen.getByRole("button", { name: copy.providers }));
  fireEvent.change(screen.getByLabelText("Provider draft"), { target: { value: "unsaved provider" } });
  fireEvent.click(screen.getByRole("tab", { name: copy.catalog }));
  fireEvent.click(screen.getByRole("tab", { name: copy.settings }));
  expect(screen.getByLabelText(messages.directEnabled)).toBeChecked();
  fireEvent.click(screen.getByRole("button", { name: copy.providers }));
  expect(screen.getByLabelText("Provider draft")).toHaveValue("unsaved provider");
  expect(request.mock.calls.every(([, init]) => !init?.method)).toBe(true);
});

it("uses scoped CSV preview and refuses to commit rejected rows", async () => {
  openHotel("?tab=imports&section=import");
  await screen.findByText(copy.hotelOnly);
  fireEvent.change(screen.getByRole("textbox"), { target: { value: "kind\ntour" } });
  request.mockImplementation(async (path: string) => path.endsWith("/imports/preview") ? {
    id: "preview", rows_json: [{ line: 2, error: "service_import_scope_mismatch" }],
  } : overview);
  fireEvent.click(screen.getByRole("button", { name: messages.preview }));
  expect(await screen.findByRole("button", { name: messages.commit })).toBeDisabled();
  expect(request).toHaveBeenCalledWith("/admin/hotels/imports/preview", expect.objectContaining({ method: "POST" }));
});

it("matches dashboard review and missing-booking-link filters without narrowing the normal catalog", async () => {
  openHotel("?tab=review&section=products");
  await waitFor(() => expect(request.mock.calls[0][0]).toContain("status=pending"));
  expect(await screen.findByLabelText(messages.pending)).toBeDisabled();
  fireEvent.click(screen.getByRole("tab", { name: copy.catalog }));
  await waitFor(() => expect(request.mock.calls.at(-1)![0]).not.toContain("status="));
  act(() => {
    window.history.replaceState(null, "", "/zh-TW/admin/hotels?tab=review&section=platforms&missing_options=true");
    window.dispatchEvent(new PopStateEvent("popstate"));
  });
  await waitFor(() => expect(request.mock.calls.at(-1)![0]).toContain("missing_options=true"));
  expect(request.mock.calls.at(-1)![0]).not.toContain("status=pending");
  expect(screen.getByRole("link", { name: copy.showAllHotels })).toHaveAttribute("href", "/admin/hotels?tab=review&section=platforms");
});

it("guards hotel config navigation and restores only this member's non-secret draft after remount", async () => {
  openHotel("?tab=settings&section=catalog");
  fireEvent.click(await screen.findByLabelText(messages.directEnabled));
  const confirm = vi.spyOn(window, "confirm").mockReturnValue(false);
  const departure = new CustomEvent("admin:before-navigate", { cancelable: true, detail: { url: "/zh-TW/admin/partners" } });
  expect(window.dispatchEvent(departure)).toBe(false);
  expect(fireEvent.click(screen.getByRole("link", { name: copy.partners }))).toBe(false);
  const unloading = new Event("beforeunload", { cancelable: true });
  expect(window.dispatchEvent(unloading)).toBe(false);
  expect(confirm).toHaveBeenCalledWith(copy.leave);
  const stored = sessionStorage.getItem("mokaair:admin:hotel-config-draft:v1:admin-test");
  expect(JSON.parse(stored!)).toEqual({ version: 4, hotel_enabled: false, direct_hotel_links_enabled: true, hotel_quote_policies: {} });
  cleanup();
  request.mockResolvedValue({ ...overview, version: 5 });
  render(<TravelServicesAdmin workspace="hotels" />);
  await waitFor(() => expect(screen.getByLabelText(messages.directEnabled)).toBeChecked());
  cleanup();
  member.id = "another-admin";
  render(<TravelServicesAdmin workspace="hotels" />);
  await waitFor(() => expect(screen.getByLabelText(messages.directEnabled)).not.toBeChecked());
  confirm.mockRestore();
});

it("retains the original config version after a filtered refresh so concurrent saves conflict safely", async () => {
  openHotel("?tab=settings&section=catalog");
  fireEvent.click(await screen.findByLabelText(messages.directEnabled));
  request.mockResolvedValue({ ...overview, version: 5 });
  fireEvent.click(screen.getByRole("tab", { name: copy.catalog }));
  fireEvent.change(screen.getByLabelText(messages.pending), { target: { value: "pending" } });
  await waitFor(() => expect(request.mock.calls.some(([path]) => path.includes("status=pending"))).toBe(true));
  fireEvent.click(screen.getByRole("tab", { name: copy.settings }));
  fireEvent.click(screen.getByRole("button", { name: messages.apply }));
  await waitFor(() => expect(request.mock.calls.some(([path]) => path === "/admin/hotels/config")).toBe(true));
  const [, init] = request.mock.calls.find(([path]) => path === "/admin/hotels/config")!;
  expect(JSON.parse(init.body)).toEqual({ version: 4, hotel_enabled: false, direct_hotel_links_enabled: true, hotel_quote_policies: {} });
});

it("ignores an aborted older filter result", async () => {
  window.history.replaceState(null, "", "/zh-TW/admin/hotels");
  let resolveOld!: (value: typeof overview) => void;
  request.mockImplementation((path: string) => path.includes("status=pending") ? Promise.resolve(overview) : new Promise((resolve) => { resolveOld = resolve; }));
  render(<TravelServicesAdmin workspace="hotels" />);
  await waitFor(() => expect(request).toHaveBeenCalled());
  // Deliver the initial response, then race two subsequent destination/status requests.
  await act(async () => resolveOld(overview));
  fireEvent.change(screen.getByLabelText(messages.destinationLink), { target: { value: "tokyo" } });
  await waitFor(() => expect(request.mock.calls.length).toBe(2));
  fireEvent.change(screen.getByLabelText(messages.pending), { target: { value: "pending" } });
  await waitFor(() => expect(request.mock.calls.length).toBe(3));
  await act(async () => resolveOld({ ...overview, products: [{ ...hotel, title: "Stale hotel" }] }));
  expect(screen.queryByText("Stale hotel")).toBeNull();
  expect(screen.getByRole("heading", { name: hotel.title })).toBeTruthy();
});

it("retains conflicted settings until an explicit confirmed reload", async () => {
  openHotel("?tab=settings&section=catalog");
  fireEvent.click(await screen.findByLabelText(messages.directEnabled));
  request.mockImplementation(async (path: string) => {
    if (path === "/admin/hotels/config") throw new ApiError("Conflict", 409, "service_version_conflict");
    return { ...overview, version: 5 };
  });
  fireEvent.click(screen.getByRole("button", { name: messages.apply }));
  await screen.findByText(copy.conflict);
  expect(screen.getByLabelText(messages.directEnabled)).toBeChecked();
  const confirm = vi.spyOn(window, "confirm").mockReturnValueOnce(false).mockReturnValueOnce(true);
  fireEvent.click(screen.getByRole("button", { name: copy.reload }));
  expect(screen.getByLabelText(messages.directEnabled)).toBeChecked();
  fireEvent.click(screen.getByRole("button", { name: copy.reload }));
  await waitFor(() => expect(screen.getByLabelText(messages.directEnabled)).not.toBeChecked());
  expect(screen.queryByText(copy.conflict)).toBeNull();
  confirm.mockRestore();
});

it.each(["?type=hotel", "?tab=hotel", "#hotel"])("adapts old hotel link %s to the canonical hotel workspace", async (suffix) => {
  window.history.replaceState(null, "", `/zh-TW/admin/travel-services${suffix}`);
  request.mockResolvedValue(overview);
  render(<TravelServicesAdmin />);
  await waitFor(() => expect(router.replace).toHaveBeenCalledWith(expect.stringMatching(/^\/admin\/hotels\?/)));
  expect(request).not.toHaveBeenCalled();
});

it("keeps other travel services separate and brands on their canonical page", async () => {
  window.history.replaceState(null, "", "/zh-TW/admin/travel-services");
  request.mockResolvedValue({ ...overview, products: [] });
  const view = render(<TravelServicesAdmin />);
  await waitFor(() => expect(request.mock.calls[0][0]).toContain("exclude_hotels=true"));
  expect(screen.getByRole("link", { name: copy.title })).toBeTruthy();
  expect(screen.queryByRole("tab", { name: messages.brands })).toBeNull();
  view.unmount();
  window.history.replaceState(null, "", "/zh-TW/admin/partners");
  render(<TravelServicesAdmin workspace="partners" />);
  expect(await screen.findByRole("tab", { name: messages.brands })).toBeTruthy();
  expect(screen.getAllByRole("tab")).toHaveLength(1);
});

it("provides the same hotel workspace vocabulary in all five locales", () => {
  const keys = Object.keys(adminHotelsCopy("en"));
  for (const locale of ["en", "ja", "ko", "zh-TW", "zh-CN"]) {
    expect(Object.keys(adminHotelsCopy(locale))).toEqual(keys);
    expect(Object.values(adminHotelsCopy(locale)).every(Boolean)).toBe(true);
  }
});
