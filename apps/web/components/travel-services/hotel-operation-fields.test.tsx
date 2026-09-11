import { useState } from "react";
import { afterEach, expect, it, vi } from "vitest";
import "@testing-library/jest-dom/vitest";
import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { HotelOperationFields } from "./hotel-operation-fields";
import { TravelServicesAdmin } from "./admin";
import { ApiError } from "@/lib/api";
import messages from "@/messages/zh-TW/travelServices.json";

const { request } = vi.hoisted(() => ({ request: vi.fn() }));
vi.mock("next/navigation", () => ({ useSearchParams: () => null, usePathname: () => window.location.pathname }));
vi.mock("@/components/header-session", () => ({ useHeaderSession: () => ({ user: { id: "operating-rules-admin" }, status: "authenticated" }) }));
vi.mock("@/lib/api", async (original) => ({ ...(await original<typeof import("@/lib/api")>()), api: request }));
vi.mock("@/components/admin-map-identities-panel", () => ({ AdminMapIdentitiesPanel: () => null }));
vi.mock("@/components/admin-settings-panel", () => ({ AdminSettingsPanel: () => null }));

const copy = messages.hotelOperation;
const range = { start_date: "2026-11-03", end_date: "2026-11-06", reason: "Maintenance announcement", source_url: "https://hotel.example.com/notice" };
const product = { title: "Hotel", facts: { facilities: ["wifi"], address: "49 Jilin Road", hotel_operating_rules: { unavailable_stays: [range] } } };

function Draft({ initial = JSON.stringify(product), disabled = false }: { initial?: string; disabled?: boolean }) {
  const [json, setJson] = useState(initial);
  return <><HotelOperationFields json={json} onChange={setJson} disabled={disabled} /><textarea aria-label="Original product JSON" value={json} onChange={(event) => setJson(event.target.value)} /></>;
}

afterEach(() => { cleanup(); vi.clearAllMocks(); sessionStorage.clear(); });

it("edits operating dates in the same JSON draft and preserves other facts", () => {
  render(<Draft />);
  expect(screen.getByLabelText(copy.startDate)).toHaveValue(range.start_date);
  expect(screen.getByText(copy.rangeHint)).toBeVisible();
  fireEvent.change(screen.getByLabelText(copy.endDate), { target: { value: "2026-11-07" } });
  const draft = JSON.parse((screen.getByLabelText("Original product JSON") as HTMLTextAreaElement).value);
  expect(draft.facts).toEqual({ ...product.facts, hotel_operating_rules: { unavailable_stays: [{ ...range, end_date: "2026-11-07" }] } });
  expect(request).not.toHaveBeenCalled();
  fireEvent.change(screen.getByLabelText("Original product JSON"), { target: { value: JSON.stringify({ ...draft, facts: { ...draft.facts, hotel_operating_rules: null } }) } });
  expect(screen.queryByLabelText(copy.startDate)).toBeNull();
});

it("adds a final checkout rule with its own reason/source and removes the final rule as null", () => {
  render(<Draft initial={JSON.stringify({ facts: { facilities: ["wifi"] } })} />);
  fireEvent.click(screen.getByRole("button", { name: copy.addCutoff }));
  fireEvent.change(screen.getByLabelText(copy.lastCheckoutDate), { target: { value: "2026-12-20" } });
  fireEvent.change(screen.getByLabelText(copy.reason), { target: { value: "Final operating day" } });
  fireEvent.change(screen.getByLabelText(copy.source), { target: { value: range.source_url } });
  expect(screen.queryByRole("alert")).toBeNull();
  expect(JSON.parse((screen.getByLabelText("Original product JSON") as HTMLTextAreaElement).value).facts.hotel_operating_rules).toEqual({ unavailable_stays: [], last_checkout_date: "2026-12-20", last_checkout_reason: "Final operating day", last_checkout_source_url: range.source_url });
  fireEvent.click(screen.getByRole("button", { name: copy.removeCutoff }));
  expect(JSON.parse((screen.getByLabelText("Original product JSON") as HTMLTextAreaElement).value).facts).toEqual({ facilities: ["wifi"], hotel_operating_rules: null });
});

it("leaves invalid JSON untouched and explains why date controls are unavailable", () => {
  render(<Draft initial={'{"facts":'} />);
  expect(screen.getByRole("alert")).toHaveTextContent(copy.errors.invalidJson);
  expect(screen.getByLabelText("Original product JSON")).toHaveValue('{"facts":');
  expect(screen.queryByRole("button", { name: copy.addRange })).toBeNull();
});

it("disables operating controls while the editor is saving or read-only", () => {
  render(<Draft disabled />);
  expect(screen.getByLabelText(copy.startDate)).toBeDisabled();
  expect(screen.getByRole("button", { name: copy.addRange })).toBeDisabled();
});

it("uses the existing versioned save, retains a rejected draft, and never self-approves", async () => {
  window.history.replaceState(null, "", "/zh-TW/admin/hotels?tab=catalog&section=catalog");
  const hotel = { ...product, id: "operating-hotel", source_key: "operating-hotel", kind: "hotel", source_url: "https://hotel.example.com", destination_id: "taipei", names_json: {}, status: "pending", version: 7, booking_options: [] };
  const overview = {
    summary: { total: 1, pending: 1, approved: 0, disabled: 0 }, products: [hotel], offers: [], destination_offers: [],
    destinations: [{ id: "taipei", city: "台北", country: "台灣", role: "primary" }], brands: [], network_configured: true, version: 2,
    config: { public_enabled: false, enabled_destinations: [], enabled_kinds: [], direct_hotel_links_enabled: false, hotel_quote_policies: {} },
    quote_providers: {}, brand_definitions: {}, coverage: [], review_due: 0, imports: [], operations: {},
  };
  let rejectSave = true;
  request.mockImplementation(async (_path, options) => {
    if (options?.method === "PUT" && rejectSave) throw new ApiError("Version conflict", 409, "service_version_conflict");
    return overview;
  });
  render(<TravelServicesAdmin workspace="hotels" />);
  fireEvent.click(await screen.findByRole("button", { name: messages.edit }));
  fireEvent.change(screen.getByLabelText(copy.endDate), { target: { value: "" } });
  expect(screen.getByRole("button", { name: copy.save })).toBeDisabled();
  expect((screen.getByLabelText(messages.productJson) as HTMLTextAreaElement).value).toContain('"end_date": ""');
  fireEvent.change(screen.getByLabelText(copy.endDate), { target: { value: "2026-11-08" } });
  expect(request.mock.calls.every(([, options]) => !options?.method)).toBe(true);
  fireEvent.click(screen.getByRole("button", { name: copy.save }));
  await screen.findByText("Version conflict");
  expect(screen.getByLabelText(copy.endDate)).toHaveValue("2026-11-08");
  const [path, init] = request.mock.calls.find(([, options]) => options?.method === "PUT")!;
  expect(path).toBe("/admin/travel-services/products/operating-hotel?version=7");
  expect(JSON.parse(init.body)).toMatchObject({ facts: { facilities: ["wifi"], address: "49 Jilin Road", hotel_operating_rules: { unavailable_stays: [{ ...range, end_date: "2026-11-08" }] } } });
  expect(JSON.parse(init.body).status).toBeUndefined();
  rejectSave = false;
  fireEvent.click(screen.getByRole("button", { name: copy.save }));
  await waitFor(() => expect(screen.queryByLabelText(messages.productJson)).toBeNull());
  expect(request.mock.calls.some(([path]) => path.endsWith("/review"))).toBe(false);
});
