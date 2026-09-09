import "@testing-library/jest-dom/vitest";
import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { Stay22PublicHotels } from "./stay22-public-hotels";

const hotel = { id: "hotel-public", title: "Tokyo reviewed hotel", destination_id: "tokyo" };
const options = [
  { id: "booking", provider: "booking", name: "Booking.com", url: "https://www.booking.com/hotel/jp/reviewed.html" },
  { id: "official", provider: "official", name: "Official website", url: "https://hotel.example/" },
];
describe("public hotel script directory", () => {
  beforeEach(() => vi.stubGlobal("fetch", vi.fn().mockImplementation((url: string) => Promise.resolve(new Response(JSON.stringify(url.includes("stay22-script-options") ? { options } : { enabled: true, items: [hotel] }))))));
  afterEach(() => { vi.unstubAllGlobals(); });
  it("loads options only when opened and renders original external anchors without private controls", async () => {
    render(<Stay22PublicHotels destinationId="tokyo" locale="zh-TW" />);
    expect(await screen.findByRole("heading", { name: hotel.title })).toBeTruthy();
    expect(fetch).toHaveBeenCalledTimes(1);
    const opener = screen.getByRole("button", { name: "查看預訂平台" });
    opener.focus(); fireEvent.click(opener);
    const link = await screen.findByRole("link", { name: /前往 Booking.com/ });
    expect(link).toHaveAttribute("href", options[0].url);
    expect(link).toHaveAttribute("rel", "sponsored noopener noreferrer");
    expect(screen.getByRole("link", { name: /前往 飯店官網/ })).toHaveAttribute("href", options[1].url);
    expect(document.querySelectorAll("form,input,iframe")).toHaveLength(0);
    for (const [, init] of vi.mocked(fetch).mock.calls) expect(init).toMatchObject({ credentials: "omit", cache: "no-store" });
    fireEvent.keyDown(document, { key: "Escape" });
    expect(screen.queryByRole("dialog")).toBeNull();
    expect(opener).toHaveFocus();
  });
  it("keeps the page and supports retry after a settings change or unavailable endpoint", async () => {
    vi.mocked(fetch).mockResolvedValueOnce(new Response(JSON.stringify({ enabled: true, items: [hotel] })))
      .mockResolvedValueOnce(new Response("not enabled", { status: 404 }))
      .mockResolvedValueOnce(new Response(JSON.stringify({ options })));
    render(<Stay22PublicHotels destinationId="tokyo" locale="zh-TW" />);
    fireEvent.click(await screen.findByRole("button", { name: "查看預訂平台" }));
    expect(await screen.findByRole("alert")).toHaveTextContent("暫時無法載入平台連結");
    fireEvent.click(screen.getByRole("button", { name: "重試" }));
    expect(await screen.findByRole("link", { name: /Booking.com/ })).toBeTruthy();
    expect(screen.getAllByText(hotel.title)).toHaveLength(2);
  });
  it("does not invent links for missing or unsafe targets", async () => {
    vi.mocked(fetch).mockResolvedValueOnce(new Response(JSON.stringify({ items: [hotel] })))
      .mockResolvedValueOnce(new Response(JSON.stringify({ options: [{ ...options[0], url: "javascript:alert(1)" }, { ...options[1], url: "https://www.stay22.com/allez/booking" }] })));
    render(<Stay22PublicHotels destinationId="tokyo" locale="zh-TW" />);
    fireEvent.click(await screen.findByRole("button", { name: "查看預訂平台" }));
    expect(await screen.findByText(/目前沒有審核有效的精確飯店連結/)).toBeTruthy();
    expect(screen.queryByRole("link")).toBeNull();
  });
  it("shows empty and transport-error states truthfully", async () => {
    vi.mocked(fetch).mockRejectedValueOnce(new Error("down")).mockResolvedValueOnce(new Response(JSON.stringify({ enabled: false, items: [] })));
    render(<Stay22PublicHotels destinationId="tokyo" locale="zh-TW" />);
    expect(await screen.findByRole("alert")).toHaveTextContent("暫時無法載入飯店");
    fireEvent.click(screen.getByRole("button", { name: "重試" }));
    await waitFor(() => expect(screen.getByText("這個目的地尚無可顯示的已審核飯店。")).toBeTruthy());
  });
});
