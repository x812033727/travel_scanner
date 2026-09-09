import { act, cleanup, render, screen, waitFor } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { useDiscoveryResource, useDiscoveryStatus } from "@/lib/discovery";
const mock = vi.hoisted(() => ({ api: vi.fn(), identity: null as object | null, clock: 1_000_000 }));
vi.mock("@/lib/api", async (original) => ({ ...await original<typeof import("@/lib/api")>(), api: mock.api }));
vi.mock("@/components/header-session", () => ({ useHeaderSession: () => ({ sessionIdentity: mock.identity }) }));
function Status({ label }: { label: string }) { const status = useDiscoveryStatus(); return <p>{label}:{String(status.enabled)}:{String(status.loading)}</p>; }
function Resource({ path }: { path: string }) { const data = useDiscoveryResource<{ value: string }>(path); return <p>{data.data?.value || "waiting"}</p>; }
beforeEach(() => { mock.api.mockReset(); mock.clock += 60_000; mock.identity = null; vi.spyOn(Date, "now").mockImplementation(() => mock.clock); });
afterEach(() => { cleanup(); vi.restoreAllMocks(); });
describe("discovery account and rollout boundaries", () => {
  it("deduplicates public status reads between simultaneous consumers", async () => {
    mock.api.mockResolvedValue({ enabled: true });
    render(<><Status label="one" /><Status label="two" /></>);
    await screen.findByText("one:true:false"); expect(screen.getByText("two:true:false")).toBeTruthy();
    expect(mock.api).toHaveBeenCalledTimes(1);
  });
  it("fails closed for partial legacy fixtures rather than treating an object as enabled", async () => {
    mock.api.mockResolvedValue({ items: [] }); render(<Status label="partial" />);
    expect(await screen.findByText("partial:false:false")).toBeTruthy();
  });
  it("refreshes on focus even when the original subscriber has unmounted", async () => {
    mock.api.mockResolvedValue({ enabled: true });
    const view = render(<><Status label="one" /><Status label="two" /></>);
    await screen.findByText("two:true:false");
    view.rerender(<Status label="two" />); mock.clock += 60_000; mock.api.mockResolvedValue({ enabled: false });
    await act(async () => window.dispatchEvent(new Event("focus")));
    expect(await screen.findByText("two:false:false")).toBeTruthy();
  });
  it("aborts and hides an old account's late private response", async () => {
    let finish!: (value: unknown) => void;
    let signal!: AbortSignal;
    mock.identity = {};
    mock.api.mockImplementationOnce((_path: string, options: RequestInit) => { signal = options.signal as AbortSignal; return new Promise((resolve) => { finish = resolve; }); });
    const view = render(<Resource path="/discovery/preferences" />);
    await waitFor(() => expect(finish).toBeTypeOf("function"));
    mock.identity = {}; mock.api.mockResolvedValue({ value: "new reader" }); view.rerender(<Resource path="/discovery/preferences" />);
    expect(signal.aborted).toBe(true); await act(async () => finish({ value: "previous private preferences" }));
    expect(await screen.findByText("new reader")).toBeTruthy(); expect(screen.queryByText("previous private preferences")).toBeNull();
  });
});
