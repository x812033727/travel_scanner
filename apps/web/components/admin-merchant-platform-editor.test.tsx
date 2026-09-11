import { useState } from "react";
import { act, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import { reservationPlatformDefinitions } from "@/lib/reservation-platforms";
import { AdminMerchantPlatformEditor, merchantPlatformLinks, type MerchantPlatformLink } from "./admin-merchant-platform-editor";

const link: MerchantPlatformLink = {
  provider: "tablecheck", provider_label: "TableCheck", status: "verified",
  canonical_url: "https://www.tablecheck.com/en/shops/sushi/reserve", localized_urls: {},
  review_note: "Owner compared official branch name and address", checked_at: "2026-09-10T01:00:00Z",
};
const other: MerchantPlatformLink = {
  provider: "inline", provider_label: "inline", status: "verified",
  canonical_url: "https://inline.app/booking/company:1/branch1", localized_urls: {},
  review_note: "Official branch evidence", checked_at: "2026-09-10T02:00:00Z",
};
const onBusyChange = vi.fn();
const onDirtyChange = vi.fn();

function Editor({ merchantId = "merchant-1" }: { merchantId?: string }) {
  const [links, setLinks] = useState([link, other]);
  return <AdminMerchantPlatformEditor merchantId={merchantId} links={links} availablePlatforms={reservationPlatformDefinitions}
    onSaved={(saved) => setLinks(merchantPlatformLinks(saved))} onBusyChange={onBusyChange} onDirtyChange={onDirtyChange} />;
}

function input(label: string) { return screen.getByLabelText(label) as HTMLInputElement; }
function selectProvider(value: string) { fireEvent.change(screen.getByLabelText("訂位平台"), { target: { value } }); }

describe("AdminMerchantPlatformEditor", () => {
  it("keeps separate drafts across providers and saves only the selected provider", async () => {
    const fetchMock = vi.fn(async (_input: RequestInfo | URL, init?: RequestInit) => {
      const body = JSON.parse(String(init?.body));
      return new Response(JSON.stringify({ platform_links: [link, { ...other, ...body, checked_at: "2026-09-11T01:00:00Z" }], platform_link: link }));
    });
    vi.stubGlobal("fetch", fetchMock);
    render(<Editor />);
    fireEvent.change(input("查核備註"), { target: { value: "TableCheck unsaved evidence" } });
    selectProvider("inline");
    fireEvent.change(screen.getByLabelText("查核結果"), { target: { value: "disabled" } });
    selectProvider("tablecheck");
    expect(input("查核備註").value).toBe("TableCheck unsaved evidence");
    selectProvider("inline");
    expect((screen.getByLabelText("查核結果") as HTMLSelectElement).value).toBe("disabled");
    fireEvent.click(screen.getByRole("button", { name: "只儲存訂位平台" }));
    await screen.findByText("已儲存 inline 的訂位平台資料。");
    expect(fetchMock).toHaveBeenCalledTimes(1);
    expect(fetchMock.mock.calls[0][0]).toBe("/api/travel/admin/foods/merchants/merchant-1/platform-link");
    expect(fetchMock.mock.calls[0][1]?.method).toBe("PUT");
    expect(JSON.parse(String(fetchMock.mock.calls[0][1]?.body))).toEqual({
      provider: "inline", status: "disabled", canonical_url: other.canonical_url,
      localized_urls: {}, review_note: other.review_note, expected_checked_at: other.checked_at,
    });
    selectProvider("tablecheck");
    expect(input("查核備註").value).toBe("TableCheck unsaved evidence");
    expect((screen.getByLabelText("查核結果") as HTMLSelectElement).value).toBe("verified");
    expect(screen.getByText(/尚未儲存的平台草稿：TableCheck/)).toBeTruthy();
  });

  it("saves all five owner-checked language URLs and a null token for a new provider", async () => {
    const fetchMock = vi.fn(async (_input: RequestInfo | URL, init?: RequestInit) => {
      const body = JSON.parse(String(init?.body));
      return new Response(JSON.stringify({ platform_links: [link, other, { ...body, provider_label: "一休" }], platform_link: link }));
    });
    vi.stubGlobal("fetch", fetchMock);
    render(<Editor />);
    selectProvider("ikyu");
    fireEvent.change(input("精準分店網址"), { target: { value: "https://restaurant.ikyu.com/123456" } });
    fireEvent.change(input("查核備註"), { target: { value: "Owner checked official name, address, and every language page" } });
    const localized_urls = Object.fromEntries(["zh-TW", "zh-CN", "en", "ja", "ko"].map((locale) => [locale, "https://restaurant.ikyu.com/123456"]));
    for (const [locale, url] of Object.entries(localized_urls)) fireEvent.change(input(`${locale} 網址（選填）`), { target: { value: url } });
    fireEvent.change(screen.getByLabelText("查核結果"), { target: { value: "verified" } });
    fireEvent.click(screen.getByRole("button", { name: "只儲存訂位平台" }));
    await screen.findByText("已儲存 一休 的訂位平台資料。");
    expect(JSON.parse(String(fetchMock.mock.calls[0][1]?.body))).toMatchObject({ provider: "ikyu", status: "verified", localized_urls, expected_checked_at: null });
  });

  it("retains the draft on an error and retries without a second request while saving", async () => {
    let complete: (response: Response) => void = () => undefined;
    const fetchMock = vi.fn<(input: RequestInfo | URL, init?: RequestInit) => Promise<Response>>(() => new Promise<Response>((resolve) => { complete = resolve; }));
    vi.stubGlobal("fetch", fetchMock);
    render(<Editor />);
    fireEvent.change(input("查核備註"), { target: { value: "Keep this evidence" } });
    const save = screen.getByRole("button", { name: "只儲存訂位平台" });
    save.focus();
    fireEvent.click(save);
    fireEvent.click(save);
    expect(fetchMock).toHaveBeenCalledTimes(1);
    expect((input("查核備註").closest("fieldset") as HTMLFieldSetElement).disabled).toBe(true);
    await act(async () => complete(new Response(JSON.stringify({ detail: "Temporary service error" }), { status: 503 })));
    expect(await screen.findByRole("alert")).toHaveProperty("textContent", "Temporary service error");
    expect(input("查核備註").value).toBe("Keep this evidence");
    expect(document.activeElement).toBe(save);
    fireEvent.click(screen.getByRole("button", { name: "只儲存訂位平台" }));
    expect(fetchMock).toHaveBeenCalledTimes(2);
    await act(async () => complete(new Response(JSON.stringify({ platform_links: [{ ...link, review_note: "Keep this evidence" }, other], platform_link: link }))));
    await screen.findByText("已儲存 TableCheck 的訂位平台資料。");
    expect(document.activeElement).toBe(save);
  });

  it("requires explicit comparison after a 409, retaining the draft and using the refreshed token", async () => {
    let puts = 0;
    const latest = { ...link, canonical_url: "https://www.tablecheck.com/en/shops/latest/reserve", review_note: "Other owner evidence", checked_at: "2026-09-11T09:00:00Z" };
    const fetchMock = vi.fn(async (_input: RequestInfo | URL, init?: RequestInit) => {
      if (init?.method === "PUT" && ++puts === 1) return new Response(JSON.stringify({ detail: "Changed", code: "reservation_platform_version_conflict" }), { status: 409 });
      if (init?.method === "PUT") return new Response(JSON.stringify({ platform_links: [{ ...latest, review_note: "My checked evidence", canonical_url: link.canonical_url }, other], platform_link: latest }));
      return new Response(JSON.stringify({ platform_links: [latest, other], platform_link: latest }));
    });
    vi.stubGlobal("fetch", fetchMock);
    render(<Editor />);
    fireEvent.change(input("查核備註"), { target: { value: "My checked evidence" } });
    fireEvent.click(screen.getByRole("button", { name: "只儲存訂位平台" }));
    await screen.findByText(/此平台資料已由其他人更新/);
    expect(input("查核備註").value).toBe("My checked evidence");
    fireEvent.click(screen.getByRole("button", { name: "重新載入平台狀態並保留草稿" }));
    await screen.findByText("Other owner evidence");
    expect(input("精準分店網址").value).toBe(link.canonical_url);
    expect((screen.getByRole("button", { name: "只儲存訂位平台" }) as HTMLButtonElement).disabled).toBe(true);
    expect(fetchMock.mock.calls[1][0]).toBe("/api/travel/admin/foods/merchants/merchant-1/platform-links");
    const confirmRetry = screen.getByRole("button", { name: "我已核對最新資料，使用我的草稿" });
    confirmRetry.focus();
    fireEvent.click(confirmRetry);
    expect(document.activeElement).toBe(screen.getByRole("button", { name: "只儲存訂位平台" }));
    fireEvent.click(screen.getByRole("button", { name: "只儲存訂位平台" }));
    await screen.findByText("已儲存 TableCheck 的訂位平台資料。");
    expect(JSON.parse(String(fetchMock.mock.calls[2][1]?.body))).toMatchObject({ expected_checked_at: latest.checked_at, canonical_url: link.canonical_url, review_note: "My checked evidence" });
  });

  it("gates new merchants and rejects unsafe previews or mismatched language branches", async () => {
    const { unmount } = render(<Editor merchantId="" />);
    expect(screen.getByText("請先儲存新店家資料，再新增與查核訂位平台。")).toBeTruthy();
    expect((input("精準分店網址").closest("fieldset") as HTMLFieldSetElement).disabled).toBe(true);
    unmount();
    render(<Editor />);
    fireEvent.change(input("精準分店網址"), { target: { value: "https://tablecheck.com.evil.test/en/shops/sushi/reserve" } });
    expect(screen.queryByRole("link", { name: "開啟核對" })).toBeNull();
    expect((screen.getByRole("button", { name: "只儲存訂位平台" }) as HTMLButtonElement).disabled).toBe(true);
    fireEvent.change(input("精準分店網址"), { target: { value: link.canonical_url } });
    fireEvent.change(input("ja 網址（選填）"), { target: { value: "https://www.tablecheck.com/ja/shops/another/reserve" } });
    expect((screen.getByRole("button", { name: "只儲存訂位平台" }) as HTMLButtonElement).disabled).toBe(true);
    fireEvent.change(input("ja 網址（選填）"), { target: { value: "https://www.tablecheck.com/ja/shops/sushi/reserve" } });
    expect((screen.getByRole("button", { name: "只儲存訂位平台" }) as HTMLButtonElement).disabled).toBe(false);
    await waitFor(() => expect(onDirtyChange).toHaveBeenCalledWith(true));
  });

  it("shows branch ownership conflicts without offering a stale-version retry", async () => {
    vi.stubGlobal("fetch", vi.fn(async () => new Response(JSON.stringify({ code: "reservation_platform_url_conflict", detail: "This branch belongs to another merchant" }), { status: 409 })));
    render(<Editor />);
    fireEvent.change(input("查核備註"), { target: { value: "My branch evidence" } });
    fireEvent.click(screen.getByRole("button", { name: "只儲存訂位平台" }));
    expect(await screen.findByRole("alert")).toHaveProperty("textContent", "This branch belongs to another merchant");
    expect(screen.queryByRole("button", { name: "重新載入平台狀態並保留草稿" })).toBeNull();
    expect(input("查核備註").value).toBe("My branch evidence");
  });

  it("keeps booking-platform message keys in all five admin catalogs", async () => {
    const catalogs = await Promise.all([
      import("@/messages/zh-TW/admin.json"), import("@/messages/zh-CN/admin.json"),
      import("@/messages/en/admin.json"), import("@/messages/ja/admin.json"), import("@/messages/ko/admin.json"),
    ]);
    const keys = (catalog: typeof catalogs[number]) => Object.keys(catalog.default.foodMerchantsPanel).filter((key) => key.startsWith("platform")).sort();
    for (const catalog of catalogs) {
      expect(keys(catalog)).toEqual(keys(catalogs[0]));
      expect(catalog.default.foodMerchantsPanel.platformSaveOnly.trim()).not.toBe("");
      expect(catalog.default.foodMerchantsPanel.platformStale.trim()).not.toBe("");
    }
  });
});
