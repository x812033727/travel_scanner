import { act, fireEvent, render, screen } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { PlacePicker } from "./place-picker";

describe("PlacePicker", () => {
  beforeEach(() => vi.useFakeTimers());
  afterEach(() => {
    vi.useRealTimers();
    vi.unstubAllGlobals();
  });

  it("uses Google region, nearby bias, and one session token through place selection", async () => {
    const onSelect = vi.fn();
    const fetchMock = vi.fn()
      .mockResolvedValueOnce(new Response(JSON.stringify([
        {
          provider: "google_places",
          place_id: "ChIJ-test",
          name: "淺草寺",
          address: "日本東京都台東區",
          distance_meters: 4210,
          attribution: "Google Maps",
        },
      ]), { status: 200 }))
      .mockResolvedValueOnce(new Response(JSON.stringify({
        provider: "google_places",
        place_id: "ChIJ-test",
        name: "淺草寺",
        address: "日本東京都台東區",
        latitude: 35.7148,
        longitude: 139.7967,
        attribution: "Google Maps",
      }), { status: 200 }));
    vi.stubGlobal("fetch", fetchMock);

    render(
      <PlacePicker
        value="淺草"
        confirmed={false}
        countryCodes={["jp"]}
        bias={{ latitude: 35.6812, longitude: 139.7671 }}
        onTextChange={() => undefined}
        onSelect={onSelect}
      />,
    );
    await act(async () => {
      await vi.advanceTimersByTimeAsync(320);
      await Promise.resolve();
    });
    expect(fetchMock).toHaveBeenCalledTimes(1);

    const autocompleteUrl = new URL(String(fetchMock.mock.calls[0][0]), "https://travel.test");
    expect(autocompleteUrl.searchParams.get("country_codes")).toBe("jp");
    expect(autocompleteUrl.searchParams.get("latitude")).toBe("35.6812");
    const sessionToken = autocompleteUrl.searchParams.get("session_token");
    expect(sessionToken).toBeTruthy();
    expect(screen.getByText(/約 4 公里/)).toBeTruthy();
    expect(screen.getByText("地點資料：Google Maps")).toBeTruthy();

    await act(async () => {
      fireEvent.click(screen.getByRole("option", { name: /淺草寺/ }));
      await Promise.resolve();
    });
    expect(fetchMock).toHaveBeenCalledTimes(2);
    const detailsUrl = new URL(String(fetchMock.mock.calls[1][0]), "https://travel.test");
    expect(detailsUrl.searchParams.get("session_token")).toBe(sessionToken);
    expect(onSelect).toHaveBeenCalledWith(expect.objectContaining({
      place_id: "ChIJ-test",
      latitude: 35.7148,
      attribution: "Google Maps",
    }));
  });

  it("exposes combobox semantics and supports keyboard selection", async () => {
    const onSelect = vi.fn();
    vi.stubGlobal("fetch", vi.fn()
      .mockResolvedValueOnce(new Response(JSON.stringify([
        { provider: "google_places", place_id: "one", name: "東京站" },
        { provider: "google_places", place_id: "two", name: "淺草站" },
      ]), { status: 200 }))
      .mockResolvedValueOnce(new Response(JSON.stringify({ provider: "google_places", place_id: "two", name: "淺草站" }), { status: 200 })));
    render(<PlacePicker inputId="destination" descriptionId="destination-help" value="東京" confirmed={false} onTextChange={() => undefined} onSelect={onSelect} />);
    await act(async () => {
      await vi.advanceTimersByTimeAsync(320);
      await Promise.resolve();
    });
    const input = screen.getByRole("combobox", { name: "目的地" });
    expect(input.getAttribute("aria-describedby")).toBe("destination-help");
    expect(input.getAttribute("aria-expanded")).toBe("true");
    await act(async () => {
      fireEvent.keyDown(input, { key: "ArrowDown" });
      fireEvent.keyDown(input, { key: "Enter" });
      await Promise.resolve();
    });
    expect(onSelect).toHaveBeenCalledWith(expect.objectContaining({ place_id: "two" }));
  });

  it("labels NAVER Korean results and preserves the provider on selection", async () => {
    const onSelect = vi.fn();
    const fetchMock = vi.fn()
      .mockResolvedValueOnce(new Response(JSON.stringify([{
        provider: "naver_local",
        place_id: "naver-opaque-place",
        name: "景福宮",
        address: "서울특별시 종로구 사직로 161",
        attribution: "NAVER",
      }]), { status: 200 }))
      .mockResolvedValueOnce(new Response(JSON.stringify({
        provider: "naver_local",
        place_id: "naver-opaque-place",
        name: "景福宮",
        address: "서울특별시 종로구 사직로 161",
        latitude: 37.5796,
        longitude: 126.977,
        naver_maps_url: "https://map.naver.com/p/search/%EA%B2%BD%EB%B3%B5%EA%B6%81",
        attribution: "NAVER",
      }), { status: 200 }));
    vi.stubGlobal("fetch", fetchMock);
    render(<PlacePicker value="景福宮" confirmed={false} countryCodes={["kr"]} onTextChange={() => undefined} onSelect={onSelect} />);

    await act(async () => {
      await vi.advanceTimersByTimeAsync(320);
      await Promise.resolve();
    });
    expect(screen.getByText("地點資料：NAVER")).toBeTruthy();
    expect(screen.getAllByText("NAVER").length).toBeGreaterThan(0);
    await act(async () => {
      fireEvent.click(screen.getByRole("option", { name: /景福宮/ }));
      await Promise.resolve();
    });
    expect(onSelect).toHaveBeenCalledWith(expect.objectContaining({
      provider: "naver_local",
      latitude: 37.5796,
    }));
    const autocompleteUrl = new URL(String(fetchMock.mock.calls[0][0]), "https://travel.test");
    expect(autocompleteUrl.searchParams.get("country_codes")).toBe("kr");
  });

  it("shows when the Google Maps service is not configured", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(new Response(JSON.stringify({
      code: "google_maps_not_configured",
      detail: "Google Maps 地點搜尋尚未啟用",
    }), { status: 503 })));
    render(
      <PlacePicker
        value="淺草"
        confirmed={false}
        onTextChange={() => undefined}
        onSelect={() => undefined}
      />,
    );
    await act(async () => {
      await vi.advanceTimersByTimeAsync(320);
      await Promise.resolve();
    });
    expect(screen.getByRole("alert").textContent).toContain("Google Maps 地點搜尋尚未啟用");
  });
  it("stays closed when the search finishes after the reader dismissed it", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(new Response(JSON.stringify([
      { provider: "google_places", place_id: "one", name: "東京站" },
    ]), { status: 200 })));
    render(<PlacePicker value="東京" confirmed={false} onTextChange={() => undefined} onSelect={() => undefined} />);

    fireEvent.keyDown(screen.getByRole("combobox", { name: "目的地" }), { key: "Escape" });
    await act(async () => {
      await vi.advanceTimersByTimeAsync(320);
      await Promise.resolve();
    });

    expect(screen.queryByRole("option")).toBeNull();
    expect(screen.getByRole("combobox", { name: "目的地" }).getAttribute("aria-expanded")).toBe("false");
  });

  it("closes when the reader presses somewhere else on the page", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(new Response(JSON.stringify([
      { provider: "google_places", place_id: "one", name: "東京站" },
    ]), { status: 200 })));
    render(<PlacePicker value="東京" confirmed={false} onTextChange={() => undefined} onSelect={() => undefined} />);
    await act(async () => {
      await vi.advanceTimersByTimeAsync(320);
      await Promise.resolve();
    });
    expect(screen.getByRole("option", { name: /東京站/ })).toBeTruthy();

    await act(async () => {
      fireEvent.pointerDown(document.body);
      await Promise.resolve();
    });
    expect(screen.queryByRole("option")).toBeNull();
  });

  it("consumes only the first Escape, leaving the containing editor open while dismissing suggestions", async () => {
    const parentEscape = vi.fn();
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(new Response(JSON.stringify([
      { provider: "google_places", place_id: "one", name: "東京站" },
    ]))));
    render(<div onKeyDown={(event) => { if (event.key === "Escape") parentEscape(); }}>
      <PlacePicker value="東京" confirmed={false} onTextChange={vi.fn()} onSelect={vi.fn()} />
    </div>);
    await act(async () => { await vi.advanceTimersByTimeAsync(320); });
    fireEvent.keyDown(screen.getByRole("combobox"), { key: "Escape" });
    expect(parentEscape).not.toHaveBeenCalled();
    expect(screen.queryByRole("listbox")).toBeNull();
    fireEvent.keyDown(screen.getByRole("combobox"), { key: "Escape" });
    expect(parentEscape).toHaveBeenCalledOnce();
  });

  it("restarts the same query when refocused after cancelling before debounce", async () => {
    const fetchMock = vi.fn().mockResolvedValue(new Response(JSON.stringify([
      { provider: "google_places", place_id: "one", name: "東京站" },
    ])));
    vi.stubGlobal("fetch", fetchMock);
    render(<PlacePicker value="東京" confirmed={false} onTextChange={vi.fn()} onSelect={vi.fn()} />);
    fireEvent.keyDown(screen.getByRole("combobox"), { key: "Escape" });
    await act(async () => { await vi.advanceTimersByTimeAsync(320); });
    expect(fetchMock).not.toHaveBeenCalled();
    fireEvent.focus(screen.getByRole("combobox"));
    await act(async () => { await vi.advanceTimersByTimeAsync(320); });
    expect(screen.getByRole("option", { name: /東京站/ })).toBeTruthy();
    expect(fetchMock).toHaveBeenCalledOnce();
  });

  it.each(["unmount", "owner", "query", "escape"] as const)("aborts details and ignores late success after %s", async (change) => {
    let complete!: (response: Response) => void;
    const onSelect = vi.fn();
    const fetchMock = vi.fn()
      .mockResolvedValueOnce(new Response(JSON.stringify([{ provider: "google_places", place_id: "one", name: "東京站" }])))
      .mockImplementationOnce(() => new Promise<Response>((resolve) => { complete = resolve; }));
    vi.stubGlobal("fetch", fetchMock);
    const props = { value: "東京", confirmed: false, selectionContextKey: "item-a", onTextChange: vi.fn(), onSelect };
    const view = render(<PlacePicker {...props} />);
    await act(async () => { await vi.advanceTimersByTimeAsync(320); });
    fireEvent.click(screen.getByRole("option", { name: /東京站/ }));
    const signal = fetchMock.mock.calls[1][1].signal as AbortSignal;
    expect(signal.aborted).toBe(false);
    if (change === "unmount") view.unmount();
    if (change === "owner") view.rerender(<PlacePicker {...props} selectionContextKey="item-b" />);
    if (change === "query") view.rerender(<PlacePicker {...props} value="大阪" />);
    if (change === "escape") fireEvent.keyDown(screen.getByRole("combobox"), { key: "Escape" });
    expect(signal.aborted).toBe(true);
    await act(async () => {
      complete(new Response(JSON.stringify({ provider: "google_places", place_id: "one", name: "東京站", latitude: 35.6, longitude: 139.7 })));
    });
    expect(onSelect).not.toHaveBeenCalled();
    expect(screen.queryByRole("alert")).toBeNull();
  });

  it("ignores an earlier detail response when the reader chooses another result", async () => {
    let first!: (response: Response) => void;
    const onSelect = vi.fn();
    const fetchMock = vi.fn()
      .mockResolvedValueOnce(new Response(JSON.stringify([
        { provider: "google_places", place_id: "one", name: "東京站" },
        { provider: "google_places", place_id: "two", name: "東京塔" },
      ])))
      .mockImplementationOnce(() => new Promise<Response>((resolve) => { first = resolve; }))
      .mockResolvedValueOnce(new Response(JSON.stringify({ provider: "google_places", place_id: "two", name: "東京塔" })));
    vi.stubGlobal("fetch", fetchMock);
    render(<PlacePicker value="東京" confirmed={false} onTextChange={vi.fn()} onSelect={onSelect} />);
    await act(async () => { await vi.advanceTimersByTimeAsync(320); });
    fireEvent.click(screen.getByRole("option", { name: /東京站/ }));
    await act(async () => { fireEvent.click(screen.getByRole("option", { name: /東京塔/ })); });
    await act(async () => { first(new Response(JSON.stringify({ provider: "google_places", place_id: "one", name: "東京站" }))); });
    expect(fetchMock.mock.calls[1][1].signal.aborted).toBe(true);
    expect(onSelect).toHaveBeenCalledOnce();
    expect(onSelect).toHaveBeenCalledWith(expect.objectContaining({ place_id: "two" }));
  });

  it("ignores late autocomplete and detail failures after their owner changes", async () => {
    let oldSearch!: (response: Response) => void;
    let failDetails!: (reason: Error) => void;
    const onSelect = vi.fn();
    const fetchMock = vi.fn()
      .mockImplementationOnce(() => new Promise<Response>((resolve) => { oldSearch = resolve; }))
      .mockResolvedValueOnce(new Response(JSON.stringify([{ provider: "google_places", place_id: "current", name: "大阪站" }])))
      .mockImplementationOnce(() => new Promise<Response>((_resolve, reject) => { failDetails = reject; }));
    vi.stubGlobal("fetch", fetchMock);
    const props = { value: "東京", confirmed: false, onTextChange: vi.fn(), onSelect };
    const view = render(<PlacePicker {...props} />);
    await act(async () => { await vi.advanceTimersByTimeAsync(320); });
    view.rerender(<PlacePicker {...props} value="大阪" />);
    expect(fetchMock.mock.calls[0][1].signal.aborted).toBe(true);
    await act(async () => {
      await vi.advanceTimersByTimeAsync(320);
      oldSearch(new Response(JSON.stringify([{ provider: "google_places", place_id: "old", name: "東京站" }])));
    });
    expect(screen.queryByRole("option", { name: /東京站/ })).toBeNull();
    fireEvent.click(screen.getByRole("option", { name: /大阪站/ }));
    view.rerender(<PlacePicker {...props} value="大阪" selectionContextKey="another-day" />);
    await act(async () => { failDetails(new Error("Old failed response")); });
    expect(fetchMock.mock.calls[2][1].signal.aborted).toBe(true);
    expect(screen.queryByRole("alert")).toBeNull();
    expect(onSelect).not.toHaveBeenCalled();
  });
});
