import { useEffect } from "react";
import { act, cleanup, render, screen, waitFor } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { SavedItemsProvider, useSavedItems } from "./saved-items-provider";
const mock = vi.hoisted(() => ({ api: vi.fn(), session: { status: "authenticated", user: { id: "user-a" }, sessionIdentity: {} as object | null } }));
vi.mock("@/lib/api", async (original) => ({ ...await original<typeof import("@/lib/api")>(), api: mock.api }));
vi.mock("./header-session", () => ({ useHeaderSession: () => mock.session }));
type Value = ReturnType<typeof useSavedItems>;
function Probe({ report }: { report: (value: Value) => void }) { const value = useSavedItems(); useEffect(() => report(value), [value, report]); return <p>{value.status}:{value.isSaved("hotspot", "one") ? "saved" : "empty"}</p>; }
function setup() { const report = vi.fn<(value: Value) => void>(); const view = render(<SavedItemsProvider><Probe report={report} /></SavedItemsProvider>); return { ...view, current: () => report.mock.calls.at(-1)![0], update: () => view.rerender(<SavedItemsProvider><Probe report={report} /></SavedItemsProvider>) }; }
async function ready(view: ReturnType<typeof setup>) { await waitFor(() => expect(view.current().status).toBe("authenticated")); }
beforeEach(() => { mock.session = { status: "authenticated", user: { id: "user-a" }, sessionIdentity: {} }; mock.api.mockReset(); mock.api.mockImplementation(async (path: string, init?: RequestInit) => path === "/saved-items/states" ? { items: JSON.parse(String(init?.body)).keys.map((key: string) => ({ key, saved: false, collection_ids: [] })) } : { items: [] }); });
afterEach(cleanup);
describe("saved state account and request boundaries", () => {
  it("coalesces visible state probes into batches of 100 beyond the legacy bootstrap", async () => {
    const view = setup(); await ready(view);
    await act(async () => { await Promise.all(Array.from({ length: 205 }, (_, index) => view.current().ensureStates([`hotspot:${index}`]))); });
    const calls = mock.api.mock.calls.filter(([path]) => path === "/saved-items/states");
    expect(calls.map(([, init]) => JSON.parse(init.body).keys.length)).toEqual([100, 100, 5]);
    expect(view.current().state("hotspot:204")).toEqual({ key: "hotspot:204", saved: false, collection_ids: [] });
    await act(async () => { await view.current().ensureStates(["hotspot:204"]); });
    expect(mock.api.mock.calls.filter(([path]) => path === "/saved-items/states")).toHaveLength(3);
    expect(view.current().revision).toBe(0); // Reads do not invalidate collection pages.
  });
  it("hides prior saves synchronously and aborts a pending mutation when login changes", async () => {
    mock.api.mockResolvedValueOnce({ items: [{ type: "hotspot", id: "one" }] });
    const view = setup(); await ready(view); expect(screen.getByText("authenticated:saved")).toBeTruthy();
    let finish!: (value: unknown) => void; let signal!: AbortSignal;
    mock.api.mockImplementation((path: string, init?: RequestInit) => init?.method === "PUT" ? new Promise((resolve) => { finish = resolve; signal = init.signal as AbortSignal; }) : Promise.resolve({ items: [] }));
    let mutation!: Promise<unknown>; act(() => { mutation = view.current().setSaved("hotspot", "two", true).catch((error: Error) => error.name); });
    await waitFor(() => expect(finish).toBeTypeOf("function"));
    expect(mock.api.mock.calls.some(([path]) => path === "/saved-items/hotspot/two?expected_user_id=user-a")).toBe(true);
    mock.session = { ...mock.session, user: { id: "user-b" }, sessionIdentity: {} }; view.update();
    expect(screen.queryByText("authenticated:saved")).toBeNull(); expect(signal.aborted).toBe(true);
    await act(async () => { finish({ collection_ids: ["a-private-list"] }); expect(await mutation).toBe("AbortError"); });
    await ready(view); expect(view.current().state("hotspot:two")).toBeUndefined(); expect(view.current().isSaved("hotspot", "one")).toBe(false);
  });
  it("does not let a late state read overwrite a newer explicit save", async () => {
    const view = setup(); await ready(view); let finish!: (value: unknown) => void;
    mock.api.mockImplementation((path: string) => path === "/saved-items/states" ? new Promise((resolve) => { finish = resolve; }) : Promise.resolve({ collection_ids: [] }));
    let stateRequest!: Promise<void>; act(() => { stateRequest = view.current().ensureStates(["hotspot:one"]); });
    await waitFor(() => expect(finish).toBeTypeOf("function"));
    await act(async () => { await view.current().setSaved("hotspot", "one", true); });
    await act(async () => { finish({ items: [{ key: "hotspot:one", saved: false, collection_ids: [] }] }); await stateRequest; });
    expect(view.current().isSaved("hotspot", "one")).toBe(true); expect(view.current().revision).toBe(1);
  });
  it("ignores an older state probe after a forced membership refresh finishes first", async () => {
    const view = setup(); await ready(view); let finishOld!: (value: unknown) => void;
    mock.api.mockImplementationOnce(() => new Promise((resolve) => { finishOld = resolve; }));
    let old!: Promise<void>; act(() => { old = view.current().ensureStates(["hotspot:one"]); });
    await waitFor(() => expect(finishOld).toBeTypeOf("function"));
    mock.api.mockResolvedValueOnce({ items: [{ key: "hotspot:one", saved: true, collection_ids: ["new-list"] }] });
    await act(async () => { await view.current().ensureStates(["hotspot:one"], true); });
    await act(async () => { finishOld({ items: [{ key: "hotspot:one", saved: true, collection_ids: [] }] }); await old; });
    expect(view.current().state("hotspot:one")?.collection_ids).toEqual(["new-list"]);
  });
  it("keeps state on a same-login profile update and can retry a failed exact probe", async () => {
    const view = setup(); await ready(view); await act(async () => { await view.current().setSaved("hotspot", "one", true); });
    mock.session = { ...mock.session, user: { ...mock.session.user } }; view.update();
    expect(screen.getByText("authenticated:saved")).toBeTruthy();
    expect(mock.api.mock.calls.filter(([path]) => path === "/saved-items?limit=100")).toHaveLength(1);
    mock.api.mockRejectedValueOnce(new Error("Network"));
    await act(async () => { await expect(view.current().ensureStates(["guide:other"])).rejects.toThrow("Network"); });
    await act(async () => { await view.current().ensureStates(["guide:other"]); });
    expect(view.current().state("guide:other")?.saved).toBe(false);
  });
});
