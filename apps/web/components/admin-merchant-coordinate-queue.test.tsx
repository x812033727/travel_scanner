import { render, screen, waitFor } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import { AdminMerchantCoordinateQueue } from "./admin-merchant-coordinate-queue";

/**
 * vitest.setup.tsx hands every component the zh-TW catalog, so a hardcoded Chinese string
 * and a translated one look identical in every other test. This file swaps the catalog for
 * one that echoes the key it was asked for and reads the panel as an English-speaking
 * operator: any Han character left on screen is copy the component wrote itself, which no
 * other language can reach. Same approach as account-list-i18n.test.tsx, and its own file
 * for the same reason — vi.mock is hoisted per file.
 */
vi.mock("next-intl", () => ({
  useLocale: () => "en",
  useFormatter: () => ({ number: (value: number) => String(value) }),
  useTranslations: (namespace: string) =>
    Object.assign((key: string) => `[${namespace}.${key}]`, { has: () => true }),
}));

const HAN = /\p{Script=Han}/u;

const queue = {
  configured: true,
  total: 1,
  page: 1,
  limit: 10,
  items: [
    {
      merchant: {
        id: "11111111-1111-4111-8111-111111111111",
        slug: "gwangjang-bindaetteok",
        name: "Gwangjang Bindaetteok",
        local_name: "광장 빈대떡",
        address: "88 Changgyeonggung-ro, Jongno-gu, Seoul",
        destination_id: "sel",
        country_code: "KR",
        latitude: null,
        longitude: null,
        map_match_status: "pending",
        review_status: "pending",
        needs_naver_url: true,
      },
      candidate: {
        place_id: "ChIJ-market",
        name: "Gwangjang Market",
        address: "88 Changgyeonggung-ro",
        google_maps_url: "https://maps.google.com/?cid=2",
        latitude: 37.5699,
        longitude: 126.9997,
      },
      signals: { verdict: "check" as const, name_score: 0.72, distance_km: 0.4, place_id_taken: true },
    },
  ],
};

describe("AdminMerchantCoordinateQueue in a language that is not Chinese", () => {
  it("writes none of its own Chinese across the header, the table and the pager", async () => {
    vi.stubGlobal("fetch", vi.fn(async () => new Response(JSON.stringify(queue))));
    render(<AdminMerchantCoordinateQueue />);

    await screen.findByText("[admin.merchantCoordinateQueue.title]");
    // The row renders: a verdict that needs a human, both signal numbers, the Korean
    // publishing note and the taken Place ID — the cells that used to be literals.
    expect(screen.getByText("[admin.merchantCoordinateQueue.verdictCheck]")).toBeTruthy();
    expect(screen.getByText("[admin.merchantCoordinateQueue.nameScore]")).toBeTruthy();
    expect(screen.getByText("[admin.merchantCoordinateQueue.distanceKm]")).toBeTruthy();
    expect(screen.getByText("[admin.merchantCoordinateQueue.koreaNote]")).toBeTruthy();
    expect(screen.getByText("[admin.merchantCoordinateQueue.placeIdTaken]")).toBeTruthy();
    expect(screen.getByText("[admin.merchantCoordinateQueue.openInGoogleMaps]")).toBeTruthy();

    // Every cell carries the column name for the phone layout, and it is the same
    // translated string the header uses — not a second copy of the words.
    const headers = screen.getAllByRole("columnheader").map((cell) => cell.textContent);
    const labels = [...document.querySelectorAll("tbody td")].map((cell) => cell.getAttribute("data-label"));
    expect(headers).toEqual(labels);

    await waitFor(() => expect(document.body.textContent?.match(HAN)).toBeNull());
  });
});
