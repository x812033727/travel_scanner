import { act, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { Stay22MapPanel } from "./stay22-map-panel";
import type { Stay22MapContext } from "@/lib/stay22";

const context: Stay22MapContext = { destination_id: "tokyo", country_code: "JP", city_code: "NRT", check_in: "2099-11-10", check_out: "2099-11-15", travelers: { adults: 2, children: 1, rooms: 1 } };
const area = { name: "Asakusa", latitude: 35.71, longitude: 139.79 };
const load = "同意並載入 Stay22 地圖";
afterEach(() => { vi.useRealTimers(); vi.unstubAllGlobals(); });

describe("Stay22 map panel", () => {
  it("does not load any frame until consent; safely unloads and returns focus", async () => {
    const onManual = vi.fn();
    render(<Stay22MapPanel context={context} area={area} onManualLodging={onManual} />);
    expect(document.querySelector("iframe, script[src*='stay22'], link[rel='preconnect']")).toBeNull();
    expect(screen.getByText(/2 位成人 · 1 位兒童 · 1 間房/)).toBeTruthy();
    expect(screen.getByText(/不會傳送兒童年齡/)).toBeTruthy();
    fireEvent.click(screen.getByRole("button", { name: load }));
    const frame = document.querySelector("iframe")!;
    expect(frame.src).toContain("aid=mokaair");
    expect(frame.getAttribute("referrerpolicy")).toBe("no-referrer");
    expect(frame.getAttribute("sandbox")).not.toContain("allow-top-navigation");
    expect(frame.getAttribute("title")).toContain("Asakusa");
    expect(onManual).not.toHaveBeenCalled();
    fireEvent.load(frame);
    expect(screen.queryByText("正在載入外部地圖…")).toBeNull();
    fireEvent.click(screen.getByRole("button", { name: "關閉地圖" }));
    expect(document.querySelector("iframe")).toBeNull();
    await waitFor(() => expect(document.activeElement).toBe(screen.getByRole("button", { name: load })));
  });
  it("leaves a safe external fallback and manual selection with no automatic writes", () => {
    const onManual = vi.fn();
    render(<Stay22MapPanel context={context} area={area} onManualLodging={onManual} />);
    const link = screen.getByRole("link", { name: "在新分頁開啟 Stay22 地圖" });
    expect(link.getAttribute("target")).toBe("_blank");
    expect(link.getAttribute("rel")).toBe("noopener noreferrer sponsored");
    expect(link.getAttribute("referrerpolicy")).toBe("no-referrer");
    fireEvent.click(screen.getByRole("button", { name: load }));
    fireEvent.error(document.querySelector("iframe")!);
    expect(screen.getByRole("status").textContent).toContain("阻擋");
    fireEvent.click(screen.getByRole("button", { name: "找到飯店了？手動加入" }));
    expect(onManual).toHaveBeenCalledTimes(1);
  });
  it("shows timeout guidance and never automatically retries", () => {
    vi.useFakeTimers();
    render(<Stay22MapPanel context={context} area={area} onManualLodging={vi.fn()} />);
    fireEvent.click(screen.getByRole("button", { name: load }));
    const frame = document.querySelector("iframe");
    act(() => vi.advanceTimersByTime(12_001));
    expect(screen.getByRole("status").textContent).toContain("阻擋");
    expect(document.querySelector("iframe")).toBe(frame);
    fireEvent.click(screen.getByRole("button", { name: "重新載入地圖" }));
    expect(document.querySelector("iframe")).not.toBe(frame);
  });
  it("requires new consent when destination, dates or party changes", () => {
    const { rerender } = render(<Stay22MapPanel context={context} area={area} onManualLodging={vi.fn()} />);
    fireEvent.click(screen.getByRole("button", { name: load }));
    rerender(<Stay22MapPanel context={{ ...context, check_out: "2099-11-18" }} area={area} onManualLodging={vi.fn()} />);
    expect(document.querySelector("iframe")).toBeNull();
    expect(screen.getByRole("button", { name: load })).toBeTruthy();
  });
  it("discloses omitted dates and missing party instead of inventing them", () => {
    render(<Stay22MapPanel context={{ ...context, check_in: null, travelers: null }} area={area} onManualLodging={vi.fn()} />);
    expect(screen.getByText(/不會傳送日期/)).toBeTruthy();
    expect(screen.getByText(/不會傳送人數/)).toBeTruthy();
    fireEvent.click(screen.getByRole("button", { name: load }));
    const url = new URL(document.querySelector("iframe")!.src);
    expect(url.searchParams.has("adults")).toBe(false);
    expect(url.searchParams.has("checkin")).toBe(false);
  });
  it.each([{ doNotTrack: "1" }, { globalPrivacyControl: true }])("respects browser tracking preferences %j", (privacy) => {
    vi.stubGlobal("navigator", { ...privacy });
    render(<Stay22MapPanel context={context} area={area} onManualLodging={vi.fn()} />);
    expect(screen.queryByRole("button", { name: load })).toBeNull();
    expect(screen.queryByRole("link", { name: "在新分頁開啟 Stay22 地圖" })).toBeNull();
    expect(document.querySelector("iframe")).toBeNull();
    expect(screen.getByRole("status").textContent).toContain("Do Not Track");
  });
  it("does not expose the map for legacy responses or nonpilot cities", () => {
    const { rerender, container } = render(<Stay22MapPanel area={area} onManualLodging={vi.fn()} />);
    expect(container.innerHTML).toBe("");
    rerender(<Stay22MapPanel context={{ ...context, destination_id: "seoul", country_code: "KR" }} area={area} onManualLodging={vi.fn()} />);
    expect(container.innerHTML).toBe("");
  });
});
