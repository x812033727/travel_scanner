import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { AccountList } from "./account-list";

/**
 * vitest.setup.tsx hands every component the zh-TW catalog, so in every other test
 * here a hardcoded Chinese string and a translated one look exactly the same. This
 * file swaps the catalog for one that echoes the key it was asked for, and reads
 * the list as an English-speaking member: any Han character still on screen is copy
 * the component wrote itself, which no other language can ever reach.
 *
 * It is its own file because vi.mock is hoisted per file — overriding the shared
 * next-intl mock inside account-list.test.tsx would take that suite's copy with it.
 */
vi.mock("next-intl", () => ({
  useLocale: () => "en",
  useFormatter: () => ({ number: (value: number) => String(value) }),
  useTranslations: (namespace: string) =>
    Object.assign((key: string) => `[${namespace}.${key}]`, { has: () => true }),
}));

const apiMock = vi.fn();
vi.mock("@/lib/api", async () => {
  const actual = await vi.importActual<typeof import("@/lib/api")>("@/lib/api");
  return { ...actual, api: (...args: unknown[]) => apiMock(...args) };
});

const HAN = /\p{Script=Han}/u;

const trip = {
  id: "trip-1",
  name: "Kyoto in five days",
  destination_name: "Kyoto",
  start_date: "2026-11-10",
  end_date: "2026-11-14",
  status: "ready",
  total_price: 48000,
  currency: "TWD",
};
const alert = {
  id: "alert-1",
  resource_type: "flight",
  resource_id: "flight-1",
  title: "Starlux",
  subtitle: "TPE → NRT",
  target_price: 14000,
  current_price: 15000,
  currency: "TWD",
  price_updated_at: "2026-08-31T08:00:00Z",
  active: true,
  monitoring_mode: "manual_only",
};
const usage = { limits: { saved_trips: 20, price_alerts: 20 }, counts: { saved_trips: 1, price_alerts: 1 } };

function stub(routes: Record<string, (init?: RequestInit) => unknown>) {
  apiMock.mockImplementation(async (path: string, init?: RequestInit) => {
    const handler = routes[`${init?.method || "GET"} ${path}`];
    if (!handler) throw new Error(`unexpected api call ${init?.method || "GET"} ${path}`);
    return handler(init);
  });
}

/** Every character the reader can actually see, including labels read aloud. */
function visibleText() {
  const attributes = [...document.querySelectorAll("[aria-label], [placeholder]")]
    .flatMap((node) => [node.getAttribute("aria-label"), node.getAttribute("placeholder")])
    .filter(Boolean)
    .join(" ");
  return `${document.body.textContent ?? ""} ${attributes}`;
}

function offendingRun() {
  return visibleText().match(/\p{Script=Han}+/u)?.[0];
}

describe("AccountList in a language that is not Chinese", () => {
  beforeEach(() => {
    apiMock.mockReset();
  });

  it("writes no Chinese of its own into a saved trip", async () => {
    stub({ "GET /trips": () => [trip], "GET /usage": () => usage });
    render(<AccountList kind="trips" />);
    await screen.findByText(trip.name);

    // The date range shares its element with the destination, so read the text.
    expect(visibleText()).toContain("[trips.list.dateRange]");
    // A trip deletes through TripActions, whose labels come from
    // lib/frontend-navigation rather than the catalog; the confirmation does not.
    fireEvent.click(screen.getByLabelText("More options: Kyoto in five days"));
    fireEvent.click(screen.getByRole("button", { name: "Delete trip" }));
    expect(screen.getByText("[trips.list.deleteConfirm]")).toBeTruthy();
    expect(offendingRun(), "hardcoded copy on the trips list").toBeUndefined();
  });

  it("writes no Chinese of its own into the empty trips list", async () => {
    stub({ "GET /trips": () => [], "GET /usage": () => usage });
    render(<AccountList kind="trips" />);

    await screen.findByText("[trips.list.empty]");
    expect(screen.getByText("[trips.list.emptyAction]")).toBeTruthy();
    expect(offendingRun(), "hardcoded copy on the empty state").toBeUndefined();
  });

  it("writes no Chinese of its own into a price alert, its editor or its delete prompt", async () => {
    stub({ "GET /alerts": () => [alert], "GET /usage": () => usage });
    render(<AccountList kind="alerts" />);
    await screen.findByText(alert.title);

    // The badges, the target line and the quoted time all used to be literals.
    // The target and current price share one sentence, so these are read as text.
    for (const key of ["active", "modeManual", "targetBelow", "currentPrice", "quotedAt", "targetGap"]) {
      expect(visibleText(), key).toContain(`[alerts.list.${key}]`);
    }
    fireEvent.click(screen.getByLabelText("[alerts.list.edit]"));
    expect(screen.getByLabelText("[alerts.list.targetInput]")).toBeTruthy();
    fireEvent.click(screen.getByLabelText("[alerts.list.deleteAction]"));
    // The one that matters most: an irreversible delete, confirmed in a language
    // the reader does not have to guess at.
    expect(screen.getByText("[alerts.list.deleteConfirm]")).toBeTruthy();
    expect(offendingRun(), "hardcoded copy on the alerts list").toBeUndefined();
  });

  it("writes no Chinese of its own when the list cannot be loaded", async () => {
    const { ApiError } = await vi.importActual<typeof import("@/lib/api")>("@/lib/api");
    stub({
      "GET /trips": () => {
        throw new ApiError("upstream unavailable", 403);
      },
      "GET /usage": () => usage,
    });
    render(<AccountList kind="trips" />);

    await screen.findByText("[common.accountList.forbidden]");
    expect(screen.getByText("[common.accountList.reload]")).toBeTruthy();
    expect(offendingRun(), "hardcoded copy on the error state").toBeUndefined();
  });

  it("reports a failed delete without a Chinese sentence around the reason", async () => {
    const { ApiError } = await vi.importActual<typeof import("@/lib/api")>("@/lib/api");
    stub({
      "GET /alerts": () => [alert],
      "GET /usage": () => usage,
      "DELETE /alerts/alert-1": () => {
        throw new ApiError("upstream unavailable", 503);
      },
    });
    render(<AccountList kind="alerts" />);
    await screen.findByText(alert.title);
    fireEvent.click(screen.getByLabelText("[alerts.list.deleteAction]"));
    fireEvent.click(screen.getByText("[common.accountList.deleteConfirmYes]"));

    await waitFor(() => expect(screen.getByText("[common.accountList.actionFailed]")).toBeTruthy());
    expect(offendingRun(), "hardcoded copy around a failure reason").toBeUndefined();
  });
});

/** Keeps the regex above honest: it must actually find Han when Han is present. */
it("the Han detector recognises Chinese", () => {
  expect(HAN.test("刪除")).toBe(true);
  expect(HAN.test("Delete")).toBe(false);
});
