import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { SavedItemsProvider } from "./saved-items-provider";
import { AccountSavedItems } from "./account-saved-items";

const apiMock = vi.fn();
vi.mock("@/lib/api", async () => {
  const actual = await vi.importActual<typeof import("@/lib/api")>("@/lib/api");
  return { ...actual, api: (...args: unknown[]) => apiMock(...args) };
});

const items = [
  {
    type: "hotspot",
    id: "hotspot-1",
    title: "香港海洋公園",
    subtitle: "香港 · 親子",
    map_links: [{ label: "Google Maps", url: "https://maps.example/hotspot" }],
  },
  {
    type: "food",
    id: "food-1",
    title: "港式奶茶",
    subtitle: "絲襪奶茶",
    map_links: [],
  },
  {
    type: "restaurant",
    id: "place-1",
    title: "茶餐廳",
    subtitle: "Google Maps 地點",
    map_links: [
      { label: "Google Maps", url: "https://maps.example/restaurant" },
    ],
  },
  {
    type: "merchant",
    id: "merchant-1",
    title: "Hankook Jib",
    subtitle: "首爾 · 明洞",
    map_links: [{ label: "Naver Map", url: "https://map.naver.com/p/entry/place/1" }],
  },
];

describe("AccountSavedItems", () => {
  beforeEach(() => {
    apiMock.mockReset();
    apiMock.mockImplementation((_path: string, init?: RequestInit) =>
      init?.method === "DELETE"
        ? Promise.resolve(undefined)
        : Promise.resolve({ items }),
    );
  });

  it("filters saved categories and removes an item from the account", async () => {
    render(
      <SavedItemsProvider>
        <AccountSavedItems />
      </SavedItemsProvider>,
    );
    await screen.findByText("香港海洋公園");
    fireEvent.click(screen.getByRole("tab", { name: /美食/ }));
    expect(screen.getByText("港式奶茶")).toBeTruthy();
    expect(screen.queryByText("香港海洋公園")).toBeNull();

    fireEvent.click(screen.getByRole("tab", { name: /全部/ }));
    fireEvent.click(
      screen.getByRole("button", { name: "移除收藏：香港海洋公園" }),
    );
    await waitFor(() =>
      expect(apiMock).toHaveBeenCalledWith("/saved-items/hotspot/hotspot-1", {
        method: "DELETE",
      }),
    );
    expect(screen.queryByText("香港海洋公園")).toBeNull();
  });

  it("lists saved merchants under their own tab", async () => {
    render(
      <SavedItemsProvider>
        <AccountSavedItems />
      </SavedItemsProvider>,
    );
    await screen.findByText("Hankook Jib");
    fireEvent.click(screen.getByRole("tab", { name: /店家/ }));
    expect(screen.getByText("Hankook Jib")).toBeTruthy();
    expect(screen.queryByText("港式奶茶")).toBeNull();
    expect(screen.queryByText("香港海洋公園")).toBeNull();
  });
});
