import { act, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { useState, type ComponentProps } from "react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { createPlaceBrowserState, ItineraryPlaceBrowser, type PlaceOption } from "./itinerary-place-browser";

const option: PlaceOption = {
  key: "hotspot:a", id: "a", kind: "hotspot", title: "淺草寺", subtitle: "東京",
  is_saved: true, distance_km: 0.42,
  item: { item_type: "activity", title: "淺草寺", latitude: 35.71, longitude: 139.79,
    provider_place_id: "asakusa", duration_minutes: 90, locked: false, is_estimated: false, data: { catalog_selection: { kind: "hotspot", id: "a" } } },
};
function setup(empty = false) {
  const fetchMock = vi.fn(async (url: RequestInfo | URL, init?: RequestInit) => ({ ok: String(url).includes("/place-options?") && !init?.signal?.aborted, json: async () => ({ items: empty ? [] : [option], next_offset: null as number | null, context: "nearby" }) }));
  vi.stubGlobal("fetch", fetchMock);
  const onAdd = vi.fn(() => true), onManual = vi.fn(), onUndo = vi.fn();
  const props: ComponentProps<typeof ItineraryPlaceBrowser> = {
    tripId: "trip", reference: { latitude: 35.7, longitude: 139.8 },
    following: { latitude: 35.72, longitude: 139.82 }, countryCodes: ["jp"], items: [],
    onAdd, onManual, onUndo, canUndo: true,
  };
  const view = render(<ItineraryPlaceBrowser {...props} />);
  return { fetchMock, onAdd, onManual, onUndo, props, ...view };
}

function deferred<T>() {
  let resolve!: (value: T) => void;
  let reject!: (reason?: unknown) => void;
  const promise = new Promise<T>((resolvePromise, rejectPromise) => {
    resolve = resolvePromise; reject = rejectPromise;
  });
  return { promise, resolve, reject };
}
afterEach(() => { vi.unstubAllGlobals(); });

describe("contextual place browser", () => {
  it("loads saved and nearby catalog options, never paid place search on open", async () => {
    const { fetchMock, onAdd, onUndo } = setup();
    fireEvent.click(await screen.findByRole("button", { name: "選擇 淺草寺" }));
    expect(onAdd).toHaveBeenCalledWith(option.item);
    expect(screen.getByRole("tab", { name: "我的收藏" })).toBeTruthy();
    expect(screen.getByText("已選擇「淺草寺」，確認加入後才會更新行程。")).toBeTruthy();
    expect(screen.queryByText("已加入 淺草寺")).toBeNull();
    expect(fetchMock.mock.calls.every(([url]) => String(url).includes("/place-options?"))).toBe(true);
    fireEvent.click(screen.getByRole("button", { name: "復原" }));
    expect(onUndo).toHaveBeenCalledOnce();
  });
  it("switches sources with the keyboard and keeps query and radius scoped to the current context", async () => {
    const { fetchMock } = setup(true);
    await screen.findByText("附近暫時沒有符合的地點。");
    fireEvent.keyDown(screen.getByRole("tab", { name: "為你挑選" }), { key: "ArrowRight" });
    await waitFor(() => expect(fetchMock.mock.calls.some(([url]) => String(url).includes("source=favorites"))).toBe(true));
    expect(document.activeElement).toBe(screen.getByRole("tab", { name: "我的收藏" }));
    fireEvent.click(screen.getByRole("checkbox", { name: "也顯示其他城市的收藏" }));
    await waitFor(() => expect(fetchMock.mock.calls.some(([url]) => String(url).includes("all_cities=true"))).toBe(true));
    expect(fetchMock.mock.calls.some(([url]) => String(url).includes("next_latitude=35.72"))).toBe(true);
  });
  it.each([
    { field: "reference", parameter: "latitude", latitude: 35.71 },
    { field: "following", parameter: "next_latitude", latitude: 35.73 },
  ] as const)("resets pagination immediately when $field changes without losing add feedback or focus", async ({ field, parameter, latitude }) => {
    const { fetchMock, props, rerender, onAdd } = setup();
    fetchMock.mockImplementation(async () => ({ ok: true, json: async () => ({ items: [option], next_offset: 12, context: "nearby" }) }));
    await screen.findByRole("button", { name: "選擇 淺草寺" });
    fireEvent.click(screen.getByRole("button", { name: "下一頁" }));
    await waitFor(() => expect(fetchMock.mock.calls.some(([url]) => new URL(String(url), "http://test").searchParams.get("offset") === "12")).toBe(true));
    await waitFor(() => expect((screen.getByRole("button", { name: "上一頁" }) as HTMLButtonElement).disabled).toBe(false));
    const add = screen.getByRole("button", { name: "選擇 淺草寺" });
    add.focus(); fireEvent.click(add);
    expect(onAdd).toHaveBeenCalledOnce();
    rerender(<ItineraryPlaceBrowser {...props} {...{ [field]: { latitude, longitude: 139.8 } }} />);
    expect(add.getAttribute("aria-disabled")).toBe("true");
    fireEvent.click(add);
    expect(onAdd).toHaveBeenCalledOnce();
    await waitFor(() => expect(fetchMock.mock.calls.some(([url]) => new URL(String(url), "http://test").searchParams.get(parameter) === String(latitude))).toBe(true));
    await waitFor(() => expect((screen.getByRole("button", { name: "上一頁" }) as HTMLButtonElement).disabled).toBe(true));
    const changedRequests = fetchMock.mock.calls.map(([url]) => new URL(String(url), "http://test").searchParams)
      .filter((params) => params.get(parameter) === String(latitude));
    expect(changedRequests.every((params) => params.get("offset") === "0")).toBe(true);
    expect(screen.getByText("已選擇「淺草寺」，確認加入後才會更新行程。")).toBeTruthy();
    expect(document.activeElement).toBe(add);
    // Returning to the original reference must not resurrect its old second page.
    rerender(<ItineraryPlaceBrowser {...props} />);
    await waitFor(() => expect(fetchMock.mock.calls.at(-1)?.[0]).toContain(`${parameter}=${props[field]?.latitude}`));
    expect(new URL(String(fetchMock.mock.calls.at(-1)?.[0]), "http://test").searchParams.get("offset")).toBe("0");
  });
  it.each(["resolve", "reject"] as const)("aborts an obsolete second-page request and ignores its late %s", async (completion) => {
    const { fetchMock, props, rerender, unmount } = setup();
    type FetchResult = Awaited<ReturnType<typeof fetchMock>>;
    const obsolete = deferred<FetchResult>();
    const current = deferred<FetchResult>();
    const staleOption = { ...option, key: "hotspot:stale", title: "過期列表地點" };
    const currentOption = { ...option, key: "hotspot:current", title: "新位置地點" };
    fetchMock.mockImplementation(async (url) => {
      const params = new URL(String(url), "http://test").searchParams;
      if (params.get("latitude") === "35.71") return current.promise;
      if (params.get("offset") === "12") return obsolete.promise;
      return { ok: true, json: async () => ({ items: [option], next_offset: 12, context: "nearby" }) };
    });
    await screen.findByRole("button", { name: "選擇 淺草寺" });
    fireEvent.click(screen.getByRole("button", { name: "下一頁" }));
    await waitFor(() => expect(fetchMock.mock.calls.some(([url]) => String(url).includes("offset=12"))).toBe(true));
    const obsoleteSignal = fetchMock.mock.calls.find(([url]) => String(url).includes("offset=12"))?.[1]?.signal;
    expect(obsoleteSignal?.aborted).toBe(false);
    rerender(<ItineraryPlaceBrowser {...props} reference={{ latitude: 35.71, longitude: 139.8 }} />);
    await waitFor(() => expect(fetchMock.mock.calls.some(([url]) => String(url).includes("latitude=35.71"))).toBe(true));
    expect(obsoleteSignal?.aborted).toBe(true);
    const latest = fetchMock.mock.calls.at(-1)!;
    expect(new URL(String(latest[0]), "http://test").searchParams.get("offset")).toBe("0");
    await act(async () => {
      current.resolve({ ok: true, json: async () => ({ items: [currentOption], next_offset: null, context: "nearby" }) });
    });
    await screen.findByRole("button", { name: "選擇 新位置地點" });
    // An adapter may resolve after abort; neither that result nor AbortError may
    // replace the current results or turn a normal context change into an error.
    await act(async () => {
      if (completion === "resolve") obsolete.resolve({ ok: true, json: async () => ({ items: [staleOption], next_offset: null, context: "nearby" }) });
      else obsolete.reject(new DOMException("Aborted", "AbortError"));
    });
    expect(screen.queryByRole("button", { name: "選擇 過期列表地點" })).toBeNull();
    expect(screen.getByRole("button", { name: "選擇 新位置地點" })).toBeTruthy();
    expect(screen.queryByRole("alert")).toBeNull();
    unmount();
    expect(latest[1]?.signal?.aborted).toBe(true);
  });
  it("keeps manual entry available when offline", async () => {
    const { fetchMock, onManual } = setup();
    fetchMock.mockRejectedValue(new TypeError("offline"));
    Object.defineProperty(window.navigator, "onLine", { value: false, configurable: true });
    expect((await screen.findByRole("alert")).textContent).toContain("目前離線");
    fireEvent.click(screen.getByRole("button", { name: "自行填寫行程" }));
    expect(onManual).toHaveBeenCalledOnce();
    Object.defineProperty(window.navigator, "onLine", { value: true, configurable: true });
  });

  it("keeps a single query across catalog, favorites, and map search, with manual entry before results", async () => {
    const { fetchMock, onManual } = setup();
    await screen.findByRole("button", { name: "選擇 淺草寺" });
    const manual = screen.getByRole("button", { name: "自行填寫行程" });
    expect(manual.closest(".itinerary-picker-actions-sticky")).toBeTruthy();
    expect(manual.compareDocumentPosition(screen.getByRole("tablist")) & Node.DOCUMENT_POSITION_FOLLOWING).toBeTruthy();
    fireEvent.change(screen.getByRole("textbox", { name: "搜尋地點" }), { target: { value: "咖啡" } });
    fireEvent.click(screen.getByRole("tab", { name: "我的收藏" }));
    expect((screen.getByRole("textbox", { name: "搜尋地點" }) as HTMLInputElement).value).toBe("咖啡");
    await waitFor(() => expect(fetchMock.mock.calls.some(([url]) => {
      const params = new URL(String(url), "http://test").searchParams;
      return params.get("source") === "favorites" && params.get("q") === "咖啡";
    })).toBe(true));
    fireEvent.click(screen.getByRole("tab", { name: "搜尋地圖" }));
    expect((screen.getByRole("combobox", { name: "搜尋地點" }) as HTMLInputElement).value).toBe("咖啡");
    expect(screen.queryByRole("textbox")).toBeNull();
    fireEvent.click(manual);
    expect(onManual).toHaveBeenCalledOnce();
    // Leave before the paid-search debounce; switching back never clears text.
    fireEvent.click(screen.getByRole("tab", { name: "為你挑選" }));
    expect((screen.getByRole("textbox", { name: "搜尋地點" }) as HTMLInputElement).value).toBe("咖啡");
    expect(fetchMock.mock.calls.every(([url]) => String(url).includes("/place-options?"))).toBe(true);
  });

  it("restores controlled source and query after returning from a manual draft", async () => {
    const { props, unmount } = setup();
    unmount();
    function Parent() {
      const [state, setState] = useState(createPlaceBrowserState());
      const [manual, setManual] = useState(false);
      return manual ? <button onClick={() => setManual(false)}>返回搜尋</button>
        : <ItineraryPlaceBrowser {...props} state={state} onStateChange={setState} onManual={() => setManual(true)} />;
    }
    render(<Parent />);
    fireEvent.change(screen.getByRole("textbox", { name: "搜尋地點" }), { target: { value: "茶" } });
    fireEvent.click(screen.getByRole("tab", { name: "我的收藏" }));
    fireEvent.click(screen.getByRole("checkbox", { name: "也顯示其他城市的收藏" }));
    fireEvent.click(screen.getByRole("button", { name: "自行填寫行程" }));
    fireEvent.click(screen.getByRole("button", { name: "返回搜尋" }));
    expect(screen.getByRole("tab", { name: "我的收藏" }).getAttribute("aria-selected")).toBe("true");
    expect((screen.getByRole("textbox", { name: "搜尋地點" }) as HTMLInputElement).value).toBe("茶");
    expect((screen.getByRole("checkbox", { name: "也顯示其他城市的收藏" }) as HTMLInputElement).checked).toBe(true);
    await screen.findByRole("button", { name: "選擇 淺草寺" });
  });
});
